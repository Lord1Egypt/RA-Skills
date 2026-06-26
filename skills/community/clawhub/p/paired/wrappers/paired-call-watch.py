#!/usr/bin/env python3
"""paired-call-watch — Long-running watcher that auto-answers incoming calls.

Subscribes to ofono D-Bus signals. When a new VoiceCall enters state=incoming,
optionally auto-answers it (configurable per call: always / never / via hook).

Architecture:
  1. Listen for org.ofono.VoiceCallManager InterfacesAdded signals
  2. When a new VoiceCall1 appears with State=incoming, dispatch
  3. Optionally call a hook script (env vars BTCALL_*) for routing decisions
  4. If --auto-answer or hook returns 0, call ofono Answer() on the call
  5. Log all events to ${PAIRED_DATA_DIR}/call-events.jsonl

Usage:
  paired-call-watch --watch                       # foreground, log only (no auto-answer)
  paired-call-watch --watch --auto-answer         # foreground, auto-answer every call
  paired-call-watch --watch --hook /path/to/hook  # let hook decide (exit 0=answer, !=0=ignore)
  paired-call-watch --status                      # show daemon state
  paired-call-watch --last 10                     # show last 10 logged events

Hook env vars (when --hook is set):
  BTCALL_NUMBER         - calling number (e.g. '+447911123456')
  BTCALL_LINE_ID        - same, raw from LineIdentification
  BTCALL_NAME           - from Name field if available (often empty)
  BTCALL_TYPE           - 'incoming' (only state we trigger on)
  BTCALL_MODEM          - ofono modem path
  BTCALL_TIMESTAMP      - 20260427T215000

Hook exit code meaning:
  0 = answer the call
  1 = let it ring (don't auto-answer)
  2 = hang up immediately (reject)
"""
from __future__ import annotations
import os
import sys
import json
import time
import signal
import argparse
import logging
import subprocess
import threading
from pathlib import Path
from datetime import datetime, timezone

import dbus
import dbus.mainloop.glib
from gi.repository import GLib

OFONO_SERVICE = "org.ofono"
VOICECALL_IFACE = "org.ofono.VoiceCall"
VOICECALLMGR_IFACE = "org.ofono.VoiceCallManager"

LOG_DIR = Path.home() / "bt-skill-expansion"
EVENT_LOG = LOG_DIR / "call-events.jsonl"
PID_FILE = Path(f"/run/user/{os.getuid()}/paired-call-watch.pid")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [paired-call-watch] %(levelname)s: %(message)s")
log = logging.getLogger()


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def safe_str(v, default=""):
    if v is None:
        return default
    try:
        return str(v)
    except Exception:
        return default


def append_event_log(event: dict):
    try:
        EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with EVENT_LOG.open("a") as f:
            f.write(json.dumps(event) + "\n")
    except OSError as e:
        log.warning(f"event log write failed: {e}")


