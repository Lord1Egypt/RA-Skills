<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/overview.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# CLI Overview

`hp` lets you control HTTPeep from the terminal for local debugging, automation, and CI pipelines.

`hp` is the short alias for `httpeep-cli`; both command names work the same way.

## What you can do with CLI

- **Manage proxy lifecycle** — start, pause, resume, and stop the proxy engine
- **Query and inspect sessions** — list, filter, watch, and delete captured traffic
- **Manage DNS overrides** — replace DNS configs, switch active environments, and update host mappings
- **Create and test rules** — upsert, validate, test, import, and export forwarding rules
- **Launch capture-ready apps** — open browsers, terminals, Electron apps, and desktop apps through HTTPeep
- **Send and replay requests** — issue HTTP requests through the proxy and replay captured sessions
- **Record traffic flows** — capture sessions into reusable script files
- **Import external traffic** — convert cURL commands, HAR files, or raw HTTP messages
- **Monitor live traffic** — watch real-time traffic in a terminal dashboard
- **Manage certificates** — install and inspect the HTTPS interception root CA

## Command guides


### CLI Basics

Installation, global flags, output formats, and troubleshooting.

### Proxy

Start, pause, resume, stop, and configure the proxy engine.

### Sessions

Browse, filter, watch, and delete captured sessions.

### DNS

Manage global and environment-scoped DNS overrides.

### Shell

Enter an interactive shell with proxy environment variables set.

### License

Activate a license key and inspect license runtime status.

### Launch

Launch browsers, terminals, and apps with capture enabled.

### Rules

Manage traffic manipulation rules from the terminal.

### Request

Send HTTP requests through the proxy with temporary rules.

### Replay

Replay captured sessions with retry and temporary overrides.

### Record

Record traffic flows into reusable script files.

### Certificate

Install and inspect the HTTPS interception root CA.

### Import

Import traffic from cURL, HAR, and raw HTTP files.

### Monitor

Watch live traffic in a real-time terminal dashboard.

## Common workflows

### Start the proxy and watch traffic

```bash
hp proxy start --port 8800
hp --format json sessions watch
```

### Enter a proxy-enabled shell

```bash
hp shell
curl https://api.example.com/users
exit
```

### Launch Chrome and watch new captures

```bash
hp launch chrome --url "https://example.com" --watch
```

### Send a request and inspect the result

```bash
hp --format json request --method GET --url "https://httpbin.org/get"
hp sessions list --keyword httpbin
```

### Apply a temporary redirect and auto-rollback

```bash
hp rules run \
  --map-remote "api.example.com=http://127.0.0.1:3000" \
  -- hp request --method GET --url "https://api.example.com/users"
```

### Replay a session with retry

```bash
hp replay --id <session_id> --retry-times 3 --retry-interval-ms 800
```

> **Tip:**
> All commands support `--format json` for machine-parseable output. Combine with `jq` for powerful scripting pipelines.
