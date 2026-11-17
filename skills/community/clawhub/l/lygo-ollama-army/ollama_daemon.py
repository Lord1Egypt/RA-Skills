#!/usr/bin/env python3
"""
LYGO Ollama Daemon — ClawHub-safe local roles only.

Queue-driven local Ollama helpers. No planting, no social outbound,
no stack mutators, no public HTTPS probes.
"""
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from ollama_client import chat, classify_and_summarize, is_ollama_ready, simple_draft_reply

HERE = Path(__file__).resolve().parent
QUEUE = HERE / "ollama_queue"
RESULTS = HERE / "ollama_results"
CC_TASKS = HERE / "ollama_command_center" / "tasks"
CC_RESULTS = HERE / "ollama_command_center" / "results"
CHAMPIONS_FILE = HERE / "champions.json"

# Explicit allowlist — anything else is refused
SAFE_ROLES = frozenset(
    {
        "hb-light",
        "memory-triage",
        "draft-simple",
        "draft",
        "classify",
        "general",
        "resonance-analyst",
        "champion-chat",
    }
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_dirs() -> None:
    for d in (QUEUE, RESULTS, CC_TASKS, CC_RESULTS):
        d.mkdir(parents=True, exist_ok=True)


def queue_dirs() -> list[Path]:
    dirs = [QUEUE]
    if CC_TASKS.is_dir():
        dirs.insert(0, CC_TASKS)
    return dirs


def write_result(stem: str, payload: dict) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    (RESULTS / f"{stem}.result.json").write_text(text, encoding="utf-8")
    CC_RESULTS.mkdir(parents=True, exist_ok=True)
    (CC_RESULTS / f"{stem}.result.json").write_text(text, encoding="utf-8")


def load_champions() -> dict[str, str]:
    if CHAMPIONS_FILE.is_file():
        try:
            data = json.loads(CHAMPIONS_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return {str(k): str(v) for k, v in data.items()}
        except (OSError, json.JSONDecodeError):
            pass
    return {
        "LYRA": "You are LYRA, a warm local LYGO-aligned assistant. Be truthful and concise.",
        "ARKOS": "You are ARKOS, a careful systems architect. Prefer clear structure.",
    }


def system_for(champion: str | None) -> str:
    if not champion:
        return "You are a helpful local LYGO-aligned assistant. Be concise."
    return load_champions().get(champion.upper(), f"You are {champion}, a local LYGO helper.")


def process_task(task: dict, model: str, champion: str | None = None) -> dict:
    role = str(task.get("role") or "general")
    payload = task.get("payload") if isinstance(task.get("payload"), dict) else {}
    out: dict = {
        "task_id": task.get("id", "unknown"),
        "role": role,
        "ts": utc_now(),
        "model": model,
        "signature": "Delta9Phi963-ARMY-DAEMON-v0.9.0",
    }
    if role not in SAFE_ROLES:
        out["ok"] = False
        out["result"] = {
            "gated": True,
            "reason": f"role not in SAFE_ROLES (ClawHub-safe army). refused: {role}",
        }
        return out

    system = system_for(champion or task.get("champion"))

    if role in ("draft", "draft-simple"):
        q = str(payload.get("query") or payload.get("prompt") or payload.get("text") or "")
        out["result"] = {"draft": simple_draft_reply(model, q)}
        out["ok"] = True
        return out

    if role == "memory-triage":
        text = str(payload.get("prompt") or payload.get("text") or "")
        out["result"] = classify_and_summarize(model, text, role="memory-triage")
        out["ok"] = True
        return out

    if role == "classify":
        text = str(payload.get("text") or payload.get("prompt") or "")
        out["result"] = classify_and_summarize(model, text, role="classify")
        out["ok"] = True
        return out

    if role == "resonance-analyst":
        # Advisory only — does not run external tools
        image_path = str(payload.get("image_path") or "")
        out["result"] = {
            "note": "Local advisory only. Use lygo-resonance skill separately if installed.",
            "image_path_hint": image_path[:200],
            "advice": chat(
                model,
                f"Give a short creative brief for sonifying/image-to-sound for: {image_path or 'an image'}",
                system=system,
                options={"temperature": 0.5, "num_predict": 120},
            ),
        }
        out["ok"] = True
        return out

    if role in ("hb-light", "general", "champion-chat"):
        prompt = str(payload.get("prompt") or payload.get("query") or payload.get("text") or "Say ready.")
        out["result"] = {
            "reply": chat(
                model,
                prompt,
                system=system,
                options={"temperature": 0.4, "num_predict": 160},
            )
        }
        out["ok"] = True
        return out

    out["ok"] = False
    out["result"] = {"gated": True, "reason": f"unhandled safe role {role}"}
    return out


def run_daemon(role: str, model: str, poll: float = 5.0, champion: str | None = None) -> None:
    if role not in SAFE_ROLES:
        print(f"REFUSE: role {role!r} not in SAFE_ROLES")
        return
    ensure_dirs()
    print(f"LYGO Ollama daemon | role={role} model={model} (local-only SAFE_ROLES)")
    while True:
        try:
            ollama_up = is_ollama_ready()
            by_name: dict[str, Path] = {}
            for qd in queue_dirs():
                for tf in sorted(qd.glob("*.task.json")):
                    by_name.setdefault(tf.name, tf)
            for tf in sorted(by_name.values(), key=lambda p: p.name):
                try:
                    if not tf.is_file():
                        continue
                    lock = tf.parent / f"{tf.stem}.lock"
                    try:
                        tf.replace(lock)
                    except OSError:
                        continue
                    task = json.loads(lock.read_text(encoding="utf-8"))
                    task_role = str(task.get("role") or "general")
                    # Only process matching role OR stack-worker style general safe queue
                    if task_role != role and role not in ("hb-light", "general"):
                        lock.replace(tf)
                        continue
                    if task_role not in SAFE_ROLES:
                        # Refuse and drop privileged queue items so they cannot pile up silently
                        write_result(
                            lock.stem,
                            {
                                "ok": False,
                                "task_id": task.get("id"),
                                "role": task_role,
                                "result": {"gated": True, "reason": "role not allowlisted in v0.9.0"},
                            },
                        )
                        lock.unlink(missing_ok=True)
                        for qd in queue_dirs():
                            (qd / tf.name).unlink(missing_ok=True)
                        print(f"[REFUSED] {task_role}")
                        continue
                    if not ollama_up:
                        lock.replace(tf)
                        continue
                    result = process_task(task, model, champion)
                    write_result(lock.stem, result)
                    lock.unlink(missing_ok=True)
                    for qd in queue_dirs():
                        (qd / tf.name).unlink(missing_ok=True)
                    print(f"[PROCESSED] {task.get('id')} role={task_role}")
                except FileNotFoundError:
                    continue
                except Exception as e:  # noqa: BLE001
                    print(f"[TASK ERR] {e}")
            time.sleep(poll)
        except KeyboardInterrupt:
            print("Daemon stopped.")
            break


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ollama_daemon")
    ap.add_argument("--role", required=True, choices=sorted(SAFE_ROLES))
    ap.add_argument("--model", default="llama3.2:1b")
    ap.add_argument("--poll", type=float, default=5.0)
    ap.add_argument("--champion", default=None)
    args = ap.parse_args(argv)
    run_daemon(args.role, args.model, args.poll, args.champion)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
