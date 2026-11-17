#!/usr/bin/env python3
"""探测远程图片显示宽高并组装 imagegen aspectRatio。

用 Pillow 读图片头部即可拿到 `.size`（不会加载整张像素）。
爆款复刻在用户选择默认比例时逐张调用本脚本，把当前图二的真实显示宽高
原样组装为 ``W:H``（不约分），传给 imagegen 的 ``aspectRatio``。

用法:
    python probe_image_size.py <url> [<url> ...]

输出 (stdout，每个 URL 一行 JSON):
    {"url": "...", "width": 1200, "height": 1600, "aspectRatio": "1200:1600"}
    {"url": "...", "error": "..."}
"""
import io
import json
import sys
import urllib.request

from PIL import Image

TIMEOUT = 15
_UA = "Mozilla/5.0 (compatible; linkfox-image-probe/1.0)"
_EXIF_ORIENTATION = 274
_SWAPPED_ORIENTATIONS = frozenset({5, 6, 7, 8})


def _fetch(url, nbytes):
    """优先用 Range 只取前 nbytes 字节；服务端不支持 Range 时退化为普通 GET。"""
    req = urllib.request.Request(
        url, headers={"Range": f"bytes=0-{nbytes - 1}", "User-Agent": _UA}
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read(nbytes)
    except Exception:
        req2 = urllib.request.Request(url, headers={"User-Agent": _UA})
        with urllib.request.urlopen(req2, timeout=TIMEOUT) as resp:
            return resp.read(nbytes)


def _display_size(image):
    """返回考虑 EXIF 旋转后的显示宽高，不加载完整像素。"""
    width, height = image.size
    try:
        orientation = image.getexif().get(_EXIF_ORIENTATION)
    except Exception:
        orientation = None
    if orientation in _SWAPPED_ORIENTATIONS:
        width, height = height, width
    if width <= 0 or height <= 0:
        raise ValueError(f"图片宽高非法: {width}x{height}")
    return width, height


def probe(url):
    # 先取 64KB，头部读不出尺寸（如 SOF 较靠后的 JPEG）再扩到 512KB 重试一次
    for nbytes in (64 * 1024, 512 * 1024):
        data = _fetch(url, nbytes)
        try:
            with Image.open(io.BytesIO(data)) as im:
                width, height = _display_size(im)
                return {
                    "url": url,
                    "width": width,
                    "height": height,
                    "aspectRatio": f"{width}:{height}",
                }
        except Exception:
            continue
    return {"url": url, "error": "无法从文件头解析宽高"}


def main():
    urls = sys.argv[1:]
    if not urls:
        print(json.dumps({"error": "用法: python probe_image_size.py <url> [<url> ...]"},
                         ensure_ascii=False))
        sys.exit(1)
    for url in urls:
        try:
            out = probe(url)
        except Exception as e:  # noqa: BLE001 — 单张失败不影响其余 URL
            out = {"url": url, "error": str(e)}
        print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
