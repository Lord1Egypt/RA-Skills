"""
Multi-camera Physical Conflict Detector (Continuous Mode)
Architecture: N RTSP streams -> shared YOLO person pre-filter -> shared LLM
conflict analysis -> per-event alert push + per-camera video clip -> keep
monitoring (no exit on event).

Execution Mode:
  Runs in a single process and never exits on event detection. For every camera
  in `config.json -> cameras[]` (or the single `--rtsp_url` passed on the CLI),
  a dedicated worker thread polls frames, runs the YOLO person filter, and on
  >= min_persons forwards a multi-frame batch to the Kami LLM. When the LLM
  confirms a conflict, the worker saves a per-camera video clip, pushes an
  alert (stdout / inbox file / Feishu / Discord / Telegram) tagged with the
  camera name, and immediately resumes monitoring. The process only exits on
  KeyboardInterrupt or fatal startup error.

Exit Codes:
  0 - Normal exit (Ctrl+C, all streams ended, no fatal error)
  1 - Runtime error (model not found, missing API key, no camera configured)

Threading Model:
  - One FrameGrabber thread per camera: continuously reads its RTSP stream and
    maintains a private ring buffer + latest frame.
  - One detect-worker thread per camera: YOLO pre-filter + multi-frame
    collection + LLM analysis + alert push.
  - YOLO ONNX inference is serialized across cameras via a single
    inference_lock so the shared session stays thread-safe.
  - Main thread: starts workers, supervises shutdown.
"""

import cv2
import numpy as np
import onnxruntime as ort
import time
import os
import sys
import json
import logging
import argparse
import threading
import base64
import requests
from collections import deque
from datetime import datetime

# ==================== Exit Codes ====================
# Continuous mode: a detected conflict does NOT terminate the process; it only
# pushes an alert. Exit codes are restricted to normal shutdown / fatal error.
EXIT_NORMAL = 0
EXIT_ERROR = 1

# ==================== i18n: Push Notification Labels ====================
# Labels rendered in Feishu/Discord/Telegram alerts. The channel decides the
# language: Feishu uses Chinese, Discord/Telegram use English. The LLM-
# generated `description` text is NOT translated here (it comes from the
# remote API).
I18N = {
    "zh": {
        "title": "\U0001f94a 肢体冲突告警",
        "alert_type": "告警类型",
        "camera": "摄像头",
        "description": "描述",
        "time": "时间",
        "clip_duration": "视频时长",
        "video_clip": "视频片段",
        "snapshot": "冲突快照",
        "empty": "(无)",
    },
    "en": {
        "title": "\U0001f94a Physical Conflict Alert",
        "alert_type": "Alert Type",
        "camera": "Camera",
        "description": "Description",
        "time": "Time",
        "clip_duration": "Clip Duration",
        "video_clip": "Video Clip",
        "snapshot": "Conflict Snapshot",
        "empty": "(none)",
    },
}

# Target pixel size for the longest side of saved conflict snapshot images.
# Ensures consistent display dimensions across all push notification channels.
SNAPSHOT_LONG_SIDE = 640

# ==================== YOLO-World Class Vocabulary ====================
# YOLOv8-World is an open-vocabulary detector. BOTH the ONNX export step
# (model.set_classes) AND the runtime parser (PersonDetector) must use the
# same class list, otherwise the ONNX output head dimension won't match the
# parser's indices and `person_count` will be meaningless.
YOLO_CLASS_NAMES = [
    "parcel", "package", "delivery box", "person",
    "Cardboard box", "Packaging Box", "backpack", "handbag", "suitcase",
]

# ==================== Logging ====================
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, "conflict_detector.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger("conflict_detector")


def video_frames_to_base64(frames):
    """Convert a list of frames to base64-encoded JPEG strings."""
    base64_frames = []
    for frame in frames:
        _, encoded_frame = cv2.imencode('.jpg', frame)
        base64_frame = base64.b64encode(encoded_frame).decode('utf-8')
        base64_frames.append(base64_frame)
    logger.info(f"Extracted {len(base64_frames)} frames to base64")
    return base64_frames


# ==================== YOLO Utility Functions ====================
def letterbox(img, new_shape=320, color=(114, 114, 114)):
    shape = img.shape[:2]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    dw /= 2
    dh /= 2
    if shape[::-1] != new_unpad:
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return img, r, (dw, dh)


def parse_output(output, conf_threshold=0.25, class_names=None):
    if len(output.shape) == 3:
        output = output.transpose(0, 2, 1)[0]
    else:
        output = output[0]
    boxes, scores, class_ids = [], [], []
    num_classes = len(class_names) if class_names else output.shape[1] - 4
    for pred in output:
        cls_scores = pred[4 : 4 + num_classes]
        max_score = np.max(cls_scores)
        if max_score > conf_threshold:
            boxes.append(pred[:4])
            scores.append(max_score)
            class_ids.append(np.argmax(cls_scores))
    return np.array(boxes), np.array(scores), np.array(class_ids)


def xywh2xyxy(x):
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2
    return y


def scale_boxes(boxes, orig_shape, ratio, pad):
    if len(boxes) == 0:
        return boxes
    boxes = xywh2xyxy(boxes)
    boxes[:, [0, 2]] -= pad[0]
    boxes[:, [1, 3]] -= pad[1]
    boxes /= ratio
    boxes[:, [0, 2]] = np.clip(boxes[:, [0, 2]], 0, orig_shape[1])
    boxes[:, [1, 3]] = np.clip(boxes[:, [1, 3]], 0, orig_shape[0])
    return boxes.astype(int)


def nms(boxes, scores, iou_threshold):
    if len(boxes) == 0:
        return []
    indices = cv2.dnn.NMSBoxes(boxes.tolist(), scores.tolist(), 0.0, iou_threshold)
    return indices.flatten() if len(indices) > 0 else []


