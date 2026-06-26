"""
IMA Media Utilities
Version: 1.0.0

Handles media file type detection and metadata extraction.
"""

import mimetypes
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple

import requests

from ima_logger import get_logger

logger = get_logger()

# Media type detection
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".webm", ".mkv", ".flv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}


def detect_media_type(path_or_url: str) -> Literal["image", "video", "audio", "unknown"]:
    """
    Detect media type from file extension.
    
    Args:
        path_or_url: Local file path or remote URL
        
    Returns:
        "image" | "video" | "audio" | "unknown"
    """
    ext = Path(path_or_url).suffix.lower()
    
    if ext in IMAGE_EXTENSIONS:
        return "image"
    elif ext in VIDEO_EXTENSIONS:
        return "video"
    elif ext in AUDIO_EXTENSIONS:
        return "audio"
    else:
        return "unknown"


def get_image_dimensions(file_path: str) -> Tuple[int, int]:
    """
    Get image dimensions using PIL (if available) or ffprobe.
    
    Returns:
        (width, height) or (0, 0) if detection fails
    """
    try:
        # Try PIL first (faster)
        from PIL import Image
        with Image.open(file_path) as img:
            return img.size  # (width, height)
    except ImportError:
        # Fallback to ffprobe
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height",
                 "-of", "csv=s=x:p=0", file_path],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                width, height = map(int, result.stdout.strip().split('x'))
                return (width, height)
        except Exception as e:
            logger.warning(f"Failed to get image dimensions: {e}")
    except Exception as e:
        logger.warning(f"Failed to get image dimensions: {e}")
    
    return (0, 0)


def get_video_metadata(file_path: str) -> Dict[str, any]:
    """
    Get video metadata using ffprobe.
    
    Returns:
        {
            "duration": float (seconds),
            "width": int,
            "height": int,
            "fps": float
        }
    """
    try:
        # Get duration
        duration_result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            capture_output=True, text=True, timeout=10
        )
        duration = float(duration_result.stdout.strip()) if duration_result.returncode == 0 else 0.0
        
        # Get dimensions and fps
        dimension_result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,r_frame_rate",
             "-of", "default=noprint_wrappers=1", file_path],
            capture_output=True, text=True, timeout=10
        )
        if dimension_result.returncode == 0:
            width = height = 0
            fps = 0.0
            for line in dimension_result.stdout.strip().splitlines():
                if line.startswith("width="):
                    width = int(line.split("=", 1)[1])
                elif line.startswith("height="):
                    height = int(line.split("=", 1)[1])
                elif line.startswith("r_frame_rate="):
                    frame_rate = line.split("=", 1)[1]
                    if "/" in frame_rate:
                        numerator, denominator = frame_rate.split("/", 1)
                        denominator_value = float(denominator or 0)
                        fps = float(numerator) / denominator_value if denominator_value else 0.0
                    else:
                        fps = float(frame_rate)
        else:
            width, height, fps = 0, 0, 0.0
        
        return {
            "duration": duration,
            "width": width,
            "height": height,
            "fps": fps,
        }
    except Exception as e:
        logger.warning(f"Failed to get video metadata: {e}")
        return {"duration": 0.0, "width": 0, "height": 0, "fps": 0.0}


def download_remote_media_to_temp(url: str, suffix: str = "") -> str:
    """Download remote media URL to a temporary local file and return the path."""
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            for chunk in response.iter_content(chunk_size=1024 * 64):
                if chunk:
                    temp_file.write(chunk)
            return temp_file.name


def extract_video_cover_frame(file_path: str) -> str:
    """Extract the first frame of a video to a temporary JPEG file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        output_path = temp_file.name

    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                file_path,
                "-frames:v",
                "1",
                "-q:v",
                "2",
                output_path,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "ffmpeg cover extraction failed")
        return output_path
    except Exception:
        if os.path.exists(output_path):
            os.unlink(output_path)
        raise


def get_audio_duration(file_path: str) -> float:
    """
    Get audio duration using ffprobe.
    
    Returns:
        duration in seconds, or 0.0 if detection fails
    """
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
    except Exception as e:
        logger.warning(f"Failed to get audio duration: {e}")
    
    return 0.0


def extract_media_metadata(file_path: str, media_type: str, url: str) -> Dict:
    """
    Extract metadata based on media type.
    
    Args:
        file_path: Local file path (for metadata extraction)
        media_type: "image" | "video" | "audio"
        url: Remote URL (after upload)
        
    Returns:
        dict with structure matching IMA API requirements:
        - image: {"url": str, "width": int, "height": int}
        - video: {"url": str, "duration": float, "width": int, "height": int, "cover": str}
        - audio: {"url": str, "duration": float}
    """
    if media_type == "image":
        width, height = get_image_dimensions(file_path)
        return {
            "url": url,
            "width": width,
            "height": height
        }
    
    elif media_type == "video":
        metadata = get_video_metadata(file_path)
        return {
            "url": url,
            "duration": metadata["duration"],
            "width": metadata["width"],
            "height": metadata["height"],
            "fps": metadata["fps"],
            "cover": ""  # Cover image URL (optional, can be generated later)
        }
    
    elif media_type == "audio":
        duration = get_audio_duration(file_path)
        return {
            "url": url,
            "duration": duration
        }
    
    else:
        # Unknown type, return minimal structure
        return {"url": url}


def classify_media_inputs(urls_with_metadata: List[Dict]) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Classify processed media into images, videos, and audio.
    
    Args:
        urls_with_metadata: List of dicts with {"url": str, "type": str, ...metadata}
        
    Returns:
        (images, videos, audios) - three lists of metadata dicts
    """
    images = []
    videos = []
    audios = []
    
    for item in urls_with_metadata:
        media_type = item.get("type", "unknown")
        # Remove "type" key before adding to result (not needed in API)
        metadata = {k: v for k, v in item.items() if k != "type"}
        
        if media_type == "image":
            images.append(metadata)
        elif media_type == "video":
            videos.append(metadata)
        elif media_type == "audio":
            audios.append(metadata)
    
    return (images, videos, audios)
