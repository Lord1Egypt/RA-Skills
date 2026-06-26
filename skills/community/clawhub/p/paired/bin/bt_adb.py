"""
bt_adb.py — ADB companion library for the bluetooth skill.

Provides ADB-based fallback / complementary capabilities when the BT-native
path is blocked by phone-side restrictions (Samsung disabling OBEX OPP,
locking MAP-send, etc.) or when we want richer phone control than BT
profiles expose (notifications, screenshots, app launching, typing).

Architecture: every public function takes optional `serial=None` to pick
which adb device. If only one device is connected we use it; if multiple,
caller must specify.

Note: this lives on .86 alongside the BT tools. ADB binary at /usr/bin/adb
(installed via apt). Phone connects via USB cable directly to .86.
"""
from __future__ import annotations

import json
import re
import shlex
import subprocess
from pathlib import Path
from typing import Optional


ADB = "/usr/bin/adb"


class AdbError(RuntimeError):
    pass


def _adb(*args: str, serial: Optional[str] = None,
         timeout: float = 30.0,
         input_text: Optional[str] = None) -> str:
    """Run adb with optional -s serial and return stdout. Raises on failure."""
    cmd = [ADB]
    if serial:
        cmd += ["-s", serial]
    cmd += list(args)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout, input=input_text)
    except subprocess.TimeoutExpired:
        raise AdbError(f"adb {' '.join(args)} timed out after {timeout}s")
    if p.returncode != 0:
        raise AdbError(
            f"adb {' '.join(args)} exit={p.returncode}: "
            f"{p.stderr.strip() or p.stdout.strip()}"
        )
    return p.stdout


