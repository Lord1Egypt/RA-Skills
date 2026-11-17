import hashlib
import json
import sys

from PIL import Image

# 各引擎脚本共用的图片小工具（跨平台，依赖 Pillow）：
#   png <输入> <输出>   转成真正的 PNG
#   size <文件>         宽高
#   fp <文件>...        解码后像素的 sha256：同一张图换了格式也认得出；一次可传多个文件
#   style <图> <锚>...  调色板相似度，0 到 1。系列模式用它筛图，不联网。

_BOX = Image.Resampling.BOX if hasattr(Image, "Resampling") else Image.BOX
_COLOR_WEIGHT = 0.8
_STRUCTURE_WEIGHT = 0.2


def fingerprint(path):
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        return hashlib.sha256(f"{rgba.width}x{rgba.height}".encode() + rgba.tobytes()).hexdigest()


def _cosine(left, right):
    dot = left_norm = right_norm = 0.0
    for a, b in zip(left, right):
        dot += a * b
        left_norm += a * a
        right_norm += b * b
    if left_norm <= 0.0 or right_norm <= 0.0:
        return 0.0
    return dot / ((left_norm ** 0.5) * (right_norm ** 0.5))


def _features(path):
    with Image.open(path) as image:
        rgb = image.convert("RGB").resize((64, 64), _BOX)
        pixels = list(rgb.getdata())
    hist = [0.0] * 512
    grid = [0.0] * 16
    for index, (red, green, blue) in enumerate(pixels):
        hist[(red // 32) * 64 + (green // 32) * 8 + (blue // 32)] += 1.0
        row, col = divmod(index, 64)
        grid[(row // 16) * 4 + (col // 16)] += 0.2126 * red + 0.7152 * green + 0.0722 * blue
    total = float(len(pixels)) or 1.0
    return [value / total for value in hist], grid


def style_score(output, anchors):
    if not anchors:
        raise SystemExit("style needs an output and at least one anchor")
    out_hist, out_grid = _features(output)
    best = 0.0
    for anchor in anchors:
        hist, grid = _features(anchor)
        score = _COLOR_WEIGHT * _cosine(out_hist, hist) + _STRUCTURE_WEIGHT * _cosine(out_grid, grid)
        if score > best:
            best = score
    return {
        "method": "palette-histogram",
        "score": round(best, 4),
        "color_weight": _COLOR_WEIGHT,
        "structure_weight": _STRUCTURE_WEIGHT,
    }


def main():
    command = sys.argv[1]
    if command == "fp":
        print(json.dumps({"fp": [fingerprint(item) for item in sys.argv[2:]]}))
        return
    if command == "style":
        print(json.dumps(style_score(sys.argv[2], sys.argv[3:])))
        return
    path = sys.argv[2]
    with Image.open(path) as image:
        if command == "png":
            image.save(sys.argv[3], "PNG")
            result = {"width": image.width, "height": image.height}
        elif command == "size":
            result = {"width": image.width, "height": image.height}
        else:
            raise SystemExit(f"unknown command: {command}")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
