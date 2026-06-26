#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RENDERS_DIR="${ROOT}/Renders"
render_mode="hosted"
gallery_name=""
skip_failures=0
open_on_finish=0
declare -a presets=()
declare -a forward_args=()

usage() {
  cat <<'EOF'
Usage:
  render-preset-gallery.sh [options] [-- wrapper-args...]

Options:
  --preset NAME        Add a preset to the gallery. Repeatable.
  --gallery-name NAME  Name prefix for generated gallery files.
  --render-mode MODE   hosted (default), auto, or unity.
  --skip-failures      Continue rendering and record failed presets instead of stopping.
  --open               Open the generated HTML gallery when finished.
  --help               Show this help.

Notes:
  - If no presets are provided, the helper renders:
      blank-eth, aagent-eth, portrait-eth
  - Extra args after `--` are forwarded to render-custom-gotchi.sh for every preset.

Examples:
  render-preset-gallery.sh
  render-preset-gallery.sh --preset aagent-eth --preset portrait-eth
  render-preset-gallery.sh --skip-failures
  render-preset-gallery.sh --preset aagent-eth --gallery-name quicklook --open
  render-preset-gallery.sh --gallery-name radio -- --bg gotchi-radio
  render-preset-gallery.sh --render-mode auto --preset blank-eth
EOF
}

sanitize_name() {
  printf '%s' "${1:-}" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9_-]+/-/g; s/^-+//; s/-+$//'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --preset)
      presets+=("$2")
      shift 2
      ;;
    --gallery-name)
      gallery_name="$2"
      shift 2
      ;;
    --render-mode)
      render_mode="$2"
      shift 2
      ;;
    --skip-failures)
      skip_failures=1
      shift
      ;;
    --open)
      open_on_finish=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    --)
      shift
      forward_args+=("$@")
      break
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

case "$render_mode" in
  hosted|auto|unity) ;;
  *)
    echo "Unknown render mode: $render_mode" >&2
    exit 1
    ;;
esac

if [[ "${#presets[@]}" -eq 0 ]]; then
  presets=(blank-eth aagent-eth portrait-eth)
fi

mkdir -p "$RENDERS_DIR"

if [[ -z "$gallery_name" ]]; then
  gallery_name="preset-gallery-$(date +%Y%m%d-%H%M%S)"
fi
gallery_slug="$(sanitize_name "$gallery_name")"
if [[ -z "$gallery_slug" ]]; then
  gallery_slug="preset-gallery"
fi

declare -a item_jsons=()
had_failures=0

for preset in "${presets[@]}"; do
  preset_slug="$(sanitize_name "$preset")"
  render_slug="${gallery_slug}-${preset_slug}"
  manifest_path="${RENDERS_DIR}/${render_slug}-manifest.json"
  error_path="${RENDERS_DIR}/${render_slug}-error.json"

  rm -f "$manifest_path" "$error_path"

  printf 'Rendering preset %s -> %s\n' "$preset" "$render_slug"
  render_output=""
  render_status=0
  if [[ "${#forward_args[@]}" -gt 0 ]]; then
    if ! render_output="$(
      bash "${ROOT}/scripts/render-custom-gotchi.sh" \
        --preset "$preset" \
        --slug "$render_slug" \
        --render-mode "$render_mode" \
        "${forward_args[@]}" 2>&1
    )"; then
      render_status=$?
    fi
  else
    if ! render_output="$(
      bash "${ROOT}/scripts/render-custom-gotchi.sh" \
        --preset "$preset" \
        --slug "$render_slug" \
        --render-mode "$render_mode" 2>&1
    )"; then
      render_status=$?
    fi
  fi

  printf '%s\n' "$render_output"

  if [[ "$render_status" -ne 0 || ! -f "$manifest_path" ]]; then
    had_failures=1
    jq -n \
      --arg preset "$preset" \
      --arg slug "$render_slug" \
      --arg render_mode "$render_mode" \
      --arg output "$render_output" \
      --argjson exit_code "$render_status" \
      '{
        ok: false,
        status: "gallery_render_failed",
        preset: $preset,
        slug: $slug,
        render_mode: $render_mode,
        exit_code: $exit_code,
        message: ($output | split("\n") | map(select(length > 0)) | .[-1] // "Render failed."),
        output_log: $output
      }' > "$error_path"

    if [[ "$skip_failures" -eq 0 ]]; then
      echo "Preset failed and --skip-failures was not enabled." >&2
      exit "${render_status:-1}"
    fi

    item_jsons+=("$(jq -c \
      --arg preset "$preset" \
      --arg slug "$render_slug" \
      '{preset:$preset,slug:$slug,ok:.ok,status:.status,message:(.message // ""),error_json:.error_json,output_log:(.output_log // "")}' \
      < <(jq '. + {error_json: "'"$error_path"'"}' "$error_path"))")
    continue
  fi

  item_jsons+=("$(jq -c \
    --arg preset "$preset" \
    --arg slug "$render_slug" \
    '{preset:$preset,slug:$slug,ok:.ok,status:.status,full_png:.full_png,headshot_png:.headshot_png,manifest_json:.manifest_json,warnings:(.warnings // [])}' \
    "$manifest_path")")
