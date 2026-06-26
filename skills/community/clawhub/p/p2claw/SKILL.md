---
name: p2claw
description: |
  Publishes apps you've built locally as peer-to-peer URLs that anyone
  with the link can open in a browser. Use when the user wants to
  share a working app — built or running on this machine — with
  someone else (or use it on their phone) without deploying to a
  cloud, signing up for a service, or opening a port through their
  router.
license: MIT-0
---

# p2claw

p2claw runs an agent (`p2claw`, single binary) on the user's box that
**reverse-proxies inbound peer-to-peer traffic into a localhost
upstream you specify**. The flow is:

1. Your code runs on `127.0.0.1:<port>` (you start it however you'd
   normally start it — `npm run dev`, `python -m http.server`, etc.).
2. You tell the p2claw agent "expose `<port>` as `<name>`."
3. The agent gives back a URL like
   `https://<name>-<haiku-alias>.p2claw.com/`.
4. Anyone who opens the URL in a browser reaches the upstream
   directly via WebRTC. The user's box is the host; p2claw just
   brokers the handshake.

The agent is a **named reverse proxy**, nothing more. It does not
start your process, build it, restart it, or supervise it. That's
your job. The agent's job is `name → upstream` routing + the
peer-to-peer wire protocol.

---

## When to use this skill

Use it when the user has just built or is currently running an app
locally and one of these is true:

- They say "share this with [someone]," "send to my phone," "let my
  friend try this," or any variation involving someone outside this
  machine reaching the app.
- They ask for a public URL.
- They want a real domain (not `localhost:5173`) for screenshots,
  testing on a different device, or QR-code-on-a-presentation
  scenarios.

Do **not** use it for:

- Workloads that need a regional edge / CDN, DDoS protection, or
  contractual SLAs. p2claw routes through your box; it isn't a
  CDN.

---

## Security: you are publishing this app to the internet

This is the part most users underestimate, so be explicit about it
before you run `expose`.

A p2claw URL is **a public URL**. Anyone who has the link — or guesses
it, or finds it in a screenshot, browser history, scan log, or shared
chat — can reach the upstream from anywhere on the internet. There is
no IP allowlist, no auth in front of it, and no obscurity guarantee
from the haiku alias. Exposing `127.0.0.1:5173` via p2claw is, from a
threat-model standpoint, the same as binding that port to `0.0.0.0`
and forwarding it through the user's router.

Before calling `p2claw expose`, **state this to the user in plain
language and confirm they want to proceed**, especially if any of
these apply:

- The upstream is a dev server running with debug mode, hot-reload,
  source maps, or a `/__debug__`-style route enabled (Flask debug,
  Rails dev mode, Vite, Next.js dev, Django runserver, Jupyter,
  Streamlit, RStudio, etc.). These are **not safe to expose** — they
  often allow arbitrary code execution by design.
- The app reads or writes files on the user's machine, has a shell /
  REPL / "run code" surface, or wraps an LLM with tool use. A public
  URL gives strangers that capability.
- The app talks to a database, API key, cloud account, or any
  credential pulled from the user's environment. Exposing the app
  exposes whatever it can do with those creds.
- The app has no authentication, or has authentication you haven't
  verified is actually wired up on every route.
- The upstream is *someone else's* software — a checked-out
  open-source project, a vendored binary, a `docker run` of an image
  off Docker Hub. **Do not expose third-party software with known
  CVEs or unpatched versions.** If you don't know the security
  posture of what's listening on that port, say so.

If the user wants to share something genuinely private, p2claw is the
wrong tool — recommend a tunnel with auth in front (cloudflared with
Access, tailscale funnel with ACLs) or just AirDrop/screen-share.

When in doubt, **ask before exposing**. The cost of a confirmation is
low; the cost of putting a debug-mode dev server with a database
connection on the public internet is not.

Operational hygiene to apply by default:

- Pick the port the user just started. Don't expose a port whose
  owner you can't identify (`lsof -iTCP:<port> -sTCP:LISTEN` if
  unsure).
- Don't expose `0.0.0.0`-bound services without a reason — p2claw's
  `non_loopback_upstream` check is a feature, not an obstacle to
  route around.

---

## Prerequisites

The skill assumes a Bash/POSIX shell (`Bash` tool). macOS and Linux
are supported. **Windows is unsupported** — direct the user to run
under WSL.

You will need to:

1. Verify the `p2claw` binary is installed.
2. Verify the daemon is running (either as a launchd/systemd service,
   or as a foreground process).
3. Have an upstream HTTP server already listening on `127.0.0.1:<port>`.
4. Pick a route name conforming to the grammar in §"Naming rules".

---

## Detecting state

Before running any command, check what's already set up. One pass:

