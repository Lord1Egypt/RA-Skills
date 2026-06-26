---
name: peekaboo-linux-gnome-wayland-computer-use
description: See and control GNOME Wayland desktops using gnome-screenshot, ydotool, Window Calls, AT-SPI hybrid element coordinates, and optional GNOME Remote Desktop. The Linux/Wayland counterpart to macOS computer-use ("peekaboo") — a native agent on the box can screenshot, reason over the image, locate UI elements by role/name, and click/type them, with no human, no RDP, and no global-coordinate accessibility. Covers the native single-actor loop, the remote-over-SSH path, and an optional RDP fallback for hands-on human access.
metadata: {"clawdbot":{"emoji":"🖥️","os":["darwin","linux"]}}
---

# peekaboo-linux-gnome-wayland-computer-use

The Linux/Wayland counterpart to macOS computer-use — *"see and poke the screen of a box for
troubleshooting or automation."* On macOS that's trivial (CGWindowList + CGEvent + AX tree). On
**GNOME/Wayland it's locked down by design**, but it can be made to work end-to-end:

- **See** → `gnome-screenshot` (re-enabled on GNOME 49+ via a small GNOME extension).
- **Act** → `ydotool` (writes to `/dev/uinput`, no root).
- **Target elements** → AT-SPI **WINDOW**-relative extents + the **Window Calls** extension's
  window origin, composed into real absolute click coordinates (works where naive AT-SPI returns `(0,0)`).
- **Hands-on (optional)** → GNOME Remote Desktop in Remote-Login mode for a human at an RDP client.

Both the "see" and "act" sides work **natively** (an agent process running ON the box) and
**remotely** (from another machine over SSH). A native agent is a **single actor** — it can
screenshot, analyze, then ydotool-click in one loop. No second machine, no human, no RDP roundtrip.

Context tags below — `[NATIVE]` = an agent process running ON the GNOME box (sharing the desktop
session of `user@1000`); `[REMOTE]` = on another machine, reaching the box over SSH.

> Verified on Ubuntu 26.04 LTS + GNOME Shell 50 (Wayland), NVIDIA + AMD multi-GPU, multi-monitor.
> Substitute your own host/user where the examples use `USER@HOST` and `/run/user/UID`.

## Capability matrix

| Capability | Native (on box) | Remote (from another machine) |
|---|---|---|
| **Screenshot** | yes — `gnome-screenshot -f out.png` (extension unlocks it) | yes — same over SSH, then scp the file |
| **Inject input** (mouse/keys) | yes — ydotool via `/dev/uinput` (no root) | yes — over SSH, same ydotool |
| **Click element by role/name** | yes — `locate-element` (AT-SPI WINDOW extents + Window Calls origin) | yes — same over SSH |
| **Full see→reason→act loop** | yes — single actor, no RDP | yes — drive over SSH |
| **Live interactive desktop** | n/a | yes — RDP client (optional, for a human) |

## Target environment assumptions

