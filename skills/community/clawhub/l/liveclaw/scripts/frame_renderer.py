#!/usr/bin/env python3
"""
OpenClaw Agent Live — 纯 Pillow 帧渲染器
替代 tkinter Dashboard + Xvfb + FFmpeg 屏幕采集的整条链路。
直接在内存中用 Pillow 绘制 Dashboard 画面，输出 numpy RGB 数组供 PyAV 编码。

布局 (1920×1080):
  左侧 560px: 纯黑背景（浏览器端 avatar 会覆盖此区域）
  分隔线 1px
  右侧: 推理链路事件流（模拟 dashboard_v3 的样式）
"""
import json
import os
import re
import time
import datetime
import numpy as np
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise ImportError("Pillow is required: pip install Pillow")

try:
    from platform_utils import get_work_dir
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from platform_utils import get_work_dir

# ── 画面尺寸 ────────────────────────────────────────────────
WIDTH, HEIGHT = 1920, 1080
LEFT_W = 560         # 左侧虚拟形象区宽度
DIVIDER_X = LEFT_W   # 分隔线 X
RIGHT_X = LEFT_W + 1 # 右侧起始 X

# ── 颜色 (RGB) ───────────────────────────────────────────────
BG      = (8, 12, 20)
PANEL   = (13, 20, 33)
BORDER  = (26, 39, 68)
ACCENT  = (0, 212, 255)
GREEN   = (0, 255, 136)
YELLOW  = (255, 204, 0)
RED     = (255, 68, 68)
PURPLE  = (204, 136, 255)
DIMTEXT = (74, 96, 128)
TEXT    = (204, 232, 255)
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)

KIND_COLOR = {
    "task":   (0, 212, 255),  "think":  (255, 204, 0),  "tool":   (204, 136, 255),
    "exec":   (0, 255, 136),  "fetch":  (0, 212, 255),  "search": (34, 204, 204),
    "write":  (255, 136, 204), "memory": (255, 204, 0),  "result": (0, 255, 136),
    "error":  (255, 68, 68),  "stream": (0, 255, 136),  "info":   (74, 96, 128),
}
KIND_LABEL = {
    "task": "▶ TASK", "think": "◈ THINK", "tool": "⚡ TOOL", "exec": "⚙ EXEC",
    "fetch": "↓ FETCH", "search": "◎ SEARCH", "write": "✎ WRITE", "memory": "◈ MEM",
    "result": "✔ RESULT", "error": "✖ ERROR", "stream": "▶ STREAM", "info": "· INFO",
}
KIND_ICON = {
    "task": "▶", "think": "◈", "tool": "⚡", "exec": "⚙",
    "fetch": "↓", "search": "◎", "write": "✎", "memory": "◈",
    "result": "✔", "error": "✖", "stream": "▶", "info": "·",
}

# 需要用符号字体渲染的字符集（主 CJK 字体通常不含这些 Dingbats/Symbols）
_SYMBOL_CHARS = set("◈⚡⚙✎✔✖")

# ── Emoji 清洗 ────────────────────────────────────────────────
_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F9FF"
    "\U00002702-\U000027B0"
    "\U0000FE00-\U0000FE0F"
    "\U0000200D"
    "\U00002600-\U000026FF"
    "\U0001FA00-\U0001FAFF"
    "\U00010000-\U0001FFFF"
    "]+",
    flags=re.UNICODE
)

def _clean(text: str) -> str:
    if not text:
        return ""
    return _EMOJI_RE.sub("", text)


# ══════════════════════════════════════════════════════════════
#  FrameRenderer — 帧渲染器
# ══════════════════════════════════════════════════════════════

