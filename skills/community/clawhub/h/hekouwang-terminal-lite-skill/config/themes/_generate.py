#!/usr/bin/env python3
# ============================================================
# hekouwang-terminal-skill — 主题生成器（唯一真相源）
# 用法: python3 _generate.py   （在 config/themes/ 目录下跑）
#
# 一份色板 → 一整条工具链的配色。改色只改 palettes/*.py，重跑本脚本，
# 别手改任何生成出来的文件（下次重跑就没了）。
#
# 产物：
#   <name>.json    iTerm2 Dynamic Profile（保存即生效）
#
# 付费包在时，generators/pro.py 会接管并多出一批产物（多终端与整条工具链的配色）；
# 那批产物的文件格式与各 App 的口径写在付费包自己的文档里，本文件不重复。
#
# 不生成 starship：starship 的 style 用的是 ANSI 色名（blue / purple / bright-black），
# 天然跟随终端调色板换肤，生成 hex 反而把它钉死。这是设计选择，不是漏了。
# ============================================================
import glob
import json
import os
import re
import shutil
import plistlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "lib"))
from palettes import load, default_theme, BRAND_THEMES, ADJUSTMENTS  # noqa: E402
from palettes import _audit as palette_audit  # noqa: E402
from i18n import t  # noqa: E402

# ⚠️ 不在 import 期加载色板：开源版根本没有 palettes/ 里的色板文件，
#    在这里 sys.exit 会让开源版直接跑不起来。改成 main() 里按需加载。
GUID = "catppuccin-mocha-dynamic-2026"  # 历史遗留命名，现作所有主题的共享稳定 Guid

# ---- 字体 --------------------------------------------------
# Maple Mono NF CN（SIL OFL-1.1，免费可商用可分发）：等宽 + 内置 Nerd Font 图标 + 中文等宽，
# 一套顶过去「主字体 + Symbols Nerd Font 兜底」两套。
# ⚠️ PostScript 名不是猜的，是从字体文件的 name 表读出来的（family = Maple Mono NF CN）；
#    写错时 iTerm2 会静默回退到系统字体，肉眼不一定看得出来 —— doctor.sh 第 2 节会验。
# 想换成自己买过授权的商业字体（如 Operator Mono）：改这两行，重跑本脚本再 ./scripts/theme.sh。
NORMAL_FONT = "MapleMono-NF-CN-Regular 15"
SYMBOL_FONT = "SymbolsNFM 15"   # 图标兜底；Maple NF 已自带图标，这层是双保险
COLUMNS = 180   # 新窗口默认列数
ROWS = 46       # 新窗口默认行数

# ---- 质感层（毛玻璃 / 光标）------------------------------------
# TRANSPARENCY 是唯一需要按口味调的旋钮：
#   0     = 完全不透（录屏最干净，桌面绝不入镜）
#   0.08  = 默认，一点空气感，桌面被 BLUR_RADIUS 糊成色块认不出内容
#   >0.15 = 开始影响可读性，且录屏时背后画面会跟着动，不建议
TRANSPARENCY = 0.08
BLUR_RADIUS = 20    # 有效范围 0–30，越大背后越糊
CURSOR_VERTICAL_BAR = 1   # iTerm2 光标形态：0=下划线 1=竖条 2=方块

# 标签栏染色：Minimal 主题下整条顶栏跟着 Tab Color 走（截图里最上面那一条）。
# 品牌原色直接上去太喊，兑进底色只留一丝暖调 —— 一眼认得出是哪套主题，又不抢正文。
# 0 = 关掉染色（顶栏＝底色）。关掉时这个键**仍然会写**，免得沿用缓存里的旧颜色。
# 标题栏染色比例。**默认 0 = 标题栏与背景同色**，整窗一块画布。
# ⛔ 别改回非 0：那样标题栏取的是「光标色掺进背景」，而**光标色是任意的** ——
#    品牌四套的光标是品牌色，掺出来好看；但导入的社区主题（./scripts/import.sh）光标什么颜色都有，
#    实测 adventure-time 背景 #1f1d45（深紫）+ 光标 #efbf38（金黄）→ 标题栏 #443a43（褐灰），
#    跟窗体明显不是一家。而 SKILL 第一句写的就是「Minimal 主题，整窗一块画布」。
#    另：社区三套的染色彩度本来只有 0.07–0.15（肉眼看不出），改成 0 它们什么也没损失。
TAB_TINT = 0.0

