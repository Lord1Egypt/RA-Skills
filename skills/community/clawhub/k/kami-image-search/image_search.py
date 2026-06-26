#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kami-image-search: AI-powered image content search skill"""

import os
import sys
import json
import logging
import base64
from datetime import datetime, timedelta, timezone


# ============================================================
# CONFIG — All configurable parameters
# ============================================================

class CameraConfig:
    """Per-camera configuration. Camera-specific fields that can override globals."""

    STREAM_URL: str = ""
    DEVICE_ID: str = "CAM-001"
    CAPTURE_INTERVAL: int = 10          # Frame capture interval (seconds)
    OUTPUT_WIDTH: int = 640
    OUTPUT_HEIGHT: int = 360
    SKIP_DUPLICATE: bool = True
    DUPLICATE_THRESHOLD: float = 5.0
    RECONNECT_DELAY: int = 3

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)


class Config:
    """Load config from image_config.json; missing fields use defaults.

    Supports both legacy single-camera format and new multi-camera format
    with a 'cameras' array.
    """

    # --- Per-camera defaults (used when cameras array omits fields) ---
    STREAM_URL: str = ""
    DEVICE_ID: str = "CAM-001"
    CAPTURE_INTERVAL: int = 10
    OUTPUT_WIDTH: int = 640
    OUTPUT_HEIGHT: int = 360
    SKIP_DUPLICATE: bool = True
    DUPLICATE_THRESHOLD: float = 5.0
    RECONNECT_DELAY: int = 3

    # --- VLM description ---
    ENABLE_DESCRIPTION: bool = True
    VLM_PROMPT: str = ""

    # --- Cloud API ---
    KAMIVISION_API_URL: str = "https://kamiclaw-test.kamivision.com/v1/detect"
    KAMIVISION_API_KEY: str = ""

    # --- Search ---
    SIMILARITY_THRESHOLD: float = 0.35
    SEARCH_TOP_K: int = 5

    # --- Storage ---
    DATA_DIR: str = "/opt/image_data"
    RETENTION_DAYS: int = 30

    # --- Timezone ---
    TIME_ZONE_OFFSET: int = -12

    # --- Multi-camera ---
    cameras: list = None  # List[CameraConfig]

    # Camera-specific field names (used to build CameraConfig from globals)
    _CAMERA_FIELDS = (
        "STREAM_URL", "DEVICE_ID", "CAPTURE_INTERVAL",
        "OUTPUT_WIDTH", "OUTPUT_HEIGHT", "SKIP_DUPLICATE",
        "DUPLICATE_THRESHOLD", "RECONNECT_DELAY",
    )

    @classmethod
    def from_json(cls, path: str) -> "Config":
        """Load config from JSON file; missing fields use defaults.

        If JSON contains a 'cameras' array, parse as multi-camera mode.
        Otherwise, fall back to legacy single-camera mode (wrap top-level
        STREAM_URL/DEVICE_ID into a single-element cameras list).
        Exits with code 1 if config file is missing or malformed.
        """
        cfg = cls()
        if not os.path.exists(path):
            print(f"Error: config file not found: {path}", file=sys.stderr)
            sys.exit(1)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Error: invalid config file: {path} ({e})", file=sys.stderr)
            sys.exit(1)

        # Load all top-level fields (except 'cameras') into Config
        for k, v in data.items():
            if k == "cameras":
                continue
            if hasattr(cfg, k):
                setattr(cfg, k, v)

        # Build cameras list
        if "cameras" in data and isinstance(data["cameras"], list):
            cfg.cameras = []
            for cam_data in data["cameras"]:
                # Start with global defaults for camera fields
                cam_kwargs = {f: getattr(cfg, f) for f in cls._CAMERA_FIELDS}
                # Override with per-camera values
                cam_kwargs.update({k: v for k, v in cam_data.items()
                                   if k in cls._CAMERA_FIELDS})
                cfg.cameras.append(CameraConfig(**cam_kwargs))
        else:
            # Legacy single-camera mode: wrap top-level fields
            cam_kwargs = {f: getattr(cfg, f) for f in cls._CAMERA_FIELDS}
            cfg.cameras = [CameraConfig(**cam_kwargs)]

        # Validate DEVICE_ID uniqueness
        device_ids = [c.DEVICE_ID for c in cfg.cameras]
        if len(device_ids) != len(set(device_ids)):
            print("Error: duplicate DEVICE_ID found in cameras array",
                  file=sys.stderr)
            sys.exit(1)

        return cfg

    def get_camera(self, device_id: str) -> "CameraConfig":
        """Find CameraConfig by DEVICE_ID; returns None if not found."""
        for cam in self.cameras:
            if cam.DEVICE_ID == device_id:
                return cam
        return None

# ============================================================
# LOGGING — Unified logging configuration
# ============================================================

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: int = logging.INFO, log_file: str = None):
    """
    Initialize logging. Outputs to both stderr and an optional log file.
    """
    root = logging.getLogger()
    root.setLevel(level)
    # Avoid adding duplicate handlers
    if root.handlers:
        return

    fmt = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # Console (stderr)
    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(fmt)
    root.addHandler(console)

    # File
    if log_file:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(fmt)
        root.addHandler(fh)


logger = logging.getLogger("image_search")


# ============================================================
# Utility functions
# ============================================================

def timestamp_to_local_12hr(timestamp: int, time_zone_offset: int = -7) -> str:
    """Unix timestamp → local 12-hour format string, e.g. '2025-08-15 10:00:07 AM'"""
    utc_dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    local_dt = utc_dt + timedelta(hours=time_zone_offset)
    return local_dt.strftime("%Y-%m-%d %I:%M:%S %p")

# ============================================================
# INDEX MANAGER — FAISS vector index + SQLite metadata
# ============================================================

