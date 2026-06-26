#!/usr/bin/env python3
"""
PPT Compressor — 解包 PPTX，压缩内嵌图片与视频后重新打包。
支持 low / medium / high / extreme 四档压缩预设，也可自定义参数。
视频压缩依赖 ffmpeg；图片压缩依赖 Pillow。
"""

import argparse
import io
import os
import re
import subprocess
import sys
import shutil
import tempfile
import zipfile
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("错误: 缺少 Pillow 库，请先运行  pip install Pillow", file=sys.stderr)
    sys.exit(1)

LEVEL_PRESETS = {
    "low":     {"quality": 85, "max_dim": 2560, "strip_thumbnail": False, "convert_png": False,
                "video_crf": 23, "video_scale": None, "video_preset": "medium"},
    "medium":  {"quality": 70, "max_dim": 1920, "strip_thumbnail": True,  "convert_png": True,
                "video_crf": 28, "video_scale": 1080, "video_preset": "medium"},
    "high":    {"quality": 50, "max_dim": 1440, "strip_thumbnail": True,  "convert_png": True,
                "video_crf": 32, "video_scale": 720, "video_preset": "slow"},
    "extreme": {"quality": 30, "max_dim": 1024, "strip_thumbnail": True,  "convert_png": True,
                "video_crf": 38, "video_scale": 480, "video_preset": "slow"},
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".gif", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".wmv", ".m4v", ".webm", ".mkv"}
MEDIA_PREFIX = "ppt/media/"
THUMBNAIL_PATH = "docProps/thumbnail.jpeg"
COMMENT_PREFIX = "ppt/comments/"


def find_ffmpeg():
    """检测 ffmpeg 是否可用，返回路径或 None。"""
    path = shutil.which("ffmpeg")
    if path:
        return path
    common_paths = [
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"C:\tools\ffmpeg\bin\ffmpeg.exe",
        "/usr/local/bin/ffmpeg",
        "/usr/bin/ffmpeg",
    ]
    for p in common_paths:
        if os.path.isfile(p):
            return p
    return None


def print_ffmpeg_install_guide():
    print("\n" + "=" * 60, file=sys.stderr)
    print("  ffmpeg 未找到 — 视频将保留原始数据（不压缩）", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print("\n安装方法:", file=sys.stderr)
    if sys.platform == "win32":
        print("  方法 1 (winget):  winget install Gyan.FFmpeg", file=sys.stderr)
        print("  方法 2 (scoop):   scoop install ffmpeg", file=sys.stderr)
        print("  方法 3 (choco):   choco install ffmpeg", file=sys.stderr)
        print("  方法 4 (手动):    https://www.gyan.dev/ffmpeg/builds/", file=sys.stderr)
        print("                    下载后将 bin 目录加入系统 PATH", file=sys.stderr)
    elif sys.platform == "darwin":
        print("  brew install ffmpeg", file=sys.stderr)
    else:
        print("  sudo apt install ffmpeg   # Debian/Ubuntu", file=sys.stderr)
        print("  sudo dnf install ffmpeg   # Fedora", file=sys.stderr)
        print("  sudo pacman -S ffmpeg     # Arch", file=sys.stderr)
    print(file=sys.stderr)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="压缩 PPTX 文件体积（图片 + 视频）")
    parser.add_argument("input", help="输入 PPTX 文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径（默认在原文件名后加 _compressed）")
    parser.add_argument("-l", "--level", choices=LEVEL_PRESETS.keys(), default="medium",
                        help="压缩档次 (default: medium)")
    # 图片参数
    parser.add_argument("--image-quality", type=int, help="JPEG 质量 1-100，覆盖 level 默认")
    parser.add_argument("--max-width", type=int, help="图片最大宽度像素")
    parser.add_argument("--max-height", type=int, help="图片最大高度像素")
    parser.add_argument("--strip-thumbnail", action="store_true", default=None,
                        help="移除文档缩略图")
    parser.add_argument("--strip-comments", action="store_true", default=False,
                        help="移除幻灯片批注")
    parser.add_argument("--convert-png", action="store_true", default=None,
                        help="将不含透明通道的 PNG 转为 JPEG")
    parser.add_argument("--no-convert-png", action="store_true", default=False,
                        help="禁止 PNG 转 JPEG")
    # 视频参数
    parser.add_argument("--video-crf", type=int, help="视频 CRF 值 (0-51，越高压缩率越大)，覆盖 level 默认")
    parser.add_argument("--video-scale", type=int, help="视频最大短边像素（如 720、1080），超出则缩小")
    parser.add_argument("--video-preset", choices=["ultrafast", "superfast", "veryfast", "faster",
                                                     "fast", "medium", "slow", "slower", "veryslow"],
                        help="ffmpeg x264 编码预设")
    parser.add_argument("--no-video", action="store_true", default=False,
                        help="跳过视频压缩，保留原始视频数据")
    return parser.parse_args(argv)


