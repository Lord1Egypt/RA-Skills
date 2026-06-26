# Wayland click-by-element (SOM): the hybrid coordinate technique

Why "click the element labeled Save" appears impossible on GNOME/Wayland, and the
**working** way to do it anyway. Backs `locate-element` (Capability B+) in SKILL.md.
Verified end-to-end on Ubuntu 26.04, GNOME Shell 50, Wayland.

## The problem (and why naive AT-SPI fails)

- Under **X11**, `Atspi.Component.get_extents(ATSPI_COORD_TYPE_SCREEN)` returned real
  screen rects because every app shared one global coordinate space the X server owned.
- **Wayland deliberately removes global coordinates** — a client never learns where its
  surface sits on screen (isolation/security by design). So toolkits return `(0,0)` for
  SCREEN extents. On GTK4/Electron this is universal; GTK3/Qt/Xwayland sometimes still fill them.
- Net effect: walking the AT-SPI tree gives you element **roles + names** but
  `get_extents(SCREEN)` is `(0,0)` → you can't turn "the Save button" into a click point
  the naive way. This is the wall Dogtail and Talon hit too; their standard workaround is
  vision/OCR → synthesized input.

## The fix: compose WINDOW-relative extents with the window's screen origin

The key empirical finding (this is what unlocks it):

> **`get_extents(ATSPI_COORD_TYPE_WINDOW)` IS populated on GTK4/Electron even when SCREEN is (0,0).**
> Verified: gnome-text-editor reported 81 window-sized elements, Nautilus 181, where every
> SCREEN extent was 0.

And Mutter (the compositor) *does* know each window's screen position — surfaced by the
**Window Calls** extension's `Details(<id>)` → `{x, y, width, height, ...}`. Compose them:

```
abs_x = window_origin_x + element_window_x + element_w / 2
abs_y = window_origin_y + element_window_y + element_h / 2
```

Then `ydotool mousemove -a -x abs_x -y abs_y; ydotool click 0xC0`. Proven: computed a text
widget at `(1920, 3244)`, clicked it, typed — **confirmed the text landed by reading the
document back via `Atspi.Text.get_text`** (not just a screenshot guess).

## Recipe (what `locate-element` automates)

1. `Atspi.init()`; `Atspi.get_desktop(0)`; find the app child whose name matches (AT-SPI app
   name e.g. `gnome-text-editor`).
2. Recurse; for each element read `get_extents(Atspi.CoordType.WINDOW)`; keep those with `w>0 and h>0`
   matching the requested role/name (case-insensitive substring).
3. Resolve the window's screen origin via Window Calls `List` → match wm_class → `Details(id)`.
   **wm_class ≠ AT-SPI app name** (`org.gnome.TextEditor` vs `gnome-text-editor`) — normalize
   by stripping `org.gnome./com.` prefixes and dashes/dots before matching.
4. Compute abs center, drive ydotool.

## Gotchas (all hit live)

- **Focus / link-detection races.** GTK editors auto-detect URL-like substrings; a click can
  land on a detected "link" overlay instead of the text caret, so typed text silently goes
  nowhere. Mitigate: click, then a settling key (`Ctrl+End` to move to a known caret position)
  before typing, and **verify by reading element text back via AT-SPI**, not by screenshot OCR.
- **wm_class vs app-name mismatch** (above) — match loosely both directions + normalized.
- **Window Calls / extensions flip INACTIVE** after any Shell state change — D-Bus path
  `/org/gnome/Shell/Extensions/Windows` returns `UnknownMethod`/`Object does not exist`.
  Fix = `sudo systemctl restart gdm3` (a disable/enable cycle is NOT enough). Same gotcha as
  `allow-gnome-screenshot`. Re-check `gnome-extensions info <ext> | grep State` → ACTIVE.
- Requires `gsettings set org.gnome.desktop.interface toolkit-accessibility true` and ydotoold running.

## VLM fallback (the real remaining edge)

Some elements zero **even WINDOW** extents (deeply custom-drawn canvases, some Electron
internals). For those only: `screenshot-display --window 'wm_class=X' --out /tmp/w.png` →
`vision_analyze` for pixel coords → `ydotool mousemove -a -x X -y Y`. `locate-element` exits
non-zero and prints this recipe automatically when no element has non-zero WINDOW extents.

## Newton: NOT usable today (don't wait for it)

Newton is the clean upstream Wayland-native a11y rewrite (Sovereign-Tech-Fund-funded,
AccessKit-based, Matt Campbell). As of the 2024-06 update it **still lacks window coordinates
and synthesized mouse events**, GNOME Shell itself still uses old AT-SPI, and it only ships on
GNOME 46 prototype branches. It does NOT work on a GNOME 50 box. AccessKit already gives GTK4
real a11y trees on Windows/macOS — proving the data exists at the toolkit layer; it's purely
the Wayland transport that drops coordinates, which the hybrid recovers. Track Newton; depend
on the hybrid.

Refs: GNOME a11y bugzilla #797424 ("window frame coordinates always 0,0 on wayland", RESOLVED
OBSOLETE); gnome-remote-desktop issue #249; Newton update (blogs.gnome.org/a11y 2024-06-18);
github.com/splondike/wayland-accessibility-notes.
