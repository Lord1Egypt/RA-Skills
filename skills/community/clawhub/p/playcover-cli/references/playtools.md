# `playtools` — manage PlayTools installation

PlayTools is the PlayCover runtime injected into iOS apps to map keyboard/mouse input to touch events and provide other iOS-on-macOS bridges. The `playtools` command is a **group** for managing its system-wide installation.

---

## `playtools install`

Install (or repair) PlayTools on the system.

| Arg/Flag | Type | Description |
|----------|------|-------------|
| — | — | No arguments. |

- This is a **system-wide** setup step — PlayTools is installed once and then available to every app installed with `--play-tools`.
- The command waits up to approximately **60 seconds** for the install to complete, then reports the outcome.
- Output: `PlayTools installed` on success, or an error to stderr on timeout/failure.

```bash
# One-time setup before installing any app with PlayTools
PlayCover.app/Contents/MacOS/PlayCover playtools install
```

## When to run this

- Before the first `install ... --play-tools`.
- After a macOS upgrade that breaks the existing PlayTools install.
- If an installed app fails to launch with a "PlayTools missing" error.

## Notes

- `playtools install` is idempotent — running it when PlayTools is already installed repairs/reasserts the install rather than failing.
- It is **not** a per-app command. To inject PlayTools into a specific app at install time, use `install <ipa> --play-tools`.
- To remove PlayTools from a specific app, use `install <ipa> --no-play-tools` on re-install, or `uninstall` the app.
