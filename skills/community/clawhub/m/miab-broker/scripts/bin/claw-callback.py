#!/usr/bin/env python3
"""
claw-callback — file-based callback/continuation registry for the OpenClaw agent ensemble.

Lets a delegating agent yield instead of blocking: it packages a compact "resume"
context (what to do when woken), fires the delegation, and ends its turn. The
finishing agent wakes the next agent in the return stack via the agent-to-agent
message tool, forwarding the whole envelope so prior callbacks travel with the work.

State: one JSON envelope per callback in <root>/state/callbacks/, plus an append-only
ledger.jsonl. Completed envelopes are deleted (cleanup-on-completion); a one-line
summary is kept in the ledger for audit.

Model: a LIFO return stack. Each frame is an agent waiting to be resumed, with the
compact context it needs. Delegating pushes a frame; finishing pops the top frame and
wakes that agent. See CALLBACKS.md for the full protocol.

Subcommands:
  create   originator delegates work, registers a callback         (push origin frame)
  forward  a holder delegates further, packaging prior callbacks   (push another frame)
  return   the current holder finishes, wakes the next agent       (pop top frame)
  resolve  the origin completes the whole task; clean up           (delete + ledger)
  show     print one envelope
  list     list active envelopes
  sweep    find/fail stale orphaned callbacks (safety net)

All mutating subcommands print a JSON object to stdout for the agent to act on.
"""

import argparse
import datetime as _dt
import json
import os
import secrets
import sys
from pathlib import Path
from typing import Optional

VERSION = 1


# --------------------------------------------------------------------------- paths
def root_dir() -> Path:
    """Resolve the .openclaw root. CLAW_HOME wins, else standard default ~/.openclaw."""
    env = os.environ.get("CLAW_HOME")
    if env:
        return Path(env).expanduser()
    return Path("~/.openclaw").expanduser()


def cb_dir() -> Path:
    d = root_dir() / "state" / "callbacks"
    d.mkdir(parents=True, exist_ok=True)
    return d


def ledger_path() -> Path:
    return cb_dir() / "ledger.jsonl"


def registry_path() -> Path:
    return cb_dir() / "agent-registry.json"


def load_registry() -> dict:
    """Load agent registry; return empty structure if missing."""
    p = registry_path()
    if not p.exists():
        return {"version": 1, "agents": {}}
    try:
        return json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return {"version": 1, "agents": {}}


def save_registry(reg: dict) -> None:
    reg["updatedAt"] = now_iso()
    p = registry_path()
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(reg, indent=2, ensure_ascii=False))
    tmp.replace(p)


def lookup_agent(logical_name: str) -> Optional[dict]:
    """Return the registry entry for a logical agent name, or None if not found."""
    reg = load_registry()
    return reg.get("agents", {}).get(logical_name)


def envelope_path(cid: str) -> Path:
    return cb_dir() / f"{cid}.json"


# --------------------------------------------------------------------------- helpers
def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_id() -> str:
    stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%d%H%M%S")
    suffix = secrets.token_hex(3)   # 3 bytes = 6 hex chars, cryptographically random
    return f"cb-{stamp}-{suffix}"


def load(cid: str) -> dict:
    p = envelope_path(cid)
    if not p.exists():
        die(f"no such callback: {cid} (looked in {p})")
    return json.loads(p.read_text())


def save(env: dict) -> Path:
    """Atomic write."""
    env["updatedAt"] = now_iso()
    p = envelope_path(env["id"])
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(env, indent=2, ensure_ascii=False))
    tmp.replace(p)
    return p


