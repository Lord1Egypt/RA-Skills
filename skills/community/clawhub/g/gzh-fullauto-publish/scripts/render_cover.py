# -*- coding: utf-8 -*-
"""公众号封面渲染：一次出两张图（首图 900×383 + 方图 383×383）。

用法
----
    python render_cover.py --title "文章标题" --out-dir ./out
    python render_cover.py --title "文章标题" --tag "深度" --subtitle "副标题" --out-dir ./out
    python render_cover.py --master 母版1283x383.png --out-dir ./out

为什么不用 AI 文生图
--------------------
中文标题交给文生图模型必出乱码/缺笔画。正确做法是 HTML + 浏览器渲染叠字，
字体用本机系统字体（微软雅黑 / 思源黑体 / 苹方 / 思源等），本脚本会自动探测可用字体，
找不到会给出明确报错而不是悄悄渲染成方框。

两张图的分工
------------
- `cover_900x383.png`：订阅号首图（列表/正文头部，比例约 2.35:1）
- `cover_383x383.png`：1:1 方图（分享到朋友圈 / 群 / 搜一搜 / 公众号主页用的就是这张）
只用 900×383 一张，分享出去的卡片封面会被裁掉；900×500 是网页头图比例，进公众号同样会被裁。

兼容模式（--master）
--------------------
如果你手上已有 1283×383 的母版（左边 900 首图 + 右边 383 方图拼在一起），
用 `--master` 直接切两张，不叠字、不改色。

配色为硬约束：米白底 #FAF9F5、点睛琥珀金 #D4A853，文字暖黑 #141413 / 深咖 #3D3D3A / 暖灰 #73726C。
"""

import argparse
import os
import sys

W_FIRST, H_FIRST = 900, 383
W_SQUARE, H_SQUARE = 383, 383

BG = "#FAF9F5"
CREAM = "#F5E6D3"
GOLD = "#D4A853"
GOLD2 = "#B8925A"
SAND = "#E8DDD3"
INK = "#141413"
MUTED = "#73726C"

# 系统字体探测：文件路径 → 字体族名（不放任何用户目录写死的路径）
FONT_DIRS = []
for _env in ("WINDIR", "SystemRoot"):
    if os.environ.get(_env):
        FONT_DIRS.append(os.path.join(os.environ[_env], "Fonts"))
FONT_DIRS += [
    "/System/Library/Fonts",
    "/Library/Fonts",
    os.path.expanduser("~/.fonts") if os.environ.get("HOME") else "",
    "/usr/share/fonts/opentype/noto",
    "/usr/share/fonts/truetype",
    "/usr/share/fonts",
]

FONT_CANDIDATES = [
    ("msyh.ttc", "Microsoft YaHei", "regular"),
    ("msyhbd.ttc", "Microsoft YaHei", "bold"),
    ("msyhl.ttc", "Microsoft YaHei Light", "regular"),
    ("SourceHanSansSC-Regular.otf", "Source Han Sans SC", "regular"),
    ("SourceHanSansSC-Bold.otf", "Source Han Sans SC", "bold"),
    ("NotoSansSC-VF.ttf", "Noto Sans SC", "regular"),
    ("NotoSansSC-Regular.otf", "Noto Sans SC", "regular"),
    ("NotoSansSC-Bold.otf", "Noto Sans SC", "bold"),
    ("NotoSansCJK-Regular.ttc", "Noto Sans CJK SC", "regular"),
    ("NotoSansCJK-Bold.ttc", "Noto Sans CJK SC", "bold"),
    ("simhei.ttf", "SimHei", "regular"),
    ("PingFang.ttc", "PingFang SC", "regular"),
    ("Hiragino Sans GB.ttc", "Hiragino Sans GB", "regular"),
    ("wqy-zenhei.ttc", "WenQuanYi Zen Hei", "regular"),
]


def find_fonts(explicit_file=None, explicit_family=None):
    """返回 (regular_path, bold_path, family, 搜索过的目录清单)。"""
    searched = []
    reg = bold = family = None

    if explicit_file:
        if not os.path.isfile(explicit_file):
            raise SystemExit("错误：--font-file 指定的字体文件不存在：%s" % explicit_file)
        reg = explicit_file
        family = explicit_family or "GZHCoverFont"
        return reg, bold, family, searched

    for d in FONT_DIRS:
        if not d or not os.path.isdir(d):
            continue
        searched.append(d)
        for fn in os.listdir(d):
            low = fn.lower()
            for cand, fam, kind in FONT_CANDIDATES:
                if low == cand.lower():
                    path = os.path.join(d, fn)
                    if kind == "bold" and not bold:
                        bold = path
                    elif kind == "regular" and not reg:
                        reg, family = path, fam
        # 目录里顺手找找思源黑体这类带后缀的写法
        if not reg:
            for fn in os.listdir(d):
                low = fn.lower()
                if "sourcehansanssc" in low and ("regular" in low or "normal" in low):
                    reg, family = os.path.join(d, fn), "Source Han Sans SC"
                elif "sourcehansanssc" in low and "bold" in low and not bold:
                    bold = os.path.join(d, fn)
        if reg:
            break

    if not reg:
        raise SystemExit(
            "错误：没找到可用的中文字体，无法渲染中文标题。\n"
            "已搜索这些目录：\n  %s\n"
            "请任选一种方式解决：\n"
            "  1) 加参数 --font-file \"<字体文件完整路径>\"（推荐 .ttf/.otf/.ttc）\n"
            "  2) 安装任一中文字体（微软雅黑 / 思源黑体 / Noto Sans SC / 苹方）后重跑" % "\n  ".join(searched))
    return reg, bold, (explicit_family or family or "GZHCoverFont"), searched


