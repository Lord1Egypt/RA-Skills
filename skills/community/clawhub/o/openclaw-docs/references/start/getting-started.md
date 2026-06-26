# Getting Started

Source: https://docs.openclaw.ai/start/getting-started

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationFirst stepsGetting StartedGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpHome
OpenClaw
Overview
Showcase
Core concepts
Features
First steps
Getting StartedOnboarding OverviewOnboarding: CLIOnboarding: macOS App
Guides
Personal Assistant Setup
On this page
- [Getting Started](#getting-started)
- [Prereqs](#prereqs)
- [Quick setup (CLI)](#quick-setup-cli)
- [Optional checks and extras](#optional-checks-and-extras)
- [Useful environment variables](#useful-environment-variables)
- [Go deeper](#go-deeper)
- [What you will have](#what-you-will-have)
- [Next steps](#next-steps)

​Getting Started
Goal: go from zero to a first working chat with minimal setup.
Fastest chat: open the Control UI (no channel setup needed). Run `openclaw dashboard`
and chat in the browser, or open `http://127.0.0.1:18789/` on the
gateway host.
Docs: [Dashboard](/web/dashboard) and [Control UI](/web/control-ui).
​Prereqs

- Node 22 or newer

Check your Node version with `node --version` if you are unsure.
​Quick setup (CLI)
1Install OpenClaw (recommended)

 macOS/Linux Windows (PowerShell)
Copy```
curl -fsSL https://openclaw.ai/install.sh | bash

```

Copy```
iwr -useb https://openclaw.ai/install.ps1 | iex

```

Other install methods and requirements: [Install](/install).2Run the onboarding wizard

Copy```
openclaw onboard --install-daemon

```

The wizard configures auth, gateway settings, and optional channels.
See [Onboarding Wizard](/start/wizard) for details.3Check the Gateway

If you installed the service, it should already be running:Copy```
openclaw gateway status

```

4Open the Control UI

Copy```
openclaw dashboard

```

If the Control UI loads, your Gateway is ready for use.
​Optional checks and extras
Run the Gateway in the foreground

Useful for quick tests or troubleshooting.Copy```
openclaw gateway --port 18789

```

Send a test message

Requires a configured channel.Copy```
openclaw message send --target +15555550123 --message "Hello from OpenClaw"

```

​Useful environment variables
If you run OpenClaw as a service account or want custom config/state locations:

- `OPENCLAW_HOME` sets the home directory used for internal path resolution.

- `OPENCLAW_STATE_DIR` overrides the state directory.

- `OPENCLAW_CONFIG_PATH` overrides the config file path.

Full environment variable reference: [Environment vars](/help/environment).
​Go deeper
## Onboarding Wizard (details)

Full CLI wizard reference and advanced options.## macOS app onboarding

First run flow for the macOS app.
​What you will have

- A running Gateway

- Auth configured

- Control UI access or a connected channel

​Next steps

- DM safety and approvals: [Pairing](/channels/pairing)

- Connect more channels: [Channels](/channels)

- Advanced workflows and from source: [Setup](/start/setup)

FeaturesOnboarding Overview⌘I