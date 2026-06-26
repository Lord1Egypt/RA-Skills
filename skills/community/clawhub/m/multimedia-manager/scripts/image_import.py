#!/usr/bin/env python3
"""Import images into the vault — copy, generate thumbnails, extract metadata."""

import sys
import os
import shutil
import json
from pathlib import Path
from datetime import datetime

from PIL import Image, ExifTags

sys.path.insert(0, os.path.dirname(__file__))
from image_db import (
    get_db, init_db, file_hash, generate_vault_filename, image_exists,
    add_image, update_image, extract_gps_from_exif,
    ORIGINALS_DIR, THUMBNAILS_DIR,
)

THUMB_SIZE = (400, 400)
SUPPORTED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff", ".svg"}
SUPPORTED_VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".3gp", ".flv"}
SUPPORTED_EXTS = SUPPORTED_IMAGE_EXTS | SUPPORTED_VIDEO_EXTS

SOURCE_HINTS = {
    "image-gen": "generated",
    "img_": "generated",
    "screenshot": "screenshot",
    "calib": "screenshot",
    "cover": "generated",
    "wechat_templates": "template",
}


def guess_source(filepath: str) -> str:
    fp = filepath.lower()
    for hint, src in SOURCE_HINTS.items():
        if hint in fp:
            return src
    return "imported"


def guess_category(filepath: str, source: str) -> str:
    fp = filepath.lower()
    if source == "generated":
        return "ai-generated"
    if source == "screenshot":
        return "screenshots"
    if source == "template":
        return "templates"
    if "cover" in fp:
        return "covers"
    if "家庭" in fp or "family" in fp:
        return "family"
    return "uncategorized"


def extract_exif_date(filepath: str) -> str | None:
    try:
        img = Image.open(filepath)
        exif = img._getexif()
        if exif:
            for tag_id, value in exif.items():
                tag = ExifTags.TAGS.get(tag_id, "")
                if tag == "DateTimeOriginal":
                    dt = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    return dt.isoformat()
    except Exception:
        pass
    return None


