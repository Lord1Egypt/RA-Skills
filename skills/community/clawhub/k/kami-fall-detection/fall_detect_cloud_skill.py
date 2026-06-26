"""
Fall Detection Skill (Cloud) — Two-stage pipeline:
  Stage 1: Lightweight temporal change detection on RTSP stream
  Stage 2: Send clip to KamiClaw API for fall analysis

Usage:
    # Cameras are declared in config.json under the 'cameras' array.
    python fall_detect_cloud_skill.py --api_key sk_live_xxxxxxxx
"""

import argparse
import base64
import json
import logging
import math
import os
import sys
import tempfile
import threading
import time
from collections import deque
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np
import requests

# ── Paths & Logging ──────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
LOGS_DIR   = SCRIPT_DIR / "logs"
CLIPS_DIR  = LOGS_DIR / "clips"
LOGS_DIR.mkdir(exist_ok=True)
CLIPS_DIR.mkdir(exist_ok=True)

# Import notification modules
sys.path.insert(0, str(SCRIPT_DIR))
from feishu_notifier import send_fall_alarm as send_feishu_alarm, create_notifier_from_config
from telegram_notifier import send_fall_alarm as send_telegram_alarm, get_bot_token_from_config
from discord_notifier import (
    send_fall_alarm as send_discord_webhook,
    send_fall_alarm_bot as send_discord_bot,
    get_discord_notifier
)

app_handler = TimedRotatingFileHandler(
    str(LOGS_DIR / "app.log"), when="midnight", backupCount=30, encoding="utf-8"
)
# Include camera_name in every record so multi-camera logs are traceable.
app_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(camera_name)s] %(message)s"
))
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(camera_name)s] %(message)s"
))


class _DefaultCameraNameFilter(logging.Filter):
    """Ensure every record has a camera_name field (default '-' for global logs)."""
    def filter(self, record: logging.LogRecord) -> bool:  # type: ignore[override]
        if not hasattr(record, "camera_name"):
            record.camera_name = "-"
        return True


app_handler.addFilter(_DefaultCameraNameFilter())
stream_handler.addFilter(_DefaultCameraNameFilter())

logging.basicConfig(level=logging.INFO, handlers=[app_handler, stream_handler])
logger = logging.getLogger(__name__)


def get_camera_logger(camera_name: str) -> logging.LoggerAdapter:
    """Return a LoggerAdapter that injects camera_name into every record."""
    return logging.LoggerAdapter(logger, {"camera_name": camera_name})

ALARM_LOG      = LOGS_DIR / "alarms.jsonl"
TRANSITION_LOG = LOGS_DIR / "transitions.jsonl"


