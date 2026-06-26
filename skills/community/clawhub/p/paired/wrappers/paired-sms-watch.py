#!/usr/bin/env python3
"""
paired-sms-watch v2 — long-running MAP-MNS push notification listener.

Watches for new SMS/MMS arriving on a paired phone via Bluetooth MAP-MNS.
When a new message hits the phone's inbox, BlueZ surfaces it as an
`org.bluez.obex.Message1` D-Bus object on the session bus. We subscribe to
`InterfacesAdded` signals and dispatch on each new message.

v2 enhancement over v1:
  - When InterfacesAdded fires with empty/sparse props (the MNS "notification"
    stub case), we call Message1.Get() to fetch the bMessage envelope, then
    parse it to extract sender, subject, body. This means the Telegram hook
    receives real data instead of "(empty)".

Architecture:
  1. Open OBEX MAP session to phone (target=00001132...).
  2. Phone-side opens reverse OBEX MNS session (target=BB582B41...).
  3. Navigate to /telecom/msg/inbox - this primes MNS notifications.
  4. Subscribe to ObjectManager.InterfacesAdded for org.bluez.obex.Message1.
  5. Filter for new (Read=False, Sent=False, Folder=/telecom/msg/inbox).
  6. If sender/subject empty -> Get() the bMessage, parse for real values.
  7. Log to JSONL at ${PAIRED_DATA_DIR}/sms-events.jsonl.
  8. Run optional hook command (e.g. Telegram/HA notify).
  9. Heartbeat keepalive: if session goes stale, recreate.

Usage:
  paired-sms-watch --watch              # foreground daemon
  paired-sms-watch --once               # exit after first new SMS
  paired-sms-watch --status             # session state, recent events
  paired-sms-watch --last 10            # show last 10 logged events
  paired-sms-watch --hook CMD           # exec CMD on each event (env vars set)
  paired-sms-watch --phone MAC          # specific phone (default: first paired)
  paired-sms-watch --print-events-only  # log only, don't dispatch hook

Hook env vars (when --hook is set):
  BTSMS_SENDER         - '<contact-1>' (vCard FN, or Sender prop)
  BTSMS_SENDER_ADDR    - '+07911123456' (vCard TEL, or SenderAddress prop)
  BTSMS_SUBJECT        - first ~80 chars of message body
  BTSMS_BODY           - full message body (from bMessage MSG section)
  BTSMS_TIMESTAMP      - 20260427T192534
  BTSMS_TYPE           - sms-gsm | mms
  BTSMS_FOLDER         - /telecom/msg/inbox
  BTSMS_SOURCE         - 'props' | 'bmessage' (where the data came from)
"""
from __future__ import annotations
import os
import re
import sys
import json
import time
import signal
import argparse
import logging
import subprocess
import threading
import tempfile
from pathlib import Path
from datetime import datetime, timezone

import dbus
import dbus.mainloop.glib
from gi.repository import GLib

OBEX_BUS = "org.bluez.obex"
OBEX_PATH = "/org/bluez/obex"
CLIENT_IFACE = "org.bluez.obex.Client1"
MAP_IFACE = "org.bluez.obex.MessageAccess1"
MSG_IFACE = "org.bluez.obex.Message1"

LOG_DIR = Path.home() / "bt-skill-expansion"
EVENT_LOG = LOG_DIR / "sms-events.jsonl"
SEEN_DB = LOG_DIR / "sms-seen.db"
PID_FILE = Path(f"/run/user/{os.getuid()}/paired-sms-watch.pid")
BMSG_TMP_DIR = LOG_DIR / "bmessage-cache"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [paired-sms-watch] %(levelname)s: %(message)s"
)
log = logging.getLogger()


# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------

def now_iso():
    return datetime.now(timezone.utc).isoformat()


def safe_str(v, default=""):
    if v is None:
        return default
    try:
        return str(v)
    except Exception:
        return default


