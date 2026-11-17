#!/usr/bin/env bash
set -euo pipefail

# Usage: generate_default_icon_macos.sh <output-dir>
output_dir="${1:?output directory is required}"
[[ "$(uname -s)" == "Darwin" ]] || { echo "This icon converter is macOS-only." >&2; exit 1; }

mkdir -p "$output_dir"
svg_path="$output_dir/icon.svg"
iconset_path="$output_dir/icon.iconset"
mkdir -p "$iconset_path"

cat > "$svg_path" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#176b62"/><stop offset="1" stop-color="#092923"/></linearGradient></defs>
  <rect width="1024" height="1024" rx="228" fill="url(#g)"/>
  <path d="M252 566c0-188 142-318 316-318 116 0 213 57 260 151" fill="none" stroke="#7df5bd" stroke-linecap="round" stroke-width="132"/>
  <circle cx="757" cy="393" r="74" fill="#baffd9"/><circle cx="781" cy="378" r="15" fill="#08221d"/>
  <path d="M481 743c80 55 180 54 254 1" fill="none" stroke="#7df5bd" stroke-linecap="round" stroke-width="96"/>
  <circle cx="780" cy="705" r="46" fill="#ff6e89"/>
</svg>
SVG

for size in 16 32 128 256 512; do
  sips -s format png -Z "$size" "$svg_path" --out "$iconset_path/icon_${size}x${size}.png" >/dev/null
  double=$((size * 2))
  sips -s format png -Z "$double" "$svg_path" --out "$iconset_path/icon_${size}x${size}@2x.png" >/dev/null
done
iconutil -c icns "$iconset_path" -o "$output_dir/icon.icns"
echo "Created $svg_path and $output_dir/icon.icns"
