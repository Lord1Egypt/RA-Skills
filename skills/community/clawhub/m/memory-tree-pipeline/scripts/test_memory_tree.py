#!/usr/bin/env python3
"""
Memory Tree Tests — Jarvis Symbiotic Claw

Tests the complete memory tree pipeline.

Usage:
    python3 test_memory_tree.py
"""

import importlib.util
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# ── Import modules via importlib (hyphenated filenames) ────────────────────────

SCRIPT_DIR = Path(__file__).parent.resolve()

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

seal_worker = load_module("seal_worker", SCRIPT_DIR / "seal-worker.py")
migrate_memory = load_module("migrate_memory", SCRIPT_DIR / "migrate-memory.py")
index_manager = load_module("index_manager", SCRIPT_DIR / "index-manager.py")
tools = load_module("tools_mod", SCRIPT_DIR / "tools.py")

# ── Test workspace ─────────────────────────────────────────────────────────────

TEST_DIR = Path(tempfile.mkdtemp(prefix="memory_tree_test_"))
TEST_MEMORY = TEST_DIR / "memory"
TEST_SOURCE = TEST_MEMORY / "source"
TEST_TOPIC = TEST_MEMORY / "topic"
TEST_GLOBAL = TEST_MEMORY / "global"
TEST_META = TEST_MEMORY / "_meta"
TEST_INDEX = TEST_META / "index.json"
TEST_BACKUP = TEST_MEMORY / "_backup_flat"

# ── Sample data ────────────────────────────────────────────────────────────────

SAMPLE_CONVERSATION = """# Daily Notes — 2026-05-22

## Stratium Theft Investigation
- Eric's Stratium account was compromised
- 2.198 SOL stolen through unauthorized withdrawals
- Attack vector: Telegram session compromise
- Lilo audit: our systems are CLEAN
- Security fixes applied: Gateway localhost, .env permissions

## Security Audit Results
- Network scan: all connections verified
- No keyloggers or C2 infrastructure found
- All SSH logins from known devices only
- JSC Gateway bound to localhost
- Homepage bound to localhost

## Model Routing Architecture
- coding -> qwen-coder + think
- reasoning -> deepseek-r1 + think
- chat -> qwen3-14b (no think)
- huge context -> glm-5.1:cloud
- Eric proposed middleware router for model selection
"""

SAMPLE_INFRASTRUCTURE = """# Daily Notes — 2026-05-21

## Service Recovery
- 4173 Command Center: restarted
- 3143 Website: restarted
- Cloudflare tunnel: restarted
- All services confirmed running

## Homepage Dashboard
- Port 3010, Docker container
- 14 services across 4 groups
- Dark theme matching JSC
- Docker integration working

## Device Fleet
- Desktop: ONLINE via Tailscale
- Surface Go: Awaiting Ubuntu install
- S21: ADB connected, battery 46%
- Razer Edge: ONLINE, battery 100%
"""

SAMPLE_TEAM = """# OpenClaw Team — May 21, 2026

## Department Updates
- Mario: CTO, leading Nova, Rex, Spark
- Nova: Infrastructure Engineer (servers, Docker, monitoring)
- Rex: Build & Release Engineer (CI/CD, APK, ROM)
- Spark: QA & Integration Tester (smoke tests, regression)

## Delegation Rules
1. Infrastructure tasks -> Nova
2. Build/release tasks -> Rex
3. QA/testing tasks -> Spark
4. UI/design tasks -> Frida
5. Security tasks -> Lilo
6. Mario reviews ALL team output
7. Escalation: Team -> Mario -> Jarvis -> Eric
"""

SAMPLE_DAILY = """# 2026-05-15 — Heavy Day

## JSC API Layer
- Architecture: Eric -> Open Jarvis -> JSC API (3132) -> JarvisOS Core -> Mini Claws
- Endpoints: POST /api/task, GET /api/health, GET /api/briefing
- Service: jsc-api.service (systemd, port 3132, localhost-only)
- Audit logging active

## Phase 7 — Adaptive Evolution Governance
- Observe -> Analyze -> Simulate -> Score -> Absorb selectively
- Engine: jsc-core/upgrade-intelligence/upgrade-engine.py
- Doctrine preservation: bounded_autonomy, simulation_first, deletion_approval
- Current versions: OpenClaw 2026.5.7, Ollama 0.23.2, Node v22.22.2

## Voice Configuration
- Ryan (en-GB-RyanNeural) — PRIMARY DEFAULT
- Thomas (en-GB-ThomasNeural) — AUTHORITY MODE
- Christopher (en-US-ChristopherNeural) — FALLBACK
- Eric preference: Ryan all the way (confirmed May 15, 2026)
"""


