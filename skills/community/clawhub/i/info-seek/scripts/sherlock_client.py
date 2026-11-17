#!/usr/bin/env python3
"""
scripts/sherlock_client.py — Sherlock 身份归因客户端（M0.3，默认 OFF）

Sherlock（sherlock-project）：用户名 → 平台存在性快速枚举（~400 站点，
亚分钟级、低依赖、支持 --tor）。定位 Maigret 的"快扫前置"，
与 Maigret 同族（identity_attribution），经注册表 degrade_to 形成替代链。

设计同 maigret_client：默认 OFF + 合规闸 + subprocess CLI + 错误分类复用 lifecycle。

────────────────────────────────────────────────────────────────────────
CLI 契约（sherlock-project v0.16.x 实测，2026-09-18 沙箱实证）
────────────────────────────────────────────────────────────────────────
旧实现把 ``sherlock <user> --json`` 当作"JSON 打到 stdout"，**三处全错**：
  1. ``--json FILE`` 是「站点数据输入文件/在线 data.json」，不是结果输出开关；
  2. Sherlock **不产出 JSON 结果文件**，结果只有 txt / csv / xlsx；
  3. stdout 是人类可读文本（进度条 + [+] 行），不是 JSON。

正确契约（本模块采用）：
  sherlock <user> --csv --print-found --timeout N [--tor]
    - ``--csv``            在工作目录写 ``<user>.csv``（列：
                           username,name,url_main,url_user,exists,
                           http_status,response_time_s）
    - ``--print-found``    CSV 只保留命中行（exists=Claimed），并在 stdout 打印
    - ``-o/--output``      仅配合 --txt，且单用户名；csv 固定文件名 <user>.csv
    - QueryStatus：Claimed（命中）/ Available（未命中）/ Unknown / Illegal / WAF
本模块在临时工作目录运行，结束后读回唯一 *.csv，不依赖 <user> 文件名合法性。
"""

from __future__ import annotations

import csv
import io
import logging
import os
import subprocess
import sys
import tempfile
from typing import Dict, List

log = logging.getLogger("infoseek.sherlock")

try:
    from core.capability_errors import CapabilityError, ConsentRequired, CapabilityUnavailable
    from core.capability_registry import (
        get_capability, grant_consent, is_effective_enabled, is_enabled,
        requires_consent,
    )
except ImportError:
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent / "core"))
    from capability_errors import CapabilityError, ConsentRequired, CapabilityUnavailable
    from capability_registry import (
        get_capability, grant_consent, is_effective_enabled, is_enabled,
        requires_consent,
    )

CAP_NAME = "Sherlock"

_dr = None


def _dep_reg():
    global _dr
    if _dr is None:
        _core = str(__import__("pathlib").Path(__file__).resolve().parent.parent / "core")
        if _core not in sys.path:
            sys.path.insert(0, _core)
        import dep_registry as _mod
        _dr = _mod
    return _dr

# exists 列 → 是否纳入 + 置信度（仅 Claimed 为真实命中）
_STATUS_MAP = {
    "Claimed": (True, 0.85),
    "Available": (False, 0.4),    # 未命中（--print-found 已过滤，防御性保留）
    "Unknown": (False, 0.0),
    "Illegal": (False, 0.0),
    "WAF": (False, 0.0),
}


def _resolve_cli() -> List[str]:
    """定位 sherlock 可执行：PATH → 隔离 venv（INFOSEEK_SHERLOCK_VENV）。

    返回命令片段（list），调用方以 cli + [username, ...] 拼接，
    兼容 Windows 控制台脚本（sherlock.exe）与模块式回退。
    """
    cli = _dep_reg().which_path("sherlock")
    if cli:
        return [cli]
    venv = os.environ.get("INFOSEEK_SHERLOCK_VENV")
    if venv:
        scripts = __import__("pathlib").Path(venv) / ("Scripts" if sys.platform == "win32" else "bin")
        for name in ("sherlock", "sherlock.exe"):
            cand = scripts / name
            if cand.exists():
                return [str(cand)]
        py = scripts / ("python.exe" if sys.platform == "win32" else "python")
        if py.exists():
            return [str(py), "-m", "sherlock_project"]
    return ["sherlock"]


