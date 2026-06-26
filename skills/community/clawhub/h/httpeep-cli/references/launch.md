<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/launch.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# Launch

`hp launch` starts another application with HTTPeep proxy capture enabled. It can auto-start the proxy, reuse an existing proxy instance, launch known browsers, open a capture-ready terminal, and optionally restrict capture to the launched process ID.

`hp` is the short alias for `httpeep-cli`; both command names work the same way.

## launch chrome

Launch Google Chrome with HTTPeep proxy settings.

```bash
hp launch chrome
hp launch chrome --url "https://example.com"
hp launch chrome --url "https://example.com" --watch
```

## launch edge

Launch Microsoft Edge with HTTPeep proxy settings.

```bash
hp launch edge
hp launch edge --url "https://example.com"
```

## launch terminal

Open a new terminal session with HTTPeep proxy environment variables configured.

```bash
hp launch terminal
```

This is useful when you want a separate terminal window instead of replacing the current terminal session with `hp shell`.

## launch electron

Launch an Electron app and force the Electron launcher strategy.

```bash
hp launch electron --app ./dist/my-electron-app.exe
hp launch electron --pick
```

## launch app

Launch any selected application with HTTPeep proxy settings.

```bash
hp launch app --app "C:\\Program Files\\Example\\Example.exe"
hp launch app --pick
hp launch app --app ./MyApp --kind executable
```

| Option | Description |
|---|---|
| `--app <PATH>` | Application path to launch |
| `--pick` | Select an application with a system picker |
| `--kind <kind>` | Force launcher strategy: `auto`, `chromium`, `electron`, `app`, or `executable` |
| `--url <url>` | URL to open for Chromium-based targets |

## Legacy root form

For compatibility, `hp launch` still accepts app launch flags directly at the root level.

```bash
hp launch --app ./MyApp
hp launch --pick
hp launch --app ./MyApp --kind electron --url "https://example.com"
```

Prefer the explicit subcommands for new scripts:

```bash
hp launch app --app ./MyApp
hp launch electron --app ./MyElectronApp
```

## Proxy and capture options

These options are available on browser and app launch commands.

| Option | Description |
|---|---|
| `--port <port>` / `-p <port>` | Proxy port to auto-start or reuse |
| `--no-start-proxy` | Do not auto-start the proxy; fail if no live proxy is available |
| `--capture-pid-only` | After launch, update capture policy to only capture the launched process PID |
| `--watch` | Watch newly captured sessions after launch |

Examples:

```bash
# Start or reuse proxy on a specific port
hp launch chrome --port 8800 --url "https://example.com"

# Require an already-running proxy
hp launch app --app ./MyApp --no-start-proxy

# Capture only the launched process
hp launch chrome --capture-pid-only

# Launch and immediately stream new sessions
hp launch chrome --url "https://example.com" --watch
```

> **Note:**
> `--watch` streams newly captured sessions until you stop it with `Ctrl+C`. Use `hp --format json sessions watch` separately when you need NDJSON output for automation.
