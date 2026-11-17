# Scripts

These stdlib-only scripts provide deterministic CLI update and execution handling. The default execution path remains:

`modellix-cli model run --wait` → `modellix-cli task download`

## preflight.py

Environment check for CLI-first routing. Before doctor or any paid submit, it queries the public npm `latest` tag and installs the exact release only when the CLI is missing or older. It never downgrades a newer installed CLI.

Usage:

```bash
python scripts/preflight.py
python scripts/preflight.py --json
```

Checks:

- `modellix-cli` availability
- Installed and public-latest CLI versions, update source, and any non-fatal update warning
- Safe automatic upgrade before execution; `MODELLIX_CLI_AUTO_UPDATE=0|false|off` disables it
- Doctor result (Node, auth source, connectivity, balance) when CLI exists; a failed doctor check blocks a ready recommendation
- `MODELLIX_API_KEY` / discoverable profile auth
- Recommended mode (`cli`, `rest`, or `none` when readiness is not verified)

Credential handling policy:

- Default to session-only `MODELLIX_API_KEY` usage.
- Persist with explicit user approval via `modellix-cli auth login` / `init` (preferred) or user-level env.
- Do not write system-level env vars or other agent config files.

## invoke_and_poll.py

Optional wrapper: CLI uses `model run --wait`; REST keeps submit + poll fallback.
If this script fails, switch to the direct CLI commands and continue.

Usage:

```bash
python scripts/invoke_and_poll.py \
  --model-slug google/nano-banana-2-lite \
  --body '{"prompt":"A cinematic portrait of a fox in a misty forest at sunrise"}'

python scripts/invoke_and_poll.py \
  --model-slug bytedance/seedance-2.0-mini-t2v \
  --body '{"prompt":"A cat in a garden"}' \
  --timeout 10m \
  --output-dir ./outputs
```

Key behavior:

- Mode `auto` (default): resolve/update CLI before paid submission, pin that executable for submit/wait/download, otherwise use REST
- CLI path: single `modellix-cli model run --wait --json` (no hand-rolled poll loop; no paid-submit auto-retry)
- Optional `--output-dir` triggers `task download` after a successful CLI wait
- REST path: submit a paid POST exactly once, then retry only safe task-status reads on transient `408`/`429`/`5xx` responses or transport failures
- An explicit `--api-key` is passed to child CLI processes through `MODELLIX_API_KEY`, never as a process argument
- `--model-slug` is required in `provider/model` format
- Skill defaults when user omits a model: T2I=`google/nano-banana-2-lite`, T2V=`bytedance/seedance-2.0-mini-t2v`, TTS=`alibaba/qwen-audio-3.0-tts-flash`, STT=`openai/whisper-1`, STS=`alibaba/cosyvoice-clone` (full table in `SKILL.md`)