class FrameRenderer:
    """纯 Pillow 帧渲染器，直接输出 numpy RGB24 数组"""

    def __init__(self, font_path: str = None, logger=None):
        self._log = logger or (lambda msg, lvl="INFO": None)
        self._work_dir = get_work_dir()
        self._bus_file = self._work_dir / "agent_events.jsonl"

        # 事件缓存（增量读取）
        self._events_cache = []
        self._file_pos = 0
        self._file_size = 0

        # 打字机动画
        self._typewriter_queue = []
        self._typewriter_shown = ""
        self._last_typewriter_text = ""
        self._typewriter_color = ACCENT
        self._tick = 0

        # 帧缓存（仅在事件变化时重绘右侧）
        self._last_event_ts = ""
        self._cached_right_img = None

        # 加载字体
        self._load_fonts(font_path)

        # 预渲染静态元素
        self._bg_image = self._create_background()

        self._log("FrameRenderer initialized (Pillow-based, no Xvfb/tkinter/FFmpeg)")

    def _load_fonts(self, font_path: str = None):
        """加载双字体：CJK 主字体 + 符号字体（Dingbats/Symbols 回退）"""
        # ── 1. CJK 主字体（中文 + 基础拉丁） ──
        cjk_candidates = []
        if font_path:
            cjk_candidates.append(font_path)

        # 内嵌字体路径（如有）
        script_dir = Path(__file__).resolve().parent
        cjk_candidates.extend([
            str(script_dir.parent / "assets" / "fonts" / "NotoSansCJKsc-Regular.otf"),
            str(self._work_dir / "assets" / "fonts" / "NotoSansCJKsc-Regular.otf"),
        ])

        # 系统 CJK 字体（Linux apt 安装后的路径）
        cjk_candidates.extend([
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/System/Library/Fonts/PingFang.ttc",      # macOS
            "/System/Library/Fonts/STHeiti Light.ttc",  # macOS
            "C:\\Windows\\Fonts\\msyh.ttc",             # Windows
        ])

        cjk_file = None
        for c in cjk_candidates:
            if c and Path(c).exists():
                cjk_file = c
                break

        # ── 2. 符号字体（Dingbats: ◈⚡⚙✎✔✖ 等） ──
        symbol_candidates = [
            # 预置极小子集（DejaVu Sans 子集，仅含 KIND_ICON 符号，~3KB）
            str(script_dir.parent / "assets" / "fonts" / "Symbols.ttf"),
            str(self._work_dir / "assets" / "fonts" / "Symbols.ttf"),
            # 系统符号字体回退
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",            # fonts-dejavu
            "/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf",  # fonts-symbola (Debian/Ubuntu)
            "/usr/share/fonts/TTF/Symbola.ttf",                           # Arch
            "/usr/share/fonts/gdouros-symbola/Symbola.ttf",               # Fedora
            "/System/Library/Fonts/Menlo.ttc",                            # macOS
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",       # macOS
            "C:\\Windows\\Fonts\\seguisym.ttf",                           # Windows
        ]

        symbol_file = None
        for c in symbol_candidates:
            if c and Path(c).exists():
                symbol_file = c
                break

        # GitHub 回退：本地无 Symbols.ttf 时下载（仅 3KB）
        if symbol_file is None:
            _gh_symbol_url = "https://raw.githubusercontent.com/jerryang-cool/LiveClaw/main/assets/fonts/Symbols.ttf"
            _local_symbol = self._work_dir / "assets" / "fonts" / "Symbols.ttf"
            try:
                _local_symbol.parent.mkdir(parents=True, exist_ok=True)
                from urllib.request import urlretrieve
                urlretrieve(_gh_symbol_url, str(_local_symbol))
                symbol_file = str(_local_symbol)
                self._log(f"Symbol font downloaded from GitHub: {symbol_file}")
            except Exception as e:
                self._log(f"Symbol font download failed: {e}", "WARN")

        # ── 3. 构建字体对象 ──
        if cjk_file:
            self._log(f"CJK font loaded: {cjk_file}")
            self._font_sm = ImageFont.truetype(cjk_file, 13)
            self._font_md = ImageFont.truetype(cjk_file, 15)
            self._font_lg = ImageFont.truetype(cjk_file, 17)
            self._font_hdr = ImageFont.truetype(cjk_file, 13)
        else:
            self._log("No CJK font found, using default (Chinese may show as boxes)", "WARN")
            self._font_sm = ImageFont.load_default()
            self._font_md = ImageFont.load_default()
            self._font_lg = ImageFont.load_default()
            self._font_hdr = ImageFont.load_default()

        if symbol_file:
            self._log(f"Symbol font loaded: {symbol_file}")
            self._sym_sm = ImageFont.truetype(symbol_file, 13)
            self._sym_md = ImageFont.truetype(symbol_file, 15)
        else:
            self._log("No symbol font found, Dingbats may not render", "WARN")
            self._sym_sm = self._font_sm   # 回退到主字体
            self._sym_md = self._font_md

    def _create_background(self) -> Image.Image:
        """预渲染静态背景"""
        img = Image.new("RGB", (WIDTH, HEIGHT), BG)
        draw = ImageDraw.Draw(img)

        # 左侧纯黑区域
        draw.rectangle([0, 0, LEFT_W - 1, HEIGHT - 1], fill=BLACK)

        # 分隔线
        draw.line([(DIVIDER_X, 0), (DIVIDER_X, HEIGHT)], fill=BORDER, width=1)

        # 右侧 header
        draw.text((RIGHT_X + 12, 8), "▶ REASONING TRACE [ TASK → THINK → EXEC → RESULT ]",
                  font=self._font_hdr, fill=DIMTEXT)

        return img

    # ── 事件读取（增量）───────────────────────────────────────

    def _read_events(self, n=55):
        """增量读取 agent_events.jsonl"""
        try:
            if not self._bus_file.exists():
                return self._events_cache[-n:] if self._events_cache else []

            current_size = self._bus_file.stat().st_size
            if current_size < self._file_size:
                self._file_pos = 0
                self._events_cache = []
            self._file_size = current_size

            if current_size <= self._file_pos:
                return self._events_cache[-n:] if len(self._events_cache) > n else self._events_cache

            with open(self._bus_file, "r", encoding="utf-8") as f:
                f.seek(self._file_pos)
                new_lines = f.readlines()
                self._file_pos = f.tell()

            for line in new_lines:
                line = line.strip()
                if line:
                    try:
                        self._events_cache.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

            if len(self._events_cache) > 250:
                self._events_cache = self._events_cache[-200:]

            return self._events_cache[-n:] if len(self._events_cache) > n else self._events_cache
        except Exception:
            return self._events_cache[-n:] if self._events_cache else []

    # ── 文本换行辅助 ─────────────────────────────────────────

    def _wrap_text(self, text: str, font, max_width: int) -> list:
        """将文本按像素宽度换行"""
        if not text:
            return [""]
        lines = []
        current = ""
        for ch in text:
            test = current + ch
            bbox = font.getbbox(test)
            w = bbox[2] - bbox[0] if bbox else 0
            if w > max_width and current:
                lines.append(current)
                current = ch
            else:
                current = test
        if current:
            lines.append(current)
        return lines if lines else [""]

    # ── 核心渲染 ─────────────────────────────────────────────

    def render_frame(self) -> np.ndarray:
        """渲染一帧 Dashboard 画面，返回 numpy RGB24 数组 (H, W, 3)"""
        self._tick += 1

        # 读取事件
        events = self._read_events(55)

        # 检查是否有新事件（仅新事件到达时重绘右侧）
        latest_ts = events[-1].get("ts", "") if events else ""
        need_redraw = (latest_ts != self._last_event_ts) or (self._cached_right_img is None)

        if need_redraw:
            self._last_event_ts = latest_ts
            self._cached_right_img = self._render_right_panel(events)

        # 合成最终帧
        img = self._bg_image.copy()

        # 粘贴右侧面板
        if self._cached_right_img:
            img.paste(self._cached_right_img, (RIGHT_X, 30))

        # 更新打字机动画（每帧）
        if events:
            last = events[-1]
            txt = _clean(last.get("text", ""))[:60]
            kind = last.get("kind", "idle")
            color = KIND_COLOR.get(kind, ACCENT)
            if txt != self._last_typewriter_text:
                self._last_typewriter_text = txt
                self._typewriter_queue = list(txt)
                self._typewriter_shown = ""
                self._typewriter_color = color

        # 打字机逐字
        if self._typewriter_queue:
            chars = 2 if len(self._typewriter_queue) > 20 else 1
            for _ in range(chars):
                if self._typewriter_queue:
                    self._typewriter_shown += self._typewriter_queue.pop(0)

        # 在左侧下方绘制当前任务文字（打字机效果）
        draw = ImageDraw.Draw(img)
        cursor = "_" if self._tick % 6 < 3 else " "
        task_text = self._typewriter_shown + cursor
        if task_text.strip():
            # 在左侧底部显示当前任务
            draw.text((20, HEIGHT - 60), task_text, font=self._font_md,
                      fill=self._typewriter_color)

        return np.array(img)

    def _render_right_panel(self, events) -> Image.Image:
        """渲染右侧事件流面板（从底部向上，最新事件始终可见）"""
        panel_w = WIDTH - RIGHT_X
        panel_h = HEIGHT - 30  # 去掉 header 高度
        img = Image.new("RGB", (panel_w, panel_h), PANEL)
        draw = ImageDraw.Draw(img)

        if not events:
            draw.text((12, 20), "等待 Agent 事件...", font=self._font_md, fill=DIMTEXT)
            return img

        # 过滤直播系统通道事件
        filtered = []
        for ev in events:
            text = _clean(ev.get("text", ""))
            if any(kw in text for kw in ("启动直播", "直播已在运行", "直播已运行",
                                          "检查直播系统状态", "直播系统正在运行")):
                continue
            filtered.append(ev)

        if not filtered:
            return img

        # 预计算每个事件的行高（考虑文本换行）
        line_height = 22
        max_text_w = panel_w - 240
        event_heights = []
        for ev in filtered:
            text = _clean(ev.get("text", ""))
            wrapped = self._wrap_text(text, self._font_md, max_text_w)
            lines = min(len(wrapped), 2)  # 最多 2 行
            h = lines * line_height
            detail = _clean(ev.get("detail", ""))
            if detail:
                h += 0  # detail 不占额外行（叠加在最后一行下方）
            event_heights.append(h)

        # 从底部向上选取能显示的事件
        available_h = panel_h - 16  # 上下各留 8px
        display_indices = []
        total_h = 0
        for i in range(len(filtered) - 1, -1, -1):
            if total_h + event_heights[i] > available_h:
                break
            display_indices.insert(0, i)
            total_h += event_heights[i]

        # 从顶部开始绘制选中的事件
        y = 8
        for idx in display_indices:
            ev = filtered[idx]
            if y + line_height > panel_h - 8:
                break

            text = _clean(ev.get("text", ""))
            kind = ev.get("kind", "info")
            color = KIND_COLOR.get(kind, DIMTEXT)
            label = KIND_LABEL.get(kind, kind)

            # 时间戳
            try:
                ts = datetime.datetime.fromisoformat(ev.get("ts", "")).strftime("%H:%M:%S")
            except Exception:
                ts = "--:--:--"

            # 绘制一行: [时间] [标签] [图标] 内容
            x = 12
            draw.text((x, y), f" {ts} ", font=self._font_sm, fill=DIMTEXT)
            x += 80

            # 标签（符号+文字拆分渲染）
            icon = KIND_ICON.get(kind, "·")
            label_text = label[len(icon):].strip() if label.startswith(icon) else label
            sym_font = self._sym_sm if icon in _SYMBOL_CHARS else self._font_sm
            draw.text((x, y), f" {icon}", font=sym_font, fill=color)
            bbox = sym_font.getbbox(f" {icon}")
            x += (bbox[2] - bbox[0]) if bbox else 16
            draw.text((x, y), f" {label_text} ", font=self._font_sm, fill=color)
            x += 80

            # 图标
            sym_font2 = self._sym_sm if icon in _SYMBOL_CHARS else self._font_sm
            draw.text((x, y), f" {icon} ", font=sym_font2, fill=color)
            x += 30

            # 事件文本
            remaining_w = panel_w - x - 12
            wrapped = self._wrap_text(text, self._font_md, remaining_w)

            for i, line in enumerate(wrapped[:2]):
                draw.text((x, y), line, font=self._font_md, fill=color)
                y += line_height
                if i == 0 and len(wrapped) > 1:
                    pass
            if len(wrapped) <= 1:
                y += line_height

            # 详情
            detail = _clean(ev.get("detail", ""))
            if detail:
                draw.text((x, y - line_height + 14), f"  → {detail[:50]}",
                          font=self._font_sm, fill=DIMTEXT)

        return img


# ── 测试入口 ─────────────────────────────────────────────────
if __name__ == "__main__":
    renderer = FrameRenderer(logger=lambda msg, lvl="INFO": print(f"[{lvl}] {msg}"))

    # 渲染一帧并保存为 PNG 预览
    frame = renderer.render_frame()
    print(f"Frame shape: {frame.shape}, dtype: {frame.dtype}")

    img = Image.fromarray(frame)
    out_path = "/tmp/frame_preview.png"
    img.save(out_path)
    print(f"Preview saved: {out_path}")