def pick_phone() -> str | None:
    """Find first paired+connected device with MAP support, return BD addr."""
    try:
        sys_bus = dbus.SystemBus()
        manager = dbus.Interface(
            sys_bus.get_object("org.bluez", "/"),
            "org.freedesktop.DBus.ObjectManager",
        )
        objects = manager.GetManagedObjects()
        for path, ifaces in objects.items():
            if "org.bluez.Device1" not in ifaces:
                continue
            dev = ifaces["org.bluez.Device1"]
            if not dev.get("Paired", False):
                continue
            if not dev.get("Connected", False):
                continue
            uuids = [str(u).lower() for u in dev.get("UUIDs", [])]
            if any(u.startswith("00001132") for u in uuids):
                return str(dev.get("Address", ""))
    except Exception as e:
        log.error(f"pick_phone failed: {e}")
    return None


def load_seen_ids() -> set:
    if not SEEN_DB.exists():
        return set()
    try:
        return set(SEEN_DB.read_text().splitlines())
    except OSError:
        return set()


def append_seen_id(msg_id: str):
    try:
        SEEN_DB.parent.mkdir(parents=True, exist_ok=True)
        with SEEN_DB.open("a") as f:
            f.write(f"{msg_id}\n")
    except OSError as e:
        log.warning(f"seen-db write failed: {e}")


def append_event_log(event: dict):
    try:
        EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with EVENT_LOG.open("a") as f:
            f.write(json.dumps(event) + "\n")
    except OSError as e:
        log.warning(f"event log write failed: {e}")


def msg_id_for(msg_props: dict) -> str:
    """Stable identifier for a message — used for dedup across daemon runs.
    Falls back to msg_path when props are empty (stub case)."""
    ts = safe_str(msg_props.get("Timestamp"))
    sender = safe_str(msg_props.get("SenderAddress"))
    subj = safe_str(msg_props.get("Subject"))[:40]
    return f"{ts}__{sender}__{subj}"


# ---------------------------------------------------------------------------
# bMessage parsing
# ---------------------------------------------------------------------------

def parse_bmessage(text: str) -> dict:
    """Parse the bMessage envelope (RFC 2822-ish, MAP spec section 3.1.6).

    Returns dict with keys: sender_name, sender_addr, body, status, msg_type, folder.
    Missing keys default to empty string.
    """
    out = {
        "sender_name": "",
        "sender_addr": "",
        "body": "",
        "status": "",
        "msg_type": "",
        "folder": "",
    }
    if not text:
        return out

    m = re.search(r"^STATUS:(.+)$", text, re.MULTILINE)
    if m:
        out["status"] = m.group(1).strip()
    m = re.search(r"^TYPE:(.+)$", text, re.MULTILINE)
    if m:
        out["msg_type"] = m.group(1).strip()
    m = re.search(r"^FOLDER:(.+)$", text, re.MULTILINE)
    if m:
        out["folder"] = m.group(1).strip()

    vc = re.search(r"BEGIN:VCARD(.*?)END:VCARD", text, re.DOTALL)
    if vc:
        vc_text = vc.group(1)
        fn = re.search(r"^FN:(.+)$", vc_text, re.MULTILINE)
        if fn:
            out["sender_name"] = fn.group(1).strip()
        tel = re.search(r"^TEL[^:]*:(.+)$", vc_text, re.MULTILINE)
        if tel:
            out["sender_addr"] = tel.group(1).strip()

    msg = re.search(r"BEGIN:MSG\r?\n(.*?)\r?\nEND:MSG", text, re.DOTALL)
    if msg:
        out["body"] = msg.group(1).strip()

    return out


