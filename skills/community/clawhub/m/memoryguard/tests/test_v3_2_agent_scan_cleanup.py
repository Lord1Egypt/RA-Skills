"""v3.2 Agent 扫描 + stale 检测 + 清理流程测试。"""
from __future__ import annotations

import os
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from memoryguard.agent_mapping import (
    AGENT_PRODUCT_MAP, detect_stale_status,
    STALE_THRESHOLD_SECONDS, LIKELY_UNINSTALLED_THRESHOLD_SECONDS,
    product_for_dot_dir, is_known_product,
)
from memoryguard.agent_cleanup import AgentCleanup
from memoryguard.gui import GovernanceApi


def _check(label: str, ok: bool, detail: str = "") -> bool:
    status = "PASS" if ok else "FAIL"
    msg = f"[{status}] {label}"
    if detail:
        msg += f" :: {detail}"
    print(msg)
    return ok


def main() -> int:
    all_pass = True

    print("\n=== 1. 映射表覆盖国产 Agent ===")
    products = {v for v in AGENT_PRODUCT_MAP.values()}
    all_pass &= _check("trae 已映射", "trae" in products)
    all_pass &= _check("zcode 已映射", "zcode" in products)
    all_pass &= _check("echobird 已映射", "echobird" in products)
    all_pass &= _check("claude-code 已映射", "claude-code" in products)
    all_pass &= _check("windsurf 已映射", "windsurf" in products)
    all_pass &= _check("product_for_dot_dir", product_for_dot_dir(".trae-cn") == "trae")
    all_pass &= _check("未知目录返回 None", product_for_dot_dir(".unknown-thing") is None)

    print("\n=== 2. stale 检测：active ===")
    with tempfile.TemporaryDirectory() as tmp:
        active_dir = Path(tmp) / ".active-agent"
        active_dir.mkdir()
        (active_dir / "config.json").write_text("{}", encoding="utf-8")
        # 设置 mtime 为当前时间
        os.utime(active_dir, (time.time(), time.time()))
        stale = detect_stale_status(active_dir)
        all_pass &= _check("active 目录 -> active", stale["stale_status"] == "active",
                           f"status={stale['stale_status']}, days={stale['days_since_modified']}")

    print("\n=== 3. stale 检测：stale (30+ 天) ===")
    with tempfile.TemporaryDirectory() as tmp:
        stale_dir = Path(tmp) / ".stale-agent"
        stale_dir.mkdir()
        (stale_dir / "config.json").write_text("{}", encoding="utf-8")
        old_time = time.time() - (35 * 24 * 3600)  # 35 天前
        os.utime(stale_dir, (old_time, old_time))
        os.utime(stale_dir / "config.json", (old_time, old_time))
        stale = detect_stale_status(stale_dir)
        all_pass &= _check("35 天前 -> stale", stale["stale_status"] == "stale",
                           f"status={stale['stale_status']}, days={stale['days_since_modified']}")

    print("\n=== 4. stale 检测：likely_uninstalled (60+ 天) ===")
    with tempfile.TemporaryDirectory() as tmp:
        uninstalled_dir = Path(tmp) / ".old-agent"
        uninstalled_dir.mkdir()
        (uninstalled_dir / "config.json").write_text("{}", encoding="utf-8")
        old_time = time.time() - (65 * 24 * 3600)  # 65 天前
        os.utime(uninstalled_dir, (old_time, old_time))
        os.utime(uninstalled_dir / "config.json", (old_time, old_time))
        stale = detect_stale_status(uninstalled_dir)
        all_pass &= _check("65 天前 -> likely_uninstalled",
                           stale["stale_status"] == "likely_uninstalled",
                           f"status={stale['stale_status']}, days={stale['days_since_modified']}")

    print("\n=== 5. stale 检测：有可执行文件不标 stale ===")
    with tempfile.TemporaryDirectory() as tmp:
        exe_dir = Path(tmp) / ".exe-agent"
        exe_dir.mkdir()
        exe_file = exe_dir / "agent.exe"
        exe_file.write_text("fake", encoding="utf-8")
        old_time = time.time() - (90 * 24 * 3600)  # 90 天前
        os.utime(exe_dir, (old_time, old_time))
        os.utime(exe_file, (old_time, old_time))
        stale = detect_stale_status(exe_dir)
        all_pass &= _check("有 .exe 但 90 天 -> active（has_executable=True）",
                           stale["stale_status"] == "active",
                           f"status={stale['stale_status']}, has_executable={stale['has_executable']}")

    print("\n=== 6. 清理：标记/取消标记 uninstalled ===")
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        api = GovernanceApi(str(workspace))
        marked = api.mark_agent_uninstalled("test-agent", dir_path="/fake/path", reason="test")
        all_pass &= _check("标记成功", marked.get("marked_uninstalled") is True)
        uninstalled_file = workspace / ".memoryguard" / "cleanup" / "uninstalled.json"
        all_pass &= _check("uninstalled.json 存在", uninstalled_file.exists())
        unmarked = api.unmark_agent_uninstalled("test-agent")
        all_pass &= _check("取消标记成功", unmarked.get("marked_uninstalled") is False)
        history = api.list_cleanup_history()
        all_pass &= _check("历史含 mark + unmark", len(history.get("history", [])) >= 2,
                           f"count={len(history.get('history', []))}")

    print("\n=== 7. 清理：归档/恢复 ===")
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        api = GovernanceApi(str(workspace))
        agent_dir = workspace / ".fake-agent"
        agent_dir.mkdir()
        (agent_dir / "memory.json").write_text("{}", encoding="utf-8")
        archived = api.archive_agent_dir("fake-agent", str(agent_dir), reason="cleanup test")
        all_pass &= _check("归档成功", archived.get("ok") is True)
        all_pass &= _check("原目录已移走", not agent_dir.exists())
        archive_id = archived.get("archive_id", "")
        restored = api.restore_archived_agent(archive_id)
        all_pass &= _check("恢复成功", restored.get("ok") is True)
        all_pass &= _check("原目录已恢复", agent_dir.exists())
        archives = api.list_archived_agents()
        all_pass &= _check("归档列表有记录", archives.get("total", 0) >= 1)

    print("\n=== 8. 候选列表 API（通过 GovernanceApi） ===")
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        api = GovernanceApi(str(workspace))
        # list_agent_candidates 扫的是真实 Path.home()，只验证 API 不崩溃
        candidates = api.list_agent_candidates()
        all_pass &= _check("候选 API 返回列表", isinstance(candidates.get("candidates"), list))
        all_pass &= _check("候选含 total 字段", "total" in candidates)

    print("\n" + "=" * 50)
    if all_pass:
        print("All v3.2 Agent scan + cleanup tests PASSED")
        return 0
    print("Some Agent scan + cleanup tests FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
