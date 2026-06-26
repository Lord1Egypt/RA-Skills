#!/usr/bin/env python3
"""Capture the GNOME/Wayland desktop, a single monitor, or a specific window
(peekaboo-style per-display / per-window).

Reads live monitor geometry from Mutter DisplayConfig and (optionally) window
geometry from the Window Calls extension, captures the full virtual desktop via
gnome-screenshot (needs the allow-gnome-screenshot extension), then crops.

Usage:
  screenshot-display --list                       # enumerate monitors
  screenshot-display --list-windows               # enumerate open windows (needs Window Calls ext)
  screenshot-display --monitor primary            # primary monitor (default)
  screenshot-display --monitor DP-4               # monitor by connector name
  screenshot-display --monitor 2                  # monitor by index (sorted L->R, T->B)
  screenshot-display --window focused             # crop to the focused window's rect
  screenshot-display --window "wm_class=firefox"  # crop to first window matching wm_class substring
  screenshot-display --window "title=Settings"    # crop to first window whose title contains text
  screenshot-display --window-display focused      # crop to the MONITOR the focused window is on
  screenshot-display --window-display "wm_class=Code"  # crop to the monitor that window sits on
Add --out PATH to control the output file.
"""
import argparse, json, os, subprocess, sys, tempfile

WINDOWS_DEST = "org.gnome.Shell"
WINDOWS_PATH = "/org/gnome/Shell/Extensions/Windows"
WINDOWS_IFACE = "org.gnome.Shell.Extensions.Windows"

def _env():
    e = dict(os.environ)
    e.setdefault("XDG_RUNTIME_DIR", "/run/user/%d" % os.getuid())
    e.setdefault("DBUS_SESSION_BUS_ADDRESS", "unix:path=%s/bus" % e["XDG_RUNTIME_DIR"])
    return e

def _bus():
    import gi
    gi.require_version("Gio", "2.0")
    from gi.repository import Gio
    return Gio, Gio.bus_get_sync(Gio.BusType.SESSION, None)

def get_monitors():
    """List of {connector,x,y,w,h,primary} in logical pixels, sorted L->R, T->B."""
    Gio, bus = _bus()
    res = bus.call_sync("org.gnome.Mutter.DisplayConfig", "/org/gnome/Mutter/DisplayConfig",
                        "org.gnome.Mutter.DisplayConfig", "GetCurrentState", None,
                        None, Gio.DBusCallFlags.NONE, -1, None).unpack()
    serial, monitors, logical, props = res
    cur = {}
    for mon in monitors:
        (conn, vendor, prod, ser), modes, mprops = mon
        for m in modes:
            mid, mw, mh, rr, scale, scales, mp = m
            if mp.get("is-current"):
                cur[conn] = (mw, mh)
    out = []
    for lm in logical:
        x, y, scale, transform, primary, mons, lprops = lm
        conn = mons[0][0]
        w, h = cur.get(conn, (0, 0))
        out.append({"connector": conn, "x": int(x), "y": int(y),
                    "w": int(w/scale), "h": int(h/scale), "primary": bool(primary)})
    out.sort(key=lambda m: (m["x"], m["y"]))
    return out

def _win_call(method, *args):
    Gio, bus = _bus()
    from gi.repository import GLib
    variant = GLib.Variant("(%s)" % ("u"*len(args)), tuple(args)) if args else None
    r = bus.call_sync(WINDOWS_DEST, WINDOWS_PATH, WINDOWS_IFACE, method, variant,
                      None, Gio.DBusCallFlags.NONE, -1, None).unpack()
    return r[0]

def list_windows():
    """Return list of window dicts (needs Window Calls extension)."""
    try:
        return json.loads(_win_call("List"))
    except Exception as e:
        sys.stderr.write("window list failed (is the 'Window Calls' extension enabled?): %s\n" % e)
        return []

def window_details(wid):
    return json.loads(_win_call("Details", int(wid)))

def pick_window(spec):
    wins = list_windows()
    if not wins:
        return None
    if spec == "focused":
        w = next((w for w in wins if w.get("focus")), None)
        return window_details(w["id"]) if w else None
    if "=" in spec:
        field, _, needle = spec.partition("=")
        needle = needle.lower()
        for w in wins:
            if needle in str(w.get(field, "")).lower():
                return window_details(w["id"])
    return None

def capture_full():
    tmp = tempfile.mktemp(suffix=".png")
    subprocess.run(["gnome-screenshot", "-f", tmp], env=_env(), check=True, timeout=30)
    return tmp

def crop_save(rect, out):
    from PIL import Image
    tmp = capture_full()
    im = Image.open(tmp)
    x, y, w, h = rect
    x = max(0, x); y = max(0, y)
    crop = im.crop((x, y, min(x+w, im.width), min(y+h, im.height)))
    crop.save(out)
    os.unlink(tmp)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--monitor", default=None)
    ap.add_argument("--window", default=None)
    ap.add_argument("--window-display", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--list-windows", action="store_true")
    a = ap.parse_args()

    if a.list:
        for i, m in enumerate(get_monitors()):
            print("%d  %-6s %dx%d+%d+%d%s" % (i, m["connector"], m["w"], m["h"], m["x"], m["y"], "  (primary)" if m["primary"] else ""))
        return 0
    if a.list_windows:
        for w in list_windows():
            print("%-12s id=%-12s focus=%-5s mon=%s  %s" % (
                w.get("wm_class",""), w.get("id",""), w.get("focus"), w.get("monitor",""), w.get("title","")))
        return 0

    if a.window:
        d = pick_window(a.window)
        if not d:
            sys.stderr.write("no window matched %r; try --list-windows\n" % a.window); return 2
        out = a.out or os.path.expanduser("~/screenshot-window-%s.png" % d.get("wm_class","win"))
        crop_save((d["x"], d["y"], d["width"], d["height"]), out)
        print(out); return 0

    if a.window_display:
        d = pick_window(a.window_display)
        if not d:
            sys.stderr.write("no window matched %r; try --list-windows\n" % a.window_display); return 2
        cx, cy = d["x"] + d["width"]//2, d["y"] + d["height"]//2
        sel = next((m for m in get_monitors() if m["x"] <= cx < m["x"]+m["w"] and m["y"] <= cy < m["y"]+m["h"]), None)
        if not sel:
            sys.stderr.write("could not map window to a monitor\n"); return 2
        out = a.out or os.path.expanduser("~/screenshot-%s.png" % sel["connector"])
        crop_save((sel["x"], sel["y"], sel["w"], sel["h"]), out)
        print(out); return 0

    mons = get_monitors()
    key = a.monitor or "primary"
    if key == "primary":
        sel = next((m for m in mons if m["primary"]), mons[0])
    elif key.isdigit():
        sel = mons[int(key)]
    else:
        sel = next((m for m in mons if m["connector"] == key), None)
    if not sel:
        sys.stderr.write("monitor %r not found; use --list\n" % key); return 2
    out = a.out or os.path.expanduser("~/screenshot-%s.png" % sel["connector"])
    crop_save((sel["x"], sel["y"], sel["w"], sel["h"]), out)
    print(out); return 0

sys.exit(main())
