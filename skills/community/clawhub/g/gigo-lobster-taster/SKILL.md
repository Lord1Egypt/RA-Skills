---
name: gigo-lobster-taster
description: "🦞 GIGO · gigo-lobster-taster: 正式试吃模式：跑完整评测，默认上传云端、生成个人结果页并进入排行榜。 Triggers: 试吃我的龙虾 / 品鉴我的龙虾 / lobster taste / lobster taster."
metadata: {"openclaw":{"emoji":"🦞","os":["darwin","linux","win32"],"requires":{"anyBins":["python3","python","py"]}}}
---

# gigo-lobster-taster

## Mission

- 正式试吃模式：跑完整评测，默认上传云端、生成个人结果页并进入排行榜。
- Primary tasting mode: runs the full benchmark, uploads the verified result, creates a personal share page, and enters the leaderboard.

## Trigger Phrases

- 中文：试吃我的龙虾 / 品鉴我的龙虾 / 鉴定我的龙虾 / 评估我的龙虾
- English: lobster taste / lobster taster / taste my lobster / lobster eval

## Execution Rules

1. Use a direct Python command on this skill directory's wrapper file. Never use `cd ... && python ...`; OpenClaw preflight may reject it.
2. Prefer `python3`, then `python`, then `py`.
3. If the user asked in Chinese, append `--lang zh`. If the user asked in English, append `--lang en`.
4. Stream short progress updates while the benchmark is running.
5. Keep stdout/stderr visible and remind the user that the full log is written to `gigo-run.log`.
6. Do not run `--help`, inspect the whole repo, or switch to `main.py` once the wrapper command is clear. Start the wrapper directly.
7. If the wrapper starts a long-running process, do not kill it just because stdout is quiet for a while. A full tasting run often takes 15-25 minutes.
8. While a long run is in progress, monitor the process and tail the log file under `~/.openclaw/workspace/outputs/gigo-lobster-taster/gigo-run.log` instead of improvising a second execution path.
9. Only declare failure if the process exits non-zero, the log shows a traceback, or the user explicitly asks to cancel.
10. Stay attached until the wrapper exits. Do not end the conversation with “I will keep monitoring”; keep polling and only report completion once you have the final score/result files/ref_code (if any).
11. Prefer `process poll` plus `exec tail -n 50 .../gigo-run.log` while monitoring. Do not use a generic full-file `read` on `gigo-run.log`, because the log can be large and may break the chat output.

## Default Behavior

- 中文：默认会正式上传、生成个人结果页并进入排行榜。
- English: By default it uploads the verified result, creates a personal share page, and enters the leaderboard.

## Recommended Command Shape

```bash
python3 /absolute/path/to/run_upload.py --lang zh
```

If the user explicitly asks for overrides, append the matching CLI flags:

- `--lobster-name "..."` and `--lobster-tags "tag1,tag2"` for a custom lobster persona
- `--output-dir /custom/path` for a custom output directory
- `--require-png-cert` when the user refuses the SVG fallback
- `--skip-upload` or `--register-only` only when the user explicitly asks to change the default upload behavior

## Persona Defaults

- Explicit CLI overrides win first: `--lobster-name` and `--lobster-tags`
- Then read `GIGO_LOBSTER_NAME` and `GIGO_LOBSTER_TAGS`
- Then read `SOUL.md`
- Finally fall back to the default lobster persona

Do not stop for interactive questions unless the user explicitly asks for an interactive run.
