#!/usr/bin/env python3
"""memory-guardian: File → meta.json sync engine.

Scans MEMORY.md and memory/*.md (daily notes) for new/updated content,
compares against existing meta.json entries via dedup check, and ingests
any new memories through IngestService.

v0.4.5 changes:
  - Incremental scanning: only processes files modified since last_sync_at
  - Paragraph-level sync: splits by paragraphs instead of ## headings
  - _inbox processing: handles needs_review timeouts
  - Exponential backoff cooldown
  - memory_id primary key support

Designed to run automatically in cmd_run before decay, ensuring meta.json
stays in sync with manually edited files.

Usage:
  python3 memory_sync.py [--workspace <path>] [--dry-run] [--meta <path>]
"""
import argparse
import os
import re
import sys
from datetime import datetime, timedelta, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from mg_utils import (
    load_meta, save_meta, read_text_file,
    _now_iso, CST,
)
from mg_utils import workspace_path
from mg_repo.meta_json_repository import MetaJsonRepository
from mg_app.ingest_service import IngestService
from memory_ingest import quick_dedup_check


# ── Importance assignment (mirrors bootstrap logic) ──────────

_MEMORY_MD_IMPORTANCE = {
    "人设与偏好": 0.9,
    "项目": 0.8,
    "技术踩坑": 0.8,
    "社区": 0.7,
    "API 参考": 0.7,
    "版本状态": 0.6,
    "待推进": 0.6,
    "飞书文档体系": 0.6,
    "核心架构": 0.7,
    "模块清单": 0.5,
    "帖子索引": 0.4,
    "InStreet 帖子索引": 0.4,
    "记忆写作规范": 0.5,
    "安全": 0.8,
}

# Keywords that signal actionable content (not just logs/links)
_ACTION_KEYWORDS = [
    "决策", "确认", "修了", "修正", "新", "发布", "注册", "完成",
    "失败", "成功", "更新", "修改", "修复", "优化", "重构",
    "配置", "部署", "推送", "合并", "解决", "设计", "实现",
    "创建", "删除", "迁移", "升级", "废弃", "归档",
]

# Headings that are index/link lists — skip these
_SKIP_HEADINGS = {"索引", "文件位置", "Git Code", "Git"}

# ── v0.4.5: Exponential backoff ────────────────────────────

_COOLDOWN_BASE_MINUTES = 30
_COOLDOWN_MAX_MINUTES = 240  # 4h cap


def get_cooldown_minutes(consecutive_failures):
    """Calculate exponential backoff cooldown.

    30min → 1h → 2h → 4h (capped)
    """
    minutes = _COOLDOWN_BASE_MINUTES * (2 ** min(consecutive_failures, 3))
    return min(minutes, _COOLDOWN_MAX_MINUTES)


# ── v0.4.5: Incremental scanning ───────────────────────────

def _file_needs_sync(file_path, last_sync_at=None):
    """Check if a file needs syncing based on mtime vs last_sync_at.

    Returns True if file was modified after last_sync_at or if last_sync_at is None.
    """
    if not os.path.exists(file_path):
        return False
    mtime = datetime.fromtimestamp(os.path.getmtime(file_path), tz=CST)
    if last_sync_at is None:
        return True
    try:
        last_dt = datetime.fromisoformat(last_sync_at)
        if last_dt.tzinfo is None:
            last_dt = last_dt.replace(tzinfo=CST)
        return mtime > last_dt
    except (ValueError, TypeError):
        return True


def _dir_needs_sync(dir_path, last_sync_at=None):
    """Check if any file in directory was modified after last_sync_at.

    Returns True if directory mtime is newer, or if last_sync_at is None.
    """
    if not os.path.isdir(dir_path):
        return False
    if last_sync_at is None:
        return True
    # Check directory mtime (updated when files are added/modified)
    dir_mtime = datetime.fromtimestamp(os.path.getmtime(dir_path), tz=CST)
    try:
        last_dt = datetime.fromisoformat(last_sync_at)
        if last_dt.tzinfo is None:
            last_dt = last_dt.replace(tzinfo=CST)
        return dir_mtime > last_dt
    except (ValueError, TypeError):
        return True


# ── v0.4.5: Paragraph-level extraction ─────────────────────

def _extract_paragraphs(text, min_length=30):
    """Extract paragraphs from text, filtering short ones.

    Paragraphs are separated by blank lines. Each must have min_length chars.
    """
    paragraphs = []
    for para in text.split("\n\n"):
        para = para.strip()
        if len(para) >= min_length:
            paragraphs.append(para)
    return paragraphs


