---
name: mac-mini
description: Keep a Mac mini agent host reachable 24/7 without MDM — Tailscale SSH, pmset, auto-login vs FileVault. Use when setting up or recovering an always-on Mac. Trigger on "mac mini", "mac won't come back after reboot", "tailscale ssh", "auto-login".
metadata: {"clawdbot":{"emoji":"🔌","requires":{"bins":["ssh","pmset","fdesetup"]},"homepage":"https://openclaw.ai"}}
---

# Mac mini as an always-on agent host

A Mac agent host is only as available as its worst reboot. **Always-on = power comes back + the disk unlocks + a GUI session opens + the agent's LaunchAgent starts.** Miss one link and the machine is powered, pingable, and useless — often with no way back in from a distance.

## Read first — what this skill changes, and the trade-off it asks you to make

| Item | What happens |
|---|---|
| Remote access | Enables macOS Remote Login (sshd) over a private Tailscale network. No port is opened to the internet. Key-based SSH for daily use. |
| Power | Disables sleep, enables wake-on-network and restart after power loss. |
| Login | Discusses auto-login. **This skill never turns FileVault off and never writes login credentials itself.** A human decides, in System Settings. |
| Permissions | Privacy grants (Accessibility, Screen Recording, Input Monitoring) stay a human click on the machine. Nothing here edits the TCC database. |
| Data | None collected. The only persistent artefacts are the ones you create: a Tailscale node, an `authorized_keys` line, power settings. |

**The core trade-off.** An OpenClaw-style gateway runs as a per-user LaunchAgent: it starts at GUI login, not at boot. After an unattended reboot, something must log a user in. On macOS, automatic login and FileVault are mutually exclusive.

| Option | After a reboot | What you accept |
|---|---|---|
| **A. FileVault on, no auto-login** (the macOS default, and the safer one) | Machine waits at the login window. macOS 26 on Apple Silicon lets you unlock the disk over SSH, but that opens **no GUI session**: the agent stays down until a human logs in (screen sharing or on site). | Downtime after every reboot, power cut and OS update until someone logs in. |
| **B. FileVault off + auto-login** | Machine boots to the desktop, agent restarts alone. | Anyone who takes the machine reads the disk, and the auto-login user's session (and login keychain) is open to anyone at the keyboard. |

Option B is a **deliberate weakening of local security in exchange for availability** — not a best practice. Take it only when all of these hold; otherwise stay on A and plan for human logins:

- the machine is **dedicated** to the agent — no personal mail, no documents, no unrelated accounts;
- it sits in a **locked, physically controlled** place, not a shared desk or a shop floor;
- the auto-login account is a **standard (non-admin) account** that runs only the agent; administration uses a separate admin account whose password is never stored on the machine;
- the agent's credentials are scoped to what it needs and revocable remotely (API keys, not personal passwords);
- the owner of the machine has agreed to it in writing.

Never on a laptop. Set it (or revert it) only through System Settings → Users & Groups → *Automatically log in as*, and System Settings → Privacy & Security → FileVault. Do not script either.

## When to use

| Trigger | Action |
|---|---|
| "set up a new mac mini for the agent" | §Bootstrap checklist, in order, with a human on site for steps 1, 5 and 7 |
| "mac won't come back after reboot" | §Failure tree, top to bottom |
| "can I reach the mac from home?" | §Tailscale — formula, reusable key, key expiry off |
| "the agent is up but can't click anything" | §The walls without MDM — TCC grant |
| "check all the macs" | §Fleet health |
| "sudo pmset worked, didn't it?" | §Power — verify in the same line |

## Bootstrap checklist — order is causal

Work from a remote-desktop session or on site: steps 1, 5 and 7 need a screen. Placeholders are bare words (`HOSTNAME`, `APPNAME`), never `<KEY>` — in zsh, `<` is a redirection. Every `sudo` step runs from the admin account; if you chose Option B, the agent account is standard and has no sudo.

