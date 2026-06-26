<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/shell.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# Shell

`hp shell` opens an interactive terminal session with proxy environment variables already configured for HTTPeep. It is the fastest way to capture traffic from command-line tools, package managers, SDKs, and test commands that honor `HTTP_PROXY` and `HTTPS_PROXY`.

`hp` is the short alias for `httpeep-cli`; both command names work the same way.

## What it does

When you run `hp shell`, the CLI:

1. Starts the HTTPeep proxy if it is not already running.
2. Reuses the running proxy when a live proxy instance is already available.
3. Generates capture setup files under `~/.httpeep/automatic-setup/`.
4. Loads proxy environment variables such as `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, `http_proxy`, and `https_proxy`.
5. Enables runtime hooks for Node.js, Python, Ruby, and Java/JVM tooling.
6. Enters a child shell in the current terminal.

When you exit that child shell, you return to your original terminal session.

> **Note:**
> A normal CLI process cannot mutate the parent shell environment directly. `hp shell` intentionally enters a child shell so capture stays scoped to that terminal session.

## How it chooses the proxy endpoint

`hp shell` uses the configured proxy host and port from the running HTTPeep runtime. If the proxy is configured to bind to an unspecified address such as `0.0.0.0`, `::`, or `[::]`, the shell uses `127.0.0.1` for client-side proxy environment variables.

This keeps local command-line tools connecting to the loopback interface while the proxy can still listen on a wider bind address.

## Verify the capture environment

Inside the shell, run:

```bash
echo "$HTTPEEP_INTERCEPT_ACTIVE"
echo "$HTTP_PROXY"
curl -v https://httpbin.org/get
```

Then open HTTPeep and confirm the request appears in the session list.

## Inspect captured traffic

Open another terminal or run after leaving the shell:

```bash
hp sessions list --keyword api.example.com
hp --format json sessions list --fields id,method,url,status_code,timing
```

## Disable capture inside the shell

If you want to keep the shell open but remove the HTTPeep environment, run:

```bash
httpeep_intercept_off
```

You can also leave the capture shell entirely:

```bash
exit
```

## Generated setup files

The command writes reusable setup artifacts to:

```text
~/.httpeep/automatic-setup/
```

Important files include:

| File | Purpose |
|---|---|
| `httpeep_env_automatic_setup.sh` | POSIX shell environment setup |
| `httpeep_env_automatic_setup_run.sh` | POSIX run script used by `hp shell` |
| `httpeep_env_automatic_setup.ps1` | PowerShell environment setup |
| `node/httpeep-node-bootstrap.js` | Node.js runtime hook |
| `python/sitecustomize.py` | Python runtime hook |
| `ruby/httpeep_proxy.rb` | Ruby runtime hook |

## When to use it

Use `hp shell` when you want to capture a sequence of terminal commands without editing each command individually:

```bash
hp shell
npm install
python scripts/smoke_test.py
curl -v https://api.example.com/health
exit
```

For non-interactive automation, prefer explicit environment variables or command-specific proxy flags so scripts do not block inside an interactive shell.

For launching desktop applications or browsers with capture enabled, use `hp launch` instead.

> **Tip:**
> `hp shell` is also used by `hp record start --shell` workflows so recorded terminal traffic goes through the same proxy setup path. If you only need to send one request through HTTPeep, `hp request --url ...` is usually simpler.