def resolve_options(args):
    preset = LEVEL_PRESETS[args.level]
    quality = args.image_quality if args.image_quality is not None else preset["quality"]
    quality = max(1, min(100, quality))

    max_w = args.max_width if args.max_width else preset["max_dim"]
    max_h = args.max_height if args.max_height else preset["max_dim"]

    strip_thumbnail = args.strip_thumbnail if args.strip_thumbnail is not None else preset["strip_thumbnail"]
    if args.no_convert_png:
        convert_png = False
    elif args.convert_png is not None and args.convert_png:
        convert_png = True
    else:
        convert_png = preset["convert_png"]

    video_crf = args.video_crf if args.video_crf is not None else preset["video_crf"]
    video_crf = max(0, min(51, video_crf))
    video_scale = args.video_scale if args.video_scale else preset["video_scale"]
    video_preset = args.video_preset if args.video_preset else preset["video_preset"]

    return {
        "quality": quality,
        "max_width": max_w,
        "max_height": max_h,
        "strip_thumbnail": strip_thumbnail,
        "strip_comments": args.strip_comments,
        "convert_png": convert_png,
        "no_video": args.no_video,
        "video_crf": video_crf,
        "video_scale": video_scale,
        "video_preset": video_preset,
    }


def has_transparency(img):
    if img.mode == "RGBA":
        alpha = img.getchannel("A")
        extrema = alpha.getextrema()
        if extrema[0] < 255:
            return True
    elif img.mode == "PA" or (img.mode == "P" and "transparency" in img.info):
        return True
    return False


def compress_image(data, name, opts):
    """压缩单张图片，返回 (new_bytes, new_name, was_converted_to_jpg)。"""
    ext = Path(name).suffix.lower()
    if ext not in IMAGE_EXTENSIONS:
        return data, name, False

    try:
        img = Image.open(io.BytesIO(data))
    except Exception:
        return data, name, False

    orig_size = len(data)
    converted_to_jpg = False

    w, h = img.size
    scale = min(opts["max_width"] / w, opts["max_height"] / h, 1.0)
    if scale < 1.0:
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        img = img.resize((new_w, new_h), Image.LANCZOS)

    buf = io.BytesIO()

    if ext == ".png" and opts["convert_png"] and not has_transparency(img):
        img = img.convert("RGB")
        img.save(buf, format="JPEG", quality=opts["quality"], optimize=True)
        converted_to_jpg = True
    elif ext in (".jpg", ".jpeg"):
        if img.mode in ("RGBA", "P", "PA"):
            img = img.convert("RGB")
        img.save(buf, format="JPEG", quality=opts["quality"], optimize=True)
    elif ext == ".png":
        img.save(buf, format="PNG", optimize=True)
    elif ext == ".bmp":
        img = img.convert("RGB")
        img.save(buf, format="JPEG", quality=opts["quality"], optimize=True)
        converted_to_jpg = True
    elif ext in (".tiff", ".tif"):
        if img.mode in ("RGBA", "P", "PA"):
            img = img.convert("RGB")
        img.save(buf, format="JPEG", quality=opts["quality"], optimize=True)
        converted_to_jpg = True
    elif ext == ".gif":
        buf = io.BytesIO(data)
    elif ext == ".webp":
        img.save(buf, format="WEBP", quality=opts["quality"])
    else:
        return data, name, False

    result = buf.getvalue()
    if len(result) >= orig_size and not converted_to_jpg:
        return data, name, False
    return result, name, converted_to_jpg