- [ ] **1. Remote desktop as a service, not an app.** Whatever tool you use must be a login item *and* allowed in the background (System Settings → General → Login Items & Extensions), with a permanent unattended password and its privacy grants. A remote-desktop app launched by hand dies with the session — the classic way a Mac becomes unreachable at the login window.
- [ ] **2. Tailscale, formula build** (§Tailscale).
- [ ] **3. Remote Login (sshd)** + your public key in the agent account's `~/.ssh/authorized_keys` (mode 600, dir 700).
- [ ] **4. Power** (§Power), verified in the same line.
- [ ] **5. The login decision** (§Read first): Option A or B, by a human, in System Settings.
- [ ] **6. Agent service** installed as a LaunchAgent of the agent account (see `always-on-agent-ops` for the gateway itself).
- [ ] **7. Privacy grants** clicked once for every binary that drives the GUI.
- [ ] **8. Smart plug** upstream of the Mac if the site may lose power.
- [ ] **9. Reboot drill** with a person on site (§Reboot drill), then §Host report.

## Tailscale — the four decisions that make access permanent

Formula (never `--cask`), started as a root LaunchDaemon so it is up before any login. The auth key goes through a 600 file, read once, then deleted — copy the key first, in the remote-desktop session:

```bash
(umask 077; pbpaste > "$HOME/.tskey")
brew install tailscale
sudo brew services start tailscale
sudo tailscale up --auth-key "file:$HOME/.tskey" --hostname=HOSTNAME; rm -f "$HOME/.tskey"; tailscale ip -4
# Output: the node's Tailscale IPv4 address
```

| Decision | Why | Trap if you skip it |
|---|---|---|
| Formula, not cask | The formula ships the open-source `tailscaled`, which runs **before** any user logs in. The cask is the GUI app: it dies with the session. | A reboot to the login window takes the network down with it — the exact failure you installed Tailscale to survive. |
| Auth key **Reusable** | One key enrols a batch of machines. | A single-use key is consumed by the first Mac; the next ones get a generic `invalid key: API key ... not valid` that never says "already used". |
| **Disable key expiry** per device (admin console → Machines → ⋯) | This click, not the auth key's lifetime, keeps the node on the network. Auth keys only enrol (90 days max) and can be revoked afterwards without cutting anyone. | Node keys expire (default 180 days) and the host silently drops off. |
| Native sshd over Tailscale, **not** `tailscale up --ssh` | Tailscale SSH's default `check` mode re-authenticates in a browser every 12 h. | Every unattended script breaks twice a day. |

`--auth-key file:PATH` keeps the key out of shell history and `ps`. `sudo brew services list` must show `tailscale` started as `root` — listed only under your user means it will not survive logout. The flag is `--auth-key`; `--authkey` is an accepted alias.

```bash
tailscale status --json | python3 -c 'import json,sys; s=json.load(sys.stdin)["Self"]; print(s["HostName"], s["Online"], "KeyExpiry" in s)'
# Output: HOSTNAME True False        <- False = expiry disabled for this node
```

## Remote Login

```bash
sudo launchctl enable system/com.openssh.sshd
sudo launchctl bootstrap system /System/Library/LaunchDaemons/ssh.plist
nc -z -G 3 127.0.0.1 22; echo "sshd=$?"
# Output: sshd=0
```

`Bootstrap failed: 5: Input/output error` = sshd already loaded, harmless. `systemsetup -getremotelogin` can report `Off` while sshd answers — trust the port probe. On macOS 26 + Apple Silicon, enabling Remote Login also enables the **pre-boot FileVault unlock over SSH** (`man apple_ssh_and_filevault`): password authentication, then the connection drops while the data volume mounts; reconnect. It unlocks the disk; it does not log anyone into the GUI.

## Power — verify in the same line

```bash
sudo pmset -a sleep 0 disksleep 0 womp 1 autorestart 1; pmset -g | grep -E '^ *(sleep|disksleep|womp|autorestart) '
# Output:  sleep 0 / disksleep 0 / womp 1 / autorestart 1
```

**A `sudo` that fails leaves no trace you will notice.** Over a remote terminal the password prompt scrolls away, the command "ran", and the setting is unchanged — observed on 5 machines out of 6 in one pass. The verification must be in the **same line**, and a missing `autorestart` line is a fail (hardware without the feature, e.g. laptops, prints nothing). Scripts run over SSH use `sudo -n`: it fails fast with `a password is required` instead of hanging on a prompt nobody sees.

