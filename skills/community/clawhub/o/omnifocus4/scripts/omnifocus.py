#!/usr/bin/env python3
"""
OmniFocus CLI — Omni Automation wrapper.

Usage:
    omnifocus.py <command> [args...]

All output is JSON to stdout. Errors print {"error": "..."} and exit 1.
"""

import json
import pathlib
import subprocess
import sys
from textwrap import dedent


# ---------------------------------------------------------------------------
# Write authorization
# ---------------------------------------------------------------------------

PREFS_DIR  = pathlib.Path.home() / ".omnifocus4"
PREFS_FILE = PREFS_DIR / "prefs.json"

WRITE_COMMANDS = frozenset({
    "add", "newproject", "newfolder", "newtag",
    "complete", "uncomplete", "delete", "rename",
    "note", "setnote", "defer", "due", "flag",
    "tag", "untag", "move", "repeat", "unrepeat",
})

_DEFAULT_PREFS = {"mode": "once", "approved": []}


def _load_prefs() -> dict:
    try:
        with open(PREFS_FILE) as f:
            data = json.load(f)
    except FileNotFoundError:
        return dict(_DEFAULT_PREFS)
    except (json.JSONDecodeError, OSError):
        return dict(_DEFAULT_PREFS)
    mode = data.get("mode", "once")
    if mode not in ("yolo", "once", "every"):
        mode = "once"
    approved = data.get("approved", [])
    if not isinstance(approved, list):
        approved = []
    return {"mode": mode, "approved": [str(x) for x in approved]}


def _save_prefs(prefs: dict) -> None:
    PREFS_DIR.mkdir(parents=True, exist_ok=True)
    with open(PREFS_FILE, "w") as f:
        json.dump(prefs, f, indent=2)


def _auth_required(cmd: str, mode: str) -> None:
    if mode == "once":
        how = f"omnifocus.py prefs approve {cmd}"
        msg = f"Command '{cmd}' requires one-time approval. Run: {how}"
    else:
        how = f"Re-run with --authorized flag"
        msg = f"Command '{cmd}' requires authorization. {how}"
    print(json.dumps({
        "auth_required": True,
        "cmd": cmd,
        "mode": mode,
        "message": msg,
        "how_to_proceed": how,
    }))
    sys.exit(2)


def _require_auth(cmd: str, authorized: bool) -> None:
    """Gate every write command. Exits with code 2 if authorization is needed."""
    prefs = _load_prefs()
    mode  = prefs["mode"]
    if mode == "yolo":
        return
    if mode == "once":
        if cmd in prefs["approved"]:
            return
        _auth_required(cmd, mode)
    if mode == "every":
        if authorized:
            return
        _auth_required(cmd, mode)


# ---------------------------------------------------------------------------
# osascript bridge
# ---------------------------------------------------------------------------

OSASCRIPT_TIMEOUT = 30  # seconds; raises RuntimeError on timeout


def run_osascript(script: str) -> str:
    """Run an AppleScript string and return stdout. Raises RuntimeError on failure."""
    try:
        proc = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            check=False,
            timeout=OSASCRIPT_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(
            f"OmniFocus did not respond within {OSASCRIPT_TIMEOUT}s. "
            "Check for a macOS automation permissions dialog, or that OmniFocus is running."
        )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip())
    return (proc.stdout or "").strip()


def run_omni_js(js_expr: str):
    """
    Execute Omni Automation JS inside OmniFocus via evaluate javascript.
    The JS must end with a return JSON.stringify(...) expression.
    Returns a parsed Python object.
    """
    # Embed the JS as an AppleScript string literal to avoid shell quoting issues
    script = dedent(f"""\
        try
          tell application "OmniFocus"
            tell default document
              set js to {json.dumps(js_expr)}
              return evaluate javascript js
            end tell
          end tell
        on error errMsg number errNum
          return "__ERROR__|" & errNum & "|" & errMsg
        end try
    """)
    raw = run_osascript(script)
    if raw.startswith("__ERROR__|"):
        raise RuntimeError(raw)
    return json.loads(raw)


# ---------------------------------------------------------------------------
# Omni Automation JS preamble — injected into every call
# ---------------------------------------------------------------------------

