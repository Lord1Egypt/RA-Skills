#!/usr/bin/env python3
"""locate-element: find UI elements via AT-SPI and click/type them on GNOME/Wayland.

On Wayland, AT-SPI getExtents(SCREEN) returns (0,0) for GTK4/Electron, so element
clicking appears broken. This tool uses the HYBRID approach that DOES work:

  absolute_screen_coord = window_origin (from Window Calls ext, Mutter's view)
                        + element_extents(COORD_TYPE_WINDOW)   (from AT-SPI)

It then drives ydotool to click/type. For elements that zero even WINDOW extents
(custom-drawn canvases, some Electron internals), fall back to the VLM loop:
screenshot-display --window ... -> vision model -> ydotool mousemove -a.

Usage:
  locate-element --app gnome-text-editor --list
  locate-element --app gnome-text-editor --role "push button" --name Open --click
  locate-element --app org.gnome.Nautilus --name "New Folder" --click
  locate-element --window-id 4249767539 --role text --click --type "hello"
  locate-element --app firefox --name Reload --print          # just print coords

Matching: --role / --name are case-insensitive substring filters. First visible
element with non-zero WINDOW extents wins (or use --index N to pick the Nth match).

Requires: python3-gi (Atspi), the 'Window Calls' GNOME extension, ydotool +
ydotoold running, and accessibility enabled
(`gsettings set org.gnome.desktop.interface toolkit-accessibility true`).
"""
import argparse, json, os, subprocess, sys, time

WINDOWS_DEST = "org.gnome.Shell"
WINDOWS_PATH = "/org/gnome/Shell/Extensions/Windows"
WINDOWS_IFACE = "org.gnome.Shell.Extensions.Windows"


def _env():
    e = dict(os.environ)
    e.setdefault("XDG_RUNTIME_DIR", "/run/user/%d" % os.getuid())
    e.setdefault("DBUS_SESSION_BUS_ADDRESS", "unix:path=%s/bus" % e["XDG_RUNTIME_DIR"])
    e.setdefault("YDOTOOL_SOCKET", "%s/.ydotool_socket" % e["XDG_RUNTIME_DIR"])
    return e


def _win_call(method, *args):
    import gi
    gi.require_version("Gio", "2.0")
    from gi.repository import Gio, GLib
    bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    variant = GLib.Variant("(%s)" % ("u" * len(args)), tuple(args)) if args else None
    r = bus.call_sync(WINDOWS_DEST, WINDOWS_PATH, WINDOWS_IFACE, method, variant,
                      None, Gio.DBusCallFlags.NONE, -1, None).unpack()
    return r[0]


def list_windows():
    try:
        return json.loads(_win_call("List"))
    except Exception as e:
        sys.stderr.write("window list failed (is 'Window Calls' enabled?): %s\n" % e)
        return []


def window_details(wid):
    return json.loads(_win_call("Details", int(wid)))


def _norm(s):
    s = (s or "").lower()
    for p in ("org.gnome.", "org.kde.", "com.", "org."):
        if s.startswith(p):
            s = s[len(p):]
    return s.replace("-", "").replace("_", "").replace(".", "")


def resolve_window(app=None, window_id=None, title=None):
    """Return (window_id, origin_x, origin_y) for the target window.

    Matches `app` against wm_class loosely: substring either direction, plus a
    normalized form (strips org.gnome./com. prefixes, dashes, dots) so an AT-SPI
    app name like 'gnome-text-editor' matches wm_class 'org.gnome.TextEditor'.
    """
    if window_id is not None:
        d = window_details(window_id)
        return int(window_id), d["x"], d["y"]
    wins = list_windows()
    if not wins:
        return None
    na = _norm(app) if app else None
    cand = None
    for w in wins:
        wm = str(w.get("wm_class", "")).lower()
        ti = str(w.get("title", "")).lower()
        if app and (app.lower() in wm or wm in app.lower() or (na and na in _norm(wm)) or (na and _norm(wm) in na)):
            cand = w; break
        if title and title.lower() in ti:
            cand = w; break
    if cand is None and (app or title):
        return None
    if cand is None:
        cand = next((w for w in wins if w.get("focus")), wins[0])
    d = window_details(cand["id"])
    return int(cand["id"]), d["x"], d["y"]


def _atspi():
    import gi
    gi.require_version("Atspi", "2.0")
    from gi.repository import Atspi
    Atspi.init()
    return Atspi


def find_app_root(Atspi, app):
    """Return the AT-SPI application accessible whose name matches `app`."""
    d = Atspi.get_desktop(0)
    matches = []
    for i in range(d.get_child_count()):
        a = d.get_child_at_index(i)
        try:
            nm = a.get_name() or ""
        except Exception:
            nm = ""
        if app is None or app.lower() in nm.lower() or nm.lower() in app.lower():
            matches.append((nm, a))
    return matches


