import cv2
import numpy as np
import onnxruntime as ort
import time
import os
import sys
import json
import logging
import math
import argparse
from datetime import datetime, timedelta, timezone
import re

DEFAULT_DATE = "2000-01-01"  # Default date for time-only strings


def parse_time(time_str: str) -> datetime:
    """
    Parse a time string and return a timezone-aware datetime object.
    Supports three formats:
      1) ISO UTC: "2024-03-25T06:00:00Z"
      2) CST local: "14:00:00 2024-03-25"  (UTC+8)
      3) Time only: "14:00:00"             (default date + CST)
    """
    # Format 1: ISO UTC ending with Z
    if time_str.endswith('Z') and 'T' in time_str:
        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    # Format 2: CST local "HH:MM:SS YYYY-MM-DD"
    pattern_full = r'^(\d{2}):(\d{2}):(\d{2}) (\d{4})-(\d{2})-(\d{2})$'
    match = re.match(pattern_full, time_str)
    if match:
        h, m, s, y, mo, d = map(int, match.groups())
        cst_tz = timezone(timedelta(hours=8))
        return datetime(y, mo, d, h, m, s, tzinfo=cst_tz)

    # Format 3: Time only "HH:MM:SS" (default date + CST)
    pattern_time = r'^(\d{2}):(\d{2}):(\d{2})$'
    match = re.match(pattern_time, time_str)
    if match:
        h, m, s = map(int, match.groups())
        cst_tz = timezone(timedelta(hours=8))
        y, mo, d = map(int, DEFAULT_DATE.split('-'))
        return datetime(y, mo, d, h, m, s, tzinfo=cst_tz)

    raise ValueError(f"Unsupported time format: {time_str}")


# ==================== Logging Configuration ====================
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, "yolo_world_onnx_log.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ------------------ Helper Functions ------------------
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
    boxes = []
    scores = []
    class_ids = []
    num_classes = len(class_names) if class_names is not None else output.shape[1] - 4
    for pred in output:
        bbox = pred[:4]
        cls_scores = pred[4:4+num_classes]
        max_score = np.max(cls_scores)
        if max_score > conf_threshold:
            class_id = np.argmax(cls_scores)
            boxes.append(bbox)
            scores.append(max_score)
            class_ids.append(class_id)
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
    if len(indices) > 0:
        return indices.flatten()
    return []


def get_color(class_id):
    colors = [
        (255, 0, 0),    # blue
        (0, 255, 0),    # green
        (0, 0, 255),    # red
        (255, 255, 0),  # cyan
        (255, 0, 255),  # magenta
        (0, 255, 255)   # yellow
    ]
    return colors[class_id % len(colors)]


def format_detection_result(class_name: str, bbox: list) -> dict:
    """Format a single detection result as a dictionary."""
    return {
        "class_name": class_name,
        "bbox": {"x1": int(bbox[0]), "y1": int(bbox[1]), "x2": int(bbox[2]), "y2": int(bbox[3])}
    }


