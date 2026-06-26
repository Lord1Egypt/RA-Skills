# Installer Internals

Source: https://docs.openclaw.ai/install/installer

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationInstall overviewInstaller InternalsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpInstall overview
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
- [Installer internals](#installer-internals)
- [Quick commands](#quick-commands)
- [install.sh](#install-sh)
- [Flow (install.sh)](#flow-install-sh)
- [Source checkout detection](#source-checkout-detection)
- [Examples (install.sh)](#examples-install-sh)
- [install-cli.sh](#install-cli-sh)
- [Flow (install-cli.sh)](#flow-install-cli-sh)
- [Examples (install-cli.sh)](#examples-install-cli-sh)
- [install.ps1](#install-ps1)
- [Flow (install.ps1)](#flow-install-ps1)
- [Examples (install.ps1)](#examples-install-ps1)
- [CI and automation](#ci-and-automation)
- [Troubleshooting](#troubleshooting)

​Installer internals
OpenClaw ships three installer scripts, served from `openclaw.ai`.
ScriptPlatformWhat it does[`install.sh`](#installsh)macOS / Linux / WSLInstalls Node if needed, installs OpenClaw via npm (default) or git, and can run onboarding.[`install-cli.sh`](#install-clish)macOS / Linux / WSLInstalls Node + OpenClaw into a local prefix (`~/.openclaw`). No root required.[`install.ps1`](#installps1)Windows (PowerShell)Installs Node if needed, installs OpenClaw via npm (default) or git, and can run onboarding.
​Quick commands

 install.sh install-cli.sh install.ps1
Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install.sh | bash

```

Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --help

```

Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install-cli.sh | bash

```

Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --help

```

Copy```
iwr -useb https://openclaw.ai/install.ps1 | iex

```

Copy```
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -Tag beta -NoOnboard -DryRun

```

If install succeeds but `openclaw` is not found in a new terminal, see [Node.js troubleshooting](/install/node#troubleshooting).

​install.sh
Recommended for most interactive installs on macOS/Linux/WSL.
​Flow (install.sh)
1Detect OS

Supports macOS and Linux (including WSL). If macOS is detected, installs Homebrew if missing.2Ensure Node.js 22+

Checks Node version and installs Node 22 if needed (Homebrew on macOS, NodeSource setup scripts on Linux apt/dnf/yum).3Ensure Git

Installs Git if missing.4Install OpenClaw

- `npm` method (default): global npm install

- `git` method: clone/update repo, install deps with pnpm, build, then install wrapper at `~/.local/bin/openclaw`

5Post-install tasks

- Runs `openclaw doctor --non-interactive` on upgrades and git installs (best effort)

- Attempts onboarding when appropriate (TTY available, onboarding not disabled, and bootstrap/config checks pass)

- Defaults `SHARP_IGNORE_GLOBAL_LIBVIPS=1`

​Source checkout detection
If run inside an OpenClaw checkout (`package.json` + `pnpm-workspace.yaml`), the script offers:

- use checkout (`git`), or

- use global install (`npm`)

If no TTY is available and no install method is set, it defaults to `npm` and warns.
The script exits with code `2` for invalid method selection or invalid `--install-method` values.
​Examples (install.sh)

 Default Skip onboarding Git install Dry run
Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install.sh | bash

```

Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-onboard

```

Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git

```

Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --dry-run

```

Flags reference

FlagDescription`--install-method npm|git`Choose install method (default: `npm`). Alias: `--method``--npm`Shortcut for npm method`--git`Shortcut for git method. Alias: `--github``--version <version|dist-tag>`npm version or dist-tag (default: `latest`)`--beta`Use beta dist-tag if available, else fallback to `latest``--git-dir <path>`Checkout directory (default: `~/openclaw`). Alias: `--dir``--no-git-update`Skip `git pull` for existing checkout`--no-prompt`Disable prompts`--no-onboard`Skip onboarding`--onboard`Enable onboarding`--dry-run`Print actions without applying changes`--verbose`Enable debug output (`set -x`, npm notice-level logs)`--help`Show usage (`-h`)Environment variables reference

VariableDescription`OPENCLAW_INSTALL_METHOD=git|npm`Install method`OPENCLAW_VERSION=latest|next|<semver>`npm version or dist-tag`OPENCLAW_BETA=0|1`Use beta if available`OPENCLAW_GIT_DIR=<path>`Checkout directory`OPENCLAW_GIT_UPDATE=0|1`Toggle git updates`OPENCLAW_NO_PROMPT=1`Disable prompts`OPENCLAW_NO_ONBOARD=1`Skip onboarding`OPENCLAW_DRY_RUN=1`Dry run mode`OPENCLAW_VERBOSE=1`Debug mode`OPENCLAW_NPM_LOGLEVEL=error|warn|notice`npm log level`SHARP_IGNORE_GLOBAL_LIBVIPS=0|1`Control sharp/libvips behavior (default: `1`)

​install-cli.sh
Designed for environments where you want everything under a local prefix (default `~/.openclaw`) and no system Node dependency.
​Flow (install-cli.sh)
1Install local Node runtime

Downloads Node tarball (default `22.22.0`) to `<prefix>/tools/node-v<version>` and verifies SHA-256.2Ensure Git

If Git is missing, attempts install via apt/dnf/yum on Linux or Homebrew on macOS.3Install OpenClaw under prefix

Installs with npm using `--prefix <prefix>`, then writes wrapper to `<prefix>/bin/openclaw`.
​Examples (install-cli.sh)

 Default Custom prefix + version Automation JSON output Run onboarding
Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install-cli.sh | bash

```

Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --prefix /opt/openclaw --version latest

```

Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw

```

Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --onboard

```

Flags reference

FlagDescription`--prefix <path>`Install prefix (default: `~/.openclaw`)`--version <ver>`OpenClaw version or dist-tag (default: `latest`)`--node-version <ver>`Node version (default: `22.22.0`)`--json`Emit NDJSON events`--onboard`Run `openclaw onboard` after install`--no-onboard`Skip onboarding (default)`--set-npm-prefix`On Linux, force npm prefix to `~/.npm-global` if current prefix is not writable`--help`Show usage (`-h`)Environment variables reference

VariableDescription`OPENCLAW_PREFIX=<path>`Install prefix`OPENCLAW_VERSION=<ver>`OpenClaw version or dist-tag`OPENCLAW_NODE_VERSION=<ver>`Node version`OPENCLAW_NO_ONBOARD=1`Skip onboarding`OPENCLAW_NPM_LOGLEVEL=error|warn|notice`npm log level`OPENCLAW_GIT_DIR=<path>`Legacy cleanup lookup path (used when removing old `Peekaboo` submodule checkout)`SHARP_IGNORE_GLOBAL_LIBVIPS=0|1`Control sharp/libvips behavior (default: `1`)

​install.ps1
​Flow (install.ps1)
1Ensure PowerShell + Windows environment

Requires PowerShell 5+.2Ensure Node.js 22+

If missing, attempts install via winget, then Chocolatey, then Scoop.3Install OpenClaw

- `npm` method (default): global npm install using selected `-Tag`

- `git` method: clone/update repo, install/build with pnpm, and install wrapper at `%USERPROFILE%\.local\bin\openclaw.cmd`

4Post-install tasks

Adds needed bin directory to user PATH when possible, then runs `openclaw doctor --non-interactive` on upgrades and git installs (best effort).
​Examples (install.ps1)

 Default Git install Custom git directory Dry run Debug trace
Copy```
iwr -useb https://openclaw.ai/install.ps1 | iex

```

Copy```
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git

```

Copy```
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git -GitDir "C:\openclaw"

```

Copy```
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -DryRun

```

Copy```
# install.ps1 has no dedicated -Verbose flag yet.
Set-PSDebug -Trace 1
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
Set-PSDebug -Trace 0

```

Flags reference

FlagDescription`-InstallMethod npm|git`Install method (default: `npm`)`-Tag <tag>`npm dist-tag (default: `latest`)`-GitDir <path>`Checkout directory (default: `%USERPROFILE%\openclaw`)`-NoOnboard`Skip onboarding`-NoGitUpdate`Skip `git pull``-DryRun`Print actions onlyEnvironment variables reference

VariableDescription`OPENCLAW_INSTALL_METHOD=git|npm`Install method`OPENCLAW_GIT_DIR=<path>`Checkout directory`OPENCLAW_NO_ONBOARD=1`Skip onboarding`OPENCLAW_GIT_UPDATE=0`Disable git pull`OPENCLAW_DRY_RUN=1`Dry run mode
If `-InstallMethod git` is used and Git is missing, the script exits and prints the Git for Windows link.

​CI and automation
Use non-interactive flags/env vars for predictable runs.

 install.sh (non-interactive npm) install.sh (non-interactive git) install-cli.sh (JSON) install.ps1 (skip onboarding)
Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-prompt --no-onboard

```

Copy```
OPENCLAW_INSTALL_METHOD=git OPENCLAW_NO_PROMPT=1 \
  curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install.sh | bash

```

Copy```
curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw

```

Copy```
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard

```

​Troubleshooting
Why is Git required?

Git is required for `git` install method. For `npm` installs, Git is still checked/installed to avoid `spawn git ENOENT` failures when dependencies use git URLs.Why does npm hit EACCES on Linux?

Some Linux setups point npm global prefix to root-owned paths. `install.sh` can switch prefix to `~/.npm-global` and append PATH exports to shell rc files (when those files exist).sharp/libvips issues

The scripts default `SHARP_IGNORE_GLOBAL_LIBVIPS=1` to avoid sharp building against system libvips. To override:Copy```
SHARP_IGNORE_GLOBAL_LIBVIPS=0 curl -fsSL --proto &#x27;=https&#x27; --tlsv1.2 https://openclaw.ai/install.sh | bash

```

Windows: "npm error spawn git / ENOENT"

Install Git for Windows, reopen PowerShell, rerun installer.Windows: "openclaw is not recognized"

Run `npm config get prefix`, append `\bin`, add that directory to user PATH, then reopen PowerShell.Windows: how to get verbose installer output

`install.ps1` does not currently expose a `-Verbose` switch.
Use PowerShell tracing for script-level diagnostics:Copy```
Set-PSDebug -Trace 1
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
Set-PSDebug -Trace 0

```

openclaw not found after install

Usually a PATH issue. See [Node.js troubleshooting](/install/node#troubleshooting).InstallDocker⌘I