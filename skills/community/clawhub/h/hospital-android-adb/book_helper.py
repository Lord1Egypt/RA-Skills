#!/usr/bin/env python3
"""Drive the WeChat 服务号「上海市级医院互联网总平台」 booking flow over USB ADB.

Companion to SKILL.md. It navigates as far as the 预约信息 (confirmation) page and
**deliberately stops there** — submitting is a separate, explicit command so a human
confirmation can sit in between.

    book_helper.py shot                 # screenshot + OCR dump (use when lost)
    book_helper.py slots                # list the date/time rows currently on screen
    book_helper.py reach                # 便民服务 -> 预约信息, then request the SMS code
    book_helper.py code 123456          # paste the SMS code into the 验证码 field
    book_helper.py submit --confirm "<details>"
                                        # re-OCR 确认预约, then tap it

`submit` REQUIRES `--confirm`, and the value must contain the hospital, department,
date and 上午/下午 **as OCR'd from the page at submit time** — run `submit` with no
`--confirm` first and it prints exactly what it expects. The point is that you cannot
reach submission without having read the 预约信息 page and shown it to the user; the
flag is an acknowledgement, not a rubber stamp.

Target date/AM-PM come from the environment so you can retarget without editing:

    HOSPITAL_DATE=2026-10-21 HOSPITAL_AMPM=上午 book_helper.py reach

Requires: uiautomator2, rapidocr-onnxruntime (see SKILL.md "Setup"), and the
appium-android-adb base skill, which ships ocr_bridge.py. ClawHub has no dependency
resolver, so that skill must be installed alongside this one:

    clawhub install appium-android-adb
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from pathlib import Path

# --- locate ocr_bridge.py (appium-android-adb base skill) ---------------------

BASE_SKILL = "appium-android-adb"

MISSING_BASE_HELP = f"""cannot find ocr_bridge.py — the {BASE_SKILL} base skill is not installed.

This skill depends on it; ClawHub has no dependency resolver, so install both:
  clawhub install {BASE_SKILL}

Or point at it explicitly if you keep skills somewhere unusual:
  export ADB_OCR_BASE=/path/to/skills/{BASE_SKILL}
"""


def _candidate_bases():
    """Where the base skill might be, most portable first.

    Note: OCR_BRIDGE_DIR is deliberately NOT consulted here. It is the
    screenshot cache directory (see ocr_bridge._shot_dir), and pointing it at
    a skill directory — which the previous error message told people to do —
    would write screen captures, including payment and booking pages, into
    that skill directory.
    """
    here = Path(__file__).resolve().parent
    override = os.environ.get("ADB_OCR_BASE")
    if override:
        return [Path(override)]
    return [
        here.parent / BASE_SKILL,                                   # sibling install
        Path.home() / ".openclaw/workspace/skills" / BASE_SKILL,
        Path.home() / "caremate/skills" / BASE_SKILL,
    ]


def _load_ocr_bridge():
    for base in _candidate_bases():
        if (base / "ocr_bridge.py").is_file():
            sys.path.insert(0, str(base))
            import ocr_bridge  # noqa: E402
            return ocr_bridge
    sys.exit(MISSING_BASE_HELP)


ob = _load_ocr_bridge()
import uiautomator2 as u2  # noqa: E402

D = u2.connect()

TARGET_DATE = os.environ.get("HOSPITAL_DATE", "2026-10-21")
WANT = os.environ.get("HOSPITAL_AMPM", "上午")          # 上午 / 下午

# Tapping the 有号 in the row *below* the target is the classic failure mode,
# so the date box's own y-band is the anchor for every match.
ROW_BAND = 70          # px — how far a 上午/下午 label may sit from its date line
HAV_BELOW = 300        # px — how far below the date line the 有号 button may sit


# --- screen helpers ----------------------------------------------------------

def shot():
    """OCR the screen: [(text, left, top, right, bottom), ...]."""
    return ob.shot()


def boxes(text, pred=None):
    """All OCR boxes whose text contains `text` (exact match if pred is None)."""
    return [b for b in shot() if text in b[0] and (pred is None or pred(b))]


def box(text, pred=None, what=None):
    got = boxes(text, pred)
    if not got:
        die(f"no {what or text!r} on screen")
    return got[0]


def center(b):
    return (b[1] + b[3]) // 2, (b[2] + b[4]) // 2


def tap(x, y, settle=2.0):
    D.click(x, y)
    time.sleep(settle)


def tap_box(b, settle=2.0):
    tap(*center(b), settle=settle)


def wait_for(text, timeout=25):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if any(text in b[0] for b in shot()):
            print(f"   ok: {text!r}")
            return
        time.sleep(2)
    die(f"timed out waiting for {text!r}")


def die(msg):
    print(f"FAIL: {msg}\n--- screen ---")
    for b in shot():
        print("   ", b)
    raise SystemExit(1)


def dump(label=""):
    print(f"--- {label} ---")
    for b in shot():
        print("   ", b)


# --- schedule list -----------------------------------------------------------

def find_slot(date=TARGET_DATE, want=WANT, verbose=False):
    """Locate the 有号 button for `date` + `want`, if that row is on screen."""
    screen = shot()
    dates = [b for b in screen if date in b[0]]
    if not dates:
        return None
    d = dates[0]
    amps = [b for b in screen
            if want in b[0] and b[1] > d[1] and abs(b[2] - d[2]) < ROW_BAND]
    if not amps:
        return None
    hav = [b for b in screen
           if b[0].strip() == "有号"
           and d[2] < b[2] < d[4] + HAV_BELOW
           and b[1] > 700]
    if verbose:
        print(f"   date={d}\n   ampm={amps}\n   有号={hav}")
    return hav[0] if hav else None


def scroll_to(date=TARGET_DATE, want=WANT, max_swipes=14):
    for _ in range(max_swipes):
        found = find_slot(date, want)
        if found:
            return found
        ob.scroll("up", scale=0.3, sleep=1.5)
    die(f"never found {date} {want} — is the date inside the booking window?")


def cmd_slots():
    """Print the date/time rows currently visible, so you can see what's bookable."""
    seen = set()
    for b in shot():
        t = b[0].strip()
        if ("星期" in t or t in ("上午", "下午")) and b[1] < 600:
            seen.add((t, b[2]))
    for t, y in sorted(seen, key=lambda x: x[1]):
        print(f"  y={y:<5} {t}")


