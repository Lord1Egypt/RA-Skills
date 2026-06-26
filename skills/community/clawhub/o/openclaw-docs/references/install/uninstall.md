# Uninstall

Source: https://docs.openclaw.ai/install/uninstall

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationMaintenanceUninstallGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpInstall overview
InstallInstaller Internals
Other install methods
DockerPodmanNixAnsibleBun (Experimental)
Maintenance
UpdatingMigration GuideUninstall
Hosting and deployment
Fly.ioHetznerGCPmacOS VMsexe.devDeploy on RailwayDeploy on RenderDeploy on Northflank
Advanced
Development Channels
On this page
- [Uninstall](#uninstall)
- [Easy path (CLI still installed)](#easy-path-cli-still-installed)
- [Manual service removal (CLI not installed)](#manual-service-removal-cli-not-installed)
- [macOS (launchd)](#macos-launchd)
- [Linux (systemd user unit)](#linux-systemd-user-unit)
- [Windows (Scheduled Task)](#windows-scheduled-task)
- [Normal install vs source checkout](#normal-install-vs-source-checkout)
- [Normal install (install.sh / npm / pnpm / bun)](#normal-install-install-sh-%2F-npm-%2F-pnpm-%2F-bun)
- [Source checkout (git clone)](#source-checkout-git-clone)

​Uninstall
Two paths:

- **Easy path** if `openclaw` is still installed.

- **Manual service removal** if the CLI is gone but the service is still running.

​Easy path (CLI still installed)
Recommended: use the built-in uninstaller:
Copy```
openclaw uninstall

```

Non-interactive (automation / npx):
Copy```
openclaw uninstall --all --yes --non-interactive
npx -y openclaw uninstall --all --yes --non-interactive

```

Manual steps (same result):

- Stop the gateway service:

Copy```
openclaw gateway stop

```

- Uninstall the gateway service (launchd/systemd/schtasks):

Copy```
openclaw gateway uninstall

```

- Delete state + config:

Copy```
rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"

```

If you set `OPENCLAW_CONFIG_PATH` to a custom location outside the state dir, delete that file too.

- Delete your workspace (optional, removes agent files):

Copy```
rm -rf ~/.openclaw/workspace

```

- Remove the CLI install (pick the one you used):

Copy```
npm rm -g openclaw
pnpm remove -g openclaw
bun remove -g openclaw

```

- If you installed the macOS app:

Copy```
rm -rf /Applications/OpenClaw.app

```

Notes:

- If you used profiles (`--profile` / `OPENCLAW_PROFILE`), repeat step 3 for each state dir (defaults are `~/.openclaw-<profile>`).

- In remote mode, the state dir lives on the **gateway host**, so run steps 1-4 there too.

​Manual service removal (CLI not installed)
Use this if the gateway service keeps running but `openclaw` is missing.
​macOS (launchd)
Default label is `bot.molt.gateway` (or `bot.molt.<profile>`; legacy `com.openclaw.*` may still exist):
Copy```
launchctl bootout gui/$UID/bot.molt.gateway
rm -f ~/Library/LaunchAgents/bot.molt.gateway.plist

```

If you used a profile, replace the label and plist name with `bot.molt.<profile>`. Remove any legacy `com.openclaw.*` plists if present.
​Linux (systemd user unit)
Default unit name is `openclaw-gateway.service` (or `openclaw-gateway-<profile>.service`):
Copy```
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload

```

​Windows (Scheduled Task)
Default task name is `OpenClaw Gateway` (or `OpenClaw Gateway (<profile>)`).
The task script lives under your state dir.
Copy```
schtasks /Delete /F /TN "OpenClaw Gateway"
Remove-Item -Force "$env:USERPROFILE\.openclaw\gateway.cmd"

```

If you used a profile, delete the matching task name and `~\.openclaw-<profile>\gateway.cmd`.
​Normal install vs source checkout
​Normal install (install.sh / npm / pnpm / bun)
If you used `https://openclaw.ai/install.sh` or `install.ps1`, the CLI was installed with `npm install -g openclaw@latest`.
Remove it with `npm rm -g openclaw` (or `pnpm remove -g` / `bun remove -g` if you installed that way).
​Source checkout (git clone)
If you run from a repo checkout (`git clone` + `openclaw ...` / `bun run openclaw ...`):

- Uninstall the gateway service **before** deleting the repo (use the easy path above or manual service removal).

- Delete the repo directory.

- Remove state + workspace as shown above.

Migration GuideFly.io⌘I