def _extract_paragraph_candidates(workspace, last_sync_at=None):
    """v0.4.5: Paragraph-level candidate extraction from all memory files.

    Scans MEMORY.md and memory/*.md, extracting action-containing paragraphs.
    Uses incremental scanning to skip unchanged files.
    """
    candidates = []

    # MEMORY.md
    memory_md_path = os.path.join(workspace, "MEMORY.md")
    if _file_needs_sync(memory_md_path, last_sync_at):
        text = read_text_file(memory_md_path)
        sections = re.split(r"\n(?=## )", text)
        for section in sections:
            heading_match = re.match(r"##\s+([^\n]+)", section)
            if not heading_match:
                continue
            heading_text = heading_match.group(1).strip()
            if any(skip in heading_text for skip in _SKIP_HEADINGS):
                continue

            paragraphs = _extract_paragraphs(section)
            has_action_para = False
            for para in paragraphs:
                if any(kw in para for kw in _ACTION_KEYWORDS):
                    has_action_para = True
                    importance = _assign_importance(heading_text)
                    candidates.append({
                        "content": f"[{heading_text}] {para[:500]}",
                        "importance": importance,
                        "tags": ["synced", "MEMORY.md"],
                        "source": "MEMORY.md",
                        "heading": heading_text,
                    })

            # Fallback: use section-level extraction if no paragraph had action keywords
            # but the section as a whole does (handles short action lines spanning paragraphs)
            if not has_action_para:
                lines = section.strip().splitlines()
                content_lines = []
                for line in lines[1:]:  # skip heading
                    if re.match(r"^##\s+", line):
                        break
                    content_lines.append(line)
                content = "\n".join(content_lines).strip()
                if content and len(content) >= 10 and any(kw in content for kw in _ACTION_KEYWORDS):
                    importance = _assign_importance(heading_text)
                    candidates.append({
                        "content": f"[{heading_text}] {content[:500]}",
                        "importance": importance,
                        "tags": ["synced", "MEMORY.md"],
                        "source": "MEMORY.md",
                        "heading": heading_text,
                    })

    # Daily notes
    memory_dir = workspace_path("memory", workspace=workspace)
    if _dir_needs_sync(memory_dir, last_sync_at):
        for fname in sorted(os.listdir(memory_dir)):
            if not re.match(r"\d{4}-\d{2}-\d{2}\.md$", fname):
                continue
            fpath = os.path.join(memory_dir, fname)
            if not _file_needs_sync(fpath, last_sync_at):
                continue

            text = read_text_file(fpath)
            sections = re.split(r"\n(?=##+ )", text)

            for section in sections:
                heading_match = re.match(r"##+\s+(.+?)(?:\s*\((.+?)\))?", section)
                if not heading_match:
                    continue
                section_title = heading_match.group(1).strip()

                paragraphs = _extract_paragraphs(section)
                has_action_para = False
                for para in paragraphs:
                    action_lines = [
                        line for line in para.splitlines()
                        if (line.startswith("- ") or (len(line) > 10 and not line.startswith("#")))
                        and any(kw in line for kw in _ACTION_KEYWORDS)
                    ]
                    if action_lines:
                        has_action_para = True
                        candidates.append({
                            "content": f"[{fname} {section_title}] {'; '.join(action_lines[:5])}",
                            "importance": 0.5,
                            "tags": ["synced", "daily-note", fname],
                            "source": f"memory/{fname}",
                            "heading": section_title,
                        })

                # Fallback: section-level extraction
                if not has_action_para:
                    action_lines = []
                    for line in section.splitlines():
                        # Match both list items (- xxx) and plain lines with action keywords
                        if line.startswith("- ") and any(kw in line for kw in _ACTION_KEYWORDS):
                            action_lines.append(line)
                        elif not line.startswith("#") and not line.startswith("-") and any(kw in line for kw in _ACTION_KEYWORDS) and len(line) > 10:
                            action_lines.append(line.strip())
                    if action_lines:
                        candidates.append({
                            "content": f"[{fname} {section_title}] {'; '.join(action_lines[:5])}",
                            "importance": 0.5,
                            "tags": ["synced", "daily-note", fname],
                            "source": f"memory/{fname}",
                            "heading": section_title,
                        })

    return candidates


# ── v0.4.5: _inbox processing ──────────────────────────────

