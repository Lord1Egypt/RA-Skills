#!/usr/bin/env python3
import json
import shlex
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR = SCRIPT_DIR / "validate_cron_spec.py"


def load_spec(path_arg: str | None):
    if path_arg and path_arg != "-":
        return json.loads(Path(path_arg).read_text())
    return json.load(sys.stdin)


def shell_join(parts: list[str]) -> str:
    return " \\\n  ".join(shlex.quote(p) for p in parts)


def add_opt(parts: list[str], flag: str, value):
    if value is None:
        return
    if isinstance(value, bool):
        if value:
            parts.append(flag)
        return
    text = str(value)
    if text.strip():
        parts.extend([flag, text])


def run_validator(spec: dict):
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), "-"],
        input=json.dumps(spec),
        text=True,
        capture_output=True,
    )
    if proc.stdout:
        try:
            return proc.returncode, json.loads(proc.stdout)
        except Exception:
            return proc.returncode, {"ok": False, "issues": [proc.stdout.strip()], "warnings": []}
    return proc.returncode, {"ok": proc.returncode == 0, "issues": [], "warnings": []}


def main():
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        spec = load_spec(path_arg)
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"failed to load spec: {e}"}, ensure_ascii=False))
        raise SystemExit(2)

    rc, validation = run_validator(spec)
    if rc != 0:
        print(json.dumps({"ok": False, "validation": validation}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    parts = ["openclaw", "cron", "add"]
    add_opt(parts, "--name", spec.get("name"))
    add_opt(parts, "--description", spec.get("description"))
    add_opt(parts, "--agent", spec.get("agentId"))
    add_opt(parts, "--session-key", spec.get("sessionKey"))

    schedule = spec["schedule"]
    kind = schedule["kind"]
    if kind == "at":
        add_opt(parts, "--at", schedule.get("at"))
    elif kind == "every":
        every_ms = schedule.get("everyMs")
        add_opt(parts, "--every", f"{every_ms}ms")
    elif kind == "cron":
        add_opt(parts, "--cron", schedule.get("expr"))
        add_opt(parts, "--tz", schedule.get("tz"))

    add_opt(parts, "--session", spec.get("sessionTarget"))
    add_opt(parts, "--wake", spec.get("wakeMode"))

    payload = spec["payload"]
    if payload["kind"] == "systemEvent":
        add_opt(parts, "--system-event", payload.get("text"))
    else:
        add_opt(parts, "--message", payload.get("message"))
        add_opt(parts, "--model", payload.get("model"))
        add_opt(parts, "--thinking", payload.get("thinking"))
        add_opt(parts, "--timeout-seconds", payload.get("timeoutSeconds"))
        add_opt(parts, "--light-context", payload.get("lightContext"))

    if spec.get("deleteAfterRun") is True:
        parts.append("--delete-after-run")
    elif spec.get("deleteAfterRun") is False:
        parts.append("--keep-after-run")

    delivery = spec.get("delivery")
    if isinstance(delivery, dict):
        mode = delivery.get("mode")
        if mode == "announce":
            parts.append("--announce")
            add_opt(parts, "--channel", delivery.get("channel"))
            add_opt(parts, "--to", delivery.get("to"))
            add_opt(parts, "--account", delivery.get("accountId"))
            add_opt(parts, "--best-effort-deliver", delivery.get("bestEffort"))
        elif mode == "none":
            parts.append("--no-deliver")
        elif mode == "webhook":
            # Current CLI has no first-class --webhook flag on cron add.
            # Emit structured note so caller can use tool/API or follow-up edit path.
            print(
                json.dumps(
                    {
                        "ok": True,
                        "warning": "webhook delivery is better created via cron tool/API JSON payload than raw CLI flags",
                        "validation": validation,
                        "command": shell_join(parts),
                        "delivery": delivery,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            raise SystemExit(0)

    print(
        json.dumps(
            {
                "ok": True,
                "validation": validation,
                "command": shell_join(parts),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
