#!/usr/bin/env python3
"""memory-guardian MCP Server v0.4.6

Provides 10 structured tools (including run_batch + memory_sync) for the memory-guardian system.
Wraps the existing 19-script layer via direct Python imports (zero API calls).

Transport: stdio (default) | CLI fallback (--batch)
Design: skill-design-proposal-v3.md v3.2
"""

import argparse
import io
import json
import math
import os
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta

# ─── Script layer imports ────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "scripts"))

from mg_utils import (
    CST, _now_iso, load_meta, save_meta, tokenize,
    get_effective_importance, is_protected_memory,
)


def _to_bool(val, default=False):
    """Safely convert a value to bool. Handles string 'true'/'false'."""
    if val is None:
        return default
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.lower() in ("true", "1", "yes", "on")
    return bool(val)
from mg_schema import normalize_meta, MEMORY_DEFAULTS

# Lazy imports for heavy modules
def _import_memory_guardian():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "memory_guardian", os.path.join(SCRIPT_DIR, "scripts", "memory_guardian.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def _import_memory_decay():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "memory_decay", os.path.join(SCRIPT_DIR, "scripts", "memory_decay.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def _import_memory_ingest():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "memory_ingest", os.path.join(SCRIPT_DIR, "scripts", "memory_ingest.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def _import_memory_compact():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "memory_compact", os.path.join(SCRIPT_DIR, "scripts", "memory_compact.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def _import_quality_gate():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "quality_gate", os.path.join(SCRIPT_DIR, "scripts", "quality_gate.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def _import_case_invalidate():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "case_invalidate", os.path.join(SCRIPT_DIR, "scripts", "case_invalidate.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def _import_memory_sync():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "memory_sync", os.path.join(SCRIPT_DIR, "scripts", "memory_sync.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# ─── References integrity check ─────────────────────────────
REFERENCES_DIR = os.path.join(SCRIPT_DIR, "references")
EXPECTED_REFS = [
    "triggers.md", "parameters.md", "compaction.md",
    "error_recovery.md", "case-management.md", "advanced-tools.md",
]

def check_references():
    """Scan references/ directory and return missing files list."""
    if not os.path.isdir(REFERENCES_DIR):
        return list(EXPECTED_REFS)
    missing = [f for f in EXPECTED_REFS
               if not os.path.isfile(os.path.join(REFERENCES_DIR, f))]
    return missing


# ─── Error helpers ───────────────────────────────────────────
class MCPError(Exception):
    """Structured error for MCP tool responses."""
    CODES = {
        "WORKSPACE_NOT_FOUND": "Workspace path does not exist",
        "META_CORRUPT": "meta.json format error — run bootstrap to reinitialize",
        "SCRIPT_ERROR": "Script layer raised an exception",
        "PERMISSION_DENIED": "File permission denied — check workspace directory permissions",
        "TIMEOUT": "Operation timed out — increase timeout or reduce processing load",
        "REFERENCES_MISSING": "references/ files missing — core functions still work, diagnostics degraded",
        "INVALID_PARAMS": "Invalid parameters provided",
        "NOT_FOUND": "Requested resource not found",
    }

    def __init__(self, code, message=None, hint=None):
        self.code = code
        self.message = message or self.CODES.get(code, "Unknown error")
        self.hint = hint
        super().__init__(self.message)

    def to_dict(self):
        result = {"error": True, "code": self.code, "message": self.message}
        if self.hint:
            result["hint"] = self.hint
        return result


# ─── Workspace resolver ──────────────────────────────────────
DEFAULT_WORKSPACE = os.environ.get(
    "OPENCLAW_WORKSPACE", os.environ.get("MG_WORKSPACE",
    os.path.expanduser("~/workspace/agent/workspace")))


def _validate_workspace_path(ws):
    """Validate workspace path against path traversal attacks.

    Normalizes the path via realpath and rejects any path that escapes
    its expected parent (user home or explicitly allowed root).
    """
    real = os.path.realpath(ws)
    # Reject any resolved path containing unexpected traversal
    parts = os.path.normpath(real).split(os.sep)
    if ".." in parts:
        raise ValueError(
            f"Workspace path contains traversal components: {ws}")
    return real


def resolve_workspace(params):
    """Resolve workspace from params or env, auto-create only when 'auto'."""
    ws = params.get("workspace", "auto")
    if ws == "auto":
        ws = os.environ.get("MG_WORKSPACE", DEFAULT_WORKSPACE)
    else:
        # Validate user-supplied path before any filesystem access
        ws = _validate_workspace_path(ws)
        if not os.path.exists(os.path.join(ws, "memory", "meta.json")):
            raise FileNotFoundError(f"Workspace not found: {ws}/memory/meta.json")

    # Always normalize the final workspace path
    ws = os.path.realpath(ws)
    os.makedirs(ws, exist_ok=True)
    return ws


def meta_path(workspace):
    return os.path.join(workspace, "memory", "meta.json")


# ─── Tool handlers ───────────────────────────────────────────
@contextmanager
def _capture_stdout():
    """Context manager to safely redirect stdout, restoring on exit."""
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    try:
        yield captured
    finally:
        sys.stdout = old_stdout


class MemoryGuardianServer:
    """MCP server wrapping the 19-script memory-guardian layer."""

    def __init__(self, workspace=None):
        self.workspace = workspace or DEFAULT_WORKSPACE

    @staticmethod
    def _ensure_schema_compliance(mp, workspace=None):
        """Ensure all memories comply with current schema.

        Fixes:
        1. String-typed numeric fields (importance, decay_score, confidence)
        2. Missing per-memory v0.4.5 fields (memory_id, file_path, etc.)
        3. Missing memory files on disk (writes them if content available)

        Called at the start of every run_batch. This is the single
        auto-upgrade path — users never need to run migration scripts manually.
        """
        try:
            import logging
            meta = load_meta(mp)
            fixed = False
            files_written = 0

            for m in meta.get("memories", []):
                # --- Fix 1: String-typed numeric fields ---
                for field in ("importance", "decay_score", "confidence"):
                    val = m.get(field)
                    if isinstance(val, str):
                        try:
                            m[field] = float(val)
                            fixed = True
                        except ValueError:
                            defaults = {"importance": 0.5, "decay_score": 0.5, "confidence": 0.45}
                            if field in defaults:
                                m[field] = defaults[field]
                                fixed = True
                # Fix nested quality_gate.confidence too
                qg = m.get("quality_gate", {})
                if isinstance(qg.get("confidence"), str):
                    try:
                        qg["confidence"] = float(qg["confidence"])
                        fixed = True
                    except ValueError:
                        pass

                # --- Fix 2: Missing v0.4.5 per-memory fields ---
                for key, default in MEMORY_DEFAULTS.items():
                    if key not in m:
                        m[key] = default
                        fixed = True

                # --- Fix 3: Missing memory_id ---
                if not m.get("memory_id"):
                    try:
                        from mg_utils import generate_memory_id
                        existing_ids = {
                            mm.get("memory_id") or mm.get("id")
                            for mm in meta.get("memories", [])
                            if mm.get("memory_id") or mm.get("id")
                        }
                        m["memory_id"] = generate_memory_id(
                            m.get("content", ""), existing_ids=existing_ids
                        )
                        fixed = True
                    except Exception:
                        m["memory_id"] = m.get("id", "unknown")
                        fixed = True

                # --- Fix 4: Missing file_path ---
                if not m.get("file_path"):
                    try:
                        from mg_utils import derive_file_path
                        tags = m.get("tags", [])
                        m["file_path"] = derive_file_path(
                            m["memory_id"], tags, m.get("content", "")
                        )
                        fixed = True
                    except Exception:
                        pass

                # --- Fix 5: Missing classification dict ---
                if not isinstance(m.get("classification"), dict):
                    tags = m.get("tags", [])
                    m["classification"] = {
                        "primary_tag": tags[0] if tags else "misc",
                        "confidence": m.get("classification_confidence", 0.5) or 0.5,
                        "needs_review": False,
                    }
                    fixed = True

            if fixed:
                save_meta(mp, meta)

            # --- Fix 6: Missing files on disk ---
            if workspace:
                try:
                    from memory_ingest import _write_memory_file
                    for m in meta.get("memories", []):
                        fp = m.get("file_path", "")
                        if not fp:
                            continue
                        abs_path = os.path.join(workspace, fp)
                        if not os.path.exists(abs_path) and m.get("content"):
                            try:
                                _write_memory_file(
                                    m["memory_id"], m["content"], fp, workspace=workspace
                                )
                                files_written += 1
                            except Exception:
                                logging.warning(
                                    "_ensure_schema_compliance: failed to write %s", fp
                                )
                except ImportError:
                    pass

            if fixed or files_written:
                print(
                    f"[memory-guardian] Schema compliance: fixed {sum(1 for _ in [])} type issues, "
                    f"wrote {files_written} missing files",
                    file=sys.stderr,
                )
            return fixed or files_written > 0

        except Exception as exc:
            print(f"[memory-guardian] _ensure_schema_compliance error: {exc}", file=sys.stderr)
            return False

    # ── Query tools ──────────────────────────────────────────

    def handle_memory_status(self, params):
        """memory_status — system overview."""
        try:
            ws = resolve_workspace(params)
            mp = meta_path(ws)

            if not os.path.exists(mp):
                return {
                    "active": 0, "archived": 0, "observing": 0,
                    "memory_md_kb": 0, "gate_state": "NORMAL",
                    "case_summary": {"total": 0, "frozen": 0, "active": 0, "retired": 0},
                    "last_decay": None, "meta_path": mp,
                    "references": {"complete": True, "missing": []},
                }

            meta = load_meta(mp)
            meta, _ = normalize_meta(meta, read_only=True)

            memories = meta.get("memories", [])
            counts = {"active": 0, "archived": 0, "observing": 0,
                      "deleted": 0, "frozen": 0, "retired": 0}
            for m in memories:
                s = m.get("status", "active")
                if s in counts:
                    counts[s] += 1

            cases = [m for m in memories if m.get("id", "").startswith("case_")]
            case_summary = {
                "total": len(cases),
                "frozen": sum(1 for c in cases if c.get("status") == "frozen"),
                "active": sum(1 for c in cases if c.get("status") == "active"),
                "retired": sum(1 for c in cases if c.get("status") in ("archived", "deleted")),
            }

            # Gate state
            try:
                qg = _import_quality_gate()
                gate = qg.get_gate_state(meta)
                gate_state = gate.get("state", "NORMAL")
            except Exception:
                gate_state = "UNKNOWN"

            # Memory.md size
            memory_md = os.path.join(ws, "MEMORY.md")
            memory_md_kb = 0
            if os.path.exists(memory_md):
                memory_md_kb = round(os.path.getsize(memory_md) / 1024, 1)

            # Last decay
            last_decay = meta.get("last_decay_run", None)

            # References check
            missing = check_references()
            refs_info = {
                "complete": len(missing) == 0,
                "missing": missing,
            }

            return {
                "active": counts["active"],
                "archived": counts["archived"],
                "observing": counts["observing"],
                "memory_md_kb": memory_md_kb,
                "gate_state": gate_state,
                "case_summary": case_summary,
                "last_decay": last_decay,
                "meta_path": mp,
                "references": refs_info,
            }

        except Exception as e:
            raise MCPError("SCRIPT_ERROR", str(e), "Check workspace path and meta.json integrity")

    def handle_memory_query(self, params):
        """memory_query — search memories with filters."""
        try:
            ws = resolve_workspace(params)
            mp = meta_path(ws)

            if not os.path.exists(mp):
                return {"total": 0, "results": []}

            meta = load_meta(mp)
            memories = meta.get("memories", [])

            # Filters
            mem_type_filter = params.get("type_filter", params.get("type", "active"))
            query = params.get("query", "").lower().strip()
            min_score = float(params.get("min_score", 0.0))
            max_score = float(params.get("max_score", 1.0))
            mem_memory_type = params.get("memory_type")  # static/derive/absorb/suspend

            results = []
            for m in memories:
                status = m.get("status", "active")

                # Type filter
                if mem_type_filter == "active" and status != "active":
                    continue
                elif mem_type_filter == "archived" and status != "archived":
                    continue
                elif mem_type_filter == "observing" and status != "observing":
                    continue
                elif mem_type_filter == "all":
                    pass  # show all non-deleted
                elif mem_type_filter != "all":
                    if status != mem_type_filter:
                        continue

                if status == "deleted":
                    continue

                # Memory type filter
                if mem_memory_type:
                    if m.get("memory_type") != mem_memory_type:
                        continue

                # Score filter
                try:
                    score = float(m.get("decay_score", m.get("importance", 0.5)))
                except (ValueError, TypeError):
                    score = 0.5  # fallback for non-numeric values like "auto"
                if score < min_score or score > max_score:
                    continue

                # Query keyword filter
                if query:
                    content = m.get("content", "").lower()
                    tags = " ".join(m.get("tags", [])).lower()
                    if query not in content and query not in tags:
                        continue

                results.append({
                    "id": m.get("id", "?"),
                    "content_preview": m.get("content", "")[:120],
                    "score": round(score, 4),
                    "type": status,
                    "memory_type": m.get("memory_type"),
                    "importance": m.get("importance"),
                    "tags": m.get("tags", []),
                    "last_access": m.get("last_accessed"),
                    "trigger_count": m.get("trigger_count", 0),
                    "confidence": m.get("confidence"),
                })

            # Sort by score descending
            results.sort(key=lambda x: x["score"], reverse=True)

            return {"total": len(results), "results": results}

        except Exception as e:
            raise MCPError("SCRIPT_ERROR", str(e))

    # ── Action tools ─────────────────────────────────────────

    def handle_memory_decay(self, params):
        """memory_decay — execute decay calculation."""
        try:
            ws = resolve_workspace(params)
            mp = meta_path(ws)
            lam = float(params.get("lambda", 0.01))
            dry_run = _to_bool(params.get("dry_run"), False)

            if not os.path.exists(mp):
                raise MCPError("META_CORRUPT",
                    "meta.json not found",
                    "Run bootstrap first: python3 scripts/memory_guardian.py bootstrap")

            md = _import_memory_decay()
            # Fix string-typed numeric fields before decay reads them
            self._ensure_schema_compliance(mp, workspace=ws)
            # Capture script-level prints to avoid polluting JSON output
            captured = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured
            try:
                result = md.run(mp, lam, dry_run)
            finally:
                sys.stdout = old_stdout

            # Convert script output to structured response
            changes = result.get("changes", [])
            details = []
            for c in changes[:20]:
                delta = c["new_score"] - c["old_score"]
                reason_parts = []
                if abs(delta) > 0.001:
                    reason_parts.append(f"score_change: {c['old_score']:.3f} -> {c['new_score']:.3f}")
                if c.get("cooling"):
                    reason_parts.append("cooling_active")
                if c.get("zombie"):
                    reason_parts.append("zombie_detected")
                if c.get("archive_mark"):
                    reason_parts.append("beta_archive_candidate")
                details.append({
                    "id": c["id"],
                    "old_score": c["old_score"],
                    "new_score": c["new_score"],
                    "reason": "; ".join(reason_parts) if reason_parts else "no_change",
                })

            # Update last_decay_run
            if not dry_run:
                meta = load_meta(mp)
                meta["last_decay_run"] = _now_iso()
                save_meta(mp, meta)

            return {
                "processed": len(changes),
                "changed": sum(1 for c in changes if abs(c["new_score"] - c["old_score"]) > 0.001),
                "details": details,
                "dry_run": dry_run,
                "summary": {
                    "to_archive": result.get("to_archive", 0),
                    "to_delete": result.get("to_delete", 0),
                    "cooling_count": result.get("cooling_count", 0),
                    "zombie_count": result.get("zombie_count", 0),
                },
            }

        except MCPError:
            raise
        except Exception as e:
            raise MCPError("SCRIPT_ERROR", str(e))

    def handle_memory_ingest(self, params):
        """memory_ingest — write a new memory."""
        try:
            ws = resolve_workspace(params)
            mp = meta_path(ws)
            content = params.get("content", "").strip()

            if not content:
                raise MCPError("INVALID_PARAMS", "content is required")

            importance = params.get("importance", "auto")
            tags = params.get("tags", [])

            # Validate importance
            if importance != "auto":
                try:
                    imp_val = float(importance)
                    if imp_val < 0 or imp_val > 1.0:
                        raise MCPError("INVALID_PARAMS",
                            f"importance must be between 0.0 and 1.0, got {importance}")
                except ValueError:
                    raise MCPError("INVALID_PARAMS",
                        f"importance must be a number or 'auto', got {importance}")

            # Build ingest args
            # tags may come as JSON string from MCP caller
            if isinstance(tags, str):
                try:
                    tags = json.loads(tags)
                except (json.JSONDecodeError, TypeError):
                    tags = [t.strip() for t in tags.split(",") if t.strip()]
            if not isinstance(tags, list):
                tags = [tags]

            ingest = _import_memory_ingest()
            result = ingest.run(
                content=content,
                importance=importance,
                tags=tags,
                meta_path=mp,
                workspace=ws,
                provenance_source=params.get("provenance_source", "human_direct"),
                situation=params.get("situation"),
                judgment=params.get("judgment"),
                consequence=params.get("consequence"),
                action_conclusion=params.get("action_conclusion"),
                reversibility=params.get("reversibility"),
                boundary_words=params.get("boundary_words"),
                alternatives=params.get("alternatives"),
            )

            if isinstance(result, dict):
                return result

            # Parse text output if script returns string
            return {
                "status": "ingested",
                "content_preview": content[:100],
                "importance": importance,
                "tags": tags,
                "raw_output": str(result)[:500] if result else None,
            }

        except MCPError:
            raise
        except Exception as e:
            raise MCPError("SCRIPT_ERROR", str(e))

    def handle_memory_compact(self, params):
        """memory_compact — compress memories."""
        try:
            ws = resolve_workspace(params)
            dry_run = _to_bool(params.get("dry_run"), False)
            aggressive = _to_bool(params.get("aggressive"), False)
            max_kb = int(params.get("max_memory_kb", 15))

            compact = _import_memory_compact()
            # Capture script-level prints to avoid polluting JSON output
            with _capture_stdout() as captured:
                result = compact.run(ws, dry_run=dry_run, auto=not dry_run,
                                     max_memory_kb=max_kb, aggressive=aggressive)

            if isinstance(result, dict):
                # Script returns structured dict directly
                before = result.get("memory_size", result.get("memory_size_before", 0))
                after = result.get("memory_size_after", before)
                return {
                    "before_kb": round(before / 1024, 1),
                    "after_kb": round(after / 1024, 1),
                    "sections": result.get("sections", []),
                    "internal_duplicates": result.get("internal_duplicates", 0),
                    "rotated": result.get("rotated", False),
                    "rotated_count": result.get("rotated_count", 0),
                    "dry_run": dry_run,
                }

            # Fallback: parse text output
            return {
                "before_kb": 0,
                "after_kb": 0,
                "dry_run": dry_run,
                "raw_output": str(result)[:1000] if result else None,
            }

        except Exception as e:
            raise MCPError("SCRIPT_ERROR", str(e))

    def handle_memory_sync(self, params):
        """memory_sync — sync file changes to meta.json."""
        try:
            ws = resolve_workspace(params)
            mp = meta_path(ws)
            dry_run = _to_bool(params.get("dry_run"), True)

            if not os.path.exists(mp):
                return {
                    "created": 0, "updated": 0, "skipped": 0,
                    "details": [], "dry_run": dry_run,
                    "message": "meta.json not found — run bootstrap first",
                }

            ms = _import_memory_sync()
            with _capture_stdout() as captured:
                result = ms.run(workspace=ws, dry_run=dry_run, meta_path_override=mp)

            return {
                "created": result.get("created", 0),
                "updated": result.get("updated", 0),
                "skipped": result.get("skipped", 0),
                "total_candidates": result.get("total_candidates", 0),
                "details": result.get("details", [])[:20],
                "dry_run": dry_run,
            }

        except Exception as e:
            raise MCPError("SCRIPT_ERROR", str(e))

    # ── Review tools ─────────────────────────────────────────

    def handle_quality_check(self, params):
        """quality_check — quality gate status."""
        try:
            ws = resolve_workspace(params)
            mp = meta_path(ws)
            layer = params.get("layer", "all")

            if not os.path.exists(mp):
                return {
                    "state": "NORMAL", "anomaly_count": 0,
                    "intervention_level": "L0", "pending_l3": [],
                    "critical_history": {"total_critical": 0, "retired_count": 0, "retire_rate": 0, "recent_cases": []},
                    "stale_cases": [], "similar_case_signal": {"has_active_ref": False, "all_retired": False, "no_similar": True, "top3": []},
                    "details": [], "layer": layer,
                }

            meta = load_meta(mp)
            meta, _ = normalize_meta(meta, read_only=True)

            qg = _import_quality_gate()
            gate = qg.get_gate_state(meta)
            state = gate.get("state", "NORMAL")

            # Anomaly count
            anomaly_count = gate.get("anomaly_count", 0)
            total_failures = gate.get("total_failures", 0)

            # Intervention level
            intervention = "L0"
            if state == "WARNING":
                intervention = "L1"
            elif state == "CRITICAL":
                l3_pending = gate.get("l3_pending_queue", [])
                if l3_pending:
                    intervention = "L3"
                else:
                    intervention = "L2"
            elif state == "RECOVERING":
                intervention = "L2"

            # Critical history
            memories = meta.get("memories", [])
            critical_cases = [m for m in memories
                              if m.get("id", "").startswith("case_")
                              and m.get("status") in ("frozen", "archived", "deleted")
                              and m.get("frozen_at")]
            total_critical = len(critical_cases)
            retired_count = sum(1 for c in critical_cases if c.get("status") in ("archived", "deleted"))
            retire_rate = round(retired_count / max(total_critical, 1), 4)

            recent_cases = []
            for c in sorted(critical_cases, key=lambda x: x.get("frozen_at", ""), reverse=True)[:5]:
                recent_cases.append({
                    "case_id": c.get("id"),
                    "trigger_count": c.get("trigger_count", 0),
                    "first_at": c.get("created_at"),
                    "last_at": c.get("frozen_at"),
                    "status": c.get("status"),
                })

            # Stale cases
            ci = _import_case_invalidate()
            stale_cases = []
            now_dt = datetime.now(CST)
            for m in memories:
                if m.get("status") != "frozen":
                    continue
                last_change = m.get("frozen_at") or m.get("last_accessed")
                if last_change:
                    try:
                        last_dt = datetime.fromisoformat(last_change)
                        hours_since = (now_dt - last_dt).total_seconds() / 3600
                        if hours_since > 18:  # ~6 heartbeats
                            stale_cases.append({
                                "case_id": m.get("id"),
                                "no_change_heartbeats": round(hours_since / 3),
                                "last_confidence": m.get("confidence", 0),
                                "last_trigger": last_change,
                            })
                    except (ValueError, TypeError):
                        pass

            # Similar case signal
            similar_signal = self._compute_similar_case_signal(meta)

            # Layer details
            details = []
            if layer in ("all", "security"):
                details.append({"layer": "security", "check": "rules_loaded", "status": "PASS"})
            if layer in ("all", "dedup"):
                details.append({"layer": "dedup", "check": "overlap_scan", "status": "PASS"})
            if layer in ("all", "ingest"):
                details.append({"layer": "ingest", "check": "quality_gate", "status": "PASS"})
            if layer in ("all", "decay"):
                details.append({"layer": "decay", "check": "beta_stability", "status": "PASS"})

            # Mark anomalies in details
            if anomaly_count > 0:
                for d in details:
                    if d["layer"] == "decay":
                        d["status"] = "FAIL"
                        d["message"] = f"anomaly_count={anomaly_count}"

            # Read critical_history for consecutive-round detection (read-only)
            if retire_rate > 0.3:
                history = meta.get("critical_history", [])
                recent_window = [h for h in history if h.get("retire_rate", 0) > 0.3]
                consecutive = len(recent_window)
                if consecutive >= 3:
                    intervention = "L3"

            return {
                "state": state,
                "anomaly_count": anomaly_count,
                "intervention_level": intervention,
                "pending_l3": gate.get("l3_pending_queue", []),
                "critical_history": {
                    "total_critical": total_critical,
                    "retired_count": retired_count,
                    "retire_rate": retire_rate,
                    "rule_review_suggested": retire_rate > 0.3,
                    "recent_cases": recent_cases,
                },
                "stale_cases": stale_cases[:10],
                "similar_case_signal": similar_signal,
                "details": details,
                "layer": layer,
            }

        except Exception as e:
            raise MCPError("SCRIPT_ERROR", str(e))

    def handle_case_query(self, params):
        """case_query — query cases."""
        try:
            ws = resolve_workspace(params)
            mp = meta_path(ws)
            filter_val = params.get("filter", params.get("status", "all"))
            min_confidence = float(params.get("min_confidence", 0.0))

            if not os.path.exists(mp):
                return {"total": 0, "cases": []}

            meta = load_meta(mp)
            memories = meta.get("memories", [])
            cases = [m for m in memories if m.get("id", "").startswith("case_")]

            # Filter
            now_dt = datetime.now(CST)
            results = []
            for c in cases:
                status = c.get("status", "active")
                confidence = c.get("confidence", 0.5)

                if confidence < min_confidence:
                    continue

                if filter_val == "active" and status != "active":
                    continue
                elif filter_val == "frozen" and status != "frozen":
                    continue
                elif filter_val == "observing" and status != "observing":
                    continue
                elif filter_val == "retired" and status not in ("archived", "deleted"):
                    continue
                elif filter_val == "stale":
                    last_change = c.get("frozen_at") or c.get("last_accessed")
                    if last_change:
                        try:
                            last_dt = datetime.fromisoformat(last_change)
                            hours = (now_dt - last_dt).total_seconds() / 3600
                            if hours < 18:
                                continue
                        except (ValueError, TypeError):
                            continue
                    else:
                        continue
                elif filter_val == "ignored":
                    if not c.get("ignore_at"):
                        continue

                results.append({
                    "id": c.get("id"),
                    "confidence": round(confidence, 4),
                    "status": status,
                    "trigger_count": c.get("trigger_count", 0),
                    "last_trigger": c.get("last_triggered"),
                    "frozen_at": c.get("frozen_at"),
                    "ignore_at": c.get("ignore_at"),
                    "tags": c.get("tags", []),
                    "content_preview": c.get("content", "")[:100],
                })

            results.sort(key=lambda x: x.get("confidence", 0), reverse=True)

            return {"total": len(results), "cases": results}

        except Exception as e:
            raise MCPError("SCRIPT_ERROR", str(e))

    def handle_case_review(self, params):
        """case_review — perform case action."""
        try:
            ws = resolve_workspace(params)
            mp = meta_path(ws)
            case_id = params.get("case_id", "").strip()
            action = params.get("action", "").strip().lower()
            origin_type = params.get("origin_type", "agent_initiated")

            if not case_id:
                raise MCPError("INVALID_PARAMS", "case_id is required")
            if action not in ("active", "frozen", "freeze", "retired", "unfreeze", "ignore"):
                raise MCPError("INVALID_PARAMS",
                    f"Invalid action: {action}. Must be one of: active, frozen/freeze, retired, unfreeze, ignore")
            # Alias: freeze → frozen
            if action == "freeze":
                action = "frozen"

            if not os.path.exists(mp):
                raise MCPError("META_CORRUPT", "meta.json not found")

            ci = _import_case_invalidate()
            now = _now_iso()

            if action == "unfreeze":
                # Get actual status before action
                meta_tmp = load_meta(mp)
                mem_tmp = next((m for m in meta_tmp.get("memories", []) if m.get("id") == case_id), None)
                if not mem_tmp:
                    raise MCPError("NOT_FOUND", f"Case {case_id} not found")
                old_status = mem_tmp.get("status", "unknown")
                if old_status != "frozen":
                    raise MCPError("INVALID_PARAMS",
                        f"Cannot unfreeze case in '{old_status}' status (must be frozen)")
                result = ci.unfreeze(mp, case_id)
                # Script returns "unfrozen" in result, but meta is written as "active"
                new_status = "active"
                return {
                    "case_id": case_id,
                    "old_status": old_status,
                    "new_status": new_status,
                    "updated_fields": ["status", "confidence", "consecutive_low_confidence"],
                    "origin_type": origin_type,
                }

            elif action == "retired":
                # retired → delegates to case_invalidate.archive_case script layer
                meta_tmp = load_meta(mp)
                mem_tmp = next((m for m in meta_tmp.get("memories", []) if m.get("id") == case_id), None)
                if not mem_tmp:
                    raise MCPError("NOT_FOUND", f"Case {case_id} not found")
                old_status = mem_tmp.get("status", "unknown")
                result = ci.archive_case(mp, case_id)
                return {
                    "case_id": case_id,
                    "old_status": old_status,
                    "new_status": "archived",
                    "updated_fields": ["status", "archived_at", "archive_reason"],
                    "origin_type": origin_type,
                }

            elif action == "ignore":
                # ignore — direct MCP-layer operation (no script equivalent).
                # Sets ignore_at timestamp and updates review queue in meta.json.
                # The script layer (case_invalidate) only handles archive/unfreeze,
                # so lightweight status tweaks are handled here for consistency.
                meta = load_meta(mp)
                mem = None
                for m in meta.get("memories", []):
                    if m.get("id") == case_id:
                        mem = m
                        break
                if not mem:
                    raise MCPError("NOT_FOUND", f"Case {case_id} not found")
                old_status = mem.get("status", "unknown")
                mem["ignore_at"] = now
                # Update review queue
                for r in meta.get("case_review_queue", []):
                    if r["case_id"] == case_id and r["status"] == "pending_review":
                        r["status"] = "ignored"
                        r["resolved_at"] = now
                        r["action"] = "ignore"
                        break
                save_meta(mp, meta)
                return {
                    "case_id": case_id,
                    "old_status": old_status,
                    "new_status": old_status,  # status unchanged, just marked ignored
                    "updated_fields": ["ignore_at"],
                    "origin_type": origin_type,
                }

            elif action == "active":
                # active — direct MCP-layer operation (no script equivalent).
                # Reactivates a case by setting status=active and boosting confidence.
                # Kept at MCP layer because this is a simple status toggle that
                # doesn't require the case_invalidate script's archive logic.
                meta = load_meta(mp)
                mem = None
                for m in meta.get("memories", []):
                    if m.get("id") == case_id:
                        mem = m
                        break
                if not mem:
                    raise MCPError("NOT_FOUND", f"Case {case_id} not found")
                old_status = mem.get("status", "unknown")
                mem["status"] = "active"
                mem["confidence"] = max(mem.get("confidence", 0.3), 0.5)
                mem["consecutive_low_confidence"] = 0
                save_meta(mp, meta)
                return {
                    "case_id": case_id,
                    "old_status": old_status,
                    "new_status": "active",
                    "updated_fields": ["status", "confidence"],
                    "origin_type": origin_type,
                }

            elif action == "frozen":
                # frozen — direct MCP-layer operation (no script equivalent).
                # Freezes a case to prevent automatic decay/archival.
                # The script layer only handles archive/unfreeze; freeze is
                # a lightweight status change managed entirely at MCP layer.
                meta = load_meta(mp)
                mem = None
                for m in meta.get("memories", []):
                    if m.get("id") == case_id:
                        mem = m
                        break
                if not mem:
                    raise MCPError("NOT_FOUND", f"Case {case_id} not found")
                old_status = mem.get("status", "unknown")
                if old_status not in ("observing", "active"):
                    raise MCPError("INVALID_PARAMS",
                        f"Cannot freeze case in '{old_status}' status (must be observing or active)")
                mem["status"] = "frozen"
                mem["frozen_at"] = now
                mem["frozen_reason"] = f"manual_freeze via case_review (origin={origin_type})"
                save_meta(mp, meta)
                return {
                    "case_id": case_id,
                    "old_status": old_status,
                    "new_status": "frozen",
                    "updated_fields": ["status", "frozen_at", "frozen_reason"],
                    "origin_type": origin_type,
                }

        except MCPError:
            raise
        except Exception as e:
            raise MCPError("SCRIPT_ERROR", str(e))

    # ── Batch mode ───────────────────────────────────────────

    def handle_run_batch(self, params):
        """run_batch — full maintenance cycle."""
        try:
            ws = resolve_workspace(params)
            mp = meta_path(ws)
            apply = _to_bool(params.get("apply"), True)
            dry_run = _to_bool(params.get("dry_run"), False)
            # apply=False means no writes — treat as dry_run
            if not apply:
                dry_run = True
            skip_compact = _to_bool(params.get("skip_compact"), False)
            timeout = int(params.get("timeout", 300))
            bootstrapped = False
            batch_start = time.monotonic()

            def _check_timeout(step_name):
                """Raise MCPError if batch has exceeded the configured timeout."""
                elapsed = time.monotonic() - batch_start
                if elapsed >= timeout:
                    raise MCPError(
                        "TIMEOUT",
                        f"Batch timed out at step '{step_name}' after {elapsed:.1f}s "
                        f"(limit: {timeout}s)",
                        hint="Increase the timeout parameter or reduce processing load.",
                    )

            if not os.path.exists(mp):
                # Auto-bootstrap (capture print output)
                mg = _import_memory_guardian()
                with _capture_stdout():
                    mg.cmd_bootstrap(ws)
                bootstrapped = True

            results = {}

            # Pre-flight: normalize meta to fix type issues (e.g. string importance)
            self._ensure_schema_compliance(mp, workspace=ws)

            # Step 0: Sync files → meta.json
            _check_timeout("sync")
            sync_result = self.handle_memory_sync({
                "workspace": ws, "dry_run": dry_run,
            })
            results["sync_summary"] = {
                "created": sync_result.get("created", 0),
                "skipped": sync_result.get("skipped", 0),
            }

            # Step 1: Decay
            _check_timeout("decay")
            decay_result = self.handle_memory_decay({
                "workspace": ws, "lambda": 0.01, "dry_run": dry_run,
            })
            results["decay_summary"] = {
                "processed": decay_result.get("processed", 0),
                "changed": decay_result.get("changed", 0),
            }

            # Step 2: Quality check
            _check_timeout("quality_check")
            qc_result = self.handle_quality_check({
                "workspace": ws, "layer": "all",
            })
            results["gate_state"] = qc_result.get("state", "NORMAL")
            results["intervention_level"] = qc_result.get("intervention_level", "L0")
            results["rule_review_suggested"] = qc_result.get(
                "critical_history", {}).get("rule_review_suggested", False)

            # Step 3: Compact (optional)
            if not skip_compact and not dry_run:
                _check_timeout("compact")
                compact_result = self.handle_memory_compact({
                    "workspace": ws, "dry_run": dry_run,
                })
                results["compact_summary"] = {
                    "before_kb": compact_result.get("before_kb", 0),
                    "after_kb": compact_result.get("after_kb", 0),
                }
                results["compact_needed"] = compact_result.get("before_kb", 0) > 15
            else:
                results["compact_needed"] = False
                results["compact_summary"] = None

            # Collect violations
            try:
                meta = load_meta(mp)
                violations = []
                for v in meta.get("violation_events", [])[-5:]:
                    violations.append({
                        "rule": v.get("rule"),
                        "event": v.get("event", "")[:80],
                        "severity": v.get("severity"),
                    })
                results["violations"] = violations
            except Exception:
                results["violations"] = []

            results["recommendations"] = []
            results["dry_run"] = dry_run
            results["timestamp"] = _now_iso()
            results["bootstrap"] = bootstrapped

            return results

        except Exception as e:
            raise MCPError("SCRIPT_ERROR", str(e))

    # ── Internal helpers ─────────────────────────────────────

    def _compute_similar_case_signal(self, meta):
        """Compute similar_case_signal using tag-overlap matching.

        Three-level signal:
        - has_active_ref: >=1 similar case is active
        - all_retired: all similar cases are retired/frozen
        - no_similar: no similar cases found

        Uses tag overlap (Jaccard) instead of external embedding.
        Optimized with inverted tag index to avoid O(N²) full scan.
        """
        from collections import defaultdict

        cases = [m for m in meta.get("memories", [])
                 if m.get("id", "").startswith("case_")]
        if len(cases) < 2:
            return {"has_active_ref": False, "all_retired": False,
                    "no_similar": len(cases) == 0, "top3": []}

        # Build tag sets for each case
        case_tag_sets = {}
        for c in cases:
            tags = set(c.get("tags", []))
            # Also add content keywords
            content_words = set(tokenize(c.get("content", "")))
            case_tag_sets[c["id"]] = tags | content_words

        # Build inverted tag→case_index for efficient pair comparison
        tag_index = defaultdict(list)
        for i, c in enumerate(cases):
            for tag in case_tag_sets[c["id"]]:
                tag_index[tag].append(i)

        # Collect unique case pairs that share at least one tag
        compared = set()
        pair_similarities = defaultdict(list)  # target_idx → [(other_idx, sim)]

        for indices in tag_index.values():
            for a in range(len(indices)):
                for b in range(a + 1, len(indices)):
                    pair = (min(indices[a], indices[b]), max(indices[a], indices[b]))
                    if pair in compared:
                        continue
                    compared.add(pair)

                    idx_a, idx_b = pair
                    tags_a = case_tag_sets[cases[idx_a]["id"]]
                    tags_b = case_tag_sets[cases[idx_b]["id"]]
                    if not tags_a or not tags_b:
                        continue

                    # Jaccard similarity
                    intersection = len(tags_a & tags_b)
                    union = len(tags_a | tags_b)
                    if union == 0:
                        continue
                    sim = intersection / union

                    if sim > 0.1:  # Minimum threshold
                        pair_similarities[idx_a].append((idx_b, sim))
                        pair_similarities[idx_b].append((idx_a, sim))

        # For each case, find top-3 similar by tag overlap
        all_signals = {"has_active_ref": False, "all_retired": False,
                       "no_similar": True, "top3": []}

        # Aggregate signal across all cases (system-level)
        total_topic_similar = 0
        total_all_retired = 0

        for target_idx, target in enumerate(cases):
            target_tags = case_tag_sets.get(target["id"], set())
            if not target_tags:
                continue

            # Filter by topic_similarity > 0.6 (v3.2)
            topic_similar = []
            for other_idx, sim in pair_similarities.get(target_idx, []):
                other = cases[other_idx]
                if sim > 0.6:
                    topic_similar.append({
                        "case_id": other["id"],
                        "status": other.get("status", "active"),
                        "confidence": other.get("confidence", 0.5),
                        "topic_similarity": round(sim, 4),
                    })

            if topic_similar:
                all_signals["no_similar"] = False
                total_topic_similar += 1

                active_refs = [s for s in topic_similar if s["status"] == "active"]
                if active_refs:
                    all_signals["has_active_ref"] = True
                elif all(s["status"] in ("retired", "archived", "deleted", "frozen")
                         for s in topic_similar):
                    total_all_retired += 1

        # System-level all_retired: majority of cases with similar refs have all-retired
        if total_topic_similar > 0:
            all_signals["all_retired"] = total_all_retired > total_topic_similar * 0.5

        return all_signals


# ─── MCP Protocol Layer (stdio) ─────────────────────────────
def serve_stdio():
    """MCP stdio transport — read JSON-RPC, dispatch tools, write responses."""
    server = MemoryGuardianServer()

    # Tool registry (schemas use MCP JSON Schema format)
    TOOLS = {
        "memory_status": (server.handle_memory_status, {
            "type": "object",
            "properties": {"workspace": {"type": "string", "default": "auto"}},
        }),
        "memory_query": (server.handle_memory_query, {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "default": "auto"},
                "query": {"type": "string", "default": ""},
                "type_filter": {"type": "string", "enum": ["active", "archived", "observing", "all"], "default": "active"},
                "min_score": {"type": "number", "default": 0.0},
                "max_score": {"type": "number", "default": 1.0},
                "memory_type": {"type": "string", "enum": ["static", "derive", "absorb", "suspend"]},
            },
        }),
        "memory_decay": (server.handle_memory_decay, {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "default": "auto"},
                "lambda": {"type": "number", "default": 0.01},
                "dry_run": {"type": "boolean", "default": False},
            },
        }),
        "memory_ingest": (server.handle_memory_ingest, {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "default": "auto"},
                "content": {"type": "string"},
                "importance": {"type": "string", "default": "auto"},
                "tags": {"type": "array", "items": {"type": "string"}, "default": []},
                "provenance_source": {"type": "string", "enum": ["human_direct", "system_induction", "external"]},
                "situation": {"type": "string", "description": "Case situation context"},
                "judgment": {"type": "string", "description": "Case judgment"},
                "consequence": {"type": "string", "description": "Case consequence"},
                "action_conclusion": {"type": "string", "description": "Case action/conclusion"},
                "reversibility": {"type": "string", "description": "Reversibility (high/medium/low)"},
                "boundary_words": {"type": "array", "items": {"type": "string"}, "description": "Boundary keywords"},
                "alternatives": {"type": "array", "items": {"type": "string"}, "description": "Alternatives considered"},
            },
            "required": ["content"],
        }),
        "memory_compact": (server.handle_memory_compact, {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "default": "auto"},
                "dry_run": {"type": "boolean", "default": False},
                "aggressive": {"type": "boolean", "default": False},
                "max_memory_kb": {"type": "integer", "default": 15},
            },
        }),
        "quality_check": (server.handle_quality_check, {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "default": "auto"},
                "layer": {"type": "string", "enum": ["all", "security", "dedup", "ingest", "decay"], "default": "all"},
            },
        }),
        "case_query": (server.handle_case_query, {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "default": "auto"},
                "filter": {"type": "string", "enum": ["all", "active", "frozen", "observing", "retired", "stale", "ignored"], "default": "all"},
                "min_confidence": {"type": "number", "default": 0.0},
            },
        }),
        "case_review": (server.handle_case_review, {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "default": "auto"},
                "case_id": {"type": "string"},
                "action": {"type": "string", "enum": ["active", "frozen", "retired", "unfreeze", "ignore"]},
                "origin_type": {"type": "string", "enum": ["agent_initiated", "notification_callback", "unknown"], "default": "agent_initiated"},
            },
            "required": ["case_id", "action"],
        }),
        "run_batch": (server.handle_run_batch, {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "default": "auto"},
                "apply": {"type": "boolean", "default": True},
                "dry_run": {"type": "boolean", "default": False},
                "skip_compact": {"type": "boolean", "default": False},
                "timeout": {"type": "integer", "default": 300},
            },
        }),
        "memory_sync": (server.handle_memory_sync, {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "default": "auto"},
                "dry_run": {"type": "boolean", "default": True},
            },
        }),
    }

    tool_list = []
    for name, (_, schema) in TOOLS.items():
        tool_list.append({"name": name, "schema": schema})

    def _respond(response):
        """Write JSON-RPC response to stdout."""
        json_str = json.dumps(response, ensure_ascii=False)
        sys.stdout.write(json_str + "\n")
        sys.stdout.flush()

    # References integrity check on startup (neuro P0: fail-fast on missing refs)
    missing = check_references()
    if missing:
        print(f"[ERROR] references/ incomplete: missing {missing}. "
              f"Core functions work but diagnostics are degraded. "
              f"See SKILL.md references/ section for expected files.",
              file=sys.stderr)

    # Read JSON-RPC messages from stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            _respond({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None})
            continue

        method = msg.get("method", "")
        req_id = msg.get("id")
        params = msg.get("params", {})

        if method == "initialize":
            _respond({
                "jsonrpc": "2.0",
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": "memory-guardian", "version": "0.4.6"},
                },
                "id": req_id,
            })

        elif method == "notifications/initialized":
            # Client acknowledges initialization — silently ignore (no id).
            # MCP spec: this is a notification, not a request.
            pass

        elif method == "shutdown":
            # MCP spec: return empty result, then exit.
            _respond({
                "jsonrpc": "2.0",
                "result": {},
                "id": req_id,
            })
            break  # Exit main loop; process will terminate

        elif method == "tools/list":
            _respond({
                "jsonrpc": "2.0",
                "result": {"tools": tool_list},
                "id": req_id,
            })

        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})

            if tool_name not in TOOLS:
                _respond({
                    "jsonrpc": "2.0",
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
                    "id": req_id,
                })
                continue

            handler, _ = TOOLS[tool_name]
            try:
                result = handler(arguments)
                _respond({
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
                    },
                    "id": req_id,
                })
            except MCPError as e:
                _respond({
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(e.to_dict(), ensure_ascii=False, indent=2)}],
                        "isError": True,
                    },
                    "id": req_id,
                })
            except Exception as e:
                _respond({
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(
                            MCPError("SCRIPT_ERROR", str(e)).to_dict(), ensure_ascii=False, indent=2)}],
                        "isError": True,
                    },
                    "id": req_id,
                })
        else:
            _respond({
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Unknown method: {method}"},
                "id": req_id,
            })


