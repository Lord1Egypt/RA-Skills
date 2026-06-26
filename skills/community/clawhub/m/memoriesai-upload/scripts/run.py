#!/usr/bin/env python3
"""Luci-upload — upload a video or image to memories.ai with time and location metadata.

Usage:
    python run.py --file /path/to/video.mp4
    python run.py --file /path/to/photo.png --datetime "2025-09-01 00:00:00" --timezone Asia/Shanghai --location "Shunde, China"
    python run.py --file /path/to/video.mp4 --time 1769097600000 --lon 120.59 --lat 31.3
    python run.py --probe /path/to/file   # just show extracted metadata, don't upload
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
import mimetypes
import uuid
import re

API_HOST = "https://mavi-backend.memories.ai"
UPLOAD_PATH = "/serve/luci/api/manual/upload"
USERINFO_API = API_HOST + "/serve/api/userinfo"

ENV_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")


def _load_env():
    """Load MEMORIES_AI_KEY from .env file next to the skill root."""
    if not os.path.exists(ENV_FILE):
        return None
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line.startswith("MEMORIES_AI_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def get_api_key():
    api_key = os.environ.get("MEMORIES_AI_KEY", "").strip() or _load_env()
    if not api_key:
        print("Error: MEMORIES_AI_KEY not found.", file=sys.stderr)
        print(f"Please create {ENV_FILE} with:", file=sys.stderr)
        print("  MEMORIES_AI_KEY=sk-your-key-here", file=sys.stderr)
        sys.exit(1)
    return api_key


# ---------------------------------------------------------------------------
# Metadata extraction via ffprobe
# ---------------------------------------------------------------------------

def probe_video(filepath):
    """Extract creation time and GPS from media metadata using ffprobe.

    Works for video and (sometimes) JPEG/HEIC images with embedded EXIF.
    Returns empty values for formats without metadata (e.g. PNG screenshots).
    """
    info = {"creation_time": None, "latitude": None, "longitude": None}
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", filepath],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            return info
        data = json.loads(result.stdout)
    except (FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired):
        return info

    tags = data.get("format", {}).get("tags", {})

    # Creation time
    for key in ("creation_time", "com.apple.quicktime.creationdate", "date"):
        val = tags.get(key)
        if val:
            info["creation_time"] = val
            break

    # GPS — common in iPhone/Android videos
    location_str = tags.get("com.apple.quicktime.location.ISO6709") or tags.get("location")
    if location_str:
        # ISO 6709: +31.3000+120.5900+... or +31.3000+120.5900/
        match = re.match(r'([+-][\d.]+)([+-][\d.]+)', location_str)
        if match:
            info["latitude"] = float(match.group(1))
            info["longitude"] = float(match.group(2))

    return info


# ---------------------------------------------------------------------------
# Geocoding via Nominatim (free, no key)
# ---------------------------------------------------------------------------

def geocode(location_name):
    """Convert a location name to (latitude, longitude) using Nominatim."""
    params = urllib.parse.urlencode({"q": location_name, "format": "json", "limit": 1})
    url = f"https://nominatim.openstreetmap.org/search?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "luci-upload-skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            results = json.loads(resp.read())
        if results:
            return float(results[0]["lat"]), float(results[0]["lon"])
    except Exception as e:
        print(f"Warning: geocoding failed for '{location_name}': {e}", file=sys.stderr)
    return None, None


# ---------------------------------------------------------------------------
# Time parsing
# ---------------------------------------------------------------------------

def parse_datetime_to_epoch_ms(dt_str, tz_str=None):
    """Parse a datetime string to epoch milliseconds.

    Supports:
      - ISO 8601 with timezone: 2025-06-22T14:00:00+08:00
      - Date + time: 2025-06-22 14:00:00 (needs tz_str)
      - Date only: 2025-06-22 (assumes noon, needs tz_str)
      - Epoch ms directly: 1769097600000
    """
    # Already epoch ms?
    if dt_str.isdigit() and len(dt_str) >= 12:
        return int(dt_str)

    tz = None
    if tz_str:
        # Handle common timezone offsets
        tz_offsets = {
            "Asia/Shanghai": 8, "Asia/Tokyo": 9, "Asia/Seoul": 9,
            "US/Eastern": -5, "US/Central": -6, "US/Mountain": -7, "US/Pacific": -8,
            "America/New_York": -5, "America/Chicago": -6, "America/Los_Angeles": -8,
            "Europe/London": 0, "Europe/Paris": 1, "Europe/Berlin": 1,
            "UTC": 0,
        }
        offset_hours = tz_offsets.get(tz_str)
        if offset_hours is not None:
            tz = timezone(timedelta(hours=offset_hours))
        else:
            # Try parsing as +HH:MM or numeric offset
            try:
                tz = timezone(timedelta(hours=float(tz_str)))
            except (ValueError, TypeError):
                print(f"Warning: unknown timezone '{tz_str}', assuming UTC", file=sys.stderr)
                tz = timezone.utc
    else:
        tz = timezone.utc

    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(dt_str.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=tz)
            return int(dt.timestamp() * 1000)
        except ValueError:
            continue

    print(f"Error: could not parse datetime '{dt_str}'", file=sys.stderr)
    sys.exit(1)


def parse_ffprobe_time(creation_time_str):
    """Parse ffprobe creation_time to epoch ms. These are usually UTC."""
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d %H:%M:%S"):
        try:
            dt = datetime.strptime(creation_time_str.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp() * 1000)
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------

def multipart_upload(filepath, start_time_ms, longitude, latitude, api_key):
    """Upload media file via multipart/form-data POST."""
    boundary = uuid.uuid4().hex
    filename = os.path.basename(filepath)

    # Build query string
    params = urllib.parse.urlencode({
        "startTime": start_time_ms,
        "longitude": longitude,
        "latitude": latitude,
    })
    url = f"{API_HOST}{UPLOAD_PATH}?{params}"

    # Build multipart body
    with open(filepath, "rb") as f:
        file_data = f.read()

    content_type = mimetypes.guess_type(filepath)[0] or "application/octet-stream"

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n"
        f"\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "authorization": api_key,
    })

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"Error: HTTP {e.code} from upload API\n{error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Upload video or image to memories.ai")
    parser.add_argument("--file", "-f", required=True, help="Path to video or image file")
    parser.add_argument("--probe", action="store_true", help="Only show extracted metadata, don't upload")
    # Explicit overrides
    parser.add_argument("--time", default=None, help="Start time as epoch ms (e.g. 1769097600000)")
    parser.add_argument("--datetime", default=None, help="Start time as datetime (e.g. '2025-06-22 14:00:00')")
    parser.add_argument("--timezone", default=None, help="Timezone for --datetime (e.g. Asia/Shanghai, UTC, +8)")
    parser.add_argument("--lat", type=float, default=None, help="Latitude")
    parser.add_argument("--lon", type=float, default=None, help="Longitude")
    parser.add_argument("--location", default=None, help="Location name to geocode (e.g. 'Suzhou, China')")
    args = parser.parse_args()

    filepath = os.path.expanduser(args.file)
    if not os.path.isfile(filepath):
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    # Step 1: Probe file metadata
    print(f"Probing file: {filepath}")
    meta = probe_video(filepath)
    print(f"  creation_time: {meta['creation_time'] or 'not found'}")
    print(f"  latitude: {meta['latitude'] or 'not found'}")
    print(f"  longitude: {meta['longitude'] or 'not found'}")

    if args.probe:
        return

    # Step 2: Resolve start time
    start_time_ms = None
    if args.time:
        start_time_ms = int(args.time)
    elif args.datetime:
        start_time_ms = parse_datetime_to_epoch_ms(args.datetime, args.timezone)
    elif meta["creation_time"]:
        start_time_ms = parse_ffprobe_time(meta["creation_time"])
        if start_time_ms:
            print(f"  → using embedded creation time: {start_time_ms} ms")

    if start_time_ms is None:
        print("Error: could not determine capture time.", file=sys.stderr)
        print("Please provide --time (epoch ms), --datetime, or a file with creation_time metadata.", file=sys.stderr)
        sys.exit(1)

    # Step 3: Resolve location
    lat, lon = args.lat, args.lon
    if lat is None or lon is None:
        if args.location:
            lat, lon = geocode(args.location)
            if lat is not None:
                print(f"  → geocoded '{args.location}' to lat={lat}, lon={lon}")
        elif meta["latitude"] is not None and meta["longitude"] is not None:
            lat, lon = meta["latitude"], meta["longitude"]
            print(f"  → using embedded GPS: lat={lat}, lon={lon}")

    if lat is None or lon is None:
        print("Error: could not determine location.", file=sys.stderr)
        print("Please provide --lat/--lon, --location, or a file with GPS metadata.", file=sys.stderr)
        sys.exit(1)

    # Step 4: Upload
    api_key = get_api_key()
    print(f"\nUploading {os.path.basename(filepath)}...")
    print(f"  startTime: {start_time_ms}")
    print(f"  longitude: {lon}, latitude: {lat}")

    result = multipart_upload(filepath, start_time_ms, lon, lat, api_key)
    print(f"\nUpload result: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    main()
