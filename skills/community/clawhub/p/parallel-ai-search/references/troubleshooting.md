# Troubleshooting

## `parallel-cli` not found

- If installed via the shell script, ensure `~/.local/bin` is on `PATH`.
- Install:

```bash
curl -fsSL https://parallel.ai/install.sh | bash
```

Fallback install:

```bash
pipx install "parallel-web-tools[cli]"
pipx ensurepath
```

## Auth failures

Run:

```bash
parallel-cli auth
```

If not authenticated:

```bash
parallel-cli login
# or
parallel-cli login --device
```

Or set:

```bash
export PARALLEL_API_KEY="your_api_key"
```

## Timeouts

Some operations can run longer than the agent’s tool execution limit.

- Prefer `--no-wait` on long-running operations (`research run`, `enrich run`, `findall run`).
- Poll with a bounded `--timeout` (e.g., 540 seconds).
- If the poll times out, re-run the same poll command — the job continues server-side.

## Bad inputs / schema errors

- For Enrich and FindAll, validate JSON arguments are valid JSON (double quotes, no trailing commas).
- For CSV enrichment, ensure `--source-columns` actually match the CSV header names.

## Server/API errors

- If the CLI returns an API error, include the error message in your response and suggest retrying.
- If the issue persists, check Parallel status page (if available in your environment).
