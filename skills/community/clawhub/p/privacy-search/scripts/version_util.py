"""
版本解析工具 - 单一真相源
==========================
V1.2 新增（修复 P0-1）

问题背景：
    V1.1 发版时 SKILL.md 的 version 改为 1.1.0，但 update_checker.py 中的
    CURRENT_VERSION 常量仍停留在 "1.0.0"，导致：
      - 已安装 1.1.0 的用户，程序自我认知为 1.0.0
      - 与线上 1.1.0 比较后判定"有新版本"
      - 升级后仍然提示，且缓存 24 小时即每天弹一次
      - 死规则 11 的更新提醒功能实质失效

解决方案：
    版本号唯一来源为 SKILL.md 的 frontmatter，运行时解析。
    以后发版只需修改 SKILL.md 一处，本模块自动跟随。
    解析失败时回落到 FALLBACK_VERSION，保证不因读取异常而崩溃。
"""

import os
import re
import sys
from functools import lru_cache
from typing import Optional, Tuple

# 不生成 __pycache__（死规则 13）
sys.dont_write_bytecode = True

# 解析失败时的兜底版本（应与 SKILL.md 保持一致，仅作保险）
FALLBACK_VERSION = "1.2.0"

# frontmatter 版本行正则
# 兼容三种写法：version: 1.2.0 / version: "1.2.0" / version: '1.2.0'
# 说明：死规则 8 要求不带引号，但解析端保持宽容以避免误判
_VERSION_PATTERN = re.compile(
    r'^\s*version:\s*["\']?(\d+(?:\.\d+)*(?:-[0-9A-Za-z.-]+)?)["\']?\s*$',
    re.MULTILINE,
)


