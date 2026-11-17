"""v3.2 §3.2 补充：用户 HOME 目录下 .config 目录名 -> Agent 产品名映射表。

数据文件，不执行脚本。用于 AgentLocator.discover_candidates() 自动识别本机已安装的 Agent。
映射方向：~/.<dot_dir_name> -> <product_name>。

添加新产品只需在 AGENT_PRODUCT_MAP 中加入一行，无需改扫描逻辑。
未知目录显示为 product="unknown"，可在 GUI 手动添加 Profile。

安全边界：
- 只读 %HOME% 下一级子目录的 Name/FullName，不读正文
- 不做递归搜索（stale 检测最多 2 层 stat）
- 不做系统进程探测

stale 检测阈值：
- 30 天未修改 -> stale
- 60 天未修改 -> likely_uninstalled
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

# stale 判定阈值（秒）
STALE_THRESHOLD_SECONDS = 30 * 24 * 3600       # 30 天
LIKELY_UNINSTALLED_THRESHOLD_SECONDS = 60 * 24 * 3600  # 60 天

# ---------------------------------------------------------------------------
# AGENT_PRODUCT_MAP：点目录名 -> 产品名
# ---------------------------------------------------------------------------

AGENT_PRODUCT_MAP: dict[str, str] = {
    # ---------- 海外 Agent（已有完整 Profile）----------
    ".claude": "claude-code",
    ".codex": "codex",
    ".cursor": "cursor",
    ".codeium": "windsurf",

    # ---------- 国产 Agent（独立 IDE / CLI）----------
    ".trae-cn": "trae",       # 字节跳动 TRAE（含 MarsCode 继承），独立 IDE
    ".trae": "trae",
    ".zcode": "zcode",        # zcode CLI Agent
    ".lingma": "lingma",      # 阿里通义灵码 IDE
    ".comate": "comate",      # 百度文心快码 IDE
    ".qoder": "qoder",        # Qoder AI IDE（项目级 .qoder/rules + .qoder/skills）

    # ---------- 国产 Agent（桌面 AI 助手）----------
    ".workbuddy": "workbuddy",  # 腾讯 WorkBuddy 桌面 AI 助手

    # ---------- 开源 / 套壳 Agent ----------
    ".openclaw": "openclaw",    # OpenClaw AI 智能体（含 MEMORY.md/SOUL.md/AGENTS.md）
    ".opencode": "opencode",    # OpenCode CLI coding agent（~/.config/opencode/）

    # ---------- 国产 Agent（插件型，数据在 VSCode/JetBrains 扩展目录）----------
    # CodeGeeX / CodeBuddy 作为插件时数据在宿主 IDE 扩展目录，无法用 ~/. 映射
    # 用户需手动添加 SourceRoot 指向扩展目录

    # ---------- 其他可探测目录 ----------
    ".echobird": "echobird",  # 本地模型管理器（非 coding agent）
    ".gumiho": "gumifox",
}

# APPDATA 下的 Agent 目录（Windows 专用，非 ~/. 目录）
APPDATA_AGENT_MAP: dict[str, str] = {
    "CodeBuddy": "codebuddy",  # 腾讯 CodeBuddy
}

# VSCode 扩展目录中的 Agent 插件名前缀
VSCODE_EXTENSION_AGENT_MAP: dict[str, str] = {
    "aminer.codegeex": "codegeex",      # 智谱 CodeGeeX
    "codebuddy": "codebuddy",            # 腾讯 CodeBuddy VSCode 插件
    "lingma": "lingma",                  # 通义灵码 VSCode 插件
    "comate": "comate",                  # 文心快码 VSCode 插件
}

# 从映射表中提取的已知产品名集合（不含 unknown）
KNOWN_PRODUCTS: set[str] = set(AGENT_PRODUCT_MAP.values())

# 需要跳过的非 Agent 目录名（精确匹配）
IGNORED_DIRS: set[str] = {
    ".config",
    ".vscode",
    ".vscode-server",
    ".vscode-shared",
    ".cache",
    ".android",
    ".chocolatey",
    ".dotnet",
    ".lldb",
    ".local",
    ".bun",
    ".ohos",
    ".ohpm",
    ".hvigor",
    ".djl.ai",
    ".BigNox",
    ".agents",
    ".agent-reach",
    ".codegraph",
    ".qmf",
    ".sbx-denybin",
    ".Icecream PDF Split and Merge",
    ".cc-switch",
    ".cc-weixin",
    ".harmony",
    ".ollama",
    ".headroom",
    ".tuval",
}


def product_for_dot_dir(dot_dir_name: str) -> str | None:
    """返回点目录对应的产品名。未匹配返回 None。"""
    return AGENT_PRODUCT_MAP.get(dot_dir_name)


def is_known_product(product_name: str) -> bool:
    """检查产品名是否在映射表中。"""
    return product_name in KNOWN_PRODUCTS


def candidate_agent_products() -> list[dict[str, Any]]:
    """返回当前映射表支持的所有 Agent 产品信息（静态数据）。"""
    result = []
    seen_products: set[str] = set()
    for dot_dir, product in AGENT_PRODUCT_MAP.items():
        if product in seen_products:
            continue
        seen_products.add(product)
        result.append({
            "product": product,
            "dot_dir_name": dot_dir,
            "has_profile": is_known_product(product),
        })
    return result


def detect_stale_status(dir_path: str | Path) -> dict[str, Any]:
    """检测 Agent 目录的 stale 状态。

    只做 stat，不读正文，递归最多 2 层统计文件数和大小。

    返回:
        {
            "stale_status": "active" | "stale" | "likely_uninstalled",
            "mtime": float,
            "mtime_iso": str,
            "size_bytes": int,
            "file_count": int,
            "has_executable": bool,
            "days_since_modified": float,
        }
    """
    path = Path(dir_path)
    if not path.exists() or not path.is_dir():
        return {
            "stale_status": "likely_uninstalled",
            "mtime": 0.0,
            "mtime_iso": "",
            "size_bytes": 0,
            "file_count": 0,
            "has_executable": False,
            "days_since_modified": -1,
        }

    total_size = 0
    file_count = 0
    has_executable = False
    latest_mtime = path.stat().st_mtime

    def _scan(dir_path: Path, depth: int) -> None:
        nonlocal total_size, file_count, has_executable, latest_mtime
        if depth > 2:
            return
        try:
            for entry in dir_path.iterdir():
                try:
                    st = entry.stat()
                except OSError:
                    continue
                if entry.is_file():
                    total_size += st.st_size
                    file_count += 1
                    if st.st_mtime > latest_mtime:
                        latest_mtime = st.st_mtime
                    if entry.suffix.lower() in (".exe", ".app") or (
                        entry.suffix == "" and os.access(entry, os.X_OK)
                    ):
                        has_executable = True
                elif entry.is_dir():
                    if st.st_mtime > latest_mtime:
                        latest_mtime = st.st_mtime
                    _scan(entry, depth + 1)
        except (OSError, PermissionError):
            pass

    _scan(path, 0)

    now = time.time()
    age_seconds = now - latest_mtime
    days_since = age_seconds / (24 * 3600)

    if age_seconds >= LIKELY_UNINSTALLED_THRESHOLD_SECONDS and not has_executable:
        stale_status = "likely_uninstalled"
    elif age_seconds >= STALE_THRESHOLD_SECONDS and not has_executable:
        stale_status = "stale"
    else:
        stale_status = "active"

    from datetime import datetime, timezone
    mtime_iso = datetime.fromtimestamp(latest_mtime, tz=timezone.utc).isoformat() if latest_mtime > 0 else ""

    return {
        "stale_status": stale_status,
        "mtime": latest_mtime,
        "mtime_iso": mtime_iso,
        "size_bytes": total_size,
        "file_count": file_count,
        "has_executable": has_executable,
        "days_since_modified": round(days_since, 1),
    }