done

json_path="${RENDERS_DIR}/${gallery_slug}-gallery.json"
html_path="${RENDERS_DIR}/${gallery_slug}-gallery.html"

printf '%s\n' "${item_jsons[@]}" \
  | jq -s \
    --arg gallery_name "$gallery_slug" \
    --arg render_mode "$render_mode" \
    --argjson had_failures "$had_failures" \
    '{gallery_name:$gallery_name,render_mode:$render_mode,had_failures:$had_failures,items:.}' \
  > "$json_path"

{
  cat <<EOF
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${gallery_slug}</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f7f2ea;
      --card: #fffaf3;
      --ink: #1f1a17;
      --muted: #6c6259;
      --line: #ded2c2;
      --accent: #1dda8d;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 32px;
      font-family: "Avenir Next", "Trebuchet MS", sans-serif;
      background: radial-gradient(circle at top, #fff8ef 0%, var(--bg) 65%);
      color: var(--ink);
    }
    h1 { margin: 0 0 8px; font-size: 34px; }
    p.meta { margin: 0 0 24px; color: var(--muted); }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
    }
    .card {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 18px;
      box-shadow: 0 16px 36px rgba(59, 43, 24, 0.08);
    }
    .card h2 {
      margin: 0 0 6px;
      font-size: 22px;
    }
    .card p {
      margin: 0 0 14px;
      color: var(--muted);
    }
    .status {
      display: inline-block;
      margin-bottom: 12px;
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 600;
      background: #eef8f2;
      color: #145b38;
    }
    .status.fail {
      background: #fff1ef;
      color: #9c2f1f;
    }
    .images {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 14px;
    }
    .images img {
      width: 100%;
      display: block;
      border-radius: 12px;
      border: 1px solid var(--line);
      background: white;
    }
    .links {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
    .links a {
      color: var(--ink);
      text-decoration: none;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 8px 12px;
      background: white;
    }
    .links a:hover {
      border-color: var(--accent);
    }
  </style>
</head>
<body>
  <h1>${gallery_slug}</h1>
  <p class="meta">Render mode: ${render_mode}</p>
  <div class="grid">
EOF

  for entry in "${item_jsons[@]}"; do
    preset="$(jq -r '.preset' <<< "$entry")"
    slug="$(jq -r '.slug' <<< "$entry")"
    ok="$(jq -r '.ok' <<< "$entry")"
    status="$(jq -r '.status' <<< "$entry")"

    if [[ "$ok" == "true" ]]; then
      full_png="$(jq -r '.full_png' <<< "$entry")"
      headshot_png="$(jq -r '.headshot_png' <<< "$entry")"
      manifest_png="$(jq -r '.manifest_json' <<< "$entry")"
      full_base="$(basename "$full_png")"
      headshot_base="$(basename "$headshot_png")"
      manifest_base="$(basename "$manifest_png")"

      cat <<EOF
    <section class="card">
      <h2>${preset}</h2>
      <p>${slug}</p>
      <span class="status">${status}</span>
      <div class="images">
        <img src="${full_base}" alt="${preset} full render">
        <img src="${headshot_base}" alt="${preset} headshot render">
      </div>
      <div class="links">
        <a href="${full_base}">Full PNG</a>
        <a href="${headshot_base}">Headshot PNG</a>
        <a href="${manifest_base}">Manifest</a>
      </div>
    </section>
EOF
    else
      message="$(jq -r '.message' <<< "$entry")"
      error_json="$(jq -r '.error_json' <<< "$entry")"
      error_base="$(basename "$error_json")"

      cat <<EOF
    <section class="card">
      <h2>${preset}</h2>
      <p>${slug}</p>
      <span class="status fail">${status}</span>
      <p>${message}</p>
      <div class="links">
        <a href="${error_base}">Error JSON</a>
      </div>
    </section>
EOF
    fi
  done

  cat <<EOF
  </div>
</body>
</html>
EOF
} > "$html_path"

printf 'Gallery JSON: %s\n' "$json_path"
printf 'Gallery HTML: %s\n' "$html_path"

if [[ "$open_on_finish" -eq 1 ]]; then
  if ! command -v open >/dev/null 2>&1; then
    echo "The --open option requires the macOS 'open' command." >&2
    exit 1
  fi
  open "$html_path"
fi
