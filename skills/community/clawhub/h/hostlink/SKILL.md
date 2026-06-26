---
name: hostlink
description: >
  Execute commands on the host machine from inside the OpenClaw container via
  the HostLink daemon. Provides secure, authenticated remote shell execution
  over a Unix domain socket (local) or TCP/WireGuard (remote). Use when you
  need to run commands on the host: access files outside the container, run
  host-side tools, interact with the Qwen3 merge project, manage Docker on the
  host, or execute anything requiring host-level access. The 'hostlink' binary
  is in PATH. Triggers on: "run on host", "execute on host", "host command",
  "outside container", "host machine", "hostlink", "hostlinkd".
---

# HostLink Skill

Execute commands on the host machine from inside this container.

## Quick Reference

```bash
# Execute a command on the host
hostlink exec "ls /home/jebadiah"

# Ping the daemon (connection test)
hostlink ping

# With explicit socket/token (if env vars not set)
hostlink -s /run/hostlink/hostlink.sock -k $HOSTLINK_TOKEN exec "echo hello"

# Set working directory
hostlink -w /home/jebadiah exec "pwd"

# Set environment variables
hostlink -e MY_VAR=value exec "echo $MY_VAR"

# With timeout (ms)
hostlink -T 60000 exec "long-running-command"

# JSON output (machine-readable)
hostlink -j exec "ls -la" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['stdout'])"

# List configured targets
hostlink targets
```

## Environment Variables

Set these so you don't need to pass flags every time:

| Variable | Purpose | Default |
|----------|---------|---------|
| `HOSTLINK_SOCKET` | Unix socket path | `/run/hostlink/hostlink.sock` |
| `HOSTLINK_TOKEN` | Auth token | (required) |
| `HOSTLINK_TARGET` | Target node name | (optional) |

Best place to set these: `workspace/.env` or `openclaw.json` env.vars section.

## Connection Status

Check if hostlinkd is reachable:
```bash
hostlink ping
# Expected: [hostname] pong - uptime Xs
# If error: daemon not running or socket not mounted
```

## Common Use Cases

### Access host filesystem
```bash
hostlink exec "ls /home/jebadiah/projects"
hostlink exec "cat /etc/hostname"
```

### Run host-side GPU/ML tools
```bash
hostlink exec "nvidia-smi"
hostlink exec "ollama list"
hostlink exec "ls ~/.cache/huggingface/hub"
```

### Access the Qwen3 merge project
```bash
hostlink exec "ls /path/to/qwen3-merge"
hostlink exec "cat /path/to/qwen3-merge/README.md"
```

### Docker management on host
```bash
hostlink exec "docker ps"
hostlink exec "docker stats --no-stream"
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Remote command failed (check exit_code in JSON output) |
| 2 | Connection failed (daemon unreachable) |
| 3 | Authentication failed (wrong token) |
| 5 | Timeout |
| 7 | Client error (bad args, missing targets file) |

## Troubleshooting

**"Connection failed" / exit 2:**
- hostlinkd not running on host: `sudo systemctl start hostlinkd`
- Socket not mounted: check docker-compose volume mount
- Wrong socket path: check `HOSTLINK_SOCKET` env var

**"Authentication failed" / exit 3:**
- Wrong `HOSTLINK_TOKEN` — must match auth_token in `/etc/hostlink/hostlink.conf`

**"server busy" error:**
- Host is at max_concurrent limit — retry shortly

## Architecture

```
Container (you are here)          Host machine
┌─────────────────────┐          ┌──────────────────────────┐
│  hostlink (client)  │◄────────►│  hostlinkd (daemon)      │
│  workspace/bin/     │  Unix    │  /etc/hostlink/           │
│                     │  socket  │  auth_token = <secret>    │
└─────────────────────┘          │  shell = /bin/bash        │
                                 └──────────────────────────┘
```

See `references/setup.md` for installation and docker-compose configuration.
