"""Module telemetry storage and reporting."""

import json
import os
import tempfile

from mg_utils import _now_iso, file_lock_acquire

ZERO_INPUT_BREAK_THRESHOLD = 3
MAX_TELEMETRY_FILE_SIZE = 1 * 1024 * 1024  # 1MB
MAX_TELEMETRY_RUN_RECORDS = 1000


def telemetry_path(workspace):
    return os.path.join(workspace, ".memory-guardian", "telemetry.json")


def _default_module_stats():
    return {
        "runs": 0,
        "hits": 0,
        "misses": 0,
        "input_total": 0,
        "output_total": 0,
        "last_input_count": 0,
        "last_output_count": 0,
        "zero_input_streak": 0,
        "max_zero_input_streak": 0,
        "pipeline_break_candidate": False,
        "last_run_at": None,
    }


def load_telemetry(workspace):
    path = telemetry_path(workspace)
    if not os.path.exists(path):
        return {"schema_version": "v0.4.2", "modules": {}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _trim_run_records(state):
    """Trim run_records if present and too many, keeping the newest entries."""
    records = state.get("run_records")
    if records and len(records) > MAX_TELEMETRY_RUN_RECORDS:
        state["run_records"] = records[-MAX_TELEMETRY_RUN_RECORDS:]


def save_telemetry(workspace, state):
    path = telemetry_path(workspace)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Bug 7: Rotate if file exceeds size limit
    if os.path.exists(path) and os.path.getsize(path) > MAX_TELEMETRY_FILE_SIZE:
        # Trim per-module run_records to keep file small
        modules = state.get("modules", {})
        for mod in modules.values():
            runs = mod.get("run_records")
            if runs and len(runs) > MAX_TELEMETRY_RUN_RECORDS:
                mod["run_records"] = runs[-MAX_TELEMETRY_RUN_RECORDS:]
        _trim_run_records(state)

    # Bug 6: Atomic write via temp file + rename
    dir_name = os.path.dirname(path)
    try:
        fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=True, indent=2)
        os.replace(tmp_path, path)
    except Exception:
        # Clean up temp file on failure
        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


def record_module_run(workspace, module_name, input_count=0, output_count=0, hit=None):
    """Record one module execution."""
    path = telemetry_path(workspace)
    # Ensure directory exists before acquiring lock
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with file_lock_acquire(path):
        state = load_telemetry(workspace)
        modules = state.setdefault("modules", {})
        module = modules.setdefault(module_name, _default_module_stats())

        module["runs"] += 1
        module["input_total"] += max(input_count, 0)
        module["output_total"] += max(output_count, 0)
        module["last_input_count"] = max(input_count, 0)
        module["last_output_count"] = max(output_count, 0)
        module["last_run_at"] = _now_iso()

        effective_hit = bool(hit) if hit is not None else input_count > 0
        if effective_hit:
            module["hits"] += 1
            module["zero_input_streak"] = 0
        else:
            module["misses"] += 1
            if input_count <= 0:
                module["zero_input_streak"] += 1
                module["max_zero_input_streak"] = max(
                    module["max_zero_input_streak"], module["zero_input_streak"]
                )
            else:
                module["zero_input_streak"] = 0

        module["pipeline_break_candidate"] = (
            module["zero_input_streak"] >= ZERO_INPUT_BREAK_THRESHOLD
        )
        save_telemetry(workspace, state)
    return module


def build_report(workspace):
    """Build a current telemetry report."""
    state = load_telemetry(workspace)
    modules = state.setdefault("modules", {})
    break_candidates = sorted(
        name for name, stats in modules.items() if stats.get("pipeline_break_candidate")
    )
    return {
        "schema_version": state.get("schema_version", "v0.4.2"),
        "generated_at": _now_iso(),
        "modules": modules,
        "break_candidates": break_candidates,
    }