import sqlite3
import threading
import time as _time
from typing import Optional, List, Tuple
import numpy as np
from pathlib import Path

try:
    import faiss
except ImportError:
    faiss = None
    logger.warning("faiss-cpu not installed, IndexManager will be unavailable")


class IndexManager:
    """FAISS vector index + SQLite metadata manager.

    FAISS uses IndexIDMap(IndexFlatIP) with SQLite auto-increment IDs as vector IDs,
    ensuring a 1:1 mapping. All write operations are thread-safe via threading.Lock.
    """

    def __init__(self, data_dir: str, device_id: str, dim: int = 2048):
        self.data_dir = data_dir
        self.device_id = device_id
        self.dim = dim

        self._device_dir = Path(data_dir) / device_id
        self._device_dir.mkdir(parents=True, exist_ok=True)

        self._db_path = str(self._device_dir / "metadata.db")
        self._faiss_path = str(self._device_dir / "faiss.index")

        self._lock = threading.Lock()

        self._init_db()
        self._init_faiss(dim)

    # ----------------------------------------------------------
    # SQLite initialization
    # ----------------------------------------------------------

    def _init_db(self) -> None:
        """Initialize SQLite table schema with WAL mode."""
        conn = sqlite3.connect(self._db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS images (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path     TEXT NOT NULL,
                device_id      TEXT NOT NULL,
                timestamp      INTEGER NOT NULL,
                description    TEXT,
                source_type    TEXT NOT NULL CHECK(source_type IN ('stream', 'import')),
                embedding_mode TEXT NOT NULL DEFAULT 'text',
                created_at     TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE INDEX IF NOT EXISTS idx_images_timestamp ON images(timestamp);
            CREATE INDEX IF NOT EXISTS idx_images_device_id ON images(device_id);
        """)
        conn.close()

    # ----------------------------------------------------------
    # FAISS initialization
    # ----------------------------------------------------------

    def _init_faiss(self, dim: int) -> None:
        """Create or load FAISS IndexIDMap(IndexFlatIP) index from disk."""
        if faiss is None:
            raise RuntimeError("faiss-cpu not installed, cannot initialize IndexManager")

        if os.path.exists(self._faiss_path):
            try:
                self._index = faiss.read_index(self._faiss_path)
                logger.info("Loaded FAISS index: %s (%d vectors)",
                            self._faiss_path, self._index.ntotal)
            except Exception as e:
                logger.error("FAISS index file corrupted, rebuilding empty index: %s", e)
                self._index = faiss.IndexIDMap(faiss.IndexFlatIP(dim))
        else:
            self._index = faiss.IndexIDMap(faiss.IndexFlatIP(dim))
            logger.info("Created new FAISS index (dim=%d)", dim)

    # ----------------------------------------------------------
    # Add record
    # ----------------------------------------------------------

    def add(self, image_path: str, device_id: str, timestamp: int,
            description: Optional[str], source_type: str,
            embedding_mode: str, embedding: np.ndarray) -> int:
        """Insert a record (SQLite + FAISS), return the assigned ID.

        embedding should be an L2-normalized 1D float32 vector.
        """
        with self._lock:
            conn = sqlite3.connect(self._db_path)
            try:
                cur = conn.execute(
                    """INSERT INTO images
                       (image_path, device_id, timestamp, description,
                        source_type, embedding_mode)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (image_path, device_id, timestamp, description,
                     source_type, embedding_mode),
                )
                row_id = cur.lastrowid
                conn.commit()
            finally:
                conn.close()

            # Add to FAISS — requires (1, dim) float32 matrix and (1,) int64 ID array
            vec = np.asarray(embedding, dtype=np.float32).reshape(1, -1)
            ids = np.array([row_id], dtype=np.int64)
            self._index.add_with_ids(vec, ids)

            return row_id

    # ----------------------------------------------------------
    # Metadata query
    # ----------------------------------------------------------

    def get_metadata(self, ids: List[int]) -> List[dict]:
        """Get metadata from SQLite by ID list, return list of dicts."""
        if not ids:
            return []
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        try:
            placeholders = ",".join("?" for _ in ids)
            rows = conn.execute(
                f"SELECT * FROM images WHERE id IN ({placeholders})", ids
            ).fetchall()
        finally:
            conn.close()
        return [dict(r) for r in rows]

    def get_ids_in_time_range(self, time_start: Optional[int],
                               time_end: Optional[int]) -> List[int]:
        """Query record IDs within a time range from SQLite."""
        conn = sqlite3.connect(self._db_path)
        try:
            conditions = []
            params: list = []
            if time_start is not None:
                conditions.append("timestamp >= ?")
                params.append(time_start)
            if time_end is not None:
                conditions.append("timestamp <= ?")
                params.append(time_end)

            sql = "SELECT id FROM images"
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            rows = conn.execute(sql, params).fetchall()
        finally:
            conn.close()
        return [r[0] for r in rows]

    # ----------------------------------------------------------
    # FAISS vector search
    # ----------------------------------------------------------

    def search_by_vector(self, query_vec: np.ndarray, top_k: int,
                         id_filter: Optional[List[int]] = None
                         ) -> List[Tuple[int, float]]:
        """FAISS vector search, returns [(id, score), ...].

        When id_filter is not None, only searches within the specified ID subset.
        """
        if self._index.ntotal == 0:
            return []

        vec = np.asarray(query_vec, dtype=np.float32).reshape(1, -1)

        if id_filter is not None:
            if not id_filter:
                return []
            # Search all, then filter
            search_k = min(self._index.ntotal, max(top_k * 10, 200))
            scores, ids = self._index.search(vec, search_k)
            id_set = set(id_filter)
            results = []
            for score, idx in zip(scores[0], ids[0]):
                if idx == -1:
                    continue
                if int(idx) in id_set:
                    results.append((int(idx), float(score)))
                if len(results) >= top_k:
                    break
            return results
        else:
            k = min(top_k, self._index.ntotal)
            scores, ids = self._index.search(vec, k)
            results = []
            for score, idx in zip(scores[0], ids[0]):
                if idx == -1:
                    continue
                results.append((int(idx), float(score)))
            return results

    # ----------------------------------------------------------
    # Persistence
    # ----------------------------------------------------------

    def save(self) -> None:
        """Persist FAISS index to disk."""
        with self._lock:
            faiss.write_index(self._index, self._faiss_path)
            logger.info("FAISS index saved: %s (%d vectors)",
                        self._faiss_path, self._index.ntotal)

    # ----------------------------------------------------------
    # Expiration cleanup
    # ----------------------------------------------------------

    def purge_expired(self, retention_days: int) -> int:
        """Purge expired records (SQLite + FAISS + image files), return count deleted.

        Does nothing when retention_days=0.
        """
        if retention_days <= 0:
            return 0

        cutoff = int(_time.time()) - retention_days * 86400

        with self._lock:
            conn = sqlite3.connect(self._db_path)
            try:
                rows = conn.execute(
                    "SELECT id, image_path FROM images WHERE timestamp < ?",
                    (cutoff,),
                ).fetchall()

                if not rows:
                    conn.close()
                    return 0

                expired_ids = [r[0] for r in rows]
                expired_paths = [r[1] for r in rows]

                # Delete SQLite records
                placeholders = ",".join("?" for _ in expired_ids)
                conn.execute(
                    f"DELETE FROM images WHERE id IN ({placeholders})",
                    expired_ids,
                )
                conn.commit()
            finally:
                conn.close()

            # Remove vectors from FAISS IndexIDMap
            id_array = np.array(expired_ids, dtype=np.int64)
            self._index.remove_ids(id_array)

            # Delete image files
            for p in expired_paths:
                try:
                    path_obj = Path(p)
                    if path_obj.exists():
                        path_obj.unlink()
                        # Try to clean up empty date directories
                        parent = path_obj.parent
                        if parent.exists() and not any(parent.iterdir()):
                            parent.rmdir()
                except OSError as e:
                    logger.warning("Failed to delete image file: %s (%s)", p, e)

            deleted = len(expired_ids)
            logger.info("Purged %d expired records (retention_days=%d)",
                        deleted, retention_days)
            return deleted


# ============================================================
# KAMIVISION API — Cloud image description + vector generation
# ============================================================

import requests as _requests


def _kamivision_call(cfg: Config, detect_type: str,
                     image_b64: str = "", prompt: str = "") -> Optional[dict]:
    """Call Kamivision cloud API, return result dict or None on failure."""
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": cfg.KAMIVISION_API_KEY,
    }
    payload = {
        "detectType": detect_type,
        "detectSubType": "",
        "skillId": "SK_IMAGE_TEXT_SEARCH",
        "prompt": prompt,
        "imageFile": image_b64,
        "videoFile": "",
    }
    try:
        resp = _requests.post(cfg.KAMIVISION_API_URL, headers=headers,
                              json=payload, timeout=60)
        resp.raise_for_status()
        body = resp.json()
        if body.get("code") != 200:
            logger.error("Kamivision API error: %s", body.get("msg", ""))
            return None
        result_str = body.get("data", {}).get("result", "")
        if not result_str:
            return None
        return json.loads(result_str)
    except Exception as e:
        logger.error("Kamivision API call failed (%s): %s", detect_type, e)
        return None


