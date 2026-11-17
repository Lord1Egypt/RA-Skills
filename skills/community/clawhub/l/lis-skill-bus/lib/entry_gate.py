#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""entry_gate.py — 算量技能统一入口依赖闸门（纯 stdlib，不联网）。

正式链路固定为::

    cad-file-reader -> cad-contract/v1 -> lis-skill-bus -> 算量技能

本模块只回答“现在能不能进入这条链路”，不解析 DWG/DXF，不下载依赖，也不
自动安装任何东西。五个算量技能都 vendored 此文件，因而即使 bus 整包缺失，
主入口仍能稳定返回 21，而不是抛普通 ImportError。

退出码
------
20  缺 cad-file-reader 或版本 < 0.41.0
21  缺 lis-skill-bus 或版本 < 0.1.11
22  契约无效（版本/结构/来源/哈希/单位等 contract_guard 1-4）
23  直接传 DWG/DXF/DWT 等图纸
24  只有手工来源却要求正式量，或契约证据不足（contract_guard 5）

测试沙箱
--------
设置 ``CODEX_SKILLS_ROOT`` 后只搜索该目录，不回落到真实 $HOME/.codex/skills、
~/.claude/skills 或 WorkBuddy。格式::

    CODEX_SKILLS_ROOT=/tmp/sandbox python3 - <<'PY'
    from entry_gate import require_reader, require_bus
    require_reader(); require_bus()
    PY

本文件 vendored 到各技能 scripts/ 时，文件头会额外记录 canonical 源 SHA-256；
修改时先改 canonical，再同步副本，不允许各技能私改行为。
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

GATE_VERSION = "1.0.0"
READER_MIN = "0.41.0"
BUS_MIN = "0.1.11"
DRAWING_SUFFIXES = frozenset({".dwg", ".dxf", ".dwt"})
DRAWING_REJECT_MESSAGE = (
    "本技能不直接识图，请先安装并调用 cad-file-reader 生成 cad-contract.json，"
    "再经 lis-skill-bus 传入；不许 fallback 到内置解析。"
)
INSTALL_HINT = (
    "skillhub install cad-file-reader --namespace user_43faedd6\n"
    "bash ${CODEX_HOME:-$HOME/.codex}/skills/lis-skill-bus/install_skillbus.sh --apply"
)
_VERSION_RE = re.compile(r"^[0-9]+(?:\.[0-9]+)*$")


class GateError(Exception):
    """入口闸门错误；code 是稳定退出码。"""

    def __init__(self, code: int, message: str, hint: str = "",
                 *, cause_code: int | None = None) -> None:
        super().__init__(message)
        self.code = int(code)
        self.message = str(message)
        self.hint = str(hint or "")
        self.cause_code = cause_code

    def __str__(self) -> str:
        text = "[ENTRY_GATE %d] %s" % (self.code, self.message)
        if self.hint:
            text += "\n修复: " + self.hint
        return text


# --------------------------------------------------------------------------- #
# 路径与版本
# --------------------------------------------------------------------------- #
def _sandbox_root() -> Path | None:
    raw = str(os.environ.get("CODEX_SKILLS_ROOT") or "").strip()
    if not raw:
        return None
    return Path(raw).expanduser().resolve()


def _default_roots() -> list[Path]:
    return [
        Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex")) / "skills",
        Path.home() / ".codex" / "skills",
        Path.home() / ".claude" / "skills",
    ]


def _candidate_paths(slug: str) -> list[Path]:
    sandbox = _sandbox_root()
    if sandbox is not None:
        # 沙箱优先即唯一来源；绝不回落真实技能目录。
        return [sandbox / slug]
    out: list[Path] = []
    if slug == "cad-file-reader":
        for key in ("CAD_FILE_READER_HOME", "CAD_SKILL_DIR"):
            raw = str(os.environ.get(key) or "").strip()
            if raw:
                out.append(Path(raw).expanduser())
    elif slug == "lis-skill-bus":
        raw = str(os.environ.get("SKILLBUS_HOME") or "").strip()
        if raw:
            out.append(Path(raw).expanduser())
    out.extend(root / slug for root in _default_roots())
    if slug == "cad-file-reader":
        out.extend(sorted(Path.home().glob(".workbuddy/skills/*/cad-file-reader")))
    return out


