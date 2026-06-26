#!/usr/bin/env python3
"""memory-guardian: Unified CLI entry point (v0.4).

Commands:
  status        — Health check (compact + dedup + decay)
  ingest        — Add a new memory/case
  bootstrap     — Extract memories from existing .md files
  snapshot      — Diff MEMORY.md against last snapshot
  run           — Full maintenance cycle (status + snapshot)
  violations    — Check violation patterns & rule health
  violations-health — Show violation rule health summary
  vlog          — Log a violation event
  revise        — Mark rule as revised
  rescan        — Re-extract entities for all memories
  migrate       — Migrate meta.json v0.3 → v0.4
  security      — Security constraint layer (extract/check/save/list)
  case-grow     — Case self-growth engine (Phase 2)

Designed to be called from SKILL.md or heartbeat.
"""
import argparse
import importlib.util
import logging
import os
import subprocess
import sys
from datetime import datetime, timedelta
from types import ModuleType
from mg_utils import _now_iso, CST, load_meta, read_text_file, safe_print, workspace_path, DEFAULT_WORKSPACE
from mg_schema import normalize_meta, MEMORY_DEFAULTS, SCHEMA_VERSION
from mg_events.telemetry import record_module_run

print = safe_print

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def run_script(name, args, workspace):
    """Run a guardian script and return its output."""
    script = os.path.join(SCRIPT_DIR, name)
    if not os.path.exists(script):
        return f"[ERROR] Script not found: {name}"
    cmd = [sys.executable, script] + args + ["--workspace", workspace]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        if result.returncode == 0:
            return result.stdout

        error_text = (result.stderr or "").strip() or (result.stdout or "").strip()
        if not error_text:
            return f"[ERROR] {name} exited with code {result.returncode}"
        return error_text if error_text.startswith("[ERROR]") else f"[ERROR] {error_text}"
    except subprocess.TimeoutExpired:
        return "[ERROR] Script timed out"


def emit_result(result):
    """Print deferred string results while ignoring already-emitted structured values."""
    if isinstance(result, str) and result:
        print(result)



def add_option(args_list, flag, value):
    """Append one flag/value pair when value is present."""
    if value is None or value == "":
        return
    args_list += [flag, str(value)]



def add_flag(args_list, flag, enabled):
    """Append one boolean flag when enabled."""
    if enabled:
        args_list.append(flag)



def add_csv_option(args_list, flag, values):
    """Append one comma-separated option when values are present."""
    if values:
        args_list += [flag, ",".join(values)]



def run_and_print(name, args, workspace):
    """Run a child script and print its text result immediately."""
    emit_result(run_script(name, args, workspace))


def _load_local_module(module_name, script_name) -> tuple[ModuleType | None, str | None]:
    """Load one repository script as a Python module with defensive checks."""
    script_path = os.path.join(SCRIPT_DIR, script_name)
    if not os.path.exists(script_path):
        return None, f"[ERROR] Script not found: {script_name}"

    try:
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        if spec is None or spec.loader is None:
            return None, f"[ERROR] Failed to load module: {script_name}"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module, None
    except Exception as e:
        return None, f"[ERROR] Failed to load module {script_name}: {e}"


def save_meta(path, meta):
    from mg_utils import save_meta as _save
    _save(path, meta)


def load_normalized_meta(path, persist=False):
    """Load meta.json and normalize schema aliases/defaults."""
    meta = load_meta(path)
    normalized, changed = normalize_meta(meta)
    if persist and changed:
        save_meta(path, normalized)
    return normalized


def workspace_memory_count(workspace):
    """Return number of memories in workspace meta.json."""
    meta_path = workspace_path("memory", "meta.json", workspace=workspace)
    if not os.path.exists(meta_path):
        return 0
    meta = load_normalized_meta(meta_path, persist=True)
    return len(meta.get("memories", []))


# ─── Existing Commands ───────────────────────────────────────

def cmd_rescan(workspace):
    """Re-extract entities for all memories that have empty entities."""
    mod, error = _load_local_module("memory_ingest", "memory_ingest.py")
    if mod is None:
        print(error)
        return

    meta_path = os.path.join(workspace, "memory", "meta.json")
    if not os.path.exists(meta_path):
        print("No meta.json found. Run bootstrap first.")
        return

    meta = load_normalized_meta(meta_path, persist=True)

    updated = 0
    total_entities = 0
    for mem in meta.get("memories", []):
        content = mem.get("content", "")
        entities = mod.extract_entities(content)
        old_count = len(mem.get("entities", []))
        mem["entities"] = entities
        new_count = len(entities)
        if new_count != old_count:
            updated += 1
            total_entities += new_count
            if new_count > 0:
                print(f"  [{mem['id']}] {old_count} → {new_count} entities")

    save_meta(meta_path, meta)
    print(f"\nRescan complete: {updated} memories updated, {total_entities} entities total")


