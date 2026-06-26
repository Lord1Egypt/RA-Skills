# Enabling agent screenshots + input on Ubuntu GNOME/Wayland

Step-by-step to give an agent (or any CLI caller) the ability to **screenshot**, **target
windows/displays**, and **inject input** on an Ubuntu GNOME/Wayland box. Verified on Ubuntu 26.04,
GNOME Shell 50, Wayland. Use this to replicate on any GNOME/Wayland host.

> **Why this is needed:** GNOME 49+ on Wayland revokes the private screenshot API from non-core
> apps and blocks `Shell.Eval`/`Introspect`/`ScreenCast`/`kmsgrab`/`grim`. The only robust, scoped,
> persistent unlock is a pair of GNOME Shell extensions (one per capability) plus a userspace input
> daemon. See the parent SKILL.md "Why the stock capture paths fail" section.

## Prerequisites / facts to confirm first
- `loginctl show-session <ID> -p Type` → `wayland`, and there's an **active** graphical session
  (autologin strongly recommended so a reboot brings the desktop back unattended).
- You can reach the box and run commands as the desktop user with that user's **session bus env**:
  `XDG_RUNTIME_DIR=/run/user/$(id -u)` and
  `DBUS_SESSION_BUS_ADDRESS=unix:path=$XDG_RUNTIME_DIR/bus`. A bare detached SSH session is NOT in
  the graphical session — always export these (a native `systemd --user` service already has them).
- The ability to run `sudo` (passwordless or interactive) for the apt installs + the GDM restart.

## ⚠️ The one disruptive step: reloading GNOME Shell
On Wayland you **cannot** reload the Shell in place (`Alt+F2 r` is X11-only and unavailable over
SSH). Installing an extension requires the Shell to rescan, which means **`sudo systemctl restart
gdm3`**. That briefly tears down the live GUI session:
- With **autologin on**, the desktop user is auto-logged back in ~10-15s — no human needed.
- `systemd --user` services (agent gateways, ydotoold) **survive** if user **lingering** is on
  (`loginctl enable-linger <user>`). Confirm before restarting.
- Do NOT do this mid-GUI-task. Verify recovery after:
  `loginctl list-sessions` shows the user on `seat0` with `Type=wayland Active=yes`.
- **NEVER** try to enable `unsafe_mode` via gdb injection into gnome-shell — it CRASHES the Shell
  (verified — drops the box to the GDM greeter). The extensions are the safe path.
- **Autologin can stall if a stale graphical session lingers.** A GDM restart can leave the greeter
  on seat0 with the old session stuck in `State=closing`/`Active=no` instead of auto-logging back
  in. Fix: `loginctl terminate-session <stale_id>` then `sudo systemctl restart gdm3` again; verify
  a NEW seat0 session shows `Active=yes State=active`.
  Also: toggling `toolkit-accessibility` (for AT-SPI element targeting) can flip extensions to
  INACTIVE until the next Shell reload — re-run `gnome-extensions enable` after the restart.

## Step 1 — Screenshot capability (allow-gnome-screenshot extension)
```bash
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export DBUS_SESSION_BUS_ADDRESS=unix:path=$XDG_RUNTIME_DIR/bus

sudo apt-get install -y gnome-screenshot git python3-gi python3-pil

# allow-gnome-screenshot: re-allowlists the gnome-screenshot binary for the private API.
# Scoped to that one D-Bus sender; does NOT enable global unsafe_mode.
D=~/.local/share/gnome-shell/extensions/allow-gnome-screenshot@siddh.me
git clone --depth 1 https://github.com/siddhpant/allow-gnome-screenshot.git /tmp/ags
mkdir -p "$D" && cp -r /tmp/ags/allow-gnome-screenshot@siddh.me/* "$D/"
```

## Step 2 — Window enumeration / targeting (Window Calls extension)
```bash
# Window Calls: exposes List/Details (geometry + monitor + focus) over D-Bus at
# /org/gnome/Shell/Extensions/Windows. Needed for --window / --window-display targeting.
D=~/.local/share/gnome-shell/extensions/window-calls@domandoman.xyz
git clone --depth 1 https://github.com/ickyicky/window-calls.git /tmp/wc
mkdir -p "$D" && cp /tmp/wc/extension.js /tmp/wc/metadata.json "$D/"
```

## Step 3 — Reload the Shell so it discovers both extensions, then enable
```bash
sudo systemctl restart gdm3        # disruptive — see WARNING above
sleep 14                           # wait for autologin

export XDG_RUNTIME_DIR=/run/user/$(id -u)
export DBUS_SESSION_BUS_ADDRESS=unix:path=$XDG_RUNTIME_DIR/bus
gnome-extensions enable allow-gnome-screenshot@siddh.me
gnome-extensions enable window-calls@domandoman.xyz
gnome-extensions info allow-gnome-screenshot@siddh.me | grep State   # expect ACTIVE
gnome-extensions info window-calls@domandoman.xyz       | grep State   # expect ACTIVE
# Both are now persisted in `org.gnome.shell enabled-extensions` → survive reboot.
```