# ==================== Frame Grabber Thread ====================
class FrameGrabber:
    """Dedicated thread that continuously reads RTSP stream, maintains a ring buffer and keeps only the latest frame for inference."""

    def __init__(self, rtsp_url: str, buffer_seconds: int = 30, fps: int = 15):
        self.cap = cv2.VideoCapture(rtsp_url)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open video source: {rtsp_url}")

        self.fps = fps
        self.buffer_size = buffer_seconds * fps
        self.is_local_file = not rtsp_url.startswith(("rtsp://", "http://", "https://"))
        self.ring_buffer = deque(maxlen=self.buffer_size)
        self.latest_frame = None
        self.lock = threading.Lock()
        self.running = True
        self.frame_count = 0

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        mode_str = "local file (throttled)" if self.is_local_file else "live stream"
        logger.info(f"Frame grabber started, mode: {mode_str}, resolution: {self.width}x{self.height}, buffer: {buffer_seconds}s")

    def _run(self):
        frame_interval = 1.0 / self.fps
        while self.running:
            t0 = time.time()
            ret, frame = self.cap.read()
            if not ret:
                if self.is_local_file:
                    logger.info("Local video playback finished")
                    self.running = False
                    break
                logger.warning("Frame read failed, attempting reconnect...")
                time.sleep(1)
                continue
            with self.lock:
                self.latest_frame = frame.copy()
                self.ring_buffer.append((time.time(), frame.copy()))
                self.frame_count += 1
            if self.is_local_file:
                elapsed = time.time() - t0
                if elapsed < frame_interval:
                    time.sleep(frame_interval - elapsed)

    def get_latest_frame(self):
        """Get latest frame (non-blocking), returns (frame, frame_count) or (None, 0)."""
        with self.lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy(), self.frame_count
            return None, 0

    def get_buffer_snapshot(self):
        """Get ring buffer snapshot for video clip export."""
        with self.lock:
            return list(self.ring_buffer)

    def stop(self):
        self.running = False
        self.thread.join(timeout=3)
        self.cap.release()
        logger.info("Frame grabber stopped")


# ==================== YOLO Person Detector ====================
class PersonDetector:
    """Uses YOLO to count persons in frame as a pre-filter for LLM analysis."""

    def __init__(self, model_path: str, input_size: int = 320, conf_threshold: float = 0.25):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        self.session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name
        self.input_size = input_size
        self.conf_threshold = conf_threshold
        self.iou_threshold = 0.45
        self.class_names = list(YOLO_CLASS_NAMES)
        self.person_idx = self.class_names.index("person")
        logger.info(f"YOLO person detector loaded: {model_path}")

    def count_persons(self, frame: np.ndarray) -> int:
        """Return the number of persons detected in the frame."""
        orig_shape = frame.shape[:2]
        img, ratio, pad = letterbox(frame, self.input_size)
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img).astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)

        outputs = self.session.run(None, {self.input_name: img})
        if len(outputs) == 0:
            return 0

        boxes, scores, class_ids = parse_output(outputs[0], self.conf_threshold, self.class_names)
        if len(boxes) == 0:
            return 0

        boxes_scaled = scale_boxes(boxes, orig_shape, ratio, pad)
        keep = nms(boxes_scaled, scores, self.iou_threshold)

        person_count = sum(1 for i in keep if class_ids[i] == self.person_idx)
        return person_count


