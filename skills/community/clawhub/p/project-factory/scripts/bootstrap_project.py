#!/usr/bin/env python3
"""Bootstrap a new content-pipeline project from collected parameters."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SHARED = Path(__file__).resolve().parents[2] / "projects" / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

WORKSPACE = Path(__file__).resolve().parents[3] / "projects"

# all-projects check
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from allprojects_check import run_all_projects
except ImportError:
    def run_all_projects(): pass  # fallback

# Expose as _run_all_projects for consistency with handler
try:
    _run_all_projects = run_all_projects
except NameError:
    pass  # fallback already assigned
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
OPENCLAW_CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap a new content-pipeline project")
    parser.add_argument("--project-key")
    parser.add_argument("--project-name")
    parser.add_argument("--description")
    parser.add_argument("--bot-token")
    parser.add_argument("--chat-id")
    parser.add_argument("--routing-group")
    parser.add_argument("--thread-ids", default="")
    parser.add_argument("--cron-schedule")
    parser.add_argument("--cron-timeout", type=int, default=1200)
    parser.add_argument("--flowchart", default="")
    parser.add_argument("--nodes-json", default="[]")
    parser.add_argument("--wechat-publish", default="no")
    parser.add_argument("--wechat-clash-selector", default="GLOBAL")
    parser.add_argument("--wechat-clash-unix", default="/tmp/verge/verge-mihomo.sock")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created without writing anything")
    parser.add_argument("--plan", action="store_true", help="Unified preview: files + config + cron + agent changes (new or existing project)")
    parser.add_argument("--validate-only", help="Validate an existing project scaffold (path to project dir)")
    parser.add_argument("--fix-suggestions", action="store_true", help="Emit concrete fix blocks for --validate-only findings")
    parser.add_argument("--fix", action="store_true", help="Apply auto-safe fixes to an existing scaffold (back up + write)")
    parser.add_argument("--fix-dry-run", action="store_true", help="Show what --fix would change without applying")
    parser.add_argument("--continue-from-fix", help="After --fix, continue bootstrap config writes using an existing project dir")
    parser.add_argument("--fix-and-continue", action="store_true", help="Shorthand: --fix --continue-from-fix in one step")
    parser.add_argument("--interactive", action="store_true", help="Interactive step-by-step parameter collection with validation")
    parser.add_argument("--all-projects", action="store_true", help="Run health check on all projects under projects/ and print a summary table")
    parser.add_argument("--cron-list", action="store_true", help="List all openclaw cron jobs with project mapping")
    parser.add_argument("--cron-remove", metavar="JOB_ID", help="Remove a cron job by its ID (see --cron-list)")
    return parser.parse_args()


def parse_thread_ids(raw: str) -> dict[str, str]:
    result = {}
    for part in raw.split(","):
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        result[k.strip()] = v.strip()
    return result


def T(ctx: dict, template: str) -> str:
    """Substitute ${KEY} in template with ctx values."""
    for k, v in ctx.items():
        template = template.replace(f"${{{k}}}", str(v))
    return template


def ensure_dirs(root: Path) -> None:
    for sub in [
        "data/rewrite_queue", "data/rewrite_results",
        "data/publish_queue", "data/publish_receipts",
        "data/state", "data/trend_pool",
        "deliverables/drafts", "deliverables/wechat",
        "logs/run_summaries", "logs/.trend_step", "logs/.content_step",
        "config", "scripts", ".locks", "memory",
    ]:
        (root / sub).mkdir(parents=True, exist_ok=True)


def load_static_template(name: str) -> str:
    return (Path(__file__).resolve().parent / name).read_text(encoding="utf-8")


def write_project_files(root: Path, ctx: dict, sources_json: str) -> None:
    key = ctx["PROJECT_KEY"]

    (root / "PROJECT.md").write_text(PROJECT_MD(ctx), encoding="utf-8")
    (root / "AGENTS.md").write_text(AGENTS_MD(ctx), encoding="utf-8")
    (root / "IDENTITY.md").write_text(IDENTITY_MD(ctx), encoding="utf-8")
    (root / "PROJECT_IDENTITY.md").write_text(PROJECT_IDENTITY_MD(ctx), encoding="utf-8")
    (root / "PROJECT_POLICY.md").write_text(PROJECT_POLICY_MD(ctx), encoding="utf-8")
    (root / "GROUP_PROFILE.md").write_text(GROUP_PROFILE_MD(ctx), encoding="utf-8")
    (root / "USER.md").write_text(USER_MD(ctx), encoding="utf-8")
    (root / "SOUL.md").write_text(SOUL_MD(ctx), encoding="utf-8")
    (root / "TOOLS.md").write_text(TOOLS_MD(ctx), encoding="utf-8")
    (root / "HEARTBEAT.md").write_text(HEARTBEAT_MD(ctx), encoding="utf-8")
    (root / "WORKFLOW.md").write_text(WORKFLOW_MD(ctx), encoding="utf-8")
    (root / "BOOTSTRAP.md").write_text(BOOTSTRAP_MD(ctx), encoding="utf-8")
    (root / "style-guide.md").write_text(STYLE_GUIDE_MD(ctx), encoding="utf-8")

    try:
        sources = json.loads(sources_json)
    except json.JSONDecodeError:
        sources = []
    (root / "sources.json").write_text(
        json.dumps({"sources": sources}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (root / "brand_map.json").write_text(
        json.dumps({"brands": []}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    (root / "config" / "runtime.env").write_text(RUNTIME_ENV(ctx), encoding="utf-8")
    (root / ".env").write_text(ENV_FILE(ctx), encoding="utf-8")

    (root / "scripts" / "project_routing.py").write_text(PROJECT_ROUTING_PY(ctx), encoding="utf-8")
    (root / "scripts" / "broadcast_event.py").write_text(BROADCAST_EVENT_PY(ctx), encoding="utf-8")
    (root / "scripts" / "write_run_summary.py").write_text(WRITE_RUN_SUMMARY_PY(ctx), encoding="utf-8")
    (root / "scripts" / "pipeline_reporter.py").write_text(PIPELINE_REPORTER_PY(ctx), encoding="utf-8")
    (root / "scripts" / "run_pipeline.sh").write_text(RUN_PIPELINE_SH(ctx), encoding="utf-8")
    (root / "scripts" / f"{key}_bot.py").write_text(BOT_PY(ctx), encoding="utf-8")
    for static_name in ["self_check.py", "upgrade_project.py", "update_memory.py"]:
        (root / "scripts" / static_name).write_text(load_static_template(static_name), encoding="utf-8")

    for script in (root / "scripts").glob("*.sh"):
        script.chmod(0o755)
    for script in (root / "scripts").glob("*.py"):
        script.chmod(0o755)

    (root / "logs" / "latest_run_summary.json").write_text(
        json.dumps({
            "schemaVersion": 1, "projectKey": key,
            "status": "initialized",
            "runDate": datetime.now().strftime("%Y-%m-%d"),
            "generatedAt": NOW,
        }, indent=2) + "\n", encoding="utf-8"
    )

    print(f"  Created {root.name}/ — {len(list(root.rglob('*')))} files/dirs")


def update_routing(args: argparse.Namespace, threads: dict[str, str]) -> None:
    path = WORKSPACE.parent / "config" / "project_routing.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = {"version": 1, "updatedAt": NOW, "routingGroups": {}, "projects": {}}

    data.setdefault("version", 1)
    data["updatedAt"] = NOW
    data.setdefault("routingGroups", {})
    data.setdefault("projects", {})

    group_key = args.routing_group
    group_cfg = data["routingGroups"].setdefault(group_key, {})
    group_cfg.update({
        "channel": "telegram",
        "defaultTarget": args.project_name,
        "chatId": args.chat_id,
        "threadId": threads.get("report", "2"),
        "reportThreadId": threads.get("report", "2"),
        "chatThreadId": threads.get("chat", "3"),
        "generalThreadId": threads.get("general", "1"),
        "source": group_cfg.get("source", "bootstrap"),
        "notes": (
            "Project-scoped routing enabled by bootstrap_project.py: "
            f"general={threads.get('general', '1')}, report={threads.get('report', '2')}, "
            f"chat={threads.get('chat', '3')}"
        ),
        "projectId": args.project_key,
        "contextGate": True,
        "routeMode": "project-scoped",
        "assistantMap": {
            "general": "main",
            "report": f"{args.project_key}-chat",
            "chat": f"{args.project_key}-chat",
        },
        "topicOwnership": {
            "general": {
                "ownerAgent": "main",
                "projectScope": args.project_key,
                "mode": "router-only",
            },
            "report": {
                "ownerAgent": f"{args.project_key}-chat",
                "projectScope": args.project_key,
                "mode": "answering",
            },
            "chat": {
                "ownerAgent": f"{args.project_key}-chat",
                "projectScope": args.project_key,
                "mode": "answering",
            },
        },
    })

    key = args.project_key
    project_cfg = data["projects"].setdefault(key, {})
    project_cfg.update({
        "routingGroup": group_key,
        "syncToMain": "exception-only",
        "conversationScope": "project-only",
        "primaryAssistant": f"{args.project_key}-chat",
        "generalAssistantMode": "router-only",
    })

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  Updated config/project_routing.json")


def ensure_project_agent_registration(args: argparse.Namespace) -> None:
    path = OPENCLAW_CONFIG_PATH
    if not path.exists():
        print(f"  ⚠️  Skipped project assistant registration: {path} not found")
        return

    agent_id = f"{args.project_key}-chat"
    agent_dir = Path.home() / ".openclaw" / "agents" / agent_id / "agent"
    sessions_dir = Path.home() / ".openclaw" / "agents" / agent_id / "sessions"
    agent_dir.mkdir(parents=True, exist_ok=True)
    sessions_dir.mkdir(parents=True, exist_ok=True)

    main_agent_dir = Path.home() / ".openclaw" / "agents" / "main" / "agent"
    for filename in ["auth-profiles.json", "models.json"]:
        src = main_agent_dir / filename
        dst = agent_dir / filename
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)

    sessions_json = sessions_dir / "sessions.json"
    if not sessions_json.exists():
        sessions_json.write_text('{"version":1,"sessions":[]}\n', encoding="utf-8")

    data = json.loads(path.read_text(encoding="utf-8"))
    agents = data.setdefault("agents", {}).setdefault("list", [])
    if not any(a.get("id") == agent_id for a in agents):
        agents.append({
            "id": agent_id,
            "name": agent_id,
            "workspace": str(WORKSPACE / args.project_key),
            "agentDir": str(agent_dir),
            "model": "minimax-portal/MiniMax-M2.5",
            "identity": {
                "name": f"{args.project_name} Chat",
                "emoji": "🧭",
            },
        })
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  Registered project assistant: {agent_id}")


def update_openclaw_telegram_config(args: argparse.Namespace, threads: dict[str, str]) -> None:
    path = OPENCLAW_CONFIG_PATH
    if not path.exists():
        print(f"  ⚠️  Skipped ~/.openclaw/openclaw.json update: {path} not found")
        return

    data = json.loads(path.read_text(encoding="utf-8"))
    telegram = data.setdefault("channels", {}).setdefault("telegram", {})
    groups = telegram.setdefault("groups", {})

    groups[str(args.chat_id)] = {
        "requireMention": False,
        "projectId": args.project_key,
        "contextGate": True,
        "assistantRoutingMode": "project-scoped",
        "topics": {
            threads.get("general", "1"): {
                "requireMention": True,
                "systemPrompt": (
                    f"This is the general topic for the {args.project_key} project. "
                    "You are acting as a router only. Do not answer project facts directly unless the user asks a pure routing question. "
                    "For project questions, direct the user to the project chat topic and keep the answer short."
                ),
                "agentId": "main",
            },
            threads.get("report", "2"): {
                "requireMention": False,
                "systemPrompt": (
                    f"This is the report topic for the {args.project_key} project. "
                    "Answer inside project scope only. Apply a context gate before answering: use project-local documents, workflows, and logs first. "
                    "If a similar pattern exists in another project, label it explicitly as analogy instead of fact."
                ),
                "agentId": f"{args.project_key}-chat",
            },
            threads.get("chat", "3"): {
                "requireMention": False,
                "systemPrompt": (
                    f"This is the chat topic for the {args.project_key} project. "
                    "Answer as the dedicated project assistant. Use project-local facts, workflows, logs, and policies first. "
                    "Do not substitute facts from another project. If cross-project experience is useful, label it as analogy."
                ),
                "agentId": f"{args.project_key}-chat",
            },
        },
    }

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  Updated {path}")


def validate_generated_project(root: Path) -> None:
    scripts_dir = root / "scripts"
    py_scripts = sorted(str(path) for path in scripts_dir.glob("*.py"))
    if py_scripts:
        result = subprocess.run([sys.executable, "-m", "py_compile", *py_scripts], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Python validation failed:\n{result.stderr.strip() or result.stdout.strip()}")

    shell_script = scripts_dir / "run_pipeline.sh"
    if shell_script.exists():
        result = subprocess.run(["bash", "-n", str(shell_script)], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Shell validation failed:\n{result.stderr.strip() or result.stdout.strip()}")

    print("  ✅ Generated scripts validated (py_compile + bash -n)")


def check_template_safety(content: str, filepath: str) -> list[str]:
    """Check template for unresolved variables and path safety issues. Returns list of warnings."""
    warnings = []
    # Unresolved ${KEY} patterns (but ignore ${ that are in code strings)
    import re
    unresolved = re.findall(r'\$\{[A-Z_][A-Z0-9_]*\}', content)
    if unresolved:
        # Dedupe
        seen = set()
        for v in unresolved:
            if v not in seen:
                seen.add(v)
                warnings.append(f"  ❌  {filepath}: unresolved variable {v}")
    # Double-brace Mermaid decision nodes without matching close
    double_braces = re.findall(r'\{\{[^}]+\}\}\s*-->', content)
    if double_braces:
        warnings.append(f"  ⚠️  {filepath}: possibly malformed decision node (mismatched {{")
    # Path traversal attempts
    if '..' in content and 'Path(' in content:
        warnings.append(f"  ⚠️  {filepath}: possible path traversal detected")
    return warnings


# fix record: (severity, category, message, fix_block)
# fix_block is None or a string with actionable content to paste/apply

def validate_scaffold_dir(project_dir: Path, emit_fixes: bool = False) -> tuple[bool, list]:
    """Run full validation on an existing project scaffold.
    Returns (all_ok, fixes). fixes is a list of (severity, category, message, fix_block)."""
    print(f"\n🔍 Validating scaffold: {project_dir}")
    all_ok = True
    fixes = []  # (severity, category, message, fix_block)

    # helpers
    def add(sev, cat, msg, fix=None):
        fixes.append((sev, cat, msg, fix))
        if sev == "FAIL":
            nonlocal all_ok; all_ok = False

    project_key = project_dir.name

    # ── 1. Required files ──────────────────────────────────────────────────
    for fname in ["PROJECT.md", "AGENTS.md", "IDENTITY.md"]:
        p = project_dir / fname
        if not p.exists():
            add("FAIL", "files", f"  ❌ Missing required file: {fname}")
        else:
            add("OK", "files", f"  ✅ {fname}")

    # ── 2. config/runtime.env ────────────────────────────────────────────────
    runtime_env = project_dir / "config" / "runtime.env"
    if not runtime_env.exists():
        fix = f"""\
