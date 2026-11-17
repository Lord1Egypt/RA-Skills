# 🎬 Movie Subtitler

**Point it at any video and get it back with English subtitles.** A URL or a local file, one
command, no cloud and no API keys.

It pulls the video with `yt-dlp` (or takes a file you already have), transcribes and translates
it with [WhisperX](https://github.com/m-bain/whisperX), and puts the subtitles back in with
`ffmpeg`. Everything runs on your own machine, so nothing gets uploaded anywhere.

Ships as an [OpenClaw](https://openclaw.ai) skill, but `subtitle.sh` is plain bash and works
standalone.

## ✨ What you get

- 📼 **Any source**: a YouTube link, anything else yt-dlp handles, or a local file
- 🌍 **Translation to English** from any language Whisper knows, or keep the original with `--no-translate`
- 🎞️ **A subtitled video** plus a matching `.srt` sidecar, named so VLC pairs them automatically
- ⚡ **Soft-mux by default**, which is fast and lossless; `--burn` bakes subtitles into the pixels
- 🔒 **Fully local**: no account, no API key, no upload

## 📦 Install

```bash
git clone https://github.com/NelsonScott/movie-subtitler
cd movie-subtitler
chmod +x subtitle.sh
```

Or as an OpenClaw skill:

```bash
openclaw skills install @nelsonscott/movie-subtitler
```

You also need `ffmpeg`, `whisperx`, and `yt-dlp` (URLs only). See
[Prerequisites in SKILL.md](SKILL.md#prerequisites) for per-OS install commands, plus the
`WHISPERX_BIN` / `YTDLP_BIN` / `FFMPEG_BIN` overrides if they are not on your `PATH`.

## 🚀 Use

```bash
# a URL, Turkish source
./subtitle.sh --input "https://www.youtube.com/watch?v=..." --lang tr

# a local file, Japanese source, subtitles burned into the picture
./subtitle.sh --input ~/Videos/film.mkv --lang ja --burn
```

Always pass `--lang` with the source language code. Output lands in the current directory
(`-o/--outdir` to change that) as `<name>.subbed.mp4` and `<name>.subbed.eng.srt`.

## 🖥️ GPU optional

The script looks for `nvidia-smi`. With an NVIDIA GPU it uses WhisperX's CUDA default
(float16); without one, Apple silicon included, it falls back to CPU at `float32`. CPU works
fine, it just takes roughly a third to a half of the video's runtime, so a two hour film is
about 30 to 60 minutes. Run it in the background.

## ⚠️ Known limitations

- **No speaker labels.** Diarization (`whisperx --diarize` with pyannote) was implemented and
  tested, then removed because it did not hold up: in translate mode Whisper emits 20-30 second
  mega-cues, so a single `[SPEAKER_01]` tag lands on an entire multi-person exchange, and the
  clusterer over-split a two-actor scene into several speakers once music and shouting entered
  the mix. [SKILL.md](SKILL.md) documents the design that would actually work if you want to
  pick it up: transcribe in the original language with alignment first, then translate cue by
  cue.
- **English is the only translation target.** Whisper translates into English, not between
  arbitrary language pairs.
- **Timestamps are ~1s accurate when translating.** WhisperX cannot align translated English to
  foreign audio, so the script skips alignment in that mode. Fine for subtitles.

## 📄 License

MIT
