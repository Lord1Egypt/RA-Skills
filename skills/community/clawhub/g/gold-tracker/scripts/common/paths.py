"""路径解析与环境引导。

所有脚本入口 MUST 先调用 `ensure_env()`：
  1. 补全最小 PATH（cron / systemd 等无交互环境不依赖用户 shell 配置，P1-9）；
  2. 确保 `common` 包可被 import；
  3. 返回项目根目录 ROOT。

ROOT 始终基于本文件位置推导，与当前工作目录无关（平台无关，P1-10 的相对路径约束）。
"""

import os
import sys
from pathlib import Path

# scripts/common/paths.py -> parents[0]=common, [1]=scripts, [2]=项目根目录
ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "scripts"
COMMON_DIR = SCRIPTS_DIR / "common"


def bootstrap_path():
    """在 PATH 中补充常见的系统可执行目录（仅添加已存在的目录）。

    cron 的默认 PATH 通常只有 /usr/bin:/bin；homebrew 安装的 curl/python 可能
    不在其中。这里做最小引导，避免因 shell 配置缺失而崩溃。
    """
    extra = [
        "/opt/homebrew/bin",
        "/usr/local/bin",
        "/usr/bin",
        "/bin",
        "/usr/sbin",
        "/sbin",
    ]
    cur = os.environ.get("PATH", "")
    parts = [p for p in cur.split(os.pathsep) if p]
    for p in extra:
        if p not in parts and os.path.isdir(p):
            parts.append(p)
    os.environ["PATH"] = os.pathsep.join(parts)


def resolve(path):
    """把相对技能根目录的路径解析为绝对路径；绝对路径原样返回。"""
    p = Path(path)
    if p.is_absolute():
        return p
    return ROOT / p


def ensure_env():
    """脚本入口统一引导。返回项目根目录 Path。"""
    bootstrap_path()
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    return ROOT
