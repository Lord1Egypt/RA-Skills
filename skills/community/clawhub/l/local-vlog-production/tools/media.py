"""Read-only inventory and contact sheets. Generation never marks review complete."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess

from workspace import (DEFAULT_ROOT, Workspace, configure_console, inside, is_link,
                       now, read_json, run_command, write_json_new, write_text_new)

IMAGES = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp", ".gif", ".heic", ".heif", ".avif", ".dng", ".cr2", ".cr3", ".nef", ".arw"}
VIDEOS = {".mp4", ".mov", ".m4v", ".mkv", ".avi", ".mts", ".m2ts", ".webm", ".insv", ".360"}
AUDIO_COMPANIONS = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".aiff", ".aif"}
REVIEW = {"images_viewed": False, "video_frames_viewed": False, "motion_watched": False, "audio_listened": False}


def classify(path):
    suffix = path.suffix.lower()
    return "images" if suffix in IMAGES else "videos" if suffix in VIDEOS else "companions"


def scan_theme(workspace, theme, folder, skipped, errors):
    """os.scandir without following any symlink or Windows reparse point."""
    try:
        with os.scandir(folder) as listing:
            entries = sorted(listing, key=lambda item: item.name.casefold())
    except OSError as exc:
        errors.append({"path": workspace.relative(folder), "operation": "list_directory", "error": str(exc)})
        return
    for entry in entries:
        path = Path(entry.path)
        try:
            if is_link(path):
                skipped.append({"path": path.relative_to(workspace.root).as_posix(), "reason": "symbolic_link_or_reparse_point"})
            elif entry.is_dir(follow_symlinks=False):
                yield from scan_theme(workspace, theme, path, skipped, errors)
            elif entry.is_file(follow_symlinks=False):
                yield inside(workspace.sources, path)
            else:
                skipped.append({"path": workspace.relative(path), "reason": "not_regular_file"})
        except (OSError, ValueError) as exc:
            errors.append({"path": path.relative_to(workspace.root).as_posix(), "operation": "inspect_entry", "error": str(exc)})


def fingerprint(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def probe(path, ffprobe):
    if not ffprobe:
        raise RuntimeError("ffprobe 未配置或未在 PATH 中找到")
    code, out, err = run_command([ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)], 90)
    if code:
        raise RuntimeError(f"ffprobe 退出码 {code}: {err[-2000:]}")
    data = json.loads(out)
    # The input path is already stored relative to the workspace.
    data.get("format", {}).pop("filename", None)
    return data


def image_metadata(path):
    from PIL import Image, ExifTags
    with Image.open(path) as image:
        exif = image.getexif()
        tags = {ExifTags.TAGS.get(key, str(key)): value for key, value in exif.items()}
        try:
            tags.update({ExifTags.TAGS.get(key, str(key)): value for key, value in exif.get_ifd(34665).items()})
        except (AttributeError, KeyError, TypeError):
            pass
        selected = {}
        for key in ("DateTime", "DateTimeOriginal", "DateTimeDigitized", "OffsetTime", "OffsetTimeOriginal", "OffsetTimeDigitized", "Make", "Model", "Orientation", "Software"):
            if key in tags:
                value = tags[key]
                selected[key] = value if isinstance(value, (str, int, float)) else str(value)
        return {"width": image.width, "height": image.height, "format": image.format, "mode": image.mode, "exif": selected, "pixel_decode": "not_tested_by_inventory"}


def time_candidates(path, metadata):
    candidates = []
    exif = metadata.get("image", {}).get("exif", {})
    for key, offset_key in (("DateTimeOriginal", "OffsetTimeOriginal"), ("DateTimeDigitized", "OffsetTimeDigitized"), ("DateTime", "OffsetTime")):
        if exif.get(key):
            raw = str(exif[key]).strip()
            normalized = None
            try:
                normalized = datetime.strptime(raw, "%Y:%m:%d %H:%M:%S").isoformat()
            except ValueError:
                pass
            candidates.append({"source": "EXIF." + key, "raw": raw, "iso_candidate": normalized, "timezone": exif.get(offset_key, "unknown"), "status": "unverified" if normalized else "invalid_or_unparsed"})
    ffprobe = metadata.get("ffprobe", {})
    containers = [("format", ffprobe.get("format", {}))] + [(f"stream[{i}]", stream) for i, stream in enumerate(ffprobe.get("streams", []))]
    for location, item in containers:
        for key, value in item.get("tags", {}).items():
            if key.lower() in ("creation_time", "date", "com.apple.quicktime.creationdate"):
                raw = str(value)
                parsed = None
                try:
                    parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
                except ValueError:
                    pass
                candidates.append({"source": f"ffprobe.{location}.{key}", "raw": raw, "iso_candidate": parsed.isoformat() if parsed else None, "timezone": str(parsed.tzinfo) if parsed and parsed.tzinfo else "unknown", "status": "unverified" if parsed else "invalid_or_unparsed"})
    for match in re.finditer(r"(?<!\d)(20\d{6})[_-](\d{6})(?!\d)", path.stem):
        raw = match.group(0)
        parsed = None
        try:
            parsed = datetime.strptime(match.group(1) + match.group(2), "%Y%m%d%H%M%S").isoformat()
        except ValueError:
            pass
        candidates.append({"source": "filename", "raw": raw, "iso_candidate": parsed, "timezone": "unknown", "status": "unverified" if parsed else "invalid_or_unparsed"})
    return {"status": "candidates_require_review" if candidates else "unknown", "selected_capture_time": None, "candidates": candidates, "filesystem_mtime_used": False, "note": "文件名、EXIF 和 creation_time 仅是候选；导出/转发可能改变时间，不自动校时或猜测时区。"}


def inventory(workspace, themes, output):
    selected = workspace.theme_paths(themes)
    target = workspace.output(output)
    ffprobe = workspace.tool("ffprobe")
    report = {"schema_version": 1, "generated_at": now(), "themes": [theme for theme, _ in selected], "asset_id_policy": "A + first_20_hex(SHA256(workspace_relative_posix_path_UTF8)); stable when moving the whole workspace; renamed paths receive a new ID", "assets": [], "skipped": [], "errors": [], "review": dict(REVIEW)}
    for theme, folder in selected:
        for path in scan_theme(workspace, theme, folder, report["skipped"], report["errors"]):
            relative = workspace.relative(path)
            asset = {"asset_id": "A" + hashlib.sha256(relative.encode("utf-8")).hexdigest()[:20], "path": relative, "theme": theme, "kind": classify(path), "metadata": {}, "errors": [], "review": dict(REVIEW)}
            try:
                before = path.stat()
                asset["size_bytes"] = before.st_size
                asset["sha256"] = fingerprint(path)
                after = path.stat()
                if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                    asset["errors"].append({"operation": "fingerprint", "error": "文件在读取期间变化；指纹需重新盘点"})
            except OSError as exc:
                asset["errors"].append({"operation": "fingerprint", "error": str(exc)})
            if asset["kind"] in ("images", "videos") or path.suffix.lower() in AUDIO_COMPANIONS | {".lrv"}:
                try:
                    asset["metadata"]["ffprobe"] = probe(path, ffprobe)
                except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
                    asset["errors"].append({"operation": "ffprobe", "error": str(exc)})
            if asset["kind"] == "images":
                try:
                    asset["metadata"]["image"] = image_metadata(path)
                except Exception as exc:
                    asset["errors"].append({"operation": "Pillow_metadata", "error": str(exc)})
            asset["capture_time"] = time_candidates(path, asset["metadata"])
            report["assets"].append(asset)
    # Same-stem companions are candidates only; this does not assert Live Photo identity.
    groups = {}
    for asset in report["assets"]:
        path = Path(asset["path"])
        groups.setdefault((path.parent.as_posix(), path.stem.casefold()), []).append(asset["asset_id"])
    for asset in report["assets"]:
        path = Path(asset["path"])
        asset["same_stem_candidates"] = [value for value in groups[(path.parent.as_posix(), path.stem.casefold())] if value != asset["asset_id"]]
    report["counts"] = {kind: sum(asset["kind"] == kind for asset in report["assets"]) for kind in ("images", "videos", "companions")}
    report["assets_with_errors"] = sum(bool(asset["errors"]) for asset in report["assets"])
    target.parent.mkdir(parents=True, exist_ok=True)
    write_json_new(target, report)
    return {"manifest": workspace.relative(target), "counts": report["counts"], "assets_with_errors": report["assets_with_errors"], "scan_errors": len(report["errors"]), "skipped_links_or_special_files": len(report["skipped"]), "review": dict(REVIEW)}


def positive_float(value):
    try:
        number = float(value)
        return number if math.isfinite(number) and number >= 0 else None
    except (TypeError, ValueError):
        return None


def thumb_image(source, target):
    from PIL import Image, ImageOps
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original).convert("RGB")
        image.thumbnail((640, 480), Image.Resampling.LANCZOS)
        with target.open("xb") as output:
            image.save(output, "JPEG", quality=88)


def extract_frame(workspace, ffmpeg, source, folder, index, seek):
    target = folder / f"frame_{index:03d}.jpg"
    logfile = folder / f"frame_{index:03d}.log"
    command = [ffmpeg, "-hide_banner", "-nostdin", "-loglevel", "info", "-ss", f"{seek:.6f}", "-copyts", "-i", str(source), "-map", "0:v:0", "-an", "-sn", "-frames:v", "1", "-vf", "showinfo,scale=640:-2", "-q:v", "3", "-n", str(target)]
    frame = {"requested_seek_seconds": seek, "decoded_pts_seconds": None, "pts_basis": "unavailable", "ffmpeg_command": command, "log": workspace.relative(logfile), "reviewed": False}
    try:
        code, _, err = run_command(command, 120)
        write_text_new(logfile, err)
        frame["returncode"] = code
        if code or not target.is_file():
            frame["error"] = "ffmpeg 未成功生成图片；详见日志"
        else:
            # showinfo reports timestamps of actual decoded frames with -copyts.
            matches = re.findall(r"\bn:\s*0\s+pts:\s*-?\d+\s+pts_time:\s*([-+0-9.eE]+)", err)
            if matches:
                value = float(matches[0])
                if math.isfinite(value):
                    frame["decoded_pts_seconds"] = value
                    frame["pts_basis"] = "decoded_source_stream_pts_with_copyts"
            frame["image"] = workspace.relative(target)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        if not logfile.exists():
            write_text_new(logfile, str(exc))
        frame["error"] = str(exc)
    return frame


def contact_sheets(workspace, target, thumbnails):
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    pages = []
    font = ImageFont.load_default()
    cell_w, cell_h, columns, page_size = 320, 280, 4, 16
    for offset in range(0, len(thumbnails), page_size):
        group = thumbnails[offset:offset + page_size]
        rows = math.ceil(len(group) / columns)
        canvas = Image.new("RGB", (cell_w * columns, cell_h * rows), "#eeeeee")
        draw = ImageDraw.Draw(canvas)
        for index, entry in enumerate(group):
            x, y = (index % columns) * cell_w, (index // columns) * cell_h
            with Image.open(inside(workspace.root, entry["image"])) as thumbnail:
                fit = ImageOps.contain(thumbnail.convert("RGB"), (308, 220))
                canvas.paste(fit, (x + (cell_w - fit.width) // 2, y + (226 - fit.height) // 2))
            draw.text((x + 6, y + 230), entry["asset_id"], fill="black", font=font)
            draw.text((x + 6, y + 248), entry["caption"], fill="black", font=font)
        path = target / f"contact_{offset // page_size + 1:03d}.jpg"
        with path.open("xb") as output:
            canvas.save(output, "JPEG", quality=90)
        pages.append(workspace.relative(path))
    return pages


def contacts(workspace, manifest, output, samples):
    if not 1 <= samples <= 30:
        raise ValueError("--samples 必须在 1 到 30 之间")
    from PIL import Image  # Check dependency before creating outputs.
    data = read_json(inside(workspace.root, manifest))
    selected = {theme for theme, _ in workspace.theme_paths(data["themes"])}
    target = workspace.output(output)
    assets = []
    seen = set()
    for asset in data["assets"]:
        if asset["kind"] not in ("images", "videos"):
            continue
        source = inside(workspace.sources, workspace.root / asset["path"])
        if not source.is_file() or source.relative_to(workspace.sources).parts[0] not in selected:
            raise ValueError("清单包含不存在的素材或所选主题之外的路径")
        if not re.fullmatch(r"A[0-9a-f]{20}", asset["asset_id"]) or asset["asset_id"] in seen:
            raise ValueError("清单 asset_id 无效或重复")
        seen.add(asset["asset_id"])
        assets.append((asset, source))
    ffmpeg = workspace.tool("ffmpeg")
    if any(asset["kind"] == "videos" for asset, _ in assets) and not ffmpeg:
        raise ValueError("视频抽帧需要 ffmpeg；先运行 doctor")
    target.mkdir(parents=True, exist_ok=False)
    result = {"schema_version": 1, "generated_at": now(), "source_manifest": workspace.relative(inside(workspace.root, manifest)), "samples_per_video_requested": samples, "assets": [], "review": dict(REVIEW), "status": "generated_not_reviewed", "color_note": "概览缩略图未做 HDR tone mapping 或逐镜调色；HDR 素材的显示颜色/亮度可能与正确色彩管理播放不同，不据此确认调色。", "timing_note": "requested_seek_seconds 是输入寻址请求。decoded_pts_seconds 仅在 showinfo 实际返回 PTS 时填写，是原流时间戳而非必然从零开始；没有 PTS 时不以请求值代替精确时间。抽帧不等于连续观看。"}
    thumbnails = []
    for asset, source in assets:
        item = {"asset_id": asset["asset_id"], "source": asset["path"], "kind": asset["kind"], "frames": [], "errors": [], "review": dict(REVIEW)}
        folder = target / asset["asset_id"]
        folder.mkdir()
        try:
            if asset.get("sha256") and fingerprint(source) != asset["sha256"]:
                raise ValueError("素材指纹已变化，请重新盘点后生成联系表")
            if asset["kind"] == "images":
                path = folder / "thumbnail.jpg"
                thumb_image(source, path)
                frame = {"image": workspace.relative(path), "reviewed": False}
                item["frames"].append(frame)
                thumbnails.append({"image": frame["image"], "asset_id": asset["asset_id"], "caption": "PHOTO | not reviewed"})
            else:
                probe_data = asset.get("metadata", {}).get("ffprobe", {})
                streams = [stream for stream in probe_data.get("streams", []) if stream.get("codec_type") == "video"]
                duration = positive_float(probe_data.get("format", {}).get("duration"))
                if duration is None and streams:
                    duration = positive_float(streams[0].get("duration"))
                item["duration_seconds"] = duration
                item["stream_start_time"] = streams[0].get("start_time") if streams else None
                if duration is None or duration == 0:
                    seeks = [0.0]
                    item["errors"].append("时长未知，仅请求片头一帧；不能据此宣称覆盖全片")
                else:
                    # Leave a small tail margin to avoid EOF, retaining separate actual PTS.
                    end = max(0.0, duration - min(0.2, duration / 10))
                    seeks = [end * index / (samples - 1) for index in range(samples)] if samples > 1 else [end / 2]
                for index, seek in enumerate(seeks):
                    frame = extract_frame(workspace, ffmpeg, source, folder, index, seek)
                    item["frames"].append(frame)
                    if frame.get("image"):
                        pts = frame["decoded_pts_seconds"]
                        caption = f"seek={seek:.2f}s | PTS={pts:.3f}s" if pts is not None else f"seek={seek:.2f}s | PTS unknown"
                        thumbnails.append({"image": frame["image"], "asset_id": asset["asset_id"], "caption": caption})
        except Exception as exc:
            item["errors"].append(str(exc))
        result["assets"].append(item)
    result["contact_sheets"] = contact_sheets(workspace, target, thumbnails)
    result["error_count"] = sum(len(item["errors"]) + sum(bool(frame.get("error")) for frame in item["frames"]) for item in result["assets"])
    write_json_new(target / "contacts.json", result)
    return {"report": workspace.relative(target / "contacts.json"), "contact_sheets": result["contact_sheets"], "generated_images": len(thumbnails), "error_count": result["error_count"], "review": dict(REVIEW)}


def main():
    configure_console()
    parser = argparse.ArgumentParser(description="只读素材盘点与抽帧联系表；不自动标记审阅")
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    commands = parser.add_subparsers(dest="command", required=True)
    inventory_parser = commands.add_parser("inventory")
    inventory_parser.add_argument("--themes", nargs="+", required=True)
    inventory_parser.add_argument("--out", required=True, help="新 JSON 清单；工作区内且不在素材目录")
    contacts_parser = commands.add_parser("contacts")
    contacts_parser.add_argument("--manifest", required=True)
    contacts_parser.add_argument("--out", required=True, help="新的输出目录，不覆盖旧版")
    contacts_parser.add_argument("--samples", type=int, default=5, help="每段视频的均匀抽样数量，1 到 30")
    args = parser.parse_args()
    try:
        workspace = Workspace(args.root)
        result = inventory(workspace, args.themes, args.out) if args.command == "inventory" else contacts(workspace, args.manifest, args.out, args.samples)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.command == "inventory":
            return 2 if result["assets_with_errors"] or result["scan_errors"] else 0
        return 2 if result["error_count"] else 0
    except (OSError, ValueError, KeyError, ImportError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"错误：{exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