`autorestart` only helps if power **comes back**. A Mac that was switched off, or lost power for good, answers nothing: Wake-on-LAN wakes a sleeping Mac, not a powered-off one, and poorly over Wi-Fi. The only remote fix is a smart plug upstream: cut, restore, `autorestart 1` boots it.

## The walls without MDM

| Wall | Why no shell gets past it | What to do |
|---|---|---|
| Privacy grants (Accessibility, Screen Recording, Input Monitoring) | `tccutil` only **resets**; it has no add verb. `TCC.db` is SIP-protected, even as root. | One human click per binary per machine, in a GUI session. Budget it in the setup visit. |
| `sudo` | Password required; nothing here installs a `sudoers.d` rule. | Human via remote desktop, or `sudo -n` in scripts so it fails loudly. A passwordless sudo rule is a per-machine decision with the owner, not a default. |
| First login of a CLI/agent that authenticates in a browser | Needs a browser in the user's session. | Remote desktop, once. |
| Screen sharing | `sudo launchctl enable system/com.apple.screensharing` + `bootstrap` starts the service, but the ARD `kickstart` tool no longer grants control from the CLI (since 10.14). | Confirm the Screen Sharing toggle in System Settings → General → Sharing, once, on site. |
| Major macOS update | Can reset privacy grants and, reported, re-enable FileVault. | Rerun §Host report after every major update. |

## Host report — the artefact to produce

Run as the agent account, over SSH, after setup, after every OS update, and on any incident:

```bash
{ printf 'filevault: '; fdesetup status | head -1
  printf 'autologin: '; defaults read /Library/Preferences/com.apple.loginwindow autoLoginUser 2>/dev/null || echo none
  printf 'console: '; stat -f %Su /dev/console
  pmset -g | grep -E '^ *(sleep|womp|autorestart) ' | awk '{printf "%s=%s ", $1, $2}'; echo
  printf 'pressure: '; sysctl -n kern.memorystatus_vm_pressure_level
  printf 'tailscaled: '; pgrep -x tailscaled >/dev/null && echo up || echo DOWN
  printf 'agent: '; launchctl print "gui/$(id -u)/ai.openclaw.gateway" >/dev/null 2>&1 && echo loaded || echo NOT-LOADED; }
```

```text
host-a — <OK | Degraded | Down>
filevault: FileVault is Off.        autologin: agent        console: agent
sleep=0 womp=1 autorestart=1        pressure: 1
tailscaled: up                      agent: loaded
Decision: Option B (recorded <date>, owner approval <ref>)
Next action: none
```

`console: root` means the login window is showing: no GUI session, so no LaunchAgent. Memory: gate on `kern.memorystatus_vm_pressure_level` (1 normal, 2 warning, 4 critical), never on `vm_stat` "free", which sits near zero on a healthy Mac.

## Failure tree — work top to bottom, stop at the first red

| # | Check (from your machine) | Red means | Fix |
|---|---|---|---|
| 1 | `tailscale ping -c 3 host-a` | Mac off, site offline, node key expired, or the **cask** app died with the session | Admin console: last seen + key expiry. Off → smart plug cycle. Cask → reinstall as formula. |
| 2 | `ssh -o ConnectTimeout=8 -o BatchMode=yes agent@host-a true` | Remote Login off, or key not in `authorized_keys` | Remote desktop → §Remote Login. |
| 3 | Password prompt, then the connection drops | macOS 26 pre-boot FileVault unlock (Option A after a reboot) | Expected. Reconnect; then step 4 will be red until a human logs in. |
| 4 | `ssh agent@host-a 'stat -f %Su /dev/console'` → `root` | No GUI session: auto-login not set, or FileVault came back after an update | Log in via screen sharing; re-check §Read first. |
| 5 | `ssh agent@host-a 'launchctl print gui/$(id -u)/ai.openclaw.gateway'` fails | Session up, service not loaded | `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`; if absent, reinstall the service (`always-on-agent-ops`). |
| 6 | Agent runs, GUI actions silently do nothing | Privacy grant missing or reset by an update | Human click (§Walls). |
| 7 | Remote desktop shows a black screen / dead mouse | Its own privacy grants were reset | Same: human click on site or via SSH-only triage. |

