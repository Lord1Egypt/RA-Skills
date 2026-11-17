# codex engine details

`codex-image.mjs` runs `codex exec --json -c model_provider="openai" -m <model> --sandbox <mode> -C
<outdir> [--image <ref>]... -`, tells the session to call the built-in `image_gen.imagegen`, and
copies this run's image from `$CODEX_HOME/generated_images/` to `--out`. It uses your Codex login
and never reads `OPENAI_API_KEY`.

## Flags

| Flag | Meaning |
|---|---|
| `--aspect` | `1:1` (default), `3:2`, `2:3`, `4:3`, `3:4`, `16:9`, `9:16`, `2.35:1`. `image_gen` has no size parameter, so the script appends the format to the prompt it hands over (e.g. "Square 1:1 image.") and asks Codex to pass it on unchanged; measured outputs: 1:1 → 1254×1254 or 1024×1024, 4:3 → 1448×1086, 16:9 → 1672×941 |
| `--model` / `--effort` | Codex model and reasoning effort, default `gpt-6-luna` / `low`; it only has to call the image tool |
| `--sandbox` | Default `workspace-write` (only the output folder is writable); `read-only` cannot work |
| `--escalate-sandbox` | Does not widen the sandbox by itself. A later attempt uses `danger-full-access` only when the log says the sandbox blocked the write and the user has set `IMAGE_GEN_SANDBOX_ESCALATE=yes`. The agent must not set that variable. Other failures stay in `workspace-write` |
| `--retries` | Default 2 (3 attempts in total) |
| `--timeout` | Milliseconds per attempt, default 300000 |

## Why the provider is pinned

A Codex config can route requests through a custom provider or local gateway (for example
`model_provider = "local-gateway"` with `model = "auto"`). Such gateways may not forward image
generation, and switching only the provider then fails with `The model 'auto' is unavailable`. The
script therefore passes the official provider and a concrete model on every call and leaves your
config file untouched.

## Why old images are rejected

A PNG header does not prove the image is new. During a network outage, Codex once failed to call the
image tool and copied an unrelated two-month-old picture out of `generated_images/` instead. The
script lists and hashes only that subdirectory of `CODEX_HOME` before each run. It does not read
auth, config, or session files. An output whose sha256 matches an older file is deleted, counted as
a failure and retried.

## Common errors

| Error | What to do |
|---|---|
| `codex_not_installed` | Install Codex and run `codex login` |
| `no valid PNG at <out>` | Codex did not call the image tool, or the sandbox blocked the write. Read the log. Ask the user before a wider sandbox. They set `IMAGE_GEN_SANDBOX_ESCALATE=yes` themselves if they approve it |
| `rejected output: byte-identical to a pre-existing image` | The image tool failed underneath and Codex reused an old file; check the log for network errors and retry. Never treat it as success |
| `timeout` | Raise `--timeout` and check the network |

On failure the logs stay in `<outdir>/.codex-img-<timestamp>/attempt-N.log`; on success they are
deleted.