# ---- 状态栏：默认关 ------------------------------------------
# 2026-07-16 实测后关掉：CPU/内存/网速/电池/时钟这些 macOS 菜单栏已有，
# 目录/分支/耗时 starship 已有 —— 状态栏夹在中间两头不靠，只占一行高度。
# 布局结构本身是验证过能跑的（见 status_bar()），想复活改这里即可。
SHOW_STATUS_BAR = False


# ============================================================
# 色值工具
# ============================================================
def col(hex6, alpha=1.0):
    r = int(hex6[0:2], 16) / 255
    g = int(hex6[2:4], 16) / 255
    b = int(hex6[4:6], 16) / 255
    return {"Color Space": "sRGB", "Red Component": r, "Green Component": g,
            "Blue Component": b, "Alpha Component": alpha}


def rgb(hex6):
    return tuple(int(hex6[i:i + 2], 16) for i in (0, 2, 4))


def mix(hex_a, hex_b, t):
    """把 a 按比例 t 混进 b（t=0 全是 b，t=1 全是 a）。用来调 diff 底色这类淡色块。"""
    a, b = rgb(hex_a), rgb(hex_b)
    return "".join(f"{round(a[i] * t + b[i] * (1 - t)):02x}" for i in range(3))


def truecolor(hex6, bold=False):
    """LS_COLORS / EZA_COLORS 用的 24 位色转义码。"""
    r, g, b = rgb(hex6)
    return f"{'1;' if bold else ''}38;2;{r};{g};{b}"


# ============================================================
# iTerm2 Dynamic Profile —— 开源版：Minimal 骨架
#
# 开源版给的是**窗口形态**：Minimal 主题配套的那套结构（无标题栏/无边框/无滚动条、
# 窗口尺寸、无限回滚、静音、字体），**不含任何配色**，用 iTerm2 自己的默认色。
#
# 配色、质感层（毛玻璃/透明度/光标）、Triggers（日志标色/密码管理器）、状态栏
# 由付费包的 generators/pro.py 接管 —— 它在时会把这些键合并进同一个 Profile。
# 这么切是有意的，划线口径 = **能力**：
#   开源版 = 一台配好的 iTerm2（窗口形态 + 完整配色 + Triggers + 键映射）
#   付费版 = 同一份色板走出 iTerm2（多终端 + 整条工具链）
# ⛔ 2026-07-23 修正过一次：以前是「脚本全开源、只门控配置内容」，结果免费仓里
#    躺着多终端同步的完整实现，别人补几个生成器就复刻了。现在付费能力的**实现**
#    也在付费包里，免费仓只留广告位 + exec。
# ============================================================
def build_minimal():
    """无配色的 Minimal 骨架。付费模块在时，pro.py 会往里合并配色与质感层。"""
    return {
        "Name": "会勇禾口王 · Minimal",
        "Guid": GUID,
        "Normal Font": NORMAL_FONT,
        "Non Ascii Font": SYMBOL_FONT,
        "Use Non-ASCII Font": True,
        "ASCII Anti Aliased": True,
        "Non-ASCII Anti Aliased": True,
        "Use Bold Font": True,
        "Use Italic Font": True,
        "Thin Strokes": 1,
        "Unicode Version": 9,
        "Horizontal Spacing": 1,
        "Vertical Spacing": 1.05,
        "Columns": COLUMNS,
        "Rows": ROWS,
        "Unlimited Scrollback": True,
        "Scrollback Lines": 0,
        "Silence Bell": True,
        "Window Type": 0,
        # ⚠️ 必须显式声明为空：Dynamic Profile 只覆盖 JSON 里出现过的键，
        # 没声明的键会沿用 iTerm2 缓存(New Bookmarks)里的旧值。
        # 2026-07-16 实测：某次 GUI 手滑把路径粘进「Send text at start」，
        # 导致每开一个 tab 都被自动敲一行 cd，换肤/重装都清不掉——就是因为没声明这个键。
        "Initial Text": "",
        "Rewritable": True,
        "Use Separate Colors for Light and Dark Mode": False,
    }


