#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stream_recorder.py

Real-time stream recording + description generation + vector search module

Features:
  1. Pull RTSP/RTMP/HTTP streams, save as configurable-duration segments
  2. Generate VLM description + embedding for each segment
  3. Support text-based video clip search
  4. Automatic cleanup of expired data

Usage:
  python stream_recorder.py                        # Start recording
  python stream_recorder.py --search "someone entered"  # Search mode
"""

import requests as http_requests
import os
import sys
import json
import time
import signal
import logging
import argparse
import threading
import numpy as np
from pathlib import Path
import base64
import requests
import sqlite3
from datetime import datetime, timedelta, timezone
from collections import deque
from typing import Optional, List, Dict, Tuple

# ============================================================
# LOGGING — Unified logging configuration
# ============================================================

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def file_to_base64(file_path):
    """
    Convert a file to a base64-encoded string.

    Args:
        file_path: Path to the file

    Returns:
        Base64-encoded string
    """
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def setup_logging(level: int = logging.INFO, log_file: str = None):
    """
    Initialize logging. Output to both stderr and an optional log file.
    """
    root = logging.getLogger()
    root.setLevel(level)
    # Avoid adding duplicate handlers
    if root.handlers:
        return

    fmt = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # Console
    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(fmt)
    root.addHandler(console)

    # File (overwrite on each start)

    if log_file:
        fh = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        fh.setFormatter(fmt)
        root.addHandler(fh)


logger = logging.getLogger("stream_recorder")

# ============================================================
# CONFIG — All configurable parameters centralized here
# ============================================================


class Config:
    # --- Stream ---
    STREAM_URL: str = "rtsp://admin:password@192.168.1.100:554/stream1"
    DEVICE_ID: str = "CAM-001"

    # --- Segmentation ---
    SEGMENT_DURATION: int = 10          # Segment duration in seconds
    OUTPUT_WIDTH: int = 640
    OUTPUT_HEIGHT: int = 360

    # --- Timestamp ---
    # "ntp" uses system clock, "pts" uses stream PTS
    TIMESTAMP_SOURCE: str = "ntp"

    # --- VLM Description ---
    VLM_PROMPT: str = ""                # Custom prompt, empty uses default
    ENABLE_DESCRIPTION: bool = True     # Whether to generate descriptions
    # Skip static frames (frame diff detection)
    SKIP_STATIC: bool = True
    # Frame diff mean below this is considered static
    STATIC_THRESHOLD: float = 5.0

    # --- Kamivision API ---
    # Kamivision API endpoint
    KAMI_API_URL: str = "https://kamiclaw-skill-api.kamihome.com/v1/detect"
    KAMI_API_KEY: str = ""              # Kamivision API key
    KAMI_API_RETRY: int = 3             # API call retry count
    # Video description endpoint
    SUMMARY_DETECT_TYPE: str = "SUMMARY"    # Video description detectType
    SUMMARY_DETECT_SUB_TYPE: str = ""       # Video description detectSubType
    SUMMARY_PROMPT: str = ""                # Video description prompt
    # Upload mode: "image"=extracted frames, "video"=full video file
    SUMMARY_UPLOAD_MODE: str = "image"
    SUMMARY_SAMPLE_FPS: int = 1             # Frames per second in image mode
    # Text Embedding endpoint
    EMBED_DETECT_TYPE: str = "EMBED"        # Embedding detectType
    EMBED_DETECT_SUB_TYPE: str = ""         # Embedding detectSubType

    # --- Search ---
    EMBEDDING_DIM: int = 2048           # Embedding dimension
    SIMILARITY_THRESHOLD: float = 0.35
    SEARCH_TOP_K: int = 5
    LIST_TOP_K: int = 50              # Max results for list_recent

    # --- Storage ---
    DATA_DIR: str = "stream_data"       # Root storage directory
    RETENTION_DAYS: int = 3             # Data retention days, 0=keep forever
    INDEX_FILE: str = "index.db"        # Index database filename
    PROCESS_WORKERS: int = 5            # Segment processing worker threads

    # --- Reconnection ---
    RECONNECT_DELAY: int = 3            # Reconnect delay (seconds)
    MAX_RECONNECT: int = 0              # Max reconnect attempts, 0=unlimited
    skillId: str = "SK_VIDEO_SEARCH"    # Kamivision API skillId
    # Log file path, empty = script directory/stream_recorder.log
    LOG_FILE: str = ""

    # --- Multi-camera ---
    cameras: List[Dict] = None          # Camera list from config

    @classmethod
    def from_json(cls, path: str) -> "Config":
        """Load config from JSON file, use defaults for unspecified fields"""
        cfg = cls()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in data.items():
                if hasattr(cfg, k):
                    setattr(cfg, k, v)
        return cfg

    def to_json(self, path: str):
        """Export current config to JSON"""
        data = {k: v for k, v in vars(self.__class__).items()
                if not k.startswith("_") and not callable(v)}
        # Override with instance values
        data.update({k: v for k, v in self.__dict__.items()})
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def resolve_cameras(self) -> List["Config"]:
        """
        Resolve multi-camera config into a list of per-camera Config instances.
        Each camera inherits all top-level params and can override with its own.
        Backward compatible: if no 'cameras' field, use top-level STREAM_URL/DEVICE_ID.
        """
        if not self.cameras:
            # Legacy single-camera mode
            return [self]

        configs = []
        for cam in self.cameras:
            c = Config()
            # Copy all top-level values
            for k, v in self.__dict__.items():
                if k != "cameras":
                    setattr(c, k, v)
            # Override with per-camera values
            for k, v in cam.items():
                if hasattr(c, k):
                    setattr(c, k, v)
            c.cameras = None  # Per-camera config doesn't need cameras list
            configs.append(c)
        return configs

    def get_device_ids(self) -> List[str]:
        """Return all configured DEVICE_IDs"""
        if not self.cameras:
            return [self.DEVICE_ID]
        return [cam.get("DEVICE_ID", self.DEVICE_ID) for cam in self.cameras]

# ============================================================
# Index Management — SQLite storage for segment metadata
# ============================================================


class IndexManager:
    """
    segments table schema:
        video_path  TEXT PRIMARY KEY
        device_id   TEXT
        timestamp   INTEGER
        description TEXT (nullable)
        embedding   BLOB (nullable, float32 bytes)
        is_static   INTEGER (0/1)
        created_at  TEXT
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._lock = threading.Lock()
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS segments (
                video_path  TEXT PRIMARY KEY,
                device_id   TEXT,
                timestamp   INTEGER,
                description TEXT,
                embedding   BLOB,
                is_static   INTEGER DEFAULT 0,
                created_at  TEXT
            )
        """)
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_timestamp ON segments(timestamp)"
        )
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_created_at ON segments(created_at)"
        )
        self._conn.commit()
        logger.debug("IndexManager initialized (SQLite): %s", db_path)

    def append(self, record: dict):
        """Insert a record (thread-safe)"""
        emb = record.get("embedding")
        emb_blob = None
        if emb is not None:
            if isinstance(emb, np.ndarray):
                emb_blob = emb.astype(np.float32).tobytes()
            elif isinstance(emb, list):
                emb_blob = np.array(emb, dtype=np.float32).tobytes()
        with self._lock:
            self._conn.execute(
                """INSERT OR REPLACE INTO segments
                   (video_path, device_id, timestamp, description, embedding, is_static, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    record.get("video_path", ""),
                    record.get("device_id", ""),
                    record.get("timestamp", 0),
                    record.get("description"),
                    emb_blob,
                    1 if record.get("is_static") else 0,
                    record.get("created_at", ""),
                )
            )
            self._conn.commit()

    def load_all(self) -> List[dict]:
        """Load all records"""
        cursor = self._conn.execute(
            "SELECT video_path, device_id, timestamp, description, embedding, is_static, created_at FROM segments"
        )
        records = []
        for row in cursor:
            rec = {
                "video_path": row[0],
                "device_id": row[1],
                "timestamp": row[2],
                "description": row[3],
                "embedding": np.frombuffer(row[4], dtype=np.float32) if row[4] else None,
                "is_static": bool(row[5]),
                "created_at": row[6],
            }
            records.append(rec)
        return records

    def load_with_embeddings(self) -> Tuple[List[dict], np.ndarray]:
        """Load records with embeddings, return (records, embedding_matrix)"""
        cursor = self._conn.execute(
            """SELECT video_path, device_id, timestamp, description, embedding, is_static, created_at
               FROM segments WHERE embedding IS NOT NULL AND description IS NOT NULL"""
        )
        records = []
        embeddings = []
        for row in cursor:
            rec = {
                "video_path": row[0],
                "device_id": row[1],
                "timestamp": row[2],
                "description": row[3],
                "is_static": bool(row[5]),
                "created_at": row[6],
            }
            records.append(rec)
            embeddings.append(np.frombuffer(row[4], dtype=np.float32))
        if embeddings:
            return records, np.vstack(embeddings)
        return records, np.array([])

    def purge_expired(self, retention_days: int):
        """Delete expired records and corresponding video files, clean up empty directories"""
        if retention_days <= 0:
            return
        local_now = _local_now()
        cutoff = (local_now - timedelta(days=retention_days)
                  ).strftime("%Y-%m-%dT%H:%M:%S")

        # Query records to delete, get file paths
        cursor = self._conn.execute(
            "SELECT video_path FROM segments WHERE created_at < ?", (cutoff,)
        )
        empty_dirs = set()
        removed = 0
        for (vp,) in cursor.fetchall():
            if vp and os.path.exists(vp):
                parent_dir = os.path.dirname(vp)
                os.remove(vp)
                empty_dirs.add(parent_dir)
            removed += 1

        # Delete database records
        if removed:
            with self._lock:
                self._conn.execute(
                    "DELETE FROM segments WHERE created_at < ?", (cutoff,))
                self._conn.commit()

        # Clean up empty directories (hour dir → date dir)
        for d in empty_dirs:
            try:
                if os.path.isdir(d) and not os.listdir(d):
                    os.rmdir(d)
                    logger.debug("Removed empty directory: %s", d)
                    parent = os.path.dirname(d)
                    if os.path.isdir(parent) and not os.listdir(parent):
                        os.rmdir(parent)
                        logger.debug("Removed empty directory: %s", parent)
            except OSError as e:
                logger.warning("Failed to clean directory: %s => %s", d, e)

        if removed:
            logger.info("Purged %d expired records", removed)
        else:
            logger.debug("Purge complete, nothing to delete")

    def vacuum(self):
        """Compact database file to reclaim disk space"""
        with self._lock:
            self._conn.execute("VACUUM")
        logger.info("Database VACUUM complete")

    def close(self):
        """Close database connection"""
        self._conn.close()