# Create config/runtime.env with at least these vars:
PROJECT_KEY={project_key}
CHAT_ID=TODO_your_chat_id
BOT_TOKEN=TODO_your_bot_token
ROUTING_GROUP=TODO_your_routing_group
CRON_SCHEDULE="0 9 * * *"
CRON_TIMEOUT=1200
"""
        add("FAIL", "env", f"  ❌ config/runtime.env missing", fix)
    else:
        add("OK", "env", f"  ✅ config/runtime.env")
        env_content = runtime_env.read_text()
        for var in ["PROJECT_KEY", "CHAT_ID", "BOT_TOKEN"]:
            if var not in env_content:
                fix = f'# Add to config/runtime.env:\n{var}=TODO_replace_with_real_value'
                add("FAIL", "env", f"  ❌ runtime.env missing required var: {var}", fix)
            else:
                val = env_content.split(var + "=")[1].split("\n")[0].strip()
                if val in ("", "TODO", "YOUR_" + var):
                    add("WARN", "env", f"  ⚠️  runtime.env: {var} is a placeholder — replace with real value")

    # ── 3. Run script ──────────────────────────────────────────────────────
    run_scripts = sorted((project_dir / "scripts").glob("run_*.sh"))
    if run_scripts:
        add("OK", "shell", f"  ✅ run script: {run_scripts[0].name}")
        shell_script = run_scripts[0]
        content = shell_script.read_text()
        if "# === Add your pipeline stages here ===" in content:
            after_marker = content.split("# === Add your pipeline stages here ===")[1][:300]
            if "python3 scripts/" not in after_marker and "python3 $ROOT/scripts/" not in after_marker:
                fix = f"""\
# In {run_scripts[0].name}, replace the comment after the marker with your bot call, e.g.:
python3 $ROOT/scripts/{project_key}_bot.py >> "$RUN_LOG" 2>&1
"""
                add("HINT", "shell", "  💡 run script is a stub — add your bot call after '# === Add your pipeline stages here ==='", fix)
    else:
        fix = f"""\
