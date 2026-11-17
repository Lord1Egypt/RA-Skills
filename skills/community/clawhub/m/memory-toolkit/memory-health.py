#!/usr/bin/env python3
"""
Memory Health — Comprehensive memory system health check.

READ-ONLY by default: runs diagnostics, prints to stdout, writes nothing to disk.
Use --output-dir <path> to save JSON reports and SVG trend charts.

Runs: trace extraction, LoCoMo benchmark, size check, ontology health,
daily notes hygiene, index status, and drift detection.

Usage:
    python3 memory-health.py              # Full health check (read-only)
    python3 memory-health.py --quick      # Skip benchmark & LLM (read-only)
    python3 memory-health.py --benchmark  # Benchmark only (read-only)
    python3 memory-health.py --deep       # LLM + sessions + benchmark (weekly)
    python3 memory-health.py --output-dir results/  # Save reports to disk
    python3 memory-health.py --fix        # Fix mode (DESTRUCTIVE: archives files, rewrites ontology)
                                          # Requires confirmation or --force
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

WORKSPACE = Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw/workspace")).resolve()
SKILL_DIR = WORKSPACE / "skills" / "memory-health"
RESULTS_DIR = SKILL_DIR / "results"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
ONTOLOGY_FILE = WORKSPACE / "memory" / "ontology" / "graph.jsonl"
DAILY_NOTES_DIR = WORKSPACE / "memory"
TRACE_EXTRACTOR = WORKSPACE / "skills" / "trace-extractor" / "trace-extractor.py"
# LoCoMo benchmark harness. Optional: the skill works without it. When absent,
# --benchmark reports "not available" and never silently pretends to have run.
LOCOMO_TEST = (WORKSPACE / "skills" / "locomo-test" / "locomo_test.py").resolve()
if not LOCOMO_TEST.is_relative_to(WORKSPACE):
    LOCOMO_TEST = WORKSPACE / "skills" / "locomo-test" / "locomo_test.py"

# Security: validate all script paths are within WORKSPACE
for _path in [TRACE_EXTRACTOR, LOCOMO_TEST]:
    if not _path.resolve().is_relative_to(WORKSPACE):
        raise RuntimeError(f"Security: script path escapes workspace: {_path}")

# Expected workspace root. WORKSPACE comes from the environment, so a hostile or
# mistyped value would redirect every subprocess we launch. Allow an override
# only when it is explicitly opted into, and always require the resolved value
# to sit under the caller's home directory.
EXPECTED_WORKSPACE = (Path.home() / ".openclaw" / "workspace").resolve()
if os.environ.get("WORKSPACE_ALLOW_CUSTOM") != "1":
    if WORKSPACE != EXPECTED_WORKSPACE and WORKSPACE != EXPECTED_WORKSPACE.parent and not WORKSPACE.is_relative_to(EXPECTED_WORKSPACE):
        raise RuntimeError(
            f"Security: WORKSPACE is not the expected {EXPECTED_WORKSPACE}: {WORKSPACE}\n"
            "Set WORKSPACE_ALLOW_CUSTOM=1 to override deliberately."
        )

# Absolute path to the openclaw binary. Resolving it once, instead of trusting
# the inherited $PATH on every call, stops a poisoned PATH entry from being
# executed in place of the real CLI.
OPENCLAW_BIN = shutil.which("openclaw") or "/usr/local/bin/openclaw"

# Thresholds
MEMORY_MAX_SIZE = 5000  # 5KB limit
DAILY_NOTES_MAX_AGE = 14  # Archive notes older than 14 days


def run_trace_extraction(days=1, llm=False, sessions=False):
    """Run trace extraction.

    ⚠️ Privacy note: When --llm or --sessions flags are used, session transcript
    text is sent to the local Ollama instance for processing. Ensure OLLAMA_URL
    stays on localhost for privacy.

    ⚠️ State note: trace-extractor APPENDS to memory/ontology/graph.jsonl and
    rewrites daily notes. It therefore runs with --dry-run unless the caller has
    explicitly opted into a mutating run (``mutating=True``, set only by --fix).
    A passive health check must never change memory state.
    """
    return _run_trace_extraction(days=days, llm=llm, sessions=sessions, mutating=False)


def _run_trace_extraction(days=1, llm=False, sessions=False, mutating=False):
    """Internal runner. ``mutating`` mirrors the user's explicit --fix intent."""
    cmd = [sys.executable, str(TRACE_EXTRACTOR), "--days", str(days)]
    if llm:
        cmd.append("--llm")
    if sessions:
        cmd.append("--sessions")
    if not mutating:
        # Read-only pass: preview extraction without writing ontology/notes.
        cmd.append("--dry-run")

    try:
        # SECURITY: Local subprocess execution only. Outbound HTTP calls are isolated to the local Ollama API.
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=str(WORKSPACE))
        return result.stdout
    except subprocess.TimeoutExpired:
        return "⚠️ Trace extraction timed out (300s)"
    except Exception as e:
        return f"⚠️ Trace extraction failed: {e}"