# --- the flow ----------------------------------------------------------------

def reach():
    date, want = TARGET_DATE, WANT
    print(f"target: {date} {want}")

    print("[1] 便民服务")
    tap(385, 812, settle=5)                      # WeChat search card shortcut
    if not any("预约挂号" in b[0] for b in shot()):
        tap(300, 2319, settle=5)                 # 服务号 bottom menu
    wait_for("预约挂号")

    print("[2] 预约挂号")
    tap(540, 942, settle=5)
    wait_for("搜医院")

    print("[3] search the hospital")
    tap(540, 316, settle=3)
    wait_for("历史搜索", timeout=15)
    chip = boxes("华山医院", lambda b: b[2] < 900)          # 历史搜索 / 热门搜索 chip
    if chip:
        tap_box(chip[0], settle=5)
    else:                                                     # paste, then submit
        D.set_clipboard("华山医院")
        time.sleep(0.5)
        subprocess.run(["adb", "shell", "input", "keyevent", "279"])
        time.sleep(2)
        tap(1004, 2272, settle=5)                             # keyboard 搜索 key
    wait_for("华山医院")

    print("[4] hospital card")
    tap(540, 700, settle=5)
    wait_for("请选择就诊院区", timeout=20)

    print("[5] campus 华山医院 (总院)")
    row = [b for b in shot() if b[0].strip() == "华山医院"]    # exact match only
    if not row:
        die("no exact '华山医院' campus row")
    tap_box(row[0], settle=5)
    wait_for("普通门诊", timeout=20)
    if not any("493号" in b[0] for b in shot()):
        print("   WARNING: address line does not say 493号 — check the campus before booking")

    print("[6] 普通门诊 tab")
    tab = box("普通门诊", lambda b: b[2] < 800, what="普通门诊 tab")
    tap_box(tab, settle=4)
    wait_for("皮肤科", timeout=20)

    print("[7] 皮肤科 (left list -> right panel)")
    left = box("皮肤科", lambda b: b[2] > 800 and b[1] < 540, what="皮肤科 in dept list")
    tap_box(left, settle=4)
    right = box("皮肤科", lambda b: b[2] > 700 and b[1] > 540, what="皮肤科 in right panel")
    tap_box(right, settle=5)
    wait_for("普通门诊-[医联平台]", timeout=20)

    print("[8] open the appointment type")
    entry = box("普通门诊-[医联平台]", what="appointment type row")
    tap_box(entry, settle=6)
    wait_for("2026-", timeout=25)

    print(f"[9] find {date} {want}")
    hav = scroll_to(date, want)
    print(f"   tapping 有号 at {center(hav)}")
    tap_box(hav, settle=7)
    wait_for("预约信息", timeout=25)
    wait_for("选择就诊卡", timeout=15)

    print("[10] request the SMS code")
    tap(914, 1038, settle=3)
    if not any("秒" in b[0] or "重新发送" in b[0] for b in shot()):
        print("   no countdown — tapping 获取验证码 again")
        tap(914, 1038, settle=3)

    print("\n=== READY — 预约信息 page ===")
    dump()
    print("\n*** Verify with the user: 医院 / 科室 / 类型 / 就诊日期 / 就诊时段 / 就诊卡 / 金额.")
    print("*** The 就诊卡 checkbox must be on the right card BEFORE the code is used.")
    print("*** Then: book_helper.py code <digits>  &&  book_helper.py submit")