#!/bin/bash
set -euo pipefail
ROOT="$(dirname "$0")/.."
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"
python3 "$ROOT/scripts/{project_key}_bot.py" >> "$LOG_DIR/daily_pipeline.log" 2>&1
"""
        add("WARN", "shell", "  ⚠️  No run_*.sh found in scripts/ — create one", fix)

    # ── 4. sources.json ───────────────────────────────────────────────────────
    sources_json = project_dir / "sources.json"
    if not sources_json.exists():
        fix = '{"sources": [{"url": "https://example.com/feed", "type": "fetch"}]}\n'
        add("WARN", "json", "  ⚠️  sources.json missing — create it", fix)
    else:
        try:
            data = json.loads(sources_json.read_text())
            sources_list = data.get("sources", [])
            if not sources_list:
                fix = '{"sources": [{"url": "https://example.com/feed", "type": "fetch"}]}\n'
                add("WARN", "json", "  ⚠️  sources.json is empty — add your feed/source URLs", fix)
            else:
                add("OK", "json", f"  ✅ sources.json: {len(sources_list)} source(s)")
        except json.JSONDecodeError as e:
            fix = '{"sources": [{"url": "https://example.com/feed", "type": "fetch"}]}\n'
            add("FAIL", "json", f"  ❌ sources.json malformed JSON: {e}", fix)

    # ── 5. logs/latest_run_summary.json ──────────────────────────────────────
    summary_json = project_dir / "logs" / "latest_run_summary.json"
    if not summary_json.exists():
        fix = f"""\
{{
  "schemaVersion": 1,
  "projectKey": "{project_key}",
  "status": "initialized",
  "runDate": "{datetime.now().strftime('%Y-%m-%d')}",
  "generatedAt": "{NOW}"
}}
"""
        add("WARN", "json", "  ⚠️  logs/latest_run_summary.json missing", fix)
    else:
        try:
            data = json.loads(summary_json.read_text())
            if "status" not in data or "runDate" not in data:
                fix = f"""\
# Run this to regenerate logs/latest_run_summary.json:
python3 scripts/write_run_summary.py --summary logs/latest_run_summary.json --run-date {datetime.now().strftime('%Y-%m-%d')}
"""
                add("WARN", "json", "  ⚠️  latest_run_summary.json missing 'status' or 'runDate'", fix)
            else:
                add("OK", "json", f"  ✅ latest_run_summary.json (status={data.get('status')})")
        except json.JSONDecodeError as e:
            fix = f"""\