# ── Logging helpers ───────────────────────────────────────────────────────────
def _append_jsonl(path: Path, obj: dict):
    obj["_ts"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def log_alarm(alarm: dict, cfg: dict, log: Optional[logging.LoggerAdapter] = None):
    log = log or get_camera_logger(alarm.get("camera_name", "-"))
    log.info(f"ALARM: {alarm}")
    _append_jsonl(ALARM_LOG, {"event": "alarm", **alarm})

    # Get posture image path from config
    posture_image_path = cfg.get("fall_posture_image")
    if posture_image_path:
        # Resolve relative path to absolute
        posture_image_path = str(SCRIPT_DIR / posture_image_path)
        if not os.path.isfile(posture_image_path):
            log.warning(f"Posture image not found: {posture_image_path}")
            posture_image_path = None

    # Send Feishu notification (Webhook only)
    try:
        webhook_url = cfg.get("feishu_webhook_url")
        feishu_app_id = cfg.get("feishu_app_id", "")
        feishu_app_secret = cfg.get("feishu_app_secret", "")

        if webhook_url:
            log.info(f"Sending Feishu alarm via webhook (inline_image={'yes' if feishu_app_id and feishu_app_secret else 'no'})")
            send_feishu_alarm(
                webhook_url=webhook_url,
                alarm=alarm,
                clip_path=alarm.get("clip"),
                posture_image_path=posture_image_path,
                app_id=feishu_app_id,
                app_secret=feishu_app_secret,
            )
        else:
            log.warning("Feishu webhook_url not configured, skipping notification")
    except Exception as e:
        log.error(f"Failed to send Feishu alarm: {e}")

    # Send Telegram notification (Bot API)
    try:
        chat_id = cfg.get("telegram_chat_id")
        bot_token = cfg.get("telegram_bot_token") or get_bot_token_from_config()

        if chat_id and bot_token:
            log.info(f"Sending Telegram alarm to {chat_id}")
            send_telegram_alarm(chat_id=chat_id, bot_token=bot_token, alarm=alarm, clip_path=alarm.get("clip"), posture_image_path=posture_image_path)
        else:
            if not chat_id:
                log.warning("Telegram chat_id not configured, skipping notification")
            if not bot_token:
                log.warning("Telegram bot_token not configured, skipping notification")
    except Exception as e:
        log.error(f"Failed to send Telegram alarm: {e}")

    # Send Discord notification (Bot API or Webhook)
    try:
        bot_token = cfg.get("discord_bot_token")
        channel_id = cfg.get("discord_channel_id")
        webhook_url = cfg.get("discord_webhook_url")

        if bot_token and channel_id:
            log.info(f"Sending Discord alarm via Bot API to channel {channel_id}")
            send_discord_bot(bot_token=bot_token, channel_id=channel_id, alarm=alarm, clip_path=alarm.get("clip"), posture_image_path=posture_image_path)
        elif webhook_url:
            log.info(f"Sending Discord alarm via webhook")
            send_discord_webhook(webhook_url=webhook_url, alarm=alarm, clip_path=alarm.get("clip"), posture_image_path=posture_image_path)
        else:
            log.warning("Discord notification not configured (need bot_token+channel_id or webhook_url)")
    except Exception as e:
        log.error(f"Failed to send Discord alarm: {e}")


def log_transition(frame: int, source: str, camera: Optional[dict] = None,
                   log: Optional[logging.LoggerAdapter] = None):
    camera = camera or {}
    log = log or get_camera_logger(camera.get("name", "-"))
    log.info(f"Transition at frame {frame}")
    _append_jsonl(TRANSITION_LOG, {
        "event": "transition", "frame": frame, "source": source,
        "camera_name": camera.get("name"),
    })


def log_clip_result(frame: int, source: str, fall_detected: bool, detail: dict,
                    camera: Optional[dict] = None):
    camera = camera or {}
    _append_jsonl(ALARM_LOG, {
        "event": "clip_analyzed", "frame": frame, "source": source,
        "camera_name": camera.get("name"),
        "fall_detected": fall_detected, **detail,
    })


def save_alarm_clip(frames: list, fps: float, frame_w: int, frame_h: int,
                    alarm_type: str) -> str:
    ts       = time.strftime("%Y%m%d_%H%M%S")
    clip_path = str(CLIPS_DIR / f"alarm_{alarm_type}_{ts}.mp4")
    writer   = cv2.VideoWriter(clip_path, cv2.VideoWriter_fourcc(*"mp4v"),
                                fps, (frame_w, frame_h))
    for f in frames:
        writer.write(f)
    writer.release()
    logger.info(f"Alarm clip saved: {clip_path}")
    return clip_path


# ── KamiClaw API ─────────────────────────────────────────────────────────────
KAMICLAW_API_URL = "https://kamiclaw-skill-api.kamihome.com/v1/detect"


def validate_api_key(api_key: str) -> bool:
    """Validate the KamiClaw API key with a lightweight EMBED request."""
    headers = {"Content-Type": "application/json", "X-API-Key": api_key}
    payload = {
        "detectType": "EMBED",
        "detectSubType": "",
        "skillId": "SK_FALL_DETECTION",
        "prompt": "key validation",
        "imageFile": "",
        "videoFile": "",
    }
    try:
        resp = requests.post(KAMICLAW_API_URL, headers=headers,
                             json=payload, timeout=(10, 30))
        data = resp.json()
        if data.get("code") == 200 and data.get("data", {}).get("status") == "SUCCESS":
            logger.info("API key valid.")
            return True
        logger.error(f"API key rejected: {data.get('msg', resp.text)}")
        return False
    except Exception as e:
        logger.error(f"Key validation failed: {e}")
        return False


def _file_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def call_kamiclaw_detect(video_path: str, api_key: str) -> dict:
    """Send video clip to KamiClaw API for fall detection."""
    headers = {"Content-Type": "application/json", "X-API-Key": api_key}
    payload = {
        "detectType": "FALL",
        "detectSubType": "",
        "skillId": "SK_FALL_DETECTION",
        "prompt": "",
        "imageFile": "",
        "videoFile": _file_to_base64(video_path),
    }

    for attempt in range(3):
        try:
            resp = requests.post(KAMICLAW_API_URL, headers=headers,
                                 json=payload, timeout=(10, 300))
            logger.info(f"API response: status={resp.status_code} body={resp.text[:300]!r}")

            if not resp.text.strip():
                logger.error(f"Empty response body (HTTP {resp.status_code})")
                return {"status": "ERROR", "error": "empty response body"}

            data = resp.json()

            if resp.status_code == 429 or resp.status_code >= 500:
                wait = (attempt + 1) * 10
                logger.warning(f"API {resp.status_code}, retry in {wait}s")
                time.sleep(wait)
                continue

            if data.get("code") == 200:
                result_data = data.get("data", {})
                return {
                    "status": result_data.get("status", "UNKNOWN"),
                    "result": result_data.get("result", ""),
                }

            msg = data.get("msg", resp.text)
            logger.error(f"KamiClaw error: {msg}")
            return {"status": "ERROR", "error": msg}

        except requests.exceptions.Timeout:
            wait = (attempt + 1) * 15
            logger.warning(f"Timeout, retry in {wait}s")
            time.sleep(wait)
        except Exception as e:
            logger.error(f"API call failed: {e}")
            return {"status": "ERROR", "error": str(e)}

    return {"status": "ERROR", "error": "max retries exceeded"}


def parse_fall_result(result_text: str) -> dict:
    """Parse the API result text into a structured fall detection result."""
    text = (result_text or "").strip().lower()

    # Expected path: model returns JSON
    try:
        obj = json.loads(result_text)
        if isinstance(obj, dict):
            return {
                "fall_detected": bool(obj.get("fall_detected", False)),
                "confidence":    float(obj.get("confidence", 0.0)),
                "fall_type":     obj.get("fall_type"),
                "num_persons":   int(obj.get("num_persons", 0)),
                "reason":        str(obj.get("reason", "")),
            }
    except (json.JSONDecodeError, ValueError):
        pass

    # Fallback: keyword-based
    no_fall_kw = ["no fall", "not a fall", "no_fall", "fall_detected: false",
                  "fall_detected\":false", "fall_detected\": false"]
    fall_kw    = ["fall detected", "fall_detected", "fallen", "fell",
                  "on the floor", "collapsed", "lying on floor"]

    for kw in no_fall_kw:
        if kw in text:
            return {"fall_detected": False, "confidence": None,
                    "fall_type": None, "num_persons": None, "reason": result_text[:200]}
    for kw in fall_kw:
        if kw in text:
            return {"fall_detected": True, "confidence": None,
                    "fall_type": None, "num_persons": None, "reason": result_text[:200]}

    return {"fall_detected": False, "confidence": None,
            "fall_type": None, "num_persons": None, "reason": result_text[:200]}


# ── Stage 1 — Temporal change detection ──────────────────────────────────────
class TransitionDetector:
    def __init__(self, fps: float):
        self.prev_frame      = None
        self.prev_trans_info: list[float] = []
        self.is_first        = True
        # Lowered threshold for subtle motion detection (falls may have low frame diffs)
        # Original formula gave ~28 for 20fps, but actual fall motion can be 3-6
        self.threshold       = min(
            max((3.0 - 5.0) / (30.0 - 15.0) * (fps - 15.0) + 5.0, 3.0), 5.0
        )

    def _check(self, trans: float, window: int = 10) -> bool:
        vals = self.prev_trans_info[max(0, len(self.prev_trans_info) - window):]
        if not vals:
            return trans > self.threshold
        mean = sum(vals) / len(vals)
        std  = math.sqrt(sum((v - mean) ** 2 for v in vals) / len(vals))
        return trans > (mean + std) * 2 and trans > self.threshold

    def detect(self, frame: np.ndarray) -> bool:
        gray = cv2.cvtColor(cv2.resize(frame, (128, 128)), cv2.COLOR_BGR2GRAY)
        if self.is_first:
            self.is_first = False
            self.prev_frame = gray
            return False
        diff     = np.mean(np.abs(gray.astype(np.float32) - self.prev_frame.astype(np.float32)))
        is_trans = self._check(diff)
        if not is_trans:
            _, std_dev = cv2.meanStdDev(gray)
            if std_dev[0][0] < 5.0:
                is_trans = True
        self.prev_trans_info = [] if is_trans else self.prev_trans_info + [diff]
        self.prev_frame = gray
        return is_trans


# ── Frame buffer + clip writer ────────────────────────────────────────────────
class FrameBuffer:
    def __init__(self, max_seconds: float, fps: float):
        self.buf: deque = deque(maxlen=max(1, int(max_seconds * fps)))

    def push(self, frame: np.ndarray):   self.buf.append(frame)
    def snapshot(self) -> list:          return list(self.buf)
    def clear(self):                     self.buf.clear()


CLIP_OUT_W, CLIP_OUT_H = 640, 360  # output canvas size (16:9)
GREY = (128, 128, 128)              # BGR grey for padding


def _resize_with_padding(frame: np.ndarray) -> np.ndarray:
    """Resize frame to fit within 640x360 canvas with grey letterboxing.

    The content is scaled to fit the canvas, centered, and remaining
    area is filled with grey. For a square input (e.g. 1696x1696),
    the content becomes 360x360 centered in 640x360 with 140px grey
    bars on each side.
    """
    in_h, in_w = frame.shape[:2]
    scale = min(CLIP_OUT_W / in_w, CLIP_OUT_H / in_h)
    new_w, new_h = int(in_w * scale), int(in_h * scale)
    resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

    canvas = np.full((CLIP_OUT_H, CLIP_OUT_W, 3), GREY, dtype=np.uint8)
    x_off = (CLIP_OUT_W - new_w) // 2
    y_off = (CLIP_OUT_H - new_h) // 2
    canvas[y_off:y_off + new_h, x_off:x_off + new_w] = resized
    return canvas


def write_clip(frames: list, fps: float) -> str:
    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False, prefix="fall_clip_")
    tmp.close()
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(tmp.name, fourcc, fps, (CLIP_OUT_W, CLIP_OUT_H))
    for f in frames:
        writer.write(_resize_with_padding(f))
    writer.release()
    return tmp.name


