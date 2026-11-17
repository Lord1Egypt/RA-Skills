# Runtime and Status

Use this file before troubleshooting. Runtime checks establish whether the daemon, extension, browser, visibility mode, license, and packaged skills are healthy.

## Startup Check

Run this sequence before diagnosing browser failures:

```bash
omnibot doctor
omnibot status
omnibot tabs
omnibot visibility status
omnibot browser current
omnibot license status
```

Interpretation:

- `doctor` checks daemon and extension health.
- `status` checks daemon status only (lighter than `doctor`).
- `tabs` proves connected tabs are visible and provides tab ids.
- `visibility status` shows whether automation is visible, background, dedicated-profile, or headless.
- `browser current` shows current browser runtime ownership.
- `license status` verifies license state.

If the extension is not connected, open Chrome or Edge with the omnibot extension loaded and keep an HTTP/HTTPS page open.

## Daemon Lifecycle

Top-level shortcuts:

```bash
omnibot status   # Show daemon status
omnibot start    # Start the daemon
omnibot stop     # Stop the daemon
omnibot run      # Run daemon in foreground
```

Full form (also supported):

```bash
omnibot daemon run
omnibot daemon start
omnibot daemon stop
omnibot daemon status
```

## doctor

```bash
omnibot doctor
```

Use `doctor` first when commands fail, tabs are empty, screenshots fail, or the agent cannot reach the browser.

## tabs

```bash
omnibot tabs
```

Use `tabs` to discover tab ids. Save the target tab id and use it on every page-state command:

```bash
OMNIBOT_SESSION_TOKEN=research omnibot snapshot -i --tab-id <TAB_ID>
```

## browser list/current

```bash
omnibot browser list
omnibot browser current
```

Use browser status when multiple browser runtimes or agents may be active.

## visibility status

```bash
omnibot visibility status
```

Use visibility status to confirm whether automation should share the user's visible browser state. Headless and dedicated-profile modes do not automatically inherit user login.

## license status

```bash
omnibot license status
```

Use license status when runtime checks pass but features appear unavailable.

## version

```bash
omnibot version
omnibot --version
omnibot -V
```

Use `version` to print the installed omnibot CLI version. Output is a single line in the form `omnibot <version>` with no banner, JSON, or daemon calls. Prefer this over `omnibot --help` or `doctor` when you only need the version string.

## skills path

```bash
omnibot skills path
```

Use skills path to locate packaged skills for installation or inspection.

## Skills Install

```bash
omnibot skills install --agent hermes --profile nuwa
omnibot skills install --agent opencode
omnibot skills install --agent claude
omnibot skills install --agent codex
omnibot skills install --agent openclaw
omnibot skills install --agent workbuddy
omnibot skills install --agent trae
```

Install only when setting up or repairing an agent integration. It is not part of normal page operations.