# ============================================================
# Frame Difference Detection — Determine if segment is static
# ============================================================

def is_static_video(video_path: str, threshold: float = 5.0, sample_count: int = 5) -> bool:
    """
    Sample frame pairs and compute mean frame difference.
    Below threshold is considered static.
    """
    import cv2
    fname = os.path.basename(video_path)
    logger.debug("Frame diff detection started: %s (threshold=%.1f, samples=%d)",
                 fname, threshold, sample_count)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.warning("Cannot open video file, treating as static: %s", fname)
        return True

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames < 2:
        cap.release()
        logger.debug("Insufficient frames (<2), treating as static: %s", fname)
        return True

    indices = np.linspace(0, total_frames - 1, sample_count + 1, dtype=int)
    frames = {}
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frames[idx] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cap.release()

    if len(frames) < 2:
        logger.debug(
            "Insufficient valid frames (<2), treating as static: %s", fname)
        return True

    sorted_keys = sorted(frames.keys())
    diffs = []
    for i in range(len(sorted_keys) - 1):
        f1 = frames[sorted_keys[i]].astype(np.float32)
        f2 = frames[sorted_keys[i + 1]].astype(np.float32)
        diffs.append(np.mean(np.abs(f1 - f2)))

    avg_diff = np.mean(diffs)
    is_static = avg_diff < threshold
    logger.debug("Frame diff result: %s avg_diff=%.2f threshold=%.1f static=%s",
                 fname, avg_diff, threshold, is_static)
    return is_static


# ============================================================
# VLM Description + Embedding — Kamivision API
# ============================================================


# PROMPT_CN (commented out, kept for reference)
# """
# You are an objective scene recorder. For each provided frame sequence (from video surveillance clips, sampled at 1 fps),
# generate a single concise, objective description (max 30 words).
# Your description only includes entities present in the frame...
# """