def check_memory_size():
    """Check MEMORY.md size and composition."""
    if not MEMORY_FILE.exists():
        return {"error": "MEMORY.md not found"}
    
    content = MEMORY_FILE.read_text()
    size = len(content)
    lines = content.count("\n")
    
    # Analyze sections
    sections = {}
    current_section = "Header"
    current_size = 0
    for line in content.split("\n"):
        if line.startswith("## "):
            sections[current_section] = current_size
            current_section = line.strip()
            current_size = 0
        current_size += len(line) + 1
    sections[current_section] = current_size
    
    # Sort by size
    sorted_sections = sorted(sections.items(), key=lambda x: -x[1])
    
    return {
        "size_bytes": size,
        "size_kb": round(size / 1024, 1),
        "lines": lines,
        "over_limit": size > MEMORY_MAX_SIZE,
        "limit_kb": round(MEMORY_MAX_SIZE / 1024, 1),
        "sections": sorted_sections[:5],
        "status": "🟢 OK" if size <= MEMORY_MAX_SIZE else f"🔴 OVER LIMIT ({size}/{MEMORY_MAX_SIZE} bytes)"
    }


def check_ontology():
    """Check ontology health."""
    if not ONTOLOGY_FILE.exists():
        return {"error": "Ontology file not found"}
    
    entities = {}
    relations = []
    entity_ids = set()
    orphan_relations = 0
    
    for line in ONTOLOGY_FILE.read_text().strip().split("\n"):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
            op = entry.get("op")
            # ``state`` is the dominant write in the live graph (the ontology
            # writer emits one state record per entity snapshot); ``create`` and
            # ``upsert`` are the older/simpler forms. Counting only create/upsert
            # made every relation look orphaned once the writer switched to
            # ``state`` — the health check screamed "68 orphan relations" while
            # ontology_compact.py, which replays the full log, saw zero. Accept
            # all three so both tools agree on the same entity set.
            if op in ("create", "upsert", "state"):
                # Handle both entity and relation-style entries
                # upsert = create if not exists, update if exists
                if "entity" in entry:
                    eid = entry["entity"]["id"]
                    entities[eid] = entry["entity"]
                    entity_ids.add(eid)
                elif "relation" in entry:
                    # Malformed: create with relation instead of entity — treat as relate
                    relations.append(entry)
                    src = entry["relation"].get("from", entry["relation"].get("source"))
                    tgt = entry["relation"].get("to", entry["relation"].get("target"))
                    if src and src not in entity_ids:
                        orphan_relations += 1
                    if tgt and tgt not in entity_ids:
                        orphan_relations += 1
            elif op == "update":
                # Update ops: apply to existing entities if present
                if "entity" in entry:
                    eid = entry["entity"].get("id")
                    if eid and eid in entities:
                        entities[eid].update(entry["entity"])
            elif op == "relate":
                relations.append(entry)
                src = entry.get("from", entry.get("source"))
                tgt = entry.get("to", entry.get("target"))
                if src and src not in entity_ids:
                    orphan_relations += 1
                if tgt and tgt not in entity_ids:
                    orphan_relations += 1
        except json.JSONDecodeError:
            continue
    
    # Count types
    types = {}
    for eid, entity in entities.items():
        etype = entity.get("type", "unknown")
        types[etype] = types.get(etype, 0) + 1
    
    return {
        "total_entities": len(entities),
        "total_relations": len(relations),
        "orphan_relations": orphan_relations,
        "types": sorted(types.items(), key=lambda x: -x[1])[:10],
        "status": f"🟢 {len(entities)} entities, {len(relations)} relations" if orphan_relations == 0 else f"🟡 {orphan_relations} orphan relations"
    }