_PREAMBLE = r"""
  // Array.isArray() returns false for OmniJS collection types.
  const asArray = v => {
    if (!v) return [];
    if (Array.isArray(v)) return v;
    try { return Array.from(v); } catch (_) { return [v]; }
  };

  // Swallow errors from property access on live objects.
  const safe = (fn, fallback = null) => { try { return fn(); } catch (_) { return fallback; } };

  // Use filter() not byName(): byName() returns an ObjectSpecifier proxy
  // whose child collections (.folders, .projects) fail to enumerate.
  const findByName = (col, name) => col.filter(x => x.name === name)[0] || null;

  // Find objects by their stable primaryKey ID.
  const findById   = (col, id)   => col.filter(x => safe(() => x.id.primaryKey) === id)[0] || null;

  // Normalise a Date to ISO YYYY-MM-DD, or null.
  const isoDate = d => {
    if (!d) return null;
    const iso = d.toISOString();          // always UTC
    return iso.split('T')[0];
  };

  // ---- task helpers ----
  const taskProject   = t => safe(() => t.containingProject ? t.containingProject.name : null);
  const taskFolder    = t => safe(() =>
    t.containingProject && t.containingProject.folder
      ? t.containingProject.folder.name : null);
  const taskDue       = t => isoDate(safe(() => t.dueDate));
  const taskEffDue    = t => isoDate(safe(() => t.effectiveDueDate));
  const taskDefer     = t => isoDate(safe(() => t.deferDate));
  const taskNote      = t => safe(() => t.note || null);
  const taskTags      = t => safe(() => asArray(t.tags).map(tg => tg.name), []);
  const isCompleted   = t => safe(() => !!t.completed, false);
  const isFlagged     = t => safe(() => !!t.flagged,   false);
  const isAvailable   = t => safe(() => !!t.available, false);
  const taskRepeat    = t => safe(() => {
    const r = t.repetitionRule;
    if (!r) return null;
    return { method: String(r.method), recurrence: r.recurrence || null };
  });

  // ---- availability: fast approximation for bulk scans ----
  // task.available is slow (full chain check) and unreliable via evaluate javascript.
  // This proxy is cheaper: not completed + not deferred to the future.
  // It misses sequential blocking and on-hold projects but is fast and correct for
  // most practical queries. Use isAvailable only when full accuracy is needed.
  const isAvailableApprox = t => {
    if (safe(() => !!t.completed, true)) return false;
    const d = safe(() => t.deferDate);
    return !d || d <= new Date();
  };

  // ---- slim records for list commands ----
  // Full records (taskRecord / projectRecord) are for single-item detail (info, write responses).
  // List commands use slim records: fewer property accesses = faster bulk iteration.
  const listTaskRecord = t => ({
    id:      safe(() => t.id.primaryKey, null),
    name:    safe(() => t.name, ""),
    project: taskProject(t),
    folder:  taskFolder(t),
    due:     taskEffDue(t),
    flagged: isFlagged(t),
    tags:    taskTags(t),
  });

  const listProjectRecord = p => ({
    id:     safe(() => p.id.primaryKey, null),
    name:   safe(() => p.name, ""),
    folder: safe(() => p.folder ? p.folder.name : null),
    status: projectStatus(p),
    due:    isoDate(safe(() => p.dueDate)),
  });

  // ---- early-termination filter ----
  // Stops as soon as limit items pass the predicate.
  // Note: flattenedTasks triggers a full database scan on first access regardless
  // of iteration strategy - OmniJS loads all task objects upfront (~5-7 s for
  // large databases). Early termination saves per-task processing time only.
  const earlyFilter = (col, pred, limit) => {
    const arr = asArray(col);
    const results = [];
    for (let i = 0; i < arr.length; i++) {
      if (results.length >= limit) break;
      if (pred(arr[i])) results.push(arr[i]);
    }
    return results;
  };

  const taskRecord = t => ({
    id:               safe(() => t.id.primaryKey, null),
    name:             safe(() => t.name, ""),
    note:             taskNote(t),
    flagged:          isFlagged(t),
    completed:        isCompleted(t),
    available:        isAvailable(t),
    deferDate:        taskDefer(t),
    dueDate:          taskDue(t),
    effectiveDueDate: taskEffDue(t),
    completionDate:   isoDate(safe(() => t.completionDate)),
    estimatedMinutes: safe(() => t.estimatedMinutes || null),
    project:          taskProject(t),
    folder:           taskFolder(t),
    tags:             taskTags(t),
    repeat:           taskRepeat(t),
  });

  // ---- project helpers ----
  const projectStatus = p => safe(() => {
    if (!p.status) return null;
    const raw = String(p.status);
    const m   = raw.match(/Project\.Status:\s*(.+?)\]/i);
    return m ? m[1].toLowerCase() : raw.toLowerCase();
  });

  const projectRecord = p => ({
    id:                safe(() => p.id.primaryKey, null),
    name:              safe(() => p.name, ""),
    folder:            safe(() => p.folder ? p.folder.name : null),
    status:            projectStatus(p),
    flagged:           safe(() => !!p.flagged, false),
    completed:         safe(() => !!p.completed, false),
    due:               isoDate(safe(() => p.dueDate)),
    defer:             isoDate(safe(() => p.deferDate)),
    note:              safe(() => p.note || null),
    taskCount:         safe(() => asArray(p.flattenedTasks).length, 0),
    availableTaskCount:safe(() => asArray(p.availableTasks).length, 0),
  });
"""


def omni_js(body: str) -> str:
    """Wrap body with the preamble inside an IIFE."""
    return f"(function(){{\n{_PREAMBLE}\n{body}\n}})()"


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def _out(data) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _err(msg: str) -> None:
    print(json.dumps({"error": msg}))
    sys.exit(1)


def _ok(**kwargs) -> None:
    _out({"success": True, **kwargs})


# ---------------------------------------------------------------------------
# READ commands
# ---------------------------------------------------------------------------