def _locate_skill_md() -> Optional[str]:
    """
    定位 SKILL.md

    查找顺序：
      1. 本文件上级目录（scripts/ 的父目录，即 skill 根目录）
      2. 当前工作目录
      3. 当前工作目录的父目录
    """
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(os.path.dirname(here), "SKILL.md"),
        os.path.join(os.getcwd(), "SKILL.md"),
        os.path.join(os.path.dirname(os.getcwd()), "SKILL.md"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return None


@lru_cache(maxsize=1)
def get_current_version() -> str:
    """
    读取当前 Skill 版本号

    从 SKILL.md 的 frontmatter 解析，失败时返回 FALLBACK_VERSION。
    结果缓存，避免重复读文件。

    Returns:
        版本号字符串，如 "1.2.0"
    """
    path = _locate_skill_md()
    if not path:
        return FALLBACK_VERSION

    try:
        # utf-8-sig 兼容 BOM
        with open(path, "r", encoding="utf-8-sig") as f:
            # 只读前 60 行，frontmatter 必在文件头部
            head = "".join(f.readline() for _ in range(60))
    except (OSError, UnicodeDecodeError):
        return FALLBACK_VERSION

    match = _VERSION_PATTERN.search(head)
    if match:
        return match.group(1).strip()
    return FALLBACK_VERSION


def parse_version(version: str) -> Tuple[int, int, int]:
    """
    解析版本号为三元组

    规则：
      - 不足三位补 0（"1.2" -> (1, 2, 0)）
      - 超过三位截断（"1.2.3.4" -> (1, 2, 3)）
      - 忽略预发布后缀（"1.2.0-beta" -> (1, 2, 0)）
      - 非数字段按 0 处理，保证不抛异常

    Args:
        version: 版本号字符串

    Returns:
        (major, minor, patch)
    """
    if not version:
        return (0, 0, 0)

    # 去掉 v 前缀与预发布后缀
    cleaned = version.strip().lstrip("vV").split("-")[0].split("+")[0]

    parts = []
    for seg in cleaned.split(".")[:3]:
        try:
            parts.append(int(seg))
        except ValueError:
            parts.append(0)

    while len(parts) < 3:
        parts.append(0)

    return (parts[0], parts[1], parts[2])


def compare_versions(v1: str, v2: str) -> int:
    """
    比较两个版本号

    预发布版本（含 "-"）视为低于同号正式版：
        1.2.0-beta < 1.2.0

    Args:
        v1: 版本号 A
        v2: 版本号 B

    Returns:
        -1 表示 v1 < v2
         0 表示相等
         1 表示 v1 > v2
    """
    p1, p2 = parse_version(v1), parse_version(v2)
    if p1 < p2:
        return -1
    if p1 > p2:
        return 1

    # 主版本相同，比较预发布标记
    v1_pre = "-" in (v1 or "")
    v2_pre = "-" in (v2 or "")
    if v1_pre and not v2_pre:
        return -1
    if not v1_pre and v2_pre:
        return 1
    return 0


def is_newer(candidate: str, current: str) -> bool:
    """判断 candidate 是否比 current 更新"""
    return compare_versions(candidate, current) > 0


def display_width(text: str) -> int:
    """
    计算字符串在等宽终端中占用的列数

    中文、日文、全角标点与多数 emoji 占两列，
    而 len() 一律按一列计。用 len() 做边框对齐时，
    含中文的行会短一截、含 emoji 的行会溢出。
    """
    width = 0
    for ch in text:
        code = ord(ch)
        # 东亚全角区段 + 常用 emoji 区段
        if (0x1100 <= code <= 0x115F          # 韩文字母
                or 0x2E80 <= code <= 0xA4CF    # CJK 部首至彝文
                or 0xAC00 <= code <= 0xD7A3    # 韩文音节
                or 0xF900 <= code <= 0xFAFF    # CJK 兼容表意
                or 0xFE30 <= code <= 0xFE6F    # CJK 兼容形式
                or 0xFF00 <= code <= 0xFF60    # 全角字符
                or 0xFFE0 <= code <= 0xFFE6
                or 0x1F300 <= code <= 0x1F9FF):  # emoji
            width += 2
        else:
            width += 1
    return width


def pad_display(text: str, target: int) -> str:
    """
    按显示列数右侧补空格，使文本占满 target 列

    超出目标宽度时按列裁剪，避免把边框顶开。
    """
    if display_width(text) > target:
        clipped = ""
        used = 0
        for ch in text:
            w = display_width(ch)
            if used + w > target:
                break
            clipped += ch
            used += w
        text = clipped
        return text + " " * (target - used)
    return text + " " * (target - display_width(text))


# 模块名 -> pip 包名，两者不一致的需显式映射
_DEPENDENCIES = {
    "aiohttp": "aiohttp",
    "yaml": "pyyaml",
    "bs4": "beautifulsoup4",
}


def require_dependencies(modules: Optional[Tuple[str, ...]] = None) -> None:
    """
    检查第三方依赖，缺失时给出可直接执行的安装命令后退出

    直接 import 缺失的包只会抛裸 ModuleNotFoundError，
    首次使用的用户难以判断该装什么、用哪个解释器装。
    此处一次性收集全部缺失项并打印完整命令。

    本模块只依赖标准库，可安全地在任何入口脚本的
    第三方 import 之前调用。

    Args:
        modules: 需要检查的模块名，为空时检查全部已知依赖
    """
    targets = modules or tuple(_DEPENDENCIES)
    missing = []
    for module in targets:
        package = _DEPENDENCIES.get(module, module)
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if not missing:
        return

    here = os.path.dirname(os.path.abspath(__file__))
    req = os.path.join(os.path.dirname(here), "requirements.txt")
    message = "\n".join([
        "",
        "缺少运行所需的依赖：" + "、".join(missing),
        "",
        "请先安装依赖后重试：",
        '  %s -m pip install -r "%s"' % (sys.executable, req),
        "",
        "建议在虚拟环境中安装，避免影响系统 Python：",
        "  %s -m venv .venv" % sys.executable,
        "",
    ])
    print(message, file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    print(f"SKILL.md 路径: {_locate_skill_md()}")
    print(f"当前版本: {get_current_version()}")
    print(f"解析结果: {parse_version(get_current_version())}")