# Replace logs/latest_run_summary.json with:
{{
  "schemaVersion": 1,
  "projectKey": "{project_key}",
  "status": "initialized",
  "runDate": "{datetime.now().strftime('%Y-%m-%d')}",
  "generatedAt": "{NOW}"
}}
"""
            add("FAIL", "json", f"  ❌ latest_run_summary.json malformed JSON: {e}", fix)

    # ── 6. Template safety ───────────────────────────────────────────────────
    for md_file in project_dir.rglob("*.md"):
        rel = md_file.relative_to(project_dir)
        content = md_file.read_text(encoding="utf-8", errors="replace")
        for w in check_template_safety(content, str(rel)):
            # Unresolved ${VAR} is a bootstrap bug — upgrade to FAIL
            if "unresolved variable" in w:
                add("FAIL", "template", w)
            else:
                add("WARN", "template", w)

    # ── 7. Shell syntax ─────────────────────────────────────────────────────
    if shell_script and shell_script.exists():
        result = subprocess.run(["bash", "-n", str(shell_script)], capture_output=True, text=True)
        if result.returncode == 0:
            add("OK", "shell", f"  ✅ {shell_script.name} syntax OK")
        else:
            add("FAIL", "shell", f"  ❌ {shell_script.name}: {result.stderr.strip()}")

    # ── 8. Python syntax ────────────────────────────────────────────────────
    py_scripts = sorted((project_dir / "scripts").glob("*.py"))
    if py_scripts:
        result = subprocess.run([sys.executable, "-m", "py_compile", *py_scripts], capture_output=True, text=True)
        if result.returncode == 0:
            add("OK", "python", f"  ✅ {len(py_scripts)} Python scripts compile OK")
        else:
            for line in result.stderr.splitlines():
                add("FAIL", "python", f"  ❌ {line.strip()}")

    # ── Print all findings ───────────────────────────────────────────────────
    print()
    for sev, cat, msg, _ in fixes:
        print(msg)

    if emit_fixes:
        _print_fix_blocks(fixes, project_key)

    if all_ok:
        print("\n✅ Scaffold validation passed.")
    else:
        print("\n❌ Scaffold validation failed — run with --fix-suggestions to see repair blocks.")
    return all_ok, fixes


def _apply_fixes(project_dir: Path, fixes: list, dry_run: bool = False) -> None:
    """Apply auto-safe fixes to project_dir. If dry_run=True, only show what would change.

    Auto-safe (no confirmation needed):
    - create missing files with safe default content
    - append missing vars to runtime.env

    Needs confirmation:
    - overwrite an existing file's content (malformed JSON)
    """
    import shutil

    project_key = project_dir.name
    applied = []
    skipped = []

    for sev, cat, msg, fix in fixes:
        if sev not in ("FAIL", "WARN") or not fix:
            continue

        fix_lines = fix.strip().splitlines()

        # ── Missing sources.json ──────────────────────────────────────────
        if cat == "json" and "sources.json" in msg and "missing" in msg:
            target = project_dir / "sources.json"
            content = fix_lines[0] + "\n"  # the JSON line
            if dry_run:
                print(f"  [dry-run] WOULD create: {target}")
                print(f"            content: {content.strip()}")
            else:
                target.write_text(content, encoding="utf-8")
                print(f"  ✅ Created: {target}")
            applied.append(str(target))
            continue

        # ── Missing latest_run_summary.json ──────────────────────────────
        if cat == "json" and "latest_run_summary.json" in msg and "missing" in msg:
            target = project_dir / "logs" / "latest_run_summary.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            # extract JSON from fix block (everything between ``` fences)
            json_content = "\n".join(
                ln for ln in fix_lines
                if ln.strip() and not ln.startswith("#") and ln != "```"
            )
            if dry_run:
                print(f"  [dry-run] WOULD create: {target}")
            else:
                target.write_text(json_content + "\n", encoding="utf-8")
                print(f"  ✅ Created: {target}")
            applied.append(str(target))
            continue

        # ── runtime.env missing vars ─────────────────────────────────────
        if cat == "env" and "missing required var" in msg:
            target = project_dir / "config" / "runtime.env"
            # fix block: line0 = comment, line1 = VAR=value
            var_line = next((ln for ln in fix_lines if "=" in ln), None)
            if not var_line:
                skipped.append(f"  ⏭️  Could not parse env fix for: {msg}")
                continue
            var = var_line.split("=")[0].strip()
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                file_content = "\n".join(fix_lines) + "\n"
            else:
                file_content = "\n" + "\n".join(fix_lines) + "\n"
            if dry_run:
                print(f"  [dry-run] WOULD append to: {target}")
                print(f"            + {var}=TODO_replace_with_real_value")
            else:
                with open(target, "a", encoding="utf-8") as fh:
                    fh.write(file_content)
                print(f"  ✅ Appended {var} to: {target}")
            applied.append(str(target))
            continue

        # ── Malformed JSON files ─────────────────────────────────────────
        if cat == "json" and "malformed JSON" in msg:
            target = project_dir / "sources.json" if "sources" in msg else project_dir / "logs" / "latest_run_summary.json"
            # find the replacement content in fix block
            json_content = "\n".join(
                ln for ln in fix_lines
                if ln.strip() and not ln.startswith("#") and ln != "```"
            )
            bak_path = target.with_suffix(target.suffix + ".bak")
            if dry_run:
                print(f"  [dry-run] WOULD replace: {target} (backup → {bak_path.name})")
            else:
                shutil.copy2(target, bak_path)
                target.write_text(json_content + "\n", encoding="utf-8")
                print(f"  ✅ Replaced: {target} (backup: {bak_path.name})")
            applied.append(str(target))
            continue

        # ── Warn: placeholder in runtime.env ─────────────────────────────
        if cat == "env" and "placeholder" in msg:
            # Can't auto-fix placeholder values without knowing real values — skip
            var = msg.split(":")[1].strip().split(" ")[0]
            skipped.append(f"  ⏭️  Skipped (needs real value): {var} in runtime.env — set manually")
            continue

        # ── Warn: empty sources.json ──────────────────────────────────────
        if cat == "json" and "empty" in msg:
            # Can't auto-fill real URLs — skip
            skipped.append("  ⏭️  Skipped: sources.json empty — add real URLs manually")
            continue

    # Summary
    print()
    if dry_run:
        print(f"🫧 DRY RUN — {len(applied)} fix(es) would be applied.")
    else:
        print(f"✅ Applied {len(applied)} fix(es).")

    if skipped:
        print()
        print("Manual action needed:")
        for s in skipped:
            print(s)

    if applied and not dry_run:
        print()
        print("Re-run validation to confirm:")
        print(f"  python3 scripts/bootstrap_project.py --validate-only {project_dir} --fix-suggestions")


def _print_fix_blocks(fixes: list, project_key: str) -> None:
    """Print actionable fix blocks for FAIL/WARN items."""
    blocks = []
    for sev, cat, msg, fix in fixes:
        if fix and sev in ("FAIL", "WARN", "HINT"):
            blocks.append((sev, cat, msg.strip(), fix))

    if not blocks:
        return

    print("\n" + "=" * 60)
    print("🔧 FIX SUGGESTIONS — copy/paste or apply as needed")
    print("=" * 60)

    # Group by category
    by_cat: dict[str, list] = {}
    for sev, cat, msg, fix in blocks:
        by_cat.setdefault(cat, []).append((sev, msg, fix))

    for cat, items in by_cat.items():
        print(f"\n## [{cat}]")
        for sev, msg, fix in items:
            label = {"FAIL": "❌", "WARN": "⚠️", "HINT": "💡"}.get(sev, "⚠️")
            print(f"\n### {label} {msg}")
            print("```")
            print(fix.rstrip())
            print("```")


def register_cron_job(args: argparse.Namespace) -> str | None:
    """Register a cron job via openclaw CLI with mode=none (reporter controls delivery)."""
    job_name = f"{args.project_key}: daily run"
    pipeline_path = WORKSPACE / args.project_key / "scripts" / "run_pipeline.sh"
    ws_root = str(WORKSPACE.parent)
    agent_message = (
        f"在 {ws_root}/projects/{args.project_key} 执行 bash {ws_root}/projects/{args.project_key}/scripts/run_pipeline.sh。"
        f"不要改代码。完成后汇报：1）处理结果；2）日志路径 projects/{args.project_key}/logs/daily_pipeline.log。"
    )

    cmd = [
        "openclaw", "cron", "add",
        "--name", job_name,
        "--cron", args.cron_schedule,
        "--session", "isolated",
        "--message", agent_message,
        "--light-context",
        "--model", "minimax-portal/MiniMax-M2.5",
        "--timeout-seconds", str(args.cron_timeout),
        "--no-deliver",
        "--description", f"每日 {args.project_name} 流水线调度，项目群汇报由 reporter 控制",
    ]

    print(f"  Registering cron job: {args.cron_schedule} (mode=none)")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ⚠️  Cron registration failed: {result.stderr.strip()}")
        print(f"     Run manually: {' '.join(cmd)}")
        return None

    # Extract job ID from output
    output = result.stdout.strip()
    print(f"  ✅ Cron job registered")
    if output:
        print(f"     {output}")
    return output



def _prompt(msg: str, default: str = "", validator=None):
    """Ask user input with optional default and validator."""
    while True:
        prompt = f"  {msg}"
        if default:
            prompt += f" [{default}]: "
        else:
            prompt += ": "
        val = input(prompt).strip()
        if not val:
            val = default
        if validator:
            ok, err = validator(val)
            if ok:
                return val
            print(f"    ❌ {err}")
        else:
            return val


def _yesno(msg: str) -> bool:
    val = input(f"  {msg} [y/N]: ").strip().lower()
    return val == "y"


def _collect_interactive() -> tuple[dict, dict]:
    """Collect project parameters interactively."""
    print("\n📋 Interactive project setup — Ctrl+C to abort\n")

    project_key = _prompt(
        "project_key (英文+短横线, 如 fashion-monitor)",
        validator=lambda v: (v.replace("-","").isalnum() and v.replace("-","").islower() and v,
                            "只能用英文小写、数字、短横线") if v else (False, "不能为空")
    )

    project_name = _prompt("project_name (中文名)")
    description = _prompt("description (一句话描述项目目标)")

    chat_id = _prompt(
        "chat_id (Telegram group ID, 如 -1001234567890)",
        validator=lambda v: (v.startswith("-") and v[1:].isdigit(),
                            "chat_id 必须是以 - 开头的数字")
    )

    bot_token = _prompt(
        "bot_token (Telegram bot token, 留空跳过)",
        validator=lambda v: (len(v) >= 10, "token 太短") if v else (True, "")
    )

    routing_group = _prompt("routing_group (留空默认 new)", "new")
    cron_schedule = _prompt("cron_schedule (留空默认 0 9 * * *)", "0 9 * * *")
    wechat_publish = "no"

    general_tid = _prompt("general_thread_id", "1")
    report_tid  = _prompt("report_thread_id",  "2")
    chat_tid    = _prompt("chat_thread_id",    "3")

    params = dict(
        project_key=project_key,
        project_name=project_name,
        description=description,
        bot_token=bot_token,
        chat_id=chat_id,
        routing_group=routing_group,
        cron_schedule=cron_schedule,
        wechat_publish=wechat_publish,
    )
    threads = dict(general=general_tid, report=report_tid, chat=chat_tid)
    return params, threads


def _build_ns(params: dict, threads: dict):
    """Convert collected params + threads into a argparse.Namespace for main()."""
    import argparse
    ns = argparse.Namespace(**{
        "project_key":      params["project_key"],
        "project_name":     params["project_name"],
        "description":      params["description"],
        "bot_token":        params["bot_token"],
        "chat_id":          params["chat_id"],
        "routing_group":    params["routing_group"],
        "thread_ids":       f"general={threads['general']},report={threads['report']},chat={threads['chat']}",
        "cron_schedule":    params["cron_schedule"],
        "cron_timeout":     1200,
        "flowchart":        "",
        "nodes_json":       "[]",
        "wechat_publish":   params["wechat_publish"],
        "wechat_clash_selector": "GLOBAL",
        "wechat_clash_unix":     "/tmp/verge/verge-mihomo.sock",
        "dry_run":          False,
        "plan":             False,
        "validate_only":    None,
        "fix_suggestions":  False,
        "fix":              False,
        "fix_dry_run":      False,
        "continue_from_fix": None,
        "fix_and_continue": False,
        "interactive":      False,
    })
    return ns


def _run_interactive() -> None:
    """Run interactive collection then dispatch to main() with collected args."""
    params, threads = _collect_interactive()

    print()
    print("✅ 参数校验通过")
    print()
    for k, v in params.items():
        print(f"  {k}: {v}")
    print(f"  threads: {threads}")
    print()

    if not _yesno("确认生成项目"):
        print("Abort.")
        sys.exit(0)

    ns = _build_ns(params, threads)
    # re-enter main() with collected args — use a dispatcher
    _dispatch(ns)


def _dispatch(args):
    """Dispatch to the appropriate mode based on args."""
    import argparse as _argparse
    # Re-parse to satisfy type checks, then route
    _do_fix_and_continue(args)


def _do_fix_and_continue(args):
    from pathlib import Path
    project_dir = Path(WORKSPACE) / args.project_key
    project_dir.mkdir(parents=True, exist_ok=True)
    # Build minimal ctx and write files
    threads = parse_thread_ids(args.thread_ids)
    ctx = {
        "PROJECT_KEY": args.project_key,
        "PROJECT_NAME": args.project_name,
        "DESCRIPTION": args.description,
        "BOT_TOKEN": args.bot_token,
        "CHAT_ID": args.chat_id,
        "ROUTING_GROUP": args.routing_group,
        "CRON_SCHEDULE": args.cron_schedule,
        "CRON_TIMEOUT": args.cron_timeout,
        "GENERAL_THREAD_ID": threads.get("general", "1"),
        "REPORT_THREAD_ID":  threads.get("report",  "2"),
        "CHAT_THREAD_ID":    threads.get("chat",    "3"),
        "PROJECT_ASSISTANT_ID": f"{args.project_key}-chat",
        "WECHAT_PUBLISH":    args.wechat_publish,
        "WECHAT_CLASH_SELECTOR": args.wechat_clash_selector,
        "WECHAT_CLASH_UNIX": args.wechat_clash_unix,
        "FLOWCHART": "",
        "NODES_JSON": "[]",
        "NODES": [],
        "NOW": NOW,
    }
    ensure_dirs(project_dir)
    write_project_files(project_dir, ctx, "[]")
    ok, _ = validate_scaffold_dir(project_dir, emit_fixes=False)
    if not ok:
        print()
        print("❌ Scaffold validation failed — aborting before config writes.")
        print("   Run with --fix to auto-repair, or fix manually.")
        sys.exit(1)
    update_routing(args, threads)
    ensure_project_agent_registration(args)
    update_openclaw_telegram_config(args, threads)
    job_info = register_cron_job(args)
    print(f"\n🎉 Project '{args.project_key}' bootstrapped.")
    print(f"   Location: {project_dir}")
    sys.exit(0)




def main() -> None:
    args = parse_args()

    # ── interactive mode ──────────────────────────────────────────────────────
    if args.interactive:
        _run_interactive()

    # ── all-projects mode ────────────────────────────────────────────────────
    if args.all_projects:
        _run_all_projects()
        sys.exit(0)

    # ── cron lifecycle mode ───────────────────────────────────────────────────
    if args.cron_list:
        OPENCLAW_BIN = Path.home() / ".nvm" / "versions" / "node" / "v22.20.0" / "bin" / "openclaw"
        result = subprocess.run(
            [str(OPENCLAW_BIN), "cron", "list", "--all", "--json"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error: {result.stderr.strip()}")
            sys.exit(1)

        import json
        data = json.loads(result.stdout)
        jobs = data.get("jobs", [])

        print(f"\n\U0001f4cb Cron Jobs ({len(jobs)} total)\n")

        # Map project keys for quick lookup
        project_keys = {}
        for d in sorted(WORKSPACE.iterdir()):
            if d.is_dir() and not d.name.startswith(".") and d.name != "shared":
                project_keys[d.name] = d

        for job in jobs:
            state = job.get("state", {})
            last_status = state.get("lastRunStatus", "ok") if state else "ok"
            icon = "\u2705" if last_status == "ok" else ("\u26a0\ufe0f" if last_status == "disabled" else "\u274c")
            sched = job.get("schedule", {})
            sched_expr = sched.get("expr", "?") if sched else "?"
            sched_tz   = sched.get("tz", "") if sched else ""
            sched_str  = f"{sched_expr} @ {sched_tz}" if sched_tz else sched_expr

            # Match to a project
            name = job.get("name", "")
            matched_proj = next((pk for pk in project_keys if pk in name.lower()), "")

            print(f"  {icon} [{last_status}] {name}")
            print(f"     ID: {job['id']}")
            print(f"     Schedule: {sched_str}")
            if matched_proj:
                print(f"     Project: {matched_proj}")
            print()
        sys.exit(0)


        # Header line
        header = lines[0]
        data_lines = lines[2:] if len(lines) > 2 else lines[1:]

        print(f"\n\U0001f4cb Cron Jobs ({len(data_lines)} total)\n")

        # Map project keys to their config dirs for matching
        project_keys = {}
        for d in sorted(WORKSPACE.iterdir()):
            if d.is_dir() and not d.name.startswith(".") and d.name != "shared":
                project_keys[d.name] = d

        for line in data_lines:
            if not line.strip():
                continue
            # Parse: ID | Name | Schedule | Next | Last | Status | ...
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 7:
                continue
            job_id   = parts[0].strip()
            name     = parts[1].strip()
            schedule = parts[2].strip()
            status   = parts[5].strip().lower()
            icon = "✅" if status == "ok" else ("⚠️" if status == "disabled" else "❌")
            print(f"  {icon} [{status}] {name}")
            print(f"     ID: {job_id}")
            print(f"     Schedule: {schedule}")
            print(f"     Next: {parts[3].strip()}")
            print()
        sys.exit(0)

    if args.cron_remove:
        OPENCLAW_BIN = Path.home() / ".nvm" / "versions" / "node" / "v22.20.0" / "bin" / "openclaw"
        job_id = args.cron_remove
        print(f"Removing cron job: {job_id}")
        result = subprocess.run(
            [str(OPENCLAW_BIN), "cron", "rm", job_id],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error removing job: {result.stderr.strip()}")
            sys.exit(1)
        print(f"✅ Job removed.")
        sys.exit(0)

    # ── fix / fix-dry-run / --plan (existing project) mode ───────────────────
    # --plan on existing project = dry-run of fixes (show what would change)
    if (args.fix or args.fix_dry_run or args.plan) and args.validate_only:
        project_dir = Path(args.validate_only).resolve()
        if not project_dir.exists() or not (project_dir / "PROJECT.md").exists():
            print(f"ERROR: not a scaffold directory: {project_dir}")
            sys.exit(1)
        is_dry = args.fix_dry_run or args.plan
        ok, fixes = validate_scaffold_dir(project_dir, emit_fixes=True)
        print()
        _apply_fixes(project_dir, fixes, dry_run=is_dry)
        if is_dry:
            print(f"\n🗺️  PLAN — run without --plan to apply these changes.")
        sys.exit(0 if ok else 1)

    # ── fix-and-continue mode ────────────────────────────────────────────────
    # Apply fixes then continue bootstrap config writes in one step
    if args.fix_and_continue:
        if not args.validate_only:
            print("ERROR: --fix-and-continue requires --validate-only <path>")
            sys.exit(1)
        project_dir = Path(args.validate_only).resolve()
        if not project_dir.exists() or not (project_dir / "PROJECT.md").exists():
            print(f"ERROR: not a scaffold directory: {project_dir}")
            sys.exit(1)

        # Step 1: apply fixes
        print(f"\n🔧 [--fix-and-continue] Step 1: applying fixes...")
        ok, fixes = validate_scaffold_dir(project_dir, emit_fixes=True)
        print()
        _apply_fixes(project_dir, fixes, dry_run=False)
        print()

        # Step 2: re-validate to confirm scaffold is clean
        print(f"\n🔍 [--fix-and-continue] Step 2: re-validating scaffold...")
        ok2, _ = validate_scaffold_dir(project_dir, emit_fixes=False)
        if not ok2:
            print(f"\n❌ Scaffold still has FAILs after --fix. Fix manually before continuing.")
            sys.exit(1)

        # Step 3: continue config writes (reconstruct args from project files)
        print(f"\n🔧 [--fix-and-continue] Step 3: continuing config writes...")
        runtime_env = project_dir / "config" / "runtime.env"
        env = {}
        for ln in runtime_env.read_text().splitlines():
            ln = ln.strip()
            if '=' in ln and not ln.startswith('#'):
                k, v = ln.split('=', 1)
                env[k.strip()] = v.strip()

        class NS:
            pass
        fake_args = NS()
        fake_args.project_key = project_dir.name
        fake_args.project_name = env.get("PROJECT_NAME", project_dir.name)
        fake_args.chat_id = env.get("CHAT_ID", "")
        fake_args.routing_group = env.get("ROUTING_GROUP", "")
        fake_args.bot_token = env.get("BOT_TOKEN", "")
        fake_args.cron_schedule = env.get("CRON_SCHEDULE", "0 9 * * *")
        fake_args.cron_timeout = int(env.get("CRON_TIMEOUT", "1200"))

        env_file = project_dir / ".env"
        if env_file.exists():
            for ln in env_file.read_text().splitlines():
                if 'BOT_TOKEN' in ln and '=' in ln:
                    fake_args.bot_token = ln.split('=', 1)[1].strip().strip('"')

        threads = {"general": "1", "report": "2", "chat": "3"}
        routing_cfg = project_dir.parent.parent / "config" / "project_routing.json"
        if routing_cfg.exists():
            import json as _json
            data = _json.loads(routing_cfg.read_text())
            grp = data.get("routingGroups", {}).get(fake_args.routing_group, {})
            threads = {
                "general": grp.get("generalThreadId", "1"),
                "report": grp.get("reportThreadId", "2"),
                "chat": grp.get("chatThreadId", "3"),
            }

        print(f"  routing_group: {fake_args.routing_group}")
        print(f"  chat_id: {fake_args.chat_id}")
        print(f"  cron: {fake_args.cron_schedule}")
        print()

        update_routing(fake_args, threads)
        ensure_project_agent_registration(fake_args)
        update_openclaw_telegram_config(fake_args, threads)
        job_info = register_cron_job(fake_args)

        print()
        print(f"✅ --fix-and-continue complete for '{project_dir.name}'.")
        print(f"   Location: {project_dir}")
        sys.exit(0)

    # ── validate-only mode ──────────────────────────────────────────────────
    if args.validate_only:
        project_dir = Path(args.validate_only).resolve()
        if not project_dir.exists() or not (project_dir / "PROJECT.md").exists():
            print(f"ERROR: not a scaffold directory: {project_dir}")
            sys.exit(1)
        ok, _ = validate_scaffold_dir(project_dir, emit_fixes=args.fix_suggestions)
        sys.exit(0 if ok else 1)

    # ── plan (new project — pure impact preview, no files created) ────────────
    # --plan on a new project: show full impact without creating or validating anything
    if args.plan and not args.validate_only:
        key = args.project_key or "TODO"
        threads = parse_thread_ids(args.thread_ids) if args.thread_ids else {}
        print(f"\n🗺️  PLAN — impact preview (no files will be created)")
        print(f"\n  Project: {args.project_name or 'TODO'} ({key})")
        print(f"  chat_id: {args.chat_id or 'TODO'}")
        print(f"  routing_group: {args.routing_group or 'TODO'}")
        print(f"  threads: {threads}")
        print(f"  cron: {args.cron_schedule or 'TODO'}")
        print(f"\n  Files that would be created (30 files):")
        for sub in [
            "PROJECT.md", "AGENTS.md", "IDENTITY.md", "PROJECT_IDENTITY.md",
            "PROJECT_POLICY.md", "GROUP_PROFILE.md", "USER.md", "SOUL.md",
            "TOOLS.md", "HEARTBEAT.md", "WORKFLOW.md", "BOOTSTRAP.md",
            "style-guide.md", "sources.json", "brand_map.json",
            "config/runtime.env", ".env",
            "scripts/project_routing.py", "scripts/broadcast_event.py",
            "scripts/write_run_summary.py", "scripts/pipeline_reporter.py",
            "scripts/run_pipeline.sh", f"scripts/{key}_bot.py",
            "scripts/self_check.py", "scripts/upgrade_project.py", "scripts/update_memory.py",
            "logs/latest_run_summary.json",
        ]:
            print(f"    projects/{key}/{sub}")
        print(f"\n  Config writes:")
        print(f"    ~/.openclaw/openclaw.json → groups[{args.chat_id or 'TODO'}] with 3 topics")
        print(f"    config/project_routing.json → routingGroups + projects entry")
        print(f"    openclaw agent → register '{key}-chat' assistant")
        print(f"  Cron registration:")
        print(f"    openclaw cron add @ {args.cron_schedule or 'TODO'}")
        print(f"\n  Auto-validation will run after file creation (G: abort on FAIL).")
        print(f"\n✅ PLAN — run without --plan to execute bootstrap.")
        sys.exit(0)

    # ── continue-from-fix mode ────────────────────────────────────────────────
    # After --fix resolves scaffold issues, continue with config writes (routing/agent/cron)
    if args.continue_from_fix:
        project_dir = Path(args.continue_from_fix).resolve()
        runtime_env = project_dir / "config" / "runtime.env"
        env_file = project_dir / ".env"
        if not runtime_env.exists() or not env_file.exists():
            print(f"ERROR: {project_dir} is not a bootstrapped project (missing runtime.env or .env)")
            sys.exit(1)

        # Reconstruct args from project files
        class NS:
            pass
        fake_args = NS()
        fake_args.project_key = project_dir.name

        # Parse runtime.env
        env = {}
        for ln in runtime_env.read_text().splitlines():
            ln = ln.strip()
            if '=' in ln and not ln.startswith('#'):
                k, v = ln.split('=', 1)
                env[k.strip()] = v.strip()

        fake_args.project_name = env.get("PROJECT_NAME", project_dir.name)
        fake_args.chat_id = env.get("CHAT_ID", "")
        fake_args.routing_group = env.get("ROUTING_GROUP", "")
        fake_args.bot_token = env.get("BOT_TOKEN", "")
        fake_args.cron_schedule = env.get("CRON_SCHEDULE", "0 9 * * *")
        fake_args.cron_timeout = int(env.get("CRON_TIMEOUT", "1200"))

        # Parse .env for bot token
        for ln in env_file.read_text().splitlines():
            if 'BOT_TOKEN' in ln and '=' in ln:
                fake_args.bot_token = ln.split('=', 1)[1].strip().strip('"')

        # Default threads
        threads = {"general": "1", "report": "2", "chat": "3"}

        # Detect thread IDs from openclaw config if available
        routing_cfg = project_dir.parent.parent / "config" / "project_routing.json"
        if routing_cfg.exists():
            import json as _json
            data = _json.loads(routing_cfg.read_text())
            group_key = fake_args.routing_group
            grp = data.get("routingGroups", {}).get(group_key, {})
            threads = {
                "general": grp.get("generalThreadId", "1"),
                "report": grp.get("reportThreadId", "2"),
                "chat": grp.get("chatThreadId", "3"),
            }

        print(f"\n🔧 Continuing bootstrap config writes for: {project_dir.name}")
        print(f"  routing_group: {fake_args.routing_group}")
        print(f"  chat_id: {fake_args.chat_id}")
        print(f"  cron: {fake_args.cron_schedule}")
        print()

        update_routing(fake_args, threads)
        ensure_project_agent_registration(fake_args)
        update_openclaw_telegram_config(fake_args, threads)
        job_info = register_cron_job(fake_args)

        print()
        print(f"✅ Bootstrap complete for '{project_dir.name}'.")
        print(f"   Location: {project_dir}")
        sys.exit(0)

    # ── dry-run mode (no full args needed) ─────────────────────────────────
    # Below here, all args except --dry-run are required unless explicitly optional
    if not args.dry_run:
        missing = [a for a in [
            ("--project-key", args.project_key),
            ("--project-name", args.project_name),
            ("--description", args.description),
            ("--bot-token", args.bot_token),
            ("--chat-id", args.chat_id),
            ("--routing-group", args.routing_group),
            ("--thread-ids", args.thread_ids),
            ("--cron-schedule", args.cron_schedule),
        ] if not a[1]]
        if missing:
            names = ', '.join(m[0] for m in missing)
            print(f"ERROR: required args missing ({names})")
            sys.exit(1)

    key = args.project_key
    root = WORKSPACE / key
    threads = parse_thread_ids(args.thread_ids) if args.thread_ids else {}

    if root.exists():
        print(f"ERROR: {root} already exists")
        sys.exit(1)

    try:
        nodes = json.loads(args.nodes_json)
    except json.JSONDecodeError:
        nodes = []

    flowchart = args.flowchart.replace('\\n', '\n').replace('\\"', '"') if args.flowchart else ""

    ctx = {
        "PROJECT_KEY": key,
        "PROJECT_NAME": args.project_name,
        "DESCRIPTION": args.description,
        "BOT_TOKEN": args.bot_token,
        "CHAT_ID": args.chat_id,
        "ROUTING_GROUP": args.routing_group,
        "CRON_SCHEDULE": args.cron_schedule,
        "CRON_TIMEOUT": args.cron_timeout,
        "GENERAL_THREAD_ID": threads.get("general", "1"),
        "REPORT_THREAD_ID": threads.get("report", "2"),
        "CHAT_THREAD_ID": threads.get("chat", "3"),
        "PROJECT_ASSISTANT_ID": f"{key}-chat",
        "WECHAT_PUBLISH": args.wechat_publish,
        "WECHAT_CLASH_SELECTOR": args.wechat_clash_selector,
        "WECHAT_CLASH_UNIX": args.wechat_clash_unix,
        "FLOWCHART": flowchart,
        "NODES_JSON": args.nodes_json,
        "NODES": nodes,
        "NOW": NOW,
    }

    if args.dry_run:
        print(f"\n🫧 DRY RUN — no files will be written")
        print(f"\n  Project: {args.project_name} ({args.project_key})")
        print(f"  chat_id: {args.chat_id}")
        print(f"  routing_group: {args.routing_group}")
        threads = parse_thread_ids(args.thread_ids)
        print(f"  threads: {threads}")
        print(f"  cron: {args.cron_schedule}")

        # Compute ctx for preview
        flowchart = args.flowchart.replace('\\n', '\n').replace('\\"', '"') if args.flowchart else ""
        ctx_preview = {
            "PROJECT_KEY": args.project_key,
            "PROJECT_NAME": args.project_name,
            "DESCRIPTION": args.description,
            "BOT_TOKEN": args.bot_token,
            "CHAT_ID": args.chat_id,
            "ROUTING_GROUP": args.routing_group,
            "CRON_SCHEDULE": args.cron_schedule,
            "CRON_TIMEOUT": args.cron_timeout,
            "GENERAL_THREAD_ID": threads.get("general", "1"),
            "REPORT_THREAD_ID": threads.get("report", "2"),
            "CHAT_THREAD_ID": threads.get("chat", "3"),
            "PROJECT_ASSISTANT_ID": f"{args.project_key}-chat",
            "WECHAT_PUBLISH": args.wechat_publish,
            "WECHAT_CLASH_SELECTOR": args.wechat_clash_selector,
            "WECHAT_CLASH_UNIX": args.wechat_clash_unix,
            "FLOWCHART": flowchart,
        }

        print(f"\n  Files that would be created:")
        for sub in [
            "PROJECT.md", "AGENTS.md", "IDENTITY.md", "PROJECT_IDENTITY.md",
            "PROJECT_POLICY.md", "GROUP_PROFILE.md", "USER.md", "SOUL.md",
            "TOOLS.md", "HEARTBEAT.md", "WORKFLOW.md", "BOOTSTRAP.md",
            "style-guide.md", "sources.json", "brand_map.json",
            "config/runtime.env", ".env",
            "scripts/project_routing.py", "scripts/broadcast_event.py",
            "scripts/write_run_summary.py", "scripts/pipeline_reporter.py",
            "scripts/run_pipeline.sh", f"scripts/{args.project_key}_bot.py",
            "scripts/self_check.py", "scripts/upgrade_project.py", "scripts/update_memory.py",
            "logs/latest_run_summary.json",
        ]:
            print(f"    projects/{args.project_key}/{sub}")

        print(f"\n  Config writes:")
        print(f"    ~/.openclaw/openclaw.json → groups[{args.chat_id}] with 3 topics")
        print(f"    config/project_routing.json → routingGroups[{args.routing_group}] + projects[{args.project_key}]")
        print(f"    openclaw cron → '{args.project_key}: daily run' @ {args.cron_schedule}")
        print(f"    openclaw agent → register '{args.project_key}-chat' assistant")
        print(f"\n✅ Dry run complete — no files created.")
        sys.exit(0)

    print(f"\nBootstrap: {args.project_name} ({key})")
    print(f"  chat_id: {args.chat_id}")
    print(f"  routing_group: {args.routing_group}")
    print(f"  threads: {threads}")
    print(f"  cron: {args.cron_schedule}")

    root.mkdir(parents=True)
    ensure_dirs(root)
    # Extract sources from nodes if any fetch node has source config
    sources_from_nodes = [
        {"node": n["id"], "url": n.get("config", {}).get("sourceUrl", ""), "type": n.get("type", "")}
        for n in nodes if n.get("type") == "fetch" and n.get("config", {}).get("sourceUrl")
    ]
    sources_json_str = json.dumps(sources_from_nodes, ensure_ascii=False)
    write_project_files(root, ctx, sources_json_str)
    # G: auto-validate generated scaffold before any side-effects
    ok, _ = validate_scaffold_dir(root, emit_fixes=False)
    if not ok:
        print()
        print("❌ Scaffold validation failed — aborting bootstrap before config writes.")
        print("   Run with --fix to auto-repair, or fix manually then re-run bootstrap.")
        sys.exit(1)
    update_routing(args, threads)
    ensure_project_agent_registration(args)
    update_openclaw_telegram_config(args, threads)
    job_info = register_cron_job(args)

    print(f"\n✅ Project '{key}' bootstrapped.")
    print(f"   Location: {root}")
    print(f"   Cron: {args.cron_schedule} (mode=none — reporter controls delivery)")
    print(f"\nNext steps:")
    print(f"  1. Edit scripts/{key}_bot.py with your polling logic")
    print(f"  2. Configure sources.json and brand_map.json")
    print(f"  3. Run: bash {root.relative_to(WORKSPACE.parent)}/scripts/run_pipeline.sh")
    print(f"  4. Verify Telegram reports at thread {threads.get('report', '2')}")
    print(f"  5. Confirm ~/.openclaw/openclaw.json contains explicit group {args.chat_id} with general/report/chat topics")


# ---------------------------------------------------------------------------
# Template functions — return rendered file content
# ---------------------------------------------------------------------------

DEFAULT_FLOWCHART = "flowchart TD\n    START([开始]) --> END([结束])"

def PROJECT_MD(c): return f"""\
# Project: {c['PROJECT_NAME']}