# ── Helpers ────────────────────────────────────────────────────────────────────

def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def load_json(path: Path, default=None):
    if not path.exists():
        return default if default is not None else {}
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default if default is not None else {}


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def setup_test_env():
    if TEST_MEMORY.exists():
        shutil.rmtree(TEST_MEMORY)
    for d in [TEST_SOURCE, TEST_TOPIC, TEST_GLOBAL, TEST_META]:
        d.mkdir(parents=True, exist_ok=True)
    (TEST_SOURCE / "2026-05-22-conversation.md").write_text(SAMPLE_CONVERSATION)
    (TEST_SOURCE / "2026-05-21-infrastructure.md").write_text(SAMPLE_INFRASTRUCTURE)
    (TEST_SOURCE / "2026-05-21-team.md").write_text(SAMPLE_TEAM)
    (TEST_SOURCE / "2026-05-15-daily.md").write_text(SAMPLE_DAILY)
    index = {"version": 1, "sources": {}, "source_to_topic": {}, "topics": {}, "global": {}, "last_seal": None}
    save_json(TEST_INDEX, index)
    return True


def cleanup_test_env():
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)


def patch_module(mod, test_dir: str):
    """Patch a module's path constants for testing."""
    mem = Path(test_dir) / "memory"
    patches = {}
    for attr in ["MEMORY_ROOT", "SOURCE_DIR", "TOPIC_DIR", "GLOBAL_DIR", "META_DIR", "INDEX_FILE", "SEALING_LOG"]:
        if hasattr(mod, attr):
            patches[attr] = getattr(mod, attr)

    mod.MEMORY_ROOT = mem
    mod.SOURCE_DIR = mem / "source"
    mod.TOPIC_DIR = mem / "topic"
    mod.GLOBAL_DIR = mem / "global"
    mod.META_DIR = mem / "_meta"
    mod.INDEX_FILE = mem / "_meta" / "index.json"
    if hasattr(mod, "SEALING_LOG"):
        mod.SEALING_LOG = mem / "_meta" / "sealing-log.json"
    if hasattr(mod, "WORKSPACE"):
        mod.WORKSPACE = Path(test_dir)
    if hasattr(mod, "MEMORY_MD"):
        mod.MEMORY_MD = Path(test_dir) / "MEMORY.md"
    if hasattr(mod, "BACKUP_DIR"):
        mod.BACKUP_DIR = mem / "_backup_flat"
    return patches


def restore_module(mod, patches: dict):
    """Restore a module's original path constants."""
    for attr, orig in patches.items():
        setattr(mod, attr, orig)


# ── Tests ──────────────────────────────────────────────────────────────────────

def test_detect_topics():
    print("Test: detect_topics...")
    assert "security" in seal_worker.detect_topics("security audit found vulnerability in infrastructure", "security-audit.md")
    assert "devices" in seal_worker.detect_topics("ADB connection to phone and tablet devices battery", "device-check.md")
    assert "team" in seal_worker.detect_topics("Mario CTO department delegation team evolution", "team-update.md")
    assert "misc" in seal_worker.detect_topics("random notes about lunch today", "lunch.md")
    print("  ✅ detect_topics passed")


def test_estimate_tokens():
    print("Test: estimate_tokens...")
    assert seal_worker.estimate_tokens("") == 1
    assert seal_worker.estimate_tokens("hello world") == 2
    assert seal_worker.estimate_tokens("x" * 4000) == 1000
    print("  ✅ estimate_tokens passed")


def test_extract_date():
    print("Test: extract_date_from_filename...")
    assert seal_worker.extract_date_from_filename("2026-05-22-conversation.md") == "2026-05-22"
    assert seal_worker.extract_date_from_filename("2026-05-15-daily.md") == "2026-05-15"
    print("  ✅ extract_date_from_filename passed")