def _face_css(reg, bold, family):
    reg_url = "file:///" + os.path.abspath(reg).replace("\\", "/")
    css = ["@font-face { font-family: 'GZHCoverFont'; font-weight: 400; src: url('%s'); }" % reg_url]
    if bold:
        bmd = "file:///" + os.path.abspath(bold).replace("\\", "/")
        css.append("@font-face { font-family: 'GZHCoverFont'; font-weight: 700; src: url('%s'); }" % bmd)
    css.append("@font-face { font-family: 'GZHCoverFont'; font-weight: 400; src: local('%s'); }" % family)
    return "\n".join(css)


def _esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


HEAD = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>
%(faces)s
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'GZHCoverFont', '%(family)s', 'Microsoft YaHei', 'PingFang SC',
       'Noto Sans CJK SC', sans-serif; -webkit-font-smoothing: antialiased; }
.canvas { background: %(bg)s; border-left: 10px solid %(gold)s; overflow: hidden; }
.kicker { display: inline-block; background: %(cream)s; color: %(gold2)s; font-weight: bold;
          letter-spacing: 3px; border-radius: 4px; }
#title { color: %(ink)s; font-weight: 700; letter-spacing: 1px; }
.rule { background: %(gold)s; border-radius: 2px; }
.sub { color: %(muted)s; letter-spacing: 1px; line-height: 1.5; }
.foot { color: %(muted)s; letter-spacing: 3px; border-top: 1px solid %(sand)s; padding-top: 10px; }
</style></head>
<body>
<div class="canvas" style="width:%(w)dpx;height:%(h)dpx;padding:%(pad)s;">
  %(kicker)s
  <div id="titlebox" style="height:%(tbh)dpx;padding-top:%(tbpt)dpx;overflow:hidden;">
    <div id="title" style="font-size:%(fs)dpx;line-height:1.28;">%(title)s</div>
  </div>
  <div class="rule" style="width:%(rw)dpx;height:3px;margin:%(rmt)dpx 0 %(rmb)dpx 0;"></div>
  <div class="sub" style="font-size:%(subfs)dpx;">%(sub)s</div>
  %(foot)s