def create_thumbnail(src: str, dst: str):
    try:
        img = Image.open(src)
        img.thumbnail(THUMB_SIZE, Image.LANCZOS)
        has_alpha = img.mode in ("RGBA", "LA", "PA") or (img.mode == "P" and "transparency" in img.info)
        if has_alpha:
            img = img.convert("RGBA")
            bg = Image.new("RGBA", img.size, (30, 30, 30, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg.convert("RGB")
        elif img.mode not in ("RGB",):
            img = img.convert("RGB")
        dst_path = Path(dst).with_suffix(".webp")
        img.save(str(dst_path), "WEBP", quality=82, method=4)
        return str(dst_path)
    except Exception as e:
        print(f"  [WARN] Thumbnail failed for {src}: {e}")
        return None


def is_video(filepath: str) -> bool:
    return Path(filepath).suffix.lower() in SUPPORTED_VIDEO_EXTS


def extract_video_metadata(filepath: str) -> dict:
    """Extract video duration, width, height using ffprobe."""
    import subprocess
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_format", "-show_streams", filepath
        ]
        out = subprocess.check_output(cmd, timeout=15, text=True)
        data = json.loads(out)
        duration = float(data.get("format", {}).get("duration", 0))
        width, height = None, None
        for s in data.get("streams", []):
            if s.get("codec_type") == "video":
                width = s.get("width")
                height = s.get("height")
                break
        return {"duration": round(duration, 1), "width": width, "height": height}
    except Exception as e:
        print(f"  [WARN] ffprobe failed: {e}")
        return {}


def extract_video_cover(video_path: str, output_path: str, timestamp: float = 1.0) -> str | None:
    """Extract a single frame from video as cover image using ffmpeg."""
    import subprocess
    try:
        cmd = [
            "ffmpeg", "-y", "-ss", str(timestamp),
            "-i", video_path, "-frames:v", "1",
            "-q:v", "2", output_path
        ]
        subprocess.run(cmd, capture_output=True, timeout=15)
        if os.path.isfile(output_path) and os.path.getsize(output_path) > 0:
            return output_path
    except Exception as e:
        print(f"  [WARN] ffmpeg cover extraction failed: {e}")
    return None


def _ai_analyze(filepath: str) -> dict:
    """AI analysis stub — Pro feature, always returns empty in Community."""
    return {}


def import_single(filepath: str, source: str = None, category: str = None,
                  description: str = None, tags: list = None, copy: bool = True,
                  auto_tag: bool = True) -> dict:
    """Import a single image or video into the vault. Returns metadata dict."""
    filepath = os.path.abspath(filepath)
    if not os.path.isfile(filepath):
        return {"error": f"File not found: {filepath}"}

    ext = Path(filepath).suffix.lower()
    if ext not in SUPPORTED_EXTS:
        return {"error": f"Unsupported format: {ext}"}

    is_vid = is_video(filepath)
    fhash = file_hash(filepath)
    conn = get_db()

    if image_exists(conn, fhash):
        conn.close()
        return {"skipped": True, "reason": "duplicate", "hash": fhash, "path": filepath}

    source = source or guess_source(filepath)
    vault_name = generate_vault_filename(filepath, source)
    final_category = category or guess_category(filepath, source)
    cat_dir = os.path.join(ORIGINALS_DIR, final_category)
    os.makedirs(cat_dir, exist_ok=True)
    vault_path = os.path.join(cat_dir, vault_name)

    if copy:
        shutil.copy2(filepath, vault_path)
    else:
        shutil.move(filepath, vault_path)

    thumb_cat_dir = os.path.join(THUMBNAILS_DIR, final_category)
    os.makedirs(thumb_cat_dir, exist_ok=True)

    width, height, fmt, duration, cover_path, thumb_path = None, None, ext.lstrip("."), None, None, None

    if is_vid:
        vid_meta = extract_video_metadata(vault_path)
        width = vid_meta.get("width")
        height = vid_meta.get("height")
        duration = vid_meta.get("duration")
        fmt = ext.lstrip(".")

        cover_name = Path(vault_name).stem + "_cover.jpg"
        cover_dst = os.path.join(thumb_cat_dir, cover_name)
        ts = min(1.0, (duration or 2) / 3)
        cover_path = extract_video_cover(vault_path, cover_dst, timestamp=ts)

        if cover_path:
            thumb_dst = os.path.join(thumb_cat_dir, vault_name)
            thumb_path = create_thumbnail(cover_path, thumb_dst)
            if not thumb_path:
                thumb_path = cover_path

        ai_result = {}
        if auto_tag and not (description and tags) and cover_path:
            ai_result = _ai_analyze(cover_path)
    else:
        ai_result = {}
        if auto_tag and not (description and tags):
            ai_result = _ai_analyze(filepath)

        try:
            img = Image.open(vault_path)
            width, height = img.size
            fmt = img.format or ext.lstrip(".")
        except Exception:
            pass

        thumb_dst = os.path.join(thumb_cat_dir, vault_name)
        thumb_path = create_thumbnail(vault_path, thumb_dst)

    taken_at = None if is_vid else extract_exif_date(filepath)
    file_size = os.path.getsize(vault_path)

    gps = None if is_vid else extract_gps_from_exif(filepath)
    lat, lng = (gps if gps else (None, None))

    if ai_result and lat is None and ai_result.get("lat") and ai_result.get("lng"):
        try:
            ai_lat = float(ai_result["lat"])
            ai_lng = float(ai_result["lng"])
            if -90 <= ai_lat <= 90 and -180 <= ai_lng <= 180 and not (ai_lat == 0 and ai_lng == 0):
                lat, lng = ai_lat, ai_lng
        except (TypeError, ValueError):
            pass
    if ai_result:
        final_category = category or ai_result.get("category_hint") or final_category
    final_desc = description or (ai_result.get("description", "") if ai_result else "")
    final_tags = tags or (ai_result.get("tags", []) if ai_result else [])

    kwargs = dict(
        filename=os.path.basename(filepath),
        original_path=filepath,
        vault_path=vault_path,
        thumb_path=thumb_path,
        file_hash=fhash,
        file_size=file_size,
        width=width,
        height=height,
        format=fmt,
        source=source,
        category=final_category,
        description=final_desc,
        tags=final_tags,
        taken_at=taken_at,
        media_type="video" if is_vid else "image",
    )
    if lat is not None and lng is not None:
        kwargs["latitude"] = lat
        kwargs["longitude"] = lng
    if ai_result and ai_result.get("location"):
        kwargs["location_name"] = ai_result["location"]
    if is_vid:
        kwargs["duration"] = duration
        kwargs["cover_path"] = cover_path

    image_id = add_image(conn, **kwargs)
    conn.close()

    result = {
        "id": image_id,
        "vault_path": vault_path,
        "thumb_path": thumb_path,
        "category": final_category,
        "source": source,
        "hash": fhash,
        "media_type": "video" if is_vid else "image",
    }
    if is_vid:
        result["duration"] = duration
        result["cover_path"] = cover_path
    if ai_result and "description" in ai_result:
        result["ai_tagged"] = True
    return result


def import_directory(dirpath: str, recursive: bool = True, **kwargs) -> dict:
    """Scan a directory and import all images."""
    results = {"imported": 0, "skipped": 0, "errors": 0, "details": []}
    dirpath = os.path.abspath(dirpath)

    pattern = Path(dirpath).rglob("*") if recursive else Path(dirpath).glob("*")
    for p in sorted(pattern):
        if p.suffix.lower() in SUPPORTED_EXTS and p.is_file():
            res = import_single(str(p), **kwargs)
            if res.get("error"):
                results["errors"] += 1
            elif res.get("skipped"):
                results["skipped"] += 1
            else:
                results["imported"] += 1
            results["details"].append(res)

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Import images into the vault")
    parser.add_argument("path", help="File or directory to import")
    parser.add_argument("--source", help="Source type: generated, uploaded, imported, screenshot")
    parser.add_argument("--category", help="Category name")
    parser.add_argument("--description", "-d", help="Image description")
    parser.add_argument("--tags", "-t", help="Comma-separated tags")
    parser.add_argument("--move", action="store_true", help="Move instead of copy")
    parser.add_argument("--recursive", "-r", action="store_true", default=True)
    parser.add_argument("--auto-tag", action="store_true", default=True, help="AI auto-recognize on import (default: on)")
    parser.add_argument("--no-auto-tag", action="store_true", help="Skip AI auto-recognition")
    args = parser.parse_args()

    init_db()
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
    do_auto_tag = not args.no_auto_tag

    if os.path.isdir(args.path):
        result = import_directory(
            args.path, recursive=args.recursive,
            source=args.source, category=args.category,
            description=args.description, tags=tags, copy=not args.move,
            auto_tag=do_auto_tag,
        )
        print(f"Imported: {result['imported']}, Skipped: {result['skipped']}, Errors: {result['errors']}")
    else:
        result = import_single(
            args.path, source=args.source, category=args.category,
            description=args.description, tags=tags, copy=not args.move,
            auto_tag=do_auto_tag,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