## Step 4 — Input injection (ydotool + persistent ydotoold user service)
```bash
sudo apt-get install -y ydotool
# /dev/uinput must be writable by the user. If it's not already ACL'd, add a udev rule:
#   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
#     | sudo tee /etc/udev/rules.d/99-uinput.rules
#   sudo usermod -aG input "$USER"   # then re-login
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/ydotoold.service <<'EOF'
[Unit]
Description=ydotool daemon (uinput input injection for headless agents)
After=graphical-session.target
[Service]
ExecStart=/usr/bin/ydotoold --socket-path=%t/.ydotool_socket
Restart=on-failure
[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now ydotoold.service
loginctl enable-linger "$USER"     # so user services survive logout/reboot
```

## Step 5 — Install the helpers
Copy `scripts/screenshot-display.py` and `scripts/locate-element.py` from this skill to
`~/.local/bin/screenshot-display` and `~/.local/bin/locate-element`, `chmod +x` them, and ensure
`~/.local/bin` is on PATH.

## Step 6 — Verify end-to-end
```bash
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export DBUS_SESSION_BUS_ADDRESS=unix:path=$XDG_RUNTIME_DIR/bus
export YDOTOOL_SOCKET=$XDG_RUNTIME_DIR/.ydotool_socket

gnome-screenshot -f /tmp/t.png && ls -l /tmp/t.png         # >0 bytes, not all-black
screenshot-display --list                                  # lists monitors
screenshot-display --list-windows                          # lists open windows
screenshot-display --monitor primary --out /tmp/p.png      # one clean display
screenshot-display --window focused   --out /tmp/w.png      # tight window crop
ydotool mousemove -a 200 200 && ydotool type "ok"          # input works
```
Sanity-check captures aren't black:
`python3 -c "from PIL import Image; d=list(Image.open('/tmp/p.png').convert('RGB').getdata()); print(sum(1 for p in d[::997] if p!=(0,0,0)))"` → should be >0.

## Replicating on another GNOME/Wayland host
- Confirm the GNOME version first (`gnome-shell --version`); both extensions declare 45-50. If it's
  on a different GNOME, check each extension's `metadata.json` `shell-version` before enabling.
- If there's **no autologin**, either enable it (`/etc/gdm3/custom.conf` → `AutomaticLoginEnable=True`
  / `AutomaticLogin=<user>`) before the GDM restart, or do the restart while someone can log in at
  the console — otherwise the desktop session won't come back and the extensions won't load.
- If `/dev/uinput` isn't ACL'd to the user there, use the udev rule in Step 4.
- Deploy the skill (SKILL.md + scripts/) to that host's skills dir(s).

## Tooling versions verified
- allow-gnome-screenshot — siddhpant/master, shell-version 49/50.
- window-calls — ickyicky v1.17, shell-version 45-50 (`List`, `Details` w/ x,y,width,height,monitor,focus; `GetFrameBounds` is broken in this version — use `Details`).
- ydotool 1.0.4-3; gnome-remote-desktop 50.0 (RDP, optional).

## Window actions (focus / move / resize / close) — Window Calls

Beyond capture, Window Calls exposes window-management verbs. All take a window id from `List`.
Useful before screenshotting (focus the target first):

```bash
WIN=/org/gnome/Shell/Extensions/Windows
gdbus call --session --dest org.gnome.Shell --object-path $WIN --method $WIN.Activate <id>      # focus/raise
gdbus call --session --dest org.gnome.Shell --object-path $WIN --method $WIN.Maximize <id>
gdbus call --session --dest org.gnome.Shell --object-path $WIN --method $WIN.Unmaximize <id>
gdbus call --session --dest org.gnome.Shell --object-path $WIN --method $WIN.Move <id> <x> <y>
gdbus call --session --dest org.gnome.Shell --object-path $WIN --method $WIN.Resize <id> <w> <h>
gdbus call --session --dest org.gnome.Shell --object-path $WIN --method $WIN.Close <id>
```
`Activate` focuses the target (confirmed `focus:true` flips to it). Typical flow:
`Activate <id>` → `screenshot-display --window focused` → `ydotool` interact.

## Step 7 (optional) — RDP Remote Login (headless virtual session, for a human)

For a person to drive the desktop hands-on from another machine. Use **Remote Login**
(system/headless, multi-user — fresh negotiated display) NOT Desktop Sharing (mirrors the physical
multi-monitor desktop). Remote Login = `grdctl --system`; a device credential reaches the GDM login
screen.

