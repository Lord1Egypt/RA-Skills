# Orchestrator Quick Start

How to drive `scripts/analysis_orchestrator.py` for every input type
(audio file, two-song pair), what extraction actually improves the
output, and the per-song output layout. Load this before running any
analysis script.

> **Before running multi-output MiniMax generations,** load
> [`minimax-generation-caveats.md`](minimax-generation-caveats.md) for
> sequential-run rules, output-file verification, and duration caveats.

For any input combination, the `analysis_orchestrator.py` script is the single entry point:

```bash
# Audio file
python3 scripts/analysis_orchestrator.py --audio /tmp/song.wav

# Two songs (mashup) - gets BPM + key compatibility scoring for free
python3 scripts/analysis_orchestrator.py --audio /tmp/song_a.wav --audio /tmp/song_b.wav

# Demucs source separation — for TIMBRE/PITCH analysis of an isolated vocal, NOT for lyrics
python3 scripts/analysis_orchestrator.py --audio /tmp/song.wav --use-demucs

# Arranger triage after source separation
python3 scripts/extract_stems.py /tmp/song.wav --out-dir /tmp/stems/song
python3 scripts/per_stem_analysis.py /tmp/stems/song/stems.json --output /tmp/stems/song/per_stem_report.json

# Whisper lyrics extraction — run on the FULL mix (do NOT pre-separate with Demucs)
python3 scripts/analysis_orchestrator.py --audio /tmp/song.wav --lyrics
```

The orchestrator dispatches to the right analysis scripts and produces a unified JSON. Optional audio-analysis packages (CLAP, autochord, allin1, pyloudnorm, demucs, beat_this, basic-pitch, transformers/MERT) are detected at runtime and used when available.

> **v1.5.0:** the orchestrator is audio-only. URL download flags (`--youtube`), image flags (`--image`, `--vlm`, `--ocr`, `--faces`), and the LRCLib web-lyrics path (`--lyrics-source web|auto`) are gone. To analyze a track from a URL, fetch it locally with the private `music-source-fetch` skill first, then pass the local path.

## Extraction guidance (what actually improves the output)

These are the rules that make the extracted data useful to the downstream generator. They are tool-agnostic — they apply whether the backend is MiniMax cloud or a local model.

- **Lyrics: transcribe the FULL mix, do not Demucs-first.** Feeding Demucs-isolated vocals into Whisper measurably *worsens* transcription word-error-rate in most configurations. Run the transcriber on the original mix. Use **faster-whisper** over vanilla whisper (same accuracy, much lower latency/VRAM), and prefer the **`large-v2`** model for *sung* lyrics — `large-v3` is reliably worse on singing. Use `medium`/`base` only as a speed compromise.
- **Use Demucs only for timbre/pitch.** Source separation helps when you want clean vocal-stem features (breathiness, pitch range, vocal brightness) or per-instrument detection — never as a lyrics pre-step.
- **Prioritise the high-value features.** For driving a generation prompt, the features that matter most (in order) are **tempo/BPM, key/scale, beats/downbeats, chords, then structure (section boundaries)**. Energy/RMS and spectral centroid map to texture words (punchy, airy, sparse, dense) and to dynamic tags. Spend analysis budget there first.
- **Give key detection a long window.** Estimate key/chroma over ~120s of audio (not a short clip) for a stable result; BPM is stable from ~60s.
- **Carry confidence through to the prompt.** Hedge `low`/`medium` detections ("around 128 BPM", "likely D minor") and never inject `missing` values as facts — see the **Analysis Quality** section in SKILL.md.
- **Map structure boundaries to actions.** Detected section boundaries become the `[Verse]/[Chorus]/[Bridge]` tag roadmap, and (for backends that support it) the repaint windows for fixing one bad section instead of regenerating the whole track.

## Output file layout (per-song subfolders)

Every generation should be saved into a per-song subfolder that bundles the audio with its analysis, prompt, and lyrics. The LLM should ask the user for the project root and song slug up front (default: `~/Music mix/<project>/<song-slug>/`), then run the full chain of commands below.

```bash
# Example: demo project - Two Paths, two versions

# 1. Make the subfolder
mkdir -p ~/Music\ mix/demo-project/two-paths

# 2. Run the analysis and save JSON into the subfolder
python3 scripts/analysis_orchestrator.py \
  --audio /tmp/two_paths.wav \
  --use-demucs --lyrics \
  --output ~/Music\ mix/demo-project/two-paths/two_paths_analysis.json

# 3. Build the prompt from the analysis, save it next to the JSON
python3 scripts/emotion_to_prompt.py \
  --emotion ~/Music\ mix/demo-project/two-paths/two_paths_analysis.json \
  --output ~/Music\ mix/demo-project/two-paths/two_paths_synthwave_prompt.txt

# 4. Generate each version using the safe wrapper; verify output exists
#    before the next run (sequential only — see minimax-generation-caveats.md)
python3 scripts/generate_with_retry.py \
  --output-path ~/Music\ mix/demo-project/two-paths/M1_two_paths_synthwave.mp3 \
  -- music generate \
  --prompt "$(cat ~/Music\ mix/demo-project/two-paths/two_paths_synthwave_prompt.txt)" \
  --lyrics-file ~/Music\ mix/demo-project/two-paths/two_paths_lyrics.txt \
  --model music-2.6 \
  --out ~/Music\ mix/demo-project/two-paths/M1_two_paths_synthwave.mp3

test -f ~/Music\ mix/demo-project/two-paths/M1_two_paths_synthwave.mp3 || {
  echo "ERROR: output not found"
  exit 1
}

# Sequential cover batches use batch_cover.py; inspect commands first.
python3 scripts/batch_cover.py \
  --audio-file /tmp/two_paths.wav \
  --prompts ~/Music\ mix/demo-project/two-paths/cover_prompts.json \
  --out-dir ~/Music\ mix/demo-project/two-paths/covers \
  --expected-duration-seconds 180 \
  --dry-run
```

The result is a self-contained song folder that the user can review, archive, share, or re-generate from without losing any context.
