---
name: piccc-ai
description: Generate images, videos, and audio with Piccc AI (皮可AI), or query and download existing media tasks. Use when the user asks to create visual or audio media with Piccc AI, discover its current models or voices, check an asynchronous task, or download completed results. Do not use for editing existing local media.
---

# Piccc AI (皮可AI)

Use `{baseDir}/scripts/piccc.mjs` for every Piccc AI request. `{baseDir}` is the directory containing this file.

## Language

- Reply in the user's current language.
- Do not mix translated Chinese and English phrases in one response. The product name `Piccc AI (皮可AI)` is the only intentional bilingual form.
- Treat CLI output as internal data and explain it naturally in the user's language.

## Installation and first authorization

When the skill has just been installed, tell the user in their current language that installation is complete, browser authorization is required, and the available credit balance will be reported afterward.

Before the first request, run `node {baseDir}/scripts/piccc.mjs auth status`. If it reports `authenticated: false`:

1. Explain that the user must sign in and approve access in the browser.
2. Run `node {baseDir}/scripts/piccc.mjs auth login` and wait for it to finish. The command opens the authorization page, receives the local callback, saves the API key, and queries the available balance. Do not ask the user to report completion.
3. If the browser cannot be opened, share the displayed link and verification code while the command keeps waiting. Never ask the user to create, copy, or paste an API key.
4. After authorization, read `available_credits` from the result and report the balance in the user's current language.
5. If `available_credits` is unavailable, run `node {baseDir}/scripts/piccc.mjs credits` and then report the returned balance.

## Workflow

1. Unless the user names a model or asks for higher quality, run `models TYPE --economy` and use its selected model and defaults. Prefer lower cost over speed or quality.
2. Let explicit user requirements override economy defaults. Otherwise use one output, the lowest supported resolution and quality, the shortest supported video duration, no audio or web search, and the lowest supported audio sample rate.
3. If `special_offer` is true, warn the user in their current language before submission that special-offer models may be slower and less reliable.
4. Select only values advertised by the live model response. Never invent model IDs, voice IDs, formats, ratios, resolutions, modes, or durations.
5. Put long or multiline prompts in a UTF-8 file and use `--prompt-file`.
6. When the user expects a finished file, use `--wait --output-dir DIR` in the initial request. Do not create another task while waiting.
7. On timeout, return the task ID and latest status so the same task can be resumed. Treat `completed`, `failed`, and `cancelled` as terminal.
8. For audio, call the initial 10 credits a precharge and use `actual_cost` from the completed task as the final cost.

## Commands

```bash
node {baseDir}/scripts/piccc.mjs models image
node {baseDir}/scripts/piccc.mjs models video
node {baseDir}/scripts/piccc.mjs models audio
node {baseDir}/scripts/piccc.mjs models image --economy
node {baseDir}/scripts/piccc.mjs voices --model MODEL_ID --search Chinese

node {baseDir}/scripts/piccc.mjs generate image --model MODEL_ID --prompt-file PROMPT.txt --wait --output-dir OUTPUT_DIR
node {baseDir}/scripts/piccc.mjs generate video --model MODEL_ID --prompt-file PROMPT.txt --wait --output-dir OUTPUT_DIR
node {baseDir}/scripts/piccc.mjs generate audio --model MODEL_ID --prompt-file SCRIPT.txt --wait --output-dir OUTPUT_DIR

node {baseDir}/scripts/piccc.mjs task get TASK_ID
node {baseDir}/scripts/piccc.mjs task wait TASK_ID --output-dir OUTPUT_DIR
node {baseDir}/scripts/piccc.mjs tasks --type image --status completed --page 1 --page-size 20
node {baseDir}/scripts/piccc.mjs auth login
node {baseDir}/scripts/piccc.mjs auth login --no-browser
node {baseDir}/scripts/piccc.mjs auth status
node {baseDir}/scripts/piccc.mjs auth logout
node {baseDir}/scripts/piccc.mjs credits
node {baseDir}/scripts/piccc.mjs --help
```

Read [references/api.md](references/api.md) when selecting generation parameters or handling task responses.

## Guardrails

- Ask for clarification only when a missing creative choice would materially change the result.
- Do not raise resolution, quality, duration, output count, audio, or web search above the economy defaults unless the user requests it or the task requires it.
- Always surface the special-offer reliability warning before creating a paid task; a script warning is only a backup.
- Never claim success before status is `completed` and at least one output URL exists.
- Never expose the API key in command arguments, prompts, logs, or project files. Let the script manage its private credentials file.
- Always use the authorization command for first-time setup; do not teach environment-variable setup unless the user explicitly requests it.
- Do not create a replacement task while checking status; task reads must not trigger new charges.
- Preserve the API response when reporting parameter, content-policy, billing, or upstream failures.
