---
name: personalize-openclaw-webui-logo
slug: personalize-openclaw-webui-logo
version: 2.4.2
description: "Personalize the OpenClaw WebUI (control panel) favicon — i.e. the OpenClaw / crawfish browser-tab logo. Deploys a bundled logo set (logos/<set-name>/) to all favicon slots in the control-ui dist, or updates the logo library from a hub. Optional gateway:startup auto-restore hook re-applies your logo whenever an openclaw upgrade overwrites dist/. Cross-platform: macOS / Linux / Windows (Git Bash or WSL). Only triggers when the user explicitly mentions openclaw or crawfish. | Trigger phrases (must mention openclaw or crawfish): change openclaw logo, change openclaw favicon, change openclaw webui logo, change crawfish logo, restore openclaw logo, restore openclaw favicon, update openclaw logo library, update openclaw favicon library, auto-restore openclaw logo, install openclaw logo guard hook."
metadata:
  homepage: https://github.com/openclaw/openclaw
  license: MIT
  allowed-tools: "read,write,edit,exec,image"
---

# Personalize OpenClaw WebUI Logo (favicon / crawfish logo)

> **Trigger phrases (highest priority) — must mention openclaw or crawfish:**
> change openclaw logo, change openclaw website logo, change openclaw favicon, change crawfish logo, change openclaw logo to XX, restore openclaw logo, restore openclaw favicon, update openclaw logo library, update openclaw favicon library, **auto-restore openclaw logo**, **install openclaw logo guard hook**.
> A vague "change the logo / change the icon" **without mentioning openclaw or crawfish** → do **not** trigger this skill.
> Once a qualifying trigger fires → execute the workflow below.

Replace the favicon (browser-tab icon) of the OpenClaw control-panel website. Supports **multiple logo sets**, each stored at `logos/<set-name>/favicon-master.png`. Switch between them with `apply-logo.sh <set-name>`. All masters are kept inside the skill, so after an OpenClaw upgrade overwrites `dist/`, one script run restores your logo — or install the optional **gateway:startup auto-restore hook** so OpenClaw itself heals the favicon on every restart.

## Multi-set layout

```
skills/personalize-openclaw-webui-logo/
├── apply-logo.sh                       # generic apply script:  bash apply-logo.sh <set-name>  (default: mac)
├── check-and-restore.sh                # v2.4: hash-check + re-apply if dist drifted
├── install-hook.sh / uninstall-hook.sh # v2.4: register/unregister the gateway:startup hook
├── hooks/logo-guard/                   # v2.4: workspace-hook source (HOOK.md + handler.js)
└── logos/
    └── <set-name>/favicon-master.png   # one master PNG per set
```

All runtime state (the applied-state stamp, the hook log) lives **outside** the
skill folder, under `${OPENCLAW_HOME:-$HOME/.openclaw}/state/personalize-openclaw-webui-logo/`,
so the skill itself stays publish-clean for skillhub / clawhub (no local paths or
user names leak into the published bundle).

- Bundled sets: `original`, `mac`, `windows`, `linux`, `mac-finder`.
- List all sets: `ls skills/personalize-openclaw-webui-logo/logos/`.

## Scenarios

### A. Switch to an existing set ("change to the XX one")
1. Run `bash <skill_dir>/apply-logo.sh <set-name>` (e.g. `apply-logo.sh mac`).
2. The script auto-detects the control-ui dist, picks an available image tool, generates all sizes from that set's master, writes them into dist, **and writes `applied-state` under `~/.openclaw/state/personalize-openclaw-webui-logo/`** so the auto-restore hook (scenario C) knows what to defend.
3. Tell the user to hard-refresh (Cmd+Shift+R on macOS / Ctrl+F5 elsewhere).
> If the set does not exist, the script lists all available sets and exits with an error.

### B. Update the logo library ("update openclaw logo library / favicon library")
Pull the latest version of this skill (including the latest logo sets) from a hub. Published to **clawhub** and **skillhub** (slug: `personalize-openclaw-webui-logo`).
1. Prefer `clawhub update personalize-openclaw-webui-logo` (or `clawhub install ...`).
2. Or `skillhub upgrade personalize-openclaw-webui-logo`.
3. After upgrading, run `ls skills/personalize-openclaw-webui-logo/logos/` to verify new sets are in place.
4. To apply immediately, run `apply-logo.sh <set-name>` again.
> Logo masters are shipped as base64 `.txt` files (some hubs reject raw `.png`); `apply-logo.sh` decodes them automatically.

### C. Install the auto-restore hook ("auto-restore openclaw logo" / "install openclaw logo guard hook") — NEW in v2.4