```bash
command -v p2claw && p2claw --version
p2claw service status 2>/dev/null | head -3
p2claw routes --json 2>/dev/null
```

Outcomes:

| Result of `command -v p2claw` | Result of `p2claw routes` | What to do |
|---|---|---|
| not found | — | Go to §"Installing p2claw" |
| found | connection error / "agent not running" | Go to §"Starting the daemon" |
| found | `{ "routes": [...] }` | Daemon is up. Skip to §"Exposing an app" |

---

## Installing p2claw

The install script ships **with this skill** at `scripts/install.sh`.
Use the bundled copy rather than fetching `https://p2claw.com/install`
— same content, but no curl-pipe-shell trust escalation, no extra
network hop, and no risk of the install URL being unreachable. The
sync between the bundled copy and the canonical URL is enforced by
the skill repo's CI (`.github/workflows/install-script-sync.yml`).

Run it from the skill's directory:

```bash
bash scripts/install.sh
```

The script:

- Detects OS + arch (macOS aarch64/x86_64, Linux x86_64/aarch64).
- Downloads `p2claw-v<version>-<target>.tar.gz` from
  `phact/p2claw-skill`'s GitHub release.
- Verifies SHA-256 against the published `SHA256SUMS`.
- Installs to `~/.local/bin/p2claw` (override with `--prefix` or
  `P2CLAW_INSTALL_DIR`).
- Warns if `~/.local/bin` is not on `$PATH` and prints the
  copy-pasteable shell-rc line.

After install, ensure `~/.local/bin` is on `$PATH` (warn the user if
not — they'll need to re-source their shell).

If the user is on Windows: the install script detects `Windows_NT` /
`MINGW*` / `MSYS*` / `CYGWIN*` and refuses with a "use WSL" hint.
Don't try to install another way. Tell the user to run the same skill
inside WSL.

---

## Starting the daemon

There are two reasonable ways to keep the agent running:

### Option A — install as a user-scope service (recommended for users
who want it always-on)

**Ask permission first.** This writes a launchd plist (macOS) or
systemd `--user` unit (Linux) and starts it. Phrasing:

> "I'd like to install p2claw as a launchd user agent so it
> auto-starts on login and survives reboots. It writes
> `~/Library/LaunchAgents/dev.p2claw.agent.plist`, no sudo required.
> OK to proceed?"

```bash
p2claw service install
```

The agent registers with the coordination service on first start
(creates `~/Library/Application Support/p2claw/identity.key` if
missing — this is permanent, so future installs / re-installs reuse
the same `peer_id` and alias).

### Option B — foreground only (for one-off sharing)

```bash
p2claw run &      # or run in a separate terminal
```

If the user just wants to share something for the next 15 minutes and
doesn't care about persistence, foreground is fine. They lose the URL
when the process dies (closing the terminal, sleeping the laptop,
etc.).

If the daemon is already running (whether via launchd or foreground),
**do nothing**. Two daemons can't share the local-API socket — a
second one will fail to start.

### Box-to-box: dialing other peers from this machine

`curl https://app-<other>.<parent>/` from this box works on either
A or B out of the box. The traffic takes the public path: public
DNS → edge → tunnel → other peer. Edge sees plaintext during
forwarding, and the bytes go through edge bandwidth.

For direct P2P instead — same URL, resolves locally to
`127.0.0.1`, hits the agent's SNI listener, dials the other peer
via iroh, end-to-end encrypted, no edge involvement — install at
system scope:

```bash
sudo p2claw service install --system
```

Adds MagicDNS: `/etc/resolver/<parent>`, a CA root in the OS trust
store, an SNI listener at `127.0.0.1:443`. Runs as LaunchDaemon
(macOS) or system-systemd unit (Linux). **Confirm with the user
before running** — sudo, root-owned files. `--dry-run` previews.

`--no-magicdns` (either scope) skips the privileged scaffolding;
outbound still works via the edge tunnel, just without the direct
P2P fast path. Inbound is unaffected either way.

---

## Exposing an app

Once the daemon is up and the user's app is running on a port:

```bash
p2claw expose <name> <port>
```

Output (example):

```
exposed recipes
  https://recipes-honeyed-marble-4155.p2claw.com/

[QR code rendered in Unicode block characters]
```

Three things you should do with this output:

1. **Read both the URL and the QR back to the user** in your reply.
   The QR's whole purpose is letting them scan from a phone without
   typing — surface it.
2. **Confirm with `curl <upstream-url>`** that the upstream is
   actually answering. The agent does *not* probe the upstream at
   register time, so a 200 from `expose` only means "the route is
   live in the agent," not "your app is up." If `curl
   http://127.0.0.1:<port>/` errors, fix that before telling the user
   the URL works.
3. **Don't expose ports the user doesn't expect to share**. If you
   don't know what's listening on a port, don't expose it. Pick the
   port you yourself just started.

