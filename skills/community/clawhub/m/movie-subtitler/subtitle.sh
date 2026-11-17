#!/bin/bash
# subtitle.sh — foreign-language video → English-subtitled video, fully local.
# Pipeline: yt-dlp (if URL) → WhisperX transcribe+translate → ffmpeg remux (or burn-in).
#
# Usage:
#   ./subtitle.sh --input <url-or-file> --lang <code> [options]
#
#   --input     YouTube/any yt-dlp URL, or a local video file
#   --lang      source language code (tr, pt, es, ja, fr, ...). Required — don't rely on autodetect.
#   -o, --outdir  where the final file lands            (default: current directory)
#   --workdir   scratch dir for intermediates         (default: mktemp under /tmp)
#   --model     whisper model                          (default: large-v2; use small for speed)
#   --burn      re-encode with subtitles burned into the pixels (slow; default is soft-mux, fast)
#   --no-translate   keep subtitles in the original language instead of English
#   --name      basename for output files              (default: derived from video title/filename)
#
# NOTE — no diarization on purpose. Tried 2026-07-05 (whisperx --diarize + pyannote): in
# translate mode Whisper emits 20-30s mega-cues, so one speaker label lands on whole
# multi-person exchanges, and the clusterer over-split 2 actors into 3+ SPEAKER_NN ids.
# Verdict: not useful as a bolt-on. Doing it right = transcribe in the ORIGINAL language
# with alignment (short cues, per-word speakers), then LLM-translate each cue keeping
# timing/labels (LLM can also infer real character names). See SKILL.md "Future".
set -euo pipefail

# --- Resolve required binaries ----------------------------------------------
# Each can be overridden with an env var (e.g. if it's not on PATH, or you want a
# specific venv/conda install); otherwise falls back to a PATH lookup via `command -v`.
resolve_bin() {
  local env_name="$1" cmd_name="$2" label="$3"
  local override="${!env_name:-}"
  if [[ -n "$override" ]]; then
    if [[ -x "$override" ]] || command -v "$override" >/dev/null 2>&1; then
      echo "$override"
      return 0
    fi
    echo "[movie-subtitler] \$$env_name is set to '$override' but it's not executable/found." >&2
    exit 1
  fi
  if command -v "$cmd_name" >/dev/null 2>&1; then
    command -v "$cmd_name"
    return 0
  fi
  echo "[movie-subtitler] $label not found on PATH. Install it, or point \$$env_name at its full path." >&2
  exit 1
}

WHISPERX=$(resolve_bin WHISPERX_BIN whisperx "whisperx")
YTDLP=$(resolve_bin YTDLP_BIN yt-dlp "yt-dlp")
FFMPEG=$(resolve_bin FFMPEG_BIN ffmpeg "ffmpeg")

INPUT="" LANG_CODE="" OUTDIR="$(pwd)" WORKDIR="" MODEL="large-v2"
BURN=0 TRANSLATE=1 NAME=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input)   INPUT="$2"; shift 2;;
    --lang)    LANG_CODE="$2"; shift 2;;
    -o|--outdir)  OUTDIR="$2"; shift 2;;
    --workdir) WORKDIR="$2"; shift 2;;
    --model)   MODEL="$2"; shift 2;;
    --burn)    BURN=1; shift;;
    --no-translate) TRANSLATE=0; shift;;
    --name)    NAME="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[[ -n "$INPUT" && -n "$LANG_CODE" ]] || { echo "need --input and --lang" >&2; exit 2; }

[[ -n "$WORKDIR" ]] || WORKDIR=$(mktemp -d /tmp/movie-subtitler.XXXXXX)
mkdir -p "$WORKDIR" "$OUTDIR"
echo "[movie-subtitler] workdir: $WORKDIR"

# --- Step 1: get the video -------------------------------------------------
if [[ -f "$INPUT" ]]; then
  VIDEO="$INPUT"
  [[ -n "$NAME" ]] || NAME=$(basename "${INPUT%.*}")
else
  echo "[movie-subtitler] downloading..."
  "$YTDLP" --no-update -f "bv*[ext=mp4][height<=1080]+ba[ext=m4a]/b[ext=mp4]/b" \
    -o "$WORKDIR/source.%(ext)s" "$INPUT"
  VIDEO=$(ls "$WORKDIR"/source.* | head -1)
  [[ -n "$NAME" ]] || NAME=$("$YTDLP" --no-update --skip-download --print "%(title)s" "$INPUT" \
      | tr -cd '[:alnum:] ._-' | tr ' ' '.' | cut -c1-80)
fi
echo "[movie-subtitler] video: $VIDEO"

# --- Step 2: extract audio (faster than feeding whisperx the full video) ----
AUDIO="$WORKDIR/audio.wav"
"$FFMPEG" -y -i "$VIDEO" -vn -ac 1 -ar 16000 -c:a pcm_s16le "$AUDIO" -loglevel error
echo "[movie-subtitler] audio extracted"

# --- Step 3: WhisperX transcribe (+ translate to English) -------------------
# Compute type: WhisperX's CUDA path defaults to float16, which needs an NVIDIA GPU.
# CPU-only boxes (e.g. Apple silicon) must use float32. Detect via nvidia-smi rather
# than assuming a platform.
if command -v nvidia-smi >/dev/null 2>&1; then
  COMPUTE_TYPE_ARGS=()   # let whisperx use its CUDA default (float16)
else
  COMPUTE_TYPE_ARGS=(--compute_type float32)
fi
# --task translate → English text; alignment models are per-source-language and
# can't align translated English text, so skip alignment and keep whisper timestamps.
WX_ARGS=(--model "$MODEL" "${COMPUTE_TYPE_ARGS[@]}" --language "$LANG_CODE" --output_format srt --output_dir "$WORKDIR")
if [[ $TRANSLATE -eq 1 ]]; then WX_ARGS+=(--task translate --no_align); fi
echo "[movie-subtitler] running whisperx (this is the slow part: ~30-60 min for a 2h movie on CPU)..."
"$WHISPERX" "$AUDIO" "${WX_ARGS[@]}"
SRT="$WORKDIR/audio.srt"
[[ -s "$SRT" ]] || { echo "whisperx produced no srt" >&2; exit 1; }
# Name the sidecar to match the output video's basename so VLC auto-pairs it.
cp "$SRT" "$OUTDIR/$NAME.subbed.eng.srt"
echo "[movie-subtitler] subtitles: $OUTDIR/$NAME.subbed.eng.srt"

# --- Step 4: recreate the video with subtitles -------------------------------
OUT="$OUTDIR/$NAME.subbed.mp4"
if [[ $BURN -eq 1 ]]; then
  echo "[movie-subtitler] burning subtitles (full re-encode)..."
  "$FFMPEG" -y -i "$VIDEO" -vf "subtitles=$SRT" -c:a copy "$OUT" -loglevel error
else
  echo "[movie-subtitler] soft-muxing subtitles (no re-encode)..."
  "$FFMPEG" -y -i "$VIDEO" -i "$SRT" -map 0 -map 1 -c copy -c:s mov_text \
    -metadata:s:s:0 language=eng -disposition:s:0 default "$OUT" -loglevel error
fi
echo "[movie-subtitler] DONE: $OUT"