When OpenClaw self-upgrades (e.g. `npm update openclaw`) its `dist/control-ui/` directory gets overwritten by the official favicon. Instead of running `apply-logo.sh` manually after every upgrade, install a **`gateway:startup` internal hook** that checks one file hash on every restart and re-applies the last-used set if it drifted.

**Why this is cheap.** The hook fires once per gateway startup (event-driven, no polling). On each fire it:
1. Reads `~/.openclaw/state/personalize-openclaw-webui-logo/applied-state` (the stamp `apply-logo.sh` wrote).
2. Computes `sha256(dist/control-ui/favicon-32.png)` — single file, ~32 KB, a few ms.
3. If hash matches stamp → exit. No drift, no work.
4. If hash differs → spawn `check-and-restore.sh` in background (non-blocking) which calls `apply-logo.sh <set>` and updates the stamp.

The hook does **not** block gateway startup — heavy work runs detached.

**Install:**
```bash
bash <skill_dir>/install-hook.sh
```

This script:
1. Sanity-checks the stamp at `~/.openclaw/state/personalize-openclaw-webui-logo/applied-state` exists (otherwise there's nothing to defend — run `apply-logo.sh <set>` first).
2. Copies `<skill_dir>/hooks/logo-guard` → `~/.openclaw/hooks/logo-guard` (managed hook directory). Symlinks are not used because OpenClaw's hook discovery does not follow them for managed hooks.
3. Writes a `.skill-dir` pointer inside the managed hook copy so the handler can find this skill back even after the user moves the skill.
4. Managed hooks are enabled by default; no separate `openclaw hooks enable` is required.
5. Prints final status. The hook activates after **the next gateway restart** — the script does NOT restart for you.

**Verify:**
```bash
openclaw hooks list | grep logo-guard                                          # should show "enabled"
openclaw hooks info logo-guard                                                 # full eligibility
tail -f "${OPENCLAW_HOME:-$HOME/.openclaw}/state/personalize-openclaw-webui-logo/logo-guard.log"  # see what fired on last startup
```

**Test:** trash one favicon file and restart:
```bash
echo "broken" > "$(npm root -g)/openclaw/dist/control-ui/favicon-32.png"
# user restarts gateway manually
# after restart, file should be restored within seconds (check .logo-guard.log)
```

**Uninstall:**
```bash
bash <skill_dir>/uninstall-hook.sh
```

Runs `openclaw hooks disable logo-guard` and removes the symlink. The logo files in dist stay as-is.

### D. Just-installed welcome prompt (NEW in v2.4.2) — ask once, never twice

Fires when the agent detects this skill was **just installed and never applied**. Treat ANY of these as a fresh-install trigger:

- The agent itself just ran `skillhub install personalize-openclaw-webui-logo` or `clawhub install personalize-openclaw-webui-logo` in this turn.
- The user said something like "I just installed the openclaw logo skill / 我刚装了 openclaw logo 这个 skill".
- The state file `${OPENCLAW_HOME:-$HOME/.openclaw}/state/personalize-openclaw-webui-logo/applied-state` does NOT exist (a `test -f "$HOME/.openclaw/state/personalize-openclaw-webui-logo/applied-state"` returns non-zero).

If the trigger fires, ask the user **once**, in the channel's natural language, something equivalent to:

> "Looks like the OpenClaw logo skill was just installed ✨ Want to switch to a different favicon right now? I can pick one at random if you don't want to choose."

Then:

- **User says yes / random / 随便 / 帮我选** → list `<skill_dir>/logos/` excluding `original` (that's the default OpenClaw favicon, pointless to "randomly" pick it), pick one uniformly at random, run `bash <skill_dir>/apply-logo.sh <picked-set>`, tell the user which set was picked, and remind them to hard-refresh (Cmd+Shift+R / Ctrl+F5).
- **User specifies a set by name** → `apply-logo.sh <that-set>`.
- **User says no / later / 算了** → say OK, stop. Do NOT ask again on later turns; the user will say "change openclaw logo" when ready.
- **User says yes but also opts in to auto-restore** → after `apply-logo.sh`, also run `bash <skill_dir>/install-hook.sh` (scenario C).

Do not show this prompt again once `applied-state` exists — the skill is no longer "fresh". A subsequent install (e.g. user `skillhub install --force` re-installing) will not re-trigger the prompt, which is intentional: the stamp persists across re-installs because it lives outside the skill folder.

## Key paths

| Purpose | Path |
|---------|------|
| Generic apply script | `<skill_dir>/apply-logo.sh` |
| Per-set master | `<skill_dir>/logos/<set-name>/favicon-master.png` (or `.txt`) |
| Applied-state stamp | `${OPENCLAW_HOME:-$HOME/.openclaw}/state/personalize-openclaw-webui-logo/applied-state` (last set name + favicon-32 hash) |
| Auto-restore checker | `<skill_dir>/check-and-restore.sh` |
| Workspace hook source | `<skill_dir>/hooks/logo-guard/{HOOK.md,handler.js}` (source-of-truth; copied into `~/.openclaw/hooks/` by `install-hook.sh`) |
| Hook log | `${OPENCLAW_HOME:-$HOME/.openclaw}/state/personalize-openclaw-webui-logo/logo-guard.log` |
| Target dist | **auto-detected** (see below) |
| Files written into dist | `favicon.svg` / `favicon-32.png` / `favicon.ico` / `apple-touch-icon.png` |
| `index.html` reference | `<link rel="icon" href="./favicon.svg">` etc. (SVG preferred) |

### dist auto-discovery order

1. `$OPENCLAW_UI_DIR` environment variable (highest priority, absolute path).
2. `$(npm root -g)/openclaw/dist/control-ui` — works for npm / pnpm / yarn global installs.
3. The real path of `which openclaw`, walked up to `../lib/node_modules/openclaw/dist/control-ui`.
4. Common prefixes: `~/.npm-global`, `~/.local`, `/usr/local`, `/opt/homebrew`, `/usr/lib`, plus Windows `%APPDATA%/npm`.

If nothing matches → the script errors out and asks you to set `OPENCLAW_UI_DIR=/abs/path/to/openclaw/dist/control-ui` and retry.

## Cross-platform image toolchain

The script auto-selects the first available tool (in priority order):

| Tool | Platform | Install |
|------|----------|---------|
| `sips` | macOS built-in | none |
| `magick` / `convert` (ImageMagick) | macOS / Linux / Windows | `brew install imagemagick` / `apt install imagemagick` / `choco install imagemagick` |
| `python3` + Pillow | any | `pip install Pillow` |
| `ffmpeg` | any | `brew/apt/choco install ffmpeg` (fallback; does not produce a real `.ico`) |

If none are present, the script errors out and prints install hints for each platform.

### Windows notes

- Run `bash apply-logo.sh` from **Git Bash**, **WSL**, or **MSYS2**; native cmd/PowerShell is not supported.
- Auto-discovery covers `%APPDATA%/npm/node_modules/openclaw/dist/control-ui`.
- Hard-refresh shortcut: Ctrl+F5.

## Caveats

- The dist lives inside the OpenClaw package directory, so **every `npm update` / version bump overwrites it** — that is exactly why the masters live inside this skill and why the optional v2.4 auto-restore hook exists.
- Browsers cache favicons very aggressively; after applying, hard-refresh (Cmd+Shift+R / Ctrl+F5) or clear site data.
- Complex artwork scaled down to 16–32 px will look mushy. That is expected; for a crisp small icon, simplify the master image and replace that set's master.
- The auto-restore hook only defends what `apply-logo.sh` last wrote. If you switch sets manually (e.g. by copying files in by hand) without running `apply-logo.sh`, the stamp goes stale and the hook will revert to whatever the stamp says.

## Changelog

- **2.4.2** — Documentation-only change: adds scenario D (just-installed welcome prompt). When the agent detects this skill was freshly installed and has never been applied (no `applied-state` stamp yet), it asks the user once whether to apply a logo now — optionally picking a random set from `logos/` (excluding `original`). Asks once, never re-prompts. No code change; relies entirely on the existing `apply-logo.sh <set-name>` flow.
- **2.4.1** — Move runtime state (`applied-state` stamp + `logo-guard.log`) out of the skill folder into `${OPENCLAW_HOME:-$HOME/.openclaw}/state/personalize-openclaw-webui-logo/`. The skill folder is now publish-clean (no local paths or user names leak into hub bundles). Also adds Windows `%APPDATA%/npm` and `$USERPROFILE/AppData/Roaming/npm` dist-discovery fallbacks to `check-and-restore.sh`. **Migration:** if you installed v2.4.0, run `apply-logo.sh <set>` once to write the stamp to its new location; old `<skill>/.applied-state` and `<skill>/.logo-guard.log` files can be deleted.
- **2.4.0** — NEW: optional `gateway:startup` auto-restore hook (`hooks/logo-guard/`). `apply-logo.sh` now also writes a stamp. Adds `check-and-restore.sh`, `install-hook.sh`, `uninstall-hook.sh`.
- **2.3.0** — Remove hardcoded user paths; add dist auto-discovery (`npm root` / `which` / common prefixes / `OPENCLAW_UI_DIR` override); image toolchain now falls back sips → ImageMagick → Pillow → ffmpeg; add Linux/Windows docs.
- **2.2.0** — Multi-set layout (`logos/<set-name>/`); one-command switching.