## Overview
- **Project Key**: `{c['PROJECT_KEY']}`
- **Description**: {c['DESCRIPTION']}
- **Owner**: AK (Chief Agent)
- **Human Stakeholder**: 主人 (Alex Liu)
- **Created**: {c['NOW']}

## Success Criteria
- Sources polled on schedule ({c['CRON_SCHEDULE']})
- All runs produce structured `logs/latest_run_summary.json`
- Telegram reports delivered to correct project threads

## Communication Surface
- Telegram group: {c['CHAT_ID']}
- Routing group: {c['ROUTING_GROUP']}
- Report thread: {c['REPORT_THREAD_ID']}
"""

def AGENTS_MD(c): return f"""\
# Agents — {c['PROJECT_NAME']}

| Agent | Role | Responsibilities |
|-------|------|-----------------|
| AK | Chief Agent | Intake priorities, approve publishing, monitor pipeline |
| {c['PROJECT_KEY']}_bot | Worker | Poll sources, fetch data, manage task queue |
| Content Bot | Worker | Transform content, generate drafts |
| Publish Bot | Worker | Upload to WeChat MP, report receipts |
"""

def IDENTITY_MD(c): return f"""\
# IDENTITY — {c['PROJECT_KEY']}

- **Project Key**: `{c['PROJECT_KEY']}`
- **Name**: {c['PROJECT_NAME']}
- **Description**: {c['DESCRIPTION']}
"""


def PROJECT_IDENTITY_MD(c): return f"""\
# PROJECT_IDENTITY