def _video_to_base64(video_path: str) -> str:
    with open(video_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _extract_frames_base64(video_path: str, sample_fps: int = 1) -> List[str]:
    """Extract frames from video at specified fps, return base64-encoded JPEG list"""
    import cv2
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.warning(
            "Cannot open video for frame extraction: %s", video_path)
        return []
    src_fps = cap.get(cv2.CAP_PROP_FPS)
    if src_fps <= 0:
        src_fps = 25.0
    interval = max(1, int(src_fps / sample_fps))
    frames_b64 = []
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % interval == 0:
            _, buf = cv2.imencode(".jpg", frame)
            frames_b64.append(base64.b64encode(buf.tobytes()).decode("utf-8"))
        frame_idx += 1
    cap.release()
    return frames_b64


def _kami_detect_video(video_path: str, cfg: "Config") -> dict:
    """
    Call Kamivision /v1/detect to generate description + embedding for video.
    Based on SUMMARY_UPLOAD_MODE, upload full video or extracted frame list.
    Returns {"summary": "...", "embedding": [...]}
    """
    url = cfg.KAMI_API_URL
    if cfg.SUMMARY_UPLOAD_MODE == "video":
        b64 = _video_to_base64(video_path)
        payload = {
            "detectType": cfg.SUMMARY_DETECT_TYPE,
            "detectSubType": cfg.SUMMARY_DETECT_SUB_TYPE,
            "prompt": cfg.SUMMARY_PROMPT,
            "imageFile": "",
            "videoFile": b64,
            "skillId": cfg.skillId
        }
    else:
        frames = _extract_frames_base64(video_path, cfg.SUMMARY_SAMPLE_FPS)
        payload = {
            "detectType": cfg.SUMMARY_DETECT_TYPE,
            "detectSubType": cfg.SUMMARY_DETECT_SUB_TYPE,
            "prompt": cfg.SUMMARY_PROMPT,
            "imageFile": frames,
            "videoFile": "",
            "skillId": cfg.skillId
        }
    headers = {"Content-Type": "application/json",
               "X-API-Key": cfg.KAMI_API_KEY}

    last_error = None
    for attempt in range(1, cfg.KAMI_API_RETRY + 1):
        try:
            resp = http_requests.post(
                url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            code = data.get("code", -1)
            if code != 200:
                logger.warning("SUMMARY API returned error code=%s msg=%s (attempt %d)",
                               code, data.get("msg", ""), attempt)
                last_error = f"API code={code} msg={data.get('msg', '')}"
                continue
            # Parse result string → JSON
            result_str = data.get("data", {}).get("result", "{}")
            result = json.loads(result_str) if isinstance(
                result_str, str) else result_str
            summary = result.get("summary", "")
            # Embedding field is also a string, needs another parse
            emb_raw = result.get("embedding", "[]")
            embedding = json.loads(emb_raw) if isinstance(
                emb_raw, str) else emb_raw
            return {"summary": summary, "embedding": embedding}
        except http_requests.exceptions.RequestException as e:
            logger.warning(
                "SUMMARY API request exception: %s (attempt %d)", e, attempt)
            last_error = str(e)
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.warning(
                "SUMMARY API response parse failed: %s (attempt %d)", e, attempt)
            last_error = str(e)

    raise RuntimeError(
        f"SUMMARY API call failed after {cfg.KAMI_API_RETRY} retries: {last_error}")


def _kami_embed_texts(texts: List[str], cfg: "Config", mrl_dim: int = 2048) -> np.ndarray:
    """
    Call Kamivision /v1/detect (detectType=EMBED) to generate text embeddings.
    """
    url = cfg.KAMI_API_URL
    headers = {"Content-Type": "application/json",
               "X-API-Key": cfg.KAMI_API_KEY}
    all_embeddings = []
    for text in texts:
        payload = {
            "detectType": cfg.EMBED_DETECT_TYPE,
            "detectSubType": cfg.EMBED_DETECT_SUB_TYPE,
            "prompt": text,
            "imageFile": "",
            "videoFile": "",
            "skillId": cfg.skillId
        }
        last_error = None
        emb = None
        for attempt in range(1, cfg.KAMI_API_RETRY + 1):
            try:
                resp = http_requests.post(
                    url, headers=headers, json=payload, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                code = data.get("code", -1)
                if code != 200:
                    logger.warning("EMBED API returned error code=%s msg=%s (attempt %d)",
                                   code, data.get("msg", ""), attempt)
                    last_error = f"API code={code} msg={data.get('msg', '')}"
                    continue
                # result is a string, parse to list
                result_str = data.get("data", {}).get("result", "[]")
                emb = json.loads(result_str) if isinstance(
                    result_str, str) else result_str
                break
            except http_requests.exceptions.RequestException as e:
                logger.warning(
                    "EMBED API request exception: %s (attempt %d)", e, attempt)
                last_error = str(e)
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                logger.warning(
                    "EMBED API response parse failed: %s (attempt %d)", e, attempt)
                last_error = str(e)

        if emb is None:
            raise RuntimeError(
                f"EMBED API call failed after {cfg.KAMI_API_RETRY} retries: {last_error}")
        all_embeddings.append(np.array(emb, dtype=np.float32))
    embs = np.vstack(all_embeddings)
    embs = embs / (np.linalg.norm(embs, axis=1, keepdims=True) + 1e-10)
    return embs


def _local_now() -> datetime:
    """Get current local system time"""
    return datetime.now()


def timestamp_to_local_24hr(timestamp: int) -> str:
    """Unix timestamp → local timezone 24-hour format string"""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def parse_time_str(time_str: str) -> Optional[int]:
    """Convert user input local time string to unix timestamp, supports multiple formats.
    Input is treated as system local timezone."""
    if not time_str:
        return None
    formats = [
        "%Y-%m-%d_%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d_%H:%M",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(time_str, fmt)
            return int(dt.timestamp())
        except ValueError:
            continue
    # Fallback: try as unix timestamp
    try:
        return int(time_str)
    except ValueError:
        logger.error("Cannot parse time format: %s", time_str)
        return None


def get_vlm_functions(cfg: Config):
    """
    Return (description_func, description_prompt, embedding_func, embedding_dim)
    All using Kamivision API.
    """
    logger.debug("Initializing VLM functions: Kamivision API=%s",
                 cfg.KAMI_API_URL)

    def desc_func(video_path, prompt):
        return _kami_detect_video(video_path, cfg)

    def emb_func(texts, is_query=False, mrl_dim=None):
        dim = mrl_dim or cfg.EMBEDDING_DIM
        return _kami_embed_texts(texts, cfg, dim)

    desc_prompt = cfg.SUMMARY_PROMPT
    return desc_func, desc_prompt, emb_func, cfg.EMBEDDING_DIM


def process_segment(video_path: str, cfg: Config, index: IndexManager):
    """
    Process a single segment: static detection → description generation → embedding → write to index
    """
    # Parse timestamp from filename: CAM-001_20260424_153012_0.mp4
    # Filename time is system local time, parse directly as local timestamp
    fname_parts = Path(video_path).stem.split("_")
    try:
        date_str = fname_parts[1]  # 20260424
        time_str = fname_parts[2]  # 153012
        dt = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
        timestamp = int(dt.timestamp())
    except (IndexError, ValueError):
        timestamp = int(time.time())
    local_now = _local_now()
    record = {
        "video_path": video_path,
        "device_id": cfg.DEVICE_ID,
        "timestamp": timestamp,
        "description": None,
        "embedding": None,
        "is_static": False,
        "created_at": local_now.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    fname = os.path.basename(video_path)
    logger.info("Processing segment: %s (timestamp=%d)", fname, timestamp)

    # Static detection
    if cfg.SKIP_STATIC and is_static_video(video_path, cfg.STATIC_THRESHOLD):
        record["is_static"] = True
        index.append(record)
        logger.info("Skipped static segment: %s", fname)
        return

    if not cfg.ENABLE_DESCRIPTION:
        logger.debug(
            "Description generation disabled, writing index only: %s", fname)
        index.append(record)
        return

    # Generate description + embedding (SUMMARY API returns both)
    desc_func, desc_prompt, emb_func, emb_dim = get_vlm_functions(cfg)
    logger.debug("Calling Kamivision detect API: %s, file=%s",
                 cfg.KAMI_API_URL, fname)
    t0 = time.time()
    try:
        result = desc_func(video_path, desc_prompt)
        description = result["summary"].replace("'", "").replace('"', "")
        record["description"] = description
        # Embedding from the same API call
        emb = result.get("embedding", [])
        if emb:
            record["embedding"] = np.array(emb, dtype=np.float32)
        elapsed = time.time() - t0
        logger.info("Description+Embedding generated: %s (%.1fs) => %s...",
                    fname, elapsed, description[:80])
    except RuntimeError:
        raise  # API retries exhausted, propagate to worker to stop program
    except Exception as e:
        logger.error("Description generation failed: %s => %s",
                     fname, e, exc_info=True)
        index.append(record)
        return

    index.append(record)
    logger.debug("Index write complete: %s", fname)


# ============================================================
# Stream Recorder — OpenCV segment mode
# ============================================================

class StreamRecorder:
    """
    Pull stream with OpenCV and segment by fixed duration.
    Supports RTSP/RTMP/HTTP with auto-reconnection.
    """

    def __init__(self, cfg: Config, index: IndexManager):
        self.cfg = cfg
        self.index = index
        self._stop_event = threading.Event()
        # Processing queue
        self._pending: deque = deque()
        self._pending_lock = threading.Lock()

    @property
    def output_dir(self) -> str:
        now = _local_now()
        day = now.strftime("%Y%m%d")
        hour = now.strftime("%H")
        d = os.path.join(self.cfg.DATA_DIR, self.cfg.DEVICE_ID, day, hour)
        Path(d).mkdir(parents=True, exist_ok=True)
        return d

    def _make_segment_path(self, seg_index: int) -> str:
        now = _local_now()
        time_str = now.strftime("%Y%m%d_%H%M%S")
        fname = f"{self.cfg.DEVICE_ID}_{time_str}_{seg_index}.mp4"
        return os.path.join(self.output_dir, fname)

    def _enqueue_segment(self, video_path: str):
        """Add completed segment to processing queue"""
        size = os.path.getsize(video_path) if os.path.exists(video_path) else 0
        if size > 0:
            with self._pending_lock:
                self._pending.append(video_path)
            logger.info("New segment enqueued: %s (size=%d bytes)",
                        os.path.basename(video_path), size)
        else:
            logger.warning(
                "Segment file empty or missing, skipped: %s", video_path)

    def _capture_loop(self) -> bool:
        """
        OpenCV stream capture main loop: read all frames → segment by duration into files.
        Returns on stream disconnect, outer loop handles reconnection.
        Returns True if at least one segment was successfully recorded.
        """
        import cv2
        c = self.cfg
        recorded = False

        logger.info("OpenCV connecting to stream: %s", c.STREAM_URL)
        os.environ["OPENCV_FFMPEG_READ_ATTEMPTS"] = "65536"
        cap = cv2.VideoCapture(c.STREAM_URL)

        if not cap.isOpened():
            logger.error("OpenCV cannot open stream: %s", c.STREAM_URL)
            return

        # Get source stream fps for VideoWriter and segment calculation
        src_fps = cap.get(cv2.CAP_PROP_FPS)
        if src_fps <= 0 or src_fps > 120:
            src_fps = 25.0  # Fallback default
        src_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        src_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        logger.info("Stream info: src_fps=%.1f src_size=%dx%d => out_size=%dx%d (all frames stored)",
                    src_fps, src_w, src_h, c.OUTPUT_WIDTH, c.OUTPUT_HEIGHT)

        # Try multiple codecs, prefer H.264
        fourcc_candidates = [
            ("avc1", "H.264/avc1"),
            ("X264", "H.264/X264"),
            ("mp4v", "MPEG-4/mp4v"),
        ]
        fourcc = None
        fourcc_name = None
        test_path = os.path.join(self.output_dir, "_codec_test.mp4")
        for code, name in fourcc_candidates:
            fc = cv2.VideoWriter_fourcc(*code)
            test_writer = cv2.VideoWriter(
                test_path, fc, src_fps, (c.OUTPUT_WIDTH, c.OUTPUT_HEIGHT))
            if test_writer.isOpened():
                test_writer.release()
                fourcc = fc
                fourcc_name = name
                break
            test_writer.release()
        if os.path.exists(test_path):
            os.remove(test_path)
        if fourcc is None:
            logger.error("No available video codec found")
            return
        logger.info("Using codec: %s", fourcc_name)

        out_fps = src_fps

        seg_index = 0
        frames_in_seg = 0
        max_frames_per_seg = int(c.SEGMENT_DURATION * src_fps)
        writer: Optional[cv2.VideoWriter] = None
        current_seg_path: Optional[str] = None
        consecutive_failures = 0

        try:
            while not self._stop_event.is_set():
                ret, frame = cap.read()
                if not ret:
                    consecutive_failures += 1
                    if consecutive_failures > 100:
                        logger.warning(
                            "%d consecutive frame read failures, stream disconnected", consecutive_failures)
                        break
                    time.sleep(0.02)
                    continue

                consecutive_failures = 0

                # Resize
                resized = cv2.resize(frame, (c.OUTPUT_WIDTH, c.OUTPUT_HEIGHT))

                # Need new segment
                if writer is None or frames_in_seg >= max_frames_per_seg:
                    # Close previous segment
                    if writer is not None:
                        writer.release()
                        logger.info("Segment complete: %s (frames=%d)", os.path.basename(
                            current_seg_path), frames_in_seg)
                        self._enqueue_segment(current_seg_path)
                        recorded = True

                    current_seg_path = self._make_segment_path(seg_index)
                    writer = cv2.VideoWriter(current_seg_path, fourcc, out_fps,
                                             (c.OUTPUT_WIDTH, c.OUTPUT_HEIGHT))
                    if not writer.isOpened():
                        logger.error(
                            "Cannot create VideoWriter: %s", current_seg_path)
                        break
                    seg_index += 1
                    frames_in_seg = 0
                    logger.debug("Starting new segment: %s",
                                 os.path.basename(current_seg_path))

                writer.write(resized)
                frames_in_seg += 1

        finally:
            # Cleanup: close current segment and stream
            if writer is not None:
                writer.release()
                if frames_in_seg > 0:
                    logger.info("Segment complete (interrupted): %s (frames=%d)", os.path.basename(
                        current_seg_path), frames_in_seg)
                    self._enqueue_segment(current_seg_path)
            cap.release()
            logger.info("OpenCV stream released")
        return recorded

    def _process_worker(self):
        """Background thread: dequeue segments, run description+embedding"""
        while not self._stop_event.is_set():
            video_path = None
            with self._pending_lock:
                if self._pending:
                    video_path = self._pending.popleft()

            if video_path:
                logger.debug("Dequeued for processing: %s (remaining=%d)",
                             os.path.basename(video_path), len(self._pending))
                try:
                    process_segment(video_path, self.cfg, self.index)
                except RuntimeError as e:
                    logger.error(
                        "API retries exhausted, stopping program: %s", e)
                    self._stop_event.set()
                    os.kill(os.getpid(), signal.SIGTERM)
                    return
                except Exception as e:
                    logger.error("Segment processing error: %s => %s",
                                 os.path.basename(video_path), e, exc_info=True)
            else:
                time.sleep(0.5)

    def start(self):
        """Start recording (blocking, Ctrl+C to exit)"""
        logger.info("="*60)
        logger.info("Starting recording device=%s stream=%s",
                    self.cfg.DEVICE_ID, self.cfg.STREAM_URL)
        logger.info("Segment=%ds output=%dx%d all_frames timestamp=%s",
                    self.cfg.SEGMENT_DURATION,
                    self.cfg.OUTPUT_WIDTH, self.cfg.OUTPUT_HEIGHT,
                    self.cfg.TIMESTAMP_SOURCE)
        logger.info("VLM=Kamivision(%s) Embedding=Kamivision output_dir=%s retention_days=%d",
                    self.cfg.KAMI_API_URL,
                    self.cfg.DATA_DIR, self.cfg.RETENTION_DAYS)
        logger.info("Static_detection=%s (threshold=%.1f) description=%s",
                    self.cfg.SKIP_STATIC, self.cfg.STATIC_THRESHOLD, self.cfg.ENABLE_DESCRIPTION)
        logger.info("="*60)

        # Start processing threads
        for i in range(self.cfg.PROCESS_WORKERS):
            w = threading.Thread(target=self._process_worker,
                                 daemon=True, name=f"worker-{i}")
            w.start()
        logger.info("Segment processing threads started (workers=%d)",
                    self.cfg.PROCESS_WORKERS)

        # Periodic expired data cleanup
        def purge_loop():
            while not self._stop_event.is_set():
                try:
                    self.index.purge_expired(self.cfg.RETENTION_DAYS)
                    self.index.vacuum()
                except Exception as e:
                    logger.warning("Periodic cleanup error: %s", e)
                for _ in range(3600):
                    if self._stop_event.is_set():
                        break
                    time.sleep(1)

        purger = threading.Thread(target=purge_loop, daemon=True)
        purger.start()
        logger.info(
            "Expiry cleanup thread started (interval=1h, retention=%dd)", self.cfg.RETENTION_DAYS)

        # Main loop: stream capture + auto-reconnect
        reconnect_count = 0
        delay = self.cfg.RECONNECT_DELAY
        max_reconnect = self.cfg.MAX_RECONNECT
        while not self._stop_event.is_set():
            reconnect_count += 1
            logger.info("Starting stream connection attempt #%d",
                        reconnect_count)
            try:
                success = self._capture_loop()
                if success:
                    reconnect_count = 0  # Successfully recorded, reset counter
            except Exception as e:
                logger.error("Stream capture error: %s", e, exc_info=True)

            if self._stop_event.is_set():
                break

            if max_reconnect > 0 and reconnect_count >= max_reconnect:
                logger.error(
                    "Max reconnect attempts reached (%d), stopping recording", max_reconnect)
                break

            logger.warning(
                "Stream disconnected, reconnecting in %ds (attempt #%d)...", delay, reconnect_count + 1)
            # Interruptible wait
            for _ in range(delay):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

    def stop(self):
        """Graceful stop"""
        logger.info("Stopping recording...")
        self._stop_event.set()
        logger.info("Recording stopped")


# ============================================================
# Search Engine
# ============================================================

class VideoSearchEngine:
    """Video search based on index file"""

    def __init__(self, cfg: Config, index: IndexManager):
        self.cfg = cfg
        self.index = index

    def search(self, query: str, time_start: Optional[int] = None,
               time_end: Optional[int] = None) -> List[dict]:
        """
        Text-based video clip search.
        Returns [{video_path, description, timestamp, score}, ...]
        """
        records, emb_matrix = self.index.load_with_embeddings()
        if len(records) == 0:
            logger.info("Index is empty, nothing to search")
            return []

        # Time range filter
        if time_start or time_end:
            logger.info("Time range filter: start=%s end=%s",
                        time_start, time_end)
            mask = []
            for i, rec in enumerate(records):
                ts = rec.get("timestamp", 0)
                if time_start and ts < time_start:
                    mask.append(False)
                elif time_end and ts > time_end:
                    mask.append(False)
                else:
                    mask.append(True)
            indices = [i for i, m in enumerate(mask) if m]
            if not indices:
                logger.info("No records in time range")
                return []
            logger.info("%d records remaining after time filter", len(indices))
            records = [records[i] for i in indices]
            emb_matrix = emb_matrix[indices]

        # Generate query embedding
        _, _, emb_func, emb_dim = get_vlm_functions(self.cfg)
        logger.debug(
            "Generating query embedding: query='%s' Kamivision dim=%d", query, emb_dim)
        try:
            query_emb = emb_func([query], is_query=True, mrl_dim=emb_dim)
            if isinstance(query_emb, list):
                query_emb = np.array(query_emb)
            if query_emb.ndim == 2:
                query_emb = query_emb[0]
        except Exception as e:
            logger.error(
                "Query embedding failed: %s, falling back to NLP search", e, exc_info=True)
            # fallback: try local NLP search
            return self._search_nlp_fallback(query, records)

        # Cosine similarity
        query_norm = query_emb / (np.linalg.norm(query_emb) + 1e-10)
        emb_norms = emb_matrix / \
            (np.linalg.norm(emb_matrix, axis=1, keepdims=True) + 1e-10)
        scores = emb_norms @ query_norm

        # Filter + sort
        results = []
        for i, score in enumerate(scores):
            if score >= self.cfg.SIMILARITY_THRESHOLD:
                results.append({
                    "video_path": records[i]["video_path"],
                    "description": records[i]["description"],
                    "timestamp": records[i]["timestamp"],
                    "score": float(score),
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        logger.info("Search complete: query='%s' matched=%d/%d (threshold=%.2f)",
                    query, len(results), len(records), self.cfg.SIMILARITY_THRESHOLD)
        return results[:self.cfg.SEARCH_TOP_K]

    def _search_nlp_fallback(self, query: str, records: List[dict]) -> List[dict]:
        """NLP local search fallback (simple keyword matching)"""
        query_lower = query.lower()
        results = []
        for i, rec in enumerate(records):
            desc = rec.get("description", "")
            if not desc:
                continue
            # Simple contains match with fixed score
            if query_lower in desc.lower():
                results.append({
                    "video_path": rec["video_path"],
                    "description": rec["description"],
                    "timestamp": rec["timestamp"],
                    "score": 0.5,
                })
        results.sort(key=lambda x: x["timestamp"], reverse=True)
        return results[:self.cfg.SEARCH_TOP_K]

    def list_recent(self, hours: int = 24) -> List[dict]:
        """List non-static segments from the last N hours"""
        cutoff = int(time.time()) - hours * 3600
        records = self.index.load_all()
        results = []
        for rec in records:
            if rec.get("timestamp", 0) >= cutoff and not rec.get("is_static", False):
                results.append(rec)
        results.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        return results[:self.cfg.LIST_TOP_K]


# ============================================================
# PID File Management — Background process start/stop
# ============================================================

def _get_pid_file(cfg: Config) -> str:
    """PID file path: DATA_DIR/DEVICE_ID/recorder.pid"""
    d = os.path.join(cfg.DATA_DIR, cfg.DEVICE_ID)
    Path(d).mkdir(parents=True, exist_ok=True)
    return os.path.join(d, "recorder.pid")


def _resolve_per_camera_log(base_log_file: Optional[str], device_id: str) -> str:
    """
    Build a per-camera log file path so each camera subprocess writes to its own file.

    Rule: place the log next to the base log file (or in the current working directory
    when no base log file is provided), and name it after the DEVICE_ID, e.g.
        base_log_file=/path/to/stream_recorder.log, device_id=front-door
        -> /path/to/front-door.log
    """
    if base_log_file:
        log_dir = os.path.dirname(os.path.abspath(base_log_file))
    else:
        log_dir = os.getcwd()
    if log_dir:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
    # Sanitize device_id just in case (DEVICE_ID is already constrained to ASCII+hyphen by SKILL spec)
    safe_name = "".join(ch for ch in device_id if ch.isalnum() or ch in ("-", "_")) or "camera"
    return os.path.join(log_dir, f"{safe_name}.log")


def _read_pid(pid_file: str) -> Optional[int]:
    """Read PID file, return PID or None"""
    if not os.path.exists(pid_file):
        return None
    try:
        with open(pid_file, "r") as f:
            return int(f.read().strip())
    except (ValueError, OSError):
        return None


def _is_pid_alive(pid: int) -> bool:
    """Check if process is alive"""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _start_daemon(cfg: Config, script_path: str, config_path: str, log_file: str) -> dict:
    """Start recording as background process for a single camera, return status JSON.

    Each camera subprocess writes to its OWN log file named after DEVICE_ID, located in
    the same directory as the base log_file. The child process re-opens the file in
    write mode (see setup_logging), so its log is truncated on every (re)start.
    """
    import subprocess
    pid_file = _get_pid_file(cfg)
    existing_pid = _read_pid(pid_file)

    # Resolve per-camera log file (e.g. <log_dir>/<DEVICE_ID>.log)
    per_camera_log = _resolve_per_camera_log(log_file, cfg.DEVICE_ID)

    if existing_pid and _is_pid_alive(existing_pid):
        return {"status": "already_running", "pid": existing_pid,
                "device_id": cfg.DEVICE_ID,
                "log_file": per_camera_log,
                "message": f"[{cfg.DEVICE_ID}] Recording process already running (PID={existing_pid})"}

    # Launch background recording process
    venv_python = os.path.join(os.path.dirname(
        os.path.abspath(script_path)), ".venv", "bin", "python")
    if not os.path.exists(venv_python):
        venv_python = sys.executable

    # Pass --device so the child process knows which single camera to record,
    # and pass the per-camera log file so each subprocess writes to its own log.
    cmd = [venv_python, os.path.abspath(script_path),
           "--config", config_path, "--log-file", per_camera_log,
           "--device", cfg.DEVICE_ID]

    proc = subprocess.Popen(
        cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    with open(pid_file, "w") as f:
        f.write(str(proc.pid))

    return {"status": "started", "pid": proc.pid,
            "device_id": cfg.DEVICE_ID,
            "message": f"[{cfg.DEVICE_ID}] Recording started (PID={proc.pid})",
            "log_file": per_camera_log}


def _stop_daemon(cfg: Config) -> dict:
    """Stop background recording process, return status JSON"""
    pid_file = _get_pid_file(cfg)
    pid = _read_pid(pid_file)

    if pid is None:
        return {"status": "not_running", "device_id": cfg.DEVICE_ID,
                "message": f"[{cfg.DEVICE_ID}] No running recording process found"}

    if not _is_pid_alive(pid):
        os.remove(pid_file)
        return {"status": "not_running", "device_id": cfg.DEVICE_ID,
                "message": f"[{cfg.DEVICE_ID}] Process (PID={pid}) no longer exists, PID file cleaned up"}

    # Send SIGTERM for graceful stop
    os.kill(pid, signal.SIGTERM)
    # Wait up to 10 seconds
    for _ in range(20):
        if not _is_pid_alive(pid):
            break
        time.sleep(0.5)

    if _is_pid_alive(pid):
        os.kill(pid, signal.SIGKILL)
        time.sleep(0.5)

    if os.path.exists(pid_file):
        os.remove(pid_file)

    return {"status": "stopped", "pid": pid, "device_id": cfg.DEVICE_ID,
            "message": f"[{cfg.DEVICE_ID}] Recording stopped (PID={pid})"}


def _get_status(cfg: Config) -> dict:
    """Get recording process status"""
    pid_file = _get_pid_file(cfg)
    pid = _read_pid(pid_file)

    if pid is None:
        return {"status": "not_running", "device_id": cfg.DEVICE_ID,
                "message": f"[{cfg.DEVICE_ID}] Recording not running"}

    if _is_pid_alive(pid):
        return {"status": "running", "pid": pid, "device_id": cfg.DEVICE_ID,
                "message": f"[{cfg.DEVICE_ID}] Recording running (PID={pid})"}
    else:
        os.remove(pid_file)
        return {"status": "not_running", "device_id": cfg.DEVICE_ID,
                "message": f"[{cfg.DEVICE_ID}] Process (PID={pid}) no longer exists, PID file cleaned up"}


# ============================================================
# Multi-camera helpers
# ============================================================

def _filter_cameras(cfg: Config, device_filter: Optional[str]) -> List["Config"]:
    """
    Resolve cameras from config and filter by --device argument.
    device_filter: comma-separated DEVICE_IDs, or None for all.
    """
    all_cameras = cfg.resolve_cameras()
    if not device_filter:
        return all_cameras
    requested = [d.strip() for d in device_filter.split(",")]
    filtered = [c for c in all_cameras if c.DEVICE_ID in requested]
    if not filtered:
        available = [c.DEVICE_ID for c in all_cameras]
        logger.error("No matching cameras for --device=%s (available: %s)",
                     device_filter, ", ".join(available))
    return filtered


def _multi_search(cameras: List["Config"], query: str,
                  time_start: Optional[int], time_end: Optional[int],
                  top_k: int) -> List[dict]:
    """Search across multiple cameras, merge and sort results."""
    all_results = []
    for cam_cfg in cameras:
        index_path = os.path.join(cam_cfg.DATA_DIR, cam_cfg.DEVICE_ID, cam_cfg.INDEX_FILE)
        if not os.path.exists(index_path):
            continue
        index = IndexManager(index_path)
        engine = VideoSearchEngine(cam_cfg, index)
        results = engine.search(query, time_start=time_start, time_end=time_end)
        for r in results:
            r["device_id"] = cam_cfg.DEVICE_ID
        all_results.extend(results)
        index.close()
    all_results.sort(key=lambda x: x["score"], reverse=True)
    return all_results[:top_k]


def _multi_list_recent(cameras: List["Config"], hours: int, top_k: int) -> List[dict]:
    """List recent events across multiple cameras."""
    all_results = []
    for cam_cfg in cameras:
        index_path = os.path.join(cam_cfg.DATA_DIR, cam_cfg.DEVICE_ID, cam_cfg.INDEX_FILE)
        if not os.path.exists(index_path):
            continue
        index = IndexManager(index_path)
        engine = VideoSearchEngine(cam_cfg, index)
        results = engine.list_recent(hours)
        for r in results:
            r["device_id"] = cam_cfg.DEVICE_ID
        all_results.extend(results)
        index.close()
    all_results.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
    return all_results[:top_k]


# ============================================================
# CLI Entry Point
# ============================================================

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_config = os.path.join(script_dir, "stream_config.json")
    default_log = os.path.join(script_dir, "stream_recorder.log")

    parser = argparse.ArgumentParser(
        description="Real-time stream recording + video search")
    parser.add_argument("--config", default=default_config,
                        help="Config file path")
    parser.add_argument("--search", type=str, default=None,
                        help="Search mode: input query text")
    parser.add_argument("--list", type=int, default=None, metavar="HOURS",
                        help="List events from the last N hours")
    parser.add_argument("--export-config", action="store_true",
                        help="Export default config to JSON file")
    parser.add_argument("--time-start", type=str, default=None,
                        help="Search time range start (format: 2026-04-24_08:00:00)")
    parser.add_argument("--time-end", type=str, default=None,
                        help="Search time range end (format: 2026-04-24_12:00:00)")
    parser.add_argument("--log-level", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                        help="Log level (default INFO)")
    parser.add_argument("--log-file", default=None,
                        help="Log output file path (optional, also outputs to console)")
    # JSON output
    parser.add_argument("--json", action="store_true",
                        help="Output results in JSON format")
    # Background process management
    parser.add_argument("--start-daemon", action="store_true",
                        help="Start recording as background process")
    parser.add_argument("--stop-daemon", action="store_true",
                        help="Stop background recording process")
    parser.add_argument("--status", action="store_true",
                        help="Check recording process status")
    # Multi-camera: device filter
    parser.add_argument("--device", type=str, default=None,
                        help="Target device(s), comma-separated (e.g. CAM-001,CAM-002). "
                             "If omitted, operates on all configured cameras.")

    args = parser.parse_args()

    # Load config
    cfg = Config.from_json(args.config)

    # Resolve log file: CLI arg > config field > default (script dir)
    resolved_log = (
        args.log_file
        or (cfg.LOG_FILE if cfg.LOG_FILE else None)
        or default_log
    )

    # Initialize logging (daemon management commands don't need stderr logging)
    if not (args.start_daemon or args.stop_daemon or args.status):
        setup_logging(
            level=getattr(logging, args.log_level),
            log_file=resolved_log,
        )

    # --- Background process management (multi-camera aware) ---
    if args.start_daemon:
        cameras = _filter_cameras(cfg, args.device)
        results = []
        for cam_cfg in cameras:
            result = _start_daemon(cam_cfg, __file__, args.config, resolved_log)
            results.append(result)
        if len(results) == 1:
            print(json.dumps(results[0], ensure_ascii=False))
        else:
            print(json.dumps({"status": "ok", "cameras": results}, ensure_ascii=False))
        return

    if args.stop_daemon:
        cameras = _filter_cameras(cfg, args.device)
        results = []
        for cam_cfg in cameras:
            result = _stop_daemon(cam_cfg)
            results.append(result)
        if len(results) == 1:
            print(json.dumps(results[0], ensure_ascii=False))
        else:
            print(json.dumps({"status": "ok", "cameras": results}, ensure_ascii=False))
        return

    if args.status:
        cameras = _filter_cameras(cfg, args.device)
        results = []
        for cam_cfg in cameras:
            result = _get_status(cam_cfg)
            results.append(result)
        if len(results) == 1:
            print(json.dumps(results[0], ensure_ascii=False))
        else:
            print(json.dumps({"status": "ok", "cameras": results}, ensure_ascii=False))
        return

    # Export default config
    if args.export_config:
        cfg.to_json(args.config)
        if args.json:
            print(json.dumps(
                {"status": "ok", "message": f"Config exported to {args.config}"}, ensure_ascii=False))
        else:
            logger.info("Config exported to %s", args.config)
        return

    # Resolve target cameras
    cameras = _filter_cameras(cfg, args.device)
    if not cameras:
        logger.error("No cameras configured or matched by --device filter")
        sys.exit(1)

    # Search mode (multi-camera)
    if args.search:
        logger.info("Entering search mode: query='%s' devices=%s",
                    args.search, [c.DEVICE_ID for c in cameras])
        time_start = parse_time_str(args.time_start)
        time_end = parse_time_str(args.time_end)
        results = _multi_search(cameras, args.search, time_start, time_end, cfg.SEARCH_TOP_K)
        if args.json:
            output = []
            for r in results:
                output.append({
                    "device_id": r.get("device_id", ""),
                    "video_name": os.path.basename(r["video_path"]),
                    "video_path": r["video_path"],
                    "description": r["description"],
                    "timestamp": r["timestamp"],
                    "time": timestamp_to_local_24hr(r["timestamp"]),
                    "score": round(r["score"], 4),
                })
            print(json.dumps({"status": "ok", "query": args.search,
                              "count": len(output), "results": output}, ensure_ascii=False))
        else:
            if not results:
                print("No matching video clips found.")
            else:
                print(f"\nFound {len(results)} matching clips:\n")
                for i, r in enumerate(results, 1):
                    local_time = timestamp_to_local_24hr(r["timestamp"])
                    print(f"  [{i}] [{r.get('device_id', '')}] {local_time}  score={r['score']:.3f}")
                    print(f"      {r['description']}")
                    print(f"      {r['video_path']}\n")
        return

    # List mode (multi-camera)
    if args.list is not None:
        logger.info("Entering list mode: last %d hours, devices=%s",
                    args.list, [c.DEVICE_ID for c in cameras])
        results = _multi_list_recent(cameras, args.list, cfg.LIST_TOP_K)
        if args.json:
            output = []
            for rec in results:
                output.append({
                    "device_id": rec.get("device_id", ""),
                    "video_name": os.path.basename(rec.get("video_path", "")),
                    "video_path": rec.get("video_path", ""),
                    "description": rec.get("description", ""),
                    "timestamp": rec.get("timestamp", 0),
                    "time": timestamp_to_local_24hr(rec.get("timestamp", 0)),
                })
            print(json.dumps({"status": "ok", "hours": args.list,
                              "count": len(output), "results": output}, ensure_ascii=False))
        else:
            if not results:
                print("No records found.")
            else:
                print(f"\n{len(results)} events in the last {args.list} hours:\n")
                for rec in results:
                    local_time = timestamp_to_local_24hr(rec["timestamp"])
                    desc = rec.get("description", "(no description)")
                    dev = rec.get("device_id", "")
                    print(f"  [{dev}] {local_time}  {desc[:60]}")
        return

    # Recording mode (foreground blocking, single camera only)
    # When launched by --start-daemon, --device is always a single camera
    if len(cameras) > 1:
        logger.error("Foreground recording mode only supports a single camera. "
                     "Use --start-daemon to run multiple cameras, or specify --device.")
        sys.exit(1)

    cam_cfg = cameras[0]
    index_path = os.path.join(cam_cfg.DATA_DIR, cam_cfg.DEVICE_ID, cam_cfg.INDEX_FILE)
    logger.info("Index file: %s", index_path)
    index = IndexManager(index_path)

    # Pre-start cleanup of expired data + VACUUM
    logger.info("Pre-start expired data cleanup (retention=%d days)",
                cam_cfg.RETENTION_DAYS)
    index.purge_expired(cam_cfg.RETENTION_DAYS)
    index.vacuum()

    logger.info("Entering recording mode")
    recorder = StreamRecorder(cam_cfg, index)

    def signal_handler(sig, frame):
        logger.info("Received signal %s, preparing to stop",
                    signal.Signals(sig).name)
        recorder.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    recorder.start()


if __name__ == "__main__":
    main()
