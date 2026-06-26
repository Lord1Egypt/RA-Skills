"""
Unregistered Face Loitering Detector (Continuous Mode)
Architecture: RTSP stream -> SCRFD face detection -> ArcFace embedding -> Database matching -> Stranger tracking -> Alarm

Uses ONNX models directly (no insightface package dependency):
  - det_10g.onnx (SCRFD) for face detection + 5-point landmarks
  - w600k_r50.onnx (ArcFace) for 512-dim face embedding extraction

Cross-platform: works on Linux, macOS, and Windows with CPU inference.

Exit Codes:
  0 - Normal exit (run_time exceeded, video ended, user interrupt)
  1 - Runtime error
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
import pickle
import requests
from collections import deque
from datetime import datetime
from pathlib import Path

# ==================== Logging ====================
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, "suspicious_person.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger("suspicious_person")

# ==================== i18n: Push Notification Labels ====================
# Labels rendered in Feishu/Discord/Telegram alerts. The channel decides the
# language: Feishu uses Chinese, Discord/Telegram use English. The LLM-
# generated `message` text is NOT translated here (it comes from the remote
# API).
I18N = {
    "zh": {
        "title": "\U0001f575\ufe0f 陌生人停留告警",
        "camera": "摄像头",
        "stranger_id": "陌生人 ID",
        "duration": "停留时长",
        "hit_count": "检测次数",
        "time": "时间",
        "face_image": "人脸快照",
    },
    "en": {
        "title": "\U0001f575\ufe0f Stranger Loitering Alert",
        "camera": "Camera",
        "stranger_id": "Stranger ID",
        "duration": "Duration",
        "hit_count": "Hit Count",
        "time": "Time",
        "face_image": "Face Snapshot",
    },
}

# ==================== ArcFace alignment reference ====================
# Standard 5-point landmark positions for 112x112 aligned face
ARCFACE_REF = np.array([
    [38.2946, 51.6963],
    [73.5318, 51.5014],
    [56.0252, 71.7366],
    [41.5493, 92.3655],
    [70.7299, 92.2041],
], dtype=np.float32)


# ==================== Geometry Helpers ====================
def distance2bbox(points, distance):
    """Decode distance predictions to bounding boxes."""
    x1 = points[:, 0] - distance[:, 0]
    y1 = points[:, 1] - distance[:, 1]
    x2 = points[:, 0] + distance[:, 2]
    y2 = points[:, 1] + distance[:, 3]
    return np.stack([x1, y1, x2, y2], axis=-1)


def distance2kps(points, distance):
    """Decode distance predictions to keypoints."""
    preds = []
    for i in range(0, distance.shape[1], 2):
        px = points[:, i % 2] + distance[:, i]
        py = points[:, i % 2 + 1] + distance[:, i + 1]
        preds.append(px)
        preds.append(py)
    return np.stack(preds, axis=-1)


def nms(dets, iou_thres):
    """Pure numpy NMS."""
    x1, y1, x2, y2 = dets[:, 0], dets[:, 1], dets[:, 2], dets[:, 3]
    scores = dets[:, 4]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        ovr = (w * h) / (areas[i] + areas[order[1:]] - w * h)
        inds = np.where(ovr <= iou_thres)[0]
        order = order[inds + 1]
    return keep


def align_face(image, landmarks, image_size=112):
    """Align face using 5-point landmarks via OpenCV affine transform (no skimage needed)."""
    src = landmarks.astype(np.float32)
    dst = ARCFACE_REF.copy()
    if image_size != 112:
        dst = dst * (float(image_size) / 112.0)
    # Use partial affine (similarity transform) via cv2.estimateAffinePartial2D
    M, _ = cv2.estimateAffinePartial2D(src, dst)
    if M is None:
        # Fallback: simple affine from 3 points
        M = cv2.getAffineTransform(src[:3], dst[:3])
    warped = cv2.warpAffine(image, M, (image_size, image_size), borderValue=0.0)
    return warped


# ==================== Frame Grabber Thread ====================
class FrameGrabber:
    """Dedicated thread that continuously reads the RTSP stream, keeping only the latest frame."""

    def __init__(self, rtsp_url: str, fps: int = 15):
        self.cap = cv2.VideoCapture(rtsp_url)
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open video stream: {rtsp_url}")
        self.fps = fps
        self.is_local_file = not rtsp_url.startswith(("rtsp://", "http://", "https://"))
        self.latest_frame = None
        self.lock = threading.Lock()
        self.running = True
        self.frame_count = 0
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        mode_str = "local file (throttled)" if self.is_local_file else "live stream"
        logger.info(f"Frame grabber started, mode: {mode_str}, resolution: {self.width}x{self.height}")

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
                self.frame_count += 1
            if self.is_local_file:
                elapsed = time.time() - t0
                if elapsed < frame_interval:
                    time.sleep(frame_interval - elapsed)

    def get_latest_frame(self):
        with self.lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy(), self.frame_count
            return None, 0

    def stop(self):
        self.running = False
        self.thread.join(timeout=3)
        self.cap.release()
        logger.info("Frame grabber stopped")


# ==================== SCRFD Face Detector (ONNX) ====================
class SCRFDDetector:
    """SCRFD face detector using ONNX runtime directly. No insightface dependency."""

    def __init__(self, model_path: str, input_size=(640, 640), conf_thresh=0.5, iou_thresh=0.4):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"SCRFD model not found: {model_path}")
        file_size_mb = os.path.getsize(model_path) / (1024 * 1024)
        logger.info(f"Loading SCRFD model from {model_path} ({file_size_mb:.1f}MB)...")
        t0 = time.time()
        try:
            opts = ort.SessionOptions()
            opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_BASIC
            self.session = ort.InferenceSession(model_path, sess_options=opts, providers=["CPUExecutionProvider"])
        except Exception as e:
            logger.error(f"Failed to load SCRFD model: {e}")
            raise
        logger.info(f"SCRFD ONNX session created in {time.time() - t0:.1f}s")
        self.input_name = self.session.get_inputs()[0].name
        self.output_names = [o.name for o in self.session.get_outputs()]
        self.input_size = input_size  # (width, height)
        self.conf_thresh = conf_thresh
        self.iou_thresh = iou_thresh
        self.fmc = 3
        self.feat_strides = [8, 16, 32]
        self.num_anchors = 2
        self.center_cache = {}
        logger.info(f"SCRFD detector loaded: {model_path}, input_size={input_size}, conf={conf_thresh}")

    def detect(self, image):
        """
        Detect faces in image.
        Returns: (det, kpss)
          det: np.array shape (N, 5) — [x1, y1, x2, y2, score] in original image coords
          kpss: np.array shape (N, 5, 2) — 5-point landmarks in original image coords
        """
        width, height = self.input_size
        im_ratio = float(image.shape[0]) / image.shape[1]
        model_ratio = height / width
        if im_ratio > model_ratio:
            new_height = height
            new_width = int(new_height / im_ratio)
        else:
            new_width = width
            new_height = int(new_width * im_ratio)

        det_scale = float(new_height) / image.shape[0]
        resized = cv2.resize(image, (new_width, new_height))
        det_image = np.zeros((height, width, 3), dtype=np.uint8)
        det_image[:new_height, :new_width, :] = resized

        # Preprocess: blobFromImage with mean=127.5, std=128.0
        blob = cv2.dnn.blobFromImage(det_image, 1.0 / 128.0, (width, height),
                                     (127.5, 127.5, 127.5), swapRB=True)
        outputs = self.session.run(self.output_names, {self.input_name: blob})

        scores_list, bboxes_list, kpss_list = [], [], []
        for idx, stride in enumerate(self.feat_strides):
            scores = outputs[idx]
            bbox_preds = outputs[idx + self.fmc] * stride
            kps_preds = outputs[idx + self.fmc * 2] * stride

            h = height // stride
            w = width // stride
            key = (h, w, stride)
            if key in self.center_cache:
                anchor_centers = self.center_cache[key]
            else:
                anchor_centers = np.stack(np.mgrid[:h, :w][::-1], axis=-1).astype(np.float32)
                anchor_centers = (anchor_centers * stride).reshape((-1, 2))
                if self.num_anchors > 1:
                    anchor_centers = np.stack([anchor_centers] * self.num_anchors, axis=1).reshape((-1, 2))
                if len(self.center_cache) < 100:
                    self.center_cache[key] = anchor_centers

            pos_inds = np.where(scores >= self.conf_thresh)[0]
            bboxes = distance2bbox(anchor_centers, bbox_preds)
            kpss = distance2kps(anchor_centers, kps_preds).reshape((-1, 5, 2))
            scores_list.append(scores[pos_inds])
            bboxes_list.append(bboxes[pos_inds])
            kpss_list.append(kpss[pos_inds])

        if not scores_list or all(len(s) == 0 for s in scores_list):
            return np.empty((0, 5)), np.empty((0, 5, 2))

        scores = np.vstack(scores_list).ravel()
        bboxes = np.vstack(bboxes_list) / det_scale
        kpss = np.vstack(kpss_list) / det_scale

        order = scores.argsort()[::-1]
        pre_det = np.hstack((bboxes, scores[:, None])).astype(np.float32)
        pre_det = pre_det[order]
        kpss = kpss[order]

        keep = nms(pre_det, self.iou_thresh)
        return pre_det[keep], kpss[keep]


# ==================== ArcFace Embedding Extractor (ONNX) ====================
class ArcFaceEmbedder:
    """ArcFace face embedding extractor using ONNX runtime directly."""

    def __init__(self, model_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ArcFace model not found: {model_path}")
        file_size_mb = os.path.getsize(model_path) / (1024 * 1024)
        logger.info(f"Loading ArcFace model from {model_path} ({file_size_mb:.1f}MB)...")
        t0 = time.time()
        try:
            opts = ort.SessionOptions()
            opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_BASIC
            self.session = ort.InferenceSession(model_path, sess_options=opts, providers=["CPUExecutionProvider"])
        except Exception as e:
            logger.error(f"Failed to load ArcFace model: {e}")
            raise
        logger.info(f"ArcFace ONNX session created in {time.time() - t0:.1f}s")
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        input_shape = self.session.get_inputs()[0].shape
        self.input_size = tuple(input_shape[2:4][::-1])  # (w, h)
        self.input_mean = 127.5
        self.input_std = 127.5
        logger.info(f"ArcFace embedder loaded: {model_path}, input_size={self.input_size}")

    def get_embedding(self, image, landmarks):
        """
        Extract 512-dim L2-normalized embedding from a face.
        Args:
            image: original BGR frame
            landmarks: np.array shape (5, 2) — 5-point face landmarks
        Returns: np.array shape (512,) L2-normalized
        """
        aligned = align_face(image, landmarks, image_size=self.input_size[0])
        blob = cv2.dnn.blobFromImage(aligned, 1.0 / self.input_std, self.input_size,
                                     (self.input_mean, self.input_mean, self.input_mean),
                                     swapRB=True)
        embedding = self.session.run([self.output_name], {self.input_name: blob})[0].flatten()
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        return embedding


# ==================== Face Processor (combines detection + embedding) ====================
class FaceProcessor:
    """Combines SCRFD detection and ArcFace embedding into a single interface."""

    def __init__(self, det_model_path: str, rec_model_path: str,
                 det_size=(640, 640), det_thresh=0.5, min_face_size=40):
        self.detector = SCRFDDetector(det_model_path, input_size=det_size, conf_thresh=det_thresh)
        self.embedder = ArcFaceEmbedder(rec_model_path)
        self.min_face_size = min_face_size
        logger.info(f"Face processor initialized, min_face={min_face_size}px")

    def detect_and_extract(self, frame):
        """
        Detect faces and extract embeddings.
        Returns: list of {"bbox": [x1,y1,x2,y2], "embedding": np.array(512,), "face_img": np.array, "det_score": float}
        """
        det, kpss = self.detector.detect(frame)
        results = []
        for i in range(len(det)):
            bbox = det[i, :4].astype(int)
            score = float(det[i, 4])
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            if w < self.min_face_size or h < self.min_face_size:
                continue
            landmarks = kpss[i]
            embedding = self.embedder.get_embedding(frame, landmarks)

            # Crop face region with padding
            pad = int(max(w, h) * 0.2)
            y1 = max(0, bbox[1] - pad)
            y2 = min(frame.shape[0], bbox[3] + pad)
            x1 = max(0, bbox[0] - pad)
            x2 = min(frame.shape[1], bbox[2] + pad)
            face_img = frame[y1:y2, x1:x2].copy()

            results.append({
                "bbox": bbox.tolist(),
                "embedding": embedding,
                "face_img": face_img,
                "det_score": score,
            })
        return results


# ==================== Registered Face Database ====================
class FaceDatabase:
    """Manages the registered face embedding database."""

    def __init__(self, db_path: str, match_threshold: float = 0.4):
        self.match_threshold = match_threshold
        self.registered_faces = []
        self._load(db_path)

    def _load(self, db_path: str):
        pkl_path = os.path.join(db_path, "face_db.pkl")
        if os.path.exists(pkl_path):
            with open(pkl_path, "rb") as f:
                self.registered_faces = pickle.load(f)
            logger.info(f"Loaded face database from pkl: {len(self.registered_faces)} records")
            return

        if not os.path.isdir(db_path):
            logger.warning(f"Face database directory not found: {db_path}, running with empty database (all faces treated as strangers)")
            return

        logger.info("No face_db.pkl found. Use build_face_db.py to build the database first.")

    def match(self, embedding):
        if not self.registered_faces:
            return False, "", 0.0
        max_sim = -1.0
        matched_name = ""
        for record in self.registered_faces:
            sim = float(np.dot(embedding, record["embedding"]))
            if sim > max_sim:
                max_sim = sim
                matched_name = record["name"]
        is_registered = max_sim >= self.match_threshold
        return is_registered, matched_name, max_sim


# ==================== Stranger Tracker ====================
class StrangerTracker:
    """Cross-frame stranger tracking based on embedding similarity."""

    def __init__(self, match_threshold=0.35, expire_seconds=600, id_prefix="STR"):
        self.match_threshold = match_threshold
        self.expire_seconds = expire_seconds
        self.strangers = {}
        self._next_id = 1
        self.id_prefix = id_prefix

    def _gen_id(self):
        sid = f"{self.id_prefix}_{self._next_id:04d}"
        self._next_id += 1
        return sid

    def update(self, faces, now):
        expired = [sid for sid, rec in self.strangers.items()
                   if now - rec["last_seen"] > self.expire_seconds]
        for sid in expired:
            logger.info(f"Expired tracking record: {sid}")
            del self.strangers[sid]

        for face in faces:
            emb = face["embedding"]
            best_sid, best_sim = None, -1.0
            for sid, rec in self.strangers.items():
                sim = float(np.dot(emb, rec["avg_embedding"]))
                if sim > best_sim:
                    best_sim = sim
                    best_sid = sid

            if best_sid and best_sim >= self.match_threshold:
                rec = self.strangers[best_sid]
                rec["last_seen"] = now
                rec["hit_count"] += 1
                alpha = 0.3
                rec["avg_embedding"] = alpha * emb + (1 - alpha) * rec["avg_embedding"]
                rec["avg_embedding"] /= np.linalg.norm(rec["avg_embedding"])
                if face["det_score"] > rec["best_det_score"]:
                    rec["best_face_img"] = face["face_img"]
                    rec["best_det_score"] = face["det_score"]
            else:
                sid = self._gen_id()
                self.strangers[sid] = {
                    "avg_embedding": emb.copy(), "first_seen": now, "last_seen": now,
                    "best_face_img": face["face_img"], "best_det_score": face["det_score"],
                    "hit_count": 1, "alerted": False,
                }
                logger.info(f"New stranger detected: {sid}")

        return [{"stranger_id": sid, **rec} for sid, rec in self.strangers.items()]

    def mark_alerted(self, stranger_id):
        if stranger_id in self.strangers:
            self.strangers[stranger_id]["alerted"] = True


# ==================== Alert Delivery: Inbox file + Feishu push ====================
def append_inbox(inbox_path: str, alert: dict):
    """Append alert JSON line to inbox file for LLM heartbeat to consume."""
    try:
        os.makedirs(os.path.dirname(inbox_path), exist_ok=True)
        with open(inbox_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(alert, ensure_ascii=False) + "\n")
        logger.info(f"Alert appended to inbox: {inbox_path}")
    except Exception as e:
        logger.error(f"Failed to append inbox {inbox_path}: {e}")


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
    quota applies. Used by the Feishu push to obtain a clickable image URL
    because Feishu custom-bot cards cannot render external image URLs inline.
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


def _feishu_sign(secret: str, timestamp: int) -> str:
    """Generate Feishu webhook signature (HMAC-SHA256, base64)."""
    import hmac
    import hashlib
    import base64
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    return base64.b64encode(hmac_code).decode("utf-8")


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

    No-op if webhook_url is empty. Failures are logged but do not stop detection.

    Image rendering strategy:
      1. If app_id + app_secret are provided, upload face snapshot to Feishu
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
        face_local = alert.get("face_image", "")

        # --- Attempt to get a renderable image_key ---
        image_key = ""
        face_url = ""
        if face_local and app_id and app_secret:
            image_key = _feishu_upload_image(app_id, app_secret, face_local)
        # Fallback: public image host URL
        if not image_key and face_local:
            face_url = _upload_image_to_imghost(face_local)

        # Build the face display in lark_md
        if image_key:
            face_md = "(\u89c1\u4e0b\u65b9\u56fe\u7247)"  # "(见下方图片)"
        elif face_url:
            face_md = f"[\u67e5\u770b\u4eba\u8138\u5feb\u7167]({face_url})"
        elif face_local:
            face_md = f"`{face_local}`"
        else:
            face_md = "-"

        content_md = (
            f"**{t['camera']}**: {alert.get('camera', '-')}\n"
            f"**{t['stranger_id']}**: {alert.get('stranger_id', '')}\n"
            f"**{t['duration']}**: {alert.get('duration_display', '')} ({alert.get('duration_seconds', 0)}s)\n"
            f"**{t['hit_count']}**: {alert.get('hit_count', 0)}\n"
            f"**{t['time']}**: {_format_ts(alert.get('timestamp', ''))}\n"
            f"**{t['face_image']}**: {face_md}"
        )

        elements = [
            {"tag": "div", "text": {"tag": "lark_md", "content": content_md}},
        ]
        # If we have an image_key, insert an img element right after the text
        if image_key:
            elements.append({
                "tag": "img",
                "img_key": image_key,
                "alt": {"tag": "plain_text", "content": t["face_image"]},
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

    No-op if webhook_url is empty. Failures are logged but do not stop detection.
    Uses ``requests`` for robust HTTPS proxy support.
    """
    if not webhook_url:
        return
    t = I18N["en"]  # Discord channel always uses English labels
    try:
        camera = alert.get("camera", "-")
        stranger_id = alert.get("stranger_id", "")
        duration_display = alert.get("duration_display", "")
        duration_seconds = alert.get("duration_seconds", 0)
        hit_count = alert.get("hit_count", 0)
        timestamp = _format_ts(alert.get("timestamp", ""))
        face_image = alert.get("face_image", "")
        message = alert.get("message", "")
        embed = {
            "title": t["title"],
            "color": 15158332,  # 0xE74C3C red
            "fields": [
                {"name": t["camera"], "value": camera or "-", "inline": True},
                {"name": t["stranger_id"], "value": stranger_id or "-", "inline": True},
                {"name": t["duration"], "value": f"{duration_display} ({duration_seconds}s)" if duration_display else "-", "inline": True},
                {"name": t["hit_count"], "value": str(hit_count), "inline": True},
                {"name": t["time"], "value": timestamp or "-", "inline": False},
            ],
            "footer": {"text": message},
        }
        headers = {"User-Agent": "KamiSuspiciousPersonDetector/3.0"}
        proxies = {"https": proxy, "http": proxy} if proxy else None
        # If the face snapshot exists locally, attach it via multipart so the
        # image renders inline inside the embed (no public URL required).
        if face_image and os.path.isfile(face_image):
            filename = os.path.basename(face_image)
            embed["image"] = {"url": f"attachment://{filename}"}
            payload = {"embeds": [embed]}
            with open(face_image, "rb") as f:
                file_bytes = f.read()
            files = {"files[0]": (filename, file_bytes, "image/jpeg")}
            data = {"payload_json": json.dumps(payload, ensure_ascii=False)}
            resp = requests.post(webhook_url, data=data, files=files,
                                 headers=headers, proxies=proxies, timeout=10)
        else:
            embed["fields"].append({
                "name": t["face_image"],
                "value": f"`{face_image}`" if face_image else "-",
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
    """Push alarm to a Telegram chat via Bot API sendMessage.

    No-op if bot_token or chat_id is empty. Failures are logged but do not stop detection.
    Uses HTML parse_mode (more forgiving than Markdown with special chars).
    """
    if not bot_token or not chat_id:
        return
    t = I18N["en"]  # Telegram channel always uses English labels
    try:
        from html import escape as html_escape
        camera = html_escape(alert.get("camera", "") or "-")
        stranger_id = html_escape(alert.get("stranger_id", "") or "-")
        duration_display = html_escape(alert.get("duration_display", "") or "-")
        duration_seconds = alert.get("duration_seconds", 0)
        hit_count = alert.get("hit_count", 0)
        timestamp = html_escape(_format_ts(alert.get("timestamp", "")) or "-")
        face_image = alert.get("face_image", "") or ""
        message = html_escape(alert.get("message", "") or "")
        text = (
            f"<b>{html_escape(t['title'])}</b>\n\n"
            f"<b>{html_escape(t['camera'])}</b>: {camera}\n"
            f"<b>{html_escape(t['stranger_id'])}</b>: {stranger_id}\n"
            f"<b>{html_escape(t['duration'])}</b>: {duration_display} ({duration_seconds}s)\n"
            f"<b>{html_escape(t['hit_count'])}</b>: {hit_count}\n"
            f"<b>{html_escape(t['time'])}</b>: {timestamp}\n\n"
            f"<i>{message}</i>"
        )
        headers = {"User-Agent": "KamiSuspiciousPersonDetector/3.0"}
        proxies = {"https": proxy, "http": proxy} if proxy else None
        # If the face snapshot exists locally, push via sendPhoto so the image
        # is rendered inline; the formatted text is attached as the caption.
        if face_image and os.path.isfile(face_image):
            url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
            with open(face_image, "rb") as f:
                file_bytes = f.read()
            files = {"photo": (os.path.basename(face_image), file_bytes, "image/jpeg")}
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
                + f"\n<b>{html_escape(t['face_image'])}</b>: "
                + f"<code>{html_escape(face_image or '-')}</code>"
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


# Target pixel size for the longest side of saved face snapshots.
# Ensures consistent display dimensions across all push notification channels.
FACE_SNAPSHOT_SIZE = 320


# ==================== Alert Output ====================
def save_alert(stranger_record, output_dir):
    """Save alert info: face snapshot + JSON. Returns alert dict."""
    os.makedirs(output_dir, exist_ok=True)
    sid = stranger_record["stranger_id"]
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    face_filename = f"{sid}_{timestamp_str}.jpg"
    face_path = os.path.join(output_dir, face_filename)

    # Resize face snapshot so the longest side equals FACE_SNAPSHOT_SIZE,
    # keeping aspect ratio to avoid distortion.
    face = stranger_record["best_face_img"]
    h, w = face.shape[:2]
    if max(h, w) > 0:
        scale = FACE_SNAPSHOT_SIZE / max(h, w)
        new_w = int(w * scale)
        new_h = int(h * scale)
        interp = cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR
        face = cv2.resize(face, (new_w, new_h), interpolation=interp)
    cv2.imwrite(face_path, face)

    duration = stranger_record["last_seen"] - stranger_record["first_seen"]
    minutes = int(duration // 60)
    seconds = int(duration % 60)

    return {
        "alarm": True,
        "type": "stranger_loitering",
        "timestamp": datetime.now().isoformat(),
        "stranger_id": sid,
        "duration_seconds": round(duration, 1),
        "duration_display": f"{minutes}m{seconds}s",
        "face_image": face_path,
        "hit_count": stranger_record["hit_count"],
        "message": f"Warning: Stranger {sid} detected loitering for {minutes}m{seconds}s. Snapshot: {face_path}.",
    }


# ==================== Model Auto-Discovery ====================
def find_model(models_dir, filename):
    """Search for an ONNX model file in models_dir and its subdirectories."""
    # Direct path
    direct = os.path.join(models_dir, filename)
    if os.path.isfile(direct):
        return direct
    # Search subdirectories (e.g., models/kami-suspicious-person-model/det_10g.onnx)
    for root, dirs, files in os.walk(models_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None


# ==================== Face DB Path ====================
# The face database lives at a fixed location next to this script:
#     <skill_dir>/face_db/
# It is shared by ALL cameras (single FaceDatabase instance loaded once).
# Users only need to put photos under face_db/<person_name>/*.jpg; if the
# directory is empty or missing, every detected face is treated as a
# stranger.
FACE_DB_DIR = os.path.join(script_dir, "face_db")


def resolve_cameras(args, cfg: dict) -> list:
    """Build the list of camera configs to monitor.

    Resolution priority:
      1) CLI ``--rtsp_url`` → single-camera mode (name=camera_0).
      2) ``cfg['cameras']`` array → each entry may have ``name`` and
         ``rtsp_url``. Name auto-assigned as ``camera_<idx>`` when missing
         or empty.
      3) Legacy: ``cfg['rtsp_url']`` at top level → single-camera mode.

    Returns a list of dicts with normalized fields: ``{name, rtsp_url}``.
    The shared face_db lives at the fixed location ``<skill_dir>/face_db``.
    """
    cameras = []
    if args.rtsp_url:
        cameras.append({
            "name": "camera_0",
            "rtsp_url": args.rtsp_url,
        })
        return cameras

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
            cameras.append({
                "name": name,
                "rtsp_url": url,
            })
        return cameras

    legacy_url = (cfg.get("rtsp_url") or "").strip()
    if legacy_url:
        cameras.append({
            "name": "camera_0",
            "rtsp_url": legacy_url,
        })
    return cameras


# ==================== Per-Camera Detection Worker ====================
def run_camera_worker(cam, args, face_processor, face_db, inference_lock, stop_event):
    """Detection worker thread for a single camera.

    All cameras share ``face_processor`` (one ONNX model set). Inference is
    serialized via ``inference_lock`` so concurrent CPU sessions do not
    thrash. Each camera owns an independent FrameGrabber, StrangerTracker,
    cooldown table and snapshot subdirectory.
    """
    name = cam["name"]
    url = cam["rtsp_url"]
    cam_output_dir = os.path.join(args.output_dir, name)
    os.makedirs(cam_output_dir, exist_ok=True)

    tracker = StrangerTracker(
        match_threshold=args.stranger_match_threshold,
        expire_seconds=args.expire_seconds,
        id_prefix=f"{name}_STR",
    )
    alert_cooldowns = {}
    last_sample_time = 0.0
    start_time = time.time()

    try:
        grabber = FrameGrabber(url, fps=args.fps)
    except Exception as e:
        logger.error(f"[{name}] failed to open stream {url}: {e}")
        return

    logger.info(f"[{name}] worker started, stream={url}")

    try:
        while grabber.running and not stop_event.is_set():
            if args.run_time > 0 and (time.time() - start_time) > args.run_time:
                logger.info(f"[{name}] run_time {args.run_time}s reached, exiting worker")
                break

            frame, frame_count = grabber.get_latest_frame()
            if frame is None:
                time.sleep(0.01)
                continue

            now = time.time()
            if now - last_sample_time < args.sample_interval:
                time.sleep(0.01)
                continue
            last_sample_time = now

            # Shared model: serialize inference to avoid CPU contention.
            with inference_lock:
                faces = face_processor.detect_and_extract(frame)

            if not faces:
                if frame_count <= 3:
                    logger.info(f"[{name}] frame {frame_count}: no faces detected (detection working)")
                continue

            stranger_faces = []
            for face in faces:
                is_registered, matched_name, sim = face_db.match(face["embedding"])
                if is_registered:
                    logger.debug(f"[{name}] registered person: {matched_name} (sim={sim:.3f})")
                else:
                    stranger_faces.append(face)

            if not stranger_faces:
                continue

            logger.info(f"[{name}] detected {len(stranger_faces)} stranger face(s) (frame {frame_count})")
            active_strangers = tracker.update(stranger_faces, now)

            for rec in active_strangers:
                sid = rec["stranger_id"]
                duration = rec["last_seen"] - rec["first_seen"]
                if duration < args.loiter_threshold:
                    continue
                last_alert = alert_cooldowns.get(sid, 0)
                if now - last_alert < args.cooldown:
                    continue
                alert = save_alert(rec, cam_output_dir)
                alert["camera"] = name
                # Append camera prefix to message for visibility in stdout/inbox
                alert["message"] = f"[{name}] " + alert.get("message", "")
                print(json.dumps(alert, ensure_ascii=False), flush=True)
                # Quad-channel delivery (shared push channels across all cameras):
                #   1) inbox file consumed by the LLM heartbeat
                #   2) Feishu push (Chinese)
                #   3) Discord push (English)
                #   4) Telegram push (English)
                append_inbox(args.inbox_file, alert)
                send_feishu(args.feishu_webhook, alert, secret=args.feishu_secret,
                                            app_id=args.feishu_app_id, app_secret=args.feishu_app_secret)
                send_discord(args.discord_webhook, alert, proxy=args.proxy)
                send_telegram(args.telegram_bot_token, args.telegram_chat_id, alert, proxy=args.proxy)
                logger.warning(f"[{name}] stranger loitering alarm: {sid}, duration {alert['duration_display']}")
                alert_cooldowns[sid] = now
                tracker.mark_alerted(sid)
    except Exception as e:
        logger.exception(f"[{name}] worker crashed: {e}")
    finally:
        grabber.stop()
        logger.info(f"[{name}] worker stopped")


# ==================== Argument Parsing ====================
def parse_args():
    parser = argparse.ArgumentParser(description="Unregistered face loitering detection (continuous mode, ONNX)")
    parser.add_argument("--rtsp_url", type=str, default="", help="RTSP stream URL or local video file path. "
                        "For multi-camera mode, leave empty and configure 'cameras' array in config.json.")
    parser.add_argument("--face_db", type=str, default=FACE_DB_DIR,
                        help="Registered face database directory. Defaults to "
                             "'<skill_dir>/face_db'. Place per-person photo "
                             "folders inside; if the directory is empty or "
                             "missing, every detected face is treated as a "
                             "stranger.")
    parser.add_argument("--det_model", type=str, default=None,
                        help="SCRFD detection model path (auto-detected from models/)")
    parser.add_argument("--rec_model", type=str, default=None,
                        help="ArcFace recognition model path (auto-detected from models/)")
    parser.add_argument("--db_match_threshold", type=float, default=0.4)
    parser.add_argument("--stranger_match_threshold", type=float, default=0.35)
    parser.add_argument("--loiter_threshold", type=int, default=None,
                        help="Loitering alert threshold in seconds (default 300 = 5 minutes; can also be set in config.json)")
    parser.add_argument("--sample_interval", type=float, default=2.0)
    parser.add_argument("--cooldown", type=int, default=300,
                        help="Per-stranger alert cooldown in seconds")
    parser.add_argument("--det_thresh", type=float, default=0.5)
    parser.add_argument("--min_face_size", type=int, default=40)
    parser.add_argument("--output_dir", type=str, default=os.path.join(script_dir, "alerts"))
    parser.add_argument("--run_time", type=int, default=0, help="Max run time in seconds, 0 = unlimited")
    parser.add_argument("--fps", type=int, default=15)
    parser.add_argument("--expire_seconds", type=int, default=600)
    # --- Alarm delivery channels ---
    parser.add_argument("--inbox_file", type=str,
                        default=os.path.join(script_dir, "alerts", "pending.jsonl"),
                        help="Alarm inbox file (JSON lines). Consumed by LLM heartbeat task.")
    parser.add_argument("--feishu_webhook", type=str,
                        default="",
                        help="Feishu custom bot webhook URL (or set in config.json).")
    parser.add_argument("--feishu_secret", type=str,
                        default="",
                        help="Feishu webhook signing secret (optional).")
    parser.add_argument("--feishu_app_id", type=str,
                        default="",
                        help="Feishu self-built app ID. Required for inline image rendering in cards.")
    parser.add_argument("--feishu_app_secret", type=str,
                        default="",
                        help="Feishu self-built app secret. Required for inline image rendering in cards.")
    parser.add_argument("--discord_webhook", type=str,
                        default="",
                        help="Discord channel webhook URL (or set in config.json).")
    parser.add_argument("--telegram_bot_token", type=str,
                        default="",
                        help="Telegram Bot token from @BotFather (or set in config.json).")
    parser.add_argument("--telegram_chat_id", type=str,
                        default="",
                        help="Telegram target chat/group ID (or set in config.json).")
    parser.add_argument("--proxy", type=str,
                        default="",
                        help="HTTPS proxy for Discord/Telegram push. "
                             "Example: http://127.0.0.1:7890. Not used for Feishu.")
    return parser.parse_args()


# ==================== Main Loop ====================
def load_config() -> dict:
    """Load persistent configuration from config.json next to this script.

    Returns an empty dict if the file is missing or invalid. Values written here
    are user-provided (e.g., RTSP URL, push channel credentials), so the user
    does not have to pass them on the command line each time.
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

    # Merge args and config.json: command-line wins; otherwise fall back to
    # config.json. This lets users persist credentials in config.json instead
    # of passing them on the command line every run.
    args.feishu_webhook = (args.feishu_webhook or cfg.get("feishu_webhook", "")).strip()
    args.feishu_secret = (args.feishu_secret or cfg.get("feishu_secret", "")).strip()
    args.feishu_app_id = (args.feishu_app_id or cfg.get("feishu_app_id", "")).strip()
    args.feishu_app_secret = (args.feishu_app_secret or cfg.get("feishu_app_secret", "")).strip()
    args.discord_webhook = (args.discord_webhook or cfg.get("discord_webhook", "")).strip()
    args.telegram_bot_token = (args.telegram_bot_token or cfg.get("telegram_bot_token", "")).strip()
    args.telegram_chat_id = (args.telegram_chat_id or cfg.get("telegram_chat_id", "")).strip()

    # loiter_threshold: CLI int > config.json int > built-in default 300
    if args.loiter_threshold is None:
        cfg_loiter = cfg.get("loiter_threshold", "")
        if isinstance(cfg_loiter, (int, float)):
            args.loiter_threshold = int(cfg_loiter)
        elif isinstance(cfg_loiter, str) and cfg_loiter.strip():
            try:
                args.loiter_threshold = int(cfg_loiter.strip())
            except ValueError:
                logger.warning(f"Invalid loiter_threshold in config.json: {cfg_loiter!r}, falling back to 300")
                args.loiter_threshold = 300
        else:
            args.loiter_threshold = 300

    # ---- Resolve cameras to monitor (single-camera CLI / multi-camera config) ----
    cameras = resolve_cameras(args, cfg)
    if not cameras:
        logger.error("No camera configured. Pass --rtsp_url, or set 'cameras' (or legacy 'rtsp_url') in config.json")
        sys.exit(1)

    # The face database lives at the fixed location <skill_dir>/face_db (or
    # whatever the CLI override points to). Shared by all cameras.
    face_db_path = args.face_db or FACE_DB_DIR

    # ---- Auto-download models if not present ----
    models_dir = os.path.join(script_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    det_needed = "det_10g.onnx"
    rec_needed = "w600k_r50.onnx"
    if not find_model(models_dir, det_needed) or not find_model(models_dir, rec_needed):
        model_url = "https://publicfiles.xiaoyi.com/kami-suspicious-person-model.zip"
        zip_path = os.path.join(models_dir, "kami-suspicious-person-model.zip")
        logger.info(f"Models not found, downloading from {model_url} ...")
        import urllib.request
        import zipfile
        import shutil
        try:
            urllib.request.urlretrieve(model_url, zip_path)
            logger.info(f"Download complete, extracting...")
            extract_dir = os.path.join(script_dir, "kami-suspicious-person-model")
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(script_dir)
            # Move .onnx files from extracted folder to models/
            if os.path.isdir(extract_dir):
                for fname in os.listdir(extract_dir):
                    if fname.endswith(".onnx"):
                        src = os.path.join(extract_dir, fname)
                        dst = os.path.join(models_dir, fname)
                        shutil.move(src, dst)
                shutil.rmtree(extract_dir, ignore_errors=True)
            os.remove(zip_path)
            logger.info("Models extracted successfully")
        except Exception as e:
            logger.error(f"Failed to download/extract models: {e}")
            logger.error(f"Please manually download from {model_url} and place .onnx files into {models_dir}/")
            sys.exit(1)

    # Resolve model paths (auto-discover from models/ directory)
    det_model = args.det_model or find_model(models_dir, "det_10g.onnx")
    rec_model = args.rec_model or find_model(models_dir, "w600k_r50.onnx")
    if not det_model or not os.path.isfile(det_model):
        logger.error(f"SCRFD model not found. Searched in {models_dir}. Run setup.sh or provide --det_model")
        sys.exit(1)
    if not rec_model or not os.path.isfile(rec_model):
        logger.error(f"ArcFace model not found. Searched in {models_dir}. Run setup.sh or provide --rec_model")
        sys.exit(1)

    logger.info("===== Stranger Loitering Detection Started (Multi-Camera, Shared-Model Mode) =====")
    logger.info(f"Cameras to monitor ({len(cameras)}):")
    for cam in cameras:
        logger.info(f"  - {cam['name']}: {cam['rtsp_url']}")
    logger.info(f"Shared face database: {face_db_path}")
    logger.info(f"Detection model: {det_model}")
    logger.info(f"Recognition model: {rec_model}")
    logger.info(f"Loiter threshold: {args.loiter_threshold}s, cooldown: {args.cooldown}s, sample_interval: {args.sample_interval}s")

    # Initialize models ONCE; all cameras share this single FaceProcessor instance.
    logger.info("Loading SCRFD + ArcFace models (shared across all cameras)...")
    face_processor = FaceProcessor(
        det_model_path=det_model,
        rec_model_path=rec_model,
        det_thresh=args.det_thresh,
        min_face_size=args.min_face_size,
    )
    logger.info("Models loaded successfully")

    # Single shared FaceDatabase instance across all cameras.
    face_db = FaceDatabase(face_db_path, match_threshold=args.db_match_threshold)
    logger.info(f"Loaded shared face database from {face_db_path}")

    # Inference lock: ONNX Runtime sessions are thread-safe for Run(), but
    # concurrent CPU inference across N camera threads thrashes the cores.
    # Serializing inference keeps latency predictable per camera.
    inference_lock = threading.Lock()
    stop_event = threading.Event()

    workers = []
    for cam in cameras:
        t = threading.Thread(
            target=run_camera_worker,
            args=(cam, args, face_processor, face_db, inference_lock, stop_event),
            name=f"worker-{cam['name']}",
            daemon=True,
        )
        t.start()
        workers.append(t)

    overall_start = time.time()
    try:
        # Wait for all workers; if all of them exit (e.g. local file ended or
        # run_time reached on every camera), drop out of the wait loop.
        while True:
            alive = [t for t in workers if t.is_alive()]
            if not alive:
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("User interrupted, signalling all workers to stop...")
        stop_event.set()
        for t in workers:
            t.join(timeout=5)

    result = {
        "alarm": False,
        "type": None,
        "detail": "All camera workers exited",
        "run_seconds": round(time.time() - overall_start, 1),
        "cameras": [c["name"] for c in cameras],
    }
    print(json.dumps(result, ensure_ascii=False), flush=True)
    logger.info("===== Stranger Loitering Detection Ended =====")
    sys.exit(0)


if __name__ == "__main__":
    main()