## Fleet health — one line per host

Write this as a **bash** file and run it with `bash`; do not paste it into an interactive zsh (see §Shell traps).

```bash
#!/bin/bash
# hosts.txt: one user@host per line, e.g. agent@host-a
[ -s hosts.txt ] || { echo "hosts.txt missing or empty: nothing checked" >&2; exit 2; }
while IFS= read -r target; do
  target=${target%$'\r'}
  case $target in ''|'#'*) continue ;; esac
  printf '%-16s ' "${target#*@}"
  ssh -n -o ConnectTimeout=8 -o BatchMode=yes "$target" \
    'fdesetup status | tr -d "\n"; printf "  console=%s" "$(stat -f %Su /dev/console)";
     pmset -g | grep -E "^ *(sleep|womp|autorestart) " | awk "{printf \"  %s=%s\", \$1, \$2}";
     launchctl print "gui/$(id -u)/ai.openclaw.gateway" >/dev/null 2>&1 && printf "  agent=ON" || printf "  agent=OFF"; echo' \
    || echo "UNREACHABLE"
done < hosts.txt
# Output: host-a           FileVault is Off.  console=agent  sleep=0  womp=1  autorestart=1  agent=ON
```

`ssh -n` matters: without it, the first `ssh` swallows the rest of `hosts.txt` from stdin and the loop stops after one host.

## Shell traps on the host

| Trap | Symptom | Rule |
|---|---|---|
| zsh ties `path` (lowercase) to `PATH` | `read -r name path mode` in a loop → `command not found: ls` right after `command -v ls` worked | Never name a variable `path`, `status`, `argv`, `fpath`, `cdpath`, `manpath`. |
| `#` is not a comment in interactive zsh (`INTERACTIVE_COMMENTS` off) | `cmd   # note` passes `#`, `note` as arguments | No trailing comments in anything a human pastes; explanation on the line before. |
| No word splitting in zsh | `for f in $FILES` loops once | Arrays: `FILES=(a b)`, `"${FILES[@]}"` — or write bash scripts. |
| `<PLACEHOLDER>` | `zsh: parse error near '&&'` | Bare-word placeholders. |
| Multi-line paste through a remote-desktop terminal | `parse error`, or a stray triple backtick leaves the shell waiting for a closing backtick | One command per paste, or a single `;`-joined line; never paste Markdown fences. |
| `/usr/bin` before `/opt/homebrew/bin` in `PATH` | `python3 --version` shows Apple's old build while brew has a current one | `which -a TOOL` before diagnosing a version; absolute paths in LaunchAgents and cron argv. |
| npm 12 blocks install scripts | `npm i -g` of a native CLI "succeeds", then the CLI crashes | Reinstall with `--allow-scripts=PKG`. |

## Reboot drill — with a person on site

Softest first. The person touches nothing unless asked.

| Test | On site | Remote | Pass |
|---|---|---|---|
| Remote-desktop tool killed | quits it | `ssh agent@host-a 'open -a APPNAME'` | it reconnects |
| Screen locked | locks the screen | screen sharing, type the password | session resumes |
| Reboot | watches | `ssh -t ops-admin@host-a 'sudo reboot'` (`-t`: sudo needs a TTY for its prompt) | Option B: desktop + agent up in 1-2 min. Option A: login window, as designed |
| Power cut | pulls the plug, restores it | nothing | boots alone (`autorestart 1`) |
| Powered off | shuts down | ping | nothing answers — expected; only the smart plug recovers this |

## Scope

This skill ONLY: configures remote access over a private Tailscale network with native sshd; sets power and restart behaviour; verifies state with read-only commands; produces a host report; explains the auto-login ⇄ FileVault trade-off so a human can decide it.

This skill NEVER: disables FileVault, writes `/etc/kcpassword`, or stores a login password on the host; edits `TCC.db` or works around SIP; opens a port to the internet; installs a passwordless `sudo` rule; enables auto-login on a laptop or a machine with unrelated data; treats Option B as a hardening step.