## project_id
{c['PROJECT_KEY']}

## project_name
{c['PROJECT_NAME']}

## what_this_project_is
{c['DESCRIPTION']}

## what_this_project_is_not
- not a generic cross-project assistant
- not a substitute for other project facts
- not allowed to silently import assumptions from unrelated projects

## authoritative_surfaces
- project-local docs in this directory
- project-local workflows and logs
- routing entry in `config/project_routing.json`

## cross_project_guardrail
If another project has a similar pattern, treat it as analogy only and label it explicitly.
"""

def PROJECT_POLICY_MD(c): return f"""\
# PROJECT_POLICY

## answering_rules
- project-scope-first
- use project-local facts before global memory
- do not import another project's facts as if they belong here
- if cross-project comparison is useful, label it as analogy

## routing_rules
- general topic is router-only
- report topic is for status, run results, and operational explanation
- chat topic is for project discussion, debugging, and repair

## escalation_rules
Escalate to main chat only when the issue affects shared layers, multiple projects, or system-wide rules.
"""

def GROUP_PROFILE_MD(c): return f"""\
# GROUP_PROFILE

## project_name
{c['PROJECT_NAME']}

## project_scope
{c['DESCRIPTION']}

## my_role
Project-scoped conversation assistant and execution coordination surface

## bot_roster
1. Scheduler Bot: triggers cron workflows
2. Ops/Worker Bot: executes pipeline work
3. Project Assistant: answers inside project scope