def save_alarm_snapshot(frame: np.ndarray, detections: list, camera_name: str) -> str:
    """Draw bounding boxes on the frame and save it under snapshots/<camera_name>/.

    Args:
        frame: Original BGR frame (numpy array).
        detections: List of dicts, each with keys 'class_name', 'confidence', 'bbox'
                    (bbox = [x1, y1, x2, y2]).
        camera_name: Used as sub-directory name; sanitized for filesystem.

    Returns:
        Absolute path to the saved JPG file, or empty string on failure.
    """
    try:
        annotated = frame.copy()
        for det in detections:
            x1, y1, x2, y2 = [int(v) for v in det["bbox"]]
            cls = det.get("class_name", "object")
            conf = det.get("confidence", 0.0)
            color = (0, 0, 255)  # red, BGR
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            label = f"{cls} {conf:.2f}"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(annotated, (x1, max(0, y1 - th - 6)), (x1 + tw + 4, y1), color, -1)
            cv2.putText(annotated, label, (x1 + 2, max(th + 2, y1 - 4)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Sanitize camera name for filesystem (preserve Unicode like Chinese, only block path separators and null)
        safe_name = re.sub(r"[/\\\x00]", "_", str(camera_name) or "camera")
        snap_dir = os.path.join(script_dir, "snapshots", safe_name)
        os.makedirs(snap_dir, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # millisecond precision
        filename = f"{ts}.jpg"
        filepath = os.path.join(snap_dir, filename)
        ok = cv2.imwrite(filepath, annotated, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        return filepath if ok else ""
    except Exception as e:
        logging.getLogger("YOLO-World").warning(f"Failed to save snapshot: {e}")
        return ""


def compute_iou(box_a, box_b) -> float:
    """Compute IoU between two boxes [x1,y1,x2,y2]."""
    xa = max(box_a[0], box_b[0])
    ya = max(box_a[1], box_b[1])
    xb = min(box_a[2], box_b[2])
    yb = min(box_a[3], box_b[3])
    inter = max(0, xb - xa) * max(0, yb - ya)
    area_a = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    area_b = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0


def is_same_package(box_new, box_old, iou_threshold=0.5, size_ratio_threshold=0.3) -> bool:
    """Determine if two detections represent the same package.

    Returns True if the new detection overlaps significantly with the old one
    AND the size difference is small — i.e., likely the same package in the
    same position.

    Args:
        box_new: [x1, y1, x2, y2] of new detection
        box_old: [x1, y1, x2, y2] of previous detection
        iou_threshold: IoU above this → same location
        size_ratio_threshold: area ratio change below this → same size
    """
    iou = compute_iou(box_new, box_old)
    area_new = (box_new[2] - box_new[0]) * (box_new[3] - box_new[1])
    area_old = (box_old[2] - box_old[0]) * (box_old[3] - box_old[1])
    if area_old == 0:
        return False
    size_change = abs(area_new - area_old) / max(area_old, 1)
    # Same package: high overlap AND small size change
    return iou > iou_threshold and size_change < size_ratio_threshold


def _bbox_center(box) -> tuple:
    """Return (cx, cy) of a [x1,y1,x2,y2] bbox."""
    return ((box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0)


def match_tracked_package(box_new, tracked_box, iou_threshold=0.3,
                          center_dist_ratio=0.6, size_ratio_max=3.0) -> bool:
    """Robust same-package match that tolerates partial occlusion.

    A new detection is considered the SAME package as a tracked one if EITHER:
      (a) IoU is reasonably high (>= iou_threshold), OR
      (b) Their centers are close (relative to bbox size) AND the area ratio
          is within `size_ratio_max` (so a person occluding part of the box
          shrinks the detection but the center stays near the original).

    This is more lenient than `is_same_package` because tracking needs to
    survive transient bbox shape changes (occlusion, lighting, partial view).

    Args:
        box_new: [x1,y1,x2,y2] new detection bbox
        tracked_box: [x1,y1,x2,y2] previously tracked bbox
        iou_threshold: minimum IoU for direct match
        center_dist_ratio: max(center_dx, center_dy) / max(w, h) of tracked box
        size_ratio_max: max(area_new/area_old, area_old/area_new) tolerance
    """
    iou = compute_iou(box_new, tracked_box)
    if iou >= iou_threshold:
        return True

    # Fallback: center proximity + size sanity check
    cx_n, cy_n = _bbox_center(box_new)
    cx_t, cy_t = _bbox_center(tracked_box)
    w_t = max(1.0, tracked_box[2] - tracked_box[0])
    h_t = max(1.0, tracked_box[3] - tracked_box[1])
    ref = max(w_t, h_t)
    if ref <= 0:
        return False
    if abs(cx_n - cx_t) > ref * center_dist_ratio:
        return False
    if abs(cy_n - cy_t) > ref * center_dist_ratio:
        return False

    area_n = max(1.0, (box_new[2] - box_new[0]) * (box_new[3] - box_new[1]))
    area_t = max(1.0, w_t * h_t)
    ratio = max(area_n / area_t, area_t / area_n)
    return ratio <= size_ratio_max


# ── Stage 1 — Static frame detection (skip inference on unchanged frames) ───
class TransitionDetector:
    """Detect meaningful visual changes between frames.

    When consecutive frames are nearly identical (static scene), the detector
    returns False — allowing the main loop to skip expensive ONNX inference.
    Only when motion / change is detected does it return True.
    """

    def __init__(self, fps: float):
        self.prev_frame = None
        self.prev_diffs: list = []
        self.is_first = True
        # Adaptive threshold based on FPS (lower FPS → lower threshold)
        self.threshold = min(
            max((3.0 - 5.0) / (30.0 - 15.0) * (fps - 15.0) + 5.0, 3.0), 5.0
        )

    def _check(self, diff: float, window: int = 10) -> bool:
        vals = self.prev_diffs[max(0, len(self.prev_diffs) - window):]
        if not vals:
            return diff > self.threshold
        mean = sum(vals) / len(vals)
        std = math.sqrt(sum((v - mean) ** 2 for v in vals) / len(vals))
        return diff > (mean + std) * 2 and diff > self.threshold

    def detect(self, frame: np.ndarray) -> bool:
        """Return True if frame has meaningful change (should run inference)."""
        gray = cv2.cvtColor(cv2.resize(frame, (128, 128)), cv2.COLOR_BGR2GRAY)
        if self.is_first:
            self.is_first = False
            self.prev_frame = gray
            return True  # Always process the first frame
        diff = np.mean(np.abs(gray.astype(np.float32) - self.prev_frame.astype(np.float32)))
        has_change = self._check(diff)
        if has_change:
            self.prev_diffs = []
        else:
            self.prev_diffs.append(diff)
        self.prev_frame = gray
        return has_change


# ------------------ Configuration ------------------
DEFAULT_CLASS_NAMES = [
    "parcel", "package", "delivery box", "person",
    "Cardboard box", "Packaging Box", "backpack", "handbag", "suitcase",
]


def load_config():
    """Load config.json from the skill directory.

    Returns an empty dict if the file is missing or invalid. Empty / null
    field values are skipped so that argparse can fall back to its built-in
    defaults. This makes the script work both standalone (no config.json)
    and as part of the kami-smarthome-suite (suite distributes values into
    config.json via configure.py).

    Supports both legacy format (flat rtsp_url) and new multi-camera format
    (cameras array with device_id + rtsp_url per entry).
    """
    cfg_path = os.path.join(script_dir, "config.json")
    if not os.path.isfile(cfg_path):
        return {}
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            data = json.load(f) or {}
    except Exception as exc:
        logger.warning(f"Failed to read config.json, falling back to defaults: {exc}")
        return {}
    # Drop empty values so argparse defaults take over
    return {k: v for k, v in data.items() if v not in (None, "", [], {})}


def _resolve_camera(cfg: dict, device_id: str = None) -> dict:
    """Resolve camera configuration from config dict.

    Supports:
    - New format: cfg["cameras"] array, select by device_id or first entry
    - Legacy format: cfg["rtsp_url"] at top level

    Returns dict with at least {"rtsp_url": ..., "device_id": ...}.
    Per-camera overrides (conf_threshold, run_time) are merged if present.
    """
    cameras = cfg.get("cameras")
    if cameras and isinstance(cameras, list):
        if device_id:
            for cam in cameras:
                if cam.get("device_id") == device_id:
                    return cam
            # device_id not found — print error and exit
            available = [c.get("device_id", "?") for c in cameras]
            print(f"Error: DEVICE_ID '{device_id}' not found in config. "
                  f"Available: {available}", file=sys.stderr)
            sys.exit(1)
        else:
            return cameras[0]
    # Legacy format fallback
    return {"rtsp_url": cfg.get("rtsp_url", ""), "device_id": "CAM-001"}


def parse_args():
    cfg = load_config()
    parser = argparse.ArgumentParser(description='YOLO-World ONNX Object Detection')
    parser.add_argument('--device', type=str, default=None,
                        help='Target camera DEVICE_ID (selects from cameras array)')
    parser.add_argument('--rtsp_url', type=str, default=None,
                        help='RTSP camera URL (overrides camera selection)')
    parser.add_argument('--conf_threshold', type=float, default=None,
                        help='Confidence threshold')
    parser.add_argument('--class_names', type=str, nargs='+',
                        default=DEFAULT_CLASS_NAMES,
                        help='List of class names to detect (not distributed by suite)')
    parser.add_argument('--run_time', type=int, default=None,
                        help='Max run time in seconds, 0 for unlimited')
    parser.add_argument('--list-devices', action='store_true',
                        help='List all configured cameras and exit')
    parser.add_argument('--start-detect', action='store_true',
                        help='Start background detection (all cameras or --device)')
    parser.add_argument('--stop-detect', action='store_true',
                        help='Stop background detection (all cameras or --device)')
    parser.add_argument('--status', action='store_true',
                        help='Check detection process status')
    args = parser.parse_args()

    # Handle --list-devices
    if args.list_devices:
        cameras = cfg.get("cameras", [])
        if cameras:
            result = [{"device_id": c.get("device_id", "?"),
                       "rtsp_url": c.get("rtsp_url", "")} for c in cameras]
        else:
            result = [{"device_id": "CAM-001",
                       "rtsp_url": cfg.get("rtsp_url", "")}]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    # For daemon management commands, attach cfg and return early
    if args.start_detect or args.stop_detect or args.status:
        args._cfg = cfg
        return args

    # Resolve camera
    cam = _resolve_camera(cfg, args.device)

    # Determine final rtsp_url: CLI > camera entry > global config > built-in default
    if args.rtsp_url is None:
        rtsp_url = cam.get("rtsp_url") or cfg.get("rtsp_url") or ""
    else:
        rtsp_url = args.rtsp_url
    args.rtsp_url = rtsp_url

    # Determine conf_threshold: CLI > camera entry > global config > default
    if args.conf_threshold is None:
        args.conf_threshold = cam.get("conf_threshold") or cfg.get("conf_threshold", 0.25)

    # Determine run_time: CLI > camera entry > global config > default
    if args.run_time is None:
        args.run_time = cam.get("run_time") or cfg.get("run_time", 60)

    # Attach device_id to args for downstream use
    args.device_id = cam.get("device_id", "CAM-001")

    # Always attach cfg for notification config access
    args._cfg = cfg

    return args


# ==================== PID / Daemon Management ====================

import signal
import subprocess as _subprocess
from pathlib import Path


def _get_pid_dir(device_id: str) -> str:
    """PID directory for a camera: {script_dir}/run/{device_id}/"""
    d = os.path.join(script_dir, "run", device_id)
    Path(d).mkdir(parents=True, exist_ok=True)
    return d


def _get_pid_file(device_id: str) -> str:
    return os.path.join(_get_pid_dir(device_id), "detect.pid")


def _read_pid(pid_file: str):
    if not os.path.exists(pid_file):
        return None
    try:
        with open(pid_file, "r") as f:
            return int(f.read().strip())
    except (ValueError, OSError):
        return None


def _is_pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _start_daemon(cfg: dict, device_id: str, config_path: str) -> dict:
    """Start detection for a specific camera as a background process."""
    pid_file = _get_pid_file(device_id)
    existing_pid = _read_pid(pid_file)

    if existing_pid and _is_pid_alive(existing_pid):
        return {"status": "already_running", "pid": existing_pid,
                "device_id": device_id,
                "message": f"Detection already running (PID={existing_pid})"}

    # Prefer venv python
    venv_python = os.path.join(script_dir, ".venv", "bin", "python")
    if not os.path.exists(venv_python):
        venv_python = sys.executable

    cmd = [venv_python, os.path.abspath(__file__), "--device", device_id]

    proc = _subprocess.Popen(
        cmd, stdout=_subprocess.DEVNULL, stderr=_subprocess.DEVNULL,
        start_new_session=True,
    )

    with open(pid_file, "w") as f:
        f.write(str(proc.pid))

    return {"status": "started", "pid": proc.pid, "device_id": device_id,
            "message": f"Detection started (PID={proc.pid})"}


def _stop_daemon(device_id: str) -> dict:
    """Stop detection for a specific camera."""
    pid_file = _get_pid_file(device_id)
    pid = _read_pid(pid_file)

    if pid is None:
        return {"status": "not_running", "device_id": device_id,
                "message": "No running detection process found"}

    if not _is_pid_alive(pid):
        os.remove(pid_file)
        return {"status": "not_running", "device_id": device_id,
                "message": f"Process (PID={pid}) no longer exists, PID file cleaned up"}

    os.kill(pid, signal.SIGTERM)
    for _ in range(20):
        if not _is_pid_alive(pid):
            break
        time.sleep(0.5)

    if _is_pid_alive(pid):
        os.kill(pid, signal.SIGKILL)
        time.sleep(0.5)

    if os.path.exists(pid_file):
        os.remove(pid_file)

    return {"status": "stopped", "pid": pid, "device_id": device_id,
            "message": f"Detection stopped (PID={pid})"}


def _get_status(device_id: str) -> dict:
    """Get detection process status for a camera."""
    pid_file = _get_pid_file(device_id)
    pid = _read_pid(pid_file)

    if pid is None:
        return {"status": "not_running", "device_id": device_id,
                "message": "Detection not running"}

    if _is_pid_alive(pid):
        return {"status": "running", "pid": pid, "device_id": device_id,
                "message": f"Detection running (PID={pid})"}
    else:
        os.remove(pid_file)
        return {"status": "not_running", "device_id": device_id,
                "message": f"Process (PID={pid}) no longer exists, PID file cleaned up"}


def _get_all_cameras(cfg: dict) -> list:
    """Get list of camera dicts from config."""
    cameras = cfg.get("cameras")
    if cameras and isinstance(cameras, list):
        return cameras
    return [{"rtsp_url": cfg.get("rtsp_url", ""), "device_id": "CAM-001"}]


def main():
    args = parse_args()

    # ---- Daemon management commands ----
    if args.start_detect:
        cfg = args._cfg
        cameras = _get_all_cameras(cfg)
        if args.device:
            # Validate device exists
            _resolve_camera(cfg, args.device)
            result = _start_daemon(cfg, args.device, "")
        else:
            results = []
            for cam in cameras:
                r = _start_daemon(cfg, cam["device_id"], "")
                results.append(r)
            result = {"status": "ok", "cameras": results}
        print(json.dumps(result, ensure_ascii=False))
        return

    if args.stop_detect:
        cfg = args._cfg
        cameras = _get_all_cameras(cfg)
        if args.device:
            _resolve_camera(cfg, args.device)
            result = _stop_daemon(args.device)
        else:
            results = []
            for cam in cameras:
                r = _stop_daemon(cam["device_id"])
                results.append(r)
            result = {"status": "ok", "cameras": results}
        print(json.dumps(result, ensure_ascii=False))
        return

    if args.status:
        cfg = args._cfg
        cameras = _get_all_cameras(cfg)
        if args.device:
            _resolve_camera(cfg, args.device)
            result = _get_status(args.device)
        else:
            results = []
            for cam in cameras:
                r = _get_status(cam["device_id"])
                results.append(r)
            result = {"status": "ok", "cameras": results}
        print(json.dumps(result, ensure_ascii=False))
        return

    # ---- Foreground detection mode (continuous monitoring) ----
    from notifier import dispatch_alarm

    cfg = args._cfg
    VIDEO_PATH = args.rtsp_url
    ONNX_MODEL = os.path.join(script_dir, "yolov8s-worldv2.onnx")
    CONF_THRESHOLD = args.conf_threshold
    IOU_THRESHOLD = 0.45
    INPUT_SIZE = 320
    CLASS_NAMES = args.class_names
    max_run_time = args.run_time

    # Notification cooldown: avoid spamming (default 60 seconds between alarms)
    ALARM_COOLDOWN = cfg.get("alarm_cooldown", 60)

    # Signal handling for graceful stop
    _stop_requested = [False]

    def _signal_handler(sig, frame):
        logger.info("Received signal %s, stopping", signal.Signals(sig).name)
        _stop_requested[0] = True

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    # Clean up PID file on exit
    def _cleanup_pid():
        pid_file = _get_pid_file(args.device_id)
        if os.path.exists(pid_file):
            try:
                os.remove(pid_file)
            except OSError:
                pass

    import atexit
    atexit.register(_cleanup_pid)

    logger.info("===== Continuous monitoring started =====")
    logger.info(f"Device ID: {args.device_id}")
    logger.info(f"RTSP URL: {VIDEO_PATH}")
    logger.info(f"Model path: {ONNX_MODEL}")
    logger.info(f"Confidence threshold: {CONF_THRESHOLD}")
    logger.info(f"IOU threshold: {IOU_THRESHOLD}")
    logger.info(f"Input size: {INPUT_SIZE}")
    logger.info(f"Class names: {CLASS_NAMES}")
    logger.info(f"Alarm cooldown: {ALARM_COOLDOWN} seconds")
    if max_run_time > 0:
        logger.info(f"Max run time: {max_run_time} seconds")
    else:
        logger.info("Run time: unlimited (continuous monitoring)")

    # ------------------ Initialize ONNX Runtime ------------------
    if not os.path.exists(ONNX_MODEL):
        logger.error(f"Model file not found: {ONNX_MODEL}")
        sys.exit(1)

    logger.info(f"Loading model: {ONNX_MODEL}")
    try:
        session = ort.InferenceSession(ONNX_MODEL, providers=['CPUExecutionProvider'])
        input_name = session.get_inputs()[0].name
        logger.info("Model loaded successfully")
        logger.info(f"Input shape: {session.get_inputs()[0].shape}")
        logger.info(f"Output shape: {session.get_outputs()[0].shape}")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        sys.exit(1)

    # ------------------ Open Video ------------------
    logger.info(f"Opening video source: {VIDEO_PATH}")
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        logger.error(f"Cannot open video: {VIDEO_PATH}")
        sys.exit(1)

    logger.info("Video opened successfully")
    fps_val = cap.get(cv2.CAP_PROP_FPS) or 15.0
    logger.info(f"Resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    logger.info(f"FPS: {fps_val:.1f}")
    logger.info("Starting continuous monitoring...")

    # Initialize transition detector for static frame filtering
    trans_detector = TransitionDetector(fps_val)

    # ------------------ Main Loop (continuous) ------------------
    frame_count = 0
    skipped_static = 0
    total_fps = 0
    start_program_time = time.time()
    # Tracked packages: list of dicts {bbox, last_seen, alarm_time}
    # A package stays "tracked" as long as it keeps appearing within TRACK_TTL.
    # New alarms only fire for detections that match NO tracked package.
    tracked_packages: list = []
    TRACK_TTL = max(3600.0*24, float(ALARM_COOLDOWN) * 5)  # seconds — keep tracking long enough to outlive cooldowns and brief occlusions

    RECONNECT_DELAY = 5

    try:
        while not _stop_requested[0]:
            # Check timeout (only when run_time > 0)
            if max_run_time > 0 and (time.time() - start_program_time) > max_run_time:
                logger.info(f"Run time reached {max_run_time} seconds, exiting")
                break

            ret, frame = cap.read()
            if not ret:
                logger.warning("Stream lost — attempting reconnect...")
                cap.release()
                time.sleep(RECONNECT_DELAY)
                cap = cv2.VideoCapture(VIDEO_PATH)
                if not cap.isOpened():
                    logger.error("Reconnect failed, retrying...")
                    continue
                logger.info("Reconnected to stream")
                trans_detector = TransitionDetector(fps_val)
                continue

            frame_count += 1

            # ── Stage 1: Static frame detection ──────────────────────────
            # Skip inference on static (unchanged) frames
            if not trans_detector.detect(frame):
                skipped_static += 1
                if frame_count % 100 == 0:
                    logger.info(f"Monitoring: frame {frame_count}, "
                                f"skipped {skipped_static} static frames")
                continue

            # ── Stage 2: ONNX inference (only on changed frames) ─────────
            start_time = time.time()
            orig_shape = frame.shape[:2]

            # Preprocessing
            img, ratio, pad = letterbox(frame, INPUT_SIZE)
            img = img[:, :, ::-1].transpose(2, 0, 1)
            img = np.ascontiguousarray(img)
            img = img.astype(np.float32) / 255.0
            img = np.expand_dims(img, axis=0)

            # Inference
            outputs = session.run(None, {input_name: img})

            # Parse output
            if len(outputs) > 0:
                boxes, scores, class_ids = parse_output(outputs[0], CONF_THRESHOLD, CLASS_NAMES)

                if len(boxes) > 0:
                    boxes_scaled = scale_boxes(boxes, orig_shape, ratio, pad)
                    keep = nms(boxes_scaled, scores, IOU_THRESHOLD)

                    for i in keep:
                        x1, y1, x2, y2 = boxes_scaled[i]
                        conf = scores[i]
                        cls_id = class_ids[i]

                        # Notify when non-person target detected (package/delivery)
                        not_need_cls = ['person','handbag']
                        if CLASS_NAMES[cls_id].lower() not in not_need_cls:
                            now = time.time()
                            current_bbox = [int(x1), int(y1), int(x2), int(y2)]

                            # Prune expired entries (not seen for > TRACK_TTL)
                            tracked_packages = [
                                t for t in tracked_packages
                                if (now - t["last_seen"]) <= TRACK_TTL
                            ]

                            # Try to match against any currently tracked package.
                            # The matcher tolerates partial occlusion (center +
                            # lenient IoU) so a person walking past doesn't make
                            # us think the package is "new".
                            matched = None
                            for t in tracked_packages:
                                if match_tracked_package(current_bbox, t["bbox"]):
                                    matched = t
                                    break

                            if matched is not None:
                                # Same package, just refresh its last-seen time.
                                # Keep the original bbox stable to avoid drift
                                # caused by transient occlusion shrinking it.
                                matched["last_seen"] = now
                                continue

                            # No match → truly new (or moved) package.
                            # Apply cooldown against the most recent alarm.
                            last_alarm_time = max(
                                (t.get("alarm_time", 0.0) for t in tracked_packages),
                                default=0.0,
                            )
                            if (now - last_alarm_time) < ALARM_COOLDOWN:
                                logger.debug(
                                    f"New package detected but cooldown active, "
                                    f"class:{CLASS_NAMES[cls_id]}, conf:{conf:.2f}")
                                continue

                            # Register this new package and fire the alarm.
                            tracked_packages.append({
                                "bbox": current_bbox,
                                "last_seen": now,
                                "alarm_time": now,
                            })
                            logger.info(f"Package detected - frame:{frame_count}, "
                                        f"class:{CLASS_NAMES[cls_id]}, confidence:{conf:.2f}")

                            detection = format_detection_result(
                                CLASS_NAMES[cls_id], [x1, y1, x2, y2]
                            )
                            # Save annotated snapshot to snapshots/<camera_name>/<timestamp>.jpg
                            snapshot_path = save_alarm_snapshot(
                                frame,
                                [{
                                    "class_name": CLASS_NAMES[cls_id],
                                    "confidence": float(conf),
                                    "bbox": [x1, y1, x2, y2],
                                }],
                                args.device_id,
                            )
                            if snapshot_path:
                                logger.info(f"Snapshot saved: {snapshot_path}")

                            alarm = {
                                "alarm": True,
                                "type": "package",
                                "class_name": CLASS_NAMES[cls_id],
                                "confidence": float(conf),
                                "camera_name": args.device_id,
                                "frame": frame_count,
                                "snapshot": snapshot_path,
                                "detections": [detection],
                            }
                            # Print JSON to stdout (for upstream integration)
                            print(json.dumps(alarm, ensure_ascii=False), flush=True)
                            # Send notifications
                            dispatch_alarm(alarm, cfg, log=logger)

            # Calculate FPS
            elapsed = time.time() - start_time
            if elapsed > 0:
                fps = 1.0 / elapsed
                total_fps += fps

            # Print progress every 100 frames
            if frame_count % 100 == 0:
                avg_fps = total_fps / max(1, frame_count - skipped_static)
                logger.info(f"Monitoring: frame {frame_count}, "
                            f"skipped {skipped_static} static, Avg FPS: {avg_fps:.2f}")

    finally:
        cap.release()

    # Normal exit stats
    processed = frame_count - skipped_static
    avg_fps = total_fps / processed if processed > 0 else 0
    logger.info(f"Done! Total frames: {frame_count}, Processed: {processed}, "
                f"Skipped static: {skipped_static}, Avg FPS: {avg_fps:.2f}")
    logger.info("===== Program exit =====")


if __name__ == "__main__":
    main()
