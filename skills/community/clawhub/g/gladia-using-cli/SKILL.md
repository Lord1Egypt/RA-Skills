---
name: gladia-using-cli
description: Terminal transcription of audio files and URLs with the Gladia CLI (gladia speech-to-text). Use when the user has gladia-cli installed, wants shell-based transcription, or asks an agent to transcribe audio then answer questions about the content. For audio intelligence features not available as CLI flags, use the SDK skills instead.
license: MIT
---

# Gladia CLI

The [Gladia CLI](https://github.com/gladiaio/gladia-cli/) (`gladia`) transcribes pre-recorded audio from the terminal. Local files are auto-uploaded; URLs are passed directly to the API.

> **CLI vs SDK**: use the CLI for quick terminal workflows when `gladia` is on PATH. For app integration or audio intelligence not exposed as CLI flags, see [gladia-sdk-integration](../gladia-sdk-integration/SKILL.md) and [gladia-audio-intelligence](../gladia-audio-intelligence/SKILL.md).

## When to Use

- User mentions gladia-cli, `gladia transcribe`, or wants quick terminal transcription
- Agent should transcribe a local file, a `http(s)` URL, or a YouTube URL, then answer follow-up questions about the content
- One-off transcription without writing application code

**Prerequisites:** verify `gladia --version` succeeds and an API key is configured (`GLADIA_API_KEY`, `~/.gladia`, or `--gladia-key`).

## When NOT to Use

- **Live / real-time audio** — use [gladia-live-transcription](../gladia-live-transcription/SKILL.md)
- **Building an app or CI pipeline in code** — use [gladia-sdk-integration](../gladia-sdk-integration/SKILL.md)
- **Audio intelligence not in CLI** (translation, summarization, NER, PII, audio-to-LLM) — use [gladia-audio-intelligence](../gladia-audio-intelligence/SKILL.md) with the SDK

## References

Consult these resources as needed:

- ./references/cli-vs-sdk.md -- CLI vs SDK routing: which features have CLI flags and which require SDK skills
- ../gladia-pre-recorded-transcription/SKILL.md -- SDK pre-recorded workflow and options
- ../gladia-audio-intelligence/SKILL.md -- Addons beyond CLI flags
- ../gladia-troubleshooting/SKILL.md -- API key, upload, and polling errors
- [gladia-cli repository](https://github.com/gladiaio/gladia-cli/)

## Setup

**Install** (macOS/Linux):

```bash
curl -fsSL https://github.com/gladiaio/gladia-cli/releases/latest/download/install.sh | sh
```

**Auth** — get a key at [app.gladia.io/account](https://app.gladia.io/account). Three options:

```bash
# 1. Environment variable (preferred for CI and shells)
export GLADIA_API_KEY=<API_KEY>

# 2. Persist locally
gladia auth set <API_KEY>

# 3. Pass per command (global flag, works on any command)
gladia transcribe meeting.wav --gladia-key <API_KEY>
```

**Credential order:** `GLADIA_API_KEY` → `~/.gladia` → `--gladia-key` (first match wins)

**List valid language codes:** `gladia languages`

## Commands

| Command                      | Description                                                |
| ---------------------------- | ---------------------------------------------------------- |
| `gladia transcribe <source>` | Transcribe a local file, a `http(s)` URL, or a YouTube URL |
| `gladia auth set <key>`      | Save API key to `~/.gladia`                                |
| `gladia languages`           | List supported ISO 639-1 codes                             |

## Transcribe Flags

| Flag                                | Default     | Description                                                |
| ----------------------------------- | ----------- | ---------------------------------------------------------- |
| `-o`, `--output`                    | `text`      | `text`, `json`, `json-full`, `srt`, `vtt`                  |
| `--language`                        | —           | Expected language(s), comma-separated (`en` or `en,fr,de`) |
| `--code-switching`, `--code-switch` | off         | Detect language per utterance                              |
| `--diarize`                         | off         | Speaker identification                                     |
| `--model`                           | API default | `solaria-1` or `solaria-3`                                 |
| `-v`, `--verbose`                   | off         | Show progress while polling                                |

Global: `--gladia-key` — API key override

## Agent Workflow: Transcribe Then Q&A

1. **Check CLI** — `gladia --version`; install or use SDK skills if missing
2. **Pick flags** — match output format and options to the user's question (tables below)
3. **Run** — `gladia transcribe <source> [flags]`; capture stdout
4. **Answer** — ground responses **only** in captured output; cite speakers and timestamps when available
5. **Re-run if needed** — if the question requires data not in the current output (e.g. timestamps, speakers), re-transcribe with different flags
6. **Long audio** — use `-v` for progress; for very long transcripts, redirect stdout to a temp file and read selectively

**Do not invent transcript content.** If output is empty or unclear, say so and suggest different flags or SDK skills.

## Output Format Selection

| User need                | CLI approach                                              |
| ------------------------ | --------------------------------------------------------- |
| Plain transcript         | default or `-o text`                                      |
| Who spoke when           | `--diarize -o text` or `-o json`                          |
| Timestamps per utterance | `-o json` (utterance list with `time_begin`, `time_end`)  |
| Full API payload         | `-o json-full`                                            |
| Subtitle file            | `-o srt` or `-o vtt` (add `--diarize` for speaker labels) |
| Model choice             | `--model solaria-1` or `--model solaria-3`                |

### Language behavior

You can list all the possible languages compatible with gladia with the command `gladia languages`.

| Goal                | Command                                                    |
| ------------------- | ---------------------------------------------------------- |
| Auto-detect         | `gladia transcribe <source>`                               |
| Constrain detection | `--language en,fr,de` (does **not** enable code switching) |
| Code switching      | `--code-switching` (+ optional `--language` hints)         |

## CLI vs SDK (summary)

For full CLI vs SDK routing, see [./references/cli-vs-sdk.md](./references/cli-vs-sdk.md).

| Feature                                        | CLI                              | If not in CLI                                                                          |
| ---------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------------------- |
| Basic transcription                            | `gladia transcribe`              | —                                                                                      |
| Speaker diarization                            | `--diarize`                      | [gladia-audio-intelligence](../gladia-audio-intelligence/SKILL.md) for advanced config |
| Language / code-switch                         | `--language`, `--code-switching` | SDK for advanced `language_config`                                                     |
| Translation, NER, PII, sentiment, audio-to-LLM | No                               | [gladia-audio-intelligence](../gladia-audio-intelligence/SKILL.md)                     |
| API summarization addon                        | No                               | SDK (agent may summarize `-o text` output informally)                                  |
| Live streaming                                 | No                               | [gladia-live-transcription](../gladia-live-transcription/SKILL.md)                     |

## Examples

```bash
gladia transcribe meeting.wav
gladia transcribe https://example.com/podcast.mp3 -o json
gladia transcribe https://www.youtube.com/watch?v=jNQXAC9IVRw
gladia transcribe call.wav --diarize -o srt
gladia transcribe interview.mp3 --language en,fr --code-switching -v
gladia transcribe podcast.mp3 --model solaria-1 -o json-full
gladia transcribe meeting.wav --gladia-key <API_KEY>   # inline key, no env or ~/.gladia needed
```

## Common Mistakes

- **Treating `--language en,fr` as code-switching** — it only constrains detection; add `--code-switching` separately for per-utterance language detection
- **Answering without re-running** — timestamp or speaker questions need `-o json` or `--diarize`; plain text may lack required fields
- **Inventing CLI flags** — translation, summarization, NER, and PII have no CLI flags today; route to SDK skills
- **Using SDK code when CLI is requested** — if the user has `gladia` installed and wants terminal workflow, run shell commands
- **Skipping auth check** — transcription fails without a valid API key in env, `~/.gladia`, or `--gladia-key`

For API errors and diagnostics, see [gladia-troubleshooting](../gladia-troubleshooting/SKILL.md).

## Further Reading

- [gladia-cli README](https://github.com/gladiaio/gladia-cli/)
- [Pre-recorded quickstart](https://docs.gladia.io/chapters/pre-recorded-stt/quickstart)
