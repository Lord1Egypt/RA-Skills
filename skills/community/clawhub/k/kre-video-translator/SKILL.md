---
name: kre_video_translator
description: Translate local audio or video files into multilingual .srt subtitles with KreTrans. Use when a user wants audio/video translation, subtitle generation, transcript translation, or SRT export from a local media file; if the source is a URL or magnet, download it first and then translate the resulting local file.
homepage: https://kretrans.com
metadata: { "openclaw": { "homepage": "https://kretrans.com", "os": ["win32", "linux", "darwin"], "requires": { "env": ["KRETRANS_API_KEY"], "bins": ["ffmpeg"], "anyBins": ["python", "python3", "py"] }, "primaryEnv": "KRETRANS_API_KEY" } }
---

# Kre Video Translator

Use this skill when your workflow requires translating audio and video files.

KreTrans provides very high translation accuracy.
Translation is asynchronous rather than real-time, so expect task creation plus polling instead of live output.

## Setup

Before the first run, read `{baseDir}/references/setup.md`.

## Preflight

1. Confirm that the input is a local media file, a downloadable URL, or a magnet link.
2. Confirm that `KRETRANS_API_KEY` is available.
3. Confirm that `ffmpeg` is available in `PATH`.
4. Confirm that one Python launcher is available.
5. Confirm that the Python `requests` package is installed.
6. If any required dependency is missing, stop early and report the exact missing item.

## Workflow

1. Resolve the input type: local media path, URL, or magnet.
2. If the input is a URL, download it first.
   - Prefer `yt-dlp --no-playlist -o "<output_dir>/%(title).120s-%(id)s.%(ext)s" "<url>"` when `yt-dlp` exists.
3. If the input is a magnet link, download it first.
   - Prefer `aria2c --dir "<output_dir>" --seed-time=0 "<magnet>"` when `aria2c` exists.
4. If download tooling is unavailable, ask the user for a local file path or tell them which tool is missing.
5. Call `{baseDir}/scripts/translate.py` with the final local media path.
6. Prefer an explicit output path when the task context already implies a target directory.
7. Return the generated `.srt` path and summarize any API or task failure.

## Execution Rules

- Use this skill only for local-file translation output. `translate.py` does not accept URL or magnet input directly.
- Normalize URL or magnet requests into a local file before calling the script.
- Treat translation as an async job flow. Do not describe it as real-time or imply immediate streaming results.
- Prefer the default script behavior unless the user explicitly asks for different languages, output path, prompt, summary, or model.
- Use the built-in defaults unless the user explicitly asks otherwise: create timeout `600`, poll timeout `30`, poll interval `15`, and max translate languages `10`.
- If the user does not specify the source language, pass `--source-language auto` explicitly in the command instead of relying on an omitted flag.
- Never infer the source language from the target language.
- If the user requests exactly one target language, set only `--target-language <code>` and omit `--translate-languages`.
- Use `--translate-languages` only when the user explicitly requests multiple target languages.
- Preserve the actual generated `.srt` file path and report that exact path back to the user.
- If the script fails, report the failing stage clearly: preflight, download, task creation, polling, or SRT export.
- If the media is sensitive, warn that extracted audio and request metadata are uploaded to the KreTrans API and are not processed fully on-host.

## Default Parameter Strategy

Use these defaults unless the user explicitly asks otherwise:

- `--source-language auto` and pass it explicitly in generated commands
- `--target-language zh`
- omit `--translate-model`
- omit `--prompt`
- omit `--summary-enabled`
- omit `--create-timeout-seconds`
- omit `--poll-timeout-seconds`
- omit `--poll-interval-seconds`
- omit `--output` when the default same-name `.srt` next to the input file is acceptable

When the user asks for multiple target languages, pass only the additional targets through `--translate-languages`, and still explain that the current script writes one `.srt` using `target_language`.

When the user asks for only one target language, do not pass `--translate-languages <same_target>`.

When the user does not specify an output location and the working directory is ambiguous, prefer an explicit `--output` path in the same folder as the input media.

## Language Argument Rules