# ============================================================
# iTerm2 Dynamic Profile —— 完整主题（开源版就有）
# ============================================================
def triggers(p):
    """随 Profile 默认交付的 Triggers（配置即代码，不用手点 GUI）。
    Highlight 用 Dynamic Profile 专用的 {#前景,#背景} 简写（官方文档），
    配色取当前主题，所以换肤时标注色自动跟着变。
    action 标识符即 iTerm2 的 trigger 类名：HighlightTrigger / PasswordTrigger。
    partial=True 即 GUI 里的 Instant（不等换行就触发；密码提示没有换行，必须 Instant）。
    （不做"完成弹通知"：macOS 真实通知版式固定、删不掉"A trigger fired…"那行，
      terminal-notifier 也不好看，故不收录。）"""
    surf = palette_audit.surface_set(p)
    return [
        # 日志错误词 → 语义错误表面（只标匹配到的词，不整行）
        {"regex": r"\b(ERROR|ERRORS|FATAL|FAILED|FAILURE|PANIC|Exception)\b",
         "action": "HighlightTrigger",
         "parameter": f"{{#{surf['error_fg']},#{surf['error_bg']}}}", "partial": True},
        # 警告词 → 语义警告表面
        {"regex": r"\b(WARN|WARNING|DEPRECATED|TODO|FIXME)\b",
         "action": "HighlightTrigger",
         "parameter": f"{{#{surf['warn_fg']},#{surf['warn_bg']}}}", "partial": True},
        # 成功词 → 语义成功表面
        {"regex": r"\b(SUCCESS|SUCCEEDED|SUCCESSFUL|PASSED)\b",
         "action": "HighlightTrigger",
         "parameter": f"{{#{surf['success_fg']},#{surf['success_bg']}}}", "partial": True},
        # 密码提示 → 自动弹密码管理器（Instant：提示行没有换行）
        {"regex": r"(^|\s)([Pp]assword|[Pp]assphrase|[Ss]udo password)( for [^:]+)?:\s*$",
         "action": "PasswordTrigger", "parameter": "", "partial": True},
    ]


# ContextMenuActions 数值（iTerm2 ContextMenuActionPrefsController.h）——
# Dynamic Profile 的 actions[].action 必须是这个整数，不是类名字符串。
_OPEN_FILE = 0
_OPEN_URL = 1
_RUN_CMD = 2
_COPY = 6


def _ss_action(title, action, parameter=""):
    return {"title": title, "action": action, "parameter": parameter}