def cmd_status(workspace):
    """Combined health report."""
    workspace = workspace_path(workspace=workspace)
    print("=" * 60)
    print(f"MEMORY GUARDIAN v0.4 — Status Report")
    print(f"  Time: {datetime.now(CST).strftime('%Y-%m-%d %H:%M')}")
    print(f"  Workspace: {workspace}")
    print("=" * 60)

    meta_path = workspace_path("memory", "meta.json", workspace=workspace)
    if os.path.exists(meta_path):
        meta = load_normalized_meta(meta_path, persist=True)
        version = meta.get("version", meta.get("schema_version", "unknown"))
        memories = meta.get("memories", [])
        status_counts = {}
        for m in memories:
            s = m.get("status", "unknown")
            status_counts[s] = status_counts.get(s, 0) + 1
        case_count = sum(1 for m in memories if m.get("id", "").startswith("case_"))
        print(f"\n📁 meta.json: v{version}, {len(memories)} memories ({case_count} cases)")
        for s, c in sorted(status_counts.items()):
            icon = {"active": "🟢", "archived": "📦", "deleted": "🗑️", "draft": "📝", "observing": "👁️", "suspended": "⏸️"}.get(s, "❓")
            print(f"   {icon} {s}: {c}")

        # Security rules
        sec_rules = meta.get("security_rules", [])
        if sec_rules:
            print(f"   🔒 Security rules: {len(sec_rules)}")

        # Conflicts
        conflicts = meta.get("conflicts", [])
        if conflicts:
            print(f"   ⚡ Conflicts: {len(conflicts)}")
    else:
        print(f"\n⚠️  meta.json not found — run 'bootstrap' to initialize")

    print("\n" + "─" * 40)
    print("Compaction Analysis:")
    print("─" * 40)
    print(run_script("memory_compact.py", [], workspace))

    print("─" * 40)
    print("Dedup Check:")
    print("─" * 40)
    print(run_script("memory_dedup.py", [], workspace))

    print("─" * 40)
    print("Decay (five-track, dry-run):")
    print("─" * 40)
    print(run_script("memory_decay.py", ["--dry-run"], workspace))


def cmd_ingest(content, importance, tags, workspace, **kwargs):
    """Ingest a new memory/case."""
    args = []
    add_option(args, "--content", content)
    add_option(args, "--importance", importance)
    add_csv_option(args, "--tags", tags)
    # v0.4 case fields
    for field in ["situation", "judgment", "consequence", "action_conclusion"]:
        add_option(args, f"--{field.replace('_', '-')}", kwargs.get(field))
    add_option(args, "--reversibility", kwargs.get("reversibility"))
    add_csv_option(args, "--boundary-words", kwargs.get("boundary_words"))
    add_csv_option(args, "--alternatives", kwargs.get("alternatives"))
    add_option(args, "--update", kwargs.get("update"))
    add_option(args, "--provenance-source", kwargs.get("provenance_source"))
    run_and_print("memory_ingest.py", args, workspace)


