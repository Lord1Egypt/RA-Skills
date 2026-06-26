<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/proxy.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# Proxy

The `proxy` subcommand controls the HTTPeep proxy engine lifecycle. The `capture` alias is equivalent to `proxy` and is provided for users who think in terms of "capturing traffic" rather than "managing a proxy."

## proxy start

Start the proxy server in the background.

```bash
httpeep-cli proxy start --port 8800
```

| Flag | Description | Default |
|---|---|---|
| `--port <port>` | Listen port for the proxy | — |
| `--capture-pid <pid>` | Only capture traffic from the given process ID (repeatable) | — |
| `--watch` | Start watching new sessions immediately after the proxy starts | — |

Capture traffic from specific processes only:

```bash
httpeep-cli proxy start --capture-pid 1234 --capture-pid 5678
```

Start and immediately watch new traffic:

```bash
httpeep-cli proxy start --watch
```

## proxy pause

Pause traffic capture while keeping transparent forwarding active. Requests continue to flow through the proxy but are not stored as sessions.

```bash
httpeep-cli proxy pause
```

## proxy resume

Resume traffic capture after a pause.

```bash
httpeep-cli proxy resume
```

## proxy stop

Stop the proxy server completely.

```bash
httpeep-cli proxy stop
```

## proxy restart

Restart the proxy server. This is equivalent to `stop` followed by `start`.

```bash
httpeep-cli proxy restart
```

## proxy status

Get the current proxy status.

```bash
httpeep-cli proxy status
```

## proxy info

Show detailed instance information, including the lock file path and uptime.

```bash
httpeep-cli proxy info
```

## proxy logs

Show the log file location and tail recent logs.

```bash
# Show the last 50 lines
httpeep-cli proxy logs

# Show the last 100 lines
httpeep-cli proxy logs --lines 100

# Follow new log output
httpeep-cli proxy logs --follow
```

| Flag | Description | Default |
|---|---|---|
| `--lines <n>` | Number of lines to show | 50 |
| `--follow` / `-f` | Follow log output continuously | — |

## proxy system

Configure the system proxy settings so that all applications route traffic through HTTPeep automatically.

```bash
# Enable system proxy
httpeep-cli proxy system on

# Disable system proxy
httpeep-cli proxy system off

# Check system proxy status
httpeep-cli proxy system status
```

## capture alias

`capture` is a direct alias for `proxy`. All of the above commands work identically with `capture`:

```bash
httpeep-cli capture start --port 8800
httpeep-cli capture status
httpeep-cli capture pause
```

> **Note:**
> When the proxy is stopped, traffic no longer flows through HTTPeep. Existing captured sessions remain in the session store until you clear them.