def smart_selection_rules():
    """语义交互层 v1 · Smart Selection 规则包。

    Dynamic Profile 一旦写了 `Smart Selection Rules` 就**整表替换**继承值，
    所以必须自带 iTerm2 出厂那一组（Paths / HTTP URL …），再叠我们的产品规则。
    Cmd-click 走匹配规则的**第一条** action；右键菜单列出全部。

    产品规则（高/极高精度，压过泛 Paths）：
      · path:line[:col] → 交给 Semantic History / 打开文件
      · Git SHA → git show（失败时仍可 Copy）
      · localhost / 127.0.0.1:port → 浏览器打开
    """
    # 出厂规则：字面抄自 /Applications/iTerm.app/.../SmartSelectionRules.plist
    stock = [
        {"notes": "Word bounded by whitespace",
         "regex": r"\S+", "precision": "low"},
        {"notes": "C++ namespace::identifier",
         "regex": r"([a-zA-Z0-9_]+::)+[a-zA-Z0-9_]+", "precision": "normal"},
        {"notes": "Paths",
         "regex": r"\~?/?([[:letter:][:number:]._-]+/+)+[[:letter:][:number:]._-]+/?",
         "precision": "normal",
         "actions": [_ss_action("Open Path", _OPEN_FILE, r"\0")]},
        {"notes": "Quoted string",
         "regex": r'@?"(?:[^"\\]|\\.)*"', "precision": "normal"},
        {"notes": "Java/Python include paths",
         "regex": r"([[:letter:][:number:]._]+\.)+[[:letter:][:number:]._]+",
         "precision": "normal"},
        {"notes": "mailto URL",
         "regex": r"\bmailto:([a-z0-9A-Z_]+@)?([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\b",
         "precision": "normal"},
        {"notes": "Obj-C selector",
         "regex": r"@selector\([^)]+\)", "precision": "high"},
        {"notes": "email address",
         "regex": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b",
         "precision": "high"},
        {"notes": "HTTP URL",
         "regex": (
             r"((?<!\()https?://([a-z0-9A-Z]+(:[a-zA-Z0-9]+)?@)?([a-z0-9A-Z][-a-z0-9A-Z]*\.)*"
             r"[A-Za-z][-A-Za-z]*((:[0-9]+)?)(/[a-zA-Z0-9;/\.\-_+%?&@=#~()]*)?)"
             r"|(https?://([a-z0-9A-Z]+(:[a-zA-Z0-9]+)?@)?([a-z0-9A-Z][-a-z0-9A-Z]*\.)*"
             r"[A-Za-z][-A-Za-z]*((:[0-9]+)?)(/[a-zA-Z0-9;/\.\-_+%?&@=#~(]*)?)"
         ),
         "precision": "very_high",
         "actions": [_ss_action("Open URL", _OPEN_URL, r"\0")]},
        {"notes": "SSH URL",
         "regex": r"\bssh:([a-z0-9A-Z_]+@)?([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\b",
         "precision": "very_high"},
        {"notes": "Telnet URL",
         "regex": r"\btelnet:([a-z0-9A-Z_]+@)?([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\b",
         "precision": "very_high"},
    ]
    # 产品规则放前面：同位置多规则时更高 precision 优先；并列时列表靠前更直观
    ours = [
        {"notes": "hekouwang · path:line[:col]",
         "regex": (
             r"(?:~|/|\./|\.\./)?(?:[[:alnum:]._+-]+/)*[[:alnum:]._+-]+\."
             r"[[:alnum:]]+:[0-9]+(?::[0-9]+)?"
         ),
         "precision": "very_high",
         "actions": [
             # Semantic History 认 path:line；Open File 参数带 :line 时多数编辑器也能吃
             _ss_action("Open at line", _OPEN_FILE, r"\0"),
             _ss_action("Copy path:line", _COPY, r"\0"),
         ]},
        {"notes": "hekouwang · Git SHA",
         "regex": r"\b[0-9a-f]{7,40}\b",
         "precision": "high",
         "actions": [
             _ss_action("git show", _RUN_CMD, r"git -C '\d' show --stat \0"),
             _ss_action("Copy SHA", _COPY, r"\0"),
         ]},
        {"notes": "hekouwang · localhost port",
         "regex": r"\b(?:localhost|127\.0\.0\.1):(3[0-9]{3}|4[0-9]{3}|5[0-9]{3}|8[0-9]{3}|9[0-9]{3})\b",
         "precision": "very_high",
         "actions": [
             _ss_action("Open in browser", _OPEN_URL, r"http://\0"),
             _ss_action("Copy host:port", _COPY, r"\0"),
         ]},
    ]
    return ours + stock