def cmd_bootstrap(workspace):
    """Full first-run setup: create directories, parse files, build meta.json.

    Bootstrap handles everything needed for a fresh workspace:
    1. Create category directory structure (project/social/tech/personal/misc)
    2. Parse MEMORY.md sections into structured memories
    3. Parse daily notes (any heading format) into structured memories
    3.5 Clean up MEMORY.md — remove ingested sections, keep index + quick-reference
    4. Generate memory_id + file_path for each memory
    5. Apply v0.4.5 schema defaults
    6. Save meta.json
    """
    import re, uuid

    workspace = workspace_path(workspace=workspace)
    meta_path = workspace_path("memory", "meta.json", workspace=workspace)
    if os.path.exists(meta_path):
        print("meta.json already exists. Remove it first to re-bootstrap.")
        print(f"  Path: {meta_path}")
        return

    # --- Step 0: Create directory structure ---
    MEMORY_DIRS = [
        "memory/project",
        "memory/social",
        "memory/tech",
        "memory/personal",
        "memory/_inbox/uncertain",
        "memory/_inbox/deferred",
        "memory/_inbox/pending_review",
        "memory/_sandbox",
        "memory/misc",
    ]
    dirs_created = 0
    for dir_path in MEMORY_DIRS:
        full_path = os.path.join(workspace, dir_path)
        os.makedirs(full_path, exist_ok=True)
        dirs_created += 1
    print(f"  ✅ {dirs_created} directories created")

    # --- Step 1: Parse files into memories ---
    memories = []
    now = _now_iso()
    truncated_count = 0

    # Parse MEMORY.md
    memory_md = workspace_path("MEMORY.md", workspace=workspace)
    if os.path.exists(memory_md):
        text = read_text_file(memory_md)

        sections = re.split(r"\n(?=## )", text)
        for section in sections:
            heading = re.match(r"## (.+)", section)
            if not heading:
                continue
            heading_text = heading.group(1).strip()
            content = section.strip()
            if heading_text.startswith("MEMORY.md"):
                continue

            if heading_text in ("人设与偏好", "飞书DM回复规则（最高优先级）"):
                importance = 0.95
            elif heading_text.startswith("项目：") or "关键决策" in heading_text:
                importance = 0.9
            elif heading_text in ("社区账号", "技术踩坑", "发帖规范"):
                importance = 0.8
            elif "索引" in heading_text or "索引" in content[:50]:
                importance = 0.4
            elif heading_text in ("待推进", "文件位置", "Git Code"):
                importance = 0.6
            else:
                importance = 0.5

            truncated = len(content) > 500
            if truncated:
                truncated_count += 1
            mem = {
                "id": f"mem_{uuid.uuid4().hex[:8]}",
                "content": f"[{heading_text}] {content[:500]}",
                "importance": importance,
                "entities": [],
                "tags": ["bootstrapped", "MEMORY.md"],
                "created_at": now,
                "last_accessed": now,
                "access_count": 1,
                "decay_score": importance,
                "status": "active",
                "case_type": "case",
                "confidence": 0.5,
                "reversibility": 1,
                "beta": 1.0,
                "trigger_count": 0,
                "last_triggered": None,
                "cooling_threshold": 5,
                "boundary_words": [],
                "conflict_refs": [],
                "failure_conditions": [],
                "failure_count": 0,
                "last_failure_trigger": None,
                "last_failure_fix": None,
                "source_case_id": None,
                "alternatives_considered": [],
                "cost_factors": {"write_cost": 0, "verify_cost": 0, "human_cost": 0, "transfer_cost": 0},
                "quality_gate": {"confidence": 0.5, "gate_mode": "normal", "bypass_reason": None},
                "importance_explain": None,
                "security_version": 1,
                "cooldown_active": False,
                "cooldown_until": None,
                "observing_since": None,
                "suspended_pending_count": 0,
                "provenance_level": "L1",
                "provenance_source": "human_direct",
                "memory_type": "static",
            }
            memories.append(mem)

    # Parse daily notes — flexible section splitting (same as memory_sync)
    memory_dir = workspace_path("memory", workspace=workspace)
    if os.path.exists(memory_dir):
        _ACTION_KW = ["决策", "确认", "修了", "修正", "新", "发布", "注册", "完成", "失败", "成功",
                       "修复", "删除", "更新", "添加", "修改", "推送", "创建", "重构"]
        for fname in sorted(os.listdir(memory_dir)):
            if not re.match(r"\d{4}-\d{2}-\d{2}\.md$", fname):
                continue
            fpath = os.path.join(memory_dir, fname)
            text = read_text_file(fpath)

            # Split by any heading level (## or ###), not hardcoded format
            sections = re.split(r"\n(?=##+ )", text)
            for section in sections:
                heading = re.match(r"##+\s+(.+?)(?:\s*\((.+?)\))?", section)
                if not heading:
                    continue
                section_title = heading.group(1).strip()
                content = section.strip()

                # Extract action-relevant lines
                action_lines = []
                for line in content.splitlines():
                    if line.startswith("- ") and any(kw in line for kw in _ACTION_KW):
                        action_lines.append(line)

                if action_lines:
                    mem = {
                        "id": f"mem_{uuid.uuid4().hex[:8]}",
                        "content": f"[{fname} {section_title}] {'; '.join(action_lines[:5])}",
                        "importance": 0.5,
                        "entities": [],
                        "tags": ["bootstrapped", "daily-note", fname],
                        "created_at": now,
                        "last_accessed": now,
                        "access_count": 1,
                        "decay_score": 0.5,
                        "status": "active",
                        "case_type": "case",
                        "confidence": 0.5,
                        "reversibility": 1,
                        "beta": 1.0,
                        "trigger_count": 0,
                        "last_triggered": None,
                        "cooling_threshold": 5,
                        "boundary_words": [],
                        "conflict_refs": [],
                        "failure_conditions": [],
                        "failure_count": 0,
                        "last_failure_trigger": None,
                        "last_failure_fix": None,
                        "source_case_id": None,
                        "alternatives_considered": [],
                        "cost_factors": {"write_cost": 0, "verify_cost": 0, "human_cost": 0, "transfer_cost": 0},
                        "quality_gate": {"confidence": 0.5, "gate_mode": "normal", "bypass_reason": None},
                        "importance_explain": None,
                        "security_version": 1,
                        "cooldown_active": False,
                        "cooldown_until": None,
                        "observing_since": None,
                        "suspended_pending_count": 0,
                        "provenance_level": "L1",
                        "provenance_source": "human_direct",
                        "memory_type": "static",
                    }
                    memories.append(mem)

    # --- Step 2: Apply v0.4.5 schema (memory_id, file_path, tags defaults) ---
    from mg_utils import generate_memory_id, derive_file_path, resolve_primary_tag
    existing_ids = set()
    for mem in memories:
        content = mem.get("content", "")
        tags = mem.get("tags", [])

        # Generate memory_id
        new_mid = generate_memory_id(content, existing_ids=existing_ids)
        mem["memory_id"] = new_mid
        existing_ids.add(new_mid)

        # Classify primary tag and add to tags
        primary_tag = resolve_primary_tag(tags, content)
        if primary_tag not in tags:
            tags.append(primary_tag)
        mem["tags"] = tags
        mem["classification_confidence"] = 0.5
        mem["classification_context"] = "bootstrap"

        # Derive file_path
        mem["file_path"] = derive_file_path(new_mid, tags, content)

        # Apply v0.4.5 field defaults (single source of truth)
        for key, default in MEMORY_DEFAULTS.items():
            if key not in mem:
                mem[key] = default

    # --- Step 3: Write memory files to category directories ---
    from memory_ingest import _write_memory_file
    files_written = 0
    files_skipped = 0
    for mem in memories:
        fp = mem.get("file_path", "")
        if not fp:
            files_skipped += 1
            continue
        try:
            result = _write_memory_file(
                mem["memory_id"], mem.get("content", ""), fp, workspace=workspace
            )
            if result:
                files_written += 1
        except Exception as e:
            logging.warning("bootstrap: failed to write %s: %s", fp, e)
            files_skipped += 1
    print(f"  ✅ {files_written} memory files written to category directories")
    if files_skipped:
        logging.warning("bootstrap: %d memories skipped (no file_path or write error)", files_skipped)

    # --- Step 3.5: Clean up MEMORY.md (remove ingested sections) ---
    ingested_headings = set()
    for mem in memories:
        if "MEMORY.md" not in mem.get("tags", []):
            continue
        # Extract heading from content: "[heading_text] ..."
        m = re.match(r"^\[(.+?)\]", mem.get("content", ""))
        if m:
            ingested_headings.add(m.group(1))

    if ingested_headings and os.path.exists(memory_md):
        text = read_text_file(memory_md)
        sections = re.split(r"\n(?=## )", text)

        # Keep preamble (everything before first ##) and non-ingested sections
        kept_parts = []
        first_heading_seen = False
        for section in sections:
            heading = re.match(r"## (.+)", section)
            if heading:
                first_heading_seen = True
                heading_text = heading.group(1).strip()
                if heading_text in ingested_headings:
                    continue  # Remove this section — already in category files
            if first_heading_seen:
                kept_parts.append(section)
            else:
                kept_parts.append(section)  # Keep preamble

        # Build index header
        from mg_utils import resolve_primary_tag
        index_lines = [
            "# MEMORY.md — 长期记忆索引",
            "",
            "## 使用说明",
            "详细内容按分类存储在 `memory/` 子目录，通过 `memory_search` 语义搜索获取。",
            "本文件只放索引和速查，不重复分类文件已有内容。",
            "",
            "## 记忆存储结构",
            "- `memory/project/` — 项目详情",
            "- `memory/tech/` — 技术参考（API、编码经验、踩坑）",
            "- `memory/personal/` — 个人偏好与习惯",
            "- `memory/misc/` — 杂项（写作规范等）",
            "- `memory/daily-note/` — 每日日志摘要（段落级）",
            "- `memory/synced/` — 段落级同步记忆（主体存储）",
            "",
        ]

        # Extract any remaining sections (not ingested) to keep
        remaining_sections = []
        for section in kept_parts:
            heading = re.match(r"## (.+)", section)
            if heading:
                remaining_sections.append(section.strip())

        # Build quick-reference from ingested memories (high-importance only)
        quick_ref_lines = ["## 快速速查（不在分类文件中的内容）", ""]
        has_quick_ref = False
        for mem in memories:
            if "MEMORY.md" not in mem.get("tags", []):
                continue
            if mem.get("importance", 0) >= 0.9:
                m = re.match(r"^\[(.+?)\]\s*", mem.get("content", ""))
                if m:
                    heading_text = m.group(1)
                    content_body = mem.get("content", "")[m.end():].strip()
                    # Keep only the first 3 lines as quick reference
                    lines = content_body.split("\n")[:3]
                    quick_ref_lines.append(f"### {heading_text}")
                    quick_ref_lines.extend(lines)
                    quick_ref_lines.append("")
                    has_quick_ref = True

        if not has_quick_ref:
            quick_ref_lines = []

        # Combine: index header + remaining sections + quick reference
        new_text = "\n".join(index_lines + remaining_sections + quick_ref_lines).strip() + "\n"

        # Backup original before overwriting
        import shutil
        backup_path = memory_md + ".pre-bootstrap.bak"
        shutil.copy2(memory_md, backup_path)

        from mg_utils import atomic_write
        atomic_write(memory_md, new_text)
        print(f"  ✅ MEMORY.md cleaned: {len(ingested_headings)} sections moved to category files")
        print(f"  📦 Backup saved to: {backup_path}")

    # --- Step 4: Build and save meta.json ---
    meta = {
        "version": SCHEMA_VERSION,
        "memories": memories,
        "conflicts": [],
        "security_rules": [],
        "entities": {},
        "routing_log": [],
        "quality_gate": {"state": "NORMAL", "last_check": now, "checks": []},
    }
    meta, _ = normalize_meta(meta)
    save_meta(meta_path, meta)

    # Summary
    tag_counts = {}
    for m in memories:
        for t in m.get("tags", []):
            if t in ("bootstrapped", "synced"):
                continue
            tag_counts[t] = tag_counts.get(t, 0) + 1
    print(f"\nBootstrap complete: {len(memories)} memories")
    print(f"  Directories: {dirs_created}")
    print(f"  From MEMORY.md: {sum(1 for m in memories if 'MEMORY.md' in m['tags'])}")
    print(f"  From daily notes: {sum(1 for m in memories if 'daily-note' in m['tags'])}")
    print(f"  Tag distribution: {dict(sorted(tag_counts.items(), key=lambda x: -x[1]))}")
    print(f"  Saved to: {meta_path}")
    if truncated_count > 0:
        logging.warning("bootstrap truncated %d memories at 500 chars (content too long)", truncated_count)

