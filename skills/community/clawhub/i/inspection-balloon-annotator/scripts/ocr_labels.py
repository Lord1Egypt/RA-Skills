# -*- coding: utf-8 -*-
"""Step 1: 多方向 OCR, 输出标注文字坐标(JSON)。
用法: python ocr_labels.py <render.png> <labels.json> [--min-conf 0.4]

对 0°/90°/270° 三个方向各跑一次 OCR 再合并 —— 竖直排版的尺寸文字(如 26/14/13/5.5)
在 0° 下识别不到, 但在 90°/270° 下能识别, 从而拿到其真实坐标。
输出的 x,y 为文字框中心, 坐标系与 render.png 完全一致。
"""
import argparse, json
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR


def _run(ocr, arr):
    out = ocr(arr)
    res = out[0] if isinstance(out, tuple) else out
    if not res:
        return []
    r = []
    for it in res:
        box, text, score = it[0], it[1], it[2]
        xs = [p[0] for p in box]; ys = [p[1] for p in box]
        r.append((( min(xs)+max(xs))/2, (min(ys)+max(ys))/2,
                  max(xs)-min(xs), max(ys)-min(ys), str(text), float(score)))
    return r


def _crop_white(img, margin_frac=0.02, min_keep=0.5):
    """裁掉外围空白边（图纸白边），保留分辨率不丢文字；返回裁切图与 (x0,y0) 偏移。
    若内容占比过小（近乎整页空白或内容铺满）则放弃裁切返回原图。"""
    gray = img[..., :3].min(axis=2)
    mask = gray < 245
    ys, xs = np.where(mask)
    H, W = img.shape[:2]
    if len(xs) == 0:
        return img, (0, 0)
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    mx = max(2, int(W*margin_frac)); my = max(2, int(H*margin_frac))
    x0, x1 = max(0, x0-mx), min(W-1, x1+mx)
    y0, y1 = max(0, y0-my), min(H-1, y1+my)
    if (x1-x0)*(y1-y0) < min_keep*W*H:
        return img, (0, 0)
    return img[y0:y1+1, x0:x1+1], (x0, y0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("png"); ap.add_argument("out")
    ap.add_argument("--min-conf", type=float, default=0.40)
    ap.add_argument("--no-crop", action="store_true", help="禁用白边裁切（默认裁切以加速 OCR）")
    a = ap.parse_args()

    img = np.array(Image.open(a.png).convert("RGB"))
    H, W = img.shape[:2]
    ocr = RapidOCR()

    if a.no_crop:
        crop_img, (ox, oy) = img, (0, 0)
    else:
        crop_img, (ox, oy) = _crop_white(img)
    Hc, Wc = crop_img.shape[:2]

    items = []  # (x,y,w,h,text,conf,ori)  —— 坐标统一回偏到原图(全图)空间
    for x, y, w, h, t, s in _run(ocr, crop_img):                  # 0°
        items.append((x+ox, y+oy, w, h, t, s, "H"))
    for xr, yr, w, h, t, s in _run(ocr, np.rot90(crop_img, 1)):   # 90° CCW
        items.append(((Wc-1)-yr+ox, xr+oy, h, w, t, s, "V90"))
    for xr, yr, w, h, t, s in _run(ocr, np.rot90(crop_img, 3)):   # 270°
        items.append((yr+ox, (Hc-1)-xr+oy, h, w, t, s, "V270"))

    # 去重(同文本 + 邻近坐标)
    seen, keep = set(), []
    for it in items:
        if it[5] < a.min_conf:
            continue
        key = (it[4], round(it[0]/18), round(it[1]/18))
        if key in seen:
            continue
        seen.add(key)
        keep.append({"text": it[4], "x": round(it[0], 1), "y": round(it[1], 1),
                     "w": round(it[2], 1), "h": round(it[3], 1),
                     "conf": round(it[5], 2), "ori": it[6]})
    keep.sort(key=lambda d: (round(d["y"]/160), d["x"]))
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump({"image_size": [W, H], "count": len(keep), "labels": keep},
                  f, ensure_ascii=False, indent=1)
    print(f"OK labels={len(keep)} -> {a.out}  image={W}x{H}")


if __name__ == "__main__":
    main()