def semantic_history():
    """Cmd-click 打开文件：交给本机「最好的编辑器」（Cursor / VS Code / …）。

    action 取值见 iTermSemanticHistoryPrefsController.m：
      best editor / editor / url / command / raw command / …
    远程路径打不开时 iTerm2 自己降级提示，我们不另做静默开错文件的逻辑。
    """
    return {
        "action": "best editor",
        "editor": "",
        "text": "",
    }


def status_bar(p):
    """底部状态栏（配置即代码，不用手点 GUI）。

    选组件的原则：**只放 starship 没有的**。
    starship 已经显示目录 / git 分支 / git 状态 / 命令耗时，
    所以这里一律不放这些，只补 starship 天生给不了的机器级读数：
    CPU、内存、网速、电池、时钟。两者零重复。

    结构键名全部来自 iTerm2 二进制里的符号，不是猜的；但整体嵌套形态属推断，
    首次部署后需新开 tab 肉眼确认（静默忽略是这块最典型的失败形态）。
    """
    text = col(p["fg"])

    def comp(cls, knobs=None, priority=5):
        k = {"base: priority": priority,
             "base: compression resistance": 1,
             "shared text color": text}
        if knobs:
            k.update(knobs)
        return {"class": cls, "configuration": {"knobs": k}}

    return {
        "advanced configuration": {"remove empty components": True},
        "components": [
            comp("iTermStatusBarCPUUtilizationComponent"),
            comp("iTermStatusBarMemoryUtilizationComponent"),
            comp("iTermStatusBarNetworkUtilizationComponent"),
            # Spring = 弹簧，把后面的组件顶到最右边；优先级最低，空间不够时先被挤掉
            comp("iTermStatusBarSpringComponent", priority=1),
            comp("iTermStatusBarBatteryComponent"),
            comp("iTermStatusBarClockComponent", knobs={"format": "HH:mm"}),
        ],
    }


