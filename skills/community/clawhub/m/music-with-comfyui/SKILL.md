---
name: music-with-comfyui
description: 'Use to generate music and audio through a user-defined ComfyUI server (COMFYUI_URL env var or comfyui_url in config.json; if no server is reachable the script exits with configuration instructions) — trigger with requests like "make me a song", "make up a song", "compose", "write a song", "compose a track", "arrange a song", "编一个歌", "写歌", "作曲", "编个曲", "做首歌", or any similar instruction to write/compose/arrange a song or melody (in any language). **Important disambiguation: in Chinese, "写歌" / "写一个歌" / "来个歌" here means *generate an actual audio song through ComfyUI* (AceStep 1.5 → MP3), NOT merely writing lyrics text.** If you only want lyrics written down (words, no audio), that is plain text writing and NOT this skill. Not for simple audio file conversion, volume adjustment, or transcribing/normalizing an existing audio file (that is plain audio processing, not generation). The model is **AceStep Audio 1.5** — it turns a music-description (style/genre tags) plus optional lyrics into a generated MP3. You may specify any of theme, music length, style, lyrics — one or more; if the user gives an image, the style and/or lyrics can be derived from it. **Destructive cleanup disclosure:** after the local save succeeds the script **deletes the server-side copy of the generated audio** (`POST /purge_after_retrieval`) unless the user opts out with `--keep` / `COMFYUI_PURGE=0`; this removes remote files but only the generated audio of this run (AceStep 1.5 has no image input, so nothing the user uploaded is stored on the server). The agent should tell the user before running that the server-side copy is removed, and honor `--keep` if the user wants to retain it. This deletes only the server-side copy of the generated audio for this run; AceStep music runs upload no input materials, so there is nothing the user uploaded on the server to remove, and nothing else is touched.'

version: "0.4.14"
license: BSD-3-Clause
compatibility: 'ComfyUI with the AceStep 1.5 audio nodes installed (server >= 0.38 needed for the optional retrieve-then-purge plugin); requires python3; the endpoint is user-defined (COMFYUI_URL or config.json) — point it at a server you control and trust.'
allowed-tools: Read, Write, Edit, Exec
declared-permissions: |
  This skill is a self-contained ComfyUI HTTP client for music/audio generation.
  The script declares the host capabilities it actually uses, and the agent never
  needs anything beyond the declared allowed-tools (Read, Write, Edit, Exec):
  - env   — reads COMFYUI_URL / COMFYUI_APIKEY / COMFYUI_OUTPUT_DIR / COMFYUI_TIMEOUT /
            COMFYUI_POLL_INTERVAL / COMFYUI_PURGE / COMFYUI_KEEP_MODELS_RESIDENT from the
            environment. These are the skill's own user-facing config overrides (documented
            in the module header and SKILL.md), not a privilege escalation. The API key is
            read into an Authorization header for the configured endpoint only; it is never
            printed, logged, or sent anywhere but that endpoint.
  - network — makes HTTPS/HTTP requests to the ONE configured ComfyUI endpoint only
            (GET /queue, /history, /object_info, /view, POST /prompt, /history, /purge_after_
            retrieval). No image is ever uploaded; no outbound fetch of arbitrary hosts, no
            code execution from remote payloads. Remote hosts print a data-flow warning on
            every run.
  - filesystem — writes generated audio under the configured output_dir only (default
            media/comfyui/music); reads config.json and the bundled workflow JSON. It never
            writes outside output_dir and never reads credential/secret files.
  - No persistence: the skill does not install cron jobs, startup scripts, or state hooks.
    The purge_remote step deletes the current run's own server-side audio copy after a local
    save succeeds; it is scoped to this run and cannot touch unrelated files.