def test_extract_headings():
    print("Test: extract_headings...")
    content = "# Main Title\n\n## Section One\n\nSome text\n\n### Sub-section\n\n## Section Two"
    headings = seal_worker.extract_headings(content)
    assert "Main Title" in headings
    assert "Section One" in headings
    print("  ✅ extract_headings passed")


def test_summarize_content():
    print("Test: summarize_content...")
    short = "This is short content."
    assert seal_worker.summarize_content(short, max_tokens=100) == short
    long_content = "## Heading\n\n" + "This is a paragraph. " * 500
    result = seal_worker.summarize_content(long_content, max_tokens=100)
    assert seal_worker.estimate_tokens(result) <= 120
    print("  ✅ summarize_content passed")


def test_seal_source():
    print("Test: seal_source...")
    setup_test_env()
    p = patch_module(seal_worker, str(TEST_DIR))

    try:
        index = load_json(TEST_INDEX)
        source_file = TEST_SOURCE / "2026-05-22-conversation.md"
        result = seal_worker.seal_source(source_file, index, dry_run=False)
        assert "topics" in result
        assert result["sealed_at"] is not None
        assert "sources" in index
        assert len(index["sources"]) > 0
        topic_files = list(TEST_TOPIC.glob("*.md"))
        assert len(topic_files) > 0
        print("  ✅ seal_source passed")
    finally:
        restore_module(seal_worker, p)


def test_seal_worker_idempotency():
    print("Test: seal_worker idempotency...")
    setup_test_env()
    p = patch_module(seal_worker, str(TEST_DIR))

    try:
        seal_worker.main()
        topic_files_1 = sorted(f.name for f in TEST_TOPIC.glob("*.md"))
        global_files_1 = sorted(f.name for f in TEST_GLOBAL.glob("*.md"))

        seal_worker.main()
        topic_files_2 = sorted(f.name for f in TEST_TOPIC.glob("*.md"))
        global_files_2 = sorted(f.name for f in TEST_GLOBAL.glob("*.md"))

        assert topic_files_1 == topic_files_2, f"Topics changed: {topic_files_1} vs {topic_files_2}"
        assert global_files_1 == global_files_2, f"Globals changed: {global_files_1} vs {global_files_2}"
        print("  ✅ seal_worker idempotency passed")
    finally:
        restore_module(seal_worker, p)


def test_global_knowledge_budget():
    print("Test: global knowledge budget...")
    setup_test_env()
    p = patch_module(seal_worker, str(TEST_DIR))

    try:
        seal_worker.main()
        for gf in TEST_GLOBAL.glob("*.md"):
            tokens = estimate_tokens(gf.read_text())
            assert tokens <= 5500, f"Global {gf.name} over budget: {tokens} tokens"
        for tf in TEST_TOPIC.glob("*.md"):
            tokens = estimate_tokens(tf.read_text())
            assert tokens <= 2500, f"Topic {tf.name} over budget: {tokens} tokens"
        print("  ✅ global knowledge budget passed")
    finally:
        restore_module(seal_worker, p)


def test_tools_recall():
    print("Test: tools.recall...")
    setup_test_env()
    p = patch_module(seal_worker, str(TEST_DIR))

    try:
        seal_worker.main()
    finally:
        restore_module(seal_worker, p)

    # Tools uses its own root, need to point it at test dir
    mt = tools.MemoryTree(root=str(TEST_MEMORY))
    results = mt.recall("stratium")
    assert len(results) > 0, f"Expected results for 'stratium', got {len(results)}"

    results = mt.recall("security", scope="topic")
    assert any(r["scope"] == "topic" for r in results), f"Expected topic results for 'security'"

    results = mt.recall("nonexistent_xyz_123")
    assert len(results) == 0, "Expected no results for nonexistent query"
    print("  ✅ tools.recall passed")


def test_tools_store():
    print("Test: tools.store...")
    setup_test_env()

    mt = tools.MemoryTree(root=str(TEST_MEMORY))
    path = mt.store("Important security update about infrastructure", source_type="conversation", topic_hint="security")
    assert path, "store() should return a path"
    assert Path(path).exists(), f"Stored file should exist at {path}"
    assert "2026-" in Path(path).name
    assert "security" in Path(path).name
    content = Path(path).read_text()
    assert "type: conversation" in content
    assert "topic_hint: security" in content
    print("  ✅ tools.store passed")