def ledger_append(record: dict) -> None:
    record = {"at": now_iso(), **record}
    with ledger_path().open("a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def rotate_ledger_if_needed(max_lines: int = 10_000) -> bool:
    """Rotate ledger.jsonl if it exceeds max_lines. Returns True if rotated."""
    p = ledger_path()
    if not p.exists():
        return False
    try:
        # O(n) scan; acceptable since sweep is infrequent and max_lines bounds the cost
        text = p.read_text(encoding="utf-8")
    except OSError:
        return False
    line_count = sum(1 for line in text.splitlines() if line.strip())
    if line_count < max_lines:
        return False
    stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%d%H%M%S")
    archive = p.with_name(f"ledger.{stamp}.jsonl")
    # Handle same-second double-sweep collision
    n = 1
    while archive.exists():
        archive = p.with_name(f"ledger.{stamp}.{n}.jsonl")
        n += 1
    try:
        p.rename(archive)
    except OSError:
        return False
    return True


def emit(obj: dict) -> None:
    """Machine-readable result for the calling agent."""
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def _purge(cid: str, env: dict) -> bool:
    """Delete a finished envelope. If the FS blocks unlink, mark it resolved in
    place so it never lingers as 'pending'. Returns True if the file was removed."""
    p = envelope_path(cid)
    try:
        p.unlink(missing_ok=True)
        return True
    except OSError:
        env["status"] = env.get("status", "resolved")
        try:
            save(env)
        except OSError:
            pass
        return False


def die(msg: str, code: int = 1):
    print(json.dumps({"ok": False, "error": msg}), file=sys.stderr)
    sys.exit(code)


def build_resume(args) -> dict:
    """Assemble the compact continuation context from flags / json / file."""
    if getattr(args, "resume_file", None):
        return json.loads(Path(args.resume_file).expanduser().read_text())
    if getattr(args, "resume_json", None):
        return json.loads(args.resume_json)
    resume = {}
    if args.summary:
        resume["summary"] = args.summary
    if args.step:
        resume["steps"] = list(args.step)
    if args.expects:
        resume["expects"] = args.expects
    if args.integrate:
        resume["integrate"] = args.integrate
    if not resume:
        die("a resume context is required: use --summary/--step/--expects/--integrate, "
            "or --resume-json, or --resume-file")
    return resume


def wake_message(cid: str, target: str, resume: dict, results: list, terminal: bool) -> str:
    """The exact text the finishing agent should send to `target` via agent-to-agent."""
    last = results[-1] if results else None
    lines = [
        f"RESUME callback://{cid}",
        f"You were waiting on delegated work; it's back. Reload your context with:",
        f"  python3 Skills/miab-broker/scripts/bin/claw-callback.py show --id {cid}",
        "",
        "Your resume context:",
        f"  summary : {resume.get('summary','-')}",
    ]
    steps = resume.get("steps") or []
    if steps:
        lines.append("  steps   :")
        lines += [f"    {i+1}. {s}" for i, s in enumerate(steps)]
    if resume.get("expects"):
        lines.append(f"  expects : {resume['expects']}")
    if resume.get("integrate"):
        lines.append(f"  integrate: {resume['integrate']}")
    if last:
        lines += ["", f"Latest result from {last['from']}:", f"  {last['result']}"]
        if last.get("artifacts"):
            lines.append(f"  artifacts: {', '.join(last['artifacts'])}")
    if terminal:
        lines += ["", "This is the ORIGIN frame — finish the overall task, then run:",
                  f"  python3 Skills/miab-broker/scripts/bin/claw-callback.py resolve --id {cid} --from {target}"]
    else:
        lines += ["", "When you finish your part, hand back with `return` (or `forward` to delegate again)."]
    return "\n".join(lines)


# --------------------------------------------------------------------------- commands
def cmd_register(args):
    """Register or update an agent's routing info in the registry."""
    reg = load_registry()
    agents = reg.setdefault("agents", {})
    entry = agents.get(args.agent, {})
    entry["agentId"] = args.agent_id
    if args.description:
        entry["description"] = args.description
    entry["updatedAt"] = now_iso()
    agents[args.agent] = entry
    save_registry(reg)
    emit({
        "ok": True,
        "agent": args.agent,
        "agentId": args.agent_id,
        "next_step": (f"Agent '{args.agent}' registered with agentId '{args.agent_id}'. "
                      f"Future `return` and `wake` calls targeting this agent will use "
                      f"cron(action=wake, agentId='{args.agent_id}')."),
    })


def cmd_wake(args):
    """Look up the target agent and emit the exact cron call to wake them."""
    env = load(args.id)

    # Determine target: either --to override, or the current holder
    target_name = args.to or env.get("holder")
    if not target_name:
        die(f"Cannot determine wake target: no --to and no holder in envelope {args.id}")

    entry = lookup_agent(target_name)

    # Build the dispatch message (either from envelope's active frame or a fresh prompt)
    active = env.get("active")
    results = env.get("results", [])

    if active:
        terminal = len(env.get("stack", [])) == 0
        msg = wake_message(args.id, target_name, active["resume"], results, terminal)
    else:
        # No active frame yet: this is a delegation (create/forward), not a resume.
        # Emit a new-task assignment carrying the callback ref + the task text, matching
        # the inline next_step that `create` prints.
        msg = (f"[New Task] callback://{args.id} - {env.get('task', '(no task description)')}\n"
               f"You have been delegated work. Load full context with:\n"
               f"  python3 ~/.openclaw/scripts/claw-callback.py show --id {args.id}\n"
               f"When done, `return` (or `forward` to delegate further) — pass callback://{args.id} along.")

    if entry:
        agent_id = entry["agentId"]
        emit({
            "ok": True,
            "id": args.id,
            "wake_agent": target_name,
            "agentId": agent_id,
            "dispatch_message": msg,
            "next_step": (
                f"Call the cron tool with: action=wake, agentId='{agent_id}', "
                f"text=<dispatch_message above>. Then END YOUR TURN."
            ),
        })
    else:
        # Registry miss -- emit fallback instructions
        emit({
            "ok": False,
            "id": args.id,
            "wake_agent": target_name,
            "agentId": None,
            "dispatch_message": msg,
            "registry_miss": True,
            "next_step": (
                f"Agent '{target_name}' is not in the registry "
                f"(~/.openclaw/state/callbacks/agent-registry.json). "
                f"Either: (a) register them first with "
                f"`python3 ~/.openclaw/scripts/claw-callback.py register "
                f"--agent {target_name} --agent-id <their agentId>`, "
                f"then retry `wake`, OR (b) manually call "
                f"cron(action=wake, agentId=<their agentId>, text=<dispatch_message above>). "
                f"The dispatch_message is ready above."
            ),
        })


def cmd_create(args):
    resume = build_resume(args)
    cid = new_id()
    env = {
        "id": cid,
        "version": VERSION,
        "status": "pending",
        "task": args.task,
        "createdBy": args.frm,
        "holder": args.to,
        "createdAt": now_iso(),
        "updatedAt": now_iso(),
        "stack": [{"agent": args.frm, "resume": resume, "pushedAt": now_iso()}],
        "active": None,
        "results": [],
        "history": [{"at": now_iso(), "agent": args.frm, "action": "create",
                     "detail": f"delegate -> {args.to}"}],
    }
    save(env)
    ledger_append({"id": cid, "event": "create", "by": args.frm, "to": args.to, "task": args.task})
    emit({
        "ok": True, "id": cid, "ref": f"callback://{cid}", "file": str(envelope_path(cid)),
        "holder": args.to, "stack_depth": 1,
        "next_step": (
            f"Dispatch the task to '{args.to}' by calling: "
            f"cron(action=wake, agentId=<{args.to}'s agentId from registry>, "
            f"text='[New Task] callback://{cid} - {args.task}'). "
            f"Or use `python3 Skills/miab-broker/scripts/bin/claw-callback.py wake --id {cid} --to {args.to}` "
            f"to get the exact call. Then END YOUR TURN."
        ),
    })


def cmd_forward(args):
    env = load(args.id)
    if env["status"] != "pending":
        die(f"callback {args.id} is {env['status']}, cannot forward")
    if env["holder"] != args.frm:
        # not fatal: log it, the holder may have changed legitimately
        env["history"].append({"at": now_iso(), "agent": args.frm, "action": "forward-warn",
                               "detail": f"forwarder {args.frm} != recorded holder {env['holder']}"})
    resume = build_resume(args)
    env["stack"].append({"agent": args.frm, "resume": resume, "pushedAt": now_iso()})
    env["holder"] = args.to
    env["history"].append({"at": now_iso(), "agent": args.frm, "action": "forward",
                           "detail": f"delegate -> {args.to}"})
    save(env)
    ledger_append({"id": args.id, "event": "forward", "by": args.frm, "to": args.to})
    emit({
        "ok": True, "id": args.id, "ref": f"callback://{args.id}", "holder": args.to,
        "stack_depth": len(env["stack"]),
        "next_step": (
            f"Dispatch to '{args.to}' via cron(action=wake, agentId=<{args.to}'s agentId>, "
            f"text='[New Task] callback://{args.id} - forwarded from {args.frm}'). "
            f"Use `wake --id {args.id} --to {args.to}` for the exact call. "
            f"Your callback is packaged on the stack. END YOUR TURN."
        ),
    })


def cmd_return(args):
    env = load(args.id)
    if env["status"] != "pending":
        die(f"callback {args.id} is {env['status']}, cannot return")
    env["results"].append({
        "from": args.frm, "result": args.result,
        "artifacts": list(args.artifact or []), "at": now_iso(),
    })
    if not env["stack"]:
        die(f"callback {args.id} has an empty stack; nothing to wake. Run resolve instead.")
    frame = env["stack"].pop()
    env["active"] = frame
    env["holder"] = frame["agent"]
    terminal = len(env["stack"]) == 0
    env["history"].append({"at": now_iso(), "agent": args.frm, "action": "return",
                           "detail": f"wake -> {frame['agent']}" + (" (origin)" if terminal else "")})
    save(env)
    ledger_append({"id": args.id, "event": "return", "by": args.frm, "wake": frame["agent"]})

    # Look up wake target in registry
    entry = lookup_agent(frame["agent"])
    if entry:
        wake_instruction = (
            f"Call the cron tool with: action=wake, agentId='{entry['agentId']}', "
            f"text=<dispatch_message above>. Then END YOUR TURN."
        )
        wake_agent_id = entry["agentId"]
    else:
        wake_instruction = (
            f"Agent '{frame['agent']}' is not in the registry. "
            f"Run: python3 Skills/miab-broker/scripts/bin/claw-callback.py wake --id {args.id} "
            f"for guidance after registering them. "
            f"Or manually call cron(action=wake, agentId=<their agentId>, text=<dispatch_message>)."
        )
        wake_agent_id = None

    emit({
        "ok": True, "id": args.id, "ref": f"callback://{args.id}",
        "wake": frame["agent"], "wake_agentId": wake_agent_id, "terminal": terminal,
        "resume": frame["resume"], "results_so_far": env["results"],
        "dispatch_message": wake_message(args.id, frame["agent"], frame["resume"],
                                         env["results"], terminal),
        "next_step": wake_instruction,
    })


def cmd_resolve(args):
    env = load(args.id)
    if args.result:
        env["results"].append({"from": args.frm, "result": args.result,
                               "artifacts": [], "at": now_iso()})
    env["status"] = "resolved"
    env["history"].append({"at": now_iso(), "agent": args.frm, "action": "resolve"})
    ledger_append({
        "id": args.id, "event": "resolve", "by": args.frm,
        "task": env.get("task"), "hops": len(env.get("results", [])),
        "result": env["results"][-1]["result"] if env.get("results") else None,
    })
    # cleanup-on-completion: delete the active envelope, keep the ledger line.
    cleaned = _purge(args.id, env)
    emit({"ok": True, "id": args.id, "status": "resolved", "cleaned_up": cleaned,
          "ledger": str(ledger_path()),
          "next_step": "Callback complete" + (" and envelope removed." if cleaned else
                       " (envelope marked resolved in place; delete blocked by filesystem).")
                       + " Report the final result to the user/channel."})


def cmd_show(args):
    env = load(args.id)
    if args.json:
        emit(env)
        return
    print(f"callback://{env['id']}  [{env['status']}]")
    print(f"  task    : {env.get('task')}")
    print(f"  holder  : {env.get('holder')}   createdBy: {env.get('createdBy')}")
    print(f"  updated : {env.get('updatedAt')}")
    if env.get("active"):
        a = env["active"]
        print(f"  ACTIVE resume frame (agent={a['agent']}):")
        print(f"    summary : {a['resume'].get('summary','-')}")
        for i, s in enumerate(a["resume"].get("steps", [])):
            print(f"    step {i+1} : {s}")
        if a["resume"].get("expects"):
            print(f"    expects : {a['resume']['expects']}")
        if a["resume"].get("integrate"):
            print(f"    integrate: {a['resume']['integrate']}")
    print(f"  stack   : {len(env.get('stack', []))} frame(s) waiting "
          f"({', '.join(f['agent'] for f in env.get('stack', [])) or 'none'})")
    if env.get("results"):
        print("  results :")
        for r in env["results"]:
            print(f"    - {r['from']}: {r['result']}"
                  + (f"  [artifacts: {', '.join(r['artifacts'])}]" if r.get("artifacts") else ""))


def cmd_list(args):
    rows = []
    for p in sorted(cb_dir().glob("cb-*.json")):
        try:
            e = json.loads(p.read_text())
        except Exception:
            continue
        rows.append(e)
    if args.json:
        emit({"ok": True, "count": len(rows), "callbacks": rows})
        return
    if not rows:
        print("No active callbacks.")
        return
    print(f"{'ID':<28} {'STATUS':<9} {'HOLDER':<10} {'STACK':<6} TASK")
    for e in rows:
        print(f"{e['id']:<28} {e['status']:<9} {e.get('holder','-'):<10} "
              f"{len(e.get('stack', [])):<6} {(e.get('task') or '')[:48]}")


def cmd_sweep(args):
    """Safety net: find pending callbacks older than N minutes (orphans)."""
    # Rotate ledger if it has grown too large
    rotated = rotate_ledger_if_needed()
    cutoff = _dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(minutes=args.older_than)
    stale = []
    for p in sorted(cb_dir().glob("cb-*.json")):
        try:
            e = json.loads(p.read_text())
        except Exception:
            continue
        if e.get("status") != "pending":
            continue
        updated = _dt.datetime.strptime(e["updatedAt"], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=_dt.timezone.utc)
        if updated < cutoff:
            stale.append(e)
            if args.fail:
                e["status"] = "failed"
                e["history"].append({"at": now_iso(), "agent": "sweep", "action": "fail",
                                     "detail": f"stale > {args.older_than}m"})
                ledger_append({"id": e["id"], "event": "fail", "by": "sweep",
                               "reason": f"stale>{args.older_than}m", "holder": e.get("holder")})
                _purge(e["id"], e)
    emit({"ok": True, "stale_count": len(stale), "failed": bool(args.fail),
          "ledger_rotated": rotated,
          "stale": [{"id": e["id"], "holder": e.get("holder"), "task": e.get("task"),
                     "updatedAt": e["updatedAt"]} for e in stale]})


# --------------------------------------------------------------------------- parser
def add_resume_flags(p):
    p.add_argument("--summary", help="one-line: why you delegated / what you're waiting for")
    p.add_argument("--step", action="append", help="an ordered next-action on wake (repeatable)")
    p.add_argument("--expects", help="the artifact/result you need back")
    p.add_argument("--integrate", help="how to fold the returned result into your work")
    p.add_argument("--resume-json", help="full resume object as a JSON string")
    p.add_argument("--resume-file", help="path to a JSON file with the resume object")


def main():
    ap = argparse.ArgumentParser(prog="claw-callback", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create", help="register a callback and delegate")
    c.add_argument("--task", required=True, help="short description of the overall delegated work")
    c.add_argument("--from", dest="frm", required=True, help="your agent id (the originator)")
    c.add_argument("--to", required=True, help="agent id you are delegating to")
    add_resume_flags(c)
    c.set_defaults(func=cmd_create)

    f = sub.add_parser("forward", help="delegate further, packaging prior callbacks")
    f.add_argument("--id", required=True)
    f.add_argument("--from", dest="frm", required=True, help="your agent id (current holder)")
    f.add_argument("--to", required=True, help="agent id you are delegating to next")
    add_resume_flags(f)
    f.set_defaults(func=cmd_forward)

    r = sub.add_parser("return", help="finish your part and wake the next agent")
    r.add_argument("--id", required=True)
    r.add_argument("--from", dest="frm", required=True, help="your agent id (finishing holder)")
    r.add_argument("--result", required=True, help="what you produced / your answer")
    r.add_argument("--artifact", action="append", help="path/url of an output (repeatable)")
    r.set_defaults(func=cmd_return)

    rs = sub.add_parser("resolve", help="origin completes the whole task; clean up")
    rs.add_argument("--id", required=True)
    rs.add_argument("--from", dest="frm", required=True, help="your agent id (the origin)")
    rs.add_argument("--result", help="optional final result note for the ledger")
    rs.set_defaults(func=cmd_resolve)

    sh = sub.add_parser("show", help="print one envelope")
    sh.add_argument("--id", required=True)
    sh.add_argument("--json", action="store_true")
    sh.set_defaults(func=cmd_show)

    ls = sub.add_parser("list", help="list active callbacks")
    ls.add_argument("--json", action="store_true")
    ls.set_defaults(func=cmd_list)

    sw = sub.add_parser("sweep", help="find/fail stale orphaned callbacks")
    sw.add_argument("--older-than", type=int, default=120, help="minutes (default 120)")
    sw.add_argument("--fail", action="store_true", help="mark stale as failed and clean up")
    sw.set_defaults(func=cmd_sweep)

    reg_p = sub.add_parser("register", help="register or update an agent's routing info")
    reg_p.add_argument("--agent", required=True,
                       help="logical agent name (e.g. 'main', 'coder', 'planner')")
    reg_p.add_argument("--agent-id", required=True, dest="agent_id",
                       help="persistent routing agentId for cron(action=wake) "
                            "(e.g. 'agent:main', NOT a transient sessionId)")
    reg_p.add_argument("--description", help="human-readable description of this agent")
    reg_p.set_defaults(func=cmd_register)

    wk = sub.add_parser("wake", help="emit the exact cron call to wake the target agent")
    wk.add_argument("--id", required=True, help="callback id")
    wk.add_argument("--to", help="override target agent (default: current holder)")
    wk.set_defaults(func=cmd_wake)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