def cmd_code(code):
    if not (code.isdigit() and len(code) == 6):
        die(f"expected a 6-digit code, got {len(code)} chars")
    print(f"[code] pasting {len(code)} digits")
    field = boxes("请输入验证码")
    if field:
        tap(*center(field[0]), settle=1.5)
    else:                                  # field already filled — anchor on the label
        lbl = box("验证码", lambda b: b[1] < 250 and 900 < b[2] < 1150, what="验证码 label")
        tap(lbl[3] + 180, (lbl[2] + lbl[4]) // 2, settle=1.5)
    D.set_clipboard(code)
    time.sleep(0.5)
    subprocess.run(["adb", "shell", "input", "keyevent", "279"])      # PASTE
    time.sleep(2)
    if not any(code in b[0] for b in shot()):
        die("code does not appear in the field")
    print("   ok: code is in the field")
    dump("after code entry")


CONFIRM_ROWS = ("医院", "科室", "就诊日期", "就诊时段")


def read_confirmation_page():
    """Read the binding details off the 预约信息 page (label -> value on its row)."""
    screen = shot()
    page = {}
    for label in CONFIRM_ROWS:
        labs = [b for b in screen if b[0].strip() == label]
        if not labs:
            continue
        lab = labs[0]
        vals = [b for b in screen if b[1] > lab[3] and abs(b[2] - lab[2]) < 45]
        if vals:
            vals.sort(key=lambda b: b[1])
            page[label] = vals[0][0].strip()
    return page


def confirm_problems(page, confirm):
    """Fields the page shows that `confirm` fails to acknowledge.

    Whitespace is stripped before comparing, because OCR spacing is not stable
    (`2026-10-21星期三上午` vs `2026-10-21 星期三 上午`).
    """
    flat = re.sub(r"\s+", "", confirm)
    problems = []
    for key in ("医院", "科室", "就诊时段"):
        val = re.sub(r"\s+", "", page.get(key, ""))
        if val and val not in flat:
            problems.append(f"{key}={page.get(key, '')}")
    date = re.search(r"\d{4}-\d{2}-\d{2}", page.get("就诊日期", ""))
    if date and date.group(0) not in flat:
        problems.append(f"就诊日期={page.get('就诊日期', '')}")
    for half in ("上午", "下午"):
        if half in page.get("就诊日期", "") and half not in flat:
            problems.append(half)
    return problems


def cmd_submit(confirm=None):
    """Tap 确认预约 — but only once the caller has named the booking back.

    `--confirm` is the gate. Its value must contain the hospital, department,
    date and 上午/下午 that get OCR'd off the live page, so it cannot be produced
    without actually reading the 预约信息 page. That is what stops an agent
    running reach -> code -> submit back to back and creating a real
    appointment that was never put in front of the user.
    """
    page = read_confirmation_page()
    missing = [k for k in CONFIRM_ROWS if k not in page]
    if missing:
        die(f"not on the 预约信息 page (missing {', '.join(missing)}) — run `reach` first")

    print("   the page says:")
    for k in CONFIRM_ROWS:
        print(f"     {k}: {page[k]}")

    if not confirm:
        print("\nREFUSING TO SUBMIT — no --confirm given.")
        print("Show the above to the user, get their explicit yes, then re-run with:")
        print(f'  book_helper.py submit --confirm "{page["医院"]}/'
              f'{page["科室"]}/{page["就诊日期"]}"')
        raise SystemExit(2)

    problems = confirm_problems(page, confirm)
    if problems:
        die("--confirm does not match what is on screen; it is missing " + ", ".join(problems))

    print(f"   acknowledged: {confirm}")
    print("[submit] locating 确认预约")
    b = box("确认预约", what="确认预约 button")
    print(f"   tapping at {center(b)}")
    tap_box(b, settle=4)
    print("   waiting for the result (a spinner appears first)")
    deadline = time.time() + 60
    while time.time() < deadline:
        screen = shot()
        if any("预约成功" in x[0] or "预约详情" in x[0] for x in screen):
            print("\n=== SUCCESS ===")
            dump()
            return
        if any("错误" in x[0] or "失败" in x[0] or "重新加载" in x[0] for x in screen):
            print("\n=== FAILED — screen shows an error ===")
            dump()
            raise SystemExit(1)
        time.sleep(4)
    print("\n=== unresolved after 60s — check the screen ===")
    dump()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "shot"
    if cmd == "reach":
        reach()
    elif cmd == "code":
        if len(sys.argv) < 3:
            die("usage: book_helper.py code <6-digit>")
        cmd_code(sys.argv[2])
    elif cmd == "submit":
        rest = sys.argv[2:]
        confirm = None
        if "--confirm" in rest:
            i = rest.index("--confirm")
            if i + 1 >= len(rest):
                die("--confirm needs a value")
            confirm = rest[i + 1]
        cmd_submit(confirm)
    elif cmd == "slots":
        cmd_slots()
    elif cmd == "shot":
        dump()
    else:
        print(__doc__)
        raise SystemExit(2)