# ── Config & Args ─────────────────────────────────────────────────────────────
CONFIG_PATH = str(SCRIPT_DIR / "config.json")


def load_config() -> dict:
    if os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}


def parse_args():
    p = argparse.ArgumentParser(description="Fall detection skill (KamiClaw cloud)")
    p.add_argument("--api_key",      type=str,   default="")
    p.add_argument("--run_time",     type=int,   default=0,
                   help="Max run time in seconds (0 = unlimited)")
    p.add_argument("--pre_seconds",  type=float, default=4.0)
    p.add_argument("--post_seconds", type=float, default=4.0)
    p.add_argument("--feishu_chat_id", type=str, default="",
                   help="Feishu chat ID for alarm notifications")
    p.add_argument("--cameras_config", type=str, default="",
                   help="Path to an alternate config file containing a 'cameras' array")
    p.add_argument("--list_cameras", action="store_true",
                   help="Print resolved cameras and exit")
    return p.parse_args()


# ── Camera resolution ────────────────────────────────────────────────────────
def resolve_cameras(cfg: dict) -> List[dict]:
    """Resolve the camera list from config.

    Schema (per entry): { 'name': str (optional for single-camera), 'rtsp_url': str (required) }.

    Rules:
      - cfg['cameras'] must be a non-empty list.
      - Each entry must have a non-empty 'rtsp_url'.
      - If exactly one entry: 'name' is optional; missing/empty -> auto-fill 'default'.
      - If two or more entries: every entry must have a non-empty unique 'name'.
    """
    raw = cfg.get("cameras")
    if not isinstance(raw, list) or not raw:
        logger.error("No cameras configured. Add at least one entry to 'cameras' in config.json.")
        sys.exit(1)

    cameras: List[dict] = []
    for idx, item in enumerate(raw):
        if not isinstance(item, dict):
            logger.error(f"cameras[{idx}] must be an object, got {type(item).__name__}")
            sys.exit(1)
        url = str(item.get("rtsp_url", "")).strip()
        if not url:
            logger.error(f"cameras[{idx}] missing required 'rtsp_url'")
            sys.exit(1)
        name = str(item.get("name", "")).strip()
        cameras.append({"name": name, "rtsp_url": url})

    if len(cameras) == 1:
        if not cameras[0]["name"]:
            cameras[0]["name"] = "default"
        return cameras

    # Multi-camera: all names must be present and unique.
    names = [c["name"] for c in cameras]
    if any(not n for n in names) or len(set(names)) != len(names):
        logger.error(
            f"Multiple cameras detected. Every camera must have a unique 'name'. Got: {names}."
        )
        sys.exit(1)
    return cameras