def _parse_embedding(result: dict) -> Optional[np.ndarray]:
    """Parse embedding string from Kamivision result into numpy vector."""
    # Handle both dict and list responses
    if isinstance(result, list):
        # Direct embedding list
        try:
            vec = np.array(result, dtype=np.float32)
            norm = np.linalg.norm(vec)
            if norm < 1e-10:
                return vec
            return vec / norm
        except Exception as e:
            logger.error("Embedding parse failed (list): %s", e)
            return None
    
    emb_str = result.get("embedding", "")
    if not emb_str:
        return None
    try:
        raw = json.loads(emb_str)
        vec = np.array(raw, dtype=np.float32)
        norm = np.linalg.norm(vec)
        if norm < 1e-10:
            return vec
        return vec / norm
    except Exception as e:
        logger.error("Embedding parse failed: %s", e)
        return None


class VLMDescriber:
    """Call Kamivision SUMMARY API to generate image description + embedding.

    describe() returns (description, embedding) tuple from a single API call.
    Skipped when ENABLE_DESCRIPTION is false.
    """

    def __init__(self, cfg: Config):
        self.cfg = cfg

    def describe(self, image_path: str) -> Tuple[Optional[str], Optional[np.ndarray]]:
        """Generate image description and embedding vector; returns (None, None) on failure."""
        if not self.cfg.ENABLE_DESCRIPTION:
            logger.debug("Description generation disabled, skipping: %s", image_path)
            return None, None

        try:
            with open(image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode("utf-8")

            result = _kamivision_call(self.cfg, "SUMMARY", image_b64=img_b64)
            if result is None:
                logger.error("Image description generation failed: %s", image_path)
                return None, None

            description = result.get("summary", "").strip()
            description = description.replace("'", "").replace('"', "")
            embedding = _parse_embedding(result)

            logger.info("Image description complete: %s => %s", image_path,
                        description[:80] if description else "(empty)")
            return description or None, embedding

        except Exception as e:
            logger.error("Image description generation failed: %s => %s", image_path, e)
            return None, None


class EmbeddingGenerator:
    """Text embedding generator: calls Kamivision EMBED API for query text."""

    def __init__(self, cfg: Config):
        self.cfg = cfg

    def embed_query(self, query_text: str) -> Optional[np.ndarray]:
        """Generate embedding vector for search query text."""
        result = _kamivision_call(self.cfg, "EMBED", prompt=query_text)
        if result is None:
            logger.error("Query embedding generation failed: %s", query_text)
            return None
        return _parse_embedding(result)


# ============================================================
# IMAGE CAPTURER — Frame capture from video streams + user import
# ============================================================

import shutil
from collections import deque

SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}