def cmd_snapshot(workspace):
    mod, error = _load_local_module("memory_diff", "memory_diff.py")
    if mod is None:
        return error
    return mod.run(workspace, None)


def cleanup_snapshots(workspace, keep_days=7):
    snap_dir = os.path.join(workspace, ".memory-guardian", "diff-snapshots")
    if not os.path.exists(snap_dir):
        return
    cutoff = datetime.now(CST) - timedelta(days=keep_days)
    removed = 0
    for f in sorted(os.listdir(snap_dir)):
        if not f.endswith(".md"):
            continue
        try:
            ts_str = f.replace(".md", "")
            ts = datetime.strptime(ts_str, "%Y%m%d-%H%M%S").replace(tzinfo=CST)
            if ts < cutoff:
                os.remove(os.path.join(snap_dir, f))
                removed += 1
        except ValueError:
            continue
    if removed:
        print(f"🧹 Cleaned {removed} old snapshots (kept last {keep_days} days)")


def cmd_run(workspace, apply, dry_run=False):
    """Full maintenance cycle.

    Auto-bootstraps if meta.json doesn't exist, matching MCP behavior.
    """
    workspace = workspace_path(workspace=workspace)

    # Auto-bootstrap if meta.json is missing (matches MCP handle_run_batch)
    meta_path = os.path.join(workspace, "memory", "meta.json")
    if not os.path.exists(meta_path):
        print("No meta.json found — running bootstrap...")
        cmd_bootstrap(workspace)
        if not os.path.exists(meta_path):
            print("Bootstrap failed. Aborting.")
            return None

    # Auto-migrate if schema version is outdated
    meta = load_meta(meta_path)
    current_ver = meta.get("version", "")
    if current_ver and current_ver != SCHEMA_VERSION:
        print(f"Schema version {current_ver} is outdated — running migration...")
        migrate_result = run_script("migrate.py", ["--apply"], workspace)
        print(migrate_result)

    input_count = workspace_memory_count(workspace)
    if apply:
        # v0.4.6 Phase 1: Merge dual-layer signals before decay
        print("Signal merge:")
        print("─" * 40)
        sig_args = ["--dry-run"] if dry_run else []
        print(run_script("signal_loop.py", sig_args, workspace))
        print("\n" + "─" * 40)
        # Sync files → meta.json before decay
        print("File sync:")
        print("─" * 40)
        print(run_script("memory_sync.py", ["--dry-run"] if dry_run else [], workspace))
        print("\n" + "─" * 40)
        print(run_script("memory_decay.py", [], workspace))
        print("\n" + "─" * 40)
        print("Compaction (apply):")
        print("─" * 40)
        print(run_script("memory_compact.py", ["--auto"], workspace))

        # Quality gate auto-check: upgrade WARNING→CRITICAL if conditions met
        print("\n" + "─" * 40)
        print("Quality Gate auto-check:")
        print("─" * 40)
        print(run_script("quality_gate.py", ["auto-check"], workspace))
        # Also check L2 queue timeout
        print(run_script("quality_gate.py", ["queue-check"], workspace))
    else:
        cmd_status(workspace)

    print("\n" + "=" * 60)
    print("Snapshot:")
    print("=" * 60)
    snapshot_result = cmd_snapshot(workspace)
    cleanup_snapshots(workspace)
    record_module_run(
        workspace,
        "guardian_run",
        input_count=input_count,
        output_count=input_count,
    )
    return snapshot_result