</div>
</body></html>"""

AUTOFIT_JS = """() => {
  const box = document.getElementById('titlebox');
  const el = document.getElementById('title');
  const avail = box.clientHeight - parseFloat(getComputedStyle(box).paddingTop || '0');
  let size = parseFloat(getComputedStyle(el).fontSize);
  const min = %d;
  while (size > min && el.scrollHeight > avail) {
    size -= 2;
    el.style.fontSize = size + 'px';
  }
  return {size: size, height: el.scrollHeight, avail: avail};
}"""


def build_html(title, kicker, subtitle, foot, w, h):
    if w == W_FIRST:
        cfg = dict(pad="38px 46px", fs=46, tbh=188, tbpt=16, rw=130, rmt=16, rmb=14,
                   subfs=17, kfs=20, minfs=26, footfs=15)
    else:
        cfg = dict(pad="30px 32px", fs=34, tbh=196, tbpt=12, rw=96, rmt=14, rmb=12,
                   subfs=15, kfs=17, minfs=19, footfs=13)
    kicker_html = ('<div class="kicker" style="font-size:%dpx;padding:4px 12px;">%s</div>'
                   % (cfg["kfs"], _esc(kicker))) if kicker else ""
    foot_html = ('<div class="foot" style="font-size:%dpx;margin-top:14px;">%s</div>'
                 % (cfg["footfs"], _esc(foot))) if foot else ""
    return HEAD % dict(
        faces=_FACES, family=_FAMILY, bg=BG, gold=GOLD, cream=CREAM, gold2=GOLD2,
        ink=INK, muted=MUTED, sand=SAND,
        w=w, h=h, pad=cfg["pad"], tbh=cfg["tbh"], tbpt=cfg["tbpt"], fs=cfg["fs"],
        title=_esc(title), rw=cfg["rw"], rmt=cfg["rmt"], rmb=cfg["rmb"],
        subfs=cfg["subfs"], sub=_esc(subtitle), foot=foot_html, kicker=kicker_html,
    ), cfg["minfs"]


def render(out_dir, title, kicker, subtitle, foot, scale):
    from playwright.sync_api import sync_playwright

    os.makedirs(out_dir, exist_ok=True)
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        for (w, h, name) in ((W_FIRST, H_FIRST, "cover_900x383.png"),
                             (W_SQUARE, H_SQUARE, "cover_383x383.png")):
            html, minfs = build_html(title, kicker, subtitle, foot, w, h)
            tmp_html = os.path.join(out_dir, "_cover_%dx%d.html" % (w, h))
            with open(tmp_html, "w", encoding="utf-8") as f:
                f.write(html)
            page = browser.new_page(viewport={"width": w, "height": h},
                                    device_scale_factor=scale)
            page.goto("file:///" + os.path.abspath(tmp_html).replace("\\", "/"))
            page.evaluate("() => document.fonts ? document.fonts.ready.then(() => true) : true")
            info = page.evaluate(AUTOFIT_JS % minfs)
            out = os.path.join(out_dir, name)
            page.screenshot(path=out)
            page.close()
            os.remove(tmp_html)
            results.append((out, w, h, info))
        browser.close()
    return results


def crop_master(master, out_dir):
    from PIL import Image

    if not os.path.isfile(master):
        raise SystemExit("错误：找不到母版文件 %s" % master)
    im = Image.open(master)
    if im.width < W_SQUARE + 100 or im.height < 200:
        raise SystemExit("错误：母版尺寸 %dx%d 太小，无法切出封面。"
                         "母版应为 1283×383（左 900×383 首图 + 右 383×383 方图）。" % (im.width, im.height))
    os.makedirs(out_dir, exist_ok=True)
    first = os.path.join(out_dir, "cover_900x383.png")
    square = os.path.join(out_dir, "cover_383x383.png")
    im.crop((0, 0, W_FIRST, min(H_FIRST, im.height))).resize((W_FIRST, H_FIRST), Image.LANCZOS).save(first)
    right = im.crop((max(0, im.width - im.height), 0, im.width, im.height))
    right.resize((W_SQUARE, H_SQUARE), Image.LANCZOS).save(square)
    return [(first, W_FIRST, H_FIRST, None), (square, W_SQUARE, H_SQUARE, None)]


def main():
    ap = argparse.ArgumentParser(
        description="渲染公众号封面两张图（首图 900×383 + 方图 383×383）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--title", help="封面标题文字")
    ap.add_argument("--tag", default="", help="左上角小标签，如「深度」「实测」")
    ap.add_argument("--subtitle", default="", help="标题下方的补充一行")
    ap.add_argument("--brand", default="", help="底部署名（默认不显示，避免替使用者打广告）")
    ap.add_argument("--out-dir", default="./out", help="输出目录（默认 ./out）")
    ap.add_argument("--master", help="兼容模式：给一张 1283×383 母版，直接切成两张")
    ap.add_argument("--font-file", help="指定中文字体文件（默认自动探测系统字体）")
    ap.add_argument("--font-family", help="指定字体族名（配合 --font-file 使用）")
    ap.add_argument("--device-scale", type=float, default=1.0, help="渲染倍率，默认 1（长图/超高页面不要调高）")
    args = ap.parse_args()

    global _FACES, _FAMILY

    if args.master:
        if args.title:
            print("提示：使用 --master 兼容模式时直接切母版，不叠加文字。")
        outs = crop_master(args.master, args.out_dir)
        for path, w, h, _ in outs:
            print("COVER_OK %s %dx%d" % (path, w, h))
        print("共输出 %d 张封面（切自母版 %s）" % (len(outs), args.master))
        return 0

    if not args.title:
        raise SystemExit("错误：缺少 --title（封面标题）。")

    reg, bold, family, _searched = find_fonts(args.font_file, args.font_family)
    _FACES = _face_css(reg, bold, family)
    _FAMILY = family
    print("使用字体：%s（%s）" % (family, reg))

    outs = render(args.out_dir, args.title, args.tag, args.subtitle, args.brand, args.device_scale)

    from PIL import Image

    ok = True
    for path, w, h, info in outs:
        with Image.open(path) as im:
            real = "%dx%d" % (im.width, im.height)
        good = (im.width == w and im.height == h)
        ok = ok and good
        print("COVER_OK %s 期望 %dx%d 实际 %s%s" % (
            path, w, h, real, "" if good else "  ← 尺寸不符！"))
        if info:
            print("          标题字号 %.0fpx，占高 %d/%d px" % (info["size"], info["height"], info["avail"]))
    print("两张封面已渲染到：%s" % os.path.abspath(args.out_dir))
    return 0 if ok else 1


_FACES = ""
_FAMILY = ""

if __name__ == "__main__":
    sys.exit(main())
