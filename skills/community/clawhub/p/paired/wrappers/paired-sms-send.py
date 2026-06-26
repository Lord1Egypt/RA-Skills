#!/usr/bin/env python3
"""paired-sms-send — Send SMS via ADB UI automation (autosend version).

Workflow:
  1. Wake screen if dozing
  2. Verify keyguard is dismissed (Bouncer means PIN required - we abort)
  3. Open Samsung Messages with Intent (number + body pre-filled)
  4. Wait for the Messages compose UI to be visible
  5. Locate the Send button via uiautomator dump (resource-id send_button1)
  6. Tap Send
  7. Confirm send by checking sent-folder
  8. Power off screen (return phone to original state)

Returns clean JSON. Designed for Agent to invoke via Telegram reply hook.

CAVEATS:
  - Only works while phone is unlocked. If keyguard is locked with PIN/pattern,
    we abort with code=keyguard_locked and a clear message.
  - Tap coordinates are detected dynamically (no hardcoded bounds).
  - Uses shlex.quote for safe shell escaping.
  - 3-second wait for compose screen + 3-second wait for send confirmation.
"""
from __future__ import annotations
import argparse
import json
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path
_HOME = str(Path.home())

ADB = "/usr/bin/adb"

# Samsung Messages app + the resource-id of its Send button
MESSAGES_PKG = "com.samsung.android.messaging"
SEND_BUTTON_ID = f"{MESSAGES_PKG}:id/send_button1"

# PIN file for auto-unlock (mode 600). Optional - only used with --auto-unlock.
PIN_FILE = f"{_HOME}/.config/paired-sms-send/pin"


