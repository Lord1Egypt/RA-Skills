#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(argv, *, input_text=None, timeout=15, check=False):
    return subprocess.run(
        argv,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=check,
    )


def emit(obj, code=0):
    print(json.dumps(obj, ensure_ascii=False))
    raise SystemExit(code)


def have_bin(name):
    return shutil.which(name)


def have_module(name):
    try:
        __import__(name)
        return True
    except Exception:
        return False


def osascript(lines, *, timeout=10):
    argv = ["osascript"]
    for line in lines:
        argv.extend(["-e", line])
    return run(argv, timeout=timeout)


def parse_ints(text):
    parts = [p.strip() for p in text.replace("\n", ",").split(",") if p.strip()]
    return [int(float(p)) for p in parts]


def desktop_bounds():
    r = osascript(['tell application "Finder" to get bounds of window of desktop'])
    if r.returncode != 0:
        return None
    vals = parse_ints(r.stdout)
    if len(vals) >= 4:
        left, top, right, bottom = vals[:4]
        return {"x": left, "y": top, "w": right - left, "h": bottom - top, "raw": vals[:4]}
    return None


def image_size(path):
    try:
        from PIL import Image
        with Image.open(path) as img:
            return {"w": img.width, "h": img.height}
    except Exception as e:
        return {"error": str(e)}


def cmd_env(_args):
    sw = run(["sw_vers"], timeout=5)
    arch = run(["uname", "-m"], timeout=5)
    tmp = Path(tempfile.gettempdir()) / "mac_gui_env_capture.png"
    shot = run(["/usr/sbin/screencapture", "-x", str(tmp)], timeout=15)
    shot_size = image_size(tmp) if shot.returncode == 0 else {"error": shot.stderr.strip()}
    try:
        tmp.unlink()
    except FileNotFoundError:
        pass
    bounds = desktop_bounds()
    scale = None
    if bounds and "w" in shot_size and bounds["w"]:
        scale = shot_size["w"] / bounds["w"]
    emit({
        "sw_vers": sw.stdout.strip(),
        "arch": arch.stdout.strip(),
        "desktop_bounds": bounds,
        "screenshot_size": shot_size,
        "estimated_scale": scale,
        "bins": {name: have_bin(name) for name in ["python3", "osascript", "screencapture", "cliclick", "magick", "tesseract"]},
        "modules": {name: have_module(name) for name in ["PIL", "pyautogui", "cv2", "Vision", "Quartz", "AppKit", "psutil"]},
    })


def cmd_capture(args):
    out = Path(args.output).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    raw_out = out if args.raw else out.with_suffix(out.suffix + ".raw.png")
    r = run(["/usr/sbin/screencapture", "-x", str(raw_out)], timeout=20)
    if r.returncode != 0:
        emit({"ok": False, "error": "screencapture_failed", "stderr": r.stderr.strip()}, 1)
    if args.raw:
        emit({"ok": True, "file": str(out), "mode": "raw", "size": image_size(out)})
    bounds = desktop_bounds()
    try:
        from PIL import Image
        with Image.open(raw_out) as img:
            raw_size = {"w": img.width, "h": img.height}
            if bounds:
                img = img.resize((bounds["w"], bounds["h"]))
                img.save(out)
                raw_out.unlink(missing_ok=True)
                emit({"ok": True, "file": str(out), "mode": "logical", "size": {"w": bounds["w"], "h": bounds["h"]}, "raw_size": raw_size})
            img.save(out)
    except Exception as e:
        if raw_out != out:
            raw_out.rename(out)
        emit({"ok": True, "file": str(out), "mode": "raw_fallback", "warning": str(e), "size": image_size(out)})
    emit({"ok": True, "file": str(out), "mode": "raw_fallback", "size": image_size(out)})


def cmd_front_app(_args):
    r = osascript(['tell application "System Events" to get name of first process whose frontmost is true'])
    if r.returncode != 0:
        emit({"ok": False, "error": r.stderr.strip()}, 1)
    emit({"ok": True, "app": r.stdout.strip()})


def cmd_activate(args):
    if args.path:
        r = run(["open", args.path], timeout=10)
    else:
        r = run(["open", "-a", args.app], timeout=10)
    if r.returncode != 0:
        emit({"ok": False, "stderr": r.stderr.strip()}, 1)
    emit({"ok": True, "app": args.app, "path": args.path})


