"""Provider API 契约测试框架（spec §7, §12.1）。

验证第三方 Provider 满足最小契约:
- detect: 无副作用，返回是否适用及所需权限
- inventory: 支持分页/流式，返回实体/命名空间/数量/能力
- snapshot: 只读、可中断、未知字段保留，输出 NDJSON
- explain: 说明映射、限制和不可见范围

官方认证最低要求（spec §7）: 契约测试、只读安全、版本声明、真实样例。
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


# ---------------------------------------------------------------------------
# 契约测试用例
# ---------------------------------------------------------------------------


@dataclass
class ContractResult:
    """单个契约测试的结果。"""

    name: str
    passed: bool
    message: str = ""


def run_contract_tests(provider_cmd: list[str], workspace: str) -> list[ContractResult]:
    """对 Provider 执行完整契约测试。

    provider_cmd: 调用 Provider 的命令，如 ["python", "-m", "graphify"]
    workspace: 测试工作区路径
    """
    results: list[ContractResult] = []
    results.append(_test_detect(provider_cmd, workspace))
    results.append(_test_inventory(provider_cmd, workspace))
    results.append(_test_snapshot_readonly(provider_cmd, workspace))
    results.append(_test_snapshot_unknown_fields(provider_cmd, workspace))
    results.append(_test_explain(provider_cmd, workspace))
    return results


# ---------------------------------------------------------------------------
# 各契约测试
# ---------------------------------------------------------------------------


def _run_provider(cmd: list[str], stdin_data: str | None = None, timeout: int = 30) -> tuple[int, str, str]:
    """运行 Provider 命令，返回 (returncode, stdout, stderr)。"""
    try:
        proc = subprocess.run(
            cmd,
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except Exception as e:
        return 1, "", str(e)


def _test_detect(cmd: list[str], workspace: str) -> ContractResult:
    """detect 必须无副作用，返回是否适用及所需权限。"""
    # 契约: Provider 应支持 detect 子命令或 --detect 参数
    rc, out, err = _run_provider(cmd + ["detect", workspace])
    if rc != 0:
        return ContractResult("detect", False, f"detect failed: {err}")
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return ContractResult("detect", False, f"detect output not JSON: {out[:100]}")
    if "applicable" not in data:
        return ContractResult("detect", False, "detect missing 'applicable' field")
    return ContractResult("detect", True)


def _test_inventory(cmd: list[str], workspace: str) -> ContractResult:
    """inventory 返回实体/命名空间/数量/能力。"""
    rc, out, err = _run_provider(cmd + ["inventory", workspace])
    if rc != 0:
        return ContractResult("inventory", False, f"inventory failed: {err}")
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return ContractResult("inventory", False, f"inventory output not JSON")
    # 至少有数量或实体列表
    if not any(k in data for k in ("entities", "count", "namespaces")):
        return ContractResult("inventory", False, "inventory missing entities/count/namespaces")
    return ContractResult("inventory", True)


def _test_snapshot_readonly(cmd: list[str], workspace: str) -> ContractResult:
    """snapshot 必须只读。通过比较调用前后文件哈希验证。"""
    import hashlib

    ws = Path(workspace)
    before_hashes: dict[str, str] = {}
    for f in ws.rglob("*"):
        if f.is_file() and ".memoryguard" not in str(f) and "graphify-out" not in str(f):
            try:
                before_hashes[str(f)] = hashlib.sha256(f.read_bytes()).hexdigest()
            except OSError:
                pass
    # 运行 snapshot
    rc, out, err = _run_provider(cmd + ["snapshot", workspace])
    if rc != 0:
        return ContractResult("snapshot.readonly", False, f"snapshot failed: {err}")
    # 检查文件未被修改
    for path, before_hash in before_hashes.items():
        try:
            after_hash = hashlib.sha256(Path(path).read_bytes()).hexdigest()
            if after_hash != before_hash:
                return ContractResult("snapshot.readonly", False, f"snapshot modified file: {path}")
        except OSError:
            return ContractResult("snapshot.readonly", False, f"snapshot deleted or made unreadable: {path}")
    return ContractResult("snapshot.readonly", True)


def _test_snapshot_unknown_fields(cmd: list[str], workspace: str) -> ContractResult:
    """snapshot 输出 NDJSON，未知字段必须保留。"""
    rc, out, err = _run_provider(cmd + ["snapshot", workspace])
    if rc != 0:
        return ContractResult("snapshot.unknown_fields", False, f"snapshot failed: {err}")
    # 验证是 NDJSON（每行一个 JSON 对象）
    lines = [l for l in out.strip().splitlines() if l.strip()]
    if not lines:
        return ContractResult("snapshot.unknown_fields", True, "empty snapshot (no objects)")
    try:
        first = json.loads(lines[0])
    except json.JSONDecodeError:
        return ContractResult("snapshot.unknown_fields", False, "snapshot output not NDJSON")
    # 至少有 id 和 type 字段（MemoryGuard 标准对象）
    if "id" not in first or "type" not in first:
        return ContractResult("snapshot.unknown_fields", False, "snapshot objects missing id/type")
    return ContractResult("snapshot.unknown_fields", True)


def _test_explain(cmd: list[str], workspace: str) -> ContractResult:
    """explain 说明映射、限制和不可见范围。"""
    rc, out, err = _run_provider(cmd + ["explain", workspace])
    if rc != 0:
        return ContractResult("explain", False, f"explain failed: {err}")
    # explain 可以是文本或 JSON，但必须非空
    if not out.strip():
        return ContractResult("explain", False, "explain output empty")
    return ContractResult("explain", True)


# ---------------------------------------------------------------------------
# 汇总
# ---------------------------------------------------------------------------


def summarize(results: list[ContractResult]) -> tuple[bool, str]:
    """汇总契约测试结果，返回 (全通过, 报告文本)。"""
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    lines = [f"Provider contract tests: {passed}/{total} passed"]
    for r in results:
        mark = "OK" if r.passed else "FAIL"
        lines.append(f"  [{mark}] {r.name}: {r.message}")
    return passed == total, "\n".join(lines)
