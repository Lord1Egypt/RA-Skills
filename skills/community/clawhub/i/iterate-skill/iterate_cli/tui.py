"""统一 TUI 渲染层 — skills.sh 风格.

本模块提供所有 CLI 交互的视觉组件，基于 rich 库实现。
设计参考 @clack/prompts 的符号体系和配色方案：
  ◆ intro/outro 标志
  ◇ 问题块标志
  │ └ 垂直连接线
  ● ○ 单选选中/未选
  ✓ ✗ 成功/失败

所有组件均通过 ``TUI`` 类的实例方法调用，便于测试时注入 mock console。
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.theme import Theme

# ---------------------------------------------------------------------------
# 设计令牌 / Design Tokens
# ---------------------------------------------------------------------------

# 主题配色 — skills.sh 风格青色主调 + 语义色
_ITERATE_THEME = Theme({
    # 主色调
    "iterate.primary": "bold cyan",
    "iterate.accent": "magenta",
    # 语义色
    "iterate.success": "green",
    "iterate.error": "bold red",
    "iterate.warning": "yellow",
    "iterate.info": "blue",
    # 中性色
    "iterate.dim": "dim",
    "iterate.bold": "bold",
    "iterate.title": "bold cyan",
    "iterate.subtitle": "dim",
    "iterate.label": "bold",
    "iterate.value": "white",
    "iterate.hint": "dim italic",
})

# 符号系统 — 仿 @clack/prompts
SYM_INTRO = "◆"
SYM_QUESTION = "◇"
SYM_END = "└"
SYM_BULLET = "●"
SYM_SUCCESS = "✓"
SYM_ERROR = "✗"
SYM_WARNING = "⚠"
SYM_SPINNER = "✻"

# key_value 键名对齐宽度（显示宽度，非字符数）
KEY_VALUE_WIDTH = 22


def _display_width(text: str) -> int:
    """计算字符串的近似终端显示宽度（CJK 全角字符按 2 计）.

    Args:
        text: 待计算字符串

    Returns:
        显示宽度
    """
    width = 0
    for ch in text:
        cp = ord(ch)
        # 控制字符（C0 区、DEL 与 C1 区）不渲染、不占宽度。
        if cp < 0x20 or 0x7F <= cp <= 0x9F:
            continue
        # 组合用记号、变体选择符（VS16 等）宽度为 0，跟随前一字符。
        if (
            0x0300 <= cp <= 0x036F
            or 0xFE00 <= cp <= 0xFE0F
            or 0xE0100 <= cp <= 0xE01EF
        ):
            continue
        # 东亚全角字符（CJK 统一表意文字、全角符号、全角标点等）
        if (
            0x1100 <= cp <= 0x115F
            or 0x2E80 <= cp <= 0xA4CF
            or 0xAC00 <= cp <= 0xD7A3
            or 0xF900 <= cp <= 0xFAFF
            or 0xFE30 <= cp <= 0xFE4F
            or 0xFF00 <= cp <= 0xFF60
            or 0xFFE0 <= cp <= 0xFFE6
        ):
            width += 2
            continue
        # Emoji（含象形符号与区域指示符）在多数终端按 2 列渲染。
        if 0x1F000 <= cp <= 0x1FAFF:
            width += 2
            continue
        width += 1
    return width


def _fit_prefix(text: str, width: int) -> str:
    """Return the longest prefix of ``text`` whose display width is ≤ ``width``.

    Always returns at least one character (when ``text`` is non-empty), so a
    caller looping on the remainder is guaranteed to make progress even when a
    single character is wider than the budget.
    """
    taken = 0
    for index in range(1, len(text) + 1):
        if _display_width(text[:index]) > width:
            break
        taken = index
    return text[:taken] or text[:1]


def _wrap_display(text: str, width: int) -> list[str]:
    """Greedy word-wrap measured in *display* width, not character count.

    ``str`` length is the wrong ruler for this CLI: a Chinese value of 40
    characters occupies 80 columns, so ``textwrap`` would emit a line twice as
    wide as the terminal. Words break at spaces where possible and are
    hard-split otherwise (long paths, URLs); existing newlines stay hard breaks.
    """
    if width <= 0:
        return text.split("\n")
    lines: list[str] = []
    for paragraph in text.split("\n"):
        current = ""
        for word in paragraph.split(" "):
            candidate = word if not current else f"{current} {word}"
            if _display_width(candidate) <= width:
                current = candidate
                continue
            if current:
                lines.append(current)
            current = word
            while _display_width(current) > width:
                head = _fit_prefix(current, width)
                lines.append(head)
                current = current[len(head):]
        lines.append(current)
    return lines


# ITERATE 立体 ASCII 横幅 — 仿 skills.sh 顶部 Logo
_ITERATE_BANNER_LINES = (
    "██╗████████╗███████╗██████╗  █████╗ ████████╗███████╗",
    "██║╚══██╔══╝██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝",
    "██║   ██║   █████╗  ██████╔╝███████║   ██║   █████╗  ",
    "██║   ██║   ██╔══╝  ██╔══██╗██╔══██║   ██║   ██╔══╝  ",
    "██║   ██║   ███████╗██║  ██║██║  ██║   ██║   ███████╗",
    "╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝",
)


# ---------------------------------------------------------------------------
# TUI 渲染器
# ---------------------------------------------------------------------------


class TUI:
    """统一 TUI 渲染器，封装所有终端输出逻辑.

    所有 CLI 模块应通过此类输出内容，不直接调用 print()。
    测试时可通过 ``TUI(console=mock_console)`` 注入 mock。

    Attributes:
        console: rich Console 实例
        is_interactive: 是否为交互式终端（非管道/重定向）
    """

    def __init__(self, console: Console | None = None) -> None:
        """初始化 TUI 渲染器.

        Args:
            console: 可选的自定义 Console 实例，测试时注入 mock
        """
        if console is not None:
            self.console = console
            self.is_interactive = console.is_terminal
            # 测试时复用注入的 console 输出错误信息
            self._stderr_console = console
        else:
            # force_terminal=None 让 rich 自动检测
            self.console = Console(theme=_ITERATE_THEME, force_terminal=None)
            self.is_interactive = self.console.is_terminal
            # 独立的 stderr console，确保错误信息写入 stderr
            self._stderr_console = Console(
                theme=_ITERATE_THEME, stderr=True, force_terminal=None
            )

    # ------------------------------------------------------------------
    # 基础输出
    # ------------------------------------------------------------------

    def print(self, *args: Any, **kwargs: Any) -> None:
        """透传到 console.print，保持兼容性."""
        self.console.print(*args, **kwargs)

    def empty_line(self) -> None:
        """输出一个空行."""
        self.console.print()

    # ------------------------------------------------------------------
    # 横幅与结构
    # ------------------------------------------------------------------

    def banner(self) -> None:
        """输出 ITERATE 立体 ASCII 横幅 — 仿 skills.sh 顶部 Logo.

        横幅左对齐行首，不居中，与后续列表/步骤的缩进保持一致。
        是否展示由调用方（cli._should_show_banner）根据 ``--no-banner``
        与 ``ITERATE_NO_BANNER`` 环境变量决定，本方法只负责渲染。
        """
        self.console.print()
        for line in _ITERATE_BANNER_LINES:
            self.console.print(
                f"[iterate.primary]{line}[/]",
                soft_wrap=True,
            )
        self.console.print()

    def intro(self, title: str, subtitle: str = "") -> None:
        """输出开始横幅 — 仿 @clack/prompts intro().

        格式:
          ◆ Iterate Skill — Onboarding
            项目知识库初始化

        Args:
            title: 主标题
            subtitle: 副标题（可选，dim 灰色显示）
        """
        self.console.print()
        self.console.print(
            f"[iterate.primary]{SYM_INTRO}[/] "
            f"[iterate.title]{escape(title)}[/]"
        )
        if subtitle:
            self.console.print(f"  [iterate.subtitle]{escape(subtitle)}[/]")
        self.console.print()

    def section(self, title: str) -> None:
        """输出区块标题.

        格式:
          ── 技术栈 / Tech Stack ──

        Args:
            title: 区块标题（通常为中英双语）
        """
        self.console.print()
        self.console.print(f"  [iterate.label]── {escape(title)} ──[/]")

    def cancel(self) -> None:
        """输出取消消息."""
        self.console.print()
        self.console.print(
            f"  [iterate.dim]{SYM_END} 已取消 / Cancelled.[/]"
        )
        self.console.print()

    # ------------------------------------------------------------------
    # 信息展示
    # ------------------------------------------------------------------

    def info(self, message: str, indent: int = 2) -> None:
        """输出普通信息行.

        Args:
            message: 消息内容
            indent: 缩进空格数
        """
        prefix = " " * indent
        self.console.print(f"{prefix}{escape(message)}")

    def hint(self, message: str, indent: int = 2) -> None:
        """输出提示信息（dim 灰色）.

        Args:
            message: 提示内容
            indent: 缩进空格数
        """
        prefix = " " * indent
        self.console.print(f"{prefix}[iterate.dim]{escape(message)}[/]")

    def warning(self, message: str, indent: int = 2) -> None:
        """输出警告信息到 stderr.

        与 ``error`` 同走 stderr：stdout 只保留数据（``--json`` 模式承诺
        "stdout 恰好一个 JSON 文档"）。此前 warning 写 stdout，导致
        ``refresh --json`` / ``config set --json`` 等在 JSON 之前先打印
        ``⚠`` 警告行，管道下游 ``| jq`` 直接解析失败。

        Args:
            message: 警告内容
            indent: 缩进空格数
        """
        prefix = " " * indent
        self._stderr_console.print(
            f"{prefix}[iterate.warning]{SYM_WARNING} {escape(message)}[/]",
            soft_wrap=True,
        )

    def error(self, message: str, indent: int = 2) -> None:
        """输出错误信息到 stderr.

        Args:
            message: 错误内容
            indent: 缩进空格数（与其他语义色方法保持一致，默认 2）
        """
        prefix = " " * indent
        self._stderr_console.print(
            f"{prefix}[iterate.error]{SYM_ERROR} {escape(message)}[/]",
            soft_wrap=True,
        )

    def success(self, message: str, indent: int = 2) -> None:
        """输出成功信息.

        Args:
            message: 成功内容
            indent: 缩进空格数
        """
        prefix = " " * indent
        self.console.print(
            f"{prefix}[iterate.success]{SYM_SUCCESS} {escape(message)}[/]"
        )

    def bullet(self, message: str, indent: int = 2) -> None:
        """输出带圆点的列表项.

        Args:
            message: 列表项内容
            indent: 缩进空格数
        """
        prefix = " " * indent
        self.console.print(
            f"{prefix}[iterate.dim]{SYM_BULLET}[/] {escape(message)}"
        )

    def key_value(self, key: str, value: str, indent: int = 2) -> None:
        """输出键值对（key 加粗，value 正常）.

        值过长而折行时，**续行与首行同列**：以前续行从第 0 列开始，看起来
        像新的一段而不是同一个值，复制出去对齐也已经坏掉（`iterate scan` 的
        "Top-level dirs" 就是第一个撞上的例子）。rich 只对首行加缩进，所以
        折行在这里按**显示宽度**自己做（CJK 双宽不会被按字符数算错），
        续行预先补好左缩进。

        Args:
            key: 键名
            value: 值
            indent: 缩进空格数
        """
        # 按显示宽度（CJK 双宽）对齐 key，避免中文错位
        # Pad by the width of the *visible* label. Measuring the escaped text
        # over-counted every `[` (rich renders `\[` as one column), so a key
        # containing a bracket pushed the value column right by one per
        # bracket. Escape only when embedding into markup.
        raw_label = f"{key}:"
        padded_key = escape(
            raw_label + " " * max(KEY_VALUE_WIDTH - _display_width(raw_label), 1)
        )
        prefix = " " * indent
        # Budget for the value column: terminal width minus both the left
        # indent and the key column. Floored at 16 so a very narrow terminal
        # still gets readable chunks instead of one character per line.
        budget = max(
            (getattr(self.console, "width", None) or 80) - indent - KEY_VALUE_WIDTH, 16
        )
        wrapped = _wrap_display(value, budget)
        continuation = " " * (indent + KEY_VALUE_WIDTH)
        rendered = [
            (
                f"{prefix}[iterate.label]{padded_key}[/] "
                f"[iterate.value]{escape(wrapped[0])}[/]"
            )
        ]
        rendered.extend(
            f"{continuation}[iterate.value]{escape(line)}[/]" for line in wrapped[1:]
        )
        # One print call for the whole value: splitting it would let rich
        # interleave other output (or a spinner repaint) into the middle of a
        # single key/value row.
        self.console.print("\n".join(rendered))

    # ------------------------------------------------------------------
    # 列表展示
    # ------------------------------------------------------------------

    def numbered_list(
        self,
        items: Sequence[str],
        indent: int = 4,
        markers: Sequence[str] | None = None,
    ) -> None:
        """输出编号列表.

        Args:
            items: 列表项
            indent: 缩进空格数
            markers: 可选的自定义标记（如 ["✓", "", ""]），长度需与 items 一致
        """
        prefix = " " * indent
        for i, item in enumerate(items, 1):
            if markers and i - 1 < len(markers) and markers[i - 1]:
                marker_str = f"[iterate.success]{markers[i - 1]}[/] "
            else:
                marker_str = ""
            self.console.print(
                f"{prefix}[iterate.dim]{i}.[/] {marker_str}{escape(item)}"
            )

    # ------------------------------------------------------------------
    # 状态与进度
    # ------------------------------------------------------------------

    def status(self, message: str) -> Any:
        """返回一个 status 上下文管理器，用于耗时操作.

        用法:
            with tui.status("正在扫描项目..."):
                result = scan_project()

        非交互式终端（管道/重定向/CI）下返回 no-op 上下文管理器，
        避免在不可交互的输出中刷出 spinner 控制序列。

        Args:
            message: 状态消息

        Returns:
            rich Console.status 上下文管理器（或非交互时的 no-op）。
        """
        if not self.is_interactive:
            from contextlib import nullcontext

            return nullcontext()
        return self.console.status(
            f"[iterate.primary]{SYM_SPINNER}[/] {escape(message)}",
            spinner="dots",
        )

    def panel(self, content: str, title: str = "", style: str = "") -> None:
        """输出带边框的面板.

        Args:
            content: 面板内容
            title: 面板标题
            style: 边框样式（如 "cyan", "green"）
        """
        border_style = style or "cyan"
        self.console.print(
            Panel(
                escape(content),
                title=f"[iterate.title]{escape(title)}[/]" if title else None,
                title_align="left",
                border_style=border_style,
                padding=(0, 1),
            )
        )

    # ------------------------------------------------------------------
    # 交互输入（包装 input_func，添加样式）
    # ------------------------------------------------------------------

    def question(self, message: str) -> None:
        """输出问题标记行（不含输入），无返回值.

        用于在 input_func 调用前打印问题头。
        实际输入仍由调用方通过 input_func 完成。

        格式:
          ◇ 这是一个问题？
        """
        self.console.print(
            f"  [iterate.primary]{SYM_QUESTION}[/] {escape(message)}"
        )


# ---------------------------------------------------------------------------
# 单例实例 — 供整个 CLI 使用
# ---------------------------------------------------------------------------

# 全局 TUI 实例。模块级导入即可使用：
#   from iterate_cli.tui import tui
#   tui.intro("Hello")
#
# 测试时可替换：
#   from iterate_cli import tui as tui_module
#   tui_module.tui = TUI(console=mock_console)
tui = TUI()


def reset_tui() -> None:
    """重置全局 TUI 实例（测试用）.

    测试中如果修改了 ``tui`` 单例，调用此函数恢复默认实例。
    """
    global tui
    tui = TUI()


def set_tui(new_tui: TUI) -> None:
    """替换全局 TUI 实例（测试用）.

    Args:
        new_tui: 新的 TUI 实例
    """
    global tui
    tui = new_tui