# ─── v0.4 New Commands ───────────────────────────────────────

def cmd_violations(workspace, args):
    """Violation rule check wrapper."""
    violation_args = ["check"]
    add_option(violation_args, "--days", args.days)
    add_option(violation_args, "--min-count", args.min_count)
    run_and_print("memory_violations.py", violation_args, workspace)


def cmd_violations_health(workspace):
    """Violation rule health wrapper."""
    run_and_print("memory_violations.py", ["health"], workspace)


def cmd_vlog(workspace, args):
    """Violation event logging wrapper."""
    violation_args = ["log"]
    add_option(violation_args, "--rule", args.rule)
    add_option(violation_args, "--event", args.event)
    add_option(violation_args, "--context", args.context)
    add_option(violation_args, "--severity", args.severity)
    run_and_print("memory_violations.py", violation_args, workspace)


def cmd_revise(workspace, args):
    """Violation rule revision wrapper."""
    violation_args = ["revise"]
    add_option(violation_args, "--rule", args.rule)
    add_option(violation_args, "--cooldown-days", args.cooldown_days)
    run_and_print("memory_violations.py", violation_args, workspace)


def cmd_migrate(workspace, args):
    """Run v0.3 → v0.4 migration."""
    migrate_args = []
    add_flag(migrate_args, "--dry-run", args.dry_run)
    if args.no_backup:
        add_flag(migrate_args, "--no-backup", True)
    else:
        add_flag(migrate_args, "--backup", True)
    run_and_print("migrate_v03_to_v04.py", migrate_args, workspace)


