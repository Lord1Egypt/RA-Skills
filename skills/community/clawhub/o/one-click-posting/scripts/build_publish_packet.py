#!/usr/bin/env python3
import argparse
import json
import struct
from datetime import datetime
from pathlib import Path

ALLOWED_PLATFORMS = ("xiaohongshu", "x", "zhihu")
PLATFORM_PRIORITY = ("xiaohongshu", "x", "zhihu")
ALLOWED_COVER_MODES = ("auto", "upload", "xhs_text")

XHS_MIN_WIDTH = 720
XHS_MIN_HEIGHT = 960
XHS_TARGET_RATIO = 3 / 4
XHS_RATIO_TOLERANCE = 0.08


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build one-click publishing packet")
    parser.add_argument("--title", required=True, help="Post title")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--body", help="Post body text")
    group.add_argument("--body-file", help="Path to body text file")
    parser.add_argument("--platform", action="append", required=True, help="Target platform, repeatable")
    parser.add_argument("--cover", help="Cover image path")
    parser.add_argument(
        "--cover-mode",
        default="auto",
        choices=ALLOWED_COVER_MODES,
        help="Cover mode for Xiaohongshu: auto(default)/upload/xhs_text",
    )
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--source", default="", help="Comma-separated source labels")
    parser.add_argument("--audience", default="", help="Target audience")
    parser.add_argument("--core-viewpoint", default="", help="One-line core viewpoint")
    parser.add_argument("--first-comment", default="", help="First comment draft")
    parser.add_argument("--verify-status", default="已核验", choices=["已核验", "待核实"], help="Fact verification status")
    parser.add_argument("--schedule-at", default="", help="Schedule time text")
    parser.add_argument("--output", default="", help="Optional output file path")
    return parser.parse_args()


def read_body(args: argparse.Namespace) -> str:
    if args.body:
        return args.body.strip()

    path = Path(args.body_file).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Body file not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def validate_cover(path_text: str) -> str:
    if not path_text:
        return ""

    path = Path(path_text).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Cover file not found: {path}")
    return str(path)


def normalize_list(text: str):
    result = []
    seen = set()
    for raw in text.split(","):
        item = raw.strip()
        if not item:
            continue
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def normalize_platforms(platform_args):
    raw_items = []
    for item in platform_args:
        if not item:
            continue
        raw_items.extend(normalize_list(item))

    platforms = []
    seen = set()
    for item in raw_items:
        lowered = item.strip().lower()
        if not lowered:
            continue
        if lowered not in ALLOWED_PLATFORMS:
            allowed = ", ".join(ALLOWED_PLATFORMS)
            raise ValueError(f"Unsupported platform: {lowered}. Allowed: {allowed}")
        if lowered in seen:
            continue
        seen.add(lowered)
        platforms.append(lowered)

    if not platforms:
        raise ValueError("At least one valid platform is required")

    return platforms


def resolve_cover_mode(platforms: list, cover_path: str, requested_mode: str) -> str:
    is_xhs = "xiaohongshu" in platforms

    if not is_xhs:
        return "upload"

    if requested_mode == "auto":
        return "xhs_text" if not cover_path else "upload"

    if requested_mode == "xhs_text":
        return "xhs_text"

    return "upload"


def get_png_size(path: Path):
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24:
        return None
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def get_jpeg_size(path: Path):
    with path.open("rb") as handle:
        if handle.read(2) != b"\xff\xd8":
            return None

        while True:
            marker_start = handle.read(1)
            if not marker_start:
                return None
            if marker_start != b"\xff":
                continue

            marker = handle.read(1)
            while marker == b"\xff":
                marker = handle.read(1)

            if not marker:
                return None

            marker_code = marker[0]
            if marker_code in (0xD8, 0xD9):
                continue

            length_bytes = handle.read(2)
            if len(length_bytes) != 2:
                return None
            length = struct.unpack(">H", length_bytes)[0]
            if length < 2:
                return None

            if marker_code in {
                0xC0,
                0xC1,
                0xC2,
                0xC3,
                0xC5,
                0xC6,
                0xC7,
                0xC9,
                0xCA,
                0xCB,
                0xCD,
                0xCE,
                0xCF,
            }:
                segment = handle.read(length - 2)
                if len(segment) < 5:
                    return None
                height = struct.unpack(">H", segment[1:3])[0]
                width = struct.unpack(">H", segment[3:5])[0]
                return width, height

            handle.seek(length - 2, 1)