## collaboration_entrypoints
Check project status, explain a report, inspect failures, discuss workflow behavior, and coordinate project-local fixes

## conversation_policy
- this group defaults to {c['PROJECT_KEY']} scope
- general topic routes, project topics answer
- project questions must not silently drift into another project's facts
"""

def USER_MD(c): return f"""\
# USER — {c['PROJECT_KEY']}

## Primary User
Alex Liu — System owner and decision maker.

## User Goals
{c['DESCRIPTION']}

## Working Style
Prefers modular architecture, agent specialization, project-based execution.
Response style: direct, structured reasoning, concise.
"""

def SOUL_MD(c): return f"""\
# SOUL — {c['PROJECT_KEY']}

## Narrative Style
- Tone: Informative, professional
- Content focus: {c['DESCRIPTION']}

## Content Values
- Accuracy over speed
- Clear structure with key highlights
- Original source attribution
"""

def TOOLS_MD(c): return f"""\
# TOOLS — {c['PROJECT_KEY']}

## Skills Used (from flowchart nodes)
```json
{c.get('NODES_JSON', '[]')}
```

## Scheduler
- Cron: {c['CRON_SCHEDULE']} (Asia/Shanghai)
- Timeout: {c['CRON_TIMEOUT']}s

## Telegram
- Bot token: `{c['BOT_TOKEN'][:8]}...` (stored in .env)
- Chat ID: {c['CHAT_ID']}
- Threads: general={c['GENERAL_THREAD_ID']}, report={c['REPORT_THREAD_ID']}, chat={c['CHAT_THREAD_ID']}

## WeChat Publishing
- WeChat publish: {c['WECHAT_PUBLISH']}
"""

def HEARTBEAT_MD(c): return f"""\
# HEARTBEAT — {c['PROJECT_KEY']}

## Heartbeat
Every cron run ({c['CRON_SCHEDULE']}) is also a heartbeat event.

## What to Monitor
- `logs/latest_run_summary.json` exists and is not stale (> 25 hours old)
- Telegram report delivered to thread {c['REPORT_THREAD_ID']}
- No consecutive error status

## Failure Escalation
If a run fails twice consecutively: escalate to main chat (主人).
"""

def _build_nodes_table(nodes):
    """Build a markdown table from nodes list."""
    if not nodes:
        return "_No node configuration provided yet._"
    rows = ["| Node ID | Type | Label | Skills | Config |", "|---|---|---|---|---|"]
    for n in nodes:
        node_id = n.get("id", "")
        node_type = n.get("type", "")
        label = n.get("label", "")
        skills = ", ".join(n.get("skills", [])).replace(", ", "<br>")
        config_preview = ", ".join([f"{k}: {v}" for k, v in n.get("config", {}).items()])[:80]
        rows.append(f"| `{node_id}` | {node_type} | {label} | {skills} | {config_preview} |")
    return "\n".join(rows)


def WORKFLOW_MD(c): return f"""\
# Workflow — {c['PROJECT_KEY']}

## Flowchart

```mermaid
{c.get('FLOWCHART', DEFAULT_FLOWCHART)}
```

## Trigger
- **Scheduler**: cron ({c['CRON_SCHEDULE']})
- **Manual**: bash `scripts/run_pipeline.sh`

## Nodes

{_build_nodes_table(c.get('NODES', []))}

## Pipeline Stages

| # | Stage | Output |
|---|-------|--------|
| 1 | Polling / Fetching | Raw data in `data/` |
| 2 | Content Transform | Transformed content |
| 3 | Summary Archival | `logs/latest_run_summary.json` |
| 4 | Report Delivery | Telegram thread {c['REPORT_THREAD_ID']} |
"""

def BOOTSTRAP_MD(c): return f"""\
# BOOTSTRAP — {c['PROJECT_KEY']}

Project bootstrapped {c['NOW']} using `skills/project-scaffold`.

See `skills/project-scaffold/references/onboarding_checklist.md` for full checklist.

## Post-bootstrap
- [ ] Implement `scripts/{c['PROJECT_KEY']}_bot.py`
- [ ] Configure `sources.json` and `brand_map.json`
- [ ] Run `scripts/run_pipeline.sh` and verify
- [ ] Confirm Telegram reports at thread {c['REPORT_THREAD_ID']}
- [ ] Run `scripts/self_check.py` to validate setup
- [ ] Run `scripts/update_memory.py` to scaffold today's memory entry
- [ ] Add to MEMORY.md

## Infrastructure Scripts
| Script | Purpose |
|--------|---------|
| `run_pipeline.sh` | Main pipeline entry (includes finish() trap) |
| `self_check.py` | Health check: routing, summary freshness, script existence |
| `upgrade_project.py` | Sync project to latest scaffold version |
| `update_memory.py` | Generate today's memory log entry |
"""

def STYLE_GUIDE_MD(c): return f"""\
# Style Guide — {c['PROJECT_KEY']}

## Tone
- Professional, informative
- Chinese-language content with English source attribution

## Structure
- Title: clear, descriptive
- Body: key facts first, context second
- Attribution: link to original source

## Formatting
- Use Markdown
- Avoid excessive emojis
- Minimize promotional language
"""

def RUNTIME_ENV(c): return f"""\
BOT_TOKEN={c['BOT_TOKEN']}
TELEGRAM_BOT_TOKEN={c['BOT_TOKEN']}
TELEGRAM_CHAT_ID={c['CHAT_ID']}
CRON_SCHEDULE={c['CRON_SCHEDULE']}
CRON_TIMEOUT={c['CRON_TIMEOUT']}
REPORT_THREAD_ID={c['REPORT_THREAD_ID']}
CHAT_THREAD_ID={c['CHAT_THREAD_ID']}
GENERAL_THREAD_ID={c['GENERAL_THREAD_ID']}
WECHAT_PUBLISH={c['WECHAT_PUBLISH']}
WECHAT_CLASH_SELECTOR={c['WECHAT_CLASH_SELECTOR']}
WECHAT_CLASH_CONTROLLER_UNIX={c['WECHAT_CLASH_UNIX']}
"""

def ENV_FILE(c): return f"""\
TELEGRAM_BOT_TOKEN={c['BOT_TOKEN']}
TELEGRAM_CHAT_ID={c['CHAT_ID']}
REPORT_THREAD_ID={c['REPORT_THREAD_ID']}
CHAT_THREAD_ID={c['CHAT_THREAD_ID']}
GENERAL_THREAD_ID={c['GENERAL_THREAD_ID']}
WECHAT_PUBLISH={c['WECHAT_PUBLISH']}
WECHAT_CLASH_SELECTOR={c['WECHAT_CLASH_SELECTOR']}
WECHAT_CLASH_CONTROLLER_UNIX={c['WECHAT_CLASH_UNIX']}
"""

def PROJECT_ROUTING_PY(c): return f"""\
#!/usr/bin/env python3
\"\"\"Routing loader for {c['PROJECT_KEY']}.\"\"\"

from pathlib import Path
import sys

_SHARED = Path(__file__).resolve().parents[2] / "shared"
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))

from project_routing_loader import load_project_routing


def load_routing() -> dict:
    return load_project_routing(
        project_key="{c['PROJECT_KEY']}",
        default_routing_group="{c['ROUTING_GROUP']}",
        default_chat_id="{c['CHAT_ID']}",
        default_target="{c['PROJECT_NAME']}",
    )


if __name__ == "__main__":
    print(load_routing())
"""

def BROADCAST_EVENT_PY(c): return f"""\
#!/usr/bin/env python3
\"\"\"Send event updates to the Telegram project group.\"\"\"

import argparse
from pathlib import Path
import sys

_SHARED = Path(__file__).resolve().parents[2] / "shared"
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))

from project_routing import load_routing
from summary_reporter import send_project_report


def resolve_thread_id(route: dict, thread_key: str | None) -> str | None:
    if not thread_key:
        return route.get("threadId")
    mapping = {{
        "general": route.get("generalThreadId") or route.get("threadId"),
        "report": route.get("reportThreadId") or route.get("threadId"),
        "chat": route.get("chatThreadId"),
    }}
    return mapping.get(thread_key, route.get("threadId"))



def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("message", help="Text to send")
    parser.add_argument("--thread-key", choices=["general", "report", "chat"], default="report")
    args = parser.parse_args()
    route = load_routing()
    chat_id = str(route.get("chatId", "{c['CHAT_ID']}"))
    thread_id = resolve_thread_id(route, args.thread_key)
    send_project_report(message=args.message, default_route_loader=load_routing, thread_id=thread_id)
    print(f"Sent to {{chat_id}} thread {{thread_id}}")


if __name__ == "__main__":
    main()
"""

def WRITE_RUN_SUMMARY_PY(c): return f"""\
#!/usr/bin/env python3
\"\"\"Write run summary for {c['PROJECT_KEY']}.\"\"\"

import argparse
import json
from datetime import datetime
from pathlib import Path



def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True)
    parser.add_argument("--archive-summary")
    parser.add_argument("--run-date", required=True)
    args = parser.parse_args()
    data = {{
        "schemaVersion": 1,
        "projectKey": "{c['PROJECT_KEY']}",
        "runId": datetime.now().strftime("%Y-%m-%dT%H-%M-%S"),
        "status": "success",
        "generatedAt": datetime.now().isoformat(),
        "runDate": args.run_date,
        "source": "{c['PROJECT_KEY']}_bot.py",
    }}
    Path(args.summary).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    if args.archive_summary:
        Path(args.archive_summary).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    print("Summary written.")


if __name__ == "__main__":
    main()
"""

def PIPELINE_REPORTER_PY(c): return f"""\
#!/usr/bin/env python3
\"\"\"Pipeline reporter for {c['PROJECT_KEY']}.\"\"\"

import sys
from datetime import datetime
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "shared"
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))

from project_routing import load_routing
from summary_reporter import build_report_message, send_project_report, validate_today_summary

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "logs" / "latest_run_summary.json"


def build_report() -> str:
    summary, issues = validate_today_summary(SUMMARY_PATH, expected_project_key="{c['PROJECT_KEY']}")
    bullets = [
        f"Status: {{summary.get('status', 'N/A') if summary else 'N/A'}}",
        f"Run: {{summary.get('runDate', 'N/A') if summary else 'N/A'}}",
    ]
    return build_report_message(
        title="{c['PROJECT_NAME']} Run Report",
        date_str=datetime.now().strftime("%Y-%m-%d"),
        bullets=bullets,
        issues=issues or [],
        footer="",
    )



def main() -> None:
    route = load_routing()
    thread_id = route.get("reportThreadId") or route.get("threadId")
    send_project_report(message=build_report(), default_route_loader=load_routing, thread_id=thread_id)
    print(f"Report sent to thread {{thread_id}}")


if __name__ == "__main__":
    main()
"""

def RUN_PIPELINE_SH(c):
    pk_upper = c['PROJECT_KEY'].upper()
    return f"""\
#!/bin/bash
set -euo pipefail

PROJECT_KEY="{c['PROJECT_KEY']}"
ROOT="${{{pk_upper}_ROOT:-$(dirname $0)/..}}"
LOG_DIR="$ROOT/logs"
RUN_LOG="$LOG_DIR/daily_pipeline.log"
LOCK_DIR="$ROOT/.locks/daily_pipeline.lock"
RUN_DATE="$(TZ=Asia/Shanghai date '+%Y-%m-%d')"
SUMMARY_PATH="$LOG_DIR/latest_run_summary.json"
RUN_SUMMARY_DIR="$LOG_DIR/run_summaries"
RUN_STAMP="$(TZ=Asia/Shanghai date '+%Y-%m-%dT%H-%M-%S')"

mkdir -p "$LOG_DIR" "$RUN_SUMMARY_DIR" "$ROOT/.locks"

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  echo "[$(date)] Pipeline skipped: lock exists" >> "$RUN_LOG"
  exit 0
fi

cleanup() {{ rmdir "$LOCK_DIR" >/dev/null 2>&1 || true; }}

finish() {{
  PIPELINE_STATUS=$?
  echo "[$(date)] Pipeline exit: $PIPELINE_STATUS" >> "$RUN_LOG"
  python3 "$ROOT/scripts/write_run_summary.py" \\
    --summary "$SUMMARY_PATH" \\
    --archive-summary "$RUN_SUMMARY_DIR/run_$RUN_STAMP.json" \\
    --run-date "$RUN_DATE" >> "$RUN_LOG" 2>&1 || true
  python3 "$ROOT/scripts/pipeline_reporter.py" >> "$RUN_LOG" 2>&1 || true
}}

trap 'finish; cleanup; exit 143' TERM
trap 'finish; cleanup' EXIT

echo "[$(date)] Pipeline start" >> "$RUN_LOG"
cd "$ROOT"

# === Add your pipeline stages here ===
python3 scripts/{c['PROJECT_KEY']}_bot.py >> "$RUN_LOG" 2>&1

echo "[$(date)] Pipeline finished" >> "$RUN_LOG"
"""

def BOT_PY(c): return f"""\
#!/usr/bin/env python3
\"\"\"Polling bot for {c['PROJECT_KEY']}.

Nodes defined in WORKFLOW.md — implement handlers per node.
\"\"\"

import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]



def main() -> None:
    print(f"[{c['PROJECT_KEY']}_bot] Running...")
    # See WORKFLOW.md for node definitions
    # For each fetch node: poll source, write raw data to data/<node_id>_raw.jsonl
    # For each filter node: apply logic, write to data/<node_id>_filtered.jsonl


if __name__ == "__main__":
    main()
"""

if __name__ == "__main__":
    main()