```bash
SYS=/var/lib/gnome-remote-desktop
# 1) SYSTEM TLS cert (PEM), owned by the grd system user
sudo openssl req -newkey rsa:2048 -nodes -keyout "$SYS/rdp-tls.key" \
     -x509 -days 3650 -out "$SYS/rdp-tls.crt" -subj "/CN=$(hostname)"
sudo chown gnome-remote-desktop:gnome-remote-desktop "$SYS/rdp-tls".{key,crt}
sudo chmod 600 "$SYS/rdp-tls.key"; sudo chmod 644 "$SYS/rdp-tls.crt"
# 2) enable the SYSTEM service + set TLS
sudo systemctl enable --now gnome-remote-desktop.service
sudo grdctl --system rdp set-tls-key  "$SYS/rdp-tls.key"
sudo grdctl --system rdp set-tls-cert "$SYS/rdp-tls.crt"
# 3) device credentials (generate a strong pw; store it in your password manager, don't inline)
sudo grdctl --system rdp set-credentials <rdp-user> <strong-pw>
sudo grdctl --system rdp enable
sudo systemctl restart gnome-remote-desktop.service   # REQUIRED — daemon does NOT hot-reload creds
# 4) verify + LAN-scope the port
sudo grdctl --system status            # Unit active, Status enabled, TLS set (TPM warning is harmless)
sudo ss -tlnp | grep 3389              # listener bound
sudo ufw allow from <your-lan-cidr> to any port 3389 proto tcp comment 'RDP from LAN only'
```

Connect from any RDP client (Microsoft Remote Desktop / Windows App, Remmina, etc.) → host,
user/pass = the device credentials → you land at the GDM login, then sign in as the Linux user.

### Two-stage credentials — why you authenticate twice, and how to unify them
Remote Login is **two-stage by design** (GNOME gnome-remote-desktop issue #249): the RDP **device
credential** (NLA/NTLM) only gets you to the **GDM** screen, where you then log in with the **real
Linux user account** (PAM). These can't be a single credential because **NLA needs a password
*hash* up front while PAM needs plaintext** — incompatible without Kerberos, which no distro ships.

To make it feel like one login, **set the device credential equal to the target user's Linux
password** so the same `user`/`password` works at both prompts:
```bash
# password via STDIN — never as an arg (args leak to ps/process list and shell history)
printf '%s\n' "$THE_USER_PW" | sudo grdctl --system rdp set-credentials <user>
sudo systemctl restart gnome-remote-desktop.service       # apply it to the live daemon
sudo grdctl --system status --show-credentials | grep -iE 'username|password'   # readback to confirm
# verify the unix login password matches (so the GDM stage takes the same pw):
printf '%s\n' "$THE_USER_PW" | su <user> -c 'echo OK'     # prints OK if the pw is correct
```
If the user's Linux password later rotates, re-run the `set-credentials` line **and restart the
service** to keep the two stages in sync.

### Critical gotcha — credential changes need a daemon restart
**`grdctl --system rdp set-credentials` writes the keyfile but the running daemon does NOT
hot-reload it into its NTLM SAM.** Until you `sudo systemctl restart gnome-remote-desktop.service`,
NLA fails for every client with `ntlm_fetch_ntlm_v2_hash: Could not find user in SAM database` →
`SEC_E_NO_CREDENTIALS`. Meanwhile `grdctl status` shows the *correct* creds the whole time (it reads
the file, not the live daemon state) — so don't trust status as proof. Clients surface this as
opaque transport/auth errors (`FREERDP_ERROR_CONNECT_TRANSPORT_FAILED` in RoyalTS,
`ERRCONNECT_AUTHENTICATION_FAILED` in FreeRDP). **Always restart the service after any credential
change**, then watch `sudo journalctl -u gnome-remote-desktop.service -f` during a connect — clean
NTLM/credssp lines with no `SAM`/`NO_CREDENTIALS` errors = the daemon has the creds.

> A note on the FreeRDP CLI: an earlier diagnosis blamed FreeRDP↔grd NTLM `Message Integrity Check
> (MIC) verification failed` errors on a *client-side FreeRDP bug*. That was a mis-diagnosis — the
> real cause was this stale-credential / no-restart issue. After a proper service restart, the
> FreeRDP CLI (`xfreerdp`/`sdl-freerdp`), Microsoft Remote Desktop, and Windows App all authenticate
> cleanly. The server requires NLA (`HYBRID_REQUIRED_BY_SERVER`) — that's expected. See
> `references/rdp-auth-diagnosis-server-side.md` for the full server-log→cause map.

TPM note: `Init TPM credentials failed ... using GKeyFile as fallback` is harmless on boxes without
a usable TPM — grd just stores creds in a keyfile.
