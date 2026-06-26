# WebChat

Source: https://docs.openclaw.ai/platforms/mac/webchat

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationmacOS companion appWebChatGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpPlatforms overview
PlatformsmacOS AppLinux AppWindows (WSL2)Android AppiOS App
macOS companion app
macOS Dev SetupMenu BarVoice WakeVoice OverlayWebChatCanvasGateway LifecycleHealth ChecksMenu Bar IconmacOS LoggingmacOS PermissionsRemote ControlmacOS SigningmacOS ReleaseGateway on macOSmacOS IPCSkillsPeekaboo Bridge
On this page
- [WebChat (macOS app)](#webchat-macos-app)
- [Launch & debugging](#launch-%26-debugging)
- [How it’s wired](#how-it%E2%80%99s-wired)
- [Security surface](#security-surface)
- [Known limitations](#known-limitations)

​WebChat (macOS app)
The macOS menu bar app embeds the WebChat UI as a native SwiftUI view. It
connects to the Gateway and defaults to the **main session** for the selected
agent (with a session switcher for other sessions).

- **Local mode**: connects directly to the local Gateway WebSocket.

- **Remote mode**: forwards the Gateway control port over SSH and uses that
tunnel as the data plane.

​Launch & debugging

Manual: Lobster menu → “Open Chat”.

Auto‑open for testing:
Copy```
dist/OpenClaw.app/Contents/MacOS/OpenClaw --webchat

```

Logs: `./scripts/clawlog.sh` (subsystem `bot.molt`, category `WebChatSwiftUI`).

​How it’s wired

- Data plane: Gateway WS methods `chat.history`, `chat.send`, `chat.abort`,
`chat.inject` and events `chat`, `agent`, `presence`, `tick`, `health`.

- Session: defaults to the primary session (`main`, or `global` when scope is
global). The UI can switch between sessions.

- Onboarding uses a dedicated session to keep first‑run setup separate.

​Security surface

- Remote mode forwards only the Gateway WebSocket control port over SSH.

​Known limitations

- The UI is optimized for chat sessions (not a full browser sandbox).

Voice OverlayCanvas⌘I