def test_tools_forget():
    print("Test: tools.forget...")
    setup_test_env()
    p = patch_module(seal_worker, str(TEST_DIR))

    try:
        seal_worker.main()
    finally:
        restore_module(seal_worker, p)

    mt = tools.MemoryTree(root=str(TEST_MEMORY))
    result = mt.forget("security", keep_source=True)
    assert result["removed_topic"] == True
    assert not (TEST_TOPIC / "security.md").exists()
    assert len(list(TEST_SOURCE.glob("*.md"))) > 0
    print("  ✅ tools.forget passed")


def test_tools_status():
    print("Test: tools.status...")
    setup_test_env()

    mt = tools.MemoryTree(root=str(TEST_MEMORY))
    status = mt.status()
    assert "source" in status
    assert "topic" in status
    assert "global" in status
    assert "sealed" in status
    assert "unsealed" in status
    assert status["source"]["count"] == 4
    assert status["unsealed"] == 4
    print("  ✅ tools.status passed")


def test_migration():
    print("Test: migration...")
    setup_test_env()

    memory_md = TEST_DIR / "MEMORY.md"
    memory_md.write_text("""# MEMORY.md — Test Content

## Symbiosis Doctrine
The ecosystem adapts to the user. Trust, consent, transparency.

## Security Rules
We scan OUR infrastructure. No exceptions.

## Voice Configuration
Ryan primary. Thomas authority mode.

## JSC API Layer
Port 3132. localhost-only. Audit logging active.
""")

    (TEST_MEMORY / "2026-05-22.md").write_text(SAMPLE_CONVERSATION)
    (TEST_MEMORY / "2026-05-21.md").write_text(SAMPLE_INFRASTRUCTURE)

    p = patch_module(migrate_memory, str(TEST_DIR))
    try:
        migrate_memory.main()
    finally:
        restore_module(migrate_memory, p)

    source_files = list(TEST_SOURCE.glob("*.md"))
    assert len(source_files) > 0, f"Expected source files, found {len(source_files)}"

    global_files = list(TEST_GLOBAL.glob("*.md"))
    assert len(global_files) > 0, f"Expected global files, found {len(global_files)}"

    assert TEST_BACKUP.exists(), "Backup should exist"
    assert TEST_INDEX.exists(), "Index should exist"
    assert (TEST_MEMORY / "2026-05-22.md").exists(), "Original daily file preserved"
    assert memory_md.exists(), "MEMORY.md preserved"
    print("  ✅ migration passed")


def test_index_manager_reindex():
    print("Test: index_manager reindex...")
    setup_test_env()
    p = patch_module(index_manager, str(TEST_DIR))

    try:
        index_manager.cmd_reindex()
        assert TEST_INDEX.exists()
        index = load_json(TEST_INDEX)
        assert "sources" in index
        assert "version" in index
        assert index["version"] == 1
        print("  ✅ index_manager reindex passed")
    finally:
        restore_module(index_manager, p)


def test_index_manager_verify():
    print("Test: index_manager verify...")
    setup_test_env()
    p_sw = patch_module(seal_worker, str(TEST_DIR))
    p_im = patch_module(index_manager, str(TEST_DIR))

    try:
        seal_worker.main()
        result = index_manager.cmd_verify()
        assert result is not None
        print("  ✅ index_manager verify passed")
    finally:
        restore_module(seal_worker, p_sw)
        restore_module(index_manager, p_im)


# ── Main ───────────────────────────────────────────────────────────────────────

def run_all_tests():
    test_funcs = [
        test_detect_topics,
        test_estimate_tokens,
        test_extract_date,
        test_extract_headings,
        test_summarize_content,
        test_seal_source,
        test_seal_worker_idempotency,
        test_global_knowledge_budget,
        test_tools_recall,
        test_tools_store,
        test_tools_forget,
        test_tools_status,
        test_migration,
        test_index_manager_reindex,
        test_index_manager_verify,
    ]

    print("=" * 60)
    print("Memory Tree Test Suite — Jarvis Symbiotic Claw")
    print("=" * 60)
    print()

    passed = 0
    failed = 0

    for test in test_funcs:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  ❌ {test.__name__} FAILED: {e}")
            import traceback
            traceback.print_exc()

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {len(test_funcs)} total")
    print("=" * 60)

    cleanup_test_env()

    if failed > 0:
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    run_all_tests()