def get_webp_size(path: Path):
    with path.open("rb") as handle:
        header = handle.read(12)
        if len(header) < 12:
            return None
        if header[:4] != b"RIFF" or header[8:12] != b"WEBP":
            return None

        while True:
            chunk_header = handle.read(8)
            if len(chunk_header) < 8:
                return None

            chunk_type = chunk_header[:4]
            chunk_size = struct.unpack("<I", chunk_header[4:])[0]
            chunk_data = handle.read(chunk_size)
            if len(chunk_data) < chunk_size:
                return None

            if chunk_type == b"VP8X" and len(chunk_data) >= 10:
                width = int.from_bytes(chunk_data[4:7], "little") + 1
                height = int.from_bytes(chunk_data[7:10], "little") + 1
                return width, height

            if chunk_type == b"VP8L" and len(chunk_data) >= 5 and chunk_data[0] == 0x2F:
                bits = int.from_bytes(chunk_data[1:5], "little")
                width = (bits & 0x3FFF) + 1
                height = ((bits >> 14) & 0x3FFF) + 1
                return width, height

            if chunk_type == b"VP8 " and len(chunk_data) >= 10 and chunk_data[3:6] == b"\x9d\x01\x2a":
                width = struct.unpack("<H", chunk_data[6:8])[0] & 0x3FFF
                height = struct.unpack("<H", chunk_data[8:10])[0] & 0x3FFF
                return width, height

            if chunk_size % 2 == 1:
                handle.seek(1, 1)


def get_image_size(path_text: str):
    if not path_text:
        return None

    path = Path(path_text)
    suffix = path.suffix.lower()

    if suffix == ".png":
        return get_png_size(path)
    if suffix in (".jpg", ".jpeg"):
        return get_jpeg_size(path)
    if suffix == ".webp":
        return get_webp_size(path)

    return None


def build_cover_meta(cover_path: str):
    if not cover_path:
        return {
            "path": "",
            "readable": False,
            "width": None,
            "height": None,
            "ratio": None,
        }

    size = get_image_size(cover_path)
    if not size:
        return {
            "path": cover_path,
            "readable": False,
            "width": None,
            "height": None,
            "ratio": None,
        }

    width, height = size
    ratio = width / height if height else None

    return {
        "path": cover_path,
        "readable": True,
        "width": width,
        "height": height,
        "ratio": ratio,
    }


def build_quality_checks(
    title: str,
    body: str,
    audience: str,
    core_viewpoint: str,
    sources: list,
    platforms: list,
    cover_mode: str,
    cover_meta: dict,
    verify_status: str,
):
    is_xhs = "xiaohongshu" in platforms
    need_upload_cover = is_xhs and cover_mode == "upload"

    has_cover = bool(cover_meta.get("path"))
    cover_readable = bool(cover_meta.get("readable"))
    width = cover_meta.get("width") or 0
    height = cover_meta.get("height") or 0
    ratio = cover_meta.get("ratio")

    cover_ratio_ok = False
    if ratio is not None:
        cover_ratio_ok = abs(ratio - XHS_TARGET_RATIO) <= XHS_RATIO_TOLERANCE

    cover_size_ok = width >= XHS_MIN_WIDTH and height >= XHS_MIN_HEIGHT

    checks = {
        "has_title": bool(title),
        "title_len_le_20_for_xhs": (not is_xhs) or (len(title) <= 20),
        "has_body": bool(body),
        "body_len_ge_80": len(body) >= 80,
        "has_audience": bool(audience),
        "has_core_viewpoint": bool(core_viewpoint),
        "source_traceable": bool(sources),
        "verify_status_declared": verify_status in ("已核验", "待核实"),
        "cover_mode_valid_for_xiaohongshu": (not is_xhs) or (cover_mode in ("upload", "xhs_text")),
        "has_cover_for_xiaohongshu": (not is_xhs) or (cover_mode == "xhs_text") or has_cover,
        "cover_readable_for_xiaohongshu": (not need_upload_cover) or (not has_cover) or cover_readable,
        "cover_ratio_3_4_for_xiaohongshu": (not need_upload_cover) or (not has_cover) or ((not cover_readable) or cover_ratio_ok),
        "cover_size_min_for_xiaohongshu": (not need_upload_cover) or (not has_cover) or ((not cover_readable) or cover_size_ok),
    }

    warnings = []
    if is_xhs and len(title) > 20:
        warnings.append("小红书标题建议 <=20 字")
    if len(body) < 80:
        warnings.append("正文偏短，建议补充可执行细节")
    if not sources:
        warnings.append("缺少来源字段，需补充可追溯来源")
    if verify_status == "待核实":
        warnings.append("含待核实信息，发布前务必人工复核")

    if is_xhs and cover_mode == "xhs_text":
        warnings.append("小红书采用文字配图模式：发布前需截图封面预览并经老板确认")

    if need_upload_cover and not has_cover:
        warnings.append("小红书上传封面模式下需要提供封面图")
    if need_upload_cover and has_cover and not cover_readable:
        warnings.append("封面尺寸读取失败，仅支持 png/jpg/jpeg/webp")
    if need_upload_cover and has_cover and cover_readable and not cover_ratio_ok:
        warnings.append("小红书封面建议接近 3:4 比例")
    if need_upload_cover and has_cover and cover_readable and not cover_size_ok:
        warnings.append(f"小红书封面建议不小于 {XHS_MIN_WIDTH}x{XHS_MIN_HEIGHT}")

    return checks, warnings


