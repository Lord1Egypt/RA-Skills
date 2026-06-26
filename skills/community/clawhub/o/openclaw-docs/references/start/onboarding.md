# Onboarding (macOS App)

Source: https://docs.openclaw.ai/start/onboarding

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationFirst stepsOnboarding (macOS App)Get startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpHome
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
- [Onboarding (macOS App)](#onboarding-macos-app)

​Onboarding (macOS App)
This doc describes the **current** first‑run onboarding flow. The goal is a
smooth “day 0” experience: pick where the Gateway runs, connect auth, run the
wizard, and let the agent bootstrap itself.
For a general overview of onboarding paths, see [Onboarding Overview](/start/onboarding-overview).
1Approve macOS warning

2Approve find local networks

3Welcome and security notice

4Local vs Remote

Where does the **Gateway** run?

- **This Mac (Local only):** onboarding can run OAuth flows and write credentials
locally.

- **Remote (over SSH/Tailnet):** onboarding does **not** run OAuth locally;
credentials must exist on the gateway host.

- **Configure later:** skip setup and leave the app unconfigured.

**Gateway auth tip:**

- The wizard now generates a **token** even for loopback, so local WS clients must authenticate.

- If you disable auth, any local process can connect; use that only on fully trusted machines.

- Use a **token** for multi‑machine access or non‑loopback binds.

5Permissions

Onboarding requests TCC permissions needed for:

- Automation (AppleScript)

- Notifications

- Accessibility

- Screen Recording

- Microphone

- Speech Recognition

- Camera

- Location

6CLI

This step is optional
The app can install the global `openclaw` CLI via npm/pnpm so terminal
workflows and launchd tasks work out of the box.7Onboarding Chat (dedicated session)

After setup, the app opens a dedicated onboarding chat session so the agent can
introduce itself and guide next steps. This keeps first‑run guidance separate
from your normal conversation. See [Bootstrapping](/start/bootstrapping) for
what happens on the gateway host during the first agent run.Onboarding: CLIPersonal Assistant Setup⌘I