def walk_elements(Atspi, root, role=None, name=None, cap=2000):
    """Yield (element, role_name, name, wx, wy, w, h) with non-zero WINDOW extents."""
    out = []

    def rec(acc, depth=0):
        if len(out) >= cap:
            return
        try:
            rn = acc.get_role_name()
        except Exception:
            rn = "?"
        try:
            nm = acc.get_name() or ""
        except Exception:
            nm = ""
        wx = wy = w = h = 0
        try:
            ew = acc.get_extents(Atspi.CoordType.WINDOW)
            wx, wy, w, h = ew.x, ew.y, ew.width, ew.height
        except Exception:
            pass
        if w > 0 and h > 0:
            role_ok = (role is None) or (role.lower() in rn.lower())
            name_ok = (name is None) or (name.lower() in nm.lower())
            if role_ok and name_ok:
                out.append((acc, rn, nm, wx, wy, w, h))
        try:
            n = acc.get_child_count()
        except Exception:
            n = 0
        for i in range(min(n, 80)):
            try:
                rec(acc.get_child_at_index(i), depth + 1)
            except Exception:
                pass

    rec(root)
    return out


def ydotool(*args):
    subprocess.run(["ydotool", *args], env=_env(), check=True)


def do_click(ax, ay, button="0xC0"):
    ydotool("mousemove", "-a", "-x", str(ax), "-y", str(ay))
    time.sleep(0.2)
    ydotool("click", button)


def main():
    ap = argparse.ArgumentParser(description="Locate & click AT-SPI elements on GNOME/Wayland (hybrid coords).")
    ap.add_argument("--app", help="AT-SPI app name / wm_class substring (e.g. gnome-text-editor, org.gnome.Nautilus)")
    ap.add_argument("--window-id", type=int, help="Explicit Window Calls window id")
    ap.add_argument("--title", help="Match window by title substring")
    ap.add_argument("--role", help="Element role substring (e.g. 'push button', 'text', 'menu button')")
    ap.add_argument("--name", help="Element name/label substring")
    ap.add_argument("--index", type=int, default=0, help="Pick the Nth matching element (default 0)")
    ap.add_argument("--list", action="store_true", help="List matching elements + computed coords, don't act")
    ap.add_argument("--print", dest="just_print", action="store_true", help="Print the absolute click coord only")
    ap.add_argument("--click", action="store_true", help="Click the element")
    ap.add_argument("--right-click", action="store_true", help="Right-click the element")
    ap.add_argument("--type", dest="type_text", help="After locating/clicking, type this text")
    a = ap.parse_args()

    Atspi = _atspi()

    # Resolve the window origin (screen position) via Window Calls.
    win = resolve_window(app=a.app, window_id=a.window_id, title=a.title)
    if not win:
        sys.stderr.write("no window matched (app=%r window_id=%r title=%r); try screenshot-display --list-windows\n"
                         % (a.app, a.window_id, a.title))
        return 2
    wid, ox, oy = win

    # Find the AT-SPI app root and walk for matching elements with WINDOW extents.
    roots = find_app_root(Atspi, a.app or a.title)
    if not roots:
        sys.stderr.write("no AT-SPI app matched %r (is toolkit-accessibility=true and the app a11y-enabled?)\n"
                         % (a.app or a.title))
        return 2
    elements = []
    for _, root in roots:
        elements.extend(walk_elements(Atspi, root, role=a.role, name=a.name))

    if not elements:
        sys.stderr.write("no element matched role=%r name=%r with non-zero WINDOW extents.\n"
                         "  -> Element may zero WINDOW extents (custom canvas/Electron). Use the VLM fallback:\n"
                         "     screenshot-display --window 'wm_class=%s' --out /tmp/w.png ; vision-locate ; ydotool mousemove -a -x X -y Y\n"
                         % (a.role, a.name, a.app or ""))
        return 3

    if a.list:
        for i, (el, rn, nm, wx, wy, w, h) in enumerate(elements):
            ax, ay = ox + wx + w // 2, oy + wy + h // 2
            print("%2d  role=%-16s name=%-28r win=(%d,%d %dx%d)  ABS=(%d,%d)" % (i, rn, nm[:28], wx, wy, w, h, ax, ay))
        return 0

    if a.index >= len(elements):
        sys.stderr.write("--index %d out of range (%d matches)\n" % (a.index, len(elements)))
        return 3
    el, rn, nm, wx, wy, w, h = elements[a.index]
    ax, ay = ox + wx + w // 2, oy + wy + h // 2

    if a.just_print:
        print("%d %d" % (ax, ay))
        return 0

    print("target: role=%s name=%r  ABS=(%d,%d)" % (rn, nm, ax, ay))
    if a.click:
        do_click(ax, ay, "0xC0")
    elif a.right_click:
        do_click(ax, ay, "0xC1")
    if a.type_text:
        time.sleep(0.2)
        ydotool("type", a.type_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
