# Browser Login

Source: https://docs.openclaw.ai/tools/browser-login

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationBrowserBrowser LoginGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Tools
Built-in tools
LobsterLLM TaskExec ToolWeb Toolsapply_patch ToolElevated ModeThinking LevelsReactions
Browser
Browser (OpenClaw-managed)Browser LoginChrome ExtensionBrowser Troubleshooting
Agent coordination
Agent SendSub-AgentsMulti-Agent Sandbox & Tools
Skills
Slash CommandsSkillsSkills ConfigClawHubPlugins
Extensions
Voice Call PluginZalo Personal Plugin
Automation
HooksCron JobsCron vs HeartbeatAutomation TroubleshootingWebhooksGmail PubSubPollsAuth Monitoring
Media and devices
NodesNode TroubleshootingImage and Media SupportAudio and Voice NotesCamera CaptureTalk ModeVoice WakeLocation Command
On this page
- [Browser login + X/Twitter posting](#browser-login-%2B-x%2Ftwitter-posting)
- [Manual login (recommended)](#manual-login-recommended)
- [Which Chrome profile is used?](#which-chrome-profile-is-used)
- [X/Twitter: recommended flow](#x%2Ftwitter-recommended-flow)
- [Sandboxing + host browser access](#sandboxing-%2B-host-browser-access)

​Browser login + X/Twitter posting
​Manual login (recommended)
When a site requires login, **sign in manually** in the **host** browser profile (the openclaw browser).
Do **not** give the model your credentials. Automated logins often trigger anti‑bot defenses and can lock the account.
Back to the main browser docs: [Browser](/tools/browser).
​Which Chrome profile is used?
OpenClaw controls a **dedicated Chrome profile** (named `openclaw`, orange‑tinted UI). This is separate from your daily browser profile.
Two easy ways to access it:

- **Ask the agent to open the browser** and then log in yourself.

- **Open it via CLI**:

Copy```
openclaw browser start
openclaw browser open https://x.com

```

If you have multiple profiles, pass `--browser-profile <name>` (the default is `openclaw`).
​X/Twitter: recommended flow

- **Read/search/threads:** use the **host** browser (manual login).

- **Post updates:** use the **host** browser (manual login).

​Sandboxing + host browser access
Sandboxed browser sessions are **more likely** to trigger bot detection. For X/Twitter (and other strict sites), prefer the **host** browser.
If the agent is sandboxed, the browser tool defaults to the sandbox. To allow host control:
Copy```
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        browser: {
          allowHostControl: true,
        },
      },
    },
  },
}

```

Then target the host browser:
Copy```
openclaw browser open https://x.com --browser-profile openclaw --target host

```

Or disable sandboxing for the agent that posts updates.Browser (OpenClaw-managed)Chrome Extension⌘I