def build(p, theme_name):
    """完整的 iTerm2 Profile：Minimal 骨架 + 配色 + 质感层 + Triggers + 状态栏。

    这一整层都在开源版里 —— 免费版就该有一个真正配好看的终端，
    否则它不值得被截图分享，也就当不成付费版的广告。
    付费版加的是「让这份色板走出 iTerm2」那部分，见 generators/pro.py。
    """
    prof = dict(build_minimal())
    prof.update({
        "Name": p["display"],
        # ---- 质感层 ----
        # "Only The Default BG Color Uses Transparency" 是这组的关键：
        # 只让默认背景色透，文字与带色格子（选中区/Trigger 高亮/ls 图标）保持不透明，
        # 所以开了透明也不掉可读性——录屏尤其重要。
        "Transparency": TRANSPARENCY,
        "Initial Use Transparency": True,
        "Only The Default BG Color Uses Transparency": True,
        "Blur": True,
        "Blur Radius": BLUR_RADIUS,
        "Cursor Type": CURSOR_VERTICAL_BAR,
        "Blinking Cursor": False,   # 录屏时闪烁光标会在剪辑抽帧里忽明忽暗
        "Use Cursor Guide": True,
        "Background Color": col(p["bg"]),
        "Foreground Color": col(p["fg"]),
        "Bold Color": col(p.get("bold", p["fg"])),
        "Cursor Color": col(p["cursor"]),
        "Cursor Text Color": col(
            p["fg"] if palette_audit.contrast(p["fg"], p["cursor"])
            >= palette_audit.contrast(p["bg"], p["cursor"]) else p["bg"]),
        "Cursor Guide Color": col(palette_audit.neutral_ramp(p)["border"], 0.65),
        "Selection Color": col(p["selbg"]),
        "Selected Text Color": col(p["selfg"]),
        "Link Color": col(p["ansi"][4]),
        # ---- 剩下那半打色槽 ----
        # 免费主题一般只填 bg/fg/cursor + 16 个 ANSI 就收工，剩下这些留给 iTerm2 默认值 ——
        # 于是查找命中是出厂黄、下划线是出厂蓝、徽章是出厂红，跟辛苦推出来的色板全不搭。
        # 一套主题要显得"整"，靠的就是这几个平时看不见、一用就露馅的地方。
        #
        # ⚠️ 而且这里每一个都必须**显式写出来**：Dynamic Profile 只覆盖 JSON 里出现过的键，
        #    没写的会沿用 iTerm2 缓存里的旧值（同 "Initial Text" 那条教训）。
        #    Minimum Contrast 尤其危险 —— 它一旦是个非零旧值，iTerm2 会**擅自改写**
        #    我们按 WCAG 反解出来的每一个颜色，色板全白推。
        "Underline Color": col(p["ansi"][4]),        # 下划线跟链接同色
        "Use Underline Color": True,
        "Badge Color": col(p["cursor"], 0.30),       # 项目徽章：品牌色的淡水印，不抢正文
        # 查找命中：保持主题黄的色相，解一个同时满足「对背景可见、对正文可读」
        # 的明度。旧配方固定 45% 混底色，暗底会吃掉浅色字、亮底又浅到看不见。
        "Match Background Color": col(
            p.get("matchbg") or palette_audit.solve_match(p["bg"], p["fg"], p["ansi"][3])),
        "Minimum Contrast": 0,      # 别让 iTerm2 替我们"修"颜色
        "Cursor Boost": 0,          # 非零会把除光标外的一切压暗
        "Smart Cursor Color": False,  # 我们已经显式给了 Cursor Text Color
        "Brighten Bold Text": True,   # 粗体走 bright 行（ls 的目录、git diff 的强调靠它）
        # SGR 2（暗字）的不透明度。theme.sh / starship 的右栏大量用暗字，
        # 出厂 0.5 在暗底上偏糊，抬到 0.55 刚好还是"余光信息"但读得清。
        "Faint Text Alpha": p.get("faint_text_alpha", 0.55),
        "Use Tab Color": True,
        "Tab Color": col(mix(p["cursor"], p["bg"], TAB_TINT) if TAB_TINT else p["bg"]),
        "Triggers": triggers(p),
        # ---- 语义交互层 v1（两档都有，同 Triggers）----
        # Smart Selection：quad-click / Cmd-click / 右键动作；必须自带出厂规则，见 smart_selection_rules()。
        # Semantic History：Cmd-click 路径交给本机最佳编辑器（Cursor / VS Code …）。
        "Smart Selection Rules": smart_selection_rules(),
        "Smart Selection Actions Use Interpolated Strings": False,
        "Semantic History": semantic_history(),
        # ---- 功能层：状态栏（默认关，见 SHOW_STATUS_BAR 注释）----
        # 位置（顶/底）是全局设置，不在 Profile 里，见 setup-gui.sh 的 StatusBarPosition。
        "Show Status Bar": SHOW_STATUS_BAR,
        "Status Bar Layout": status_bar(p),
    })
    for i, c in enumerate(p["ansi"]):
        prof[f"Ansi {i} Color"] = col(c)
    # 返回**裸 profile**，跟 build_minimal() 保持同一形状；
    # 外面那层 {"Profiles": [...]} 由调用方包，别在这里重复包（踩过一次，出来是双层嵌套）。
    return prof


# ============================================================
# 出片
# ============================================================
# 开源版到这里为止：一份色板 → iTerm2 的 Dynamic Profile。
# 多终端（Ghostty / Warp / macOS 自带终端）与生态配色（bat / fzf / eza /
# git diff / tmux / VS Code）的生成器在付费包的 generators/pro.py 里。
# 它不在 → 只出 iTerm2，不报错、不留半成品。
from generators import load_pro  # noqa: E402


