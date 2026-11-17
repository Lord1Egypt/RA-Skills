#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给插图做后期：裁水印（必做）+ 可选的「相框感」白边。

**默认不加框，只做裁切。**加框是可选步骤，仅当用户明确要求「留白边 / 相框感」时才传 `--frame`。
（v1.3.4 起行为变更：旧版默认加白边，现在默认不加。）

模型基本不遵守 prompt 里的「四周留白」，所以相框感只能后期加——但「要不要相框感」是用户的
选择，不是默认动作。结构（`--frame` 时）：图像 → 白隙 gap → 〔细线框 line，可选〕 → 外侧白边 pad

用法：
    python3 add_frame.py in.png out.png                                # 什么都不做（原图输出）
    python3 add_frame.py in.png out.png --auto-crop                    # 优先：自动量测水印上沿并裁
    python3 add_frame.py in.png out.png --auto-crop --ratio 2.35       # 自动裁水印 + 裁到 2.35:1
    python3 add_frame.py in.png out.png --crop-bottom 80               # 已知 CUT 时直接裁（同批复用）
    python3 add_frame.py in.png out.png --crop-bottom 70 --ratio 2.35  # 裁水印 + 裁到 2.35:1
    python3 add_frame.py in.png out.png --crop-bottom 80 --frame --line 0        # 用户要留白边时才加
    python3 add_frame.py in.png out.png --crop-bottom 70 --ratio 2.35 --frame --line 0
    python3 add_frame.py in.png out.png --crop-bottom 70 --frame --ratio 1 --pad 0.04 --line 0

依赖：Pillow（`python3 -m pip install Pillow`）。

参数说明：
    --auto-crop  自动量测右下角水印上沿并裁底边。判据是「相对背景的笔画梯度能量」，
                 不是绝对暗阈值（极淡/半透明水印也能抓）。测不到时**仍按尺寸经验值裁**
                 并打印 FALLBACK —— 测不到 ≠ 没有水印。与 --crop-bottom 互斥。
    --frame  是否加留白边框。**默认不加**；只有用户明确要求「留白边 / 相框感」时才传。
    --pad    外侧白边宽度，取短边的比例，默认 0.06（5%~6% 观感最好）；仅 --frame 时生效
    --gap    图像与外沿之间的白隙，默认 11px；仅 --frame 时生效
    --line   线框粗细，默认 3px；**传 0 则只留白边不画线**（2026-09-26 用户偏好）；仅 --frame 时生效
    --ratio  目标宽高比：不加框时指裁切后图像本身，加框时指含框后的整体