def adb(*args: str, timeout: float = 15) -> tuple[int, str, str]:
    p = subprocess.run([ADB] + list(args), capture_output=True, text=True,
                       timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def adb_shell(cmd: str, timeout: float = 15) -> tuple[int, str, str]:
    return adb("shell", cmd, timeout=timeout)


def is_keyguard_locked() -> tuple[bool, str]:
    """Returns (locked, reason). Inspects mCurrentFocus line, not the whole
    dumpsys output - the Bouncer window object is defined in the window stack
    even when phone is unlocked."""
    rc, out, err = adb_shell("dumpsys window")
    if rc != 0:
        return True, f"dumpsys failed: {err.strip()[:80]}"
    locked_indicators = []
    # Check the actual focused window line (not the whole stack)
    focus_match = re.search(r"mCurrentFocus=Window\{[^}]*\}", out)
    if focus_match:
        focus = focus_match.group(0)
        if "Bouncer" in focus or "Keyguard" in focus:
            locked_indicators.append(f"focus={focus[:80]}")
    # isStatusBarKeyguard=true is reliable
    if "isStatusBarKeyguard=true" in out:
        locked_indicators.append("isStatusBarKeyguard=true")
    # mDreamingLockscreen=true means screen is asleep AND lock is showing
    if "mDreamingLockscreen=true" in out:
        locked_indicators.append("mDreamingLockscreen=true")
    if locked_indicators:
        return True, ", ".join(locked_indicators)
    return False, "unlocked"


def wake_screen() -> None:
    adb_shell("input keyevent KEYCODE_WAKEUP")
    time.sleep(0.5)


def load_pin() -> str | None:
    """Read PIN from secure file. Returns None if not available."""
    try:
        import os, stat
        st = os.stat(PIN_FILE)
        # Refuse to read if file is too permissive
        if st.st_mode & (stat.S_IRWXG | stat.S_IRWXO):
            return None
        with open(PIN_FILE) as f:
            pin = f.read().strip()
        return pin if pin else None
    except (FileNotFoundError, PermissionError, OSError):
        return None


def unlock_with_pin(pin: str, timeout: float = 8.0) -> tuple[bool, str]:
    """Wake -> swipe to reveal Bouncer -> type PIN -> verify unlocked.
    Returns (success, info)."""
    # Wake
    adb_shell("input keyevent KEYCODE_WAKEUP")
    time.sleep(0.6)
    # Swipe up to bring up Bouncer (works on 1080x2220 override resolution)
    adb_shell("input swipe 540 2000 540 500 200")
    time.sleep(1.2)
    # Verify Bouncer is focused
    rc, out, _ = adb_shell("dumpsys window")
    focus_match = re.search(r"mCurrentFocus=Window\{[^}]*\}", out)
    if not focus_match or "Bouncer" not in focus_match.group(0):
        # Maybe it's already unlocked or the swipe didn't fire
        if "isStatusBarKeyguard=true" not in out and "mDreamingLockscreen=true" not in out:
            return True, "already unlocked after wake/swipe"
        return False, f"Bouncer not focused after swipe; focus={focus_match.group(0)[:60] if focus_match else 'none'}"
    # Type PIN. Note 9 auto-submits 4+ digit PIN.
    adb_shell(f"input text {pin}")
    time.sleep(1.5)
    # Verify unlock
    deadline = time.time() + timeout
    while time.time() < deadline:
        rc, out, _ = adb_shell("dumpsys window")
        if "isStatusBarKeyguard=false" in out and "mDreamingLockscreen=false" in out:
            focus_match = re.search(r"mCurrentFocus=Window\{[^}]*\}", out)
            if focus_match and "Bouncer" not in focus_match.group(0):
                return True, "unlocked"
        time.sleep(0.4)
    return False, "PIN entered but keyguard still showing - wrong PIN?"


def open_compose(number: str, body: str) -> tuple[bool, str]:
    """Launch Messages Intent. Returns (success, info)."""
    # shlex.quote handles spaces and special chars in body
    quoted_body = shlex.quote(body)
    quoted_num = shlex.quote(f"sms:{number}")
    cmd = (
        f"am start -a android.intent.action.SENDTO "
        f"-d {quoted_num} "
        f"--es sms_body {quoted_body}"
    )
    rc, out, err = adb_shell(cmd)
    if rc != 0:
        return False, err.strip() or out.strip()
    if "Error:" in out:
        return False, out.strip()
    return True, out.strip()


def wait_for_compose(timeout: float = 5.0) -> bool:
    """Poll until the Messages compose UI is visible.

    Samsung Messages 11.5.x renamed the focused activity from
    ConversationComposer to WithActivity, so the legacy focus-string
    check fails on current firmware. We now confirm compose is visible
    by checking that the Messages package owns the focused window AND a
    uiautomator dump contains the composer_root_view + message_edit_text
    resource-ids - both stable across the version change.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        rc, out, _ = adb_shell("dumpsys window")
        if rc == 0 and MESSAGES_PKG in out:
            focus = re.search(
                r"mCurrentFocus=Window\{[^}]*" + re.escape(MESSAGES_PKG) + r"[^}]*\}",
                out,
            )
            if focus:
                rc2, _, _ = adb_shell(
                    "uiautomator dump --compressed /sdcard/_paired_compose_check.xml",
                    timeout=5,
                )
                if rc2 == 0:
                    rc3, xml, _ = adb_shell(
                        "cat /sdcard/_paired_compose_check.xml"
                    )
                    if (
                        rc3 == 0
                        and "composer_root_view" in xml
                        and "message_edit_text" in xml
                    ):
                        return True
        time.sleep(0.3)
    return False


def find_send_button_centroid() -> tuple[int, int] | None:
    """Dump UI tree, locate the send_button1 node, return (cx, cy)."""
    rc, _, _ = adb_shell("uiautomator dump --compressed /sdcard/_paired_ui.xml",
                         timeout=10)
    if rc != 0:
        return None
    rc, xml, _ = adb_shell("cat /sdcard/_paired_ui.xml")
    if rc != 0 or not xml.strip():
        return None
    # Match a node containing the resource-id send_button1
    pat = re.compile(
        r'<node[^/>]*resource-id="' + re.escape(SEND_BUTTON_ID) +
        r'"[^/>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',
        re.DOTALL,
    )
    m = pat.search(xml)
    if not m:
        return None
    x1, y1, x2, y2 = map(int, m.groups())
    return ((x1 + x2) // 2, (y1 + y2) // 2)


def tap(x: int, y: int) -> None:
    adb_shell(f"input tap {x} {y}")


def screen_off() -> None:
    """Press POWER if screen is on (dumpsys reports state=ON)."""
    rc, out, _ = adb_shell("dumpsys power")
    if "Display Power: state=ON" in out:
        adb_shell("input keyevent KEYCODE_POWER")


def verify_in_sent(number: str, body_prefix: str) -> bool:
    """Check the sent folder for our outgoing message."""
    p = subprocess.run(
        [f"{_HOME}/bin/bt-adb-sms-list", "--sent", "--limit", "5"],
        capture_output=True, text=True, timeout=10)
    if p.returncode != 0:
        return False
    # Strip leading + from number for comparison (our number might be 07... or +447...)
    nums_to_match = {number.lstrip("+"), number}
    if number.startswith("0"):
        nums_to_match.add("+44" + number[1:])
    if number.startswith("+44"):
        nums_to_match.add("0" + number[3:])
    for line in p.stdout.splitlines():
        for nm in nums_to_match:
            if nm and nm in line:
                # Body match (first 10 chars) makes us confident this is OUR send
                if body_prefix[:10] in line:
                    return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Send SMS via ADB UI automation (autosend).")
    ap.add_argument("number", help="Phone number")
    ap.add_argument("text", help="Message body")
    ap.add_argument("--no-power-off", action="store_true",
                    help="Don't power off the screen after send (for debugging)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--allow-locked", action="store_true",
                    help="Don't abort if keyguard appears locked (try anyway)")
    ap.add_argument("--auto-unlock", action="store_true",
                    help=f"If locked, read PIN from {PIN_FILE} and unlock")
    ap.add_argument("--relock", action="store_true",
                    help="Press POWER after send to lock the phone again")
    args = ap.parse_args()

    result = {
        "ok": False,
        "number": args.number,
        "text": args.text,
        "stages": {},
    }

    # 1. Wake
    wake_screen()
    result["stages"]["wake"] = "done"

    # 2. Check keyguard
    locked, reason = is_keyguard_locked()
    result["stages"]["keyguard_check"] = {"locked": locked, "reason": reason}
    if locked:
        if args.auto_unlock:
            pin = load_pin()
            if not pin:
                result["error"] = "pin_unavailable"
                result["message"] = (f"--auto-unlock requested but PIN not readable from "
                                     f"{PIN_FILE} (must exist, mode 600).")
                if args.json:
                    print(json.dumps(result, indent=2))
                else:
                    print(result["message"], file=sys.stderr)
                return 8
            unlocked, info = unlock_with_pin(pin)
            result["stages"]["auto_unlock"] = {"ok": unlocked, "info": info}
            if not unlocked:
                result["error"] = "unlock_failed"
                result["message"] = f"Auto-unlock failed: {info}"
                if args.json:
                    print(json.dumps(result, indent=2))
                else:
                    print(result["message"], file=sys.stderr)
                return 9
            # Continue with the rest of the flow (compose, tap send, etc.)
        elif not args.allow_locked:
            result["error"] = "keyguard_locked"
            result["message"] = (f"Phone keyguard is locked ({reason}). "
                                 f"Cannot autosend SMS without unlock. "
                                 f"Use --allow-locked to try anyway, or "
                                 f"--auto-unlock to use stored PIN.")
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(result["message"], file=sys.stderr)
            return 3

    # 3. Open Messages with Intent
    ok, info = open_compose(args.number, args.text)
    result["stages"]["intent"] = {"ok": ok, "info": info[:200]}
    if not ok:
        result["error"] = "intent_failed"
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Intent failed: {info}", file=sys.stderr)
        return 4

    # 4. Wait for compose screen
    composed = wait_for_compose(timeout=5.0)
    result["stages"]["compose_visible"] = composed
    if not composed:
        result["error"] = "compose_did_not_appear"
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("Compose screen didn't appear in 5s", file=sys.stderr)
        return 5

    # 5. Find Send button
    send = find_send_button_centroid()
    result["stages"]["send_button"] = send
    if send is None:
        result["error"] = "send_button_not_found"
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("Could not locate Send button in UI tree", file=sys.stderr)
        return 6
    cx, cy = send

    # 6. Tap
    tap(cx, cy)
    result["stages"]["tap"] = {"x": cx, "y": cy}
    time.sleep(2.5)

    # 7. Verify
    sent_ok = verify_in_sent(args.number, args.text)
    result["stages"]["verified"] = sent_ok

    # 8. Power off (return to baseline state)
    if not args.no_power_off:
        screen_off()
        result["stages"]["screen_off"] = True
    # 8b. Re-lock (force keyguard back) if asked
    if args.relock:
        # POWER again forces lock immediately on most Samsungs
        adb_shell("input keyevent KEYCODE_SLEEP")
        time.sleep(0.3)
        result["stages"]["relocked"] = True

    result["ok"] = sent_ok
    if not sent_ok:
        result["error"] = "verification_failed"
        result["message"] = ("Send tap fired but message not found in sent folder "
                             "within 2.5s. Could be a delayed send or auth issue.")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if sent_ok:
            print(f"SMS sent to {args.number}: {args.text[:60]}")
        else:
            print(f"Send fired but unverified. Check phone manually. "
                  f"Stages: {json.dumps(result['stages'])}", file=sys.stderr)
    return 0 if sent_ok else 7


if __name__ == "__main__":
    sys.exit(main())