def list_devices() -> list[dict]:
    """Return [{serial, state, model?, manufacturer?}, ...]"""
    raw = _adb("devices", "-l")
    out = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("List of devices"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        serial = parts[0]
        state = parts[1]
        # Parse the rest: "device usb:1-3 product:foo model:SM-N960F device:... transport_id:..."
        d = {"serial": serial, "state": state}
        for tok in parts[2:]:
            if ":" in tok:
                k, _, v = tok.partition(":")
                d[k] = v
        out.append(d)
    return out


def find_device(serial: Optional[str] = None) -> dict:
    """Return the chosen device dict. If serial omitted and exactly one device, picks it."""
    devs = [d for d in list_devices() if d.get("state") == "device"]
    if not devs:
        raise AdbError("No ADB devices in 'device' state. Plug phone in via USB and accept debug prompt.")
    if serial:
        for d in devs:
            if d["serial"] == serial:
                return d
        raise AdbError(f"Device with serial {serial!r} not found among: {[d['serial'] for d in devs]}")
    if len(devs) > 1:
        raise AdbError(
            f"Multiple ADB devices ({len(devs)}). Pass --serial to disambiguate. "
            f"Devices: {[d['serial'] for d in devs]}"
        )
    return devs[0]


def shell(cmd: str, *, serial: Optional[str] = None,
          timeout: float = 30.0) -> str:
    """Run a shell command on the device."""
    d = find_device(serial)
    return _adb("shell", cmd, serial=d["serial"], timeout=timeout)


def push(local: str, remote: str, *, serial: Optional[str] = None,
         timeout: float = 120.0) -> dict:
    """Push a local file to the phone."""
    local = str(Path(local).expanduser().resolve())
    if not Path(local).exists():
        raise FileNotFoundError(local)
    d = find_device(serial)
    out = _adb("push", local, remote, serial=d["serial"], timeout=timeout)
    return {"local": local, "remote": remote, "stdout": out.strip()}


def pull(remote: str, local: str, *, serial: Optional[str] = None,
         timeout: float = 120.0) -> dict:
    """Pull a remote file to local disk."""
    local = str(Path(local).expanduser().resolve())
    Path(local).parent.mkdir(parents=True, exist_ok=True)
    d = find_device(serial)
    out = _adb("pull", remote, local, serial=d["serial"], timeout=timeout)
    return {"remote": remote, "local": local, "stdout": out.strip()}


# ---------------------------------------------------------------------------
# Phone identity / state
# ---------------------------------------------------------------------------
def device_info(serial: Optional[str] = None) -> dict:
    d = find_device(serial)
    s = d["serial"]
    props = {
        "serial": s,
        "model": _adb("shell", "getprop ro.product.model", serial=s).strip(),
        "manufacturer": _adb("shell", "getprop ro.product.manufacturer", serial=s).strip(),
        "android_version": _adb("shell", "getprop ro.build.version.release", serial=s).strip(),
        "build": _adb("shell", "getprop ro.build.display.id", serial=s).strip(),
        "state": d.get("state"),
    }
    return props


def battery(serial: Optional[str] = None) -> dict:
    """Return battery state via dumpsys."""
    raw = shell("dumpsys battery", serial=serial)
    out: dict = {}
    for line in raw.splitlines():
        line = line.strip()
        if ": " in line:
            k, _, v = line.partition(": ")
            out[k.strip()] = v.strip()
    # Normalise key fields
    return {
        "level_pct": int(out.get("level", -1)) if out.get("level", "").lstrip("-").isdigit() else None,
        "scale": int(out.get("scale", 100)) if out.get("scale", "").isdigit() else 100,
        "voltage_mv": int(out["voltage"]) if out.get("voltage", "").isdigit() else None,
        "temperature_c": (int(out["temperature"]) / 10.0) if out.get("temperature", "").isdigit() else None,
        "ac_powered": out.get("AC powered") == "true",
        "usb_powered": out.get("USB powered") == "true",
        "wireless_powered": out.get("Wireless powered") == "true",
        "technology": out.get("technology"),
        "health": out.get("health"),
        "status_code": out.get("status"),
        "raw": out,
    }


# ---------------------------------------------------------------------------
# SMS  (the big one — works around the Samsung MAP-send block)
# ---------------------------------------------------------------------------
_SMS_PROJ = "_id,date,address,body,read,type"


def _parse_content_query(text: str) -> list[dict]:
    """Parse adb 'content query' Row output."""
    out = []
    for line in text.splitlines():
        m = re.match(r"^Row:\s*\d+\s+(.*)$", line)
        if not m:
            continue
        parts = m.group(1)
        d: dict = {}
        # Each part is key=value, but values can contain commas/spaces.
        # Use a simple state machine.
        i = 0
        while i < len(parts):
            eq = parts.find("=", i)
            if eq < 0:
                break
            key = parts[i:eq]
            # find the next ", key=" pattern; key is alphanumeric+_
            rest = parts[eq + 1:]
            nxt = re.search(r",\s+[A-Za-z_][A-Za-z0-9_]*=", rest)
            if nxt:
                value = rest[:nxt.start()]
                i = eq + 1 + nxt.start() + 2  # skip ", "
            else:
                value = rest
                i = len(parts)
            d[key.strip()] = value
        if d:
            out.append(d)
    return out


def sms_inbox(limit: int = 20, serial: Optional[str] = None) -> list[dict]:
    """Read recent inbox SMS via content provider."""
    cmd = (f'content query --uri content://sms/inbox '
           f'--projection "{_SMS_PROJ}" --sort "date DESC"')
    raw = shell(cmd, serial=serial)
    msgs = _parse_content_query(raw)[:limit]
    # Add iso timestamp for readability
    import datetime
    for m in msgs:
        try:
            ts = int(m.get("date", "0")) / 1000
            m["timestamp"] = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            pass
    return msgs


def sms_sent(limit: int = 20, serial: Optional[str] = None) -> list[dict]:
    cmd = (f'content query --uri content://sms/sent '
           f'--projection "{_SMS_PROJ}" --sort "date DESC"')
    raw = shell(cmd, serial=serial)
    return _parse_content_query(raw)[:limit]


def sms_send(number: str, text: str, serial: Optional[str] = None) -> dict:
    """Send an SMS via the default messaging app's Intent.

    Uses am start -a android.intent.action.SENDTO with sms: scheme. This
    opens the messaging app pre-populated; we then use the keycode for
    KEYCODE_DPAD_CENTER (or the send button) — but that's UI-fragile.

    Better approach: insert directly into content://sms via content provider,
    BUT that only works if the running app is the default SMS app, which we
    aren't.

    Most reliable: use the `service call isms <code>` mechanism that calls
    SmsManager directly. Different Android versions number the codes
    differently. On Android 10+, sendTextMessage is method index 5.
    """
    # Use service call to ISms — this is the canonical SMS-send path
    # The exact transaction code varies by Android version but on N9 (Android 10)
    # SendTextMessageInternal is typically index 7 with a specific signature.
    # Simpler and more reliable: launch SMS app pre-populated, user taps send.

    # We'll do the simplest reliable thing: launch the messaging app with
    # the body pre-filled and the recipient set. User confirms by tapping send.
    # For headless agent use (no human interaction), see sms_send_silent.

    safe_body = text.replace('"', '\\"').replace("'", "\\'")
    cmd = (f'am start -a android.intent.action.SENDTO '
           f'-d "sms:{number}" '
           f'--es sms_body "{safe_body}" '
           f'--ez exit_on_sent true')
    out = shell(cmd, serial=serial)
    return {
        "method": "intent",
        "number": number,
        "text": text,
        "stdout": out.strip(),
        "note": "SMS app opened pre-populated; tap send on phone to deliver",
    }


def sms_send_silent(number: str, text: str,
                    serial: Optional[str] = None) -> dict:
    """Send SMS without UI by directly calling SmsManager via service call.

    REQUIRES: the device is rooted OR ADB has WRITE_SMS permission grant.
    Most user-mode Android 10+ devices reject this with SecurityException.
    """
    # Encode the strings as UTF-16 hex (Android Parcel format)
    def enc_str(s: str) -> str:
        # Each Parcel string is: int32 length + UTF-16-LE bytes + null term + padding
        # service call args use 's16' helper which we invoke via i32+s16
        return f's16:"{s}"'

    args = [enc_str(number),     # destAddr
            "null",              # scAddr
            enc_str(text),       # text
            "null",              # sentIntent
            "null"]              # deliveryIntent

    # Try a few common transaction codes. They differ across Android versions.
    for tx in (5, 7, 9, 4):
        cmd = f"service call isms {tx} {' '.join(args)}"
        try:
            out = shell(cmd, serial=serial, timeout=10.0)
            if "Result: Parcel" in out and "ffffffff" not in out[:80]:
                return {"method": f"service-call-tx{tx}", "result": out.strip()}
        except AdbError:
            continue
    raise AdbError(
        "service-call SMS send didn't succeed. The phone likely requires "
        "the calling app to be the default SMS handler. Use sms_send() (Intent UI) instead."
    )


# ---------------------------------------------------------------------------
# Notifications / UI / screen
# ---------------------------------------------------------------------------
def notifications(serial: Optional[str] = None) -> list[dict]:
    """List active notifications via dumpsys notification.

    Returns app, title, text fields per notification.
    """
    raw = shell("dumpsys notification --noredact", serial=serial,
                timeout=20.0)
    out: list[dict] = []
    cur: Optional[dict] = None
    for line in raw.splitlines():
        # Notification record header
        m = re.match(r'\s*NotificationRecord\(.*pkg=(\S+).*\bid=(\d+)', line)
        if m:
            if cur:
                out.append(cur)
            cur = {"package": m.group(1), "id": int(m.group(2))}
            continue
        if cur is None:
            continue
        # Look for title and text
        for field in ("android.title", "android.text", "android.subText"):
            tag = f"{field}=String "
            if tag in line:
                idx = line.find(tag)
                val = line[idx + len(tag):].strip().strip("()")
                cur[field.split(".")[-1]] = val
                break
    if cur:
        out.append(cur)
    return out


def screenshot(local_path: str = "~/Downloads/bluetooth/phone-screen.png",
               serial: Optional[str] = None) -> dict:
    """Capture phone screen and save to local file."""
    local_path = str(Path(local_path).expanduser().resolve())
    Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    remote = "/sdcard/Pictures/_paired_capture.png"
    shell(f"screencap -p {remote}", serial=serial, timeout=20.0)
    pull(remote, local_path, serial=serial)
    shell(f"rm {remote}", serial=serial)
    return {"saved_to": local_path, "size_bytes": Path(local_path).stat().st_size}


def launch_app(package_or_action: str, serial: Optional[str] = None) -> dict:
    """Launch an app by package name (e.g. com.spotify.music) or full activity."""
    if "/" in package_or_action:
        cmd = f"am start -n {package_or_action}"
    else:
        cmd = f"monkey -p {package_or_action} -c android.intent.category.LAUNCHER 1"
    out = shell(cmd, serial=serial)
    return {"target": package_or_action, "stdout": out.strip()}


def type_text(text: str, serial: Optional[str] = None) -> dict:
    """Inject text into the focused field. Spaces become %s for adb."""
    safe = text.replace(" ", "%s").replace("'", "\\'")
    out = shell(f"input text '{safe}'", serial=serial)
    return {"text": text, "stdout": out.strip()}


# ---------------------------------------------------------------------------
# Media control via media-session (alternative to AVRCP)
# ---------------------------------------------------------------------------
def media_dispatch(action: str, serial: Optional[str] = None) -> dict:
    """Send a media key event. action ∈ {play,pause,play-pause,next,previous,stop}."""
    valid = {"play", "pause", "play-pause", "next", "previous", "stop"}
    if action not in valid:
        raise ValueError(f"action must be one of {valid}")
    out = shell(f"cmd media_session dispatch {action}", serial=serial)
    return {"action": action, "stdout": out.strip()}


def media_status(serial: Optional[str] = None) -> dict:
    """Get current media session state from MediaSessionService."""
    raw = shell("dumpsys media_session", serial=serial, timeout=10.0)
    # Parse out the "active sessions" block
    in_active = False
    sessions: list[dict] = []
    cur: dict = {}
    for line in raw.splitlines():
        if "Sessions Stack" in line and "size=" in line:
            in_active = True
            continue
        if in_active and line.strip().startswith("Media session record"):
            if cur:
                sessions.append(cur)
            cur = {"raw": line.strip()}
            m = re.search(r'pkg=(\S+)', line)
            if m:
                cur["package"] = m.group(1)
            continue
        if in_active and "state=PlaybackState" in line:
            m = re.search(r'state=PlaybackState \{state=(\d+)', line)
            if m:
                states = {0: "none", 1: "stopped", 2: "paused", 3: "playing",
                          4: "fast_forwarding", 5: "rewinding", 6: "buffering",
                          7: "error", 8: "connecting", 9: "skipping_to_previous",
                          10: "skipping_to_next", 11: "skipping_to_queue_item"}
                cur["state"] = states.get(int(m.group(1)), m.group(1))
        elif in_active and "metadata:" in line:
            m = re.search(r'description=([^,]+)', line)
            if m:
                cur["title"] = m.group(1).strip()
    if cur:
        sessions.append(cur)
    return {"sessions": sessions}