def cmd_security(workspace, args):
    """Security constraint layer operations."""
    sec_args = [args.sec_command]
    if args.sec_command == "check":
        add_option(sec_args, "--content", args.content)
    elif args.sec_command == "risk":
        add_option(sec_args, "--action", args.action)
    run_and_print("security_layer.py", sec_args, workspace)


def cmd_case_grow(workspace, args):
    """Case self-growth engine."""
    script = os.path.join(SCRIPT_DIR, "memory_case_grow.py")
    if not os.path.exists(script):
        print("[ERROR] Case growth engine not found.")
        return
    grow_args = [args.grow_command]
    if args.grow_command == "record-trigger":
        add_option(grow_args, "--id", args.grow_id)
    add_flag(grow_args, "--dry-run", args.dry_run)
    run_and_print("memory_case_grow.py", grow_args, workspace)


def cmd_quality_gate(workspace, args):
    """Quality gate module."""
    qg_args = [args.qg_command]

    if args.qg_command == "check":
        add_option(qg_args, "--content", args.content)
    if args.qg_command == "record":
        add_flag(qg_args, "--pass-check", args.pass_check)
        add_flag(qg_args, "--fail-check", not args.pass_check and args.fail_check)
        add_option(qg_args, "--reason", args.reason)
    elif args.qg_command in {"force-normal", "queue-flush"}:
        add_option(qg_args, "--reason", args.reason)
    elif args.qg_command == "intervention":
        add_option(qg_args, "--action", args.action)

    run_and_print("quality_gate.py", qg_args, workspace)


def cmd_l3_confirm(workspace, args):
    """L3 人工确认机制 (v0.4.2)."""
    l3_args = [args.l3_command]
    if args.l3_id:
        l3_args.append(args.l3_id)
    add_option(l3_args, "--reason", args.reason)
    add_option(l3_args, "--action", args.l3_action)
    add_option(l3_args, "--fields", args.l3_fields)
    run_and_print("l3_confirm.py", l3_args, workspace)


