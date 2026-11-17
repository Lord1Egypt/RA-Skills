#!/usr/bin/env python3
"""
run_agent_evals.py — run the skill's scenarios through an agent that is not Claude.

A maintainer tool: the skill never runs it. `evals/evals.json` holds the scenarios. Each one
runs in its own throwaway project, with the skill installed where `npx skills add` puts a
project install for Codex, Cursor, Gemini CLI and OpenCode (.agents/skills/life-companion),
and with its own fake HOME, so ~/.companion inside a run is an empty scratch folder and the
real one is never read. Setup steps seed that folder through companion.py. Each turn goes to
the agent; after every turn the folder is snapshotted, the agent's final reply goes through
selfcheck.py, and the scenario's checks run. Everything lands in --out: a summary.json and a
digest.md per scenario, to grade against the scenario's expectations, plus a table of checks.

    python3 tools/run_agent_evals.py --list
    python3 tools/run_agent_evals.py --agent codex --only career-chat-answers
    python3 tools/run_agent_evals.py --agent codex --jobs 3 --out /tmp/life-companion-evals

Only codex is wired up: `codex exec --json` for a scenario's first turn and `codex exec resume`
for the rest. It runs on whatever account codex is logged in with; this script calls no API.
Exit status: 0 when every check passed, 1 when one failed, 2 for a usage or setup problem.
"""
import argparse
import concurrent.futures as cf
import fnmatch
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVALS = os.path.join(SKILL, "evals", "evals.json")
CODEX_HOME = os.environ.get("CODEX_HOME") or os.path.join(os.path.expanduser("~"), ".codex")
CHECK_KINDS = ("runs", "does_not_run", "reply_has", "reply_lacks", "home_empty", "file_has", "file_lacks")
TURN_LIMIT_S = 1200


class EvalError(Exception):
    """evals.json asks for something this runner cannot do."""


def load_evals(path=EVALS):
    """The scenarios, after checking that each one can actually be run and graded."""
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    evals = doc.get("evals") if isinstance(doc, dict) else None
    if not isinstance(evals, list) or not evals:
        raise EvalError(f"{path} has no evals list")
    names = set()
    for e in evals:
        name = e.get("name") if isinstance(e, dict) else None
        if not name or name in names:
            raise EvalError(f"every eval needs a name of its own; got {name!r}")
        names.add(name)
        turns = e.get("turns")
        if not isinstance(turns, list) or not turns or not all(isinstance(t, str) and t.strip() for t in turns):
            raise EvalError(f"{name}: turns must be a non-empty list of messages")
        if e.get("prompt") != turns[0]:
            raise EvalError(f"{name}: prompt must be the same as the first turn")
        for step in e.get("setup", []):
            if not isinstance(step, list) or not step or not isinstance(step[0], str):
                raise EvalError(f"{name}: a setup step is a companion.py argument list")
        for c in e.get("checks", []):
            kind = c.get("kind") if isinstance(c, dict) else None
            if kind not in CHECK_KINDS:
                raise EvalError(f"{name}: unknown check kind {kind!r}")
            turn = c.get("turn")
            if turn is not None and not (isinstance(turn, int) and 1 <= turn <= len(turns)):
                raise EvalError(f"{name}: check turn {turn!r} is not one of its {len(turns)} turns")
            if kind != "home_empty":
                if not c.get("pattern"):
                    raise EvalError(f"{name}: a {kind} check needs a pattern")
                try:
                    re.compile(c["pattern"])
                except re.error as err:
                    raise EvalError(f"{name}: pattern {c['pattern']!r} does not compile: {err}")
            if kind in ("file_has", "file_lacks") and not c.get("file"):
                raise EvalError(f"{name}: a {kind} check needs a file glob")
    return evals


def setup_argv(step):
    """A setup step as companion.py arguments; an object or a list is passed as JSON."""
    return [a if isinstance(a, str) else json.dumps(a, ensure_ascii=False) for a in step]