def write(path, content, mode="w"):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    kwargs = {} if "b" in mode else {"encoding": "utf-8"}
    with open(path, mode, **kwargs) as f:
        f.write(content)


def sweep(palettes, pro):
    """清掉「色板已经没了、产物还赖着」的旧文件。

    为什么必须有：生成器只写不删。移掉一套色板（改 palettes/*.py、或
    ./scripts/import.sh --remove）之后，它的 json / ghostty / warp / ecosystem 会**永远留着** ——
    ./scripts/theme.sh 的列表里还看得见它、还能切过去，切完发现工具链配色对不上（那半边没更新）。
    导入功能上线后这个会很常见：随手导十套试试，再想清掉就一地垃圾。

    ⛔ 三条安全线（这是个删文件的函数，写之前先划好边界）：
      1. **只删严格匹配我们命名规律的东西**，别拿"目录下所有文件"当集合
      2. **pro 没加载时一个字节都不碰** ghostty/warp/ecosystem —— 开源版本来就不生成它们，
         去删只会把用户刚解压进来的付费件误伤掉（买家装付费包的中间态就是这样）
      3. 只删文件和 ecosystem/<主题>/ 这一层目录，**绝不递归删父目录**；
         ecosystem/vscode 是共享目录，永远跳过
    """
    keep = set(palettes)
    removed = []

    def rm(path, why):
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)
        else:
            return
        removed.append(why)

    # iTerm2 主题 JSON：<名字>.json。⚠️ 目录里还有 minimal.json 这种非色板产物，
    # 所以判据是「文件名去掉 .json 之后不在色板里，且它确实曾是一套主题」——
    # 用 ghostty/ecosystem 里有没有同名兄弟来佐证，避免误删无关 json。
    for f in glob.glob("*.json"):
        name = f[:-5]
        # names.json 是显示名边表（不是某套主题的产物），跟 minimal 一样跳过
        if name in keep or name in ("minimal", "names"):
            continue
        sibling = os.path.exists(f"ecosystem/{name}") or os.path.exists(f"ghostty/hekouwang-{name}")
        if sibling or name in _known_removed_hint():
            rm(f, f"{name}.json")

    if not pro:
        return removed          # 安全线 2：开源版到此为止

    for f in glob.glob("ghostty/hekouwang-*"):
        name = os.path.basename(f)[len("hekouwang-"):]
        if name.endswith("-p3"):
            name = name[:-3]
        if name not in keep:
            rm(f, f"ghostty/{name}")

    for f in glob.glob("warp/*.yaml"):
        name = os.path.basename(f)[:-5].replace("_", "-")
        if name not in keep:
            rm(f, f"warp/{name}")

    for d in glob.glob("ecosystem/*"):
        name = os.path.basename(d)
        if name == "vscode" or not os.path.isdir(d):      # 安全线 3
            continue
        if name not in keep:
            rm(d, f"ecosystem/{name}/")

    for f in glob.glob("ecosystem/vscode/themes/hekouwang-*-color-theme.json"):
        name = os.path.basename(f)[len("hekouwang-"):-len("-color-theme.json")]
        if name not in keep:
            rm(f, f"vscode/{name}")

    return removed


def _known_removed_hint():
    """没有兄弟产物佐证时的兜底：开源版只出 json，删掉色板后就只剩一个孤零零的 json，
    上面那个 sibling 判据认不出来。这里读 palettes/ 里**曾经**出现过的名字做交叉验证 ——
    拿不到就返回空集合，**宁可漏删也不误删**。"""
    try:
        names = set()
        for f in glob.glob("palettes/*.py"):
            txt = open(f, encoding="utf-8").read()
            names |= set(re.findall(r'^\s{4}"([a-z0-9][a-z0-9-]*)":', txt, re.M))
        return names
    except Exception:
        return set()


