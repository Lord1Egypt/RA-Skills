# Runtime And Recovery

Use Python 3.10+, network access, `requests`, and FFmpeg. The CLI checks for missing tools and waits for explicit user approval before installing them with the current interpreter or an available package manager. `yt-dlp` is checked only for URL input.

The production API is fixed at `https://kretrans.com/api`. Credential setup and language-specific URLs are defined in [SKILL.md](../SKILL.md).

## Credential Files

Lookup order:

1. `KRE_VIDEO_TRANSLATOR_API_KEY`
2. `KRETRANS_API_KEY`
3. `KRE_VIDEO_TRANSLATOR_API_KEY_FILE` or `KRETRANS_API_KEY_FILE`
4. macOS/Linux: `$XDG_CONFIG_HOME/kre-video-translator/api_key` or `~/.config/kre-video-translator/api_key`
5. Windows: `%APPDATA%/KreVideoTranslator/api_key`

`auth launch` verifies a pasted Key before atomically saving it. The terminal receipt contains status and file metadata and excludes secret content. Secure automation may use `save-key --stdin` with an existing protected input stream. If `requests` is missing, ask before rerunning the account command with `--allow-install-tools`.

## FFmpeg

Media submission uses mono MP3 at 64 kbps, 44.1 kHz. Video export requires the `subtitles` filter, which is provided by an FFmpeg build compiled with libass. macOS can use Homebrew `ffmpeg-full`; Linux and Windows should use a distribution build that reports `subtitles` in `ffmpeg -filters`. Ask before installing or switching the FFmpeg build.

An unavailable filter produces a recoverable export result while the reviewed SRT remains available. Re-run video export after installing a compatible build. The installed executable must report `subtitles` in `ffmpeg -filters`; a plain FFmpeg installation is not sufficient on some platforms:

```bash
ffmpeg -hide_banner -filters
```

## Task Recovery

Use `status` for one query and `resume --task-id TASK_ID` for asynchronous waiting. The CLI keeps a 20-second polling floor, exponential backoff, and server-provided `Retry-After` handling. Reuse the saved task and idempotency IDs after an interrupted client.

## API Errors

Use `KRE_VIDEO_TRANSLATOR_ERROR_JSON.next_action` when present. `ask_user_to_approve_tool_install` means ask before installing the named tool, then rerun the same command with `--allow-install-tools` after approval. `check_skill_update_then_retry_once` means verify the installed Skill version, update it from ClawHub if available, and retry once. `user_check_balance` means stop retrying and direct the user to the localized account packages page. HTTP 429 remains a rate-limit response and follows `Retry-After`.
