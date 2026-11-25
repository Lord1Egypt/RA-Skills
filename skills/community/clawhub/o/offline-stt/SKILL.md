---
name: offline-stt
description: "Turns audio or video into text or subtitles offline with local speech models, and keeps a dictation dictionary accurate. Use when someone wants to transcribe a recording, make .srt subtitles, search past dictations, or fix recurring dictation mishearings."
license: MIT
compatibility: "Needs an assistant that runs commands on the person's computer (a terminal agent). Best on macOS 13 or newer with STT (stt-cli); works on macOS, Linux and Windows through whisper.cpp (whisper-cli) or faster-whisper. Chat sandboxes have no local audio models."
---

# Offline STT

Turns audio or video files into plain text or `.srt` subtitles offline on the
person's computer, and keeps a speech-to-text dictionary and dictation history
up to date. Answer in the language of the person's message, briefly.

Transcription happens only by running a local speech recognition tool on the
person's computer. If you cannot run commands here, say in one sentence that
this skill needs an assistant that runs commands on the person's computer, and
stop. Never invent, guess, or paraphrase a transcript from a file name or
context, and never claim a file was written unless you verified it exists and
is non-empty.

## Before the first job

A clear request runs at once without questions. Ask together, once, only when a
choice is genuinely missing:

1. Output: plain text in the reply, a `.txt` file beside the media, or `.srt`
   subtitles. Default: plain text in the reply for short clips (under ~3
   minutes), or `.txt` beside the source file for longer recordings.
2. Language: automatic detection, or a specific ISO code (`en`, `ru`, `uk`,
   `de`…). Default: automatic.

Never overwrite an existing file: if `Name.txt` exists, write `Name (2).txt`.

## Engines

Find the best engine installed on this computer once per conversation, in this
order:

### 1. macOS with `STT` / `stt-cli` (best)

`STT` is a free open-source macOS dictation and transcription app (MIT,
github.com/geragarazagh/stt) running Whisper and Parakeet locally via
`transcribe.cpp` with Silero VAD and iCloud-synced dictionary.

Find it in this order, using the first that exits 0 (`--help`, not `--version`:
STT 0.5-0.10 know only `--help`, and before 0.9 an unknown flag opens a second
copy of the app):

```sh
stt-cli --help
/Applications/STT.app/Contents/MacOS/STT --help
```

Below, `STT` stands for the full path that worked. If its help does not list
`--status`, this STT is older than 0.11: transcription, `--add-word` and
`--add-pair` work, the other commands below do not. Tell the person once that
STT's menu has Check for Updates (or `brew upgrade --cask stt` when installed
with Homebrew), and use what works meanwhile.

- **Check status** (active model, downloaded models, language, dictionary and
  history counts, running state):
  ```sh
  STT --status
  STT --status --json
  ```
  If `model: none`, tell the person to pick and download a model once in STT's
  Settings window, and stop.
- **Transcribe files** (uses the model, language, and dictionary set in STT):
  ```sh
  STT "INPUT.m4a"
  STT --srt "INPUT.mp4"
  ```
  Capture stdout to a `.txt` or `.srt` file when saving beside the source.
- **Maintain the dictation dictionary** (updates the running app live and syncs
  to other devices via iCloud; if STT is not running, start it in the
  background with `open -g -a STT --args --background`):
  ```sh
  STT --list-words
  STT --list-pairs
  STT --add-word "ExactName"
  STT --add-pair "misheard form" "ExactName"
  STT --remove-word "OldName"
  STT --remove-pair "old misheard form"
  ```
- **Search or read dictation history**:
  ```sh
  STT --history 20
  STT --history 50 --search "keyword" --json
  ```
- **Toggle live microphone dictation**:
  ```sh
  STT --toggle
  ```
  Requires Microphone permission for the terminal or host app running the
  command.

#### Keeping the dictionary clean