class CallWatcher:
    def __init__(self, auto_answer: bool, hook_cmd: str | None,
                 stop_after_first: bool = False):
        self.auto_answer = auto_answer
        self.hook_cmd = hook_cmd
        self.stop_after_first = stop_after_first
        self.bus = dbus.SystemBus()
        self.events_dispatched = 0
        self.stop_flag = threading.Event()
        # Track which call paths we've already processed so we don't double-fire
        # Path -> timestamp of last fire. Same path within DEDUPE_WINDOW_S = duplicate.
        self.seen_paths: dict = {}
        self.DEDUPE_WINDOW_S = 5.0

        # Subscribe to ofono's CallAdded signal on VoiceCallManager.
        # (Earlier code used InterfacesAdded but ofono does NOT implement
        #  org.freedesktop.DBus.ObjectManager - it has its own CallAdded
        #  signal that emits when a new VoiceCall object appears.)
        # The signal carries (object_path, properties_dict).
        self.bus.add_signal_receiver(
            self._on_call_added,
            signal_name="CallAdded",
            dbus_interface=VOICECALLMGR_IFACE,
            path_keyword="modem_path",
        )
        # Also subscribe to PropertyChanged for state transitions
        self.bus.add_signal_receiver(
            self._on_prop_changed,
            signal_name="PropertyChanged",
            dbus_interface=VOICECALL_IFACE,
            path_keyword="path",
        )
        log.info(
            f"Watching for incoming calls: auto_answer={auto_answer} "
            f"hook={'yes' if hook_cmd else 'no'}")

    def _on_iface_added(self, path, interfaces):
        if VOICECALL_IFACE not in interfaces:
            return
        props = interfaces[VOICECALL_IFACE]
        state = safe_str(props.get("State"))
        if state == "incoming":
            self._handle_incoming(str(path), props)

    def _on_call_added(self, call_path, properties, modem_path=None):
        """Fired by ofono when a new VoiceCall object appears on a modem.
        properties carries the same fields we'd otherwise read via GetProperties."""
        state = safe_str(properties.get("State"))
        log.info(f"CallAdded: path={call_path} state={state} modem={modem_path}")
        if state == "incoming":
            self._handle_incoming(str(call_path), properties)

    def _on_prop_changed(self, name, value, path=None):
        # Catch transitions to "incoming" if we missed the InterfacesAdded
        if str(name) != "State":
            return
        if str(value) != "incoming":
            return
        if not path:
            return
        # Time-windowed dedupe (matches _handle_incoming logic)
        if (time.time() - self.seen_paths.get(path, 0)) < self.DEDUPE_WINDOW_S:
            return
        # Read the call props
        try:
            obj = self.bus.get_object(OFONO_SERVICE, path)
            iface = dbus.Interface(obj, VOICECALL_IFACE)
            props = iface.GetProperties()
            self._handle_incoming(str(path), props)
        except dbus.DBusException as e:
            log.warning(f"could not read props for {path}: {e}")

    def _handle_incoming(self, path: str, props):
        # Time-windowed dedupe: same call_path within DEDUPE_WINDOW_S is a duplicate
        # (typically dual-modem firing the same logical call within ~milliseconds).
        # Outside the window it's a brand new call (ofono reuses voicecall01 path).
        now = time.time()
        last_seen = self.seen_paths.get(path, 0)
        if (now - last_seen) < self.DEDUPE_WINDOW_S:
            return
        self.seen_paths[path] = now
        # Garbage-collect entries older than 5 minutes to keep dict small
        cutoff = now - 300
        self.seen_paths = {p: t for p, t in self.seen_paths.items() if t > cutoff}

        line_id = safe_str(props.get("LineIdentification"))
        name = safe_str(props.get("Name"))
        # ofono modem path is the parent of the call path:
        # /hfp/org/bluez/hci0/dev_AABB../voicecall01 -> /hfp/org/bluez/hci0/dev_AABB..
        modem_path = "/".join(path.split("/")[:-1])

        log.info(f"INCOMING call from {line_id} ({name or '?'}) at {path}")

        event = {
            "received_at": now_iso(),
            "type": "incoming",
            "call_path": path,
            "modem_path": modem_path,
            "line_id": line_id,
            "name": name,
            "action": None,  # filled in below
        }

        decision = self._decide(event)
        event["action"] = decision

        if decision == "answer":
            ok = self._answer(path)
            event["answer_ok"] = ok
        elif decision == "hangup":
            ok = self._hangup(path)
            event["hangup_ok"] = ok
        else:
            event["note"] = "let it ring"

        append_event_log(event)
        self.events_dispatched += 1

        if self.stop_after_first:
            self.stop_flag.set()

    def _decide(self, event: dict) -> str:
        """Returns 'answer', 'hangup', or 'ignore'."""
        if self.hook_cmd:
            # Hook decides via exit code
            env = os.environ.copy()
            env.update({
                "BTCALL_NUMBER": event["line_id"],
                "BTCALL_LINE_ID": event["line_id"],
                "BTCALL_NAME": event["name"],
                "BTCALL_TYPE": "incoming",
                "BTCALL_MODEM": event["modem_path"],
                "BTCALL_TIMESTAMP": datetime.now().strftime("%Y%m%dT%H%M%S"),
            })
            try:
                p = subprocess.run(
                    self.hook_cmd, shell=True, env=env, timeout=10,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                rc = p.returncode
                log.info(f"Hook exit {rc} (0=answer, 1=ignore, 2=hangup)")
                if rc == 0:
                    return "answer"
                elif rc == 2:
                    return "hangup"
                else:
                    return "ignore"
            except (OSError, subprocess.TimeoutExpired) as e:
                log.warning(f"Hook failed: {e}; defaulting to ignore")
                return "ignore"
        if self.auto_answer:
            return "answer"
        return "ignore"

    def _answer(self, call_path: str) -> bool:
        try:
            obj = self.bus.get_object(OFONO_SERVICE, call_path)
            iface = dbus.Interface(obj, VOICECALL_IFACE)
            iface.Answer()
            log.info(f"Answered {call_path}")
            return True
        except dbus.DBusException as e:
            log.error(f"Answer failed: {e}")
            return False

    def _hangup(self, call_path: str) -> bool:
        try:
            obj = self.bus.get_object(OFONO_SERVICE, call_path)
            iface = dbus.Interface(obj, VOICECALL_IFACE)
            iface.Hangup()
            log.info(f"Hung up {call_path}")
            return True
        except dbus.DBusException as e:
            log.error(f"Hangup failed: {e}")
            return False


def cmd_status() -> int:
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            if Path(f"/proc/{pid}").is_dir():
                print(f"paired-call-watch is running (pid {pid})")
            else:
                print(f"pid file exists ({pid}) but process gone (stale)")
        except (OSError, ValueError):
            print("pid file unreadable")
    else:
        print("paired-call-watch is NOT running")
    if EVENT_LOG.exists():
        try:
            lines = EVENT_LOG.read_text().splitlines()
            print(f"\nEvent log: {EVENT_LOG} ({len(lines)} events)")
            if lines:
                last = json.loads(lines[-1])
                print(f"Last: {last.get('received_at')} from {last.get('line_id')} -> {last.get('action')}")
        except (OSError, json.JSONDecodeError):
            pass
    return 0


def cmd_last(n: int) -> int:
    if not EVENT_LOG.exists():
        print("No events logged yet.")
        return 0
    try:
        lines = EVENT_LOG.read_text().splitlines()
    except OSError as e:
        print(f"Cannot read log: {e}", file=sys.stderr)
        return 1
    for ln in lines[-n:]:
        try:
            e = json.loads(ln)
            print(f"{e.get('received_at')} from {e.get('line_id')} ({e.get('name','?')}) -> {e.get('action')}")
        except json.JSONDecodeError:
            print(f"  (malformed): {ln[:80]}")
    return 0


def cmd_watch(args) -> int:
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        PID_FILE.write_text(str(os.getpid()))
    except OSError:
        pass

    watcher = CallWatcher(args.auto_answer, args.hook, args.once)
    loop = GLib.MainLoop()

    def shutdown(signum, frame):
        log.info(f"Caught signal {signum}, shutting down")
        watcher.stop_flag.set()
        try:
            PID_FILE.unlink(missing_ok=True)
        except OSError:
            pass
        loop.quit()

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    log.info(f"Watching - events log: {EVENT_LOG}")
    if args.once:
        log.info("Will exit after first incoming call")

    def stop_watcher():
        while not watcher.stop_flag.is_set():
            time.sleep(0.5)
        loop.quit()

    threading.Thread(target=stop_watcher, daemon=True).start()

    try:
        loop.run()
    finally:
        try:
            PID_FILE.unlink(missing_ok=True)
        except OSError:
            pass

    log.info(f"Exiting. Events dispatched: {watcher.events_dispatched}")
    return 0


def main():
    p = argparse.ArgumentParser(
        description="Watch for incoming calls and optionally auto-answer.")
    p.add_argument("--auto-answer", action="store_true",
                   help="Answer every incoming call automatically")
    p.add_argument("--hook",
                   help="Shell command to decide. Exit: 0=answer 1=ignore 2=hangup")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--watch", action="store_true", help="Foreground daemon")
    g.add_argument("--once", action="store_true",
                   help="Exit after first incoming call")
    g.add_argument("--status", action="store_true")
    g.add_argument("--last", type=int, metavar="N")
    args = p.parse_args()

    if args.status:
        return cmd_status()
    if args.last is not None:
        return cmd_last(args.last)
    return cmd_watch(args)


if __name__ == "__main__":
    sys.exit(main())