def cmd_bounds(args):
    app = args.app
    attempts = []
    r = osascript([f'tell application "{app}" to get bounds of front window'])
    attempts.append({"method": "app_front_window_bounds", "code": r.returncode, "stderr": r.stderr.strip(), "stdout": r.stdout.strip()})
    if r.returncode == 0:
        vals = parse_ints(r.stdout)
        if len(vals) >= 4:
            left, top, right, bottom = vals[:4]
            emit({"ok": True, "app": app, "x": left, "y": top, "w": right - left, "h": bottom - top, "raw": vals[:4], "method": "application"})
    r = osascript([
        'tell application "System Events"',
        f'  tell process "{app}"',
        '    set p to position of front window',
        '    set s to size of front window',
        '    return (item 1 of p) & "," & (item 2 of p) & "," & (item 1 of s) & "," & (item 2 of s)',
        '  end tell',
        'end tell',
    ])
    attempts.append({"method": "system_events", "code": r.returncode, "stderr": r.stderr.strip(), "stdout": r.stdout.strip()})
    if r.returncode == 0:
        vals = parse_ints(r.stdout)
        if len(vals) >= 4:
            emit({"ok": True, "app": app, "x": vals[0], "y": vals[1], "w": vals[2], "h": vals[3], "method": "system_events"})
    emit({"ok": False, "app": app, "error": "bounds_unavailable", "attempts": attempts}, 1)


def modifier_clause(mods):
    if not mods:
        return ""
    mapping = {"cmd": "command", "command": "command", "ctrl": "control", "control": "control", "alt": "option", "opt": "option", "option": "option", "shift": "shift"}
    names = [mapping.get(m.lower(), m.lower()) + " down" for m in mods]
    return " using {" + ", ".join(names) + "}"


def cmd_key(args):
    combo = args.combo.lower().replace(" ", "")
    parts = combo.split("+")
    key = parts[-1]
    mods = parts[:-1]
    keycodes = {"return": 36, "enter": 36, "tab": 48, "escape": 53, "esc": 53, "delete": 51, "backspace": 51, "up": 126, "down": 125, "left": 123, "right": 124, "space": 49}
    using = modifier_clause(mods)
    if key in keycodes:
        line = f'tell application "System Events" to key code {keycodes[key]}{using}'
    elif len(key) == 1:
        line = f'tell application "System Events" to keystroke "{key}"{using}'
    else:
        line = f'tell application "System Events" to keystroke "{key}"{using}'
    r = osascript([line])
    if r.returncode != 0:
        emit({"ok": False, "combo": args.combo, "stderr": r.stderr.strip()}, 1)
    emit({"ok": True, "combo": args.combo})


def cmd_paste(args):
    text = sys.stdin.read() if args.stdin else args.text
    if text is None:
        emit({"ok": False, "error": "paste requires --text or --stdin"}, 2)
    r = run(["pbcopy"], input_text=text, timeout=5)
    if r.returncode != 0:
        emit({"ok": False, "error": "pbcopy_failed", "stderr": r.stderr.strip()}, 1)
    cmd_key(argparse.Namespace(combo="command+v"))


def pyautogui_backend():
    try:
        import pyautogui
        pyautogui.FAILSAFE = True
        return pyautogui
    except Exception:
        return None


def cmd_mouse(args):
    cliclick = have_bin("cliclick")
    if cliclick:
        if args.mouse_action == "position":
            r = run([cliclick, "p"], timeout=5)
        elif args.mouse_action == "move":
            r = run([cliclick, f"m:{args.x},{args.y}"], timeout=5)
        elif args.mouse_action == "click":
            r = run([cliclick, f"c:{args.x},{args.y}"], timeout=5)
        elif args.mouse_action == "double":
            r = run([cliclick, f"dc:{args.x},{args.y}"], timeout=5)
        elif args.mouse_action == "right":
            r = run([cliclick, f"rc:{args.x},{args.y}"], timeout=5)
        elif args.mouse_action == "drag":
            r = run([cliclick, f"dd:{args.x},{args.y}", f"du:{args.to_x},{args.to_y}"], timeout=10)
        else:
            emit({"ok": False, "error": "unknown_mouse_action"}, 2)
        if r.returncode != 0:
            emit({"ok": False, "backend": "cliclick", "stderr": r.stderr.strip()}, 1)
        emit({"ok": True, "backend": "cliclick", "action": args.mouse_action, "stdout": r.stdout.strip()})
    pag = pyautogui_backend()
    if not pag:
        emit({"ok": False, "error": "no_mouse_backend", "hint": "Install cliclick or pyautogui."}, 1)
    if args.mouse_action == "position":
        p = pag.position()
        emit({"ok": True, "backend": "pyautogui", "x": p.x, "y": p.y})
    if args.mouse_action == "move":
        pag.moveTo(args.x, args.y)
    elif args.mouse_action == "click":
        pag.click(args.x, args.y)
    elif args.mouse_action == "double":
        pag.doubleClick(args.x, args.y)
    elif args.mouse_action == "right":
        pag.rightClick(args.x, args.y)
    elif args.mouse_action == "drag":
        pag.moveTo(args.x, args.y)
        pag.dragTo(args.to_x, args.to_y, duration=args.duration)
    else:
        emit({"ok": False, "error": "unknown_mouse_action"}, 2)
    emit({"ok": True, "backend": "pyautogui", "action": args.mouse_action})