def cmd_pid_adaptive(workspace, args):
    """PID 全量自适应控制器 (v0.4.2)."""
    pid_args = [args.pid_command]
    add_option(pid_args, "--scene-group", args.pid_scene_group)
    add_option(pid_args, "--error", args.pid_error)
    add_flag(pid_args, "--dry-run", args.dry_run)
    run_and_print("pid_adaptive.py", pid_args, workspace)


def cmd_migrate_bootstrap_to_case(workspace, dry_run=False):
    """Migrate active bootstrap mem_* records into canonical case_* records."""
    migrate_args = []
    add_flag(migrate_args, "--dry-run", dry_run)
    run_and_print("migrate_bootstrap_to_case.py", migrate_args, workspace)


def cmd_migrate_042(workspace, args):
    """v0.4.1 → v0.4.2 migration."""
    migrate_args = []
    add_flag(migrate_args, "--dry-run", args.dry_run)
    add_flag(migrate_args, "--apply", args.apply)
    add_option(migrate_args, "--step", args.step)
    run_and_print("migrate_to_v042.py", migrate_args, workspace)


def cmd_case_invalidate(workspace, args):
    """Case 无效化机制 (v0.4.2)."""
    inv_args = [args.inv_command]
    if args.inv_id:
        inv_args.append(args.inv_id)
    if args.inv_command == "unfreeze":
        add_option(inv_args, "--new-confidence", args.inv_confidence)
    add_flag(inv_args, "--dry-run", args.dry_run)
    run_and_print("case_invalidate.py", inv_args, workspace)


