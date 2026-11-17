#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""蓝标系列图示生成器（Blueprint Badge Series）

复刻 @user_43faedd6 账号 15 个 SkillHub skill 的统一图标语言：
  - 深藏青蓝图网格底 #0A1F3C，32px 细网格 / 128px 主网格
  - 亮青蓝 #49D0FF 圆角外框与线稿，白色 #FFFFFF 辅助线
  - 工程示意线稿、无渐变、无阴影；主图标无文字，图示可带中文标注

用法：
    python3 scripts/blueprint_icons.py            # 生成全部：icon.png + 4 张系列图示
    python3 scripts/blueprint_icons.py --check    # 只校验已有 PNG 尺寸/有效性

输出：
    <skill>/icon.png                             # 512x512，SkillHub 发布时自动提取为 iconUrl
    <skill>/assets/blueprints/icon-256.png       # 256x256 副本
    <skill>/assets/blueprints/01-oneclick-flow.png
    <skill>/assets/blueprints/02-config-layers.png
    <skill>/assets/blueprints/03-verify-boundary.png
    <skill>/assets/blueprints/04-troubleshoot.png

依赖：Pillow。字体自动探测 macOS / Linux / Windows 常见中文字体。
"""

from __future__ import annotations

import argparse
import glob
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# ── 色板（从线上 cad-file-reader 图标逐像素采样得到） ──────────────────
BG = (10, 31, 60)          # #0A1F3C 深藏青底
GRID = (21, 49, 85)        # 细网格
GRID_MAJOR = (28, 62, 101)  # 主网格
CYAN = (73, 208, 255)      # #49D0FF 亮青主色
CYAN_HI = (78, 223, 255)   # 高光
CYAN_DK = (55, 157, 207)   # 暗部/次级
WHITE = (255, 255, 255)
WHITE_DIM = (196, 214, 235)
LABEL = (120, 152, 190)

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
OUT = os.path.join(SKILL, "assets", "blueprints")

_FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "C:\\Windows\\Fonts\\msyh.ttc",
]
_LATIN_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def _pick(cands):
    for p in cands:
        if os.path.exists(p):
            return p
    return None


_FONT = _pick(_FONT_CANDIDATES)
_LATIN = _pick(_LATIN_CANDIDATES) or _FONT


def font(size: int, latin: bool = False):
    path = _LATIN if latin else _FONT
    if path:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


class BP:
    """超采样画布；所有绘制方法使用逻辑坐标，内部自动乘 scale。"""

    def __init__(self, w: int, h: int, scale: int = 2, grid: int = 32):
        self.w, self.h, self.s = w, h, scale
        self.im = Image.new("RGB", (w * scale, h * scale), BG)
        self.d = ImageDraw.Draw(self.im)
        self._grid(grid)

    def _grid(self, step):
        s = self.s
        for x in range(0, self.w + 1, step):
            major = x % (step * 4) == 0
            self.d.line((x * s, 0, x * s, self.h * s),
                        fill=GRID_MAJOR if major else GRID,
                        width=(2 if major else 1) * s)
        for y in range(0, self.h + 1, step):
            major = y % (step * 4) == 0
            self.d.line((0, y * s, self.w * s, y * s),
                        fill=GRID_MAJOR if major else GRID,
                        width=(2 if major else 1) * s)

    # 基础图元 ---------------------------------------------------------
    def box(self, xy, radius=0, outline=CYAN, width=3, fill=None):
        x0, y0, x1, y1 = [int(v * self.s) for v in xy]
        r = int(radius * self.s)
        w = max(1, int(width * self.s))
        self.d.rounded_rectangle((x0, y0, x1, y1), radius=r,
                                 outline=outline, width=w, fill=fill)

    def line(self, xy, fill=CYAN, width=3):
        pts = [(int(v * self.s)) for v in _flat(xy)]
        self.d.line(pts, fill=fill, width=max(1, int(width * self.s)), joint="curve")

    def circle(self, cx, cy, r, outline=CYAN, width=3, fill=None):
        s = self.s
        self.d.ellipse(((cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s),
                       outline=outline, width=max(1, int(width * s)), fill=fill)

    def dot(self, cx, cy, r, fill=CYAN):
        s = self.s
        self.d.ellipse(((cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s), fill=fill)

    def rect(self, xy, outline=CYAN, width=3, fill=None):
        x0, y0, x1, y1 = [int(v * self.s) for v in xy]
        self.d.rectangle((x0, y0, x1, y1), outline=outline,
                         width=max(1, int(width * self.s)), fill=fill)

    def text(self, xy, s, size=22, fill=WHITE, latin=False, anchor=None):
        self.d.text((xy[0] * self.s, xy[1] * self.s), s,
                    font=font(int(size * self.s), latin), fill=fill, anchor=anchor)

    def text_c(self, cx, y, s, size=22, fill=WHITE):
        """水平居中文字"""
        f = font(int(size * self.s))
        w = self.d.textlength(s, font=f)
        self.d.text((cx * self.s - w / 2, y * self.s), s, font=f, fill=fill)

    def dashed(self, xy, fill=CYAN_DK, width=2, dash=10, gap=7):
        (x0, y0), (x1, y1) = xy
        import math
        total = math.hypot(x1 - x0, y1 - y0)
        if total == 0:
            return
        ux, uy = (x1 - x0) / total, (y1 - y0) / total
        p = 0.0
        while p < total:
            q = min(p + dash, total)
            self.line((x0 + ux * p, y0 + uy * p, x0 + ux * q, y0 + uy * q), fill=fill, width=width)
            p = q + gap

    def arrow(self, xy, fill=CYAN, width=3, head=11):
        (x0, y0), (x1, y1) = xy
        self.line((x0, y0, x1, y1), fill=fill, width=width)
        import math
        a = math.atan2(y1 - y0, x1 - x0)
        for da in (2.6, -2.6):
            self.line((x1, y1,
                       x1 + head * math.cos(a + da),
                       y1 + head * math.sin(a + da)), fill=fill, width=width)

    def frame(self, title, subtitle="", tag="BLUEPRINT / KPA", h_pad=30):
        """统一的标题条 + 外框"""
        self.box((16, 16, self.w - 16, self.h - 16), radius=22, outline=CYAN, width=3)
        self.rect((h_pad, 34, h_pad + 6, 74), fill=CYAN, width=0)
        self.text((h_pad + 18, 36), title, size=26, fill=WHITE)
        if subtitle:
            self.text((h_pad + 18, 68), subtitle, size=15, fill=LABEL)
        self.text((self.w - h_pad, 42), tag, size=15, fill=CYAN_DK, latin=True, anchor="ra")

    def save(self, path, size=None):
        im = self.im
        if size:
            im = im.resize(size, Image.LANCZOS)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        im.save(path, optimize=True)
        print("  -> %s  %s  %d KB" % (os.path.relpath(path, SKILL), im.size,
                                      os.path.getsize(path) // 1024))


def _flat(xy):
    out = []
    for v in xy:
        if isinstance(v, (tuple, list)):
            out.extend(v)
        else:
            out.append(v)
    return out


# ── 主图标：掌机正面 + 屏幕封面墙 + 十字键 / ABXY + 终端推送 + 验收勾 ──
def make_icon():
    """与同系列一致：1 个主体（掌机工程线稿）+ 1 个角标（验收勾），大留白。"""
    c = BP(512, 512, scale=3, grid=32)
    c.box((22, 22, 490, 490), radius=58, outline=CYAN, width=8)

    # 左上：图纸标题栏式短横线（系列里 cad-file-reader / tujian 都有同类装饰）
    for y, ln in ((70, 54), (86, 38), (102, 26)):
        c.line((58, y, 58 + ln, y), fill=CYAN_DK, width=4)

    # 右上：验收通过圆标
    c.circle(432, 92, 30, outline=CYAN, width=5)
    c.line((417, 92, 428, 103, 448, 81), fill=CYAN_HI, width=6)

    # 掌机机身（主体，加大留白）
    c.box((58, 146, 454, 366), radius=34, outline=CYAN, width=7)
    # 屏幕
    c.box((140, 170, 372, 342), radius=10, outline=WHITE, width=5)
    # 屏幕内：左侧平台竖栏
    c.rect((152, 182, 188, 330), outline=CYAN_DK, width=3)
    for y in (206, 250, 294):
        c.line((160, y, 180, y), fill=CYAN_DK, width=4)
    # 屏幕内：2x2 封面墙（放大格子，避免缩略图糊成一片）
    for row, y in enumerate((190, 258)):
        for x in (198, 278):
            c.box((x, y, x + 62, y + 62), radius=5,
                  outline=CYAN if row == 0 else CYAN_DK, width=4)
            c.line((x + 10, y + 14, x + 50, y + 14), fill=CYAN_DK, width=3)
    # 左十字键
    c.box((88, 226, 110, 286), radius=6, outline=CYAN, width=5)
    c.box((70, 244, 128, 268), radius=6, outline=CYAN, width=5)
    # 右 ABXY
    for cx, cy in ((412, 230), (438, 256), (412, 282), (386, 256)):
        c.circle(cx, cy, 10, outline=CYAN_HI, width=4)
    # Select / Start 胶囊
    c.box((220, 350, 246, 358), radius=4, outline=WHITE_DIM, width=3)
    c.box((264, 350, 290, 358), radius=4, outline=WHITE_DIM, width=3)

    c.save(os.path.join(SKILL, "icon.png"), (512, 512))
    c.save(os.path.join(OUT, "icon-256.png"), (256, 256))


# ── 图示 01：一键安装 7 步流程 ──────────────────────────────────────
def make_flow():
    c = BP(1440, 620, scale=2, grid=32)
    c.frame("KPA 一键安装 · 7 步幂等流程",
            "每步可重复运行；任一步失败中止后，修复即可原样重跑，不会重复写入")
    steps = [
        ("01", "应用", "RetroArch\n天马 / PPSSPP"),
        ("02", "主题", "kpa-shelf\n封面墙 + 平台栏"),
        ("03", "配置", "RA 主配置\n竖版 per-game"),
        ("04", "货架", "metadata launch\n封面 / 简介"),
        ("05", "PSP", "PPSSPP 直启\n关虚拟键"),
        ("06", "清理", "垃圾 / 冗余\n只读清单优先"),
        ("07", "验收", "静态校验 +\n实机截图"),
    ]
    x0, gap, bw, by, bh = 44, 14, 178, 176, 216
    for i, (num, name, desc) in enumerate(steps):
        x = x0 + i * (bw + gap)
        c.box((x, by, x + bw, by + bh), radius=12, outline=CYAN if i in (0, 6) else CYAN_DK, width=3)
        c.circle(x + bw / 2, by + 42, 22, outline=CYAN, width=3)
        c.text_c(x + bw / 2, by + 30, num, size=20, fill=CYAN_HI)
        c.text_c(x + bw / 2, by + 80, name, size=24)
        for j, ln in enumerate(desc.split("\n")):
            c.text_c(x + bw / 2, by + 122 + j * 30, ln, size=16, fill=WHITE_DIM)
        if i < len(steps) - 1:
            c.arrow(((x + bw + 1, by + bh / 2), (x + bw + gap - 2, by + bh / 2)),
                    fill=CYAN_DK, width=2, head=7)
    c.box((44, 424, 1396, 574), radius=12, outline=CYAN_DK, width=2)
    c.text((66, 442), "护栏（违反过、已在实机踩坑）", size=20, fill=CYAN_HI)
    guards = [
        "改 metadata / 新增目录后必须删 dataCache.json 并重启天马",
        "按键只做单点验证再推广；adb 注入按键 RetroArch 全部不接收",
        "视觉类（封面 / 遮罩）必须实机截货架确认，静态引用 0 缺失不算修好",
        "删除 ROM / CHD 前先在本机留回滚点；设备删除无废纸篓",
    ]
    for i, g in enumerate(guards):
        col, row = i % 2, i // 2
        x, y = 66 + col * 670, 478 + row * 46
        c.dot(x + 6, y + 9, 4, CYAN)
        c.text((x + 20, y), g, size=16, fill=WHITE_DIM)
    c.save(os.path.join(OUT, "01-oneclick-flow.png"), (1440, 620))


# ── 图示 02：配置分层（哪些层能改） ────────────────────────────────
def make_layers():
    c = BP(1240, 760, scale=2, grid=32)
    c.frame("RetroArch 配置分层 · 改动落点速查",
            "越往下优先级越高；禁止用上层配置去覆盖下层已验证的 per-game 结果")
    layers = [
        ("全局", "retroarch.cfg", "输入 / 视频 / 性能总基线", "全局", CYAN_DK),
        ("核心级", "config/<核心>/<核心>.cfg", "遮罩、OSD、核心级按键", "核心内所有游戏", CYAN),
        ("单游戏", "config/<核心>/<游戏名>.cfg", "竖版方向、单游戏旋转", "仅该游戏", CYAN_HI),
        ("核心选项", "<核心>.opt", "CPS3 六键 / DOSBox 自动启动", "核心级", CYAN_DK),
        ("重映射", "config/remaps/<核心>/<游戏>.rmp", "PS ABXY 等单游戏键位", "仅该游戏", CYAN_DK),
    ]
    y = 128
    for name, path, usage, scope, col in layers:
        c.box((52, y, 806, y + 96), radius=10, outline=col, width=3)
        c.text((72, y + 14), name, size=22, fill=CYAN_HI)
        c.text((72, y + 48), path, size=18, fill=WHITE)  # 含 <核心> 中文，必须用中文字体
        c.text((470, y + 20), usage, size=17, fill=WHITE_DIM)
        c.text((470, y + 52), "作用域：" + scope, size=16, fill=LABEL)
        c.arrow(((816, y + 48), (866, y + 48)), fill=CYAN_DK, width=2, head=8)
        y += 108
    c.box((884, 128, 1188, 668), radius=10, outline=CYAN_DK, width=2)
    c.text((906, 148), "典型踩坑", size=22, fill=CYAN_HI)
    notes = [
        ("竖版方向", "只替换 4 行方向，保留 a/b/start/select"),
        ("遮罩不生效", "PICO 须独立主配置 + 改 launch"),
        ("CPS3 按键", "改 .opt 的 controls_p1=arcade"),
        ("N64 方向键", "正解是把 h0* 绑到左摇杆四轴"),
        ("OSD 弹窗", "逐 per-game 或核心级才生效"),
        ("整份覆盖", "云端与设备 ROM 数不匹配会丢游戏"),
    ]
    yy = 192
    for title, body in notes:
        c.dot(908, yy + 7, 4, CYAN)
        c.text((922, yy), title, size=17, fill=WHITE)
        lines = _wrap(body, 20)
        for k, ln in enumerate(lines):
            c.text((922, yy + 24 + k * 21), ln, size=14, fill=WHITE_DIM)
        yy += 24 + 21 * len(lines) + 10
    c.save(os.path.join(OUT, "02-config-layers.png"), (1240, 760))


# ── 图示 03：验收边界（自动 vs 人手） ───────────────────────────────
def make_boundary():
    c = BP(1240, 660, scale=2, grid=32)
    c.frame("验收边界 · adb 能证明什么 / 不能证明什么",
            "把「配置全绿」写成「已修好」是本项目最大的一次误判来源")
    c.box((52, 128, 610, 604), radius=12, outline=CYAN, width=3)
    c.box((630, 128, 1188, 604), radius=12, outline=CYAN_DK, width=3)
    c.text((76, 146), "adb 可自动验证", size=24, fill=CYAN_HI)
    c.text((654, 146), "必须人手实机确认", size=24, fill=WHITE)
    left = [
        "冷启动是否黑屏 / 崩溃（看 logcat SIGSEGV）",
        "配置是否被核心写回（改前后 md5 / grep）",
        "全库 ROM / 封面引用缺失数（静态校验）",
        "metadata 条目、sort-by 置顶、playlist 死引用",
        "封面文件是否存在、尺寸与图像内容分类",
        "启动时间线截图（如汉化版 60s 片头）",
        "dataCache.json 是否已清并重建",
    ]
    right = [
        "所有实体按键手感（RA 不接收注入按键）",
        "CPS1 / CPS3 / ATOMISWAVE 街机键位",
        "PPSSPP / PS ABXY 与方向键",
        "N64 十字键驱动摇杆后的实际手感",
        "DOSBox-Pure 核心菜单内的选项操作",
        "遮罩 / 封面在货架上的真实观感",
        "「部分游戏按键不对」的具体游戏名",
    ]
    for i, (a, b) in enumerate(zip(left, right)):
        y = 202 + i * 54
        c.dot(80, y + 8, 4, CYAN)
        c.text((96, y), a, size=16, fill=WHITE_DIM)
        c.dot(658, y + 8, 4, WHITE)
        c.text((674, y), b, size=16, fill=WHITE_DIM)
    c.dashed(((620, 180), (620, 580)), fill=CYAN_DK, width=2)
    c.save(os.path.join(OUT, "03-verify-boundary.png"), (1240, 660))


# ── 图示 04：排障决策树 ────────────────────────────────────────────
def make_troubleshoot():
    c = BP(1240, 760, scale=2, grid=32)
    c.frame("排障决策树 · 先判症状根因，再动手",
            "每条都来自一次实机误判：先按本图分流，可省掉整轮无效尝试")
    rows = [
        ("游戏打不开 / 黑屏", "先看 8–26s 时间线与 lastrun.log 停留时长",
         "长片头→写简介提示；SIGSEGV→二分定位包内条目；ZIP 伪装→解包换真 ROM"),
        ("封面不对 / 没有封面", "按图像内容分类，不要按尺寸一刀切",
         "粗色桶数 <20 才是占位卡；真盒绘原样恢复；最后实机截货架"),
        ("按键不对 / 方向反了", "先查配置层级与污染来源",
         "核心级 cfg 是否被竖版映射污染；.opt 是否 gamepad；N64 是否读摇杆"),
        ("要选 .exe / 弹窗", "找核心选项，不要尝试 adb 注入菜单",
         "DOSBox-Pure：dosbox_pure_conf=outside + 同名 .conf 的 [autoexec]"),
        ("改了没生效", "十有八九是缓存或落点层级错",
         "删 dataCache.json 重启天马；遮罩改主配置；OSD 改 per-game / 核心级"),
        ("CHD / 镜像黑屏", "换核心仍黑屏即判镜像数据问题",
         "进 BIOS CD 播放器显示 TRACK 00 = 无有效引导区，只能换源或删条目"),
    ]
    y = 128
    for sym, check, act in rows:
        c.box((52, y, 1188, y + 96), radius=10, outline=CYAN_DK, width=2)
        c.box((52, y, 262, y + 96), radius=10, outline=CYAN, width=3)
        c.text((70, y + 30), sym, size=19, fill=CYAN_HI)
        c.arrow(((270, y + 48), (306, y + 48)), fill=CYAN_DK, width=2, head=7)
        c.text((320, y + 18), "判定：" + check, size=17, fill=WHITE)
        c.text((320, y + 52), "动作：" + act, size=15, fill=WHITE_DIM)
        y += 100
    c.save(os.path.join(OUT, "04-troubleshoot.png"), (1240, 760))


def _wrap(s, n):
    return [s[i:i + n] for i in range(0, len(s), n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只校验已有 PNG")
    args = ap.parse_args()

    if args.check:
        paths = [os.path.join(SKILL, "icon.png")] + sorted(glob.glob(os.path.join(OUT, "*.png")))
        ok = 0
        for p in paths:
            try:
                im = Image.open(p)
                im.verify()
                print("OK  %-46s %s" % (os.path.relpath(p, SKILL), Image.open(p).size))
                ok += 1
            except Exception as e:
                print("ERR %s %s" % (p, e))
        print("校验通过 %d/%d" % (ok, len(paths)))
        return 0 if ok == len(paths) and ok else 1

    if not _FONT:
        print("WARN 未找到中文字体，图示文字可能显示为方块；可修改 _FONT_CANDIDATES", file=sys.stderr)
    print("生成蓝标系列图示（字体：%s）" % _FONT)
    make_icon()
    make_flow()
    make_layers()
    make_boundary()
    make_troubleshoot()
    return 0


if __name__ == "__main__":
    sys.exit(main())