def fetch_bmessage(bus, msg_path: str, timeout=10.0) -> str:
    """Call Message1.Get() on a stub message path to fetch the full bMessage envelope.

    Writes to a temp file, polls for transfer completion, reads & deletes the file.
    Returns the bMessage text, or empty string if anything failed.
    """
    try:
        msg_obj = dbus.Interface(
            bus.get_object(OBEX_BUS, msg_path), MSG_IFACE)

        BMSG_TMP_DIR.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            prefix="bmsg-", suffix=".txt",
            dir=str(BMSG_TMP_DIR), delete=False,
        ) as tf:
            out_file = tf.name

        msg_obj.Get(out_file, dbus.Boolean(False))

        deadline = time.time() + timeout
        last_size = -1
        stable_count = 0
        while time.time() < deadline:
            try:
                size = os.path.getsize(out_file)
            except OSError:
                size = 0
            if size > 0 and size == last_size:
                stable_count += 1
                if stable_count >= 2:
                    break
            else:
                stable_count = 0
            last_size = size
            time.sleep(0.2)

        try:
            with open(out_file, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        finally:
            try:
                os.unlink(out_file)
            except OSError:
                pass

        return content
    except dbus.DBusException as e:
        log.warning(f"fetch_bmessage Get() failed for {msg_path}: {e}")
        return ""
    except OSError as e:
        log.warning(f"fetch_bmessage I/O failed: {e}")
        return ""


# ---------------------------------------------------------------------------
# MAP session manager
# ---------------------------------------------------------------------------

class MapWatcher:
    """Owns a MAP session and dispatches new-message events."""

    def __init__(self, phone_mac: str, hook_cmd: str | None = None,
                 stop_after_first: bool = False, print_only: bool = False):
        self.phone = phone_mac
        self.hook_cmd = hook_cmd
        self.stop_after_first = stop_after_first
        self.print_only = print_only

        self.bus = dbus.SessionBus()
        self.client = dbus.Interface(
            self.bus.get_object(OBEX_BUS, OBEX_PATH), CLIENT_IFACE)

        self.session_path: str | None = None
        self.session_obj = None
        self.map_iface = None
        self.seen_ids = load_seen_ids()
        self.events_dispatched = 0
        self.session_lock = threading.Lock()
        self.stop_flag = threading.Event()
        self.first_seen_at = time.time()

        self.bus.add_signal_receiver(
            self._on_iface_added,
            signal_name="InterfacesAdded",
            dbus_interface="org.freedesktop.DBus.ObjectManager",
        )

    def open_session(self) -> bool:
        with self.session_lock:
            try:
                if self.session_path:
                    self._close_session_locked()
                args = dbus.Dictionary({"Target": "map"}, signature="sv")
                path = self.client.CreateSession(self.phone, args)
                self.session_path = str(path)
                self.session_obj = self.bus.get_object(OBEX_BUS, self.session_path)
                self.map_iface = dbus.Interface(self.session_obj, MAP_IFACE)
                log.info(f"MAP session opened: {self.session_path}")
                self._nav_inbox()
                self.first_seen_at = time.time()
                self._prime_seen()
                return True
            except dbus.DBusException as e:
                log.error(f"CreateSession failed: {e}")
                self.session_path = None
                return False

    def _close_session_locked(self):
        if not self.session_path:
            return
        try:
            self.client.RemoveSession(self.session_path)
        except dbus.DBusException:
            pass
        self.session_path = None
        self.session_obj = None
        self.map_iface = None

    def close_session(self):
        with self.session_lock:
            self._close_session_locked()

    def _nav_inbox(self):
        try:
            self.map_iface.SetFolder("telecom")
            self.map_iface.SetFolder("msg")
            self.map_iface.SetFolder("inbox")
            log.info("Navigated to /telecom/msg/inbox")
        except dbus.DBusException as e:
            log.warning(f"Folder nav: {e}")

    def _prime_seen(self):
        """List recent messages so they're marked already-seen."""
        try:
            msgs = self.map_iface.ListMessages(
                "", dbus.Dictionary({"MaxCount": dbus.UInt16(20)}, signature="sv"))
            count = 0
            for path, props in msgs.items():
                mid = msg_id_for(props)
                if mid not in self.seen_ids:
                    self.seen_ids.add(mid)
                    append_seen_id(mid)
                count += 1
            log.info(f"Primed seen-cache with {count} existing messages")
        except dbus.DBusException as e:
            log.warning(f"ListMessages prime: {e}")

    def _on_iface_added(self, path, interfaces):
        if MSG_IFACE not in interfaces:
            return
        msg = interfaces[MSG_IFACE]

        folder = safe_str(msg.get("Folder"))
        read = bool(msg.get("Read", True))
        sent = bool(msg.get("Sent", True))

        if folder != "/telecom/msg/inbox":
            return
        if sent or read:
            return

        sender = safe_str(msg.get("Sender"))
        sender_addr = safe_str(msg.get("SenderAddress"))
        subject = safe_str(msg.get("Subject"))
        timestamp = safe_str(msg.get("Timestamp"))
        msg_type = safe_str(msg.get("Type"))
        status = safe_str(msg.get("Status"))

        is_stub = (not sender_addr) and (not subject)
        source = "props"
        body = subject

        if is_stub:
            log.info(f"Stub notification (status={status}), fetching bMessage from {path}")
            bmsg_text = fetch_bmessage(self.bus, str(path))
            if bmsg_text:
                parsed = parse_bmessage(bmsg_text)
                if parsed["sender_name"]:
                    sender = parsed["sender_name"]
                if parsed["sender_addr"]:
                    sender_addr = parsed["sender_addr"]
                if parsed["body"]:
                    body = parsed["body"]
                    subject = parsed["body"][:80]
                source = "bmessage"
                log.info(f"  Parsed bMessage: from={sender}({sender_addr}) body=\"{body[:50]}\"")
            else:
                log.warning(f"  Could not fetch bMessage for {path}")

        # Build dedup key. When MAP gives us a stable message path, include it -
        # bMessage subject+sender+empty-timestamp can collide when user sends the
        # same text twice (e.g. retrying "Hi Agent, ...").
        mid_extras = {
            "Timestamp": timestamp,
            "SenderAddress": sender_addr,
            "Subject": subject,
        }
        # Include MAP message handle - guaranteed unique per phone session
        path_str = str(path)
        if path_str:
            mid_extras["__path"] = path_str.split("/")[-1]
        mid = msg_id_for(mid_extras) + "::" + mid_extras.get("__path", "")
        if mid in self.seen_ids:
            return
        self.seen_ids.add(mid)
        append_seen_id(mid)

        self._dispatch(path, {
            "sender": sender,
            "sender_address": sender_addr,
            "subject": subject,
            "body": body,
            "timestamp": timestamp,
            "type": msg_type,
            "folder": folder,
            "status": status,
            "source": source,
            "size": int(msg.get("Size", 0)),
        })

        if self.stop_after_first:
            self.stop_flag.set()

    def _dispatch(self, msg_path, fields: dict):
        event = {
            "received_at": now_iso(),
            "phone": self.phone,
            "msg_path": str(msg_path),
            **fields,
        }
        append_event_log(event)
        self.events_dispatched += 1
        log.info(
            f"NEW {fields['type']} from {fields['sender']}({fields['sender_address']}) "
            f"[src={fields['source']}]: {fields['body'][:60]}"
        )

        if self.print_only or not self.hook_cmd:
            return

        env = os.environ.copy()
        env.update({
            "BTSMS_SENDER": fields['sender'],
            "BTSMS_SENDER_ADDR": fields['sender_address'],
            "BTSMS_SUBJECT": fields['subject'],
            "BTSMS_BODY": fields['body'],
            "BTSMS_TIMESTAMP": fields['timestamp'],
            "BTSMS_TYPE": fields['type'],
            "BTSMS_FOLDER": fields['folder'],
            "BTSMS_SOURCE": fields['source'],
            "BTSMS_PHONE": self.phone,
        })
        try:
            subprocess.Popen(
                self.hook_cmd, shell=True, env=env,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            log.info(f"Hook dispatched: {self.hook_cmd[:80]}")
        except OSError as e:
            log.warning(f"Hook exec failed: {e}")

    def heartbeat_loop(self, interval=60):
        """Periodically verify session is alive; rebuild if stale."""
        while not self.stop_flag.is_set():
            time.sleep(interval)
            if self.stop_flag.is_set():
                break
            try:
                self.map_iface.SetFolder("/")
                self.map_iface.SetFolder("telecom")
                self.map_iface.SetFolder("msg")
                self.map_iface.SetFolder("inbox")
            except dbus.DBusException as e:
                log.warning(f"Heartbeat lost session ({e}), reopening...")
                ok = False
                for attempt in range(3):
                    if self.open_session():
                        ok = True
                        break
                    time.sleep(2 ** attempt)
                if not ok:
                    log.error("Failed to reopen session after 3 attempts")


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_status() -> int:
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            if Path(f"/proc/{pid}").is_dir():
                print(f"paired-sms-watch is running (pid {pid})")
            else:
                print(f"paired-sms-watch pid file exists ({pid}) but process gone (stale)")
        except (OSError, ValueError):
            print("pid file unreadable")
    else:
        print("paired-sms-watch is NOT running")
    if EVENT_LOG.exists():
        try:
            lines = EVENT_LOG.read_text().splitlines()
            print(f"\nEvent log: {EVENT_LOG} ({len(lines)} events)")
            if lines:
                last = json.loads(lines[-1])
                print(f"Last event: {last.get('received_at')} "
                      f"from {last.get('sender')}: "
                      f"{(last.get('body') or last.get('subject', ''))[:60]}")
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
            body = e.get('body') or e.get('subject', '')
            print(f"{e.get('received_at')} [{e.get('type','?')}] "
                  f"{e.get('sender')}({e.get('sender_address')}): {body[:80]}")
        except json.JSONDecodeError:
            print(f"  (malformed): {ln[:80]}")
    return 0


def cmd_watch(args) -> int:
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    phone = args.phone or pick_phone()
    if not phone:
        log.error("No paired+connected MAP-capable phone found.")
        return 2
    log.info(f"Target phone: {phone}")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        PID_FILE.write_text(str(os.getpid()))
    except OSError:
        pass

    watcher = MapWatcher(phone, args.hook, args.once, args.print_events_only)
    if not watcher.open_session():
        log.error("Could not open initial MAP session.")
        return 3

    loop = GLib.MainLoop()

    def shutdown(signum, frame):
        log.info(f"Caught signal {signum}, shutting down")
        watcher.stop_flag.set()
        watcher.close_session()
        try:
            PID_FILE.unlink(missing_ok=True)
        except OSError:
            pass
        loop.quit()

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    if not args.once:
        threading.Thread(target=watcher.heartbeat_loop, daemon=True).start()

    log.info(f"Watching for new SMS/MMS - events log: {EVENT_LOG}")
    if args.once:
        log.info("Will exit after first new message")

    def stop_watcher():
        while not watcher.stop_flag.is_set():
            time.sleep(0.5)
        loop.quit()

    threading.Thread(target=stop_watcher, daemon=True).start()

    try:
        loop.run()
    finally:
        watcher.close_session()
        try:
            PID_FILE.unlink(missing_ok=True)
        except OSError:
            pass

    log.info(f"Exiting. Events dispatched this run: {watcher.events_dispatched}")
    return 0


def main():
    p = argparse.ArgumentParser(description="Watch for incoming SMS/MMS on a paired Bluetooth phone.")
    p.add_argument("--phone", help="Specific phone MAC")
    p.add_argument("--hook", help="Shell command to execute on each new message")
    p.add_argument("--print-events-only", action="store_true")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--watch", action="store_true")
    g.add_argument("--once", action="store_true")
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