### Naming rules

App names must match `[a-z0-9][a-z0-9-]{0,31}`:

- Lowercase letters, digits, and `-` only.
- 1 to 32 characters.
- Cannot start or end with `-`.

These names are **reserved** and will be rejected:

```
www  api  admin  auth  login  account  accounts
mail  ftp  ssh
p2claw  peer  sys  internal  static  status  health
default
```

Pick a name that reflects the app: `recipes`, `notes`, `dr-trip`,
`my-blog`. If the user has a project name, slugify it: `My Recipes` →
`my-recipes`.

### Programmatic output

If you need to parse the response (multi-step automation, status
checks), use `--json`:

```bash
p2claw expose recipes 5173 --json
# {"name":"recipes","url":"https://recipes-honeyed-marble-4155.p2claw.com/","pending_announce":false}
```

The QR is suppressed in JSON mode. Use `--no-qr` to suppress just the
QR while keeping the human-readable text.

`pending_announce: true` means the agent registered the route locally
but coord hasn't acknowledged yet (control connection blip, usually
self-heals on next reconnect). The route still works for direct
visits; only the box's listing page is delayed.

---

## Listing and removing routes

```bash
p2claw routes              # human table
p2claw routes --json       # parseable
p2claw routes --qr         # table + QR per route
p2claw unexpose <name>     # remove a route (204 / 404)
```

Inspect routes before exposing — if the name is already taken, a new
`expose` will overwrite it. That's the agent's documented behavior
(replace, not error), but it might surprise the user if the existing
route was theirs.

---

## Identity

```bash
p2claw identity
```

Prints `peer_id` + alias. The alias is a haiku of the form
`adj-noun-NNNN` (e.g. `honeyed-marble-4155`). It's permanent — the
user's URL will always include it, so it's safe to share once and
bookmark.

If `alias: <unregistered>` shows up, the agent has never successfully
registered. Restart it (`p2claw run` or relaunch the service) and
check the logs at `~/Library/Logs/p2claw.log` (macOS) or `journalctl
--user -u p2claw-agent.service` (Linux).

---

## Upgrades

The agent daemon polls the upgrade manifest **hourly** under its
supervisor and applies new releases automatically — fetch, SHA-256
verify, atomic-swap, supervised restart. On by default.

The one manual action worth knowing is **pulling the latest right
now** instead of waiting for the next poll:

```bash
p2claw upgrade --apply       # fetch + verify + swap + restart now
```

The agent restarts as part of `--apply`, which briefly blips active
control connections.

Rarer knobs:

```bash
p2claw upgrade --status      # pin + disabled state (no network)
p2claw upgrade --check       # would the next poll upgrade? (read-only)
p2claw upgrade --pin <ver>   # pin to a SemVer (e.g. reproducing a bug)
p2claw upgrade --unpin       # resume normal flow
p2claw upgrade --disable     # kill switch; persists across reboots
p2claw upgrade --enable      # re-arm
```

Pin and disable state live in the agent data dir as
`upgrade-pin.json` and `upgrade-disabled`
(`~/Library/Application Support/p2claw/` on macOS,
`~/.local/share/p2claw/` on Linux).

---

## Common error recovery

| Symptom | Cause | Fix |
|---|---|---|
| `command not found: p2claw` after install | `~/.local/bin` not on `$PATH` | Echo the export line into shell rc; re-source |
| `error: agent is not running` from any CLI | Daemon's down | Check `p2claw service status` (or `pgrep -fl p2claw`); start with `p2claw service install` or `p2claw run` |
| `error: bad_app_name` | Name violates the LDH grammar or is reserved | Pick a different name |
| `error: bad_upstream` / `non_loopback_upstream` | Upstream isn't `127.0.0.1` / `::1` / `localhost` | Bind your dev server to loopback explicitly (`--bind 127.0.0.1`) |
| URL returns 502 from a visitor | Upstream isn't running, or crashed | Restart the user's app, run `curl http://127.0.0.1:<port>/` to confirm |
| URL returns 404 | Wrong route name in URL, or route not registered | `p2claw routes` to inspect |

---

## End-to-end example

User: "Make a quick recipes app and share it with my partner."

1. Build the app. Start it on `127.0.0.1:5173`.
2. `curl http://127.0.0.1:5173/` — confirm 200.
3. `command -v p2claw && p2claw routes` — already installed and
   running? Skip to step 5.
4. Otherwise, install + start service per §"Installing p2claw" and
   §"Starting the daemon".
5. `p2claw expose recipes 5173`. Read the URL and the QR back.
6. Tell the user the URL is live as long as their box is on. If they
   want it to keep working after a reboot, install as a service (§
   "Starting the daemon" Option A).