class ImageCapturer:
    """Image capture module: video stream frame capture + user import.

    - start_capture(): Blocking stream capture, captures frames at CAPTURE_INTERVAL
    - stop_capture(): Graceful stop via threading.Event
    - import_images(path): Import single file or all supported images in a directory
    - _is_duplicate(): Pixel diff mean detection for duplicate frames
    - _save_frame(): Resize and save as JPEG
    """

    def __init__(self, cfg: Config, cam: CameraConfig = None):
        self.cfg = cfg
        self.cam = cam if cam else cfg.cameras[0]
        self._stop_event = threading.Event()
        self._pending: deque = deque()
        self._last_frame: Optional[np.ndarray] = None

    # ----------------------------------------------------------
    # Video stream frame capture
    # ----------------------------------------------------------

    def start_capture(self) -> None:
        """Blocking stream capture: captures frames at CAPTURE_INTERVAL.

        Auto-reconnect: waits RECONNECT_DELAY seconds after stream interruption.
        Call stop_capture() to set _stop_event for graceful exit.
        """
        import cv2

        cam = self.cam
        logger.info("=" * 60)
        logger.info("Starting capture device=%s stream=%s interval=%ds",
                     cam.DEVICE_ID, cam.STREAM_URL, cam.CAPTURE_INTERVAL)
        logger.info("Output=%dx%d duplicate_detection=%s (threshold=%.1f)",
                     cam.OUTPUT_WIDTH, cam.OUTPUT_HEIGHT,
                     cam.SKIP_DUPLICATE, cam.DUPLICATE_THRESHOLD)
        logger.info("=" * 60)

        reconnect_count = 0
        while not self._stop_event.is_set():
            reconnect_count += 1
            logger.info("Stream connection attempt #%d", reconnect_count)
            try:
                self._capture_loop(cv2)
            except Exception as e:
                logger.error("Stream exception: %s", e, exc_info=True)

            if self._stop_event.is_set():
                break

            logger.warning("Stream interrupted, reconnecting in %ds (attempt #%d)...",
                           cam.RECONNECT_DELAY, reconnect_count + 1)
        # Interruptible wait
            for _ in range(cam.RECONNECT_DELAY):
                if self._stop_event.is_set():
                    break
                _time.sleep(1)

    def _capture_loop(self, cv2) -> None:
        """Main capture loop: read frame → interval check → duplicate detection → save.

        Returns on stream disconnect; start_capture handles reconnection.
        """
        cam = self.cam
        logger.info("OpenCV connecting to stream: %s", cam.STREAM_URL)
        cap = cv2.VideoCapture(cam.STREAM_URL)

        if not cap.isOpened():
            logger.error("OpenCV cannot open stream: %s", cam.STREAM_URL)
            return

        consecutive_failures = 0
        last_capture_time = 0.0

        try:
            while not self._stop_event.is_set():
                ret, frame = cap.read()
                if not ret:
                    consecutive_failures += 1
                    if consecutive_failures > 100:
                        logger.warning("Stream disconnected after %d consecutive read failures",
                                       consecutive_failures)
                        break
                    _time.sleep(0.02)
                    continue

                consecutive_failures = 0
                now = _time.time()

                # Control capture frequency by CAPTURE_INTERVAL
                if now - last_capture_time < cam.CAPTURE_INTERVAL:
                    continue
                last_capture_time = now

                # Duplicate frame detection
                if cam.SKIP_DUPLICATE and self._last_frame is not None:
                    if self._is_duplicate(frame, self._last_frame):
                        logger.debug("Duplicate frame, skipping")
                        continue

                self._last_frame = frame.copy()

                # Save frame
                try:
                    saved_path = self._save_frame(frame)
                    self._pending.append(saved_path)
                    logger.info("Frame saved: %s", os.path.basename(saved_path))
                except Exception as e:
                    logger.error("Failed to save frame: %s", e)
        finally:
            cap.release()
            logger.info("OpenCV stream released")

    def stop_capture(self) -> None:
        """Gracefully stop frame capture."""
        logger.info("Stopping capture...")
        self._stop_event.set()
        logger.info("Capture stopped")

    # ----------------------------------------------------------
    # Frame save
    # ----------------------------------------------------------

    def _save_frame(self, frame: np.ndarray) -> str:
        """Resize frame and save as JPEG, return file path.

        Path format: {DATA_DIR}/{DEVICE_ID}/{YYYYMMDD}/{DEVICE_ID}_{unix_timestamp}.jpg
        """
        import cv2

        cam = self.cam
        cfg = self.cfg
        ts = int(_time.time())

        # Use configured timezone offset for local date directory
        utc_dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        local_dt = utc_dt + timedelta(hours=cfg.TIME_ZONE_OFFSET)
        date_str = local_dt.strftime("%Y%m%d")

        out_dir = os.path.join(cfg.DATA_DIR, cam.DEVICE_ID, date_str)
        Path(out_dir).mkdir(parents=True, exist_ok=True)

        fname = f"{cam.DEVICE_ID}_{ts}.jpg"
        out_path = os.path.join(out_dir, fname)

        # Resize to configured output dimensions
        resized = cv2.resize(frame, (cam.OUTPUT_WIDTH, cam.OUTPUT_HEIGHT))
        cv2.imwrite(out_path, resized)

        return out_path

    # ----------------------------------------------------------
    # Duplicate frame detection
    # ----------------------------------------------------------

    def _is_duplicate(self, new_frame: np.ndarray,
                      last_frame: np.ndarray) -> bool:
        """Pixel diff mean detection: determine if frame is a duplicate.

        Computes mean absolute pixel difference between two frames.
        Below DUPLICATE_THRESHOLD is considered duplicate.
        Always returns False when SKIP_DUPLICATE is false.
        """
        if not self.cam.SKIP_DUPLICATE:
            return False

        import cv2

        # Ensure both frames have same dimensions before comparison
        if new_frame.shape != last_frame.shape:
            h, w = last_frame.shape[:2]
            new_frame = cv2.resize(new_frame, (w, h))

        diff = np.abs(new_frame.astype(np.float32) - last_frame.astype(np.float32))
        mean_diff = float(np.mean(diff))

        return mean_diff < self.cam.DUPLICATE_THRESHOLD

    # ----------------------------------------------------------
    # User import
    # ----------------------------------------------------------

    def import_images(self, path: str) -> List[str]:
        """Import images from path (file or directory), return list of imported file paths.

        - Single file: validate format, copy to imported/ directory
        - Directory: recursively scan all supported format files and import each
        - Unsupported formats are logged and skipped
        """
        imported: List[str] = []

        if not os.path.exists(path):
            print(f"Error: path does not exist: {path}", file=sys.stderr)
            return imported

        if os.path.isfile(path):
            result = self._import_single(path)
            if result:
                imported.append(result)
        elif os.path.isdir(path):
            for root, _dirs, files in os.walk(path):
                for fname in sorted(files):
                    fpath = os.path.join(root, fname)
                    result = self._import_single(fpath)
                    if result:
                        imported.append(result)
        else:
            print(f"Error: unsupported path type: {path}", file=sys.stderr)

        logger.info("Import complete: %d images from %s", len(imported), path)
        return imported

    def _import_single(self, file_path: str) -> Optional[str]:
        """Import a single file: validate format → copy to imported/ directory.

        Returns destination path on success, None on failure.
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in SUPPORTED_FORMATS:
            print(f"Skipping unsupported format: {os.path.basename(file_path)} "
                  f"(format {ext} not in {SUPPORTED_FORMATS})",
                  file=sys.stderr)
            return None

        # Validate file is a valid image
        try:
            import cv2
            img = cv2.imread(file_path)
            if img is None:
                print(f"Skipping invalid image file: {os.path.basename(file_path)}",
                      file=sys.stderr)
                return None
        except Exception as e:
            print(f"Skipping unreadable file: {os.path.basename(file_path)} ({e})",
                  file=sys.stderr)
            return None

        # Copy to imported/ directory
        import_dir = os.path.join(self.cfg.DATA_DIR, self.cam.DEVICE_ID, "imported")
        Path(import_dir).mkdir(parents=True, exist_ok=True)

        dest = os.path.join(import_dir, os.path.basename(file_path))
        # Handle filename conflicts: append timestamp suffix
        if os.path.exists(dest):
            name, ext_part = os.path.splitext(os.path.basename(file_path))
            dest = os.path.join(import_dir,
                                f"{name}_{int(_time.time())}{ext_part}")

        shutil.copy2(file_path, dest)
        self._pending.append(dest)
        logger.info("Imported: %s => %s", file_path, dest)
        return dest


# ============================================================
# SEARCH ENGINE — Image content search engine
# ============================================================


class SearchEngine:
    """Image content search engine.

    FAISS vector search to match user queries against image vectors.
    Supports time range filtering, similarity threshold, and result count limits.
    Supports searching across multiple cameras (multiple IndexManagers).

    - search(): Natural language search, returns structured results
    - list_recent(): List non-duplicate images from the last N hours
    """

    def __init__(self, cfg: Config, indexes: list,
                 embedding_gen: EmbeddingGenerator):
        self.cfg = cfg
        # indexes: List[IndexManager] — one per camera
        self.indexes = indexes if isinstance(indexes, list) else [indexes]
        self.embedding_gen = embedding_gen

    # ----------------------------------------------------------
    # Main search method
    # ----------------------------------------------------------

    def search(self, query: str, time_start: Optional[int] = None,
               time_end: Optional[int] = None) -> dict:
        """Execute natural language search across all indexes.

        Flow:
        1. Query text -> vector (embed_query)
        2. For each index: time range filter + FAISS search
        3. Merge results, filter by threshold, sort by score
        4. Return at most SEARCH_TOP_K results
        """
        empty_result = {
            "status": "ok",
            "query": query,
            "count": 0,
            "results": [],
        }

        # 1. Generate query vector
        query_vec = self.embedding_gen.embed_query(query)
        if query_vec is None:
            logger.error("Query embedding generation failed: %s", query)
            return {
                "status": "error",
                "query": query,
                "count": 0,
                "results": [],
                "error": "Query embedding generation failed",
            }

        top_k = self.cfg.SEARCH_TOP_K
        threshold = self.cfg.SIMILARITY_THRESHOLD
        all_results = []  # [(rid, score, index_ref)]

        # 2. Search each index
        for idx in self.indexes:
            # Time range filter
            id_filter: Optional[List[int]] = None
            if time_start is not None or time_end is not None:
                id_filter = idx.get_ids_in_time_range(time_start, time_end)
                if not id_filter:
                    continue

            raw_results = idx.search_by_vector(query_vec, top_k, id_filter)
            for rid, score in raw_results:
                if score >= threshold:
                    all_results.append((rid, score, idx))

        if not all_results:
            logger.info("No matching results: %s", query)
            return empty_result

        # 3. Sort by score descending, take top_k
        all_results.sort(key=lambda x: x[1], reverse=True)
        all_results = all_results[:top_k]

        # 4. Fetch metadata and format results
        results = []
        for rid, score, idx in all_results:
            metadata_list = idx.get_metadata([rid])
            if not metadata_list:
                logger.warning("Metadata missing: id=%d", rid)
                continue
            meta = metadata_list[0]

            image_path = meta.get("image_path", "")
            image_name = os.path.basename(image_path) if image_path else ""
            timestamp = meta.get("timestamp", 0)
            time_str = timestamp_to_local_12hr(
                timestamp, self.cfg.TIME_ZONE_OFFSET
            )

            results.append({
                "image_name": image_name,
                "image_path": image_path,
                "description": meta.get("description", ""),
                "device_id": meta.get("device_id", ""),
                "timestamp": timestamp,
                "time": time_str,
                "score": round(float(score), 4),
            })

        return {
            "status": "ok",
            "query": query,
            "count": len(results),
            "results": results,
        }

    # ----------------------------------------------------------
    # List recent images
    # ----------------------------------------------------------

    def list_recent(self, hours: int = 24) -> dict:
        """List non-duplicate images from the last N hours across all indexes.

        Sorted by timestamp descending (newest first), deduplicates by image_path.
        Return format matches search() (score field set to 0).
        """
        now_ts = int(_time.time())
        time_start = now_ts - hours * 3600

        # Collect metadata from all indexes
        all_metadata = []
        for idx in self.indexes:
            ids = idx.get_ids_in_time_range(time_start=time_start, time_end=None)
            if ids:
                all_metadata.extend(idx.get_metadata(ids))

        if not all_metadata:
            return {
                "status": "ok",
                "query": f"recent:{hours}h",
                "count": 0,
                "results": [],
            }

        # Sort by timestamp descending
        all_metadata.sort(key=lambda m: m.get("timestamp", 0), reverse=True)

        # Deduplicate: keep first occurrence (newest) per image_path
        seen_paths: set = set()
        results = []
        for meta in all_metadata:
            image_path = meta.get("image_path", "")
            if image_path in seen_paths:
                continue
            seen_paths.add(image_path)

            image_name = os.path.basename(image_path) if image_path else ""
            timestamp = meta.get("timestamp", 0)
            time_str = timestamp_to_local_12hr(
                timestamp, self.cfg.TIME_ZONE_OFFSET
            )

            results.append({
                "image_name": image_name,
                "image_path": image_path,
                "description": meta.get("description", ""),
                "device_id": meta.get("device_id", ""),
                "timestamp": timestamp,
                "time": time_str,
                "score": 0,
            })

        return {
            "status": "ok",
            "query": f"recent:{hours}h",
            "count": len(results),
            "results": results,
        }


# ============================================================
# Image processing pipeline
# ============================================================

def process_image(image_path: str, cfg: Config, cam: CameraConfig,
                  index: IndexManager,
                  describer: VLMDescriber, embedding_gen: EmbeddingGenerator) -> None:
    """Process a single image: call cloud API for description + vector → write to index.

    Any step failure does not interrupt the flow; writes as much info as possible.
    """
    fname = os.path.basename(image_path)
    ts = int(_time.time())
    logger.info("Processing image: %s", fname)

    # Determine source type
    source_type = "import" if "/imported/" in image_path.replace("\\", "/") else "stream"

    # 1. Call cloud SUMMARY API for description + embedding
    description, embedding = describer.describe(image_path)
    if embedding is None:
        logger.warning("Embedding generation failed, skipping index: %s", fname)
        return

    # 2. Write to index
    try:
        row_id = index.add(
            image_path=image_path,
            device_id=cam.DEVICE_ID,
            timestamp=ts,
            description=description,
            source_type=source_type,
            embedding_mode="text",
            embedding=embedding,
        )
        index.save()
        logger.info("Image indexed: %s (id=%d)", fname, row_id)
    except Exception as e:
        logger.error("Failed to write index: %s => %s", fname, e)


# ============================================================
# PID file management — Background process start/stop
# ============================================================

import signal
import argparse


def _get_pid_file(cfg: Config, device_id: str) -> str:
    """PID file path: {DATA_DIR}/{device_id}/capturer.pid"""
    d = os.path.join(cfg.DATA_DIR, device_id)
    Path(d).mkdir(parents=True, exist_ok=True)
    return os.path.join(d, "capturer.pid")


def _read_pid(pid_file: str) -> Optional[int]:
    """Read PID file, return PID or None."""
    if not os.path.exists(pid_file):
        return None
    try:
        with open(pid_file, "r") as f:
            return int(f.read().strip())
    except (ValueError, OSError):
        return None


def _is_pid_alive(pid: int) -> bool:
    """Check if process is alive."""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _start_daemon(cfg: Config, device_id: str, script_path: str,
                  config_path: str, log_file: str) -> dict:
    """Start frame capture for a specific camera as a background process."""
    import subprocess
    pid_file = _get_pid_file(cfg, device_id)
    existing_pid = _read_pid(pid_file)

    if existing_pid and _is_pid_alive(existing_pid):
        return {"status": "already_running", "pid": existing_pid,
                "device_id": device_id,
                "message": f"Capture already running (PID={existing_pid})"}

    # Prefer venv python
    venv_python = os.path.join(
        os.path.dirname(os.path.abspath(script_path)), ".venv", "bin", "python")
    if not os.path.exists(venv_python):
        venv_python = sys.executable

    # Per-camera log file
    log_base, log_ext = os.path.splitext(log_file)
    cam_log = f"{log_base}_{device_id}{log_ext}"

    cmd = [venv_python, os.path.abspath(script_path),
           "--config", config_path, "--device", device_id,
           "--log-file", cam_log]

    proc = subprocess.Popen(
        cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    with open(pid_file, "w") as f:
        f.write(str(proc.pid))

    return {"status": "started", "pid": proc.pid, "device_id": device_id,
            "message": f"Capture started (PID={proc.pid})", "log_file": cam_log}


def _stop_daemon(cfg: Config, device_id: str) -> dict:
    """Stop background capture process for a specific camera."""
    pid_file = _get_pid_file(cfg, device_id)
    pid = _read_pid(pid_file)

    if pid is None:
        return {"status": "not_running", "device_id": device_id,
                "message": "No running capture process found"}

    if not _is_pid_alive(pid):
        os.remove(pid_file)
        return {"status": "not_running", "device_id": device_id,
                "message": f"Process (PID={pid}) no longer exists, PID file cleaned up"}

    # Send SIGTERM for graceful stop
    os.kill(pid, signal.SIGTERM)
    # Wait up to 10 seconds
    for _ in range(20):
        if not _is_pid_alive(pid):
            break
        _time.sleep(0.5)

    if _is_pid_alive(pid):
        os.kill(pid, signal.SIGKILL)
        _time.sleep(0.5)

    if os.path.exists(pid_file):
        os.remove(pid_file)

    return {"status": "stopped", "pid": pid, "device_id": device_id,
            "message": f"Capture stopped (PID={pid})"}


def _get_status(cfg: Config, device_id: str) -> dict:
    """Get capture process status for a specific camera."""
    pid_file = _get_pid_file(cfg, device_id)
    pid = _read_pid(pid_file)

    if pid is None:
        return {"status": "not_running", "device_id": device_id,
                "message": "Capture not running"}

    if _is_pid_alive(pid):
        return {"status": "running", "pid": pid, "device_id": device_id,
                "message": f"Capture running (PID={pid})"}
    else:
        os.remove(pid_file)
        return {"status": "not_running", "device_id": device_id,
                "message": f"Process (PID={pid}) no longer exists, PID file cleaned up"}


def _start_all(cfg: Config, script_path: str, config_path: str, log_file: str) -> dict:
    """Start capture for all cameras, return aggregated status."""
    results = []
    for cam in cfg.cameras:
        r = _start_daemon(cfg, cam.DEVICE_ID, script_path, config_path, log_file)
        results.append(r)
    return {"status": "ok", "cameras": results}


def _stop_all(cfg: Config) -> dict:
    """Stop capture for all cameras, return aggregated status."""
    results = []
    for cam in cfg.cameras:
        r = _stop_daemon(cfg, cam.DEVICE_ID)
        results.append(r)
    return {"status": "ok", "cameras": results}


def _get_status_all(cfg: Config) -> dict:
    """Get capture status for all cameras."""
    results = []
    for cam in cfg.cameras:
        r = _get_status(cfg, cam.DEVICE_ID)
        results.append(r)
    return {"status": "ok", "cameras": results}


# ============================================================
# CLI entry point
# ============================================================

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_config = os.path.join(script_dir, "image_config.json")
    default_log = os.path.join(script_dir, "image_search.log")

    parser = argparse.ArgumentParser(description="AI-powered image content search")
    parser.add_argument("--config", default=default_config,
                        help="Config file path")
    parser.add_argument("--start-capture", action="store_true",
                        help="Start background frame capture")
    parser.add_argument("--stop-capture", action="store_true",
                        help="Stop background frame capture")
    parser.add_argument("--status", action="store_true",
                        help="Check capture process status")
    parser.add_argument("--import", dest="import_path", type=str, default=None,
                        metavar="PATH", help="Import images (file or directory)")
    parser.add_argument("--search", type=str, default=None,
                        help="Search mode: enter query text")
    parser.add_argument("--list", type=int, default=None, metavar="HOURS",
                        help="List images from the last N hours")
    parser.add_argument("--json", action="store_true",
                        help="Output results in JSON format")
    parser.add_argument("--time-start", type=int, default=None,
                        help="Search time range start (unix timestamp)")
    parser.add_argument("--time-end", type=int, default=None,
                        help="Search time range end (unix timestamp)")
    parser.add_argument("--log-level", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                        help="Log level (default INFO)")
    parser.add_argument("--log-file", default=None,
                        help="Log output file path")
    parser.add_argument("--export-config", action="store_true",
                        help="Export default config to JSON file")
    parser.add_argument("--device", type=str, default=None,
                        help="Target camera DEVICE_ID (for per-camera operations)")

    args = parser.parse_args()

    # Background process management commands don't need stderr logging
    if not (args.start_capture or args.stop_capture or args.status):
        setup_logging(
            level=getattr(logging, args.log_level),
            log_file=args.log_file,
        )

    # Load config
    cfg = Config.from_json(args.config)

    # --- Background process management ---
    if args.start_capture:
        if args.device:
            cam = cfg.get_camera(args.device)
            if not cam:
                print(json.dumps({"status": "error",
                       "message": f"DEVICE_ID '{args.device}' not found in config"},
                      ensure_ascii=False))
                sys.exit(1)
            result = _start_daemon(cfg, args.device, __file__, args.config,
                                   args.log_file or default_log)
        else:
            result = _start_all(cfg, __file__, args.config,
                                args.log_file or default_log)
        print(json.dumps(result, ensure_ascii=False))
        return

    if args.stop_capture:
        if args.device:
            cam = cfg.get_camera(args.device)
            if not cam:
                print(json.dumps({"status": "error",
                       "message": f"DEVICE_ID '{args.device}' not found in config"},
                      ensure_ascii=False))
                sys.exit(1)
            result = _stop_daemon(cfg, args.device)
        else:
            result = _stop_all(cfg)
        print(json.dumps(result, ensure_ascii=False))
        return

    if args.status:
        if args.device:
            cam = cfg.get_camera(args.device)
            if not cam:
                print(json.dumps({"status": "error",
                       "message": f"DEVICE_ID '{args.device}' not found in config"},
                      ensure_ascii=False))
                sys.exit(1)
            result = _get_status(cfg, args.device)
        else:
            result = _get_status_all(cfg)
        print(json.dumps(result, ensure_ascii=False))
        return

    # --- Export config ---
    if args.export_config:
        cfg_data = {k: v for k, v in vars(Config).items()
                    if not k.startswith("_") and not callable(v)}
        cfg_data.update(vars(cfg))
        with open(args.config, "w", encoding="utf-8") as f:
            json.dump(cfg_data, f, indent=2, ensure_ascii=False)
        print(json.dumps({"status": "ok",
                          "message": f"Config exported to {args.config}"},
                         ensure_ascii=False))
        return

    # --- Create core components ---
    embedding_gen = EmbeddingGenerator(cfg)
    describer = VLMDescriber(cfg)

    # Determine target cameras for search/list/import
    if args.device:
        cam = cfg.get_camera(args.device)
        if not cam:
            print(f"Error: DEVICE_ID '{args.device}' not found in config",
                  file=sys.stderr)
            sys.exit(1)
        target_cams = [cam]
    else:
        target_cams = cfg.cameras

    # Build IndexManagers for target cameras
    indexes = [IndexManager(cfg.DATA_DIR, cam.DEVICE_ID) for cam in target_cams]

    # --- Search mode ---
    if args.search:
        logger.info("Entering search mode: query='%s'", args.search)
        engine = SearchEngine(cfg, indexes, embedding_gen)
        result = engine.search(args.search,
                               time_start=args.time_start,
                               time_end=args.time_end)
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            results = result.get("results", [])
            if not results:
                print("No matching images found.")
            else:
                print(f"\nFound {len(results)} matching images:\n")
                for i, r in enumerate(results, 1):
                    device_tag = f"[{r.get('device_id', '')}]" if r.get('device_id') else ""
                    print(f"  [{i}] {r['time']}  score={r['score']:.3f}  {device_tag}")
                    desc = r.get("description") or "(no description)"
                    print(f"      {desc}")
                    print(f"      {r['image_path']}\n")
        return

    # --- List mode ---
    if args.list is not None:
        logger.info("Entering list mode: last %d hours", args.list)
        engine = SearchEngine(cfg, indexes, embedding_gen)
        result = engine.list_recent(args.list)
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            results = result.get("results", [])
            if not results:
                print("No records.")
            else:
                print(f"\n{len(results)} images in the last {args.list} hours:\n")
                for r in results:
                    desc = r.get("description") or "(no description)"
                    device_tag = f"[{r.get('device_id', '')}]" if r.get('device_id') else ""
                    print(f"  {r['time']}  {desc[:60]}  {device_tag}")
        return

    # --- Import mode ---
    if args.import_path:
        logger.info("Entering import mode: %s", args.import_path)
        # Import targets first camera in target_cams
        import_cam = target_cams[0]
        import_index = indexes[0]
        capturer = ImageCapturer(cfg, import_cam)
        imported = capturer.import_images(args.import_path)
        for img_path in imported:
            process_image(img_path, cfg, import_cam, import_index,
                          describer, embedding_gen)
        if args.json:
            print(json.dumps({"status": "ok", "imported": len(imported),
                              "device_id": import_cam.DEVICE_ID},
                             ensure_ascii=False))
        else:
            print(f"Import complete: {len(imported)} images processed"
                  f" (device={import_cam.DEVICE_ID})")
        return

    # --- Default: foreground capture mode (called by daemon) ---
    # Foreground mode REQUIRES --device to specify which camera to capture
    if not args.device:
        print("Error: foreground capture mode requires --device DEVICE_ID",
              file=sys.stderr)
        sys.exit(1)

    cam = cfg.get_camera(args.device)
    if not cam:
        print(f"Error: DEVICE_ID '{args.device}' not found in config",
              file=sys.stderr)
        sys.exit(1)

    index = IndexManager(cfg.DATA_DIR, cam.DEVICE_ID)
    logger.info("Entering capture mode (foreground) device=%s", cam.DEVICE_ID)
    capturer = ImageCapturer(cfg, cam)

    # Background processing thread: dequeue images and run pipeline
    def _process_worker():
        while not capturer._stop_event.is_set():
            if capturer._pending:
                img_path = capturer._pending.popleft()
                try:
                    process_image(img_path, cfg, cam, index,
                                  describer, embedding_gen)
                except Exception as e:
                    logger.error("Image processing error: %s => %s",
                                 os.path.basename(img_path), e, exc_info=True)
            else:
                _time.sleep(0.5)

    worker = threading.Thread(target=_process_worker, daemon=True)
    worker.start()
    logger.info("Image processing thread started")

    # Expiration cleanup thread: runs every hour
    def _purge_loop():
        while not capturer._stop_event.is_set():
            try:
                deleted = index.purge_expired(cfg.RETENTION_DAYS)
                if deleted:
                    logger.info("Expiration cleanup: deleted %d records", deleted)
            except Exception as e:
                logger.error("Expiration cleanup error: %s", e)
            for _ in range(3600):
                if capturer._stop_event.is_set():
                    break
                _time.sleep(1)

    purger = threading.Thread(target=_purge_loop, daemon=True)
    purger.start()
    logger.info("Expiration cleanup thread started (interval=1h, retention=%dd)", cfg.RETENTION_DAYS)

    # Signal handling
    def signal_handler(sig, frame):
        logger.info("Received signal %s, stopping", signal.Signals(sig).name)
        capturer.stop_capture()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start capture (blocking)
    capturer.start_capture()


if __name__ == "__main__":
    main()
