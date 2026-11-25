import hashlib
import json
import math
import os
import sys

from PIL import Image, ImageOps

# 各引擎脚本共用的图片小工具（跨平台，依赖 Pillow）：
#   png <输入> <输出>   转成真正的 PNG
#   size <文件>         宽高
#   fp <文件>...        解码后像素的 sha256：同一张图换了格式也认得出；一次可传多个文件
#   style <图> <锚>... [--method auto|structure|clip|palette-histogram]
#                       系列模式的一致性分数，0 到 1，不联网。
#   backends            哪些打分方法能用（clip 要用户自己装 numpy、onnxruntime 和模型文件）
#
# Series-mode consistency methods. Every score is 0 to 1 and runs locally, with no network call.
#   structure          (Pillow only, the default when CLIP is not installed)
#                      0.4 x grayscale SSIM + 0.5 x gradient-orientation grid (HOG-like)
#                      + 0.1 x the palette-histogram score below.
#   clip               (optional) cosine similarity of CLIP ViT-B/32 image embeddings from a local
#                      ONNX file. Needs numpy, onnxruntime and a model file the user downloaded on
#                      purpose (SETUP.md). Nothing is downloaded here.
#   palette-histogram  the 1.3.x score: 0.8 x cosine of an 8-bin joint RGB histogram plus
#                      0.2 x cosine of a 4x4 luminance grid, from a 64x64 resize.
# structure and clip are calibrated so that 0.72 is the measured operating point of each
# method (docs/series-consistency-validation.md): the raw score is mapped piecewise linearly,
# raw 0 -> 0, raw operating point -> 0.72, raw 1 -> 1. The raw value is reported as raw_score.
# palette-histogram is not remapped, so old thresholds keep their old meaning.

_BOX = Image.Resampling.BOX if hasattr(Image, "Resampling") else Image.BOX
_BICUBIC = Image.Resampling.BICUBIC if hasattr(Image, "Resampling") else Image.BICUBIC
_COLOR_WEIGHT = 0.8
_STRUCTURE_WEIGHT = 0.2

PALETTE = "palette-histogram"
STRUCTURE = "structure"
CLIP = "clip"
AUTO = "auto"
METHODS = (AUTO, STRUCTURE, CLIP, PALETTE)
DEFAULT_THRESHOLD = 0.72
# Raw operating points: the equal-error-rate point of each method on the validation set,
# rounded to 0.01 (docs/series-consistency-validation.md).
RAW_OPERATING_POINT = {STRUCTURE: 0.42, CLIP: 0.65}
STRUCTURE_WEIGHTS = {"ssim": 0.4, "hog": 0.5, "palette": 0.1}

CLIP_MODEL_NAME = "clip-vit-b32-vision-q8.onnx"
# SHA-256 of the two Xenova/clip-vit-base-patch32 vision encoders that were validated.
CLIP_KNOWN_SHA256 = {
    "583fd1110a514667812fee7d684952aaf82a99b959760c8d7dca7e0ab9839299": "vision_model_quantized.onnx (int8, 89 MB)",
    "fd6e1402a588279d1723c7534d4bcba5bc0b14b47dfab0e46f8c47b8270d7d40": "vision_model.onnx (fp32, 352 MB)",
}
_CLIP_MEAN = (0.48145466, 0.4578275, 0.40821073)
_CLIP_STD = (0.26862954, 0.26130258, 0.27577711)


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


# ---- palette-histogram (unchanged from 1.3.x)