def compress_video(data, name, opts, ffmpeg_path, tmp_dir):
    """用 ffmpeg 压缩视频，返回 (new_bytes, new_name)。失败时返回原始数据。"""
    ext = Path(name).suffix.lower()
    orig_size = len(data)

    in_file = os.path.join(tmp_dir, f"in_video{ext}")
    out_file = os.path.join(tmp_dir, "out_video.mp4")

    with open(in_file, "wb") as f:
        f.write(data)

    cmd = [
        ffmpeg_path, "-y", "-i", in_file,
        "-c:v", "libx264",
        "-crf", str(opts["video_crf"]),
        "-preset", opts["video_preset"],
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
    ]

    if opts["video_scale"]:
        max_h = opts["video_scale"]
        max_w = max_h * 16 // 9
        # ffmpeg filter 中逗号须转义为 \, 以避免被当作过滤器分隔符
        vf = f"scale=min(iw\\,{max_w}):min(ih\\,{max_h}):force_original_aspect_ratio=decrease:force_divisible_by=2"
        cmd += ["-vf", vf]

    cmd.append(out_file)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"  [视频压缩失败] {Path(name).name}: ffmpeg 返回 {result.returncode}", file=sys.stderr)
            if result.stderr:
                for line in result.stderr.strip().split("\n")[-3:]:
                    print(f"    {line}", file=sys.stderr)
            return data, name

        new_data = open(out_file, "rb").read()
        new_size = len(new_data)

        if new_size >= orig_size:
            return data, name

        new_name = str(Path(name).with_suffix(".mp4")) if ext != ".mp4" else name
        return new_data, new_name

    except subprocess.TimeoutExpired:
        print(f"  [视频压缩超时] {Path(name).name}: 超过 300 秒", file=sys.stderr)
        return data, name
    except Exception as e:
        print(f"  [视频压缩异常] {Path(name).name}: {e}", file=sys.stderr)
        return data, name
    finally:
        for f in (in_file, out_file):
            try:
                os.remove(f)
            except OSError:
                pass


def update_content_types(ct_xml, renames):
    if not renames:
        return ct_xml
    for old_name, new_name in renames.items():
        old_part = "/" + old_name
        new_part = "/" + new_name
        ct_xml = ct_xml.replace(old_part, new_part)

        old_ext = Path(old_name).suffix.lower()
        new_ext = Path(new_name).suffix.lower()
        if old_ext != new_ext:
            ext_to_mime = {
                ".jpeg": "image/jpeg", ".jpg": "image/jpeg",
                ".png": "image/png", ".gif": "image/gif",
                ".mp4": "video/mp4", ".avi": "video/x-msvideo",
                ".mov": "video/quicktime", ".wmv": "video/x-ms-wmv",
                ".webm": "video/webm",
            }
            old_mime = ext_to_mime.get(old_ext, "")
            new_mime = ext_to_mime.get(new_ext, "")
            if old_mime and new_mime and old_part.replace(old_ext, new_ext) == new_part:
                pass  # already handled by path replacement
    return ct_xml


def update_rels_and_slides(xml_content, renames):
    for old_name, new_name in renames.items():
        old_basename = os.path.basename(old_name)
        new_basename = os.path.basename(new_name)
        xml_content = xml_content.replace(old_basename, new_basename)
    return xml_content


