# Install

Source: https://docs.openclaw.ai/install

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationInstall overviewInstallGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpInstall overview
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
- [Install](#install)
- [System requirements](#system-requirements)
- [Install methods](#install-methods)
- [Other install methods](#other-install-methods)
- [After install](#after-install)
- [Troubleshooting: openclaw not found](#troubleshooting-openclaw-not-found)
- [Update / uninstall](#update-%2F-uninstall)

​Install
Already followed [Getting Started](/start/getting-started)? You’re all set — this page is for alternative install methods, platform-specific instructions, and maintenance.
​System requirements

- **[Node 22+](/install/node)** (the [installer script](#install-methods) will install it if missing)

- macOS, Linux, or Windows

- `pnpm` only if you build from source

On Windows, we strongly recommend running OpenClaw under [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).
​Install methods
The **installer script** is the recommended way to install OpenClaw. It handles Node detection, installation, and onboarding in one step.
Installer script

Downloads the CLI, installs it globally via npm, and launches the onboarding wizard.
 macOS / Linux / WSL2 Windows (PowerShell)
Copy```
curl -fsSL https://openclaw.ai/install.sh | bash

```

Copy```
iwr -useb https://openclaw.ai/install.ps1 | iex

```

That’s it — the script handles Node detection, installation, and onboarding.To skip onboarding and just install the binary:
 macOS / Linux / WSL2 Windows (PowerShell)
Copy```
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard

```

Copy```
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard

```

For all flags, env vars, and CI/automation options, see [Installer internals](/install/installer).npm / pnpm

If you already have Node 22+ and prefer to manage the install yourself:
 npm pnpm
Copy```
npm install -g openclaw@latest
openclaw onboard --install-daemon

```

sharp build errors?

If you have libvips installed globally (common on macOS via Homebrew) and `sharp` fails, force prebuilt binaries:Copy```
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest

```

If you see `sharp: Please add node-gyp to your dependencies`, either install build tooling (macOS: Xcode CLT + `npm install -g node-gyp`) or use the env var above.Copy```
pnpm add -g openclaw@latest
pnpm approve-builds -g        # approve openclaw, node-llama-cpp, sharp, etc.
openclaw onboard --install-daemon

```

pnpm requires explicit approval for packages with build scripts. After the first install shows the “Ignored build scripts” warning, run `pnpm approve-builds -g` and select the listed packages.From source

For contributors or anyone who wants to run from a local checkout.1Clone and build

Clone the [OpenClaw repo](https://github.com/openclaw/openclaw) and build:Copy```
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build
pnpm build

```

2Link the CLI

Make the `openclaw` command available globally:Copy```
pnpm link --global

```

Alternatively, skip the link and run commands via `pnpm openclaw ...` from inside the repo.3Run onboarding

Copy```
openclaw onboard --install-daemon

```

For deeper development workflows, see [Setup](/start/setup).
​Other install methods
## Docker

Containerized or headless deployments.## Podman

Rootless container: run `setup-podman.sh` once, then the launch script.## Nix

Declarative install via Nix.## Ansible

Automated fleet provisioning.## Bun

CLI-only usage via the Bun runtime.
​After install
Verify everything is working:
Copy```
openclaw doctor         # check for config issues
openclaw status         # gateway status
openclaw dashboard      # open the browser UI

```

If you need custom runtime paths, use:

- `OPENCLAW_HOME` for home-directory based internal paths

- `OPENCLAW_STATE_DIR` for mutable state location

- `OPENCLAW_CONFIG_PATH` for config file location

See [Environment vars](/help/environment) for precedence and full details.
​Troubleshooting: `openclaw` not found
PATH diagnosis and fix

Quick diagnosis:Copy```
node -v
npm -v
npm prefix -g
echo "$PATH"

```

If `$(npm prefix -g)/bin` (macOS/Linux) or `$(npm prefix -g)` (Windows) is **not** in your `$PATH`, your shell can’t find global npm binaries (including `openclaw`).Fix — add it to your shell startup file (`~/.zshrc` or `~/.bashrc`):Copy```
export PATH="$(npm prefix -g)/bin:$PATH"

```

On Windows, add the output of `npm prefix -g` to your PATH.Then open a new terminal (or `rehash` in zsh / `hash -r` in bash).
​Update / uninstall
## Updating

Keep OpenClaw up to date.## Migrating

Move to a new machine.## Uninstall

Remove OpenClaw completely.Installer Internals⌘I