def check_daily_notes():
    """Check daily notes hygiene."""
    today = date.today()
    notes = []
    stale = []
    
    for f in DAILY_NOTES_DIR.glob("2026-*.md"):
        note_date_str = f.stem
        try:
            note_date = datetime.strptime(note_date_str, "%Y-%m-%d").date()
            age = (today - note_date).days
            size = f.stat().st_size
            notes.append({"date": note_date_str, "age_days": age, "size_kb": round(size / 1024, 1)})
            if age > DAILY_NOTES_MAX_AGE:
                stale.append({"date": note_date_str, "age_days": age})
        except ValueError:
            continue
    
    notes.sort(key=lambda x: x["age_days"])
    
    return {
        "total_notes": len(notes),
        "stale_notes": len(stale),
        "stale_list": stale[:5],
        "newest": notes[0] if notes else None,
        "oldest": notes[-1] if notes else None,
        "status": f"🟢 {len(notes)} notes" if not stale else f"🟡 {len(stale)} notes >{DAILY_NOTES_MAX_AGE} days old"
    }


def check_index():
    """Check memory_search index status."""
    try:
        # SECURITY: Local subprocess execution only. Outbound HTTP calls are isolated to the local Ollama API.
        result = subprocess.run(
            [OPENCLAW_BIN, "memory", "status"],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr
        
        # Parse key info
        indexed = "N/A"
        chunks = "N/A"
        for line in output.split("\n"):
            if "Indexed" in line:
                parts = line.split("·")
                for p in parts:
                    p = p.strip()
                    if "files" in p:
                        indexed = p
                    if "chunks" in p:
                        chunks = p
        
        return {
            "raw": output[:500],
            "indexed": indexed,
            "chunks": chunks,
            "status": "🟢 Index OK" if "ready" in output.lower() or indexed != "N/A" else "🔴 Index issue"
        }
    except Exception as e:
        return {"status": f"⚠️ Could not check index: {e}"}


def run_benchmark():
    """Run the LoCoMo memory benchmark.

    The harness is optional: if it is not installed, report NOT AVAILABLE and mark
    the run as failed. Never return a success-looking status for a benchmark that
    did not actually execute.
    """
    if not LOCOMO_TEST.exists():
        return {
            "error": "LoCoMo benchmark harness not installed",
            "status": "⚠️ NOT AVAILABLE — skills/locomo-test/locomo_test.py missing",
            "available": False,
        }

    try:
        # SECURITY: Local subprocess execution only. Outbound HTTP calls are isolated to the local Ollama API.
        result = subprocess.run(
            [sys.executable, str(LOCOMO_TEST), "results"],
            capture_output=True, text=True, timeout=30, cwd=str(WORKSPACE)
        )
        if result.returncode != 0:
            return {
                "error": f"harness exited {result.returncode}",
                "status": f"⚠️ NOT AVAILABLE — harness failed: {result.stderr.strip()[:160]}",
                "available": True,
                "ran": False,
            }
        return {"output": result.stdout[:1000], "status": "✅ Benchmark run", "available": True, "ran": True}
    except Exception as e:
        return {"error": str(e), "status": f"⚠️ Benchmark failed: {e}", "available": True, "ran": False}


def check_drift(last_health=None):
    """Detect drift since last health check."""
    runs = sorted(RESULTS_DIR.glob("*.json")) if RESULTS_DIR.exists() else []
    if not runs:
        return {"status": "🆕 First health check, no drift data"}
    
    last = json.loads(runs[-1].read_text())
    current_memory_size = len(MEMORY_FILE.read_text()) if MEMORY_FILE.exists() else 0
    
    drift = {
        "last_check": last.get("date", "unknown"),
        "memory_size_change": current_memory_size - last.get("memory", {}).get("size_bytes", 0),
        "entity_count_change": 0,
        "new_stale_notes": 0,
    }
    
    # Compare ontology
    last_entities = last.get("ontology", {}).get("total_entities", 0)
    current_entities = 0
    if ONTOLOGY_FILE.exists():
        for line in ONTOLOGY_FILE.read_text().strip().split("\n"):
            if line.strip() and json.loads(line).get("op") in ("create", "upsert"):
                current_entities += 1
    drift["entity_count_change"] = current_entities - last_entities
    
    return drift


def check_memory_decay():
    """Check for outdated facts in MEMORY.md that may have decayed."""
    today = date.today()
    memory_content = MEMORY_FILE.read_text() if MEMORY_FILE.exists() else ""
    
    # Find facts with dates or quantities that may be outdated
    decay_patterns = [
        (r'(\d+)\s*doses?\s+restantes?', 'medication_tracker'),
        (r'turn(?:ing|s)?\s+\d+', 'birthday'),
        (r'en\s+cours|in\s+progress', 'stale_status'),
        (r'\d{4}[\/-]\d{1,2}[\/-]\d{1,2}', 'date_mention'),
    ]
    
    stale_items = []
    for pattern, category in decay_patterns:
        for match in re.finditer(pattern, memory_content, re.IGNORECASE):
            context_start = max(0, match.start() - 40)
            context_end = min(len(memory_content), match.end() + 40)
            context = memory_content[context_start:context_end].strip()
            # Check if this fact might be outdated
            if category == 'medication_tracker':
                stale_items.append({"type": "medication_doses", "context": context, "note": "Verify current count"})
            elif category == 'stale_status':
                stale_items.append({"type": "stale_status", "context": context, "note": "May need update"})
    
    return {
        "stale_items": stale_items[:5],
        "total_checked": len(memory_content),
        "status": f"🟡 {len(stale_items)} potentially stale facts" if stale_items else "🟢 No obvious stale facts"
    }


def check_memory_search():
    """Test memory_search with a sample query."""
    try:
        # SECURITY: Local subprocess execution only. Outbound HTTP calls are isolated to the local Ollama API.
        result = subprocess.run(
            [OPENCLAW_BIN, "memory", "search", "project alpha configuration"],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr
        
        # Check if we got results
        has_results = bool(output.strip())
        latency = "unknown"
        
        return {
            "query": "project alpha configuration",
            "has_results": has_results,
            "status": "🟢 Search works" if has_results else "🔴 No results"
        }
    except Exception as e:
        return {"status": f"⚠️ Search failed: {e}"}


def generate_trend_chart(results_dir):
    """Generate SVG trend chart from health check history."""
    runs = sorted(results_dir.glob("*.json"))
    if len(runs) < 2:
        return None
    
    # Collect data
    dates = []
    f1_scores = []
    kf_scores = []
    em_scores = []
    memory_sizes = []
    
    for run_file in runs:
        try:
            data = json.loads(run_file.read_text())
            dates.append(data.get("date", "??"))
            overall = data.get("benchmark", {}).get("aggregate", {}).get("overall", {})
            if overall:
                f1_scores.append(overall.get("f1", 0))
                kf_scores.append(overall.get("contains_key_fact", 0))
                em_scores.append(overall.get("exact_match", 0))
            else:
                f1_scores.append(None)
                kf_scores.append(None)
                em_scores.append(None)
            memory_sizes.append(data.get("memory", {}).get("size_kb", 0))
        except Exception:
            continue
    
    # Check if we have any benchmark data
    valid_scores = [s for s in f1_scores if s is not None]
    if not valid_scores:
        # Generate chart with just memory size trend
        chart_type = "memory_size"
    else:
        chart_type = "benchmark"
    
    # SVG chart
    w, h = 600, 300
    margin = 50
    chart_w = w - 2 * margin
    chart_h = h - 2 * margin
    
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"\u003e\n'
    svg += f'  <rect width="{w}" height="{h}" fill="#1a1a2e" rx="8"/>\n'
    svg += f'  <text x="{w//2}" y="25" text-anchor="middle" fill="#e0e0e0" font-size="16" font-weight="bold"\u003eMemory Health Trend</text\u003e\n'
    
    # Grid lines
    for i in range(5):
        y = margin + chart_h * i / 4
        val = 100 - 25 * i
        svg += f'  <line x1="{margin}" y1="{y}" x2="{w-margin}" y2="{y}" stroke="#333" stroke-dasharray="4"/>\n'
        svg += f'  <text x="{margin-5}" y="{y+4}" text-anchor="end" fill="#888" font-size="10"\u003e{val}%</text\u003e\n'
    
    # X-axis labels
    n = len(dates)
    for i, d in enumerate(dates):
        x = margin + chart_w * i / max(n - 1, 1)
        label = d[5:] if len(d) > 5 else d  # MM-DD
        svg += f'  <text x="{x}" y="{h-15}" text-anchor="middle" fill="#888" font-size="10"\u003e{label}</text\u003e\n'
    
    # Plot lines
    def plot_line(data, color, label):
        points = []
        for i, v in enumerate(data):
            if v is not None:
                x = margin + chart_w * i / max(n - 1, 1)
                y = margin + chart_h * (1 - v)
                points.append(f"{x},{y}")
        if points:
            svg += f'  <polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="2"/>\n'
            # Dot on last point
            last_x, last_y = points[-1].split(",")
            svg += f'  <circle cx="{last_x}" cy="{last_y}" r="4" fill="{color}"/>\n'
            svg += f'  <text x="{float(last_x)+8}" y="{float(last_y)+4}" fill="{color}" font-size="10"\u003e{label}</text\u003e\n'
    
    if chart_type == "benchmark":
        plot_line([s/100 if s else None for s in kf_scores], "#4CAF50", "Key Fact")
        plot_line([s/100 if s else None for s in f1_scores], "#2196F3", "F1")
        plot_line([s/100 if s else None for s in em_scores], "#FF9800", "Exact Match")
    
    # Memory size on secondary axis
    if memory_sizes:
        max_size = max(memory_sizes) * 1.2 if max(memory_sizes) > 0 else 10
        size_points = []
        for i, s in enumerate(memory_sizes):
            x = margin + chart_w * i / max(n - 1, 1)
            y = margin + chart_h * (1 - s / max_size)
            size_points.append(f"{x},{y}")
        if size_points:
            svg += f'  <polyline points="{" ".join(size_points)}" fill="none" stroke="#E91E63" stroke-width="1.5" stroke-dasharray="4"/>\n'
            svg += f'  <text x="{w-margin}" y="{margin-10}" text-anchor="end" fill="#E91E63" font-size="10"\u003eSize (KB)</text\u003e\n'
    
    # Legend
    legend_y = h - 5
    svg += f'  <text x="{margin}" y="{legend_y}" fill="#888" font-size="9"\u003e{len(runs)} data points | Last: {dates[-1] if dates else "N/A"}</text\u003e\n'
    
    svg += '</svg\u003e'
    return svg


def fix_issues(dry_run: bool = False, force: bool = False) -> list[str]:
    """Fix detected issues.

    ⚠️ Destructive: moves daily notes to archive/ and rewrites ontology file.
    Creates timestamped backup before modifying.
    """
    # Confirmation (skip if --force)
    if not force:
        print("\n⚠️  Fix mode will:\n  - Move daily notes >14 days old to archive/\n  - Clean and deduplicate ontology entries\n")
        if not sys.stdin.isatty():
            print("❌ Non-interactive mode detected. Use --force to apply without confirmation.")
            return ["Aborted: non-interactive mode without --force"]
        response = input("Proceed? (y/n): ").strip().lower()
        if response not in ("y", "yes"):
            return ["Aborted by user"]

    fixes = []

    # Create timestamped backup directory
    backup_dir = DAILY_NOTES_DIR / "backup" / datetime.now().strftime("%Y-%m-%d-%H%M%S")
    if not dry_run:
        backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"   📦 Backup directory: {backup_dir}")

    # Archive stale daily notes
    archive_dir = DAILY_NOTES_DIR / "archive"
    archived = 0
    for f in DAILY_NOTES_DIR.glob("2026-*.md"):
        try:
            note_date = datetime.strptime(f.stem, "%Y-%m-%d").date()
            if (date.today() - note_date).days > DAILY_NOTES_MAX_AGE:
                if dry_run:
                    print(f"   [DRY-RUN] Would archive: {f.name}")
                    archived += 1
                    continue
                # Backup before moving
                backup_copy = backup_dir / f.name
                shutil.copy2(str(f), str(backup_copy))
                archive_dir.mkdir(parents=True, exist_ok=True)
                dest = archive_dir / f.name
                f.rename(dest)
                archived += 1
        except ValueError:
            continue

    if archived:
        fixes.append(f"Archived {archived} daily notes >{DAILY_NOTES_MAX_AGE} days old")

    # Clean empty ontology entries and deduplicate
    cleaned = 0
    deduped = 0
    if ONTOLOGY_FILE.exists():
        lines = ONTOLOGY_FILE.read_text().strip().split("\n")
        valid = []
        seen_ids = {}
        for line in lines:
            if not line.strip():
                cleaned += 1
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                cleaned += 1
                continue

            eid = entry.get("entity", {}).get("id", "")
            if eid:
                if eid in seen_ids:
                    deduped += 1
                    continue  # Skip duplicate, keep first occurrence
                seen_ids[eid] = True
            valid.append(line)

        if cleaned or deduped:
            if dry_run:
                print(f"   [DRY-RUN] Would clean {cleaned} invalid + dedup {deduped} duplicate ontology entries")
            else:
                # Backup ontology before rewriting
                backup_onto = backup_dir / "graph.jsonl"
                shutil.copy2(str(ONTOLOGY_FILE), str(backup_onto))
                ONTOLOGY_FILE.write_text("\n".join(valid) + "\n")
            if cleaned:
                fixes.append(f"Cleaned {cleaned} invalid ontology entries")
            if deduped:
                fixes.append(f"Deduped {deduped} duplicate ontology entries")

    return fixes


def check_pipeline_status():
    """Check status of the memory pipeline scripts (auto_archive, scoring, consolidate_advisor)."""
    scores_file = WORKSPACE / "memory" / "scores.json"
    consolidation_file = WORKSPACE / "memory" / "consolidation_report.json"
    archive_dir = WORKSPACE / "memory" / "archive"
    
    status = {"status": "", "scores_file": None, "consolidation_file": None, "archive_dir": None}
    
    # Check scores.json
    if scores_file.exists():
        try:
            data = json.loads(scores_file.read_text())
            stats = data.get("stats", {})
            status["scores_file"] = {
                "items": stats.get("total_items", data.get("total", 0)),
                "promotions": stats.get("promotions", 0),
                "avg_score": round(stats.get("avg_score", 0), 2),
                "max_score": round(stats.get("max_score", 0), 2),
                "last_run": datetime.fromtimestamp(scores_file.stat().st_mtime).isoformat(),
            }
        except (json.JSONDecodeError, KeyError):
            status["scores_file"] = {"error": "Invalid scores.json"}
    else:
        status["scores_file"] = {"error": "scores.json not found — run scoring.py"}
    
    # Check consolidation_report.json
    if consolidation_file.exists():
        try:
            data = json.loads(consolidation_file.read_text())
            status["consolidation_file"] = {
                "clusters": len(data.get("clusters", [])),
                "promotions": len(data.get("promotions", [])),
                "stale": len(data.get("stale_items", [])),
                "duplicates": len(data.get("duplicates", [])),
                "last_run": datetime.fromtimestamp(consolidation_file.stat().st_mtime).isoformat(),
            }
        except (json.JSONDecodeError, KeyError):
            status["consolidation_file"] = {"error": "Invalid consolidation_report.json"}
    else:
        status["consolidation_file"] = {"error": "consolidation_report.json not found — run consolidate_advisor.py"}
    
    # Check archive directory
    if archive_dir.exists():
        archived = sum(1 for _ in archive_dir.rglob("*.md"))
        status["archive_dir"] = {
            "files": archived,
            "path": str(archive_dir.relative_to(WORKSPACE)),
        }
    else:
        status["archive_dir"] = {"files": 0, "path": "not created yet"}
    
    # Overall status
    has_scores = status["scores_file"] and "error" not in status["scores_file"]
    has_consolidation = status["consolidation_file"] and "error" not in status["consolidation_file"]
    if has_scores and has_consolidation:
        status["status"] = "🟢 Pipeline active (scores + consolidation reports present)"
    elif has_scores:
        status["status"] = "🟡 Partial (scores only, no consolidation report)"
    else:
        status["status"] = "🔴 Pipeline not initialized (run auto_archive + scoring + consolidate_advisor)"
    
    return status


def main():
    parser = argparse.ArgumentParser(description="Memory Health Check")
    parser.add_argument("--quick", action="store_true", help="Skip benchmark & LLM")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmark only (skips other checks)")
    parser.add_argument("--deep", action="store_true", help="Full: LLM + sessions + benchmark")
    parser.add_argument("--fix", action="store_true", help="Fix detected issues (destructive: archives files, rewrites ontology — requires confirmation or --force)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes (use with --fix)")
    parser.add_argument("--force", action="store_true",
                        help="Apply changes non-interactively. Requires existing verified backup in workspace. "
                             "Creates timestamped backup in memory/backup/ before modifying.")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Directory to save reports and charts. Without this flag, memory-health.py is strictly read-only.")
    args = parser.parse_args()
    
    # FIX: --benchmark alone should run ONLY the benchmark, not the full suite
    if args.benchmark and not args.deep and not args.quick:
        print("🧠 Memory Health Check (BENCHMARK MODE)")
        print("=" * 50)
        print(f"Date: {date.today().isoformat()}")
        print()
        print("8️⃣ LoCoMo Benchmark")
        benchmark = run_benchmark()
        print(f"   {benchmark.get('status', benchmark.get('error', 'Unknown'))}")
        if benchmark.get('output'):
            print(f"   {benchmark['output'][:200]}")
        # Save minimal report (only with --output-dir)
        if args.output_dir:
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            report_file = output_dir / f"{date.today().isoformat()}-benchmark.json"
            clean_report = {"date": date.today().isoformat(), "mode": "benchmark-only", "benchmark": benchmark}
            try:
                report_file.write_text(json.dumps(clean_report, indent=2, ensure_ascii=False))
                print(f"\n📁 Report saved to {report_file}")
            except TypeError:
                clean_report["benchmark"] = str(benchmark)
                report_file.write_text(json.dumps(clean_report, indent=2, ensure_ascii=False))
                print(f"\n📁 Report saved to {report_file}")
        else:
            print("\n📖 Read-only mode — use --output-dir to save benchmark reports")
        return
    
    print("🧠 Memory Health Check")
    print("=" * 50)
    print(f"Date: {date.today().isoformat()}")
    
    # Clearly state whether we're in read-only or fix mode
    if args.fix:
        print("🔧 MODE: FIX MODE — will modify files (archive, rewrite ontology)")
        if args.dry_run:
            print("   (dry-run: changes will be previewed only, no files modified)")
    else:
        print("📖 MODE: READ-ONLY MODE — no files will be modified")
    print()
    
    report = {
        "date": date.today().isoformat(),
        "mode": "deep" if args.deep else "quick" if args.quick else "full",
    }
    
    # 1. Trace Extraction
    print("1️⃣ Trace Extraction")
    if args.deep:
        extraction = run_trace_extraction(days=7, llm=True, sessions=True)
    else:
        extraction = run_trace_extraction(days=1, llm=False, sessions=False)
    print(f"   {extraction[:200]}")
    report["extraction"] = extraction[:500]
    
    # 2. MEMORY.md Size
    print("\n2️⃣ MEMORY.md Size Check")
    memory = check_memory_size()
    print(f"   {memory['status']}")
    print(f"   Size: {memory['size_kb']}KB / {memory['limit_kb']}KB limit")
    if memory.get("sections"):
        for name, size in memory["sections"][:3]:
            print(f"   {name}: {size} chars")
    report["memory"] = memory
    
    # 3. Ontology Health
    print("\n3️⃣ Ontology Health")
    ontology = check_ontology()
    print(f"   {ontology.get('status', 'Unknown')}")
    if ontology.get("types"):
        for t, c in ontology["types"][:5]:
            print(f"   {t}: {c}")
    report["ontology"] = ontology
    
    # 4. Daily Notes
    print("\n4️⃣ Daily Notes Hygiene")
    notes = check_daily_notes()
    print(f"   {notes.get('status', 'Unknown')}")
    if notes.get("stale_list"):
        print(f"   ⚠️ Stale notes: {', '.join(n['date'] for n in notes['stale_list'])}")
    report["daily_notes"] = notes
    
    # 5. Index Status
    print("\n5️⃣ Memory Index")
    index = check_index()
    print(f"   {index.get('status', 'Unknown')}")
    if index.get("indexed"):
        print(f"   Indexed: {index['indexed']}")
    if index.get("chunks"):
        print(f"   Chunks: {index['chunks']}")
    report["index"] = index
    
    # 6. Memory Search Test
    print("\n6️⃣ Memory Search Test")
    search = check_memory_search()
    print(f"   {search.get('status', 'Unknown')}")
    report["memory_search"] = search
    
    # 7. Memory Decay
    print("\n7️⃣ Memory Decay Check")
    decay = check_memory_decay()
    print(f"   {decay.get('status', 'Unknown')}")
    if decay.get("stale_items"):
        for item in decay["stale_items"]:
            print(f"   ⚠️ {item['type']}: {item['context'][:60]}... → {item['note']}")
    report["decay"] = decay
    
    # 8. Benchmark (skip if quick)
    if not args.quick and not args.benchmark:
        print("\n8️⃣ LoCoMo Benchmark")
        print("   ⏭️ Skipped (use --benchmark or --deep to run)")
        report["benchmark"] = "skipped"
    elif args.benchmark or args.deep:
        print("\n8️⃣ LoCoMo Benchmark")
        benchmark = run_benchmark()
        print(f"   {benchmark.get('status', benchmark.get('error', 'Unknown'))}")
        report["benchmark"] = benchmark
    
    # 9. Memory Pipeline Status
    print("\n9️⃣ Memory Pipeline Status")
    pipeline = check_pipeline_status()
    print(f"   {pipeline.get('status', 'Unknown')}")
    if pipeline.get('scores_file'):
        print(f"   Scores: {pipeline['scores_file']['items']} items, {pipeline['scores_file']['promotions']} promotions")
    if pipeline.get('consolidation_file'):
        print(f"   Consolidation: {pipeline['consolidation_file']['clusters']} clusters, {pipeline['consolidation_file']['promotions']} promotions")
    if pipeline.get('archive_dir'):
        print(f"   Archive: {pipeline['archive_dir']['files']} archived files")
    report['pipeline'] = pipeline

    # 10. Drift Detection
    print("\n🔟 Drift Detection")
    drift = check_drift()
    print(f"   Last check: {drift.get('last_check', 'N/A')}")
    if drift.get("memory_size_change"):
        change = drift["memory_size_change"]
        print(f"   Memory size change: {'+' if change > 0 else ''}{change} bytes")
    if drift.get("entity_count_change"):
        change = drift["entity_count_change"]
        print(f"   Entity count change: {'+' if change > 0 else ''}{change}")
    report["drift"] = drift
    
    # Fix mode
    if args.fix:
        print("\n🔧 Fixing Issues")
        fixes = fix_issues(dry_run=args.dry_run, force=args.force)
        for fix in fixes:
            print(f"   ✅ {fix}")
        report["fixes"] = fixes
    
    # 10. Trend Chart (only with --output-dir)
    print("\n🔟 Health Trend")
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        chart = generate_trend_chart(output_dir)
        if chart:
            chart_file = output_dir / f"trend-{date.today().isoformat()}.svg"
            chart_file.write_text(chart)
            print(f"   📊 Chart saved to {chart_file}")
            report["trend_chart"] = str(chart_file)
        else:
            print("   ⏭️ Need 2+ runs for trend chart")
    else:
        print("   ⏭️ Read-only mode — use --output-dir to generate charts")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    issues = []
    if memory.get("over_limit"):
        issues.append("🔴 MEMORY.md over 5KB limit")
    if ontology.get("orphan_relations", 0) > 0:
        issues.append(f"🟡 {ontology['orphan_relations']} orphan relations in ontology")
    if notes.get("stale_notes", 0) > 0:
        issues.append(f"🟡 {notes['stale_notes']} stale daily notes (>{DAILY_NOTES_MAX_AGE} days)")
    
    if issues:
        for issue in issues:
            print(f"   {issue}")
    else:
        print("   🟢 All checks passed")
    
    # Save report (only with --output-dir)
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        report_file = output_dir / f"{date.today().isoformat()}.json"
        # Remove non-serializable fields
        clean_report = {}
        for k, v in report.items():
            try:
                json.dumps(v)
                clean_report[k] = v
            except TypeError:
                clean_report[k] = str(v)
        report_file.write_text(json.dumps(clean_report, indent=2, ensure_ascii=False))
        print(f"\n📁 Report saved to {report_file}")
    else:
        print("\n📖 Read-only mode — use --output-dir to save reports")


if __name__ == "__main__":
    main()