def cmd_inbox() -> None:
    result = run_omni_js(omni_js("""
      const tasks = asArray(document.inboxTasks);
      return JSON.stringify(tasks.map(taskRecord));
    """))
    _out(result)


def cmd_folders() -> None:
    result = run_omni_js(omni_js("""
      const items = asArray(flattenedFolders).map(f => ({
        id:           safe(() => f.id.primaryKey, null),
        name:         safe(() => f.name, ""),
        parent:       safe(() => f.parent ? f.parent.name : null),
        projectCount: safe(() => asArray(f.projects).length, 0),
        folderCount:  safe(() => asArray(f.folders).length, 0),
      }));
      return JSON.stringify(items);
    """))
    _out(result)


def cmd_projects(folder_name: str = None, active_only: bool = True, limit: int = 100) -> None:
    status_filter = "projectStatus(p) === 'active'" if active_only else "true"
    if folder_name:
        target = json.dumps(folder_name)
        result = run_omni_js(omni_js(f"""
          const folder = findByName(flattenedFolders, {target});
          if (!folder) return JSON.stringify({{error: "Folder not found: " + {target}}});
          const items = earlyFilter(folder.projects, p => {status_filter}, {limit})
            .map(listProjectRecord);
          return JSON.stringify(items);
        """))
    else:
        result = run_omni_js(omni_js(f"""
          const items = earlyFilter(flattenedProjects, p => {status_filter}, {limit})
            .map(listProjectRecord);
          return JSON.stringify(items);
        """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_tasks(project_name: str) -> None:
    target = json.dumps(project_name)
    result = run_omni_js(omni_js(f"""
      const p = findByName(flattenedProjects, {target});
      if (!p) return JSON.stringify({{error: "Project not found: " + {target}}});
      return JSON.stringify(asArray(p.flattenedTasks).map(taskRecord));
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_tags(active_only: bool = True) -> None:
    activity_filter = "safe(() => asArray(tag.availableTasks).length > 0, false)" if active_only else "true"
    result = run_omni_js(omni_js(f"""
      const items = asArray(flattenedTags)
        .filter(tag => {activity_filter})
        .map(tag => ({{
          id:                 safe(() => tag.id.primaryKey, null),
          name:               safe(() => tag.name, ""),
          parent:             safe(() => tag.parent ? tag.parent.name : null),
          childCount:         safe(() => asArray(tag.children).length, 0),
          taskCount:          safe(() => asArray(tag.tasks).length, 0),
          availableTaskCount: safe(() => asArray(tag.availableTasks).length, 0),
        }}));
      return JSON.stringify(items);
    """))
    _out(result)


def cmd_today(limit: int = 50) -> None:
    result = run_omni_js(omni_js(f"""
      const todayEnd = new Date();
      todayEnd.setHours(23, 59, 59, 999);
      const items = earlyFilter(
        flattenedTasks,
        t => !isCompleted(t) && safe(() => {{ const d = t.effectiveDueDate; return !!d && d <= todayEnd; }}, false),
        {limit}
      ).map(listTaskRecord);
      return JSON.stringify(items);
    """))
    _out(result)


def cmd_flagged(limit: int = 50) -> None:
    result = run_omni_js(omni_js(f"""
      const items = earlyFilter(
        flattenedTasks,
        t => !isCompleted(t) && isFlagged(t),
        {limit}
      ).map(listTaskRecord);
      return JSON.stringify(items);
    """))
    _out(result)


def cmd_search(query: str, limit: int = 20) -> None:
    target = json.dumps(query.lower())
    result = run_omni_js(omni_js(f"""
      const q = {target};
      const items = earlyFilter(
        flattenedTasks,
        t => !isCompleted(t) && (
          safe(() => t.name.toLowerCase().includes(q), false) ||
          safe(() => (t.note || '').toLowerCase().includes(q), false)
        ),
        {limit}
      ).map(listTaskRecord);
      return JSON.stringify(items);
    """))
    _out(result)


def cmd_info(task_id: str) -> None:
    target = json.dumps(task_id)
    result = run_omni_js(omni_js(f"""
      const task = findById(flattenedTasks, {target})
                || findById(asArray(document.inboxTasks), {target});
      if (!task) return JSON.stringify({{error: "Task not found: " + {target}}});
      return JSON.stringify(taskRecord(task));
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


# ---------------------------------------------------------------------------
# CREATE commands
# ---------------------------------------------------------------------------

def cmd_add(name: str, project_name: str = None) -> None:
    n_js = json.dumps(name)
    if project_name:
        p_js = json.dumps(project_name)
        result = run_omni_js(omni_js(f"""
          const p = findByName(flattenedProjects, {p_js});
          if (!p) return JSON.stringify({{error: "Project not found: " + {p_js}}});
          const task = new Task({n_js}, p);
          return JSON.stringify({{success: true, task: taskRecord(task)}});
        """))
    else:
        result = run_omni_js(omni_js(f"""
          const task = new Task({n_js}, document.inbox);
          return JSON.stringify({{success: true, task: taskRecord(task)}});
        """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_newproject(name: str, folder_name: str = None) -> None:
    n_js = json.dumps(name)
    if folder_name:
        f_js = json.dumps(folder_name)
        result = run_omni_js(omni_js(f"""
          const folder = findByName(flattenedFolders, {f_js});
          if (!folder) return JSON.stringify({{error: "Folder not found: " + {f_js}}});
          const p = new Project({n_js}, folder);
          return JSON.stringify({{success: true, project: projectRecord(p)}});
        """))
    else:
        result = run_omni_js(omni_js(f"""
          const p = new Project({n_js}, document);
          return JSON.stringify({{success: true, project: projectRecord(p)}});
        """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_newfolder(name: str) -> None:
    n_js = json.dumps(name)
    result = run_omni_js(omni_js(f"""
      const folder = new Folder({n_js}, document);
      return JSON.stringify({{
        success: true,
        folder: {{
          id:   safe(() => folder.id.primaryKey, null),
          name: folder.name,
        }}
      }});
    """))
    _out(result)


def cmd_newtag(name: str) -> None:
    n_js = json.dumps(name)
    result = run_omni_js(omni_js(f"""
      const existing = findByName(flattenedTags, {n_js});
      if (existing) return JSON.stringify({{
        success: true,
        tag: {{id: safe(() => existing.id.primaryKey, null), name: existing.name}},
        existed: true,
      }});
      const tag = new Tag({n_js});
      return JSON.stringify({{
        success: true,
        tag: {{id: safe(() => tag.id.primaryKey, null), name: tag.name}},
        created: true,
      }});
    """))
    _out(result)


# ---------------------------------------------------------------------------
# MODIFY commands
# ---------------------------------------------------------------------------

def _find_task_js(task_id: str) -> str:
    """JS snippet that resolves a task by ID or returns an error object."""
    t_js = json.dumps(task_id)
    return f"""
      const task = findById(flattenedTasks, {t_js})
                || findById(asArray(document.inboxTasks), {t_js});
      if (!task) return JSON.stringify({{error: "Task not found: " + {t_js}}});
    """


def cmd_complete(task_id: str) -> None:
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      task.markComplete();
      return JSON.stringify({{success: true, task: taskRecord(task)}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_uncomplete(task_id: str) -> None:
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      task.markIncomplete();
      return JSON.stringify({{success: true, task: taskRecord(task)}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_delete(task_id: str) -> None:
    t_js = json.dumps(task_id)
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      const name = task.name;
      deleteObject(task);
      return JSON.stringify({{success: true, deleted: {{id: {t_js}, name: name}}}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_rename(task_id: str, new_name: str) -> None:
    n_js = json.dumps(new_name)
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      task.name = {n_js};
      return JSON.stringify({{success: true, task: taskRecord(task)}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_note(task_id: str, text: str) -> None:
    t_js = json.dumps(text)
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      task.note = task.note ? task.note + "\\n" + {t_js} : {t_js};
      return JSON.stringify({{success: true, task: taskRecord(task)}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_setnote(task_id: str, text: str) -> None:
    t_js = json.dumps(text)
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      task.note = {t_js};
      return JSON.stringify({{success: true, task: taskRecord(task)}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_defer(task_id: str, date_str: str) -> None:
    d_js = json.dumps(date_str)
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      const d = new Date({d_js});
      if (isNaN(d.getTime())) return JSON.stringify({{error: "Invalid date: " + {d_js}}});
      task.deferDate = d;
      return JSON.stringify({{success: true, task: taskRecord(task)}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_due(task_id: str, date_str: str) -> None:
    d_js = json.dumps(date_str)
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      const d = new Date({d_js});
      if (isNaN(d.getTime())) return JSON.stringify({{error: "Invalid date: " + {d_js}}});
      task.dueDate = d;
      return JSON.stringify({{success: true, task: taskRecord(task)}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_flag(task_id: str, value: bool = True) -> None:
    v_js = "true" if value else "false"
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      task.flagged = {v_js};
      return JSON.stringify({{success: true, task: taskRecord(task)}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_tag(task_id: str, tag_name: str) -> None:
    tg_js = json.dumps(tag_name)
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      let tag = findByName(flattenedTags, {tg_js});
      if (!tag) tag = new Tag({tg_js});
      task.addTag(tag);
      return JSON.stringify({{success: true, task: taskRecord(task)}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_untag(task_id: str, tag_name: str) -> None:
    tg_js = json.dumps(tag_name)
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      const tag = findByName(flattenedTags, {tg_js});
      if (!tag) return JSON.stringify({{error: "Tag not found: " + {tg_js}}});
      task.removeTag(tag);
      return JSON.stringify({{success: true, task: taskRecord(task)}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_move(task_id: str, project_name: str) -> None:
    p_js = json.dumps(project_name)
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      const project = findByName(flattenedProjects, {p_js});
      if (!project) return JSON.stringify({{error: "Project not found: " + {p_js}}});
      task.assignedContainer = project;
      return JSON.stringify({{success: true, task: taskRecord(task)}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


# ---------------------------------------------------------------------------
# REPEAT commands
# ---------------------------------------------------------------------------

_REPEAT_METHOD_MAP = {
    "fixed":                  "Task.RepetitionMethod.Fixed",
    "due-after-completion":   "Task.RepetitionMethod.DueAfterCompletion",
    "defer-after-completion": "Task.RepetitionMethod.DeferAfterCompletion",
}

_FREQ_MAP = {
    "days": "DAILY", "day": "DAILY",
    "weeks": "WEEKLY", "week": "WEEKLY",
    "months": "MONTHLY", "month": "MONTHLY",
    "years": "YEARLY", "year": "YEARLY",
}


def cmd_repeat(task_id: str, method: str, interval: int, unit: str) -> None:
    js_method = _REPEAT_METHOD_MAP.get(method)
    if not js_method:
        _err(f"Invalid method: {method}. Use: fixed, due-after-completion, defer-after-completion")
    freq = _FREQ_MAP.get(unit.lower())
    if not freq:
        _err(f"Invalid unit: {unit}. Use: days, weeks, months, years")
    rrule = f"FREQ={freq};INTERVAL={interval}"
    r_js = json.dumps(rrule)
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      task.repetitionRule = new Task.RepetitionRule({js_method}, {r_js});
      return JSON.stringify({{success: true, task: taskRecord(task)}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


def cmd_unrepeat(task_id: str) -> None:
    result = run_omni_js(omni_js(f"""
      {_find_task_js(task_id)}
      task.repetitionRule = null;
      return JSON.stringify({{success: true, task: taskRecord(task)}});
    """))
    if isinstance(result, dict) and "error" in result:
        _err(result["error"])
    _out(result)


# ---------------------------------------------------------------------------
# NEW READ commands (from of-read, improved)
# ---------------------------------------------------------------------------

def cmd_summary() -> None:
    # Iterate via projects + inbox rather than document.flattenedTasks.
    # document.flattenedTasks materialises ~3000 objects in one shot (~8 s);
    # iterating project.tasks one project at a time is ~4x faster.
    result = run_omni_js(omni_js("""
      const projects  = asArray(flattenedProjects);
      const inboxList = asArray(document.inboxTasks);
      const today     = new Date(); today.setHours(23,59,59,999);
      const col = flattenedTasks;
      const n   = safe(() => col.length, 0);
      let flagged = 0, due = 0, available = 0, completed = 0;
      for (let i = 0; i < n; i++) {
        const t = col[i];
        if (!t) continue;
        if (isFlagged(t)) flagged++;
        if (isCompleted(t)) { completed++; }
        else {
          if (isAvailableApprox(t)) available++;
          const d = safe(() => t.effectiveDueDate);
          if (d && d <= today) due++;
        }
      }
      return JSON.stringify({
        projects:  projects.length,
        tasks:     n,
        flagged,
        due,
        available,
        completed,
        inbox:     inboxList.length,
      });
    """))
    _out(result)


def cmd_project_tree(project_name: str, limit: int = 300) -> None:
    target = json.dumps(project_name)
    result = run_omni_js(omni_js(f"""
      const p = findByName(flattenedProjects, {target});
      if (!p) return JSON.stringify({{found: false, name: {target}}});
      let count = 0;
      const walk = (tasks, depth) => asArray(tasks).flatMap(t => {{
        if (count >= {limit}) return [];
        count++;
        const row = {{type: "task", depth, ...taskRecord(t)}};
        const children = count < {limit} ? walk(t.tasks, depth + 1) : [];
        return [row, ...children];
      }});
      const items = walk(p.tasks, 0);
      return JSON.stringify({{
        found:   true,
        project: projectRecord(p),
        count:   items.length,
        items,
      }});
    """))
    if isinstance(result, dict) and result.get("found") is False:
        _err(f"Project not found: {project_name}")
    _out(result)


def cmd_project_search(term: str, limit: int = 20) -> None:
    target = json.dumps(term.lower())
    result = run_omni_js(omni_js(f"""
      const q = {target};
      const items = asArray(flattenedProjects)
        .filter(p => safe(() => p.name.toLowerCase().includes(q), false))
        .slice(0, {limit})
        .map(projectRecord);
      return JSON.stringify({{count: items.length, items}});
    """))
    _out(result)


def cmd_folder_detail(folder_name: str, limit: int = 50) -> None:
    target = json.dumps(folder_name)
    result = run_omni_js(omni_js(f"""
      const folder = findByName(flattenedFolders, {target});
      if (!folder) return JSON.stringify({{found: false, name: {target}}});
      const childFolders = asArray(folder.folders).map(f => ({{
        type:         "folder",
        id:           safe(() => f.id.primaryKey, null),
        name:         safe(() => f.name, ""),
        folderCount:  safe(() => asArray(f.folders).length, 0),
        projectCount: safe(() => asArray(f.projects).length, 0),
      }}));
      const childProjects = asArray(folder.projects).map(p => ({{
        type: "project",
        ...projectRecord(p),
      }}));
      const items = [...childFolders, ...childProjects].slice(0, {limit});
      return JSON.stringify({{
        found:        true,
        folder:       {{id: safe(() => folder.id.primaryKey, null), name: folder.name}},
        folderCount:  childFolders.length,
        projectCount: childProjects.length,
        count:        items.length,
        items,
      }});
    """))
    if isinstance(result, dict) and result.get("found") is False:
        _err(f"Folder not found: {folder_name}")
    _out(result)


def cmd_root(limit: int = 50) -> None:
    result = run_omni_js(omni_js(f"""
      const folders = asArray(flattenedFolders)
        .filter(f => !f.parent)
        .map(f => ({{
          type:         "folder",
          id:           safe(() => f.id.primaryKey, null),
          name:         f.name,
          folderCount:  safe(() => asArray(f.folders).length,  0),
          projectCount: safe(() => asArray(f.projects).length, 0),
        }}));
      const rootProjects = asArray(flattenedProjects)
        .filter(p => !safe(() => p.folder))
        .map(p => ({{type: "project", ...projectRecord(p)}}));
      const items = [...folders, ...rootProjects].slice(0, {limit});
      return JSON.stringify({{count: items.length, items}});
    """))
    _out(result)


def cmd_tag_summary(tag_name: str, limit: int = 200) -> None:
    # Incomplete tasks only, slim records. Full taskRecord with notes
    # blew past token limits for large tags (92k+ chars for "MSIA Day").
    target = json.dumps(tag_name)
    result = run_omni_js(omni_js(f"""
      const tag = findByName(flattenedTags, {target});
      if (!tag) return JSON.stringify({{found: false, name: {target}}});
      const all = asArray(tag.tasks).filter(t => !isCompleted(t));
      const tasks = all.slice(0, {limit}).map(listTaskRecord);
      const byFolder  = {{}};
      const byProject = {{}};
      for (const t of tasks) {{
        const f = t.folder  || "(no folder)";
        const p = t.project || "(no project)";
        byFolder[f]  = (byFolder[f]  || 0) + 1;
        const key = f + " :: " + p;
        byProject[key] = (byProject[key] || 0) + 1;
      }}
      return JSON.stringify({{
        found: true,
        tag:   {{id: safe(() => tag.id.primaryKey, null), name: tag.name}},
        totalIncomplete: all.length,
        returned: tasks.length,
        truncated: all.length > tasks.length,
        byFolder,
        byProject,
        items: tasks,
      }});
    """))
    if isinstance(result, dict) and result.get("found") is False:
        _err(f"Tag not found: {tag_name}")
    _out(result)


def cmd_tag_family(tag_name: str, limit: int = 2000) -> None:
    target = json.dumps(tag_name)
    result = run_omni_js(omni_js(f"""
      const root = findByName(flattenedTags, {target});
      if (!root) return JSON.stringify({{found: false, name: {target}}});
      const gather = tag => [tag, ...asArray(tag.children).flatMap(gather)];
      const family  = gather(root);
      const tagNames       = family.map(t => t.name);
      const byTag          = Object.fromEntries(family.map(t => [t.name, asArray(t.tasks).length]));
      const availableByTag = Object.fromEntries(family.map(t => [t.name, asArray(t.availableTasks).length]));
      const seen  = new Set();
      const tasks = [];
      for (const tag of family) {{
        for (const t of asArray(tag.tasks)) {{
          const id = safe(() => t.id.primaryKey, null);
          if (!id || seen.has(id)) continue;
          seen.add(id);
          tasks.push(taskRecord(t));
          if (tasks.length >= {limit}) break;
        }}
        if (tasks.length >= {limit}) break;
      }}
      return JSON.stringify({{
        found:        true,
        family:       root.name,
        matchingTags: tagNames,
        byTag,
        availableByTag,
        totalTasks:   tasks.length,
        items:        tasks,
      }});
    """))
    if isinstance(result, dict) and result.get("found") is False:
        _err(f"Tag not found: {tag_name}")
    _out(result)


def cmd_available(limit: int = 50) -> None:
    # Iterate per-project direct tasks with early exit across projects.
    # flattenedTasks triggers a full database scan (~6-12 s) even for limit=5.
    # p.tasks accesses one project at a time; we exit as soon as limit is reached.
    # Tradeoff: misses subtasks and tasks in dropped/completed projects — acceptable
    # for "what can I work on now" queries which are always in active projects.
    result = run_omni_js(omni_js(f"""
      const projects = flattenedProjects;
      const np = projects.length;
      const items = [];
      for (let pi = 0; pi < np && items.length < {limit}; pi++) {{
        const pts = projects[pi].tasks;
        const nt  = safe(() => pts.length, 0);
        for (let ti = 0; ti < nt && items.length < {limit}; ti++) {{
          const t = pts[ti];
          if (t && isAvailableApprox(t)) items.push(listTaskRecord(t));
        }}
      }}
      return JSON.stringify({{count: items.length, items}});
    """))
    _out(result)


def cmd_review(limit: int = 50, active_only: bool = True) -> None:
    status_filter = "projectStatus(p) === 'active'" if active_only else "true"
    result = run_omni_js(omni_js(f"""
      const items = asArray(flattenedProjects)
        .filter(p => {status_filter})
        .slice(0, {limit})
        .map(projectRecord);
      return JSON.stringify({{count: items.length, items}});
    """))
    _out(result)


# ---------------------------------------------------------------------------
# Prefs management
# ---------------------------------------------------------------------------

def cmd_prefs(args: list) -> None:
    sub = args[0] if args else "show"

    if sub == "show":
        _out(_load_prefs())

    elif sub == "set":
        if len(args) < 2:
            _err("Usage: prefs set <yolo|once|every>")
        mode = args[1]
        if mode not in ("yolo", "once", "every"):
            _err(f"Invalid mode: {mode}. Use: yolo, once, every")
        prefs = _load_prefs()
        prefs["mode"] = mode
        _save_prefs(prefs)
        _ok(mode=mode)

    elif sub == "approve":
        if len(args) < 2:
            _err("Usage: prefs approve <command>")
        target = args[1]
        if target not in WRITE_COMMANDS:
            _err(f"Not a write command: {target}")
        prefs = _load_prefs()
        if target not in prefs["approved"]:
            prefs["approved"].append(target)
            _save_prefs(prefs)
        _ok(approved=prefs["approved"])

    elif sub == "revoke":
        if len(args) < 2:
            _err("Usage: prefs revoke <command>")
        target = args[1]
        prefs = _load_prefs()
        prefs["approved"] = [x for x in prefs["approved"] if x != target]
        _save_prefs(prefs)
        _ok(approved=prefs["approved"])

    elif sub == "reset":
        _save_prefs(dict(_DEFAULT_PREFS))
        _ok(reset=True)

    else:
        _err(f"Unknown prefs subcommand: {sub}. Use: show, set, approve, revoke, reset")


# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------

_HELP = {
    "commands": {
        "inbox":          "List inbox tasks",
        "folders":        "List all folders",
        "projects":       "List active projects [folder] [--all]",
        "tasks":          "List tasks in project <project>",
        "tags":           "List tags with available tasks [--all]",
        "today":          "Tasks due today or overdue",
        "flagged":        "Flagged incomplete tasks",
        "search":         "Search tasks by name or note <query>",
        "info":           "Full task details <taskId>",
        "add":            "Add task <name> [project]",
        "newproject":     "Create project <name> [folder]",
        "newfolder":      "Create folder <name>",
        "newtag":         "Create or get tag <name>",
        "complete":       "Mark complete <taskId>",
        "uncomplete":     "Mark incomplete <taskId>",
        "delete":         "Permanently delete <taskId>",
        "rename":         "Rename task <taskId> <name>",
        "note":           "Append to note <taskId> <text>",
        "setnote":        "Replace note <taskId> <text>",
        "defer":          "Set defer date <taskId> <date>",
        "due":            "Set due date <taskId> <date>",
        "flag":           "Set flag <taskId> [true|false]",
        "tag":            "Add tag <taskId> <tag>",
        "untag":          "Remove tag <taskId> <tag>",
        "move":           "Move to project <taskId> <project>",
        "repeat":         "Set repeat <taskId> <method> <interval> <unit>",
        "unrepeat":       "Remove repeat <taskId>",
        "summary":        "Database counts overview",
        "project-tree":   "Subtask tree for project <name> [limit]",
        "project-search": "Find projects by partial name <term> [limit]",
        "folder":         "Detail a folder <name> [limit]",
        "root":           "Top-level folders and unfiled projects [limit]",
        "tag-summary":    "Tasks for tag grouped by project <name> [limit]",
        "tag-family":     "Tasks across tag hierarchy <name> [limit]",
        "available":      "All available (actionable) tasks [limit]",
        "review":         "Active projects with task counts [limit] [--all]",
        "prefs":          "Write auth: prefs [show|set <mode>|approve <cmd>|revoke <cmd>|reset]",
    }
}


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

def dispatch(argv: list) -> None:
    # Strip --authorized before any arg parsing; it may appear anywhere.
    authorized = "--authorized" in argv
    argv = [a for a in argv if a != "--authorized"]

    if not argv:
        _out(_HELP)
        return

    cmd  = argv[0]
    args = argv[1:]

    # Auth guard — outside try/except so exit(2) is never swallowed as an error.
    if cmd in WRITE_COMMANDS:
        _require_auth(cmd, authorized)

    try:
        if cmd == "inbox":
            cmd_inbox()
        elif cmd == "folders":
            cmd_folders()
        elif cmd == "projects":
            all_items = "--all" in args
            non_flag = [a for a in args if not a.startswith("-")]
            folder = non_flag[0] if non_flag and not non_flag[0].isdigit() else None
            limit = int(non_flag[-1]) if non_flag and non_flag[-1].isdigit() else 100
            cmd_projects(folder, active_only=not all_items, limit=limit)
        elif cmd == "tasks":
            if not args:
                _err("Project name required")
            cmd_tasks(args[0])
        elif cmd == "tags":
            cmd_tags(active_only="--all" not in args)
        elif cmd == "today":
            cmd_today(int(args[0]) if args else 50)
        elif cmd == "flagged":
            cmd_flagged(int(args[0]) if args else 50)
        elif cmd == "search":
            if not args:
                _err("Search query required")
            non_flag = [a for a in args if not a.startswith("-")]
            limit = int(non_flag[-1]) if len(non_flag) > 1 and non_flag[-1].isdigit() else 20
            query = " ".join(a for a in non_flag if not a.isdigit() or a == non_flag[0])
            cmd_search(query, limit)
        elif cmd == "info":
            if not args:
                _err("Task ID required")
            cmd_info(args[0])
        elif cmd == "add":
            if not args:
                _err("Task name required")
            cmd_add(args[0], args[1] if len(args) > 1 else None)
        elif cmd == "newproject":
            if not args:
                _err("Project name required")
            cmd_newproject(args[0], args[1] if len(args) > 1 else None)
        elif cmd == "newfolder":
            if not args:
                _err("Folder name required")
            cmd_newfolder(args[0])
        elif cmd == "newtag":
            if not args:
                _err("Tag name required")
            cmd_newtag(args[0])
        elif cmd == "complete":
            if not args:
                _err("Task ID required")
            cmd_complete(args[0])
        elif cmd == "uncomplete":
            if not args:
                _err("Task ID required")
            cmd_uncomplete(args[0])
        elif cmd == "delete":
            if not args:
                _err("Task ID required")
            cmd_delete(args[0])
        elif cmd == "rename":
            if len(args) < 2:
                _err("Task ID and new name required")
            cmd_rename(args[0], " ".join(args[1:]))
        elif cmd == "note":
            if len(args) < 2:
                _err("Task ID and text required")
            cmd_note(args[0], " ".join(args[1:]))
        elif cmd == "setnote":
            if len(args) < 2:
                _err("Task ID and text required")
            cmd_setnote(args[0], " ".join(args[1:]))
        elif cmd == "defer":
            if len(args) < 2:
                _err("Task ID and date required")
            cmd_defer(args[0], args[1])
        elif cmd == "due":
            if len(args) < 2:
                _err("Task ID and date required")
            cmd_due(args[0], args[1])
        elif cmd == "flag":
            if not args:
                _err("Task ID required")
            value = args[1].lower() != "false" if len(args) > 1 else True
            cmd_flag(args[0], value)
        elif cmd == "tag":
            if len(args) < 2:
                _err("Task ID and tag name required")
            cmd_tag(args[0], args[1])
        elif cmd == "untag":
            if len(args) < 2:
                _err("Task ID and tag name required")
            cmd_untag(args[0], args[1])
        elif cmd == "move":
            if len(args) < 2:
                _err("Task ID and project name required")
            cmd_move(args[0], args[1])
        elif cmd == "repeat":
            if len(args) < 4:
                _err("Usage: repeat <taskId> <method> <interval> <unit>")
            cmd_repeat(args[0], args[1], int(args[2]), args[3])
        elif cmd == "unrepeat":
            if not args:
                _err("Task ID required")
            cmd_unrepeat(args[0])
        # --- new commands ---
        elif cmd == "summary":
            cmd_summary()
        elif cmd == "project-tree":
            if not args:
                _err("Project name required")
            limit = int(args[1]) if len(args) > 1 else 300
            cmd_project_tree(args[0], limit)
        elif cmd == "project-search":
            if not args:
                _err("Search term required")
            limit = int(args[1]) if len(args) > 1 else 20
            cmd_project_search(args[0], limit)
        elif cmd == "folder":
            if not args:
                _err("Folder name required")
            limit = int(args[1]) if len(args) > 1 else 50
            cmd_folder_detail(args[0], limit)
        elif cmd == "root":
            limit = int(args[0]) if args else 50
            cmd_root(limit)
        elif cmd == "tag-summary":
            if not args:
                _err("Tag name required")
            limit = int(args[1]) if len(args) > 1 else 200
            cmd_tag_summary(args[0], limit)
        elif cmd == "tag-family":
            if not args:
                _err("Tag name required")
            limit = int(args[1]) if len(args) > 1 else 2000
            cmd_tag_family(args[0], limit)
        elif cmd == "available":
            limit = int(args[0]) if args else 50
            cmd_available(limit)
        elif cmd == "review":
            all_items = "--all" in args
            non_flag = [a for a in args if not a.startswith("-")]
            limit = int(non_flag[0]) if non_flag else 50
            cmd_review(limit, active_only=not all_items)
        elif cmd == "prefs":
            cmd_prefs(args)
        elif cmd in ("help", "--help", "-h"):
            _out(_HELP)
        else:
            _err(f"Unknown command: {cmd}")
    except SystemExit:
        raise
    except RuntimeError as exc:
        _err(str(exc))
    except Exception as exc:
        _err(f"Unexpected error: {exc}")


if __name__ == "__main__":
    dispatch(sys.argv[1:])