# ─── Main ────────────────────────────────────────────────────

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="memory-guardian unified CLI v0.4.2")
    p.add_argument("command",
                   choices=["status", "ingest", "bootstrap", "snapshot", "run",
                            "violations", "violations-health", "vlog", "revise", "rescan",
                            "migrate", "security", "case-grow", "quality-gate",
                            "l3-confirm", "pid-adaptive", "migrate-bootstrap", "migrate-042", "case-invalidate"],
                   help="Command to run")
    # Common args
    p.add_argument("--content", default=None, help="Memory content (for ingest)")
    p.add_argument("--importance", type=float, default=0.5, help="Importance 0-1")
    p.add_argument("--tags", default="", help="Comma-separated tags")
    p.add_argument("--workspace", default=DEFAULT_WORKSPACE, help="Workspace path")
    p.add_argument("--apply", action="store_true", help="Apply changes")
    p.add_argument("--dry-run", action="store_true", help="Dry run mode")
    p.add_argument("--rule", default=None, help="Rule ID (for vlog/revise)")
    p.add_argument("--event", default=None, help="Event description (for vlog)")
    p.add_argument("--context", default="", help="Context (for vlog)")
    p.add_argument("--reason", default=None, help="Reason text for commands that support it")
    p.add_argument("--action", default=None, help="Generic action for commands that support it")
    p.add_argument("--days", type=int, default=7, help="Days to look back")
    p.add_argument("--min-count", type=int, default=3, help="Minimum count threshold for violations check")
    p.add_argument("--severity", default="warning", choices=["info", "warning", "error"], help="Violation severity (for vlog)")
    p.add_argument("--cooldown-days", type=int, default=14, help="Cooldown period")
    p.add_argument("--no-backup", action="store_true", help="Skip backup")
    # v0.4 case fields
    p.add_argument("--situation", default=None, help="情境")
    p.add_argument("--judgment", default=None, help="判断")
    p.add_argument("--consequence", default=None, help="后果")
    p.add_argument("--action-conclusion", default=None, help="修正")
    p.add_argument("--reversibility", type=int, default=None, choices=[0, 1, 2, 3])
    p.add_argument("--boundary-words", default=None, help="Boundary words")
    p.add_argument("--alternatives", default=None, help="Alternatives considered")
    p.add_argument("--update", default=None, help="Memory ID to update")
    p.add_argument("--provenance-source", default=None,
                   choices=["human", "system", "external"],
                   help="Provenance source (for ingest)")
    # Security subcommand
    p.add_argument("--sec-command", default="list",
                   choices=["extract", "check", "save", "list", "risk", "tag-classify"],
                   help="Security sub-command (for security)")
    # Quality gate subcommand
    p.add_argument("--qg-command", default="status",
                   choices=["check", "status", "record", "force-normal", "intervention",
                            "queue-status", "queue-flush", "queue-check", "auto-check"],
                   help="Quality gate sub-command")
    p.add_argument("--pass-check", action="store_true", help="Record pass (for quality-gate)")
    p.add_argument("--fail-check", action="store_true", help="Record fail (for quality-gate)")
    # Case-grow subcommand
    p.add_argument("--grow-command", default="status",
                   choices=["status", "grow", "merge", "conflict", "pool", "scenes", "post-stress", "record-trigger", "rescan-authority"],
                   help="Case-grow sub-command")
    p.add_argument("--grow-id", default=None, help="Case ID (for case-grow record-trigger)")
    # L3 confirm subcommand (v0.4.2)
    p.add_argument("--l3-command", default="status",
                   choices=["status", "pending", "confirm", "reject", "check-timeout", "create"],
                   help="L3 confirm sub-command")
    p.add_argument("--l3-id", default=None, help="L3 confirmation ID")
    p.add_argument("--l3-action", default=None, help="L3 write action (for create)")
    p.add_argument("--l3-fields", default=None, help="L3 fields JSON (for create)")
    # PID adaptive subcommand (v0.4.2)
    p.add_argument("--pid-command", default="status",
                   choices=["status", "compute", "update", "history", "reset"],
                   help="PID adaptive sub-command")
    p.add_argument("--pid-scene-group", default=None, help="Scene group name")
    p.add_argument("--pid-error", type=float, default=None, help="Manual error value")
    # Migrate v0.4.2 subcommand
    p.add_argument("--step", default=None,
                   choices=["p0-0", "p0-1", "p0-2", "p0-3"],
                   help="Migration step (for migrate-042)")
    # Case invalidate subcommand
    p.add_argument("--inv-command", default="status",
                   choices=["status", "check", "review", "unfreeze", "archive", "delete"],
                   help="Case invalidation sub-command")
    p.add_argument("--inv-id", default=None, help="Case ID (for unfreeze/archive/delete)")
    p.add_argument("--inv-confidence", type=float, default=0.5, help="Reset confidence (for unfreeze)")
    args = p.parse_args()

    commands = {
        "status": lambda: cmd_status(args.workspace),
        "ingest": lambda: cmd_ingest(
            args.content, args.importance,
            args.tags.split(",") if args.tags else [],
            args.workspace,
            situation=args.situation,
            judgment=args.judgment,
            consequence=args.consequence,
            action_conclusion=args.action_conclusion,
            reversibility=args.reversibility,
            boundary_words=args.boundary_words.split(",") if args.boundary_words else [],
            alternatives=args.alternatives.split(",") if args.alternatives else [],
            update=args.update,
            provenance_source=args.provenance_source,
        ),
        "bootstrap": lambda: cmd_bootstrap(args.workspace),
        "snapshot": lambda: cmd_snapshot(args.workspace),
        "run": lambda: cmd_run(args.workspace, args.apply, args.dry_run),
        "violations": lambda: cmd_violations(args.workspace, args),
        "violations-health": lambda: cmd_violations_health(args.workspace),
        "vlog": lambda: cmd_vlog(args.workspace, args),
        "revise": lambda: cmd_revise(args.workspace, args),
        "rescan": lambda: cmd_rescan(args.workspace),
        "migrate": lambda: cmd_migrate(args.workspace, args),
        "security": lambda: cmd_security(args.workspace, args),
        "case-grow": lambda: cmd_case_grow(args.workspace, args),
        "quality-gate": lambda: cmd_quality_gate(args.workspace, args),
        "l3-confirm": lambda: cmd_l3_confirm(args.workspace, args),
        "pid-adaptive": lambda: cmd_pid_adaptive(args.workspace, args),
        "migrate-bootstrap": lambda: cmd_migrate_bootstrap_to_case(args.workspace, args.dry_run),
        "migrate-042": lambda: cmd_migrate_042(args.workspace, args),
        "case-invalidate": lambda: cmd_case_invalidate(args.workspace, args),
    }

    # Validation
    if args.command == "ingest" and not args.content and not any([args.situation, args.judgment, args.consequence, args.action_conclusion]):
        print("Error: --content or case fields (--situation/--judgment/etc) required")
        sys.exit(1)
    if args.command == "vlog" and (not args.rule or not args.event):
        print("Error: --rule and --event required for vlog")
        sys.exit(1)
    if args.command == "revise" and not args.rule:
        print("Error: --rule required for revise")
        sys.exit(1)
    if args.command == "case-grow" and args.grow_command == "record-trigger" and not args.grow_id:
        print("Error: --grow-id required for case-grow record-trigger")
        sys.exit(1)
    if args.command == "migrate-042" and args.apply and args.dry_run:
        print("Error: cannot use --apply and --dry-run together for migrate-042")
        sys.exit(1)

    emit_result(commands[args.command]())
