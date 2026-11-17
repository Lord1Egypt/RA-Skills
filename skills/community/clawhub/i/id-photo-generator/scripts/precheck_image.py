#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
id-photo-generator 前置校验脚本 (Front-Gate Precheck)

在任何人脸检测 / 抠图 / 换底模型之前运行。职责（全部为确定性检查）：
  1. 魔数识别真实图片格式（防后缀欺骗），拦截 GIF、损坏文件
  2. EXIF Orientation 物理旋转矫正
  3. 文件大小 / 分辨率硬限制（512-4096px, <=10MB）
  4. CMYK 色彩空间自动转 RGB（软警告）
  5. 输入透明通道 PNG 填充中性灰后再评估（软警告）
  6. 图像质量门禁：模糊(Laplacian方差)、曝光(均值亮度)

用法:
    python precheck_image.py <图片路径> [--json]

输出:
    结构化 JSON。hard_fail 终止生成；ok=True 且 soft_warnings 非空 = 放行但附风险提示。

人脸存在/数量、人脸质量与可见性、真实性预筛、抠图等后续步骤需要
外部模型（MTCNN/RetinaFace/InsightFace、MODNet/BiRefNet 等），本脚本不覆盖，
由执行 Agent 依据 references/validation-spec.md 完成。
"""

import sys
import json
import argparse
from pathlib import Path

MIN_SIZE = 512        # 单边最小像素
MAX_SIZE = 4096       # 单边最大像素
MAX_BYTES = 10 * 1024 * 1024  # 10 MB


def detect_real_format(data: bytes) -> str:
    """读取文件头魔数识别真实格式，不依赖后缀。返回 jpeg/png/webp/gif/unknown。"""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if data[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    return "unknown"


def apply_exif_orientation(img):
    """依据 EXIF Orientation 做物理旋转矫正。"""
    try:
        exif = img.getexif()
        orientation = exif.get(0x0112, 1)
    except Exception:
        orientation = 1
    if orientation == 2:
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    if orientation == 3:
        return img.rotate(180, expand=True)
    if orientation == 4:
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    if orientation == 5:
        return img.transpose(Image.FLIP_LEFT_RIGHT).rotate(90, expand=True)
    if orientation == 6:
        return img.rotate(270, expand=True)
    if orientation == 7:
        return img.transpose(Image.FLIP_TOP_BOTTOM).rotate(90, expand=True)
    if orientation == 8:
        return img.rotate(90, expand=True)
    return img


def check_image_quality(img):
    """模糊 + 曝光门禁。返回 (ok, reason, message)。"""
    # 转灰度
    gray = img.convert("L")
    w, h = gray.size
    if w < 8 or h < 8:
        return False, "too_small", "图片分辨率过低，请上传更清晰的照片。"

    # Laplacian 方差做模糊检测
    import math
    px = gray.load()
    # 中心采样避免边缘噪声影响
    step_x = max(1, w // 200)
    step_y = max(1, h // 200)
    sum_sq = 0.0
    count = 0
    for y in range(2, h - 2, step_y):
        for x in range(2, w - 2, step_x):
            v = px[x, y]
            lap = (px[x + 1, y] + px[x - 1, y] + px[x, y + 1] + px[x, y - 1] - 4 * v)
            sum_sq += lap * lap
            count += 1
    var = (sum_sq / count) if count else 0.0
    BLUR_THRESHOLD = 80.0
    if var < BLUR_THRESHOLD:
        return False, "blurry", "图片模糊，请保持相机稳定、对焦清晰后重新拍摄。"

    # 曝光：整体均值
    total = 0
    n = 0
    for y in range(0, h, max(1, h // 100)):
        for x in range(0, w, max(1, w // 100)):
            total += px[x, y]
            n += 1
    mean = (total / n) if n else 128
    if mean < 45:
        return False, "underexposed", "图片过暗，请在光线均匀的环境下拍摄。"
    if mean > 225:
        return False, "overexposed", "图片过曝，请在光线均匀的环境下拍摄。"

    return True, "ok", ""


def precheck(path: str):
    result = {
        "ok": False,
        "hard_fail": None,        # {code, message}
        "soft_warnings": [],      # list[str]
        "meta": {},               # 规范化后的信息
    }

    p = Path(path)
    if not p.exists():
        result["hard_fail"] = {"code": "not_found", "message": "图片文件不存在，请重新上传。"}
        return result

    data = None
    try:
        data = p.read_bytes()
    except OSError as e:
        result["hard_fail"] = {"code": "read_error", "message": "图片文件读取失败，请重新上传正常图片。"}
        return result

    # 1) 魔数识别真实格式
    real_format = detect_real_format(data)
    if real_format == "gif":
        result["hard_fail"] = {"code": "gif",
                               "message": "不支持GIF动图，请上传静态JPG、PNG或WEBP图片。"}
        return result
    if real_format == "unknown":
        result["hard_fail"] = {"code": "format",
                               "message": "请上传 JPG、PNG 或 WEBP 格式的图片。"}
        return result

    # 2) 文件大小
    size_bytes = len(data)
    if size_bytes > MAX_BYTES:
        result["hard_fail"] = {"code": "too_large",
                               "message": "图片文件过大，请压缩至 10MB 以内后重试。"}
        return result

    # 3) 解码（捕获损坏文件）
    from PIL import Image, ImageOps
    try:
        img = Image.open(p)
        img.load()
    except Exception:
        result["hard_fail"] = {"code": "corrupt",
                               "message": "图片文件损坏，无法解析，请重新上传正常图片。"}
        return result

    # 4) EXIF 物理旋转矫正
    img = apply_exif_orientation(img)

    # 5) 分辨率校验（矫正后）
    w, h = img.size
    if min(w, h) < MIN_SIZE:
        result["hard_fail"] = {"code": "low_res",
                               "message": "图片分辨率过低，请上传更清晰的照片。"}
        return result
    if max(w, h) > MAX_SIZE:
        # 自动等比缩放
        scale = MAX_SIZE / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        w, h = img.size
        result["soft_warnings"].append("图片分辨率较大，已自动缩放至 4096px 以内再处理。")

    # 6) 色彩模式处理
    mode = img.mode
    if mode == "CMYK":
        img = img.convert("RGB")
        result["soft_warnings"].append(
            "图片为印刷CMYK色彩模式，已自动转为RGB，建议优先直接使用RGB拍摄的原图。")
    has_input_alpha = mode in ("RGBA", "LA", "PA") or "transparency" in img.info
    if has_input_alpha:
        # 透明区域填充中性灰后再评估质量
        from PIL import Image as _Image
        rgba = img.convert("RGBA")
        bg = _Image.new("RGBA", rgba.size, (128, 128, 128, 255))
        bg.paste(rgba, mask=rgba.getchannel("A"))
        img = bg.convert("RGB")
        result["soft_warnings"].append(
            "您上传的是自带透明通道的图片，建议使用实拍原始照片，部分官方系统不接受二次编辑图片。")

    # 7) 图像质量门禁
    ok, reason, msg = check_image_quality(img)
    if not ok:
        result["hard_fail"] = {"code": reason, "message": msg}
        return result

    result["ok"] = True
    result["meta"] = {
        "real_format": real_format,
        "size_bytes": size_bytes,
        "width": w,
        "height": h,
        "mode": img.mode,
        "had_input_alpha": has_input_alpha,
    }
    return result


def main():
    parser = argparse.ArgumentParser(description="证件照生成前置校验")
    parser.add_argument("image", help="图片路径")
    parser.add_argument("--json", action="store_true", help="仅输出 JSON")
    args = parser.parse_args()

    res = precheck(args.image)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        if res["ok"]:
            print("PASS")
            for wmsg in res["soft_warnings"]:
                print(f"  WARN: {wmsg}")
            m = res["meta"]
            print(f"  format={m['real_format']} size={m['size_bytes']}B "
                  f"dims={m['width']}x{m['height']} mode={m['mode']}")
        else:
            print("FAIL")
            print(f"  code={res['hard_fail']['code']}")
            print(f"  message={res['hard_fail']['message']}")
    return 0 if res["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
