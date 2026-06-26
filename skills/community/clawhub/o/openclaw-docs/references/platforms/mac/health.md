# Health Checks

Source: https://docs.openclaw.ai/platforms/mac/health

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationmacOS companion appHealth ChecksGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpPlatforms overview
PlatformsmacOS AppLinux AppWindows (WSL2)Android AppiOS App
macOS companion app
macOS Dev SetupMenu BarVoice WakeVoice OverlayWebChatCanvasGateway LifecycleHealth ChecksMenu Bar IconmacOS LoggingmacOS PermissionsRemote ControlmacOS SigningmacOS ReleaseGateway on macOSmacOS IPCSkillsPeekaboo Bridge
On this page
- [Health Checks on macOS](#health-checks-on-macos)
- [Menu bar](#menu-bar)
- [Settings](#settings)
- [How the probe works](#how-the-probe-works)
- [When in doubt](#when-in-doubt)

​Health Checks on macOS
How to see whether the linked channel is healthy from the menu bar app.
​Menu bar

Status dot now reflects Baileys health:

- Green: linked + socket opened recently.

- Orange: connecting/retrying.

- Red: logged out or probe failed.

- Secondary line reads “linked · auth 12m” or shows the failure reason.

- “Run Health Check” menu item triggers an on-demand probe.

​Settings

- General tab gains a Health card showing: linked auth age, session-store path/count, last check time, last error/status code, and buttons for Run Health Check / Reveal Logs.

- Uses a cached snapshot so the UI loads instantly and falls back gracefully when offline.

- **Channels tab** surfaces channel status + controls for WhatsApp/Telegram (login QR, logout, probe, last disconnect/error).

​How the probe works

- App runs `openclaw health --json` via `ShellExecutor` every ~60s and on demand. The probe loads creds and reports status without sending messages.

- Cache the last good snapshot and the last error separately to avoid flicker; show the timestamp of each.

​When in doubt

- You can still use the CLI flow in [Gateway health](/gateway/health) (`openclaw status`, `openclaw status --deep`, `openclaw health --json`) and tail `/tmp/openclaw/openclaw-*.log` for `web-heartbeat` / `web-reconnect`.

Gateway LifecycleMenu Bar Icon⌘I