# ==================== LLM Conflict Analyzer ====================
class ConflictAnalyzer:
    """Calls multimodal LLM API to determine whether physical conflict exists based on multiple frames."""

    def __init__(self, kami_api_key: str):
        self.api_key = kami_api_key
        logger.info("Conflict analyzer initialized")

    def analyze(self, frames: list[np.ndarray]) -> dict:
        """
        Analyze frames for conflict.
        Returns: {"conflict": bool, "description": str}
        """
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key,
        }
        import requests
        try:
            json_x = {
                "detectType": "VIOLENCE",
                "detectSubType": "",
                "skillId": "SK_BODY_CONFLICT",
                "prompt": "",
                "imageFile": video_frames_to_base64(frames),
                "videoFile": ""
            }

            response = requests.post('https://kamiclaw-skill-api.kamihome.com/v1/detect', headers=headers, json=json_x)
            logger.info(f"API response: {response.text}")

            response_data = json.loads(response.text)
            result_str = response_data["data"]["result"]

            result = self._extract_json(result_str)
            logger.info(f"LLM analysis result: {result}")
            return result
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return {"conflict": False, "description": f"Analysis failed: {e}"}

    @staticmethod
    def _extract_json(text: str) -> dict:
        """Extract JSON from LLM response text."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        import re
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        match = re.search(r"\{.*?\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        return {"conflict": False, "description": f"Cannot parse model output: {text}"}


# ==================== Alert Delivery: Inbox file + Feishu push ====================
def append_inbox(inbox_path: str, alert: dict):
    """Append alert JSON line to inbox file for the heartbeat task to consume.

    The heartbeat task defined in space/HEARTBEAT.md polls this file and pushes
    unreported alarms into the chat window proactively, independent of the
    OpenClaw stdout-exit channel.
    """
    try:
        os.makedirs(os.path.dirname(inbox_path), exist_ok=True)
        with open(inbox_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(alert, ensure_ascii=False) + "\n")
        logger.info(f"Alert appended to inbox: {inbox_path}")
    except Exception as e:
        logger.error(f"Failed to append inbox {inbox_path}: {e}")


def _feishu_sign(secret: str, timestamp: int) -> str:
    """Generate Feishu webhook signature (HMAC-SHA256, base64)."""
    import hmac
    import hashlib
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    return base64.b64encode(hmac_code).decode("utf-8")


def _format_ts(ts: str) -> str:
    """Format ISO 8601 timestamp string to 'YYYY-MM-DD HH:MM:SS'.

    Returns empty string for empty input; returns the original string if it
    cannot be parsed. Used to render compact timestamps inside push cards.
    """
    if not ts:
        return ""
    try:
        return datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts


def _upload_image_to_imghost(local_path: str) -> str:
    """Upload a local image to the sm.ms anonymous image host.

    Returns the public https URL on success, or '' on any failure. sm.ms
    accepts anonymous multipart uploads (no API key required); per-IP daily
    quota applies. Used by the Feishu push as a fallback to obtain a
    clickable image URL when no Feishu app credentials are configured.
    """
    if not local_path or not os.path.isfile(local_path):
        return ""
    try:
        with open(local_path, "rb") as f:
            files = {"smfile": (os.path.basename(local_path), f.read(), "image/jpeg")}
        resp = requests.post(
            "https://sm.ms/api/v2/upload",
            files=files,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("success") and data.get("data", {}).get("url"):
            return data["data"]["url"]
        # sm.ms returns image_repeated when the same image was uploaded before
        if data.get("code") == "image_repeated" and data.get("images"):
            return data["images"]
        logger.warning(f"sm.ms upload non-success response: {data}")
        return ""
    except Exception as e:
        logger.error(f"Image host upload failed ({local_path}): {e}")
        return ""


def _feishu_get_tenant_token(app_id: str, app_secret: str) -> str:
    """Obtain a tenant_access_token from Feishu OpenAPI.

    Token is valid for ~2 hours. We fetch a fresh one on each push because
    alarm frequency is low and caching adds complexity.
    """
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    body = {"app_id": app_id, "app_secret": app_secret}
    resp = requests.post(url, json=body, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"tenant_access_token error: {data}")
    return data["tenant_access_token"]


def _feishu_upload_image(app_id: str, app_secret: str, local_path: str) -> str:
    """Upload a local image to Feishu via OpenAPI and return the image_key.

    Requires a self-built Feishu app with im:resource permission. The returned
    image_key can be used in interactive card `img` elements to render the image
    inline.
    """
    if not local_path or not os.path.isfile(local_path):
        return ""
    try:
        token = _feishu_get_tenant_token(app_id, app_secret)
        url = "https://open.feishu.cn/open-apis/im/v1/images"
        with open(local_path, "rb") as f:
            file_bytes = f.read()
        files = {"image": (os.path.basename(local_path), file_bytes, "image/jpeg")}
        data = {"image_type": "message"}
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.post(url, headers=headers, data=data, files=files, timeout=15)
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") != 0:
            logger.warning(f"Feishu image upload API error: {result}")
            return ""
        return result.get("data", {}).get("image_key", "")
    except Exception as e:
        logger.error(f"Feishu image upload failed ({local_path}): {e}")
        return ""


def send_feishu(webhook_url: str, alert: dict, secret: str = "",
               app_id: str = "", app_secret: str = ""):
    """Push alarm to a Feishu custom bot webhook as an interactive card.

    No-op if webhook_url is empty. Failures are logged but do not affect the
    main detection flow (stdout/exit-10 channel still fires).

    Image rendering strategy for the conflict snapshot:
      1. If app_id + app_secret are provided, upload the snapshot to Feishu
         via OpenAPI and embed it inline using the img element (best UX).
      2. Otherwise, upload to sm.ms image host and display a clickable URL.
      3. If both fail, show the local file path as plain text.
    """
    if not webhook_url:
        return
    import urllib.request
    import urllib.error
    t = I18N["zh"]  # Feishu channel always uses Chinese labels
    try:
        timestamp = int(time.time())
        snapshot_local = alert.get("snapshot_image", "")

        # --- Attempt to get a renderable image_key ---
        image_key = ""
        snapshot_url = ""
        if snapshot_local and app_id and app_secret:
            image_key = _feishu_upload_image(app_id, app_secret, snapshot_local)
        # Fallback: public image host URL
        if not image_key and snapshot_local:
            snapshot_url = _upload_image_to_imghost(snapshot_local)

        if image_key:
            snap_md = "(\u89c1\u4e0b\u65b9\u56fe\u7247)"  # "(见下方图片)"
        elif snapshot_url:
            snap_md = f"[\u67e5\u770b\u51b2\u7a81\u5feb\u7167]({snapshot_url})"
        elif snapshot_local:
            snap_md = f"`{snapshot_local}`"
        else:
            snap_md = "-"

        content_md = (
            f"**{t['alert_type']}**: {alert.get('alert', '')}\n"
            f"**{t['camera']}**: {alert.get('camera', '') or t['empty']}\n"
            f"**{t['description']}**: {alert.get('description', '')}\n"
            f"**{t['time']}**: {_format_ts(alert.get('timestamp', ''))}\n"
            f"**{t['clip_duration']}**: {alert.get('clip_duration', '')}\n"
            f"**{t['video_clip']}**: `{alert.get('video_clip', '')}`\n"
            f"**{t['snapshot']}**: {snap_md}"
        )
        elements = [
            {"tag": "div", "text": {"tag": "lark_md", "content": content_md}},
        ]
        if image_key:
            elements.append({
                "tag": "img",
                "img_key": image_key,
                "alt": {"tag": "plain_text", "content": t["snapshot"]},
            })
        elements.append({"tag": "hr"})
        elements.append({"tag": "note", "elements": [
            {"tag": "plain_text", "content": alert.get("message", "")}
        ]})

        body = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": t["title"]},
                    "template": "red",
                },
                "elements": elements,
            },
        }
        if secret:
            body["timestamp"] = str(timestamp)
            body["sign"] = _feishu_sign(secret, timestamp)
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            webhook_url, data=data,
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            resp_body = resp.read().decode("utf-8", errors="replace")
            logger.info(f"Feishu push ok ({resp.status}): {resp_body[:200]}")
    except Exception as e:
        logger.error(f"Feishu push failed: {e}")


def send_discord(webhook_url: str, alert: dict, proxy: str = ""):
    """Push alarm to a Discord channel via webhook embed.

    No-op if webhook_url is empty. Failures are logged but do not affect the
    main detection flow (stdout/exit-10 channel still fires).

    Uses ``requests`` (already a project dependency) instead of ``urllib`` for
    robust HTTPS proxy support and proper User-Agent handling. When a local
    snapshot file exists, it is attached via multipart so the embed renders
    the image inline (no public URL required).
    """
    if not webhook_url:
        return
    t = I18N["en"]  # Discord channel always uses English labels
    try:
        alert_type = alert.get("alert", "")
        camera = alert.get("camera", "") or "-"
        timestamp = _format_ts(alert.get("timestamp", ""))
        description = alert.get("description", "")
        video_clip = alert.get("video_clip", "")
        clip_duration = alert.get("clip_duration", "")
        snapshot_image = alert.get("snapshot_image", "")
        message = alert.get("message", "")
        embed = {
            "title": t["title"],
            "color": 15158332,  # 0xE74C3C red
            "fields": [
                {"name": t["alert_type"], "value": alert_type or "-", "inline": True},
                {"name": t["camera"], "value": camera, "inline": True},
                {"name": t["time"], "value": timestamp or "-", "inline": True},
                {"name": t["description"], "value": description or t["empty"], "inline": False},
                {"name": t["clip_duration"], "value": clip_duration or "-", "inline": True},
                {"name": t["video_clip"], "value": f"`{video_clip}`" if video_clip else "-", "inline": False},
            ],
            "footer": {"text": message},
        }
        headers = {"User-Agent": "KamiConflictDetector/2.0"}
        proxies = {"https": proxy, "http": proxy} if proxy else None
        if snapshot_image and os.path.isfile(snapshot_image):
            filename = os.path.basename(snapshot_image)
            embed["image"] = {"url": f"attachment://{filename}"}
            payload = {"embeds": [embed]}
            with open(snapshot_image, "rb") as f:
                file_bytes = f.read()
            files = {"files[0]": (filename, file_bytes, "image/jpeg")}
            data = {"payload_json": json.dumps(payload, ensure_ascii=False)}
            resp = requests.post(webhook_url, data=data, files=files,
                                 headers=headers, proxies=proxies, timeout=10)
        else:
            embed["fields"].append({
                "name": t["snapshot"],
                "value": f"`{snapshot_image}`" if snapshot_image else "-",
                "inline": False,
            })
            payload = {"embeds": [embed]}
            headers["Content-Type"] = "application/json; charset=utf-8"
            resp = requests.post(webhook_url, json=payload, headers=headers,
                                 proxies=proxies, timeout=5)
        resp.raise_for_status()
        logger.info(f"Discord push ok ({resp.status_code}): {resp.text[:200]}")
    except Exception as e:
        logger.error(f"Discord push failed: {e}")


def send_telegram(bot_token: str, chat_id: str, alert: dict, proxy: str = ""):
    """Push alarm to a Telegram chat via Bot API.

    No-op if bot_token or chat_id is empty. Failures are logged but do not
    affect the main detection flow (stdout/exit-10 channel still fires).

    Uses HTML parse_mode (more forgiving than Markdown with special chars).
    When a local snapshot file exists, the alert is delivered via sendPhoto
    with the formatted text as the caption, so the image renders inline.
    """
    if not bot_token or not chat_id:
        return
    t = I18N["en"]  # Telegram channel always uses English labels
    try:
        from html import escape as html_escape
        alert_type = html_escape(alert.get("alert", "") or "-")
        camera = html_escape(alert.get("camera", "") or "-")
        timestamp = html_escape(_format_ts(alert.get("timestamp", "")) or "-")
        description = html_escape(alert.get("description", "") or t["empty"])
        video_clip = html_escape(alert.get("video_clip", "") or "-")
        clip_duration = html_escape(alert.get("clip_duration", "") or "-")
        snapshot_image = alert.get("snapshot_image", "") or ""
        message = html_escape(alert.get("message", "") or "")
        text = (
            f"<b>{html_escape(t['title'])}</b>\n\n"
            f"<b>{html_escape(t['alert_type'])}</b>: {alert_type}\n"
            f"<b>{html_escape(t['camera'])}</b>: {camera}\n"
            f"<b>{html_escape(t['description'])}</b>: {description}\n"
            f"<b>{html_escape(t['time'])}</b>: {timestamp}\n"
            f"<b>{html_escape(t['clip_duration'])}</b>: {clip_duration}\n"
            f"<b>{html_escape(t['video_clip'])}</b>: <code>{video_clip}</code>\n\n"
            f"<i>{message}</i>"
        )
        headers = {"User-Agent": "KamiConflictDetector/2.0"}
        proxies = {"https": proxy, "http": proxy} if proxy else None
        if snapshot_image and os.path.isfile(snapshot_image):
            url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
            with open(snapshot_image, "rb") as f:
                file_bytes = f.read()
            files = {"photo": (os.path.basename(snapshot_image), file_bytes, "image/jpeg")}
            data = {
                "chat_id": chat_id,
                "caption": text,
                "parse_mode": "HTML",
            }
            resp = requests.post(url, data=data, files=files,
                                 headers=headers, proxies=proxies, timeout=10)
        else:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            text_with_path = (
                text
                + f"\n<b>{html_escape(t['snapshot'])}</b>: "
                + f"<code>{html_escape(snapshot_image or '-')}</code>"
            )
            body = {
                "chat_id": chat_id,
                "text": text_with_path,
                "parse_mode": "HTML",
            }
            resp = requests.post(url, json=body, headers=headers,
                                 proxies=proxies, timeout=5)
        resp.raise_for_status()
        logger.info(f"Telegram push ok ({resp.status_code}): {resp.text[:200]}")
    except Exception as e:
        logger.error(f"Telegram push failed: {e}")


def save_conflict_snapshot(frame: np.ndarray, output_dir: str,
                           prefix: str = "snapshot") -> str:
    """Save a single frame as a JPEG snapshot, resized so its longest side
    equals SNAPSHOT_LONG_SIDE while keeping the original aspect ratio.

    Used to embed a single representative frame of the conflict moment in
    push notifications (Feishu / Discord / Telegram). Returns the saved
    file path, or '' on failure.
    """
    if frame is None:
        return ""
    try:
        os.makedirs(output_dir, exist_ok=True)
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(output_dir, f"{prefix}_{timestamp_str}.jpg")
        h, w = frame.shape[:2]
        if max(h, w) > 0:
            scale = SNAPSHOT_LONG_SIDE / max(h, w)
            new_w = max(1, int(w * scale))
            new_h = max(1, int(h * scale))
            interp = cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR
            resized = cv2.resize(frame, (new_w, new_h), interpolation=interp)
        else:
            resized = frame
        cv2.imwrite(filepath, resized, [cv2.IMWRITE_JPEG_QUALITY, 85])
        logger.info(
            f"Conflict snapshot saved: {filepath} ({resized.shape[1]}x{resized.shape[0]})"
        )
        return filepath
    except Exception as e:
        logger.error(f"Failed to save conflict snapshot: {e}")
        return ""


# ==================== Video Clip Export ====================
def save_video_clip(frames_with_ts: list, output_dir: str, fps: int = 15,
                    prefix: str = "conflict") -> str:
    """
    Save frame list as MP4 video clip.
    frames_with_ts: [(timestamp, frame), ...]
    prefix: filename prefix; pass `conflict_<camera_name>` to tag the file with
            the originating camera in multi-camera setups.
    Returns the saved file path.
    """
    if not frames_with_ts:
        # Defensive log: previously this returned silently, which made it
        # very hard to tell why no .mp4 appeared on disk. Most common root
        # cause is that the ring buffer had already dropped the target
        # clip window by the time we got here (e.g. LLM call took longer
        # than buffer_seconds).
        logger.warning(
            "Video clip not saved: frames list is empty "
            "(target window may have been dropped by the ring buffer)"
        )
        return ""

    os.makedirs(output_dir, exist_ok=True)
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp_str}.mp4"
    filepath = os.path.join(output_dir, filename)

    h, w = frames_with_ts[0][1].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(filepath, fourcc, fps, (w, h))

    for _, frame in frames_with_ts:
        writer.write(frame)
    writer.release()

    logger.info(f"Video clip saved: {filepath} ({len(frames_with_ts)} frames, {len(frames_with_ts)/fps:.1f}s)")
    return filepath


# ==================== Model Auto-Preparation ====================
# The pre-exported YOLOv8s-World ONNX model is published as a zip bundle. The
# zip extracts to a folder named ``kami-conflict-detection-model/`` containing
# one or more .onnx files (currently yolov8s-worldv2.onnx). We move the .onnx
# into the skill directory and remove the unpacked folder afterwards.
MODEL_URL = "https://publicfiles.xiaoyi.com/kami-conflict-detection-model.zip"


def ensure_yolo_model(onnx_path: str) -> str:
    """Ensure the YOLO ONNX model exists at ``onnx_path``.

    If the ONNX file is missing, this will:
      1) download a pre-exported model bundle (zip) from MODEL_URL,
      2) extract it next to the target onnx path,
      3) move the bundled .onnx files into the model directory,
      4) delete the extracted bundle folder and the downloaded zip.

    No .pt download / ultralytics conversion is needed any more.

    Returns the absolute path to the existing/freshly-downloaded .onnx file.
    """
    onnx_path = os.path.abspath(onnx_path)
    if os.path.isfile(onnx_path):
        logger.info(f"YOLO ONNX model found: {onnx_path}")
        return onnx_path

    model_dir = os.path.dirname(onnx_path) or script_dir
    os.makedirs(model_dir, exist_ok=True)

    import urllib.request
    import zipfile
    import shutil

    zip_path = os.path.join(model_dir, "kami-conflict-detection-model.zip")
    extract_dir = os.path.join(model_dir, "kami-conflict-detection-model")

    # Step 1: download zip
    logger.info(f"YOLO ONNX not found, downloading model bundle from {MODEL_URL} ...")
    try:
        urllib.request.urlretrieve(MODEL_URL, zip_path)
    except Exception as e:
        logger.error(f"Failed to download {MODEL_URL}: {e}")
        raise
    if not os.path.isfile(zip_path):
        raise RuntimeError(f"Downloaded zip not found: {zip_path}")
    logger.info(f"Downloaded model bundle: {zip_path} ({os.path.getsize(zip_path)/1e6:.1f} MB)")

    # Step 2: extract
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(model_dir)
    except Exception as e:
        logger.error(f"Failed to unzip {zip_path}: {e}")
        raise

    # Step 3: locate and move .onnx files into model_dir.
    # The bundle should extract into ``kami-conflict-detection-model/`` but
    # we also accept a flat layout where .onnx files sit directly next to the
    # zip (defensive).
    moved = []
    if os.path.isdir(extract_dir):
        for name in os.listdir(extract_dir):
            if name.endswith(".onnx"):
                src = os.path.join(extract_dir, name)
                dst = os.path.join(model_dir, name)
                if os.path.abspath(src) != os.path.abspath(dst):
                    shutil.move(src, dst)
                moved.append(dst)
        # Step 4: drop the extracted bundle folder regardless of what was inside.
        shutil.rmtree(extract_dir, ignore_errors=True)

    # Cleanup the zip file as well.
    try:
        os.remove(zip_path)
    except Exception:
        pass

    if not os.path.isfile(onnx_path):
        # Defensive: try common alternative name once.
        alt = os.path.join(model_dir, "yolov8s-worldv2.onnx")
        if os.path.isfile(alt) and alt != onnx_path:
            shutil.move(alt, onnx_path)
    if not os.path.isfile(onnx_path):
        raise RuntimeError(
            f"Model bundle extracted but expected file not found: {onnx_path}. "
            f"Moved files: {moved}"
        )

    logger.info(f"ONNX model ready: {onnx_path} ({os.path.getsize(onnx_path)/1e6:.1f} MB)")
    return onnx_path


# ==================== Argument Parsing ====================
def parse_args():
    parser = argparse.ArgumentParser(description="Multi-camera physical conflict detector (continuous mode)")
    parser.add_argument("--rtsp_url", type=str, default="",
                        help="Single-camera CLI override: RTSP URL or local video file path. "
                             "When set, takes priority over the cameras[] array in config.json. "
                             "For multi-camera setups, configure cameras[] in config.json instead.")
    parser.add_argument("--camera_name", type=str, default="",
                        help="Optional camera name used together with --rtsp_url. Defaults to 'camera_0' if omitted.")
    parser.add_argument("--kami_api_key", type=str, default="",
                        help="Kami API Key (or set in config.json)")
    parser.add_argument("--yolo_model", type=str,
                        default=os.path.join(script_dir, "yolov8s-worldv2.onnx"),
                        help="YOLO model file path")
    parser.add_argument("--conf_threshold", type=float, default=0.25, help="YOLO confidence threshold")
    parser.add_argument("--min_persons", type=int, default=2, help="Minimum person count to trigger LLM analysis")
    parser.add_argument("--sample_interval", type=float, default=1.0,
                        help="YOLO sampling interval in seconds")
    parser.add_argument("--multi_frame_count", type=int, default=3,
                        help="Number of frames to collect for LLM analysis")
    parser.add_argument("--multi_frame_gap", type=float, default=0.5,
                        help="Time gap between collected frames in seconds")
    parser.add_argument("--buffer_seconds", type=int, default=30, help="Ring buffer duration in seconds")
    parser.add_argument("--clip_before", type=int, default=5, help="Seconds of video before conflict in alert clip")
    parser.add_argument("--clip_after", type=int, default=5, help="Seconds of video after conflict in alert clip")
    parser.add_argument("--output_dir", type=str, default=os.path.join(script_dir, "alerts"),
                        help="Alert video output directory (per-camera subfolders are created automatically)")
    parser.add_argument("--fps", type=int, default=15, help="Video stream frame rate")
    # --- Alarm delivery channels (in addition to stdout JSON lines) ---
    parser.add_argument("--inbox_file", type=str,
                        default=os.path.join(script_dir, "alerts", "pending.jsonl"),
                        help="Alarm inbox file (JSON lines). Consumed by the heartbeat task to push alerts into the chat window.")
    parser.add_argument("--feishu_webhook", type=str,
                        default="",
                        help="Feishu custom bot webhook URL (or set in config.json).")
    parser.add_argument("--feishu_secret", type=str,
                        default="",
                        help="Feishu webhook signing secret (optional).")
    parser.add_argument("--feishu_app_id", type=str,
                        default="",
                        help="Feishu self-built app App ID (used to upload the "
                             "conflict snapshot so it renders inline in the card).")
    parser.add_argument("--feishu_app_secret", type=str,
                        default="",
                        help="Feishu self-built app App Secret (paired with --feishu_app_id).")
    parser.add_argument("--discord_webhook", type=str,
                        default="",
                        help="Discord channel webhook URL (or set in config.json).")
    parser.add_argument("--proxy", type=str,
                        default="",
                        help="HTTPS proxy for Discord/Telegram push. "
                             "Example: http://127.0.0.1:7890. Not used for Feishu.")
    parser.add_argument("--telegram_bot_token", type=str,
                        default="",
                        help="Telegram Bot token from @BotFather (or set in config.json).")
    parser.add_argument("--telegram_chat_id", type=str,
                        default="",
                        help="Telegram target chat/group ID (or set in config.json).")
    return parser.parse_args()


# ==================== Main Loop ====================
def resolve_cameras(args, cfg: dict) -> list:
    """Resolve the list of cameras to monitor.

    Resolution priority:
      1. CLI single-camera override: if `--rtsp_url` is provided, run a single
         camera. Its name comes from `--camera_name`; if missing, fall back to
         `camera_0` and log the auto-assignment.
      2. Otherwise, read `cfg["cameras"]` (list of {name, rtsp_url}). Entries
         with empty `rtsp_url` are skipped. Entries without `name` get
         `camera_<index>` and an info log.

    Returns a list of {"name": str, "rtsp_url": str}. Empty list means "no
    camera configured" — the caller should treat that as a fatal error.
    """
    cli_url = (getattr(args, "rtsp_url", "") or "").strip()
    if cli_url:
        raw_name = (getattr(args, "camera_name", "") or "").strip()
        if raw_name:
            name = raw_name
        else:
            name = "camera_0"
            logger.info(
                f"--rtsp_url provided without --camera_name; auto-assigned id '{name}'."
            )
        return [{"name": name, "rtsp_url": cli_url}]

    cameras = []
    cfg_cameras = cfg.get("cameras")
    if isinstance(cfg_cameras, list) and cfg_cameras:
        for idx, cam in enumerate(cfg_cameras):
            if not isinstance(cam, dict):
                continue
            url = (cam.get("rtsp_url") or "").strip()
            if not url:
                continue
            raw_name = (cam.get("name") or "").strip()
            if raw_name:
                name = raw_name
            else:
                name = f"camera_{idx}"
                logger.info(
                    f"No name provided for cameras[{idx}]; auto-assigned id '{name}'."
                )
            cameras.append({"name": name, "rtsp_url": url})
    return cameras


def detect_camera_worker(cam: dict, args, detector: "PersonDetector",
                         analyzer: "ConflictAnalyzer",
                         inference_lock: threading.Lock,
                         stop_event: threading.Event):
    """Per-camera continuous detection loop, run inside a worker thread.

    Continuous mode: detection events do NOT terminate the worker; the worker
    pushes the alert (stdout / inbox / Feishu / Discord / Telegram) and resumes
    monitoring on the same stream. The worker only stops when the stream ends
    (local file), `stop_event` is set (Ctrl+C in main thread), or a fatal
    error occurs.
    """
    cam_name = cam["name"]
    rtsp_url = cam["rtsp_url"]
    output_dir = os.path.join(args.output_dir, cam_name)

    try:
        grabber = FrameGrabber(
            rtsp_url, buffer_seconds=args.buffer_seconds, fps=args.fps
        )
    except Exception as e:
        logger.error(f"[{cam_name}] failed to open stream {rtsp_url}: {e}")
        return

    last_sample_time = 0.0
    multi_frame_buffer = []
    sample_count = 0
    last_heartbeat_time = time.time()
    HEARTBEAT_EVERY = 30

    logger.info(f"[{cam_name}] worker started, monitoring {rtsp_url}")

    try:
        while grabber.running and not stop_event.is_set():
            frame, frame_count = grabber.get_latest_frame()
            if frame is None:
                time.sleep(0.01)
                continue

            now = time.time()
            if now - last_sample_time < args.sample_interval:
                time.sleep(0.01)
                continue
            last_sample_time = now
            sample_count += 1

            # YOLO ONNX session is shared across cameras -> serialize.
            with inference_lock:
                person_count = detector.count_persons(frame)

            if sample_count % HEARTBEAT_EVERY == 0:
                elapsed = now - last_heartbeat_time
                logger.info(
                    f"[{cam_name}] [heartbeat] samples={sample_count} "
                    f"person_count={person_count} frame={frame_count} "
                    f"interval={elapsed:.1f}s (waiting for >={args.min_persons} persons)"
                )
                last_heartbeat_time = now

            if person_count < args.min_persons:
                multi_frame_buffer.clear()
                continue

            logger.info(
                f"[{cam_name}] Detected {person_count} persons, collecting frames... "
                f"({len(multi_frame_buffer)+1}/{args.multi_frame_count})"
            )
            multi_frame_buffer.append(frame)

            if len(multi_frame_buffer) < args.multi_frame_count:
                time.sleep(args.multi_frame_gap)
                continue

            conflict_anchor_time = now
            logger.info(
                f"[{cam_name}] Collected {len(multi_frame_buffer)} frames, calling LLM for analysis..."
            )

            # Snapshot frame for inline image preview in push notifications.
            # Pick the last collected frame (closest to the conflict moment);
            # multi_frame_buffer will be cleared right after the LLM call.
            snapshot_frame = (
                multi_frame_buffer[-1].copy() if multi_frame_buffer else None
            )

            # Freeze the pre-conflict clip BEFORE the (slow) LLM call so the
            # ring buffer cannot drop the target window while we wait.
            pre_snapshot = grabber.get_buffer_snapshot()
            pre_start = conflict_anchor_time - args.clip_before
            pre_clip_frames = [
                (ts, f) for ts, f in pre_snapshot
                if pre_start <= ts <= conflict_anchor_time
            ]
            logger.info(
                f"[{cam_name}] Pre-conflict clip frozen: {len(pre_clip_frames)} frames "
                f"(target window {args.clip_before}s before anchor)"
            )

            result = analyzer.analyze(multi_frame_buffer)
            multi_frame_buffer.clear()

            if result.get("conflict"):
                logger.warning(
                    f"[{cam_name}] Conflict detected: {result.get('description', 'unknown')}"
                )

                logger.info(f"[{cam_name}] Recording {args.clip_after}s after conflict...")
                time.sleep(args.clip_after)

                post_snapshot = grabber.get_buffer_snapshot()
                post_end = conflict_anchor_time + args.clip_after
                post_clip_frames = [
                    (ts, f) for ts, f in post_snapshot
                    if conflict_anchor_time < ts <= post_end
                ]
                logger.info(
                    f"[{cam_name}] Post-conflict clip captured: {len(post_clip_frames)} frames "
                    f"(target window {args.clip_after}s after anchor)"
                )

                clip_frames = sorted(
                    pre_clip_frames + post_clip_frames, key=lambda x: x[0]
                )
                clip_path = ""
                if clip_frames:
                    clip_path = save_video_clip(
                        clip_frames, output_dir, fps=args.fps,
                        prefix=f"conflict_{cam_name}",
                    )

                # Save a single representative frame as a snapshot for push
                # notifications. The frame was captured between clip_before
                # and clip_after windows (i.e. at the conflict moment).
                snapshot_path = ""
                if snapshot_frame is not None:
                    snapshot_path = save_conflict_snapshot(
                        snapshot_frame, output_dir,
                        prefix=f"snapshot_{cam_name}",
                    )

                clip_info = (
                    f"Video clip saved to {clip_path}." if clip_path
                    else "Video clip not available (frames dropped or save failed)."
                )
                alert = {
                    "alert": "conflict_detected",
                    "camera": cam_name,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "description": result.get("description", ""),
                    "video_clip": clip_path,
                    "snapshot_image": snapshot_path,
                    "clip_duration": f"{args.clip_before + args.clip_after}s",
                    "message": (
                        f"[{cam_name}] Warning: Physical conflict detected. "
                        f"{result.get('description', '')}. {clip_info} "
                        f"Please review and take appropriate action."
                    ),
                }
                # Multi-channel alarm delivery (continuous mode — do NOT exit):
                #   1) stdout JSON line
                #   2) inbox file (pending.jsonl) -> heartbeat task fallback push to chat
                #   3) Feishu webhook -> instant push (with inline snapshot)
                #   4) Discord webhook -> instant push (with inline snapshot)
                #   5) Telegram Bot API -> instant push (with inline snapshot)
                print(json.dumps(alert, ensure_ascii=False), flush=True)
                append_inbox(args.inbox_file, alert)
                send_feishu(args.feishu_webhook, alert,
                            secret=args.feishu_secret,
                            app_id=args.feishu_app_id,
                            app_secret=args.feishu_app_secret)
                send_discord(args.discord_webhook, alert, proxy=args.proxy)
                send_telegram(args.telegram_bot_token, args.telegram_chat_id, alert, proxy=args.proxy)
                logger.info(f"[{cam_name}] Alert pushed; resuming detection")
            else:
                logger.info(f"[{cam_name}] LLM result: no conflict detected")
    except Exception as e:
        logger.error(f"[{cam_name}] worker error: {e}", exc_info=True)
    finally:
        grabber.stop()
        logger.info(f"[{cam_name}] worker stopped")


def load_config() -> dict:
    """Load persistent configuration from config.json next to this script.

    Returns an empty dict if the file is missing or invalid. Values written here
    are user-provided (e.g., RTSP URL, Kami API key, push channel credentials),
    so the user does not have to pass them on the command line each time.
    """
    cfg_path = os.path.join(script_dir, "config.json")
    if not os.path.isfile(cfg_path):
        return {}
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            data = json.load(f) or {}
        return data if isinstance(data, dict) else {}
    except Exception as e:
        logger.warning(f"Failed to load config.json: {e}")
        return {}


def main():
    args = parse_args()
    cfg = load_config()

    # Merge non-camera shared fields: command-line wins; otherwise config.json.
    args.kami_api_key = (args.kami_api_key or cfg.get("kami_api_key", "")).strip()
    args.feishu_webhook = (args.feishu_webhook or cfg.get("feishu_webhook", "")).strip()
    args.feishu_secret = (args.feishu_secret or cfg.get("feishu_secret", "")).strip()
    args.feishu_app_id = (args.feishu_app_id or cfg.get("feishu_app_id", "")).strip()
    args.feishu_app_secret = (args.feishu_app_secret or cfg.get("feishu_app_secret", "")).strip()
    args.discord_webhook = (args.discord_webhook or cfg.get("discord_webhook", "")).strip()
    args.telegram_bot_token = (args.telegram_bot_token or cfg.get("telegram_bot_token", "")).strip()
    args.telegram_chat_id = (args.telegram_chat_id or cfg.get("telegram_chat_id", "")).strip()
    args.proxy = (getattr(args, "proxy", "") or cfg.get("proxy", "")).strip()

    cameras = resolve_cameras(args, cfg)
    if not cameras:
        logger.error(
            "No camera configured. Provide cameras[] in config.json (each entry "
            "with name + rtsp_url), or pass --rtsp_url for a single-camera run."
        )
        sys.exit(EXIT_ERROR)

    # Ensure YOLO ONNX model exists; auto-download .pt and export on first run.
    try:
        args.yolo_model = ensure_yolo_model(args.yolo_model)
    except Exception as e:
        logger.error(f"Failed to prepare YOLO model: {e}")
        sys.exit(EXIT_ERROR)

    if not args.kami_api_key:
        logger.error("Kami API key not provided. Pass --kami_api_key or set it in config.json")
        sys.exit(EXIT_ERROR)

    logger.info("===== Conflict Detection Started (Continuous Multi-Camera Mode) =====")
    for cam in cameras:
        logger.info(f"  camera '{cam['name']}' -> {cam['rtsp_url']}")
    logger.info(f"YOLO model: {args.yolo_model}")
    logger.info(f"Min persons to trigger: {args.min_persons}")
    logger.info(f"Sample interval: {args.sample_interval}s")
    logger.info("Mode: continuous; alerts pushed per-camera, process keeps running")

    # Shared components: ONNX session and analyzer are shared across all cameras
    # to avoid loading the model multiple times. ONNX inference is serialized
    # via inference_lock.
    detector = PersonDetector(args.yolo_model, conf_threshold=args.conf_threshold)
    analyzer = ConflictAnalyzer(args.kami_api_key)
    inference_lock = threading.Lock()
    stop_event = threading.Event()

    threads = []
    for cam in cameras:
        t = threading.Thread(
            target=detect_camera_worker,
            args=(cam, args, detector, analyzer, inference_lock, stop_event),
            name=f"worker-{cam['name']}",
            daemon=False,
        )
        t.start()
        threads.append(t)

    exit_code = EXIT_NORMAL
    try:
        # Supervise: as long as any worker is alive, stay in main thread so
        # KeyboardInterrupt is delivered here (not to a background thread).
        while any(t.is_alive() for t in threads):
            for t in threads:
                t.join(timeout=1.0)
    except KeyboardInterrupt:
        logger.info("User interrupted, signaling all workers to stop...")
        stop_event.set()
        for t in threads:
            t.join(timeout=5)
    finally:
        stop_event.set()
        logger.info(f"===== Conflict Detection Ended (exit_code={exit_code}) =====")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