def _is_skill_root(path: Path) -> bool:
    return path.is_dir() and ((path / "scripts").is_dir() or (path / "SKILL.md").is_file())


def _find(slug: str) -> Path | None:
    seen: set[str] = set()
    for path in _candidate_paths(slug):
        try:
            resolved = path.resolve()
        except OSError:
            continue
        key = str(resolved)
        if key in seen:
            continue
        seen.add(key)
        if _is_skill_root(resolved):
            return resolved
    return None


def _read_version(root: Path) -> str:
    for name in ("manifest.json", "_meta.json"):
        try:
            data = json.loads((root / name).read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        value = str(data.get("version") or "").strip()
        if value:
            return value
    for rel in (Path("skillbus.py"), Path("scripts") / "skillbus.py"):
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except Exception:
            continue
        match = re.search(r'(?m)^\s*VERSION\s*=\s*["\']([0-9][^"\']*)["\']', text)
        if match:
            return match.group(1).strip()
    return ""


def _vt(text: str) -> tuple[int, ...] | None:
    text = str(text or "").strip()
    if not _VERSION_RE.match(text):
        return None
    return tuple(int(x) for x in text.split("."))


def _at_least(actual: str, minimum: str) -> bool:
    a, m = _vt(actual), _vt(minimum)
    if a is None or m is None:
        return False
    width = max(len(a), len(m))
    return a + (0,) * (width - len(a)) >= m + (0,) * (width - len(m))


def resolve_reader() -> tuple[Path | None, str]:
    root = _find("cad-file-reader")
    return root, (_read_version(root) if root is not None else "")


def resolve_bus() -> tuple[Path | None, str]:
    root = _find("lis-skill-bus")
    return root, (_read_version(root) if root is not None else "")


# --------------------------------------------------------------------------- #
# 闸门
# --------------------------------------------------------------------------- #
def require_reader() -> dict:
    """要求 cad-file-reader>=0.41.0；失败抛 GateError(20)。"""
    root, version = resolve_reader()
    if root is None:
        raise GateError(
            20,
            "缺少 cad-file-reader（要求 >=%s），已停止，不自行解图。" % READER_MIN,
            INSTALL_HINT,
        )
    if not _at_least(version, READER_MIN):
        shown = version or "版本无法识别"
        raise GateError(
            20,
            "cad-file-reader 版本 %s < %s（%s），已停止。" % (shown, READER_MIN, root),
            INSTALL_HINT,
        )
    return {"name": "cad-file-reader", "path": str(root), "version": version,
            "minimum": READER_MIN}


def require_bus() -> dict:
    """要求 lis-skill-bus>=0.1.11；失败抛 GateError(21)。"""
    root, version = resolve_bus()
    if root is None:
        raise GateError(
            21,
            "缺少 lis-skill-bus（要求 >=%s），不能建立可追溯的契约接线。" % BUS_MIN,
            INSTALL_HINT,
        )
    if not _at_least(version, BUS_MIN):
        shown = version or "版本无法识别"
        raise GateError(
            21,
            "lis-skill-bus 版本 %s < %s（%s），已停止。" % (shown, BUS_MIN, root),
            INSTALL_HINT,
        )
    return {"name": "lis-skill-bus", "path": str(root), "version": version,
            "minimum": BUS_MIN}


def reject_drawing_input(*values) -> None:
    """任何 DWG/DXF/DWT 输入直接 GateError(23)，不尝试打开或嗅探。"""
    for value in values:
        if value is None:
            continue
        if isinstance(value, (list, tuple, set)):
            reject_drawing_input(*value)
            continue
        suffix = Path(str(value)).suffix.lower()
        if suffix in DRAWING_SUFFIXES:
            raise GateError(23, DRAWING_REJECT_MESSAGE, INSTALL_HINT)


def _contract_guard_module():
    try:
        import contract_guard  # type: ignore
        return contract_guard
    except Exception as exc:  # pragma: no cover - canonical/vendored 安装损坏
        raise GateError(
            22,
            "入口闸门找不到同目录 contract_guard.py，无法校验契约：%s" % exc,
            "重新安装当前技能，确保 contract_guard.py 与 entry_gate.py 同目录。",
            cause_code=1,
        ) from None


def require_contract(path, *, allow_manual: bool = False,
                     require_formal: bool = False,
                     require_hash: bool = True,
                     required_keys=(),
                     expected_schema: str = "cad-contract/v1",
                     evidence_ok: bool = True) -> dict:
    """校验 cad-contract/v1 并返回 guard 结果。

    * contract_guard 1-4 -> GateError(22)
    * contract_guard 5   -> GateError(24)（证据不足）
    * 手工来源 + require_formal=True -> GateError(24)
    * evidence_ok=False -> GateError(24)
    """
    if not evidence_ok:
        raise GateError(
            24,
            "输入证据不足，禁止输出正式量；请回到 cad-file-reader 补齐契约证据。",
            INSTALL_HINT,
        )
    cg = _contract_guard_module()
    try:
        guard = cg.guard_contract(
            path,
            allow_manual=bool(allow_manual),
            expected_schema=expected_schema,
            required_keys=tuple(required_keys or ()),
            require_hash=bool(require_hash),
        )
    except cg.GuardError as exc:
        code = 24 if int(getattr(exc, "code", 0) or 0) == 5 else 22
        label = "契约证据不足" if code == 24 else "契约无效"
        raise GateError(
            code,
            "%s（contract_guard code %s）：%s" % (
                label, getattr(exc, "code", "?"), getattr(exc, "message", str(exc))),
            str(getattr(exc, "hint", "") or INSTALL_HINT),
            cause_code=int(getattr(exc, "code", 0) or 0),
        ) from None
    except Exception as exc:
        raise GateError(
            22,
            "契约校验异常：%s: %s" % (type(exc).__name__, exc),
            INSTALL_HINT,
            cause_code=1,
        ) from None
    if require_formal and guard.get("mode") != "formal":
        raise GateError(
            24,
            "当前只有手工来源（provenance=%s），禁止输出正式量；"
            "请用 cad-file-reader 生成、经 lis-skill-bus 按 contract_id 传入。"
            % (guard.get("provenance") or "manual"),
            "正式入口：先 cad-file-reader 生成 cad-contract/v1，再经 lis-skill-bus 传入；"
            "临时降级必须显式 --allow-manual，且结果 final_quantity=false。",
            cause_code=3,
        )
    return guard


def format_gate_error(exc: GateError) -> str:
    return str(exc)


def print_gate_error(exc: GateError, stream=None) -> int:
    stream = stream or sys.stderr
    stream.write(str(exc) + "\n")
    return exc.code


def dependency_snapshot() -> dict:
    """只读快照，供 --check-deps 展示；不抛异常，不安装。"""
    reader_root, reader_version = resolve_reader()
    bus_root, bus_version = resolve_bus()
    reader_ok = reader_root is not None and _at_least(reader_version, READER_MIN)
    bus_ok = bus_root is not None and _at_least(bus_version, BUS_MIN)
    return {
        "ok": bool(reader_ok and bus_ok),
        "cad_file_reader": {
            "found": reader_root is not None,
            "path": str(reader_root or ""),
            "version": reader_version,
            "minimum": READER_MIN,
            "ok": reader_ok,
        },
        "lis_skill_bus": {
            "found": bus_root is not None,
            "path": str(bus_root or ""),
            "version": bus_version,
            "minimum": BUS_MIN,
            "ok": bus_ok,
        },
    }


def dependency_exit_code() -> int:
    """依赖体检的稳定退出码：0 就绪 / 20 缺 reader / 21 缺 bus。"""
    snap = dependency_snapshot()
    if not snap["cad_file_reader"]["ok"]:
        return 20
    if not snap["lis_skill_bus"]["ok"]:
        return 21
    return 0


__all__ = [
    "GATE_VERSION", "READER_MIN", "BUS_MIN", "DRAWING_REJECT_MESSAGE",
    "GateError", "resolve_reader", "resolve_bus", "require_reader", "require_bus",
    "require_contract", "reject_drawing_input", "dependency_snapshot",
    "dependency_exit_code",
    "format_gate_error", "print_gate_error",
]