"""
import argparse
from PIL import Image, ImageDraw

PAPER = (255, 255, 255)
INK = (30, 30, 30)


def frame_geoms(w, h, pad_ratio, line, gap):
    """返回 (pad, F)：pad 是外侧白边，F 是图像距外框的总边距。"""
    pad = int(min(w, h) * pad_ratio)
    return pad, pad + line + gap


def add_frame(im, pad_ratio=0.06, gap=11, line=3, ink=INK, paper=PAPER):
    w, h = im.size
    pad, F = frame_geoms(w, h, pad_ratio, line, gap)
    canvas = Image.new("RGB", (w + 2 * F, h + 2 * F), paper)
    canvas.paste(im, (F, F))
    if line > 0:
        dr = ImageDraw.Draw(canvas)
        for i in range(line):
            dr.rectangle(
                [pad - i, pad - i, w + 2 * F - 1 - pad + i, h + 2 * F - 1 - pad + i],
                outline=ink,
            )
    return canvas


def inner_h_for_ratio(w, target, pad_ratio=0.06, gap=11, line=3):
    """二分求内部高度，使「加框后」的整体宽高比恰为 target。

    注意：pad 依赖短边，短边随内部高度变化 → 不能手算，必须迭代。
    """
    lo, hi = 50, w * 4
    for _ in range(64):
        mid = (lo + hi) // 2
        _, F = frame_geoms(w, mid, pad_ratio, line, gap)
        r = (w + 2 * F) / (mid + 2 * F)
        if r > target:      # 太高，需要更大的高度
            lo = mid
        else:
            hi = mid
    return hi


def fit_ratio(im, target, pad_ratio=0.06, gap=11, line=3, top_bias=0.72):
    """裁切图像，使「加框后」整体比例恰为 target。宽高比够就裁高度，否则裁宽度。"""
    w, h = im.size
    th = inner_h_for_ratio(w, target, pad_ratio, gap, line)
    if th <= h:                                   # 目标更扁 → 裁高度
        cut = h - th
        top = int(cut * top_bias)
        return im.crop((0, top, w, top + th))
    # 目标更方/更高 → 高度不够，改裁宽度（F 以高度为短边估）
    _, F = frame_geoms(h, h, pad_ratio, line, gap)
    tw = max(1, min(w, int(target * (h + 2 * F) - 2 * F)))
    left = (w - tw) // 2
    return im.crop((left, 0, left + tw, h))


def measure_watermark_cut(im):
    """自动量测右下角水印上沿，返回 (cut, ok, detail)。

    逐行统计「相对背景的笔画梯度能量」：文字笔画在水平方向产生密集灰度跳变，
    平滑背景不会。用相对量而非绝对暗阈值，浅色 / 半透明水印也能抓。
    极淡水印（v1.3.5 实测最小灰度 122~175）仍可能整段测不到 -> ok=False。
    """
    w, h = im.size
    band_h = min(180, max(40, h // 4))
    x0 = max(0, w - min(300, w // 3))
    x1 = max(x0 + 2, w - 8)
    gray = im.crop((x0, h - band_h, x1, h)).convert("L")
    pw, ph = gray.size
    px = gray.load()
    JUMP = 12
    energy = []
    for y in range(ph):
        e = 0
        prev = px[0, y]
        for x in range(1, pw):
            cur = px[x, y]
            d = cur - prev
            if d > JUMP or d < -JUMP:
                e += 1
            prev = cur
        energy.append(e)

    head = energy[: max(1, ph // 3)]
    base = sorted(head)[len(head) // 2]
    peak = max(energy)
    thresh = max(6, base * 2.2 + 3, peak * 0.45)
    if peak < thresh or peak < 8:
        return 0, False, "peak=%d base=%d 无可识别笔画带" % (peak, base)

    # 从底部往上找最下面一段连续高能量带的上沿
    low = thresh * 0.45
    y = ph - 1
    while y > 0 and energy[y] < low:
        y -= 1
    y1 = y
    gap = 0
    while y > 0:
        if energy[y] >= low:
            gap = 0
        else:
            gap += 1
            if gap > 6:
                break
        y -= 1
    y0 = y
    band = y1 - y0 + 1
    if band < 8 or band > 100:
        return 0, False, "笔画带宽度异常 %dpx" % band

    cut = band_h - y0 + 8                       # 上沿到底边 + 8px 安全余量
    cut = max(40, min(cut, int(h * 0.18), 160))
    ref = fallback_cut(im)
    if cut > ref * 1.5:                         # 右下角有画面内容时梯度会误报，宁可退回经验值
        return 0, False, "自动量测 CUT=%d 明显偏离经验值 %d，疑似把画面内容当水印" % (cut, ref)
    return cut, True, "y0=%d band=%dpx peak=%d base=%d" % (h - band_h + y0, band, peak, base)


def fallback_cut(im):
    """自动量测没命中时的经验值。测不到 ≠ 没有水印，一律要裁。"""
    w, h = im.size
    known = {(1536, 1024): 80, (1408, 704): 70}
    if (w, h) in known:
        return known[(w, h)]
    return max(40, min(round(w / 19.5), int(h * 0.18), 110))


def residual_suspect(im):
    """裁后复测右下角是否还有文字状笔画（亮度突变到 250+）。

    对应 SKILL.md 里的人工验真「max 突变到 250+」，只作提示，不替人判。
    """
    w, h = im.size
    x0 = max(0, w - min(300, w // 3))
    box = im.crop((x0, max(0, h - 80), w, h)).convert("L")
    pw, ph = box.size
    px = box.load()
    hits = 0
    for y in range(1, ph - 1):
        for x in range(1, pw - 1):
            if px[x, y] >= 250 and (px[x - 1, y] < 200 or px[x + 1, y] < 200):
                hits += 1
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--crop-bottom", type=int, default=0, help="先裁掉底部像素（去水印）")
    ap.add_argument("--auto-crop", action="store_true",
                    help="自动量测水印上沿并裁底边；测不到时按尺寸经验值裁并打印 FALLBACK")
    ap.add_argument("--frame", action="store_true",
                    help="加留白边框。默认不加；仅用户明确要求「留白边 / 相框感」时传")
    ap.add_argument("--no-frame", action="store_true",
                    help="兼容旧调用：显式声明不加框（与默认行为一致）")
    ap.add_argument("--ratio", type=float, default=None,
                    help="目标宽高比，如 2.35 / 1；不加框时指图像本身，加框时指含框后的整体")
    ap.add_argument("--top-bias", type=float, default=0.72, help="按比例裁切时，从上方多裁的比重")
    ap.add_argument("--pad", type=float, default=0.06, help="外侧白边，短边比例；仅 --frame 时生效")
    ap.add_argument("--gap", type=int, default=11, help="图像到外沿的白隙 px；仅 --frame 时生效")
    ap.add_argument("--line", type=int, default=3, help="线框粗细 px，0=只留白边；仅 --frame 时生效")
    a = ap.parse_args()
    if a.auto_crop and a.crop_bottom:
        ap.error("--auto-crop 与 --crop-bottom 互斥：已知 CUT 用 --crop-bottom，否则用 --auto-crop")

    # 默认不加框：只有显式 --frame（且未被 --no-frame 否决）才加
    framed = a.frame and not a.no_frame
    pad_ratio, gap, line = (a.pad, a.gap, a.line) if framed else (0.0, 0, 0)

    im = Image.open(a.src).convert("RGB")
    ow, oh = im.size

    if a.auto_crop:
        cut, ok, detail = measure_watermark_cut(im)
        name = a.src.split("/")[-1]
        if ok:
            print("AUTO-CROP %s CUT=%d (%s)" % (name, cut, detail))
        else:
            cut = fallback_cut(im)
            print("FALLBACK %s 自动量测未命中（%s）；测不到 ≠ 没有水印，按经验值裁 CUT=%d"
                  % (name, detail, cut))
        im = im.crop((0, 0, im.size[0], im.size[1] - cut))
        hits = residual_suspect(im)
        print("VERIFY 右下角高亮突变=%d %s" % (
            hits,
            "SUSPECT → 请用放大刻度图 + max 突变 250+ 人工复测" if hits > 20
            else "未见明显残留，仍建议人工抽看"))
    elif a.crop_bottom:
        im = im.crop((0, 0, im.size[0], im.size[1] - a.crop_bottom))

    if a.ratio:
        im = fit_ratio(im, a.ratio, pad_ratio, gap, line, a.top_bias)

    out = add_frame(im, pad_ratio, gap, line) if framed else im
    out.save(a.dst)
    ratio = out.size[0] / out.size[1]
    print("%s %dx%d -> %s %dx%d  比例 %.4f  边框 %s" % (
        a.src.split("/")[-1], ow, oh, a.dst.split("/")[-1], out.size[0], out.size[1], ratio,
        ("有（pad %.3f / line %d）" % (pad_ratio, line)) if framed else "无"))


if __name__ == "__main__":
    main()
