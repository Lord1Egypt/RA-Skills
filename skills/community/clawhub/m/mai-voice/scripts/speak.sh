#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  speak.sh --text "hello" [--voice en-us-Jasper:MAI-Voice-1] [--style excitement] [--out /tmp/out.mp3]
  speak.sh --text-file /path/to/input.txt [--voice ...] [--style ...] [--format audio-24khz-160kbitrate-mono-mp3]
  speak.sh --list-voices

Required env:
  AZURE_SPEECH_KEY
  AZURE_SPEECH_REGION

Optional env:
  AZURE_SPEECH_OUTPUT_FORMAT   (default: audio-24khz-160kbitrate-mono-mp3)
EOF
  exit 2
}

voices=(
  "en-us-Jasper:MAI-Voice-1"
  "en-us-June:MAI-Voice-1"
  "en-us-Grant:MAI-Voice-1"
  "en-us-Iris:MAI-Voice-1"
  "en-us-Reed:MAI-Voice-1"
  "en-us-Joy:MAI-Voice-1"
)

list_voices() {
  printf '%s\n' "${voices[@]}"
}

escape_xml() {
  sed -e 's/&/\&amp;/g' \
      -e 's/</\&lt;/g' \
      -e 's/>/\&gt;/g' \
      -e "s/'/\&apos;/g" \
      -e 's/"/\&quot;/g'
}

if [[ $# -eq 0 ]]; then
  usage
fi

text=""
text_file=""
voice="en-us-Jasper:MAI-Voice-1"
style=""
out="./mai-voice.mp3"
format="${AZURE_SPEECH_OUTPUT_FORMAT:-audio-24khz-160kbitrate-mono-mp3}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --text)
      text="${2:-}"
      shift 2
      ;;
    --text-file)
      text_file="${2:-}"
      shift 2
      ;;
    --voice)
      voice="${2:-}"
      shift 2
      ;;
    --style)
      style="${2:-}"
      shift 2
      ;;
    --out)
      out="${2:-}"
      shift 2
      ;;
    --format)
      format="${2:-}"
      shift 2
      ;;
    --list-voices)
      list_voices
      exit 0
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      ;;
  esac
done

if [[ -z "${AZURE_SPEECH_KEY:-}" ]]; then
  echo "Missing AZURE_SPEECH_KEY" >&2
  exit 1
fi

if [[ -z "${AZURE_SPEECH_REGION:-}" ]]; then
  echo "Missing AZURE_SPEECH_REGION" >&2
  exit 1
fi

if [[ -n "$text" && -n "$text_file" ]]; then
  echo "Use either --text or --text-file, not both" >&2
  exit 1
fi

if [[ -z "$text" && -z "$text_file" ]]; then
  echo "Provide --text or --text-file" >&2
  exit 1
fi

if [[ -n "$text_file" ]]; then
  if [[ ! -f "$text_file" ]]; then
    echo "Text file not found: $text_file" >&2
    exit 1
  fi
  text="$(cat "$text_file")"
fi

voice_ok=0
for v in "${voices[@]}"; do
  if [[ "$voice" == "$v" ]]; then
    voice_ok=1
    break
  fi
done
if [[ "$voice_ok" -ne 1 ]]; then
  echo "Unknown voice: $voice" >&2
  echo "Supported voices:" >&2
  list_voices >&2
  exit 1
fi

mkdir -p "$(dirname "$out")"

escaped_text="$(printf '%s' "$text" | escape_xml)"
if [[ -n "$style" ]]; then
  escaped_style="$(printf '%s' "$style" | escape_xml)"
  body="<mstts:express-as style=\"${escaped_style}\">${escaped_text}</mstts:express-as>"
else
  body="${escaped_text}"
fi

ssml="<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'><voice name='${voice}'>${body}</voice></speak>"

url="https://${AZURE_SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"

curl -sS --fail-with-body \
  -X POST "$url" \
  -H "Ocp-Apim-Subscription-Key: ${AZURE_SPEECH_KEY}" \
  -H "Content-Type: application/ssml+xml" \
  -H "X-Microsoft-OutputFormat: ${format}" \
  -H "User-Agent: curl" \
  --data-raw "$ssml" \
  --output "$out"

echo "$out"
