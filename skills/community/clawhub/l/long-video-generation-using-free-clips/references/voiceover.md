# Voiceover and subtitles

## Choosing the voice

| Engine | Cost | Setup | Notes |
|---|---|---|---|
| `own` | free | record one file per scene into `audio/<id>.wav` (or mp3, m4a, flac) | Best for trust and originality. A single long recording can be cut per scene with FFmpeg. |
| `piper` | free, runs locally | `pip install piper-tts`, download a voice | Quality is decent, not human. Command line differs by version: run `python -m piper --help`, then set `PIPER_CMD` if needed (text goes to stdin). Check the licence of the specific voice for commercial use. Piper's own licence terms were not verified. |
| `elevenlabs` | paid, per character | `ELEVENLABS_API_KEY`, `voice.voice_id` | Most natural. Check the current plan's commercial-use and quota rules. Pause tags differ by model: newer v3-style models use audio tags, Multilingual v2 / Flash v2 / v2.5 accept `<break time="1.5s" />` up to 3 s (verified earlier in this project; recheck). Run `--dry-run` first to see the character count. |
| `silent` | free | none | Placeholder of estimated length for layout; swap in real audio later with `--force`. |

Do not present a synthetic voice as a real named person, and do not clone a real person's voice without their consent.

## Rules of thumb

- Scenes of 40 to 160 words give natural breaks; each file gets `voice.pad` seconds (default 0.4) of silence at the end, so scenes breathe.
- Spell out numbers, abbreviations and names the engine mispronounces ("S Q L", "Nguyen" as "win"); keep a pronunciation list in the notes. Text in `[square brackets]` is removed before synthesis, so use it for stage notes.
- Re-run only what changed: `voiceover.py DIR --scene s04`. Unchanged scenes are skipped via `audio_hash`; `--force` redoes all.
- Listen to the whole narration once before rendering; fixing audio later means re-rendering the affected scenes.
- Languages: choose a voice that supports the video's language. For right-to-left languages, prefer uploading the SRT over burning subtitles, and check shaping.

## Subtitles

- `subtitles.py DIR` (script mode) spreads each scene's words across its narration by word length and punctuation. It is dependency-free and usually within a fraction of a second, but it does not hear the audio.
- `subtitles.py DIR --mode whisper --model small` uses faster-whisper (`pip install faster-whisper`, CPU, int8) for real word timings. The text is what Whisper heard; proofread names and numbers. Models above `small` need more RAM and time; the first run downloads the model.
- Output is `out/subtitles.srt`. Upload it as captions (better for accessibility and search than burned text), or pass `--burn-subs` to `build_video.py` for hard-coded captions.