- A GNOME/Wayland box with a logged-in graphical session (the GUI session must be active on a seat).
- For remote use: SSH access (key-based recommended), and the box's session env exported in
  non-login shells — `XDG_RUNTIME_DIR=/run/user/UID`,
  `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/UID/bus`, `WAYLAND_DISPLAY=wayland-0`, `DISPLAY=:0`.
  (Replace `UID` with the session user's numeric id, e.g. `1000`.)
- If agents run under `systemd --user` with the full graphical session env + lingering enabled,
  they inherit all of the above and survive SSH disconnects.
- `gnome-screenshot` grabs the **full virtual desktop** (all monitors stitched). On multi-4K
  setups that's huge — use `-w` (focused window) or the per-display helper below.

## CAPABILITY A — Screenshot (the key unlock)

GNOME 49+ revoked `gnome-screenshot`'s access to the private Shell screenshot API, so on a stock
box every headless capture path is dead (see "why" below). The fix is the **`allow-gnome-screenshot`
extension** (https://github.com/siddhpant/allow-gnome-screenshot, GNOME 49/50): it re-adds
`org.gnome.Screenshot` to the Shell's `_senderChecker._allowlistMap`, so the **`gnome-screenshot`
binary specifically** regains access. It is scoped to that one sender — it does NOT enable global
`unsafe_mode`.

`[NATIVE]` — just call it (session env already present):
```bash
gnome-screenshot -f /tmp/shot.png        # full virtual desktop (all monitors)
gnome-screenshot -w -f /tmp/shot.png     # focused window only (smaller)
gnome-screenshot -a -f /tmp/shot.png     # interactive area (needs a human at the screen — avoid headless)
# then hand /tmp/shot.png to your image-analysis step
```
`[REMOTE]` — over SSH, then pull it back:
```bash
ssh USER@HOST '
  export XDG_RUNTIME_DIR=/run/user/UID DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/UID/bus
  gnome-screenshot -f /tmp/shot.png'
scp USER@HOST:/tmp/shot.png /tmp/   # then analyze it
```

**Sanity-check the capture** — a 4K full-desktop PNG is ~15-20 MB; a tiny/near-empty file or an
all-black image means the extension got disabled or the session dropped to the GDM greeter. Quick
non-black check:
`python3 -c "from PIL import Image; im=Image.open('/tmp/shot.png').convert('RGB'); d=list(im.getdata()); print(sum(1 for p in d[::997] if p!=(0,0,0)))"` → should be well >0.

### Installing the extension from scratch
```bash
# [NATIVE or over SSH with the session env exported]
sudo apt-get install -y gnome-screenshot
D=~/.local/share/gnome-shell/extensions/allow-gnome-screenshot@siddh.me
git clone --depth 1 https://github.com/siddhpant/allow-gnome-screenshot.git /tmp/ags
mkdir -p "$D" && cp -r /tmp/ags/allow-gnome-screenshot@siddh.me/* "$D/"
sudo systemctl restart gdm3      # reload the Shell so it discovers the extension (see WARNING below)
# after the session returns:
export XDG_RUNTIME_DIR=/run/user/UID DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/UID/bus
gnome-extensions enable allow-gnome-screenshot@siddh.me
gnome-extensions info allow-gnome-screenshot@siddh.me | grep State   # expect ACTIVE
```

### Per-display capture (capture ONE monitor, not the stitched canvas)

`gnome-screenshot -f` grabs the **entire** virtual desktop. On multi-monitor setups that's a huge,
mostly-empty canvas. To get a single clean display, use the bundled **`screenshot-display`** helper
(`scripts/screenshot-display.py`). It reads live monitor geometry from Mutter DisplayConfig and
crops the full capture to the chosen monitor.

```bash
screenshot-display --list                               # enumerate monitors + geometry
screenshot-display --monitor primary --out /tmp/p.png   # primary (default)
screenshot-display --monitor DP-4   --out /tmp/m.png    # by connector name
screenshot-display --monitor 2      --out /tmp/m.png    # by index (0-based, sorted L->R, T->B)
screenshot-display --monitor active --out /tmp/w.png    # the FOCUSED WINDOW (best "being worked on" signal)
```
Each per-monitor crop is a clean single-display image — feed it straight to your vision step.
`[REMOTE]`: run `screenshot-display` over SSH (export the session env), then scp the output back.

### Window targeting — screenshot a specific program / the display it's on

`Shell.Eval`/`Introspect` are locked, but the **Window Calls extension**
(https://github.com/ickyicky/window-calls, GNOME 45-50) exposes window list + geometry over D-Bus
at `/org/gnome/Shell/Extensions/Windows`. The `screenshot-display` helper uses it to find and crop
to a window or its monitor:

```bash
screenshot-display --list-windows                       # wm_class, id, focus, monitor, title
screenshot-display --window focused      --out /tmp/w.png   # crop to focused window's exact rect
screenshot-display --window "wm_class=firefox" --out /tmp/w.png  # match by wm_class substring
screenshot-display --window "title=Settings"   --out /tmp/w.png  # match by title substring
screenshot-display --window-display focused        --out /tmp/d.png  # the whole MONITOR that window sits on
screenshot-display --window-display "wm_class=Code" --out /tmp/d.png  # monitor a matched window is on
```
Flow: `List` → pick window (focused / wm_class / title) → `Details` gives `x,y,width,height,monitor`
→ helper crops the full capture to the window rect, or to whichever monitor's rect contains the
window's center. (`Details` works; `GetFrameBounds` is broken in this ext version — the helper
doesn't use it.)

**Full setup/enablement guide** to replicate on any GNOME/Wayland box:
`references/peekaboo-and-rdp-setup-ubuntu-gnome-wayland.md`.

## CAPABILITY B — Input injection (ydotool)

ydotool writes to `/dev/uinput` below the display server (the input analog of the screenshot
unlock). Install it, run `ydotoold` as a persistent user service (socket
`/run/user/UID/.ydotool_socket`), and ACL `/dev/uinput` to your user (no root needed at runtime).

`[NATIVE]`:
```bash
export YDOTOOL_SOCKET=/run/user/UID/.ydotool_socket
ydotool mousemove -a 960 540     # absolute pixel coords (no element targeting)
ydotool click 0xC0               # left click down+up
ydotool type "hello"
ydotool key 28:1 28:0            # Enter (keycode:press / keycode:release)
```
`[REMOTE]`:
```bash
ssh USER@HOST '
  export XDG_RUNTIME_DIR=/run/user/UID YDOTOOL_SOCKET=/run/user/UID/.ydotool_socket
  ydotool mousemove -a 700 400; ydotool click 0xC0; ydotool type "hi"'
```
If `ydotoold.service` is down — `systemctl --user enable --now ydotoold.service`. For element
targeting (not blind coords) use the `locate-element` helper below.

## CAPABILITY B+ — Click an element by role/name (SOM via hybrid coords)

**You do NOT need blind pixel guessing or a vision round-trip for most clicks.** The bundled
**`locate-element`** helper (`scripts/locate-element.py`) resolves a UI element to a real absolute
coordinate and clicks/types it.

**Why it works when AT-SPI looks broken:** on Wayland, `getExtents(SCREEN)` returns `(0,0)` for
GTK4/Electron (no global coordinates by design), so naive AT-SPI clicking fails. But
`getExtents(WINDOW)` (widget-relative) **is** populated, and **Window Calls** gives the window's
screen origin from Mutter's privileged view. The helper composes them:
`abs = window_origin + window_relative_extents + size/2`. Proven on GTK4 apps.

```bash
locate-element --app gnome-text-editor --list                       # list elements + computed ABS coords
locate-element --app gnome-text-editor --role text --click          # click first text widget
locate-element --app org.gnome.Nautilus --name "New Folder" --click  # click by visible label
locate-element --app gnome-text-editor --role text --click --type "hello"   # click then type
locate-element --window-id 1367000216 --role "push button" --name Open --click  # by explicit window id
locate-element --app firefox --name Reload --print                  # just print "X Y", act yourself
```
- `--app` matches the AT-SPI app name AND wm_class loosely (normalizes `org.gnome.TextEditor` ↔ `gnome-text-editor`).
- `--role`/`--name` are case-insensitive substring filters; `--index N` picks the Nth match.
- Needs `toolkit-accessibility=true` (`gsettings set org.gnome.desktop.interface toolkit-accessibility true`),
  Window Calls active, and ydotoold running.

**Vision fallback (only when an element zeros even WINDOW extents** — custom-drawn canvases, some
Electron internals): `locate-element` exits non-zero and prints the fallback recipe —
`screenshot-display --window 'wm_class=X' --out /tmp/w.png` → analyze for pixel coords →
`ydotool mousemove -a -x X -y Y`.

Deep dive on the technique, the gotchas, and why Newton isn't a substitute yet:
`references/wayland-atspi-hybrid-som.md`.

## The native loop (single actor — the whole point)

```
[NATIVE agent on the box]
  1. gnome-screenshot -f /tmp/s.png
  2. analyze /tmp/s.png  → "the Save button is at ~(1820, 640)"
  3. ydotool mousemove -a 1820 640 && ydotool click 0xC0
  4. gnome-screenshot again → verify it landed
```
No second machine, no human, no RDP. For element targeting prefer `locate-element` over blind coords.

## Window actions (focus / move / resize / close)

Window Calls also does focus/move/resize/close verbs (window id from `--list-windows`):
```bash
WIN=/org/gnome/Shell/Extensions/Windows
gdbus call --session --dest org.gnome.Shell --object-path $WIN --method $WIN.Activate <id>   # focus/raise
gdbus call --session --dest org.gnome.Shell --object-path $WIN --method $WIN.Move <id> <x> <y>
gdbus call --session --dest org.gnome.Shell --object-path $WIN --method $WIN.Resize <id> <w> <h>
gdbus call --session --dest org.gnome.Shell --object-path $WIN --method $WIN.Maximize <id>
gdbus call --session --dest org.gnome.Shell --object-path $WIN --method $WIN.Close <id>
```
Flow: `Activate <id>` → `screenshot-display --window focused` → `ydotool` interact.

## CAPABILITY C — Live interactive desktop via RDP (optional, for a human)

For a person to drive the desktop hands-on from another machine, use **GNOME Remote Desktop** in
**Remote Login** mode (system/headless, fresh negotiated display — NOT Desktop Sharing, which
mirrors the physical multi-monitor desktop and re-hits the huge-canvas problem).

- Mode: `grdctl --system` (system service `gnome-remote-desktop.service`, enabled at boot).
- Listener: `*:3389` — **always LAN-scope it in your firewall, never any-source.**
- TLS cert at `/var/lib/gnome-remote-desktop/rdp-tls.{crt,key}`.
- Credentials: a device user + password over NLA. Setting the device cred = the Linux user's
  password makes both stages (NLA device prompt, then GDM login) take the same credential.

Connect from a client (Microsoft Remote Desktop / Windows App, or any RDP client) → `HOST` → device
user/pass → GDM → sign in as the Linux user.

**⚠️ #1 RDP gotcha — credential changes need a daemon restart.** `grdctl --system rdp set-credentials`
writes the keyfile but the **running daemon does NOT hot-reload it into its NTLM SAM**. Until you
`sudo systemctl restart gnome-remote-desktop.service`, NLA fails for every client:
`ntlm_fetch_ntlm_v2_hash: Could not find user in SAM database` → `SEC_E_NO_CREDENTIALS` →
`transport_accept_nla: client authentication failure`. Meanwhile `grdctl status` shows the correct
creds (it reads the file). Clients report this as **`FREERDP_ERROR_CONNECT_TRANSPORT_FAILED`** (RoyalTS)
or `ERRCONNECT_AUTHENTICATION_FAILED` (FreeRDP) — looks like transport/cert, is actually stale creds.
Fix: set creds (password via STDIN) → **restart the service** → verify journald shows no `SAM`/
`NO_CREDENTIALS` errors. Server requires NLA (`HYBRID_REQUIRED_BY_SERVER`) — expected.

**Diagnosing any RDP auth failure: read the SERVER's journald, not the client error string.**
Client errors all collapse different server causes into the same opaque message. Full server-log→cause
map, the `+auth-only`/`/sec:tls` client probes, the cert/listener sanity checks, AND the
**empty-server-log case** (tcpdump proves client-vs-network — e.g. a GUI client completing TCP then
sending zero RDP bytes = client-side engine fault, fixed by recreating the connection, not touching
the server): `references/rdp-auth-diagnosis-server-side.md`.

For **automated capture you do NOT need RDP** — Capability A is simpler. RDP is for a human.
Full setup steps: `references/peekaboo-and-rdp-setup-ubuntu-gnome-wayland.md` (Step 7).

## Why the stock capture paths fail (so you don't waste time re-testing)

1. `gnome-screenshot` WITHOUT the extension → exit 0 but no file (`AccessDenied` to the private API under the hood).
2. Raw `gdbus`/`busctl` call to `org.gnome.Shell.Screenshot` → `AccessDenied`. The extension allowlists the **`gnome-screenshot` binary's** D-Bus name, not arbitrary callers — so capture must go through the `gnome-screenshot` binary, not a hand-rolled gdbus call.
3. `xdg-desktop-portal` `Screenshot` → no Response even with the PermissionStore granted (forced interactive dialog).
4. `org.gnome.Mutter.ScreenCast.CreateSession` → `Session creation inhibited` (gated to grd itself).
5. `ffmpeg kmsgrab` (KMS framebuffer) → "No usable planes" on NVIDIA proprietary KMS. `/dev/fb0` → all-black (GNOME doesn't scan out to fb0).
6. `grim` → wlroots-only, fails on Mutter. Don't `apt install grim`.
7. `enable unsafe_mode` via gdb injection into gnome-shell → **CRASHES the Shell, drops the desktop to the GDM greeter.** Do NOT use the gdb method. The extension is the safe, scoped, persistent unlock.

No usable **screen-coordinate** accessibility on Wayland — AT-SPI `getExtents(SCREEN)` is (0,0) on
GTK4/Electron. BUT this is **solved** by Capability B+ (`locate-element`): WINDOW-relative AT-SPI
extents + Window Calls window origin → real click coords. Use `locate-element` for "click element
labeled Save"; fall back to vision-locate only where even WINDOW extents are zero.

## Pitfalls

- The screenshot unlock is **binary-scoped** — only the `gnome-screenshot` binary is allowlisted. A raw gdbus Screenshot call still fails. Always shell out to `gnome-screenshot`.
- **Reloading the Shell on Wayland = restarting GDM** (`sudo systemctl restart gdm3`). There's no in-place `Alt+F2 r` over SSH. The **live GUI session is briefly torn down**, so don't do it mid-GUI-task. If autologin is enabled the desktop recovers in ~12s; `systemd --user` services survive if lingering is on. Verify recovery: `loginctl list-sessions` shows a `seat0` `Type=wayland Active=yes` session.
- **Never use the gdb `unsafe_mode` injection** — it crashes gnome-shell. Use the extension.
- **The `allow-gnome-screenshot` extension can silently flip to INACTIVE** (its allowlist hook only re-arms on a fresh Shell init). Symptom: `gnome-screenshot -f` exits 0 but writes no file. A disable/enable cycle is NOT enough — it needs a Shell reload (`sudo systemctl restart gdm3`) to re-arm. If you depend on capture in an automated loop, verify the file exists each time and reload-on-miss. (Window Calls can flip too — re-enable after any GDM restart.)
- `gnome-screenshot -a` (interactive area) needs a human at the screen — useless headless; use `-f` (full) or `-w` (window).
- Full-desktop shots are huge (multi-4K). Prefer `-w`, or downscale before analysis.
- ydotool needs `ydotoold` alive + `YDOTOOL_SOCKET`/`XDG_RUNTIME_DIR`. Re-enable if it dies. Raw `ydotool` is blind absolute pixels — prefer `locate-element` (Capability B+) for element targeting.
- A **detached SSH session** isn't fully in the graphical session — export `XDG_RUNTIME_DIR=/run/user/UID` (+ DBUS) explicitly. A native `systemd --user` service already has it.
- Always LAN-scope RDP (3389) and SSH (22) in your firewall — never any-source.