def compress_pptx(input_path, output_path, opts):
    input_path = os.path.abspath(input_path)
    if not os.path.isfile(input_path):
        print(f"错误: 文件不存在 — {input_path}", file=sys.stderr)
        return False

    ffmpeg_path = None
    has_video_in_pptx = False
    if not opts["no_video"]:
        ffmpeg_path = find_ffmpeg()

    orig_file_size = os.path.getsize(input_path)
    print(f"输入: {input_path}")
    print(f"原始大小: {format_size(orig_file_size)}")
    print(f"压缩参数: quality={opts['quality']}, max={opts['max_width']}x{opts['max_height']}, "
          f"convert_png={opts['convert_png']}, strip_thumbnail={opts['strip_thumbnail']}")
    if not opts["no_video"]:
        print(f"视频参数: crf={opts['video_crf']}, scale={opts['video_scale'] or 'auto'}, "
              f"preset={opts['video_preset']}, ffmpeg={'已就绪' if ffmpeg_path else '未找到'}")
    else:
        print("视频参数: 已跳过（--no-video）")
    print()

    renames = {}
    entries = {}
    images_processed = 0
    images_saved = 0
    videos_processed = 0
    videos_saved = 0

    tmp_dir = tempfile.mkdtemp(prefix="pptc_")

    try:
        with zipfile.ZipFile(input_path, "r") as zin:
            for info in zin.infolist():
                name = info.filename
                if name.endswith("/"):
                    continue

                data = zin.read(name)

                if opts["strip_thumbnail"] and name.lower() == THUMBNAIL_PATH.lower():
                    print(f"  [移除] {name} ({format_size(len(data))})")
                    continue

                if opts["strip_comments"] and name.lower().startswith(COMMENT_PREFIX.lower()):
                    print(f"  [移除批注] {name}")
                    continue

                if name.startswith(MEDIA_PREFIX):
                    ext = Path(name).suffix.lower()

                    if ext in IMAGE_EXTENSIONS:
                        images_processed += 1
                        old_size = len(data)
                        new_data, _, was_converted = compress_image(data, name, opts)
                        new_size = len(new_data)

                        if was_converted:
                            new_name = str(Path(name).with_suffix(".jpeg"))
                            renames[name] = new_name
                            name = new_name

                        saved = old_size - new_size
                        pct = (saved / old_size * 100) if old_size > 0 else 0
                        tag = "PNG→JPG " if was_converted else ""
                        if saved > 0:
                            images_saved += 1
                            print(f"  [压缩] {tag}{Path(name).name}: "
                                  f"{format_size(old_size)} → {format_size(new_size)} "
                                  f"(节省 {format_size(saved)}, {pct:.1f}%)")
                        else:
                            print(f"  [保留] {Path(name).name}: {format_size(old_size)} (已最优)")

                        data = new_data

                    elif ext in VIDEO_EXTENSIONS:
                        has_video_in_pptx = True
                        videos_processed += 1
                        old_size = len(data)

                        if opts["no_video"]:
                            print(f"  [跳过视频] {Path(name).name}: {format_size(old_size)}")
                        elif not ffmpeg_path:
                            print(f"  [跳过视频] {Path(name).name}: {format_size(old_size)} (ffmpeg 不可用)")
                        else:
                            new_data, new_name = compress_video(data, name, opts, ffmpeg_path, tmp_dir)
                            new_size = len(new_data)

                            if new_name != name:
                                renames[name] = new_name
                                name = new_name

                            saved = old_size - new_size
                            pct = (saved / old_size * 100) if old_size > 0 else 0
                            if saved > 0:
                                videos_saved += 1
                                print(f"  [视频压缩] {Path(name).name}: "
                                      f"{format_size(old_size)} → {format_size(new_size)} "
                                      f"(节省 {format_size(saved)}, {pct:.1f}%)")
                            else:
                                print(f"  [保留视频] {Path(name).name}: {format_size(old_size)} (已最优)")

                            data = new_data

                entries[name] = data

        if renames:
            ct_key = "[Content_Types].xml"
            if ct_key in entries:
                entries[ct_key] = update_content_types(
                    entries[ct_key].decode("utf-8"), renames
                ).encode("utf-8")

            xml_keys = [k for k in entries if k.endswith(".xml") or k.endswith(".rels")]
            for k in xml_keys:
                if k == ct_key:
                    continue
                try:
                    text = entries[k].decode("utf-8")
                    updated = update_rels_and_slides(text, renames)
                    if updated != text:
                        entries[k] = updated.encode("utf-8")
                except UnicodeDecodeError:
                    pass

        with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9) as zout:
            for name, data in entries.items():
                zout.writestr(name, data)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    new_file_size = os.path.getsize(output_path)
    total_saved = orig_file_size - new_file_size
    total_pct = (total_saved / orig_file_size * 100) if orig_file_size > 0 else 0

    print()
    print("=" * 60)
    print(f"图片处理: {images_processed} 张, 其中 {images_saved} 张被压缩")
    if videos_processed > 0 or has_video_in_pptx:
        print(f"视频处理: {videos_processed} 个, 其中 {videos_saved} 个被压缩")
    print(f"原始大小: {format_size(orig_file_size)}")
    print(f"压缩后:   {format_size(new_file_size)}")
    print(f"节省:     {format_size(total_saved)} ({total_pct:.1f}%)")
    print(f"输出:     {output_path}")
    print("=" * 60)

    if has_video_in_pptx and not ffmpeg_path and not opts["no_video"]:
        print_ffmpeg_install_guide()

    return True


def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def main():
    args = parse_args()
    opts = resolve_options(args)

    input_path = os.path.abspath(args.input)
    if not input_path.lower().endswith(".pptx"):
        print("警告: 输入文件不是 .pptx 格式，将尝试按 ZIP 处理", file=sys.stderr)

    if args.output:
        output_path = os.path.abspath(args.output)
    else:
        stem = Path(input_path).stem
        parent = Path(input_path).parent
        output_path = str(parent / f"{stem}_compressed.pptx")

    if os.path.abspath(input_path) == os.path.abspath(output_path):
        print("错误: 输入和输出路径不能相同", file=sys.stderr)
        sys.exit(1)

    success = compress_pptx(input_path, output_path, opts)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