def process_inbox(meta_path, workspace=None):
    """Process needs_review entries that have timed out.

    Entries with needs_review=True and needs_review_since older than
    needs_review_timeout get inbox_reason set and routed to _inbox.

    Returns:
        dict: {processed: int, details: list}
    """
    if not os.path.exists(meta_path):
        return {"processed": 0, "details": []}

    meta = load_meta(meta_path)
    memories = meta.get("memories", [])
    processed = 0
    details = []
    now = datetime.now(CST)

    for mem in memories:
        if not mem.get("needs_review"):
            continue

        review_since = mem.get("needs_review_since")
        timeout_str = mem.get("needs_review_timeout", "7d")

        if not review_since:
            continue

        try:
            review_dt = datetime.fromisoformat(review_since)
            if review_dt.tzinfo is None:
                review_dt = review_dt.replace(tzinfo=CST)
        except (ValueError, TypeError):
            continue

        # Parse timeout
        timeout_days = 7
        m = re.match(r"(\d+)d", timeout_str)
        if m:
            timeout_days = int(m.group(1))

        elapsed = (now - review_dt).total_seconds() / 86400
        if elapsed >= timeout_days:
            mem["inbox_reason"] = "pending_review"
            mem["needs_review"] = False
            mem["review_result"] = "divergent"
            mem["reviewed_at"] = _now_iso()
            # Move actual file to _inbox/pending_review/
            old_fp = mem.get("file_path", "")
            mid = mem.get("memory_id", mem.get("id", ""))
            inbox_dir = os.path.join(os.path.dirname(meta_path), "_inbox", "pending_review")
            new_fp = f"memory/_inbox/pending_review/{mid}.md" if mid else old_fp
            # Physically move the file FIRST, only update meta on success
            if workspace and old_fp and old_fp != new_fp:
                old_abs = os.path.join(workspace, old_fp)
                new_abs = os.path.join(workspace, new_fp)
                if os.path.exists(old_abs):
                    os.makedirs(os.path.dirname(new_abs), exist_ok=True)
                    try:
                        os.replace(old_abs, new_abs)
                        mem["file_path"] = new_fp
                    except OSError as e:
                        # Keep original file_path — file move failed
                        import logging
                        logging.warning(f"Failed to move {old_abs} -> {new_abs}: {e}")
            elif old_fp != new_fp:
                mem["file_path"] = new_fp
            processed += 1
            details.append({
                "memory_id": mem.get("memory_id", mem.get("id")),
                "action": "timed_out_to_inbox",
                "elapsed_days": round(elapsed, 1),
            })

    if processed > 0:
        save_meta(meta_path, meta)
        print(f"📬 Processed {processed} timed-out needs_review entries → _inbox")

    return {"processed": processed, "details": details}


def _assign_importance(heading_text):
    """Assign importance based on heading, same logic as bootstrap."""
    for key, val in _MEMORY_MD_IMPORTANCE.items():
        if key in heading_text:
            return val
    if "踩坑" in heading_text or "安全" in heading_text:
        return 0.8
    return 0.5


# ── Extraction: MEMORY.md ───────────────────────────────────

# ── Core sync logic ─────────────────────────────────────────