metadata:
  openclaw:
    emoji: "🎵"
    requires:
      anyBins: ["python3"]
    config:
      path: "config.json"
    primaryEnv: COMFYUI_APIKEY
    envVars:
      - name: COMFYUI_APIKEY
        required: false
        description: >-
          ComfyUI API key. Sent only as an Authorization header to the configured
          endpoint (COMFYUI_URL / config.json comfyui_url). Empty/absent = no
          Authorization header is added; the key is never printed, logged, or
          sent anywhere but that endpoint.
      - name: COMFYUI_URL
        required: false
        description: ComfyUI server URL. Falls back to config.json comfyui_url when unset.
      - name: COMFYUI_TIMEOUT
        required: false
        description: Global generation timeout in seconds. Overrides config.json timeout_seconds.
      - name: COMFYUI_POLL_INTERVAL
        required: false
        description: Seconds between polling the server for generation status. Overrides config.json poll_interval_seconds.
      - name: COMFYUI_OUTPUT_DIR
        required: false
        description: Client-side output directory override. Overrides config.json output_dir.
      - name: COMFYUI_KEEP_MODELS_RESIDENT
        required: false
        description: >-
          "1/true/yes/on" keeps models resident between runs instead of releasing
          VRAM. Overrides config.json keep_models_resident (default: false).
      - name: COMFYUI_PURGE
        required: false
        description: >-
          "0" disables purge-after-retrieval globally. config.json purge_remote governs by default.
---

# Music with ComfyUI

Call a user-defined ComfyUI server (local or remote) to generate **music / audio** with **AceStep Audio 1.5** (text + optional lyrics → MP3). The user may specify any of **theme, music length, style, and lyrics** (one or more). If no style or lyrics are given explicitly, the agent derives them from the user's request — and from any image the user provides (see [Image → Music](#image--music-deriving-style-and-lyrics)).

- **T2M (Text → Music)** → **AceStep Audio 1.5** (the only model here). A music description (style/genre tags) plus optional lyrics → an MP3.

