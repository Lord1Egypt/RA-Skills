# Scripts

Source: https://docs.openclaw.ai/help/scripts

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationEnvironment and debuggingScriptsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpHelp
HelpTroubleshootingFAQ
Community
OpenClaw Lore
Environment and debugging
Environment VariablesDebuggingTestingScripts
Node runtime
Node.js
Compaction internals
Session Management Deep Dive
Developer setup
Setup
Contributing
CI Pipeline
Docs meta
Docs HubsDocs directory
On this page
- [Scripts](#scripts)
- [Conventions](#conventions)
- [Auth monitoring scripts](#auth-monitoring-scripts)
- [When adding scripts](#when-adding-scripts)

​Scripts
The `scripts/` directory contains helper scripts for local workflows and ops tasks.
Use these when a task is clearly tied to a script; otherwise prefer the CLI.
​Conventions

- Scripts are **optional** unless referenced in docs or release checklists.

- Prefer CLI surfaces when they exist (example: auth monitoring uses `openclaw models status --check`).

- Assume scripts are host‑specific; read them before running on a new machine.

​Auth monitoring scripts
Auth monitoring scripts are documented here:
[/automation/auth-monitoring](/automation/auth-monitoring)
​When adding scripts

- Keep scripts focused and documented.

- Add a short entry in the relevant doc (or create one if missing).

TestingNode.js⌘I