def _install(dest, source):
    os.makedirs(dest, exist_ok=True)
    if source == "head":
        tar = subprocess.run(["git", "-C", SKILL, "archive", "HEAD"], capture_output=True, check=True).stdout
        subprocess.run(["tar", "-x", "-C", dest], input=tar, check=True)
    else:
        shutil.copytree(SKILL, dest, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))


def _snapshot(home):
    root, out = os.path.join(home, ".companion"), {}
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8") as f:
                    out[os.path.relpath(path, root)] = f.read()
            except (OSError, UnicodeDecodeError) as err:
                out[os.path.relpath(path, root)] = f"<unreadable: {err}>"
    return out


def _tree_state(path):
    """File sizes and modification times under path, to notice a run touching it."""
    if not os.path.exists(path):
        return None
    state = {}
    for dirpath, _dirs, files in os.walk(path):
        for name in files:
            p = os.path.join(dirpath, name)
            try:
                st = os.stat(p)
            except OSError:
                continue
            state[os.path.relpath(p, path)] = (st.st_size, st.st_mtime_ns)
    return state


def _clip(text, head=6000, tail=2000):
    """A command's output with its beginning kept: the payload a reply is graded against comes
    first, and keeping only the tail lost it."""
    if len(text) <= head + tail:
        return text
    return text[:head] + f"\n…[{len(text) - head - tail} characters cut]…\n" + text[-tail:]


def _events(path):
    thread, commands, other = None, [], []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") == "thread.started":
                thread = ev.get("thread_id")
            elif ev.get("type") == "item.completed":
                item = ev.get("item") or {}
                if item.get("type") == "command_execution":
                    commands.append({"command": item.get("command") or "", "exit_code": item.get("exit_code"),
                                     "output": _clip(item.get("aggregated_output") or "")})
                elif item.get("type") != "agent_message":
                    other.append(item.get("type"))
    return thread, commands, other


def _codex_turn(prompt, work, home, env, thread, stem):
    last, events, err = stem + ".txt", stem + ".jsonl", stem + ".err"
    common = ["--json", "-o", last, "--skip-git-repo-check"]
    if thread is None:
        argv = ["codex", "exec", *common, "-s", "workspace-write", "-C", work, "--add-dir", home, prompt]
    else:
        argv = ["codex", "exec", "resume", thread, *common, "-c", 'sandbox_mode="workspace-write"',
                "-c", "sandbox_workspace_write.writable_roots=" + json.dumps([home]), prompt]
    started = time.time()
    with open(events, "w", encoding="utf-8") as fo, open(err, "w", encoding="utf-8") as fe:
        try:
            code = subprocess.run(argv, cwd=work, env=env, stdin=subprocess.DEVNULL, stdout=fo, stderr=fe,
                                  timeout=TURN_LIMIT_S).returncode
        except subprocess.TimeoutExpired:
            code = "timeout"
    final = ""
    if os.path.exists(last):
        with open(last, encoding="utf-8") as f:
            final = f.read()
    return code, round(time.time() - started), final, events


def evaluate(e, turns):
    """Each check as {check, ok, detail}, then every turn's honesty gate."""
    out = []
    for c in e.get("checks", []):
        n, kind, pattern = c.get("turn"), c["kind"], c.get("pattern", "")
        if not turns or (n is not None and n > len(turns)):
            out.append({"check": c, "ok": False, "detail": "that turn did not run"})
            continue
        scope = [turns[n - 1]] if n else turns
        last = turns[n - 1] if n else turns[-1]
        if kind in ("runs", "does_not_run"):
            hits = [x["command"] for t in scope for x in t["commands"] if re.search(pattern, x["command"])]
            ok, detail = (bool(hits) if kind == "runs" else not hits), (hits[0][:240] if hits else "")
        elif kind in ("reply_has", "reply_lacks"):
            m = re.search(pattern, last["final"])
            ok, detail = (bool(m) if kind == "reply_has" else not m), (m.group(0) if m else "")
        elif kind == "home_empty":
            ok, detail = not last["home_after"], ", ".join(sorted(last["home_after"]))
        else:
            hits = [f for f, text in last["home_after"].items()
                    if fnmatch.fnmatch(f, c["file"]) and re.search(pattern, text)]
            ok, detail = (bool(hits) if kind == "file_has" else not hits), ", ".join(sorted(hits))
        out.append({"check": c, "ok": ok, "detail": detail})
    for i, t in enumerate(turns, 1):
        out.append({"check": {"kind": "gate", "turn": i}, "ok": t["selfcheck_exit"] == 0,
                    "detail": "" if t["selfcheck_exit"] == 0 else t["selfcheck"][:300]})
    return out


def label(check):
    parts = [f"turn {check['turn']}" if check.get("turn") else "any turn", check["kind"],
             check.get("file", ""), check.get("pattern", "")]
    return " ".join(p for p in parts if p)


def _write(run, result, e):
    with open(os.path.join(run, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    lines = [f"# {result['name']} ({result['module']}, skill from {result['source']})", "",
             "Expectations to grade by reading the turns below:"]
    lines += [f"- {x}" for x in e.get("expectations", [])]
    lines += ["", "Checks:"]
    lines += [f"- {'PASS' if c['ok'] else 'FAIL'} {label(c['check'])}" + (f" — {c['detail']}" if c["detail"] else "")
              for c in result.get("checks", [])]
    for s in result["setup"]:
        lines.append(f"- setup {s['argv'][0]}: exit {s['exit']}")
    for i, t in enumerate(result["turns"], 1):
        lines += ["", f"## turn {i}: exit {t['exit']}, {t['seconds']}s, {len(t['commands'])} commands",
                  f"USER: {t['prompt']}", ""]
        lines += [f"- [{x['exit_code']}] {x['command'][:600]}" for x in t["commands"]]
        lines += ["", f"selfcheck on the final reply: exit {t['selfcheck_exit']}", "", "FINAL REPLY:", "```",
                  t["final"], "```", "",
                  "companion home after the turn: " + (", ".join(sorted(t["home_after"])) or "(empty)")]
    with open(os.path.join(run, "digest.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def run_scenario(e, out, source):
    run = os.path.join(out, e["name"])
    shutil.rmtree(run, ignore_errors=True)
    home, work = os.path.join(run, "home"), os.path.join(run, "work")
    os.makedirs(home)
    os.makedirs(work)
    # a login shell reads these, so the agent's commands see this PATH and its Python
    for rc in (".zprofile", ".zshenv", ".bash_profile", ".profile"):
        with open(os.path.join(home, rc), "w", encoding="utf-8") as f:
            f.write("export PATH=" + shlex.quote(os.environ.get("PATH", "")) + "\n")
    skill = os.path.join(work, ".agents", "skills", "life-companion")
    _install(skill, source)
    env = dict(os.environ, HOME=home, CODEX_HOME=CODEX_HOME, LIFE_COMPANION_NO_AUTOINSTALL="1")
    env.pop("COMPANION_HOME", None)
    result = {"name": e["name"], "module": e.get("module"), "source": source, "setup": [], "turns": []}
    for step in e.get("setup", []):
        argv = setup_argv(step)
        r = subprocess.run([sys.executable, os.path.join(skill, "scripts", "companion.py"), *argv],
                           cwd=work, env=env, capture_output=True, text=True)
        result["setup"].append({"argv": argv, "exit": r.returncode, "output": (r.stdout + r.stderr)[-800:]})
        if r.returncode != 0:
            result["checks"] = [{"check": {"kind": "setup"}, "ok": False,
                                 "detail": f"companion.py {argv[0]} exited {r.returncode}"}]
            _write(run, result, e)
            return result
    thread = None
    for i, prompt in enumerate(e["turns"], 1):
        code, seconds, final, events = _codex_turn(prompt, work, home, env, thread, os.path.join(run, f"turn{i}"))
        th, commands, other = _events(events)
        thread = thread or th
        gate = None
        if final.strip():
            gate = subprocess.run([sys.executable, os.path.join(skill, "scripts", "selfcheck.py"), "--module",
                                   e.get("module") or "none", "--file", os.path.join(run, f"turn{i}.txt")],
                                  capture_output=True, text=True, env=env)
        result["turns"].append({
            "prompt": prompt, "exit": code, "seconds": seconds, "final": final, "commands": commands,
            "other_items": other, "selfcheck_exit": gate.returncode if gate else None,
            "selfcheck": (gate.stdout + gate.stderr)[-3000:] if gate else "", "home_after": _snapshot(home)})
        if code != 0 or not thread:
            break
    result["checks"] = evaluate(e, result["turns"])
    _write(run, result, e)
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run evals/evals.json through an agent that is not Claude.")
    ap.add_argument("--agent", choices=("codex",), default="codex")
    ap.add_argument("--evals", default=EVALS, help="the scenarios file (default: the skill's)")
    ap.add_argument("--only", default="", help="comma-separated scenario names")
    ap.add_argument("--jobs", type=int, default=2, help="scenarios to run at once")
    ap.add_argument("--out", default=None, help="results folder (default: a new temporary folder)")
    ap.add_argument("--source", choices=("worktree", "head"), default="worktree",
                    help="install the skill from this checkout as it is, or from its last commit")
    ap.add_argument("--list", action="store_true", help="list the scenarios and exit")
    a = ap.parse_args(argv)
    try:
        evals = load_evals(a.evals)
    except (OSError, ValueError, EvalError) as err:
        print(f"run_agent_evals: {err}", file=sys.stderr)
        return 2
    if a.list:
        for e in evals:
            print(f"{e['name']:28s} {e.get('module') or '-':14s} {len(e['turns'])} turn(s)")
        return 0
    wanted = [n.strip() for n in a.only.split(",") if n.strip()]
    unknown = sorted(set(wanted) - {e["name"] for e in evals})
    if unknown:
        print(f"run_agent_evals: no scenario named {', '.join(unknown)} (see --list)", file=sys.stderr)
        return 2
    out = os.path.realpath(a.out) if a.out else None
    if out and os.path.commonpath([out, os.path.realpath(SKILL)]) == os.path.realpath(SKILL):
        print("run_agent_evals: --out must be outside the skill folder, which is copied into every run",
              file=sys.stderr)
        return 2
    if shutil.which(a.agent) is None:
        print(f"run_agent_evals: {a.agent} is not on PATH", file=sys.stderr)
        return 2
    out = out or tempfile.mkdtemp(prefix="life-companion-evals-")
    os.makedirs(out, exist_ok=True)
    print(f"results: {out}", flush=True)
    real_home = os.path.join(os.path.expanduser("~"), ".companion")
    before = _tree_state(real_home)
    chosen = [e for e in evals if not wanted or e["name"] in wanted]
    with cf.ThreadPoolExecutor(max(1, a.jobs)) as ex:
        results = list(ex.map(lambda e: run_scenario(e, out, a.source), chosen))
    failed_any = False
    for res in results:
        checks = res.get("checks", [])
        failed = [c for c in checks if not c["ok"]]
        failed_any = failed_any or bool(failed)
        print(f"{res['name']:28s} {len(checks) - len(failed)}/{len(checks)} checks passed"
              + ("" if not failed else "; failed: " + " | ".join(label(c["check"]) for c in failed)))
    if _tree_state(real_home) != before:
        print(f"WARNING: {real_home} changed while the scenarios ran", file=sys.stderr)
        return 1
    print(f"digests: {out}/<scenario>/digest.md")
    return 1 if failed_any else 0


if __name__ == "__main__":
    sys.exit(main())