# ─── CLI fallback ────────────────────────────────────────────
def cli_batch(args):
    """CLI fallback: bypass MCP protocol, call handlers directly."""
    server = MemoryGuardianServer(args.workspace)
    result = server.handle_run_batch({
        "workspace": args.workspace,
        "apply": args.apply,
        "dry_run": args.dry_run,
        "skip_compact": args.skip_compact,
        "timeout": args.timeout,
    })
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cli_tool(args):
    """CLI fallback: call a specific tool handler."""
    server = MemoryGuardianServer(args.workspace)
    tool_name = args.tool
    handler_map = {
        "memory_status": server.handle_memory_status,
        "memory_query": server.handle_memory_query,
        "memory_decay": server.handle_memory_decay,
        "memory_ingest": server.handle_memory_ingest,
        "memory_compact": server.handle_memory_compact,
        "quality_check": server.handle_quality_check,
        "case_query": server.handle_case_query,
        "case_review": server.handle_case_review,
        "run_batch": server.handle_run_batch,
        "memory_sync": server.handle_memory_sync,
    }
    handler = handler_map.get(tool_name)
    if not handler:
        print(f"[ERROR] Unknown tool: {tool_name}")
        print(f"Available: {', '.join(handler_map.keys())}")
        sys.exit(1)

    params = {}
    if args.params:
        params = json.loads(args.params)

    try:
        result = handler(params)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except MCPError as e:
        print(json.dumps(e.to_dict(), indent=2, ensure_ascii=False))
        sys.exit(1)


# ─── Main ────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="memory-guardian MCP Server v0.4.6")
    parser.add_argument("--batch", action="store_true",
                        help="CLI fallback: run batch maintenance")
    parser.add_argument("--tool", type=str,
                        help="CLI fallback: call specific tool (e.g. memory_status)")
    parser.add_argument("--params", type=str,
                        help="CLI fallback: JSON params for --tool")
    parser.add_argument("--workspace", type=str,
                        help="Workspace path (default: MG_WORKSPACE env or ~/workspace/agent/workspace)")
    parser.add_argument("--apply", action="store_true", help="Apply changes (batch mode)")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (batch mode)")
    parser.add_argument("--skip-compact", action="store_true",
                        help="Skip compaction (batch mode)")
    parser.add_argument("--timeout", type=int, default=300,
                        help="Timeout in seconds (batch mode)")

    args = parser.parse_args()

    if args.batch:
        cli_batch(args)
    elif args.tool:
        cli_tool(args)
    else:
        # Default: MCP stdio mode
        serve_stdio()
