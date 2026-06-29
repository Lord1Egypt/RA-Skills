# Troubleshooting

## Exit Codes

| Code | Category | Meaning |
|------|----------|---------|
| 0 | success | Command completed successfully |
| 2 | config | Configuration error (missing provider, bad config, auth issue) |
| 3 | api | API error (generation/edit failure, network, auth rejected) |
| 4 | image | Image error (decode, encode, mask, canvas, file I/O) |
| 1 | generic | Unclassified error |

## Security rules while troubleshooting

- Never ask the user to paste API keys into chat or commands.
- Never configure credentials yourself unless the user explicitly asks you to start interactive auth or perform non-interactive credential setup.
- If creds are missing, instruct the user to run `potaco auth add <provider>` in an interactive TTY.
- Do not print `POTACO_API_KEY`, shell history, `~/.potaco/credentials.enc`, or `~/.potaco/.salt`.
- Share dry-run/debug output only after checking it has no private prompts, paths, or endpoint URLs.

## Error output

Friendly errors print to stderr/TTY. Raw `UserError` details append to `~/.potaco/debug.log`. Non-TTY output is plain text.

## Common errors

#### "No active provider configured"

```
Error: No active provider configured.
Hint: Run 'potaco auth add <provider>' to connect one.
```

Fix: tell the user to run `potaco auth add openai` (or `fal`/`vercel`) interactively unless they explicitly asked you to configure credentials.

#### "No API key found for the active provider"

```
Error: No API key found for the active provider.
```

Fix: the CLI hint may mention `--api-key`, but the safer instruction is for the user to re-add the provider interactively: `potaco auth add openai`.

#### "Could not load configuration"

```
Error: Could not load configuration.
Hint: Check that ~/.potaco/ is readable.
```

Fix: check permissions on `~/.potaco/` and `~/.potaco/config.yaml`. If corrupted, regenerate via interactive auth.

#### "Image generation failed"

```
Error: Image generation failed.
Hint: Check your API key, network connection, and model name.
```

Fix: if safe, check `~/.potaco/debug.log` for the raw error. Common causes:
- 401: invalid or expired API key.
- 404: model name not found by the provider. Check `potaco models`.
- 429: rate limited. Retries with exponential backoff are automatic (default 2 retries). Increase with `--retries 5` or `POTACO_RETRIES=5`.
- Timeout: increase with `--timeout 300` or `POTACO_TIMEOUT=300`.

#### "Image editing failed"

Same as generation but for the edit endpoint. Also check that the source image file exists and is a valid PNG/JPEG/WebP.

#### "Image editing is not supported by the Vercel AI Gateway provider"

```
Error: Image editing is not supported by the Vercel AI Gateway provider.
Hint: Use 'potaco use openai' or 'potaco use fal' to switch to a provider
that supports editing.
```

Fix: Switch to a provider that supports editing: `potaco use openai`, `potaco use fal`, or `potaco use custom`.

#### "Cannot write to '<path>'"

```
Error: Cannot write to '/tmp/output.png'.
Hint: Check that the path is valid and you have write permissions.
```

Fix: output path must be a writable file path and parent directory must exist.

#### "'<path>' is a directory, not a file."

```
Error: '/output/' is a directory, not a file.
Hint: Specify a filename ending in .png or .jpeg, or omit -o to auto-generate one.
```

Fix: provide a filename, not a directory path. Example: `-o /output/result.png`.

#### "Cannot write multiple images to stdout"

```
Error: Cannot write multiple images to stdout.
Hint: Use --output to write to files, or request a single image with --n 1.
```

Fix: use `--output` or set `--n 1`.

#### "Could not decode the image returned by the provider"

```
Error: Could not decode the image returned by the provider.
Hint: The provider may have returned an unsupported image format. Try a
different model or check '~/.potaco/debug.log' for details.
```

Fix: try a different model or inspect the debug log if safe.

#### "Unknown provider: <name>"

```
Error: unknown provider: foo (available: [custom fal openai vercel])
```

Fix: Use one of the registered provider names: `openai`, `fal`, `vercel`, or `custom`.

#### "A base URL is required for OpenAI-compatible providers."

```
Error: A base URL is required for OpenAI-compatible providers.
Hint: Use --base-url, set POTACO_BASE_URL, or run 'potaco config set providers.openrouter.base_url <url>'.
```

Fix: prefer `potaco auth add custom` or `potaco auth add <name> --type openai-compatible` interactively with a trusted base URL. Use `--base-url`, `POTACO_BASE_URL`, or `potaco config set providers.<name>.base_url <url>` only in explicitly approved non-interactive workflows.

## Debugging Workflow

1. Run with `--verbose`.
2. Run with `--dry-run` to inspect payload without API spend, headers are redacted.
3. Check `~/.potaco/debug.log` only if it will not expose sensitive context.
4. Run `potaco status --json` to verify the current provider, model, and key status programmatically.
5. Run `potaco auth list --json` to verify all connected providers.

## Retry Behavior

Default: 2 retries with exponential backoff + jitter for 5xx, 429, and network errors.

To override:
```sh
potaco gen --prompt "test" --retries 5
POTACO_RETRIES=5 potaco gen --prompt "test"
potaco config set retries 5
```

## Non-Interactive Mode

`--non-interactive`/`POTACO_NON_INTERACTIVE=1` skips TUI and automatic update prompts, disables color/spinner, and requires explicit args. It is plain support for agents and automated terminal execution, not a polished scripting API. For `auth add`, it requires `--api-key`; use only with explicit approval because secrets may leak through flags/env handling.

## Programmatic Usage (JSON Output)

Common JSON outputs:

- `potaco status --json`: active provider, model, base_url, all providers (with base_url, has_key, is_active, added_at), file paths.
- `potaco auth list --json`: array of providers with name, model, base_url, has_key, is_active.
- `potaco models --json` / `potaco models list --json`: array of models with id and display_name.
- `potaco version --json`: current, latest, update_available fields.
- `potaco info <path> --json`: path, format, width, height, file_size, color_model.
- `potaco gen --json` / `potaco edit --json`: path, format, dimensions, model, params, latency_ms.

Use `--json` when an agent needs to parse output programmatically. JSON output goes to stdout, error output goes to stderr.