def _features(path):
    with Image.open(path) as image:
        data = image.convert("RGB").resize((64, 64), _BOX).tobytes()
    hist = [0.0] * 512
    grid = [0.0] * 16
    for index in range(len(data) // 3):
        red, green, blue = data[3 * index], data[3 * index + 1], data[3 * index + 2]
        hist[(red // 32) * 64 + (green // 32) * 8 + (blue // 32)] += 1.0
        row, col = divmod(index, 64)
        grid[(row // 16) * 4 + (col // 16)] += 0.2126 * red + 0.7152 * green + 0.0722 * blue
    total = float(len(data) // 3) or 1.0
    return [value / total for value in hist], grid


def _palette_parts(left, right):
    histogram = _cosine(left[0], right[0])
    grid = _cosine(left[1], right[1])
    return _COLOR_WEIGHT * histogram + _STRUCTURE_WEIGHT * grid, histogram, grid


# ---- structure (Pillow only)

def load_rgb(path):
    """RGB pixels; transparent areas are composited on white so a logo cut-out compares as drawn."""
    with Image.open(path) as image:
        image.load()
        if image.mode in ("RGBA", "LA", "PA") or (image.mode == "P" and "transparency" in image.info):
            rgba = image.convert("RGBA")
            base = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
            base.alpha_composite(rgba)
            return base.convert("RGB")
        return image.convert("RGB")


def _gray64(rgb):
    return list(rgb.convert("L").resize((64, 64), _BOX).tobytes())


def _ssim(left, right, size=64, window=8, step=4):
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    total = 0.0
    count = 0
    for y0 in range(0, size - window + 1, step):
        for x0 in range(0, size - window + 1, step):
            xs = []
            ys = []
            for y in range(y0, y0 + window):
                base = y * size + x0
                xs.extend(left[base:base + window])
                ys.extend(right[base:base + window])
            n = len(xs)
            mx = sum(xs) / n
            my = sum(ys) / n
            vx = sum((v - mx) ** 2 for v in xs) / n
            vy = sum((v - my) ** 2 for v in ys) / n
            cov = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / n
            total += ((2 * mx * my + c1) * (2 * cov + c2)) / ((mx * mx + my * my + c1) * (vx + vy + c2))
            count += 1
    return max(0.0, min(1.0, total / count))


def _hog(gray, size=64, cells=4, bins=9):
    """Gradient-orientation histograms on a 4x4 grid, each cell L2-normalized (HOG-like)."""
    cell = size // cells
    hist = [[0.0] * bins for _ in range(cells * cells)]
    energy = 0.0
    for y in range(1, size - 1):
        row = y * size
        for x in range(1, size - 1):
            i = row + x
            gx = gray[i + 1] - gray[i - 1]
            gy = gray[i + size] - gray[i - size]
            if gx == 0 and gy == 0:
                continue
            magnitude = math.hypot(gx, gy)
            angle = math.degrees(math.atan2(gy, gx)) % 180.0
            hist[(y // cell) * cells + x // cell][int(angle / (180.0 / bins)) % bins] += magnitude
            energy += magnitude
    vector = []
    for values in hist:
        norm = math.sqrt(sum(v * v for v in values)) or 1.0
        vector.extend(v / norm for v in values)
    return vector, energy


def structure_features(path):
    gray = _gray64(load_rgb(path))
    hog, energy = _hog(gray)
    return {"gray": gray, "hog": hog, "flat": energy < 1.0, "palette": _features(path)}


def structure_parts(left, right):
    if left["flat"] and right["flat"]:
        hog = 1.0
    else:
        hog = max(0.0, _cosine(left["hog"], right["hog"]))
    ssim = _ssim(left["gray"], right["gray"])
    palette = _palette_parts(left["palette"], right["palette"])[0]
    parts = {"ssim": ssim, "hog": hog, "palette": palette}
    raw = sum(STRUCTURE_WEIGHTS[name] * parts[name] for name in STRUCTURE_WEIGHTS)
    return raw, parts


# ---- clip (optional)

def clip_model_path():
    configured = os.environ.get("IMAGE_GEN_CLIP_MODEL")
    if configured:
        return os.path.abspath(os.path.expanduser(configured))
    return os.path.join(os.path.expanduser("~"), ".config", "imagegen-swarm", "models", CLIP_MODEL_NAME)


def clip_status():
    """Is the optional CLIP backend usable? Never downloads anything."""
    path = clip_model_path()
    status = {"available": False, "model": path}
    missing = []
    try:
        import numpy  # noqa: F401
    except Exception:
        missing.append("numpy")
    try:
        import onnxruntime  # noqa: F401
    except Exception:
        missing.append("onnxruntime")
    if missing:
        status["reason"] = "missing Python package(s): " + ", ".join(missing)
        return status
    if not os.path.isfile(path):
        status["reason"] = "model file not found (optional; see SETUP.md, Series consistency)"
        return status
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    status["sha256"] = digest.hexdigest()
    status["known_model"] = CLIP_KNOWN_SHA256.get(status["sha256"])
    if not status["known_model"] and os.environ.get("IMAGE_GEN_CLIP_ALLOW_UNVERIFIED") != "yes":
        status["reason"] = "clip model hash is not one of the validated models; see SETUP.md"
        return status
    status["available"] = True
    return status


class _Clip:
    def __init__(self):
        status = clip_status()
        if not status["available"]:
            raise SystemExit("clip method unavailable: " + status["reason"])
        import numpy
        import onnxruntime
        self.np = numpy
        options = onnxruntime.SessionOptions()
        options.log_severity_level = 3
        self.session = onnxruntime.InferenceSession(status["model"], options, providers=["CPUExecutionProvider"])
        self.input = self.session.get_inputs()[0].name

    def embed(self, path):
        np = self.np
        image = ImageOps.pad(load_rgb(path), (224, 224), _BICUBIC, color=(255, 255, 255))
        pixels = (np.asarray(image, dtype=np.float32) / 255.0 - np.array(_CLIP_MEAN, np.float32)) / np.array(_CLIP_STD, np.float32)
        output = self.session.run(None, {self.input: pixels.transpose(2, 0, 1)[None]})[0]
        vector = output[0, 0] if output.ndim == 3 else output[0]
        return vector / (np.linalg.norm(vector) or 1.0)


# ---- scoring

def calibrate(method, raw):
    point = RAW_OPERATING_POINT.get(method)
    if point is None:
        return raw
    raw = max(0.0, min(1.0, raw))
    if raw <= point:
        return DEFAULT_THRESHOLD * raw / point
    return DEFAULT_THRESHOLD + (1.0 - DEFAULT_THRESHOLD) * (raw - point) / (1.0 - point)


def resolve_method(method):
    if method in ("palette", PALETTE):
        return PALETTE
    if method == AUTO:
        return CLIP if clip_status()["available"] else STRUCTURE
    if method not in METHODS:
        raise SystemExit("unknown style method: " + str(method) + " (use " + ", ".join(METHODS) + ")")
    return method


def _round(parts):
    return {name: round(value, 4) for name, value in parts.items()}


def style_score(output, anchors, method=PALETTE):
    if not anchors:
        raise SystemExit("style needs an output and at least one anchor")
    requested = method
    method = resolve_method(method)
    best = None
    if method == PALETTE:
        out_features = _features(output)
        for index, anchor in enumerate(anchors):
            score, histogram, grid = _palette_parts(out_features, _features(anchor))
            if best is None or score > best[0]:
                best = (score, score, {"histogram": histogram, "luminance_grid": grid}, index)
        result = {"method": PALETTE, "score": round(best[0], 4), "color_weight": _COLOR_WEIGHT,
                  "structure_weight": _STRUCTURE_WEIGHT}
    elif method == STRUCTURE:
        out_features = structure_features(output)
        for index, anchor in enumerate(anchors):
            raw, parts = structure_parts(out_features, structure_features(anchor))
            score = calibrate(STRUCTURE, raw)
            if best is None or score > best[0]:
                best = (score, raw, parts, index)
        result = {"method": STRUCTURE, "score": round(best[0], 4), "weights": STRUCTURE_WEIGHTS}
    else:
        clip = _Clip()
        out_vector = clip.embed(output)
        for index, anchor in enumerate(anchors):
            raw = float(clip.np.dot(out_vector, clip.embed(anchor)))
            score = calibrate(CLIP, raw)
            if best is None or score > best[0]:
                best = (score, raw, {"clip_cosine": raw}, index)
        result = {"method": CLIP, "score": round(best[0], 4), "model": os.path.basename(clip_model_path())}
    result.update({"raw_score": round(best[1], 4), "components": _round(best[2]), "anchor": best[3]})
    if requested != method:
        result["requested_method"] = requested
    if method in RAW_OPERATING_POINT:
        result["raw_operating_point"] = RAW_OPERATING_POINT[method]
    return result


def backends():
    clip = clip_status()
    return {
        "methods": {
            STRUCTURE: {"available": True, "weights": STRUCTURE_WEIGHTS},
            PALETTE: {"available": True, "weights": {"histogram": _COLOR_WEIGHT, "luminance_grid": _STRUCTURE_WEIGHT}},
            CLIP: {**clip, "weights": {"clip_cosine": 1.0}},
        },
        "auto": CLIP if clip["available"] else STRUCTURE,
        "default_threshold": DEFAULT_THRESHOLD,
    }


def _style_args(argv):
    method = PALETTE
    files = []
    index = 0
    while index < len(argv):
        if argv[index] == "--method":
            if index + 1 >= len(argv):
                raise SystemExit("--method needs a value")
            method = argv[index + 1]
            index += 2
            continue
        files.append(argv[index])
        index += 1
    if len(files) < 2:
        raise SystemExit("style needs an output and at least one anchor")
    return files[0], files[1:], method


def main():
    command = sys.argv[1]
    if command == "fp":
        print(json.dumps({"fp": [fingerprint(item) for item in sys.argv[2:]]}))
        return
    if command == "style":
        output, anchors, method = _style_args(sys.argv[2:])
        print(json.dumps(style_score(output, anchors, method)))
        return
    if command == "backends":
        print(json.dumps(backends()))
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