- **Words (`--add-word`)** feed Whisper's initial prompt.
  Keep personal words concise (roughly 10–30 high-frequency names or terms);
  stuffing hundreds of words dilutes Whisper's prompt. Parakeet ignores the
  word list and uses replacement pairs only.
- **Replacement pairs (`--add-pair HEARD WRITTEN`)** run after recognition on
  every model. Cyrillic heard forms automatically match Russian and Ukrainian
  case endings (adding `гитхаб → GitHub` also fixes `гитхаба`, `гитхабу`).
- Never add a heard form that is also an ordinary word in the person's language
  (for example `тему` or `сигнал`), or it will corrupt normal sentences.
- Check `--list-words` or `--list-pairs` before adding so you do not duplicate
  existing rules. When you notice a recurring unambiguous dictation slip in the
  person's messages, offer or apply the pair once; ask first if the heard form
  could be an ordinary word.

### 2. macOS without `STT`, Linux, or Windows: `whisper-cli` (`whisper.cpp`)

Check whether `whisper-cli` is installed:

```sh
whisper-cli --help
```

Look for an existing GGUF/GGML Whisper model in `~/Library/Application Support/STT/models/`,
`~/.local/share/whisper/`, or `~/.cache/whisper/`. Never download a large model
without the person's yes.

- Convert non-WAV inputs (or any format `whisper-cli` cannot decode directly)
  to 16 kHz mono WAV in a temporary folder first:
  ```sh
  ffmpeg -y -i "INPUT.m4a" -ar 16000 -ac 1 -c:a pcm_s16le "/tmp/stt_in.wav"
  ```
- Transcribe to text or `.srt` (use `-l auto` unless a language was chosen):
  ```sh
  whisper-cli -m "/path/to/ggml-large-v3-turbo.bin" -l auto -nt "/tmp/stt_in.wav"
  whisper-cli -m "/path/to/ggml-large-v3-turbo.bin" -l auto -osrt -of "OUTPUT_BASE" "/tmp/stt_in.wav"
  ```
Remove the temporary WAV after reading the output.

### 3. Python fallback: `faster-whisper`

If `whisper-cli` is absent, check for `faster-whisper` in its own virtual
environment (`~/.local/share/faster-whisper/bin/python3 -c "import faster_whisper"`).
Run a short one-off Python call that writes plain text or `.srt` to the target
path without leaving temp files behind.

## Check

- Confirm the command exited 0 and output text is non-empty (if empty, check
  with `ffprobe` that the file actually has an audio stream).
- For `.srt` files, verify valid sequential cue indices and `HH:MM:SS,mmm --> HH:MM:SS,mmm`
  timestamps.
- Report in one or two lines: output path (if saved), duration or word count,
  and engine/model used.

## Install

Name the command for the person's system and wait for a yes before installing
anything or downloading a model:

- macOS 13 or newer, Apple Silicon: `brew install geragarazagh/tap/stt` (or
  download `STT.dmg` from github.com/geragarazagh/stt/releases).
- macOS (Intel) or without STT: `brew install whisper-cpp ffmpeg`.
- Linux: install `ffmpeg` and build `whisper.cpp` (or create a venv:
  `python3 -m venv ~/.local/share/faster-whisper && ~/.local/share/faster-whisper/bin/pip install faster-whisper`).
- Windows: `winget install Gyan.FFmpeg` and `faster-whisper` in a Python venv.

## Known mistakes

- Do not pass a flag the found STT's `--help` does not list: before 0.9 an
  unknown flag launches a second copy of the app that takes the running one's
  socket.
- `--add-word`, `--add-pair`, `--remove-word`, and `--remove-pair` require the
  STT app to be running so changes sync via iCloud and reload live. If `STT is
  not running.` appears, launch `open -g -a STT --args --background`, wait 1
  second, and retry once.
- Passing an `.mp4` or `.m4a` straight to a `whisper-cli` build compiled
  without FFmpeg fails silently or prints a header error: convert to 16 kHz
  mono PCM WAV with `ffmpeg` first.
- Never retry a failing command more than twice. Report the exact error and
  what the person can do next.