# ── Per-camera worker ────────────────────────────────────────────────────────
RECONNECT_DELAY = 5


def _open_capture(url: str, log: logging.LoggerAdapter,
                  stop_event: threading.Event) -> Optional[cv2.VideoCapture]:
    """Try to open the RTSP capture, retrying until success or stop_event is set."""
    attempt = 0
    while not stop_event.is_set():
        cap = cv2.VideoCapture(url)
        if cap.isOpened():
            return cap
        cap.release()
        attempt += 1
        log.warning(f"Cannot open stream (attempt {attempt}), retrying in {RECONNECT_DELAY}s...")
        if stop_event.wait(RECONNECT_DELAY):
            return None
    return None


def run_camera(camera: dict, cfg: dict, api_key: str,
               pre_seconds: float, post_seconds: float,
               run_time: int, save_clips: bool,
               stop_event: threading.Event) -> None:
    """Run the two-stage fall-detection pipeline for a single camera.

    Each camera owns its own capture, transition detector, frame buffer, and
    state machine. All emitted alarms / log lines are tagged with this camera's
    name so downstream notifications can identify the source.
    """
    cam_name = camera["name"]
    rtsp_url = camera["rtsp_url"]
    pre_s    = float(pre_seconds)
    post_s   = float(post_seconds)
    log      = get_camera_logger(cam_name)

    log.info(f"Starting worker  source={rtsp_url}  pre={pre_s}s  post={post_s}s")

    cap = _open_capture(rtsp_url, log, stop_event)
    if cap is None:
        log.info("Worker stopped before capture opened")
        return

    fps     = cap.get(cv2.CAP_PROP_FPS) or 15.0
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    log.info(f"Opened: {frame_w}x{frame_h} @ {fps:.1f} FPS")

    trans_detector     = TransitionDetector(fps)
    pre_buffer         = FrameBuffer(pre_s, fps)
    post_frames_needed = max(1, int(post_s * fps))

    frame_count     = 0
    start_time      = time.time()
    collecting_post = False
    post_frames:    list = []
    pre_snapshot:   list = []

    try:
        while not stop_event.is_set():
            if run_time > 0 and (time.time() - start_time) > run_time:
                log.info(f"Run time {run_time}s reached")
                break

            ret, frame = cap.read()
            if not ret:
                log.warning("Stream lost — attempting reconnect...")
                cap.release()
                if collecting_post:
                    log.warning(f"Discarding incomplete clip "
                                f"({len(post_frames)}/{post_frames_needed} post-frames)")
                    collecting_post = False
                    post_frames, pre_snapshot = [], []
                    pre_buffer.clear()
                    trans_detector = TransitionDetector(fps)
                cap = _open_capture(rtsp_url, log, stop_event)
                if cap is None:
                    return
                new_fps = cap.get(cv2.CAP_PROP_FPS) or fps
                new_w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                new_h   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                log.info(f"Reconnected: {new_w}x{new_h} @ {new_fps:.1f} FPS")
                if new_fps != fps or new_w != frame_w or new_h != frame_h:
                    fps, frame_w, frame_h = new_fps, new_w, new_h
                    post_frames_needed = max(1, int(post_s * fps))
                    trans_detector = TransitionDetector(fps)
                    pre_buffer     = FrameBuffer(pre_s, fps)
                continue

            frame_count += 1

            # ── Post-transition collection ────────────────────────────────────
            if collecting_post:
                post_frames.append(frame)
                if len(post_frames) >= post_frames_needed:
                    clip_frames = pre_snapshot + post_frames
                    log.info(f"Clip ready: {len(clip_frames)} frames "
                             f"({len(pre_snapshot)} pre + {len(post_frames)} post)")

                    clip_path = write_clip(clip_frames, fps)
                    try:
                        api_result = call_kamiclaw_detect(clip_path, api_key)
                    finally:
                        os.unlink(clip_path)

                    if api_result.get("status") == "SUCCESS":
                        fall_result = parse_fall_result(api_result.get("result", ""))

                        if fall_result.get("fall_detected"):
                            clip_file = save_alarm_clip(
                                clip_frames, fps, frame_w, frame_h, "fall") if save_clips else None
                            alarm = {
                                "alarm":       True,
                                "type":        "fall",
                                "camera_name": cam_name,
                                "fall_type":   fall_result.get("fall_type"),
                                "num_persons": fall_result.get("num_persons"),
                                "confidence":  fall_result.get("confidence"),
                                "reason":      fall_result.get("reason", ""),
                                "frame":       frame_count,
                                "source":      rtsp_url,
                                "clip":        clip_file,
                            }
                            log_alarm(alarm, cfg, log=log)
                            print(json.dumps(alarm, ensure_ascii=False), flush=True)
                        else:
                            log.info(f"No fall. Reason: {fall_result.get('reason', '')[:100]}")
                            log_clip_result(frame_count, rtsp_url, False, fall_result, camera=camera)
                    else:
                        log.warning(f"API error: {api_result.get('error', 'unknown')}")

                    collecting_post = False
                    post_frames, pre_snapshot = [], []
                    pre_buffer.clear()
                    trans_detector = TransitionDetector(fps)
                continue

            # ── Stage 1: change detection ─────────────────────────────────────
            pre_buffer.push(frame)
            if trans_detector.detect(frame):
                log_transition(frame_count, rtsp_url, camera=camera, log=log)
                pre_snapshot    = pre_buffer.snapshot()
                post_frames     = []
                collecting_post = True
                continue

            if frame_count % 100 == 0:
                log.info(f"Monitoring: frame {frame_count}, {time.time() - start_time:.0f}s")

    except Exception as e:
        log.exception(f"Worker crashed: {e}")
    finally:
        try:
            cap.release()
        except Exception:
            pass

    result = {"alarm": False, "type": None,
              "detail": "Run time limit reached, no fall detected",
              "frames_processed": frame_count,
              "camera_name": cam_name,
              "source": rtsp_url}
    print(json.dumps(result, ensure_ascii=False), flush=True)
    log.info(f"Done. {frame_count} frames, no alarm.")


# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    args = parse_args()

    # Allow CLI to point to a different config file (cameras_config wins).
    cfg_path = (args.cameras_config or CONFIG_PATH).strip() if hasattr(args, "cameras_config") else CONFIG_PATH
    if cfg_path and os.path.isfile(cfg_path):
        with open(cfg_path, "r") as f:
            cfg = json.load(f)
    else:
        cfg = {}

    api_key      = (args.api_key or os.environ.get("KAMICLAW_API_KEY") or cfg.get("api_key", "")).strip()
    run_time     = args.run_time     or cfg.get("run_time", 0)
    pre_seconds  = args.pre_seconds  or cfg.get("pre_seconds", 3.0)
    post_seconds = args.post_seconds or cfg.get("post_seconds", 3.0)
    save_clips   = cfg.get("save_alarm_clips", True)

    cameras = resolve_cameras(cfg)

    if args.list_cameras:
        print(json.dumps({"cameras": cameras}, ensure_ascii=False, indent=2))
        sys.exit(0)

    if not api_key:
        logger.error("KamiClaw API key required. Pass --api_key or set KAMICLAW_API_KEY.")
        sys.exit(1)

    logger.info("Validating KamiClaw API key...")
    if not validate_api_key(api_key):
        logger.error("Invalid or expired API key.")
        sys.exit(1)

    logger.info("===== Fall detection skill started =====")
    logger.info(f"Cameras: {len(cameras)}  pre={pre_seconds}s  post={post_seconds}s")
    for c in cameras:
        logger.info(f"  - [{c['name']}] {c['rtsp_url']}")

    stop_event = threading.Event()
    threads: List[threading.Thread] = []
    for cam in cameras:
        t = threading.Thread(
            target=run_camera,
            args=(cam, cfg, api_key, pre_seconds, post_seconds, run_time, save_clips, stop_event),
            name=f"cam-{cam['name']}",
            daemon=True,
        )
        t.start()
        threads.append(t)

    try:
        # Wait for all workers; tolerate Ctrl+C.
        while any(t.is_alive() for t in threads):
            for t in threads:
                t.join(timeout=0.5)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received — signaling workers to stop")
        stop_event.set()
        for t in threads:
            t.join(timeout=10)

    logger.info("===== Program exit =====")
    sys.exit(0)


if __name__ == "__main__":
    main()