def _consent_gate(consent: bool) -> None:
    if requires_consent(CAP_NAME):
        if consent:
            grant_consent(CAP_NAME)
        elif not is_effective_enabled(CAP_NAME):
            raise ConsentRequired(CAP_NAME)


def search(username: str,
           consent: bool = False,
           timeout: int = 120,
           tor: bool = False) -> List[Dict]:
    """对公开用户名做存在性快速枚举（默认不递归、低开销）。

    返回账号列表：{platform, url, username, fullname, site_rank,
                   http_status, confidence, source}
    未启用 / 未授权 / CLI 缺失 → 返回 []（search_web 安全降级）或上抛
    （直接调用时抛 CapabilityUnavailable/ConsentRequired）。
    """
    if not is_enabled(CAP_NAME):
        log.debug(f"[{CAP_NAME}] 未启用（默认 OFF），跳过")
        return []
    # 合规闸口（未授权上抛 ConsentRequired，由 search_web / pipeline 捕获降级）
    _consent_gate(consent)

    cli = _resolve_cli()
    # v0.16.x 契约：--csv 在 cwd 写 <user>.csv；--print-found 仅保留命中；
    # 站点数据输入 --json 绝不能误用。临时目录隔离产物。
    cmd = cli + [username, "--csv", "--print-found", "--timeout", str(max(5, int(timeout)))]
    if tor:
        cmd.append("--tor")

    with tempfile.TemporaryDirectory(prefix="infoseek_sherlock_") as workdir:
        try:
            proc = subprocess.run(
                cmd, cwd=workdir, capture_output=True, text=True, timeout=timeout)
        except FileNotFoundError:
            raise CapabilityUnavailable(CAP_NAME, "CLI 未安装（隔离 venv 未配置）")
        except subprocess.TimeoutExpired:
            raise CapabilityError(f"{CAP_NAME} 超时（>{timeout}s）", code=0)
        except Exception as e:
            raise CapabilityError(f"{CAP_NAME} 执行异常: {e}", code=0, cause=e)

        if proc.returncode != 0:
            log.warning(f"[{CAP_NAME}] CLI 返回 {proc.returncode}: "
                        f"{(proc.stderr or '')[:200]}")

        # csv 固定命名 <username>.csv，但 username 可能含文件系统特殊字符，
        # 故 glob 工作目录内唯一 *.csv（一次调用只查一个用户名）。
        import pathlib
        csv_files = sorted(pathlib.Path(workdir).glob("*.csv"))
        if not csv_files:
            log.debug(f"[{CAP_NAME}] 无 CSV 产物（可能 0 命中或 CLI 异常）")
            return []
        text = csv_files[0].read_text(encoding="utf-8", errors="replace")

    return _parse_csv(text, username)


def _parse_csv(text: str, queried_username: str = "") -> List[Dict]:
    """解析 sherlock --csv 产物。

    列（v0.16.x）：username,name,url_main,url_user,exists,
                   http_status,response_time_s
    仅纳入 exists=Claimed；username 回填为查询名（旧实现写死空串，
    导致下游 cross_platform_matches 统计失效）。
    """
    if not text or not text.strip():
        return []
    out: List[Dict] = []
    try:
        reader = csv.DictReader(io.StringIO(text))
        for row in reader:
            if not isinstance(row, dict):
                continue
            exists = (row.get("exists") or "").strip()
            take, conf = _STATUS_MAP.get(exists, (False, 0.0))
            url = (row.get("url_user") or "").strip()
            if not take or not url:
                continue
            try:
                http_status = int(row.get("http_status") or 0)
            except (TypeError, ValueError):
                http_status = 0
            out.append({
                "platform": (row.get("name") or "").strip(),
                "url": url,
                # 回填实际查询用户名（CSV 首列也带，优先用之，缺失再用入参）
                "username": (row.get("username") or queried_username or "").strip(),
                "fullname": "",
                "site_rank": 0,
                "http_status": http_status,
                "confidence": conf,
                "source": CAP_NAME,
            })
    except Exception as e:  # 结构异常不致命，返回已解析部分
        log.warning(f"[{CAP_NAME}] CSV 解析异常: {e}")
    return out


def search_web(username: str, **kw) -> List[Dict]:
    try:
        return search(username, **kw)
    except (ConsentRequired, CapabilityUnavailable, CapabilityError):
        return []
