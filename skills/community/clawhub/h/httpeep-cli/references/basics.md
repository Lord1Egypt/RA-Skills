<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/basics.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# httpeep-cli: command-line interface overview

`httpeep-cli` is the command-line interface for HTTPeep. It exposes the full feature set of the proxy engine — capturing traffic, querying sessions, managing rules, and replaying requests — without requiring you to open the desktop UI.

There are three primary use cases for `httpeep-cli`:

1. **Script and CI integration** — start the proxy, run your test suite, capture sessions, and query them programmatically from shell scripts or pipeline steps
2. **AI agent workflows** — structured JSON output makes captured traffic easy for tools like Claude or Codex to parse and reason about
3. **Power user workflows** — record/replay sessions, bulk-manage rules, and monitor live traffic from an interactive terminal dashboard

## Installation

`httpeep-cli` is bundled with the HTTPeep desktop app. When you install HTTPeep, the CLI is placed on your PATH automatically during first launch. No separate install step is needed.

When you update the desktop app, the bundled `httpeep-cli` / `hp` binary updates together with it. On Linux standalone installs, use `hp update` or rerun the install script.

Verify the CLI is available:

```bash
httpeep-cli --version
```

`hp` is available as a short alias for interactive use. Documentation and automation examples use the full `httpeep-cli` command for clarity.

### Fixing PATH issues

If the CLI is installed but your shell can't find it:


### Open HTTPeep settings

Go to **Settings → MCP** in the desktop app.

### Repair the PATH installation

Click **Repair CLI / PATH Installation**.

### Restart your terminal

Open a new terminal window and run `httpeep-cli --version` to confirm the fix.

> **Note:**
> You can also trigger the repair from within an MCP-connected AI agent by calling the `httpeep_mcp_repair_cli_path_installation` tool directly.

## Global flags

These flags work with every `httpeep-cli` command.

| Flag | Description | Default |
|---|---|---|
| `--format <fmt>` | Output format: `human`, `json`, or `table` | `human` |
| `--quiet` / `-q` | Suppress informational messages | — |
| `--verbose` / `-v` | Enable verbose output | — |
| `--color <mode>` | Color output: `auto`, `always`, or `never` | `auto` |
| `-h`, `--help` | Print help | — |
| `-V`, `--version` | Print version | — |

## Output formats

Every command that produces tabular output supports three formats. Choose the format that fits your workflow.

| Format | Description | Best for |
|---|---|---|
| `human` | Human-readable plain text | Interactive terminal use |
| `json` | JSON array or object | Scripting and `jq` pipelines |
| `table` | Aligned columns with borders | Quick overview in terminal |

Append `--format <fmt>` to any command to switch formats:

```bash
httpeep-cli --format json sessions list \
  --page 1 \
  --page-size 25 \
  --fields id,method,url,status_code,timing
httpeep-cli rules list --format table
httpeep-cli --format json proxy status
```

> **Warning:**
> `sessions watch` with `--format json` outputs **NDJSON** (one JSON object per line), which is ideal for streaming pipelines.

## JSON output and jq pipelines

Use `--format json` with `jq` to build powerful one-liners over your captured traffic.

```bash
# Filter to only failed requests
httpeep-cli --format json sessions list --fields id,method,url,status_code,timing | \
  jq '.[] | select(.status_code >= 400)'

# Find slow requests (over 500 ms)
httpeep-cli --format json sessions list --fields id,method,url,status_code,timing | \
  jq '.[] | select(.timing.total_ms > 500) |
      {url, status_code, total_ms: .timing.total_ms}'

# Compute error rate
httpeep-cli --format json sessions list --fields id,status_code | \
  jq '{ total: length, errors: [.[] | select(.status_code >= 400)] | length } |
       .error_rate = (.errors / .total * 100 | round)'

# List unique domains
httpeep-cli --format json sessions list --fields domain | jq '[.[].domain] | unique | sort[]'

# Keep JSON compact for AI agents or CI logs
httpeep-cli --format json sessions list --fields id,method,url,status_code,timing
```

> **Tip:**
> In CI environments, use `--format json` together with `--fields` to get clean, machine-parseable output with no ANSI escape codes in your logs.

## Troubleshooting


### httpeep-cli: command not found

The CLI binary is not on your PATH. Open the HTTPeep desktop app, go to **Settings → MCP**, and click **Repair CLI / PATH Installation**. Then restart your terminal and try again.

### Error: proxy engine not reachable

`httpeep-cli` connects to the proxy engine through the local control endpoint. Start the app and retry, or start the proxy directly with `httpeep-cli proxy start`.

### Permission denied on cert install

Certificate installation requires elevated privileges. Run the command with `sudo`:

    ```bash
    sudo httpeep-cli cert install
    ```

    Alternatively, use **Settings → Certificate** in the desktop app, which handles the privilege prompt automatically.

### Sessions not appearing for my app

Check that your application is configured to route through the proxy:

    ```bash
    HTTP_PROXY=http://localhost:8080 HTTPS_PROXY=http://localhost:8080 your-app
    ```

    Or verify the system proxy is enabled:

    ```bash
    httpeep-cli proxy system status
    ```

    For HTTPS traffic, confirm the root CA is trusted:

    ```bash
    httpeep-cli cert status
    ```

### Output is garbled in CI logs

Color codes from terminal output can corrupt CI log displays. Use `--format json` to produce clean output:

    ```bash
    httpeep-cli --format json sessions list --fields id,method,url,status_code,timing
    ```