The workflow expects several model files on the server (see [Models](#models-and-custom-nodes) and [`MODEL_URL.txt`](MODEL_URL.txt)):

- Diffusion model: `acestep_v1.5_xl_turbo_bf16.safetensors`
- CLIP (dual): `qwen_0.6b_ace15.safetensors` + `qwen_4b_ace15.safetensors`
- VAE: `ace_1.5_vae.safetensors`

`config.json` at the skill root holds every default; any value can be overridden by an env var (see the Data & Privacy table there).

## Image → Music — Deriving Style and Lyrics

The **agent** reads the image; the workflow reads **only text**. AceStep 1.5's
graph has no image input — the sole text node is `TextEncodeAceStepAudio1.5`
(tags + lyrics). When the user sends an image and does **not** also specify a
full style prompt and/or lyrics, let the **agent** derive the tags and lyrics,
then hand only that text to the script:

- Use the image to infer a suitable **style / mood / genre** for `--tags` (and, if the song has words, draft **lyrics** in the right `--language`).
- Pass the user's theme/genre on top of what the image implies; never fabricate constraints the user didn't ask for.
- **No image is ever uploaded.** The reference image is used for **vibe extraction only** — it is never uploaded to, or sent to, any external destination.

If the user *does* give explicit style and/or lyrics, honour those first and use the image only as a mood reference.

When to use this section:
- Image arrives → follow the rules in [references/image-first.md](references/image-first.md)
- User explicitly asks for a style/genre, or writes lyrics → use them verbatim (cleaned up as needed)

## When to Use (Recognizing the Request)

This skill fires whenever the user asks to **write, compose, arrange, or make a song / melody / music track**, in any language — even if no genre or length is given. Common trigger phrases include, but are not limited to:

- **English:** "make me a song", "make up a song", "compose", "compose a song/track", "write a song", "arrange a song", "write some music", "make a melody", "produce a track", "write me a tune"
- **中文:** "写歌", "作曲", "编一首歌", "编一个歌", "编个曲", "编曲", "做首歌", "帮写首歌", "生成一首歌", "来首原创"
- **其他语言:** Japanese (曲を作る、歌を歌う、作曲する), Korean (곡 만들기, 작곡), Spanish (hacer una canción, componer, escribir una canción), etc.

The signal is the *intent to create new music* (write / compose / arrange / make / generate a song/melody/track). Match it loosely across languages; if the intent is clearly "create a new song", use this skill.

- Generate music from a description / theme → **music** (`--tags`)
- The user sends an image, then asks for a song (within reason) → **image-first mode**, see [references/image-first.md](references/image-first.md)

### When NOT to use this skill

This skill is for **generation**, not post-processing of existing audio. Do **not** use it (and do not look here) for:

- Converting / transcribing / resampling / normalizing an audio file the user already has (that is plain audio processing — use an audio tool).
- Adjusting volume, trimming, splicing, or remixing an existing file.
- Adding lyrics/subtitles to a pre-existing recording (unless the user wants a *new* song sung).

## Data & Privacy (read before running)

- **What is transmitted:** the music tags/lyrics and the workflow JSON go to the configured endpoint for **every** run. No image is ever sent — AceStep 1.5 has no image input; if the user provides one, the agent visual-reads it and turns it into tags/lyrics before calling the script.
- **Endpoint** is user-defined (`COMFYUI_URL` env var > `comfyui_url` in `config.json`; bundled default `http://localhost:8188`). A non-local host prints a data-flow warning on every run; if no server answers, the script exits with configuration instructions instead of a raw timeout. When `comfyui_api_key` is set, the Bearer key is only honored if the server runs an auth custom node that recognizes it — the reference implementation is [`sunshinejnjn/comfyui-auth`](https://github.com/sunshinejnjn/comfyui-auth) (setup in the image-with-comfyui README's *ComfyUI API Key* section).
- **Written to disk (sendable by default):** generated audio is saved under the **OpenClaw media directory** so it can be attached directly: `output_dir` (config default `media/comfyui`) + `music/` subdir, resolved against the OpenClaw workspace — e.g. `<workspace>/media/comfyui/music/`, or `~/.openclaw/media/comfyui/music/` on a headless run — a path `MEDIA:` accepts as-is. Override with `COMFYUI_OUTPUT_DIR` / `--output-dir`. **After the local save succeeds the script deletes the server-side copy** (`POST /purge_after_retrieval`; see Error Handling #4) unless `--keep` / `purge_remote: false` / `COMFYUI_PURGE=0`. Don't submit sensitive content if the endpoint is a concern.
- **Secrets:** never put credentials in the URL or logs. The script routes every request through a redirect-safe opener so the key is never sent to any host other than the configured endpoint, even if that endpoint issues a cross-origin redirect.

## Workflow Files

| Mode | Workflow | File |
|---|---|---|
| Music (AceStep 1.5) | AceStep Audio 1.5 (text/lyrics → audio) | `workflows/acestep_audio_api.json` |

The workflow is an **adapted** version of a real ComfyUI graph. Original source + exactly what was changed → [references/attribution.md](references/attribution.md).

## CLI Usage

> **⚠️ The music description is MANDATORY and must be passed via `--tags` (or `--prompt`) — never as a positional word.**
>
> `python3 music_with_comfyui.py music "lo-fi track"` → `music: error: the following arguments are required: --tags`
>
> Always write the description through `--tags "..."` on the **first** attempt. A positional word wastes a whole turn before the command ever reaches ComfyUI.
>
> **⚠️ `--tags` and `--lyrics` take the TEXT ITSELF — never a file path.**
>
> The script sends the strings verbatim to the model and **never opens files**. `--lyrics /tmp/lyrics.txt` does not read the file — the path string becomes the "lyrics" the model sings. Write the tags and the full lyric text **inline in the argument**, every time.

Full commands and the timeout table → [README.md](README.md) *CLI Reference*

### What each knob controls

- **`--tags`** *(required)* — the music description: genre, tempo, instrumentation, mood, vocal style. This is the primary prompt. ComfyUI-escaped (line breaks as `\t`/`\n`); keep it clean.
- **`--lyrics`** *(optional)* — structured Sonic-lyrics text, **passed inline** (the script sends the string verbatim and never reads a file — a file path here would be sung as lyrics). Omit (or pass empty) for an instrumental; AceStep 1.5 generates instrumental audio.
- **`--duration`** *(optional)* — seconds (default: config `default_duration`, 120). The audio latent's `seconds` is set to match, so keep them consistent.
- **`--seed`** *(optional)* — **not sent by default.** If omitted, the script uses no seed (random per run). Pass `--seed <n>` only to lock/reproduce a specific output.
- **Style/tuning flags** (`--bpm`, `--keyscale`, `--language`, `--timesignature`, `--cfg-scale`, `--temperature`, `--top-p`, `--top-k`, `--min-p`) — optional overrides of the defaults in `config.json` `music.default_params`; each omits cleanly if unset. `--language` must be one of the 51 codes in [references/cli-reference.md](references/cli-reference.md) *Language codes* (e.g. `en`, `zh`, `ja`, `ko`, `yue`) — the lyrics must be in the same language.
- **`--tags-image`** *(removed)* — AceStep 1.5 takes no image. If the user gives a reference image, the agent reads it and derives tags/lyrics itself (see [Image → Music](#image--music-deriving-style-and-lyrics)).
- **`--keep`** — retain the server-side copy of the generated audio. Without it, the script auto-deletes it on the server after the local save succeeds — this needs the server to run the [purge_after_retrieval plugin](https://github.com/sunshinejnjn/comfyui-purge-after-retrieval); if the server doesn't have it, see Error Handling #4 (3 install hints, then defaults to keep).
- **`--output-dir`** — output directory override (the default already lands in the sendable OpenClaw media directory; the audio codec is whatever the server's `SaveAudioAdvanced` writes).

## Prompt / Tags Formatting

Key points:

- Write **`--tags`** as a comma/space-separated description of **genre, tempo, instrumentation, mood, and vocal style**. Keep it clean and natural.
- ComfyUI-escape any line breaks in the description: `\\t` (tab) / `\\n` (newline). If you write the tags through `--tags "..."` the script passes the string through, so keep line breaks to a minimum or escape them.
- **Lyrics**, if any, should be structured (sections like `[Verse 1]`, `[Chorus]`, ...). Keep to the language set via `--language`.
- If the agent picks the style itself, it should still produce a concise, coherent tag line — not a wall of contradictory keywords.

## Error Handling

The script auto-detects the same categories as the image skill and reports them with install/source guidance:

1. **Missing nodes** — reports which node, its package, and a pinned GitHub install hint (the script never runs `git clone` itself).
2. **Missing models** — reports the missing model file(s); the AceStep workflow has no blind model substitution (there is only one model), so it aborts with the install hint instead of degrading.
3. **Non-critical utility nodes** (e.g. `UnloadAllModels`) — bypassed automatically without interrupting generation.
5. **Post-retrieval purge failure (取回后删除失败)** — after the local save succeeds the script asks the server to delete its copy of the generated audio (`POST /purge_after_retrieval`; AceStep 1.5 has no image input, so there are no uploaded inputs to clean up). If that fails (the server usually just lacks the plugin), generation is unaffected — the file is already local. The script then shows an install hint for the [comfyui-purge-after-retrieval](https://github.com/sunshinejnjn/comfyui-purge-after-retrieval) plugin (server-side `git clone` into `custom_nodes/` + restart), **at most 3 times** (the count is tracked in `config.json` → `purge_fail_hints`). After the 3rd hint it stops trying and defaults to `--keep` behavior (server-side file retained); to re-arm, set `purge_fail_hints` back to `0` in `config.json` (a successful purge resets it automatically). Disable entirely: `--keep` per run, or `purge_remote: false` / `COMFYUI_PURGE=0`.
6. **No output audio** — if the run completes but no audio entry is found, the script reports it (the `SaveAudioAdvanced` node may be missing on that server, or audio is stored under a different output key). Do not claim success.

## Output Delivery

**Send the generated file — do not just describe it.** Deliver in the **user's original session**, never raw paths/URLs. Per-channel prefixes, the staging/cleanup routine, and the mandatory pre-send ffprobe check are all in the bullets below.

- Generated audio is saved in the **OpenClaw media directory** by default (`<workspace>/media/comfyui/music/`, prefix `amusic_<timestamp>`, e.g. `amusic_20261006_153000.mp3`) — a path `MEDIA:` sends directly; **no staging copy to an outbound dir is needed**.
- **Attach the file** — put `MEDIA: <absolute path>` on its own line in the reply (or the message tool's media field) in the user's session. Do not send the raw file path to the group unless asked.
- **Pre-send ffprobe check (mandatory).** Before every audio send, run `ffprobe -v error -show_entries stream=codec_name,sample_rate -of csv=p=0 <file>` and confirm the file exists with an **AAC / 44100 kHz** stream. A missing file or wrong codec means **do not send** — re-transcode or regenerate.
- **Telegram gotchas.** `MEDIA:` must be the **sole content of the message** — no text before it, no `[[reply_to_current]]` — otherwise Telegram splits text + file and the file often fails to land. Use **pure ASCII** filenames in `~/.openclaw/media/outbound/`; non-ASCII names reliably fail the Telegram upload. Do **not** use the `message` tool's `sendDocument` / upload path for Telegram (returns `Network request ... failed!`). If a previous attempt failed, re-check the file exists + ASCII name, then send once more.
- **WhatsApp → transcode to 44.1kHz. Always.** AceStep 1.5 writes 48 kHz MP3, which does not play on WhatsApp. Before delivering on WhatsApp, transcode to 44.1 kHz with ffmpeg first:
  `ffmpeg -y -i <src> -c:a aac -b:a 128k -ar 44100 -ac 1 -movflags +faststart <out>.m4a`
  then send the `.m4a` via `MEDIA:` as a plain line. (mp3 also works if 44.1 kHz; 44.1 kHz is the key.)
- **Explicit original-request:** if the user asks for the original/unmodified file, do NOT transcode. Instead package the original audio as a `.zip` (e.g. `zip -j out/<name>.zip <src>.mp3`) and send the zip as a document attachment (`MEDIA:<path>.zip`, or `message(action="send", channel=..., asDocument=true, media=<path>.zip)`).
- Never send raw local file paths, ComfyUI URLs, or host info unless asked.

### Delivering the Result — Title + Lyrics

A generated song is not just an audio clip: hand it over as a complete package, and do it all in one message.

- **Song title.** If the user did not request a specific title, give the song one. Derive it from the track's mood, the `--tags`, and the lyrics — keep it short and evocative. State it clearly as the song's name.
- **Lyrics.** If the song has lyrics, return them to the user, **cleanly formatted** (each section on its own line, section headers such as `[Verse]` / `[Chorus]` intact, no stray control characters or unescaped line breaks).
- **The audio file**, attached in the user's session.

Deliver all three together — title, lyrics, and audio — not in separate hand-offs:

```
🎵  **<Song Title>**
<style note — one line>

[Verse 1]
...

[Chorus]
...

MEDIA:/…/amusic_<timestamp>.mp3
```

Never omit the title or the lyrics: a finished song should arrive with its name and, when it has words, its lyrics, in the same message as the audio. If the user supplied a title, use theirs; if the song is instrumental, skip the lyrics but still give it a title.

## Execution Discipline — One-Call Rule

The whole job is **ONE script call**: derive the tags (and lyrics, if the song has words) directly from the user's request, run the command, then deliver what it prints. GPU sampling is bounded by `timeout_seconds` in config — any extra latency is almost always **agent-side overhead**: tool calls before the audio exists.

**The allowed sequence (3 steps, at most 2 tool calls):**
1. Read `SKILL.md` **once** (first use only — the flags, language codes and defaults are all in this file).
2. Run `python3 music_with_comfyui.py music --tags "..." [--lyrics "..."] [...]` — this single call does **everything**: loads config, auto-detects missing nodes/models (with install hints), checks the endpoint, queues, polls, saves locally, purges the server copy.
3. Reply with title + lyrics + the `MEDIA:` line using the absolute path the script printed. Done.

**Never pre-check, probe, or re-verify — the script already does all of it internally:**
- ❌ Do NOT run the `test` subcommand before generating. It only adds a round-trip; the `music` call hits the same endpoint and reports the same failure, plus the actual result.
- ❌ Do NOT curl `/object_info` or otherwise inspect the server for node/model/language options — the script fetches node specs itself, auto-bypasses missing utility nodes, and prints the install hint for a missing node/model.
- ❌ Do NOT read `config.json` or `workflows/*.json` to "confirm" defaults — the script loads them at call time.
- ❌ Do NOT probe the endpoint with `curl` before the call (if you ever must, the key is sent as `Authorization: Bearer` — but don't; just run the script).
- ❌ Do NOT verify the output after the `✅` line (no `ls` / `stat` / `ffprobe` / playback checks) — the script confirmed the file exists locally and printed its path. Re-check only if the user explicitly asks about duration/format.
- ✅ If a run **fails**, read the error the script printed — it already names the missing node/model or endpoint problem. Act on that message; don't restart diagnosis from scratch.

**Repeat request** (same style, "another one", 再来一首): skip step 1 entirely — the defaults are baked in, go straight to the call.

## References

- [references/image-first.md](references/image-first.md) — image-then-music rules (vibe→tags/lyrics)
- [references/attribution.md](references/attribution.md) — original source + modifications per workflow
- [references/cli-reference.md](references/cli-reference.md) — 51 language-codes lookup