def locate_template_pillow(image_path: Path, template_path: Path, threshold: float, step: int):
    try:
        import numpy as np
        from PIL import Image
    except Exception as e:
        emit({"ok": False, "error": "template_fallback_unavailable", "detail": str(e)}, 1)

    image = Image.open(image_path).convert("L")
    templ = Image.open(template_path).convert("L")
    iw, ih = image.size
    tw, th = templ.size
    if tw > iw or th > ih:
        emit({"ok": False, "error": "template_larger_than_image", "image": [iw, ih], "template": [tw, th]}, 1)

    arr = np.asarray(image, dtype=np.float32)
    target = np.asarray(templ, dtype=np.float32)
    target = target - target.mean()
    target_norm = float(np.linalg.norm(target))
    if target_norm == 0:
        emit({"ok": False, "error": "flat_template"}, 1)

    best_score = -1.0
    best_xy = (0, 0)
    step = max(1, int(step))

    # Normalized correlation. This is slower than OpenCV but good enough for
    # small UI templates and keeps this helper useful without cv2 wheels.
    for y in range(0, ih - th + 1, step):
        for x in range(0, iw - tw + 1, step):
            patch = arr[y:y + th, x:x + tw]
            patch = patch - patch.mean()
            denom = float(np.linalg.norm(patch)) * target_norm
            if denom == 0:
                continue
            score = float((patch * target).sum() / denom)
            if score > best_score:
                best_score = score
                best_xy = (x, y)

    x, y = best_xy
    found = best_score >= threshold
    return {
        "ok": True,
        "backend": "pillow-numpy",
        "found": bool(found),
        "score": best_score,
        "x": int(x + tw / 2),
        "y": int(y + th / 2),
        "threshold": threshold,
        "step": step,
        "template_size": [tw, th],
    }


def cmd_locate_template(args):
    try:
        import cv2
    except Exception as e:
        emit(locate_template_pillow(args.image, args.template, args.threshold, args.step))
    image = cv2.imread(str(args.image))
    templ = cv2.imread(str(args.template))
    if image is None or templ is None:
        emit({"ok": False, "error": "image_or_template_unreadable"}, 1)
    res = cv2.matchTemplate(image, templ, cv2.TM_CCOEFF_NORMED)
    _min_val, max_val, _min_loc, max_loc = cv2.minMaxLoc(res)
    h, w = templ.shape[:2]
    found = max_val >= args.threshold
    emit({"ok": True, "backend": "opencv", "found": bool(found), "score": float(max_val), "x": int(max_loc[0] + w / 2), "y": int(max_loc[1] + h / 2), "threshold": args.threshold})


def main():
    p = argparse.ArgumentParser(description="Local macOS GUI control helper.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("env").set_defaults(func=cmd_env)
    cap = sub.add_parser("capture")
    cap.add_argument("--output", default="/tmp/mac_gui.png")
    cap.add_argument("--raw", action="store_true")
    cap.set_defaults(func=cmd_capture)
    sub.add_parser("front-app").set_defaults(func=cmd_front_app)
    act = sub.add_parser("activate")
    act.add_argument("--app")
    act.add_argument("--path")
    act.set_defaults(func=cmd_activate)
    b = sub.add_parser("bounds")
    b.add_argument("--app", required=True)
    b.set_defaults(func=cmd_bounds)
    k = sub.add_parser("key")
    k.add_argument("--combo", required=True)
    k.set_defaults(func=cmd_key)
    paste = sub.add_parser("paste")
    paste.add_argument("--text")
    paste.add_argument("--stdin", action="store_true")
    paste.set_defaults(func=cmd_paste)
    m = sub.add_parser("mouse")
    m.add_argument("mouse_action", choices=["position", "move", "click", "double", "right", "drag"])
    m.add_argument("--x", type=int)
    m.add_argument("--y", type=int)
    m.add_argument("--to-x", type=int)
    m.add_argument("--to-y", type=int)
    m.add_argument("--duration", type=float, default=0.2)
    m.set_defaults(func=cmd_mouse)
    lt = sub.add_parser("locate-template")
    lt.add_argument("--image", type=Path, required=True)
    lt.add_argument("--template", type=Path, required=True)
    lt.add_argument("--threshold", type=float, default=0.86)
    lt.add_argument("--step", type=int, default=2, help="Fallback scan stride when OpenCV is unavailable.")
    lt.set_defaults(func=cmd_locate_template)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