def main():
    pro = load_pro()
    palettes, origin = load()

    if not palettes:
        # 连社区色板都没有：只出一份无配色骨架，保证脚本链路能跑
        write("minimal.json", json.dumps({"Profiles": [build_minimal()]},
                                         ensure_ascii=False, indent=2))
        print(t("GEN_NO_PALETTE"))
        return

    has_brand = any(origin.get(n) == "brand" for n in palettes)
    print(t("GEN_COUNT", len(palettes),
            t("GEN_WITH_BRAND") if has_brand else t("GEN_COMMUNITY_ONLY")))
    print(t("GEN_ENGINE", t("GEN_ENGINE_PRO") if pro else t("GEN_ENGINE_OSS")))

    for name, p in palettes.items():
        tier = t("GEN_TIER_PAID") if origin.get(name) == "brand" else t("GEN_TIER_OSS")
        light = t("GEN_TONE_LIGHT") if p.get("light") else t("GEN_TONE_DARK")
        print(f"  [{tier}·{light}] {name}  {p['display']}")
        write(f"{name}.json", json.dumps({"Profiles": [build(p, name)]},
                                         ensure_ascii=False, indent=2))

    # 社区 / 导入色板在上游并不遵守本仓的约束（normal≠bright、对比度地板），
    # load() 已经就地解过一轮；这里把改动打出来，免得「颜色怎么和上游不一样」变成暗箱。
    if ADJUSTMENTS:
        print(t("GEN_ADJUSTED", len(ADJUSTMENTS)))
        for n, changes in list(ADJUSTMENTS.items())[:8]:
            slots = ", ".join(c["slot"] for c in changes[:6])
            more = t("GEN_ADJUSTED_MORE", len(changes) - 6) if len(changes) > 6 else ""
            print(f"  - {n}: {slots}{more}")

    # 显示名边表：所有生成产物里烧的都是**英文名**（公开仓要对英文用户成立），
    # 中文名由 theme.sh / _apply_pro.sh 在**部署那一刻**注入。
    # 这样两种语言共用同一套产物，不必按语言各生成一份、也就不会漂。
    write("names.json", json.dumps(
        {n: {"en": q["display"], "zh": q.get("display_zh", q["display"])}
         for n, q in palettes.items()},
        ensure_ascii=False, indent=2) + "\n")

    if pro:
        pro.generate({
            "palettes": palettes, "origin": origin, "write": write,
            "rgb": rgb, "mix": mix, "truecolor": truecolor, "col": col,
            "COLUMNS": COLUMNS, "ROWS": ROWS,
            "TRANSPARENCY": TRANSPARENCY, "BLUR_RADIUS": BLUR_RADIUS,
        })
        print(t("GEN_PRO_EXTRA"))

    # 清理旧产物必须在生成**之后**：先写新的、再扫没主的，顺序反了会把这一轮
    # 刚生成的东西当成孤儿删掉（keep 集合是按色板算的，跟生成顺序无关，但
    # 万一将来有人改成"按本轮写过的文件"判定，顺序就要命了）。
    swept = sweep(palettes, pro)
    if swept:
        print(t("GEN_SWEPT", len(swept)))
        for x in swept[:8]:
            print(f"  - {x}")
        if len(swept) > 8:
            print(t("GEN_SWEPT_MORE", len(swept) - 8))

    print(t("GEN_DEFAULT", default_theme(palettes)))
    missing = []
    if not has_brand:
        missing.append(t("GEN_MISSING_BRAND",
                         ", ".join(b for b in BRAND_THEMES if b not in palettes)))
    if not pro:
        missing.append(t("GEN_MISSING_MULTI"))
        missing.append(t("GEN_MISSING_ECO"))
        missing.append(t("GEN_MISSING_FONT"))
        missing.append(t("GEN_MISSING_AUTO"))
    if missing:
        print(t("GEN_MISSING_HEAD"))
        for m in missing:
            print(f"  · {m}")
        print(t("GEN_MISSING_TAIL"))
    print(t("GEN_DONE"))


if __name__ == "__main__":
    main()
