#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: bash find-gotchi.sh <gotchi-id> [output-dir] [--format preview|png|hires|svg|all] [--output <dir>]

Arguments:
  <gotchi-id>  Gotchi ID number (e.g., 9638)

Options:
  --format <type>    Image format to generate (default: preview)
  --output <dir>     Output directory (default: current directory)
USAGE
}

require_bin() {
  local bin="$1"
  command -v "$bin" >/dev/null 2>&1 || { echo "❌ Missing required binary: $bin"; exit 1; }
}

GOTCHI_ID=""
OUTPUT_DIR="."
FORMAT="preview"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --format)
      [[ $# -ge 2 ]] || { echo "❌ Missing value for --format"; usage; exit 1; }
      FORMAT="$2"
      shift 2
      ;;
    --output)
      [[ $# -ge 2 ]] || { echo "❌ Missing value for --output"; usage; exit 1; }
      OUTPUT_DIR="$2"
      shift 2
      ;;
    -* )
      echo "❌ Unknown option: $1"
      usage
      exit 1
      ;;
    *)
      if [[ -z "$GOTCHI_ID" ]]; then
        GOTCHI_ID="$1"
      else
        OUTPUT_DIR="$1"
      fi
      shift
      ;;
  esac
done

if [[ -z "$GOTCHI_ID" ]]; then
  usage
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

if [[ ! "$GOTCHI_ID" =~ ^[0-9]+$ ]]; then
  echo "❌ Invalid gotchi ID: \"$GOTCHI_ID\""
  echo "Please provide a numeric gotchi ID (e.g., 9638)"
  exit 1
fi

case "$FORMAT" in
  preview|png|hires|svg|all)
    ;;
  *)
    echo "❌ Invalid format: $FORMAT"
    echo "Valid formats: preview, png, hires, svg, all"
    exit 1
    ;;
esac

require_bin node

echo "🔍 Finding Gotchi #$GOTCHI_ID..."
echo "📂 Output: $OUTPUT_DIR"
echo "🎨 Format: $FORMAT"
echo

mkdir -p "$OUTPUT_DIR"

cd "$SKILL_DIR"
node scripts/fetch-gotchi.js "$GOTCHI_ID" "$OUTPUT_DIR"

SVG_FILE="$OUTPUT_DIR/gotchi-$GOTCHI_ID.svg"
if [[ ! -f "$SVG_FILE" ]]; then
  echo "❌ SVG file not found: $SVG_FILE"
  exit 1
fi

PNG_FILE="$OUTPUT_DIR/gotchi-$GOTCHI_ID.png"
HIRES_FILE="$OUTPUT_DIR/gotchi-$GOTCHI_ID-hires.png"

case "$FORMAT" in
  preview|png)
    node scripts/svg-to-png.js "$SVG_FILE" "$PNG_FILE" 512
    ;;
  hires)
    node scripts/svg-to-png.js "$SVG_FILE" "$HIRES_FILE" 1024
    ;;
  svg)
    echo "✅ SVG only - no PNG conversion"
    ;;
  all)
    node scripts/svg-to-png.js "$SVG_FILE" "$PNG_FILE" 512
    node scripts/svg-to-png.js "$SVG_FILE" "$HIRES_FILE" 1024
    ;;
esac

echo
echo "🎉 Success! Files created:"
echo "   📄 JSON: $OUTPUT_DIR/gotchi-$GOTCHI_ID.json"

if [[ "$FORMAT" != "svg" ]]; then
  if [[ "$FORMAT" == "all" || "$FORMAT" == "png" || "$FORMAT" == "preview" ]]; then
    echo "   🖼️  PNG:  $PNG_FILE (512x512)"
  fi
  if [[ "$FORMAT" == "all" || "$FORMAT" == "hires" ]]; then
    echo "   🖼️  PNG:  $HIRES_FILE (1024x1024)"
  fi
fi

echo "   🎨 SVG:  $SVG_FILE"

if [[ "$FORMAT" == "preview" ]]; then
  echo
  echo "📥 Download options:"
  echo "   • Standard PNG (512x512): --format png"
  echo "   • Hi-res PNG (1024x1024): --format hires"
  echo "   • SVG (vector): --format svg"
  echo "   • All formats: --format all"
fi