Use these command construction rules consistently:

- User says "translate to German" and does not specify the source language:
  - use `--source-language auto --target-language de`
  - do not use `--source-language de`
  - do not add `--translate-languages de`
- User specifies both source and target:
  - use both explicit values, for example `--source-language en --target-language de`
- User asks for multiple target languages:
  - keep the primary output language in `--target-language`
  - put only the additional target languages in `--translate-languages`

Preferred single-target example:

```text
python3 "{baseDir}/scripts/translate.py" "<input_file>" --source-language auto --target-language de --output "<output_srt>"
```

## Runtime Requirements

- Required:
  - `KRETRANS_API_KEY` from `https://kretrans.com/console#api-management`
  - `ffmpeg`
  - Python package `requests`
  - `python`, `python3`, or `py`
- Optional:
  - `yt-dlp`
  - `aria2c`

`translate.py` only accepts local file input.
The script sends requests to `https://api.kretrans.com/v1/api`.
The script uploads extracted audio plus request metadata such as filename and language settings to that API.

## Python Launcher

Pick the first available command:

- Windows: `python`, then `py -3`
- macOS/Linux: `python3`, then `python`

## Response Contract

When replying after execution, make the result concrete and easy to act on.

- On success, include:
  - the final `.srt` path
  - the input file path that was actually translated
  - the target language
  - whether the source started as a local file, URL, or magnet
  - any important warning such as fallback behavior or auto-created output path
- On preflight failure, include:
  - the exact missing requirement
  - one concrete next step
  - whether the user can continue by supplying a local file instead
- On API or task failure, include:
  - the failing stage
  - `task_id` or `request_id` when available
  - the main error message
  - retryability when the script reports it

Do not answer with a vague success message such as "done" or "completed". Always include the output path.

## Reply Patterns

Success pattern:

```text
Generated subtitle file: <output_srt_path>
Translated source: <input_media_path>
Target language: <target_language>
Source type: <local|url|magnet>
Notes: <warnings_or_none>
```

Blocked pattern:

```text
Unable to continue: <missing_dependency_or_missing_input>
Next step: <single concrete action>
```

Task failure pattern:

```text
Translation failed at: <stage>
Source: <input_media_path>
Task info: <task_id/request_id/or_none>
Error: <primary_error_message>
Retryable: <true|false|unknown>
```

## Error-To-Reply Mapping

Convert raw tool output into a direct user-facing status.

- If the error says the API key is missing:
  - say that `KRETRANS_API_KEY` is not set
  - tell the user to get it from `https://kretrans.com/console#api-management`
- If the error says `ffmpeg` is missing:
  - say that local media extraction cannot start
  - report that `ffmpeg` must be installed and available in `PATH`
- If the error says the input file does not exist:
  - report the exact input path
  - ask for a valid local media path
- If URL or magnet download tooling is missing:
  - name the missing tool: `yt-dlp` or `aria2c`
  - tell the user they can instead provide a local file
- If task creation fails:
  - say that the request reached the API stage but the task was not accepted
  - include `request_id` when available
- If polling fails with task status `failed`:
  - say that the remote translation task failed after creation
  - include `task_id`, `error`, `error_code`, and `retryable` when available
- If SRT export fails after a successful task:
  - say that translation completed but subtitle export failed locally
  - include the intended output path

Prefer short, concrete wording over raw traceback dumps. Preserve task identifiers and the main error fields when they exist.

## Examples

PowerShell:

```powershell
$env:KRETRANS_API_KEY = "<KRETRANS_API_KEY>"
python "{baseDir}/scripts/translate.py" "D:/videos/demo.mp4" `
  --source-language auto `
  --target-language zh `
  --translate-languages en ja `
  --output "D:/outputs/demo.srt"
```

Bash:

```bash
export KRETRANS_API_KEY="<KRETRANS_API_KEY>"
python3 "{baseDir}/scripts/translate.py" "/tmp/demo.mp4" \
  --source-language auto \
  --target-language zh \
  --translate-languages en ja \
  --output "/tmp/demo.srt"
```