def run(workspace=None, dry_run=False, meta_path_override=None):
    """Run file → meta.json sync.

    v0.4.5: Uses incremental scanning, paragraph-level extraction,
    exponential backoff, and _inbox processing.

    Args:
        workspace: Workspace root path
        dry_run: If True, preview changes without writing
        meta_path_override: Override meta.json path

    Returns:
        dict with created/skipped counts and details
    """
    workspace = workspace_path(workspace=workspace)
    meta_path = meta_path_override or os.path.join(workspace, "memory", "meta.json")

    # Check meta.json exists
    if not os.path.exists(meta_path):
        return {
            "created": 0, "updated": 0, "skipped": 0,
            "details": [], "dry_run": dry_run,
            "message": "meta.json not found — run bootstrap first",
        }

    meta = load_meta(meta_path)
    memories = meta.get("memories", [])

    # v0.4.5: Check cooldown (exponential backoff) — only active when failures occurred
    last_sync = meta.get("last_sync_at")
    consecutive_failures = meta.get("sync_consecutive_failures", 0)

    if last_sync and consecutive_failures > 0:
        try:
            last_dt = datetime.fromisoformat(last_sync)
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=CST)
            cooldown = get_cooldown_minutes(consecutive_failures)
            elapsed_min = (datetime.now(CST) - last_dt).total_seconds() / 60
            if elapsed_min < cooldown and not dry_run:
                return {
                    "created": 0, "updated": 0, "skipped": 0,
                    "details": [], "dry_run": dry_run,
                    "message": f"cooldown: {elapsed_min:.0f}/{cooldown} min (failures={consecutive_failures})",
                }
        except (ValueError, TypeError):
            pass

    # v0.4.5: Process _inbox (needs_review timeouts)
    inbox_result = {"processed": 0, "details": []}
    if not dry_run:
        try:
            inbox_result = process_inbox(meta_path, workspace)
        except Exception as e:
            print(f"⚠️  _inbox processing error: {e}")

    # v0.4.5: Paragraph-level incremental extraction
    all_candidates = _extract_paragraph_candidates(workspace, last_sync_at=last_sync)

    if not all_candidates:
        result = {
            "created": 0, "updated": 0, "skipped": 0,
            "inbox_processed": inbox_result["processed"],
            "details": inbox_result["details"],
            "dry_run": dry_run,
            "message": "No candidate memories found in files (incremental scan)",
        }
        if not dry_run:
            meta["last_sync_at"] = _now_iso()
            meta["sync_consecutive_failures"] = 0  # Reset on successful scan
            save_meta(meta_path, meta)
        return result

    # Dedup check and ingest
    created = 0
    skipped = 0
    details = []

    repo = MetaJsonRepository(meta_path, workspace=workspace)
    service = IngestService(repo)

    for candidate in all_candidates:
        content = candidate["content"]
        importance = candidate["importance"]
        tags = candidate["tags"]

        # Dedup check — v0.4.5: use memory_id or id
        dup = quick_dedup_check(content, memories, threshold=0.85)
        if dup:
            skipped += 1
            details.append({
                "action": "skipped",
                "reason": "dedup",
                "existing_id": dup.get("id"),
                "content_preview": content[:80],
            })
            continue

        if dry_run:
            created += 1
            details.append({
                "action": "would_create",
                "source": candidate["source"],
                "importance": importance,
                "content_preview": content[:80],
            })
        else:
            try:
                ingest_result = service.ingest(
                    content=content,
                    importance=importance,
                    tags=tags,
                    workspace=workspace,
                    provenance_source="system_sync",
                )

                if ingest_result.get("action") == "created":
                    created += 1
                    mem = ingest_result.get("memory", {})
                    # Write source_file so signal_loop can match access_log entries
                    if candidate.get("source") and mem.get("id"):
                        mem["source_file"] = candidate["source"]
                    details.append({
                        "action": "created",
                        "id": mem.get("id"),
                        "memory_id": mem.get("memory_id"),
                        "source": candidate["source"],
                        "importance": importance,
                        "content_preview": content[:80],
                    })
                    # Update local memories list for subsequent dedup checks
                    memories.append(mem)
                elif ingest_result.get("action") == "dedup_found":
                    skipped += 1
                    details.append({
                        "action": "skipped",
                        "reason": "service_dedup",
                        "existing_id": ingest_result.get("existing"),
                        "content_preview": content[:80],
                    })
                elif ingest_result.get("action") == "queued":
                    skipped += 1
                    details.append({
                        "action": "skipped",
                        "reason": "quality_gate_queued",
                        "id": ingest_result.get("id"),
                        "content_preview": content[:80],
                    })
                else:
                    skipped += 1
                    details.append({
                        "action": "skipped",
                        "reason": ingest_result.get("action", "unknown"),
                        "content_preview": content[:80],
                    })
            except Exception as e:
                skipped += 1
                details.append({
                    "action": "error",
                    "error": str(e),
                    "content_preview": content[:80],
                })

    # Record sync timestamp (reuse already-loaded meta to avoid overwriting
    # new memories written by IngestService during the ingest loop above)
    if not dry_run:
        meta["last_sync_at"] = _now_iso()
        meta["sync_consecutive_failures"] = 0  # Reset on success
        save_meta(meta_path, meta)

    print(f"🔄 File sync complete: {created} created, {skipped} skipped (dry_run={dry_run})")

    return {
        "created": created,
        "updated": 0,
        "skipped": skipped,
        "total_candidates": len(all_candidates),
        "inbox_processed": inbox_result["processed"],
        "details": details + inbox_result["details"],
        "dry_run": dry_run,
    }


# ── CLI ─────────────────────────────────────────────────────

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="memory-guardian: file → meta.json sync")
    p.add_argument("--workspace", default=None, help="Workspace root path")
    p.add_argument("--dry-run", action="store_true", help="Preview without writing")
    p.add_argument("--meta", default=None, help="Path to meta.json")

    args = p.parse_args()
    workspace = args.workspace or os.environ.get("MG_WORKSPACE")

    result = run(workspace=workspace, dry_run=args.dry_run, meta_path_override=args.meta)
    print(result)