def build_recommended_order(platforms: list):
    ordered = [platform for platform in PLATFORM_PRIORITY if platform in platforms]
    remainder = [platform for platform in platforms if platform not in ordered]
    return ordered + remainder


def build_packet(args: argparse.Namespace) -> dict:
    body = read_body(args)
    cover = validate_cover(args.cover)
    now = datetime.now()
    packet_id = f"post-{now.strftime('%Y%m%d-%H%M%S')}"

    title = args.title.strip()
    audience = args.audience.strip()
    core_viewpoint = args.core_viewpoint.strip()
    first_comment = args.first_comment.strip()

    platforms = normalize_platforms(args.platform)
    cover_mode = resolve_cover_mode(platforms=platforms, cover_path=cover, requested_mode=args.cover_mode)

    tags = normalize_list(args.tags)
    sources = normalize_list(args.source)

    cover_meta = build_cover_meta(cover)

    checks, warnings = build_quality_checks(
        title=title,
        body=body,
        audience=audience,
        core_viewpoint=core_viewpoint,
        sources=sources,
        platforms=platforms,
        cover_mode=cover_mode,
        cover_meta=cover_meta,
        verify_status=args.verify_status,
    )

    return {
        "schema_version": "1.3.0",
        "packet_id": packet_id,
        "created_at": now.isoformat(timespec="seconds"),
        "content": {
            "title": title,
            "body": body,
            "tags": tags,
            "cover": cover,
            "cover_mode": cover_mode,
            "cover_meta": cover_meta,
            "first_comment": first_comment,
            "audience": audience,
            "core_viewpoint": core_viewpoint,
            "verify_status": args.verify_status,
            "sources": sources,
        },
        "publish": {
            "platforms": platforms,
            "recommended_order": build_recommended_order(platforms),
            "schedule_at": args.schedule_at.strip(),
            "status": "draft",
        },
        "preflight": {
            "deai_checked": False,
            "risk_reviewed": False,
            "approval_required": True,
            "source_traceable": checks["source_traceable"],
            "quality_checks": checks,
            "warnings": warnings,
            "last_checked_at": "",
        },
        "approval": {
            "granted": False,
            "approver": "",
            "approved_at": "",
        },
        "execution": {
            "results": [],
            "screenshots": [],
            "notes": [],
        },
        "metrics": {
            "first_hour": {
                "exposure": None,
                "likes": None,
                "comments": None,
                "favorites": None,
                "shares": None,
            }
        },
    }


def resolve_output(args: argparse.Namespace, packet: dict) -> Path:
    if args.output:
        return Path(args.output).expanduser().resolve()

    date_part = datetime.now().strftime("%Y-%m-%d")
    workspace_root = Path(__file__).resolve().parents[3]
    root = workspace_root / "knowledge/daily" / date_part / "publish-packets"
    root.mkdir(parents=True, exist_ok=True)
    return root / f"{packet['packet_id']}.json"


def main() -> None:
    args = parse_args()
    packet = build_packet(args)
    output = resolve_output(args, packet)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(output))


if __name__ == "__main__":
    main()
