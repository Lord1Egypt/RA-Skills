#!/usr/bin/env bash
# generate-plantuml.sh — Convert PlantUML source to SVG, PNG, PDF, or ASCII art
#
# Usage:
#   generate-plantuml.sh <input.puml> [output_dir] [options]
#
# Options:
#   --format svg|png|pdf|txt    Output format (default: svg)
#   --cjk                       Enable CJK (Chinese/Japanese/Korean) font support
#   --no-fix                    Disable automatic aspect ratio correction
#   --max-aspect N              Max allowed aspect ratio before correction (default: 2.5)
#   --no-a4-check               Disable automatic A4 paper fit validation
#                               The A4 check ensures the rendered diagram fits within
#                               either portrait (794×1123 px @ 96 DPI) or landscape
#                               (1123×794 px) A4 dimensions and that the rendered
#                               font remains legible when printed. ON by default.
#   --min-font-pt N             Minimum legible font size on A4 paper, in pt
#                               (default: 8.0). Used only by --a4-check.
#   --use-public-server         Opt-in to render via the public Kroki server.
#                               WARNING: this uploads your diagram source to a third
#                               party (kroki.io by default). Override the host with
#                               PLANTUML_PUBLIC_SERVER=<url> to point at a self-hosted
#                               Kroki instance. Off by default.
#
# Defaults: output_dir=./output, format=svg
#
# ─────────────────────────────────────────────────────────────────────────────
# PRIVACY NOTICE
# ─────────────────────────────────────────────────────────────────────────────
# This script renders diagrams LOCALLY by default. The PlantUML source is NOT
# transmitted off-host unless you explicitly pass --use-public-server.
#
# Conversion methods (tried in strict priority order — local-first):
#   1. Docker (plantuml/plantuml image)        ← PREFERRED default, fully local
#   2. Local plantuml.jar if present           ← offline fallback (Java required)
#   3. Kroki public server (kroki.io)          ← OPT-IN ONLY (--use-public-server)
#                                                Uploads diagram source to a
#                                                third party operated by Yuzu Tech
#                                                (EU). Kroki is open source and
#                                                self-hostable — point at your
#                                                own instance with the env var
#                                                PLANTUML_PUBLIC_SERVER=<url>.
#                                                Avoid the default public host
#                                                for confidential architecture,
#                                                credentials, or proprietary
#                                                business logic.
#
# Note on the previous backend: the legacy https://www.plantuml.com/plantuml
# POST endpoint now sits behind a Cloudflare + Ezoic consent wall that returns
# HTTP 302 to a JavaScript-only HTML page, breaking automated rendering. Kroki
# replaces it as the default opt-in public backend in v1.4.1.
# ─────────────────────────────────────────────────────────────────────────────
#
# Cross-platform: works on Linux, macOS, and Windows (Git Bash / MSYS2 / WSL / Cygwin).
set -euo pipefail

INPUT=""
OUTPUT_DIR="./output"
FORMAT="svg"
CJK=false
AUTO_FIX=true
MAX_ASPECT=2.5
A4_CHECK=true
MIN_FONT_PT=8.0
USE_PUBLIC_SERVER=false

# A4 paper dimensions in pixels at 96 DPI (CSS standard: 1in = 96px, A4 = 210×297 mm)
A4_PORTRAIT_W=794
A4_PORTRAIT_H=1123
A4_LANDSCAPE_W=1123
A4_LANDSCAPE_H=794

# PlantUML/SVG default body font size in px produced by the mandatory preamble
DEFAULT_FONT_PX=12

while [[ $# -gt 0 ]]; do
    case "$1" in
        --format)
            FORMAT="${2:-svg}"
            shift 2
            ;;
        --format=*)
            FORMAT="${1#*=}"
            shift
            ;;
        --cjk)
            CJK=true
            shift
            ;;
        --no-fix)
            AUTO_FIX=false
            shift
            ;;
        --max-aspect)
            MAX_ASPECT="${2:-2.5}"
            shift 2
            ;;
        --max-aspect=*)
            MAX_ASPECT="${1#*=}"
            shift
            ;;
        --no-a4-check)
            A4_CHECK=false
            shift
            ;;
        --min-font-pt)
            MIN_FONT_PT="${2:-8.0}"
            shift 2
            ;;
        --min-font-pt=*)
            MIN_FONT_PT="${1#*=}"
            shift
            ;;
        --use-public-server)
            USE_PUBLIC_SERVER=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 <input.puml> [output_dir] [options]"
            echo ""
            echo "Options:"
            echo "  --format svg|png|pdf|txt    Output format (default: svg)"
            echo "  --cjk                       Enable CJK (Chinese/Japanese/Korean) font support"
            echo "  --no-fix                    Disable automatic aspect ratio correction"
            echo "  --max-aspect N              Max aspect ratio before correction (default: 2.5)"
            echo "  --no-a4-check               Disable A4 paper fit validation (ON by default)"
            echo "  --min-font-pt N             Min legible font size on A4 paper in pt"
            echo "                              (default: 8.0). Used only when A4 check is on."
            echo "  --use-public-server         OPT-IN: render via Kroki (kroki.io). Uploads"
            echo "                              diagram source to a third party (Yuzu Tech, EU)."
            echo "                              Override host via PLANTUML_PUBLIC_SERVER=<url>"
            echo "                              to point at a self-hosted Kroki instance."
            echo "                              Off by default."
            echo ""
            echo "Backend priority (local-first):"
            echo "  1. Docker (plantuml/plantuml)   — preferred, fully local"
            echo "  2. Local plantuml.jar           — offline fallback (Java required)"
            echo "  3. Kroki public server          — OPT-IN ONLY via --use-public-server"
            exit 0
            ;;
        -*)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
        *)
            if [[ -z "$INPUT" ]]; then
                INPUT="$1"
            elif [[ "$OUTPUT_DIR" == "./output" ]]; then
                OUTPUT_DIR="$1"
            fi
            shift
            ;;
    esac
done

if [[ -z "$INPUT" ]]; then
    echo "Usage: $0 <input.puml> [output_dir] [--format svg|png|pdf|txt]" >&2
    exit 1
fi

INPUT_BASENAME=$(basename "$INPUT" .puml)
INPUT_BASENAME="${INPUT_BASENAME%.plantuml}"
INPUT_BASENAME="${INPUT_BASENAME%.txt}"
OUTPUT_FILE="${OUTPUT_DIR}/${INPUT_BASENAME}.${FORMAT}"

mkdir -p "$OUTPUT_DIR"

if [[ ! -f "$INPUT" ]]; then
    echo "ERROR: Input file not found: $INPUT" >&2
    exit 1
fi

case "$FORMAT" in
    svg|png|pdf|txt) ;;
    *)
        echo "ERROR: Unsupported format '$FORMAT'. Use: svg, png, pdf, txt" >&2
        exit 1
        ;;
esac

# Portable temp dir (Linux/macOS: /tmp; Windows Git-Bash/MSYS: $TMPDIR or $TEMP)
PORTABLE_TMP="${TMPDIR:-${TEMP:-${TMP:-/tmp}}}"

# Portable binary-file sniffer: prefer `file` if present, otherwise read magic bytes
detect_binary_ok() {
    local path="$1"
    local fmt="$2"
    [[ -s "$path" ]] || return 1

    if command -v file &>/dev/null; then
        file "$path" | grep -qiE 'png|pdf|image' && return 0
    fi

    # Fallback: check magic bytes with `od` (available on Linux, macOS, and Git Bash)
    if command -v od &>/dev/null; then
        local magic
        magic=$(od -An -N4 -tx1 "$path" 2>/dev/null | tr -d ' \n')
        case "$fmt" in
            png) [[ "$magic" == "89504e47" ]] && return 0 ;;
            pdf) [[ "$magic" == "25504446" ]] && return 0 ;;  # %PDF
        esac
    fi

    # Last resort: assume non-empty file is valid
    return 0
}

echo "🖼️  Converting $INPUT → $OUTPUT_FILE (format: $FORMAT)"

# ═══════════════════════════════════════════════════════════════════════════════
# CJK Font Detection & Configuration
# ═══════════════════════════════════════════════════════════════════════════════

# detect_cjk — Check if file contains CJK characters
# Returns: 0 if CJK found, 1 otherwise
detect_cjk() {
    local file="$1"
    # Try python3, then python (Windows often uses "python"), then perl, then grep -P
    local py_cmd=""
    if command -v python3 &>/dev/null; then
        py_cmd="python3"
    elif command -v python &>/dev/null; then
        py_cmd="python"
    fi
    if [[ -n "$py_cmd" ]]; then
        $py_cmd -c "
import sys
data = open(sys.argv[1], 'rb').read().decode('utf-8', errors='ignore')
for c in data:
    cp = ord(c)
    if ((0x4E00 <= cp <= 0x9FFF) or (0x3400 <= cp <= 0x4DBF) or
        (0x20000 <= cp <= 0x2A6DF) or (0xF900 <= cp <= 0xFAFF) or
        (0x2F800 <= cp <= 0x2FA1F) or (0x3000 <= cp <= 0x303F) or
        (0xFF00 <= cp <= 0xFFEF) or (0x3040 <= cp <= 0x309F) or
        (0x30A0 <= cp <= 0x30FF) or (0xAC00 <= cp <= 0xD7AF)):
        sys.exit(0)
sys.exit(1)
" "$file" 2>/dev/null
        return $?
    elif command -v perl &>/dev/null; then
        perl -CS -ne 'exit(0) if /[\x{4E00}-\x{9FFF}\x{3400}-\x{4DBF}\x{F900}-\x{FAFF}\x{3040}-\x{30FF}\x{AC00}-\x{D7AF}]/' "$file" 2>/dev/null
        return $?
    else
        # grep -P (Perl regex) — supported by GNU grep, not by MSYS2/BSD
        # Fallback: check raw UTF-8 byte sequences for CJK ranges
        grep -qP '[\x{4e00}-\x{9fff}]' "$file" 2>/dev/null && return 0
        grep -qP '[\x{3040}-\x{30ff}]' "$file" 2>/dev/null && return 0
        grep -qP '[\x{ac00}-\x{d7af}]' "$file" 2>/dev/null && return 0
        return 1
    fi
}

# prepare_puml_for_cjk — Creates a modified copy of the puml with CJK font config
# Returns: path to modified puml file
prepare_puml_for_cjk() {
    local src="$1"
    local dst="${src}.cjk.puml"

    sed -e 's/skinparam defaultFontName Helvetica/skinparam defaultFontName "WenQuanYi Micro Hei"/' \
        -e 's/skinparam defaultFontName [A-Za-z]*/skinparam defaultFontName "WenQuanYi Micro Hei"/' \
        "$src" > "$dst"

    if ! grep -q 'defaultFontName' "$dst"; then
        sed -i '1s/^@startuml/@startuml\n!pragma defaultFontName "WenQuanYi Micro Hei"\nskinparam defaultFontName "WenQuanYi Micro Hei"/' "$dst"
    fi

    echo "$dst"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Aspect Ratio Validation & Auto-Fix
# ═══════════════════════════════════════════════════════════════════════════════

# get_svg_dimensions — Extract width/height from SVG viewBox
# Sets global vars: SVG_WIDTH, SVG_HEIGHT
# Returns: 0 on success, 1 on failure
get_svg_dimensions() {
    local svg_file="$1"
    SVG_WIDTH=""
    SVG_HEIGHT=""

    if [[ ! -f "$svg_file" ]]; then
        return 1
    fi

    # Extract viewBox numbers using sed + awk (portable, no grep -P dependency)
    local nums
    nums=$(sed -n 's/.*viewBox="\([0-9.]* [0-9.]* [0-9.]* [0-9.]*\)".*/\1/p' "$svg_file" 2>/dev/null | head -1)

    if [[ -n "$nums" ]]; then
        SVG_WIDTH=$(echo "$nums" | awk '{print int($3)}')
        SVG_HEIGHT=$(echo "$nums" | awk '{print int($4)}')

        if [[ -n "$SVG_WIDTH" ]] && [[ -n "$SVG_HEIGHT" ]]; then
            return 0
        fi
    fi
    return 1
}

# get_png_dimensions — Extract width/height from PNG using ImageMagick identify
# Sets global vars: PNG_WIDTH, PNG_HEIGHT
# Returns: 0 on success, 1 on failure
get_png_dimensions() {
    local png_file="$1"
    PNG_WIDTH=""
    PNG_HEIGHT=""

    if ! command -v identify &>/dev/null; then
        return 1
    fi

    local dims
    dims=$(identify -format "%w %h" "$png_file" 2>/dev/null) || return 1
    PNG_WIDTH=$(echo "$dims" | cut -d' ' -f1)
    PNG_HEIGHT=$(echo "$dims" | cut -d' ' -f2)

    [[ -n "$PNG_WIDTH" ]] && [[ -n "$PNG_HEIGHT" ]]
}

# check_aspect_ratio — Validate aspect ratio against max threshold
# Arguments: $1=image_file, $2=format (svg|png)
# Returns: 0 if OK, 1 if needs fixing, 2 if check failed (can't determine dimensions)
check_aspect_ratio() {
    local img="$1"
    local fmt="$2"
    local w h

    case "$fmt" in
        svg)
            get_svg_dimensions "$img" || return 2
            w="$SVG_WIDTH"
            h="$SVG_HEIGHT"
            ;;
        png)
            get_png_dimensions "$img" || return 2
            w="$PNG_WIDTH"
            h="$PNG_HEIGHT"
            ;;
        *) return 2 ;;
    esac

    if [[ -z "$w" ]] || [[ -z "$h" ]] || [[ "$w" -le 0 ]] || [[ "$h" -le 0 ]]; then
        return 2
    fi

    local ratio
    if [[ "$w" -gt "$h" ]]; then
        ratio=$(awk "BEGIN {printf \"%.2f\", $w / $h}")
    else
        ratio=$(awk "BEGIN {printf \"%.2f\", $h / $w}")
    fi

    echo "  📐 Dimensions: ${w}x${h}, aspect ratio: ${ratio}:1 (max: ${MAX_ASPECT}:1)"

    if awk "BEGIN {exit !($ratio > $MAX_ASPECT)}" 2>/dev/null; then
        echo "  ⚠ Aspect ratio ${ratio}:1 exceeds maximum ${MAX_ASPECT}:1 — diagram may appear stretched"
        return 1
    fi
    return 0
}

# fix_puml_aspect_ratio — Modify .puml file to improve aspect ratio
# Arguments: $1=puml_file, $2=too_wide|too_tall
# Returns: 0 on success, 1 on failure
fix_puml_aspect_ratio() {
    local puml="$1"
    local problem="$2"
    local tmp="${puml}.fixed"

    echo "  → Attempting to fix aspect ratio (${problem})..."
    cp "$puml" "$tmp"

    if grep -q '!pragma aspectRatioFixed' "$puml" 2>/dev/null; then
        echo "  → Already auto-fixed; skipping further attempts"
        rm -f "$tmp"
        return 1
    fi

    sed -i '1s/^@startuml/@startuml\n!pragma aspectRatioFixed/' "$tmp"

    if [[ "$problem" == "too_tall" ]]; then
        if grep -q '@startuml' "$tmp"; then
            sed -i '/@startuml/a\left to right direction' "$tmp"
            echo "  → Applied: left to right direction"
        fi
        if grep -qE '(participant|actor.*->)' "$tmp"; then
            sed -i '/skinparam StereotypeCBackgroundColor white/a\
skinparam ParticipantPadding 5' "$tmp"
        fi
    else
        sed -i '/left to right direction/d' "$tmp"
        if grep -q '@startuml' "$tmp"; then
            sed -i '/@startuml/a\top to bottom direction' "$tmp"
            echo "  → Applied: top to bottom direction"
        fi
        if grep -qE '(participant|actor.*->)' "$tmp"; then
            sed -i '/skinparam StereotypeCBackgroundColor white/a\
skinparam BoxPadding 5\
skinparam ParticipantPadding 5' "$tmp"
        fi
    fi

    if ! grep -q '^scale ' "$tmp"; then
        sed -i '/skinparam StereotypeCBackgroundColor white/a\
scale 0.8' "$tmp"
        echo "  → Applied: scale 0.8"
    fi

    echo "$tmp"
    return 0
}

# ═══════════════════════════════════════════════════════════════════════════════
# A4 Paper Fit Validation & Auto-Scale Fix
# ═══════════════════════════════════════════════════════════════════════════════
#
# Checks the rendered diagram against A4 paper dimensions (210×297 mm).
# PlantUML output is measured in SVG pixels at 96 DPI (the CSS standard);
# 1 in = 96 px, A4 = 210×297 mm = 8.27×11.69 in ⇒ 794×1123 px (portrait),
# 1123×794 px (landscape). The script accepts the diagram if it fits in
# EITHER orientation without overflowing.
#
# If the diagram exceeds A4 in BOTH dimensions, it applies a PlantUML "scale"
# directive computed from the smaller of the two required scale factors, then
# re-renders. After re-rendering it also estimates the effective on-paper font
# size: scale × DEFAULT_FONT_PX ÷ (96/72) = scale × DEFAULT_FONT_PX × 0.75,
# i.e. px-to-pt ratio. If the effective pt is below --min-font-pt, the diagram
# can no longer be made readable by scaling alone and the user is warned.

# check_a4_fit — Validate image fits within A4 portrait OR landscape
# Arguments: $1=image_file, $2=format (svg|png)
# Sets global: A4_SCALE_FACTOR (1.0 if already fits; otherwise required factor)
# Returns: 0 if fits A4, 1 if needs scaling, 2 if check failed
check_a4_fit() {
    local img="$1"
    local fmt="$2"
    local w h

    case "$fmt" in
        svg)
            get_svg_dimensions "$img" || return 2
            w="$SVG_WIDTH"
            h="$SVG_HEIGHT"
            ;;
        png)
            get_png_dimensions "$img" || return 2
            w="$PNG_WIDTH"
            h="$PNG_HEIGHT"
            ;;
        *) return 2 ;;
    esac

    if [[ -z "$w" ]] || [[ -z "$h" ]] || [[ "$w" -le 0 ]] || [[ "$h" -le 0 ]]; then
        return 2
    fi

    A4_SCALE_FACTOR="1.0"

    local fits_portrait fits_landscape
    awk "BEGIN {exit !($w <= $A4_PORTRAIT_W && $h <= $A4_PORTRAIT_H)}" 2>/dev/null && fits_portrait=1 || fits_portrait=0
    awk "BEGIN {exit !($w <= $A4_LANDSCAPE_W && $h <= $A4_LANDSCAPE_H)}" 2>/dev/null && fits_landscape=1 || fits_landscape=0

    if [[ "$fits_portrait" -eq 1 ]] || [[ "$fits_landscape" -eq 1 ]]; then
        echo "  📄 A4 fit: ${w}x${h}px fits A4 portrait (794x1123) or landscape (1123x794) ✓"
        return 0
    fi

    # scale = min(target_w / w, target_h / h); compute for each orientation
    local sp sl
    sp=$(awk "BEGIN {p1=($A4_PORTRAIT_W / $w); p2=($A4_PORTRAIT_H / $h); s=(p1<p2)?p1:p2; printf \"%.3f\", s}" 2>/dev/null || echo "")
    sl=$(awk "BEGIN {l1=($A4_LANDSCAPE_W / $w); l2=($A4_LANDSCAPE_H / $h); s=(l1<l2)?l1:l2; printf \"%.3f\", s}" 2>/dev/null || echo "")

    if [[ -z "$sp" ]] || [[ -z "$sl" ]]; then
        echo "  ⚠ A4 fit: could not compute scale factor (awk failed); skipping"
        return 2
    fi

    # Use the orientation that needs less shrinking (the higher of the two factors)
    A4_SCALE_FACTOR=$(awk "BEGIN {printf \"%.3f\", ($sp > $sl) ? $sp : $sl}" 2>/dev/null)

    # Clamp: never go below 0.15 — beyond that the diagram is unreadable
    local clamped
    clamped=$(awk "BEGIN {printf \"%.3f\", ($A4_SCALE_FACTOR < 0.15) ? 0.15 : $A4_SCALE_FACTOR}" 2>/dev/null)
    A4_SCALE_FACTOR="$clamped"

    echo "  📄 A4 fit: ${w}x${h}px exceeds A4 portrait (794x1123) and landscape (1123x794)"
    echo "     Required scale to fit: ${A4_SCALE_FACTOR} (portrait factor ${sp}, landscape factor ${sl})"
    return 1
}

# fix_puml_a4_fit — Insert a PlantUML scale directive into a .puml copy
# Arguments: $1=puml_file
# Uses global A4_SCALE_FACTOR set by check_a4_fit
# Returns: path to modified .puml on stdout, empty string on failure
fix_puml_a4_fit() {
    local puml="$1"
    local tmp="${puml}.a4fixed"

    if [[ -z "$A4_SCALE_FACTOR" ]] || [[ "$A4_SCALE_FACTOR" == "1.0" ]]; then
        echo ""
        return 1
    fi
    if grep -q '!pragma a4FitFixed' "$puml" 2>/dev/null; then
        echo ""
        return 1
    fi

    cp "$puml" "$tmp"
    sed -i '1s/^@startuml/@startuml\n!pragma a4FitFixed/' "$tmp"

    # PlantUML accepts only one scale directive per diagram; strip the
    # aspect-ratio auto-fix's `scale 0.8` so our A4 scale takes effect.
    sed -i '/^scale 0\.8$/d' "$tmp"

    sed -i "/!pragma a4FitFixed/a scale ${A4_SCALE_FACTOR}" "$tmp"
    echo "  → Applied: scale ${A4_SCALE_FACTOR} (A4 fit)"

    # Warn about font legibility on A4 if we shrunk a lot
    local effective_pt
    effective_pt=$(awk "BEGIN {printf \"%.1f\", $A4_SCALE_FACTOR * $DEFAULT_FONT_PX * 0.75}" 2>/dev/null)
    if [[ -n "$effective_pt" ]]; then
        if awk "BEGIN {exit !($effective_pt < $MIN_FONT_PT)}" 2>/dev/null; then
            echo "  ⚠ After scaling to ${A4_SCALE_FACTOR}, estimated font ≈ ${effective_pt}pt on A4"
            echo "    That is below --min-font-pt ${MIN_FONT_PT} and may be hard to read in print."
            echo "    Consider splitting into multiple diagrams or abbreviating labels."
        else
            echo "     Estimated font ≈ ${effective_pt}pt on A4 (≥ min ${MIN_FONT_PT}pt) ✓"
        fi
    fi

    echo "$tmp"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Rendering Backends
# ═══════════════════════════════════════════════════════════════════════════════

# ─── Method 3: Kroki Public Server (OPT-IN ONLY) ────────────────────────────
# DISABLED BY DEFAULT for privacy. Only invoked when the user explicitly passes
# --use-public-server. This backend POSTs the entire diagram source to Kroki
# (kroki.io by default, overridable via PLANTUML_PUBLIC_SERVER) — never use it
# for confidential architecture, credentials, or proprietary business
# processes. Kroki is open source and self-hostable.
convert_via_server() {
    local src="$1"

    if ! $USE_PUBLIC_SERVER; then
        echo "  → Public server disabled (privacy default). Pass --use-public-server to enable."
        return 1
    fi

    local server_host="${PLANTUML_PUBLIC_SERVER:-https://kroki.io}"
    server_host="${server_host%/}"
    local server_url="${server_host}/plantuml/${FORMAT}"

    if ! command -v curl &>/dev/null; then
        echo "  → curl not available, skipping public server"
        return 1
    fi

    local host_label
    host_label=$(echo "$server_host" | sed -E 's|^https?://||; s|/.*$||')

    echo ""
    echo "  ⚠  PRIVACY WARNING: about to upload diagram source to ${server_url}"
    echo "     The full contents of '$src' will be transmitted to ${host_label}."
    if [[ "$server_host" == "https://kroki.io" ]]; then
        echo "     kroki.io is operated by Yuzu Tech (EU). Kroki is open source and"
        echo "     self-hostable — set PLANTUML_PUBLIC_SERVER=<your-url> to use your own."
    else
        echo "     (Custom backend selected via PLANTUML_PUBLIC_SERVER.)"
    fi
    echo "     Do NOT use this backend for confidential architecture, credentials,"
    echo "     customer data, or proprietary business logic."
    echo ""
    echo "  → Trying public server (opt-in via --use-public-server)..."
    if curl -sSfL --connect-timeout 10 --max-time 60 \
            -H "Content-Type: text/plain" \
            -o "$OUTPUT_FILE" -X POST "$server_url" --data-binary "@$src" 2>/dev/null; then
        if [[ "$FORMAT" == "svg" ]] && [[ -s "$OUTPUT_FILE" ]] && grep -q '<svg' "$OUTPUT_FILE"; then
            echo "  ✓ Success (public server)"
            return 0
        elif [[ "$FORMAT" == "txt" ]] && [[ -s "$OUTPUT_FILE" ]]; then
            echo "  ✓ Success (public server)"
            return 0
        elif [[ "$FORMAT" != "svg" && "$FORMAT" != "txt" ]] && detect_binary_ok "$OUTPUT_FILE" "$FORMAT"; then
            echo "  ✓ Success (public server)"
            return 0
        fi
    fi
    echo "  ✗ Public server failed — check network or try Docker/local JAR backend"
    return 1
}

# ─── Method 1: Docker (PREFERRED — fully local) ─────────────────────────────
# Always tried first. Renders entirely on-host with no third-party network calls.
convert_via_docker() {
    local src="$1"
    if ! command -v docker &>/dev/null; then
        echo "  → Docker not available, skipping"
        return 1
    fi

    echo "  → Trying Docker (plantuml/plantuml)..."
    local ext="$FORMAT"
    [[ "$FORMAT" == "txt" ]] && ext="utxt"

    # Portable temporary working directory
    local docker_tmp="${PORTABLE_TMP}/plantuml_docker_$$"
    mkdir -p "$docker_tmp"
    cp "$src" "$docker_tmp/"

    # On Windows Git-Bash/MSYS the path passed to `docker -v` must be converted.
    local docker_mount="$docker_tmp"
    if command -v cygpath &>/dev/null; then
        docker_mount=$(cygpath -w "$docker_tmp")
    elif command -v wslpath &>/dev/null; then
        docker_mount=$(wslpath -w "$docker_tmp" 2>/dev/null || echo "$docker_tmp")
    fi

    # CJK font support: mount host font directories into container
    if $CJK; then
        local font_mounts=()
        # Linux/macOS font paths
        for font_dir in /usr/share/fonts /usr/local/share/fonts /System/Library/Fonts; do
            [[ -d "$font_dir" ]] && font_mounts+=(-v "${font_dir}:${font_dir}:ro")
        done
        # Windows font paths (Git Bash/MSYS: /c/Windows/Fonts, WSL: /mnt/c/Windows/Fonts)
        for win_fonts in /c/Windows/Fonts /mnt/c/Windows/Fonts; do
            [[ -d "$win_fonts" ]] && font_mounts+=(-v "${win_fonts}:/Windows/Fonts:ro")
        done

        if [[ ${#font_mounts[@]} -gt 0 ]]; then
            if MSYS_NO_PATHCONV=1 docker run --rm \
                -v "${docker_mount}:/data" \
                "${font_mounts[@]}" \
                --entrypoint sh plantuml/plantuml:latest \
                -c "fc-cache -f 2>/dev/null; plantuml -t${ext} /data/$(basename "$src")" 2>/dev/null; then
                local generated
                generated=$(ls "$docker_tmp"/*."$ext" 2>/dev/null || ls "$docker_tmp"/*."$FORMAT" 2>/dev/null || echo "")
                [[ -n "$generated" ]] && mv "$generated" "$OUTPUT_FILE"
                rm -rf "$docker_tmp"
                echo "  ✓ Success (Docker + CJK)"
                return 0
            fi
        else
            echo "  ⚠ CJK mode: no host font directories found. CJK characters may not render correctly."
            echo "    Install CJK fonts on your system (e.g., 'apt install fonts-wqy-zenhei')"
        fi
    fi

    # Standard Docker rendering
    if MSYS_NO_PATHCONV=1 docker run --rm -v "${docker_mount}:/data" plantuml/plantuml:latest \
        "-t${ext}" "/data/$(basename "$INPUT")" 2>/dev/null; then

        local generated
        generated=$(ls "$docker_tmp"/*."$ext" 2>/dev/null || ls "$docker_tmp"/*."$FORMAT" 2>/dev/null || echo "")
        if [[ -n "$generated" ]]; then
            mv "$generated" "$OUTPUT_FILE"
            rm -rf "$docker_tmp"
            echo "  ✓ Success (Docker)"
            return 0
        fi
    fi
    rm -rf "$docker_tmp"
    echo "  ✗ Docker conversion failed"
    return 1
}

# ─── Method 2: Local JAR (offline fallback) ─────────────────────────────────
convert_via_local() {
    local src="$1"
    local jar_paths=(
        "/usr/local/bin/plantuml.jar"
        "/usr/share/plantuml/plantuml.jar"
        "${HOME:-}/plantuml.jar"
        "${USERPROFILE:-}/plantuml.jar"
        "${PROGRAMFILES:-}/PlantUML/plantuml.jar"
        "${LOCALAPPDATA:-}/PlantUML/plantuml.jar"
        "./plantuml.jar"
    )
    local jar=""
    for p in "${jar_paths[@]}"; do
        [[ -z "$p" ]] && continue
        if [[ -f "$p" ]]; then
            jar="$p"
            break
        fi
    done
    if [[ -z "$jar" ]]; then
        echo "  → No local plantuml.jar found, skipping"
        return 1
    fi
    if ! command -v java &>/dev/null; then
        echo "  → Java not available, skipping local JAR"
        return 1
    fi

    echo "  → Trying local JAR ($jar)..."
    local ext="$FORMAT"
    [[ "$FORMAT" == "txt" ]] && ext="utxt"

    if java -jar "$jar" "-t${ext}" -o "$OUTPUT_DIR" "$src" 2>/dev/null; then
        local generated
        generated=$(ls "$OUTPUT_DIR"/"${INPUT_BASENAME}"*."$FORMAT" 2>/dev/null | head -1)
        if [[ -n "$generated" ]] && [[ "$generated" != "$OUTPUT_FILE" ]]; then
            mv "$generated" "$OUTPUT_FILE"
        fi
        if [[ -f "$OUTPUT_FILE" ]]; then
            echo "  ✓ Success (local JAR)"
            return 0
        fi
    fi
    echo "  ✗ Local JAR failed"
    return 1
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════════════════════

# ── CJK Detection ────────────────────────────────────────────────────────────
if ! $CJK; then
    if detect_cjk "$INPUT"; then
        echo ""
        echo "🔤 CJK (Chinese/Japanese/Korean) characters detected in input."
        echo "   These may not render correctly without CJK font support."
        echo "   Re-run with --cjk to enable CJK rendering, or install CJK fonts."
        echo "   Attempting to proceed anyway..."
        echo ""
    fi
fi

# ── Prepare working copy ─────────────────────────────────────────────────────
WORK_COPY="$INPUT"
CJK_COPY=""
if $CJK; then
    echo "🔤 CJK mode enabled: configuring CJK-compatible fonts"
    CJK_COPY=$(prepare_puml_for_cjk "$INPUT")
    WORK_COPY="$CJK_COPY"
fi

# ── Render ───────────────────────────────────────────────────────────────────
RENDER_OK=false
MAX_FIX_ATTEMPTS=2
FIX_ATTEMPT=0
ASPECT_DONE=false
A4_TRIED=false

while [[ "$FIX_ATTEMPT" -le "$MAX_FIX_ATTEMPTS" ]]; do
    convert_via_docker "$WORK_COPY" || convert_via_local "$WORK_COPY" || convert_via_server "$WORK_COPY" || {
        echo ""
        echo "❌ All conversion methods failed."
        echo "   Install options (local, recommended for privacy):"
        echo "   1. Docker: docker pull plantuml/plantuml:latest"
        echo "   2. Java + JAR: download plantuml.jar from https://plantuml.com/download"
        echo "   Or, to use the public Kroki server (uploads diagram to kroki.io):"
        echo "   3. Re-run with --use-public-server (review the privacy notice first)"
        echo "      Override the host with PLANTUML_PUBLIC_SERVER=<url> if self-hosting"
        [[ -n "$CJK_COPY" ]] && rm -f "$CJK_COPY"
        exit 1
    }
    RENDER_OK=true

    if [[ "$FORMAT" == "txt" ]] || [[ "$FORMAT" == "pdf" ]]; then
        break
    fi

    if $AUTO_FIX && ! $ASPECT_DONE; then
        aspect_rc=2
        check_aspect_ratio "$OUTPUT_FILE" "$FORMAT" && aspect_rc=0 || aspect_rc=$?

        if [[ "$aspect_rc" -eq 2 ]]; then
            echo "  ⓘ Could not determine image dimensions; skipping aspect ratio check."
            ASPECT_DONE=true
        elif [[ "$aspect_rc" -eq 1 ]]; then
            FIX_ATTEMPT=$((FIX_ATTEMPT + 1))
            if [[ "$FIX_ATTEMPT" -gt "$MAX_FIX_ATTEMPTS" ]]; then
                echo "  ⚠ Maximum fix attempts ($MAX_FIX_ATTEMPTS) reached. Manual adjustment may be needed."
                break
            fi

            aspect_w="$SVG_WIDTH"; aspect_h="$SVG_HEIGHT"
            if [[ "$FORMAT" == "png" ]]; then aspect_w="$PNG_WIDTH"; aspect_h="$PNG_HEIGHT"; fi

            aspect_problem="too_wide"
            [[ "$aspect_h" -gt "$aspect_w" ]] && aspect_problem="too_tall"

            aspect_fixed=$(fix_puml_aspect_ratio "$WORK_COPY" "$aspect_problem") || {
                echo "  ✗ Auto-fix failed; using original diagram."
                break
            }

            if [[ "$WORK_COPY" != "$INPUT" ]]; then
                rm -f "$WORK_COPY"
            fi
            WORK_COPY="$aspect_fixed"
            ASPECT_DONE=true
            echo "  → Re-rendering with corrected layout..."
            continue
        fi
        ASPECT_DONE=true
    fi

    if $A4_CHECK && ! $A4_TRIED; then
        a4_rc=2
        check_a4_fit "$OUTPUT_FILE" "$FORMAT" && a4_rc=0 || a4_rc=$?

        if [[ "$a4_rc" -eq 2 ]]; then
            echo "  ⓘ Could not determine image dimensions; skipping A4 check."
            break
        elif [[ "$a4_rc" -eq 1 ]]; then
            FIX_ATTEMPT=$((FIX_ATTEMPT + 1))
            if [[ "$FIX_ATTEMPT" -gt "$MAX_FIX_ATTEMPTS" ]]; then
                echo "  ⚠ Maximum fix attempts ($MAX_FIX_ATTEMPTS) reached; A4 fit may not hold."
                break
            fi

            a4_fixed=$(fix_puml_a4_fit "$WORK_COPY") || {
                echo "  ✗ A4 auto-fit failed; using current diagram."
                break
            }

            if [[ -z "$a4_fixed" ]]; then
                echo "  ✗ A4 auto-fit produced no output; using current diagram."
                A4_TRIED=true
                break
            fi

            if [[ "$WORK_COPY" != "$INPUT" ]]; then
                rm -f "$WORK_COPY"
            fi
            WORK_COPY="$a4_fixed"
            A4_TRIED=true
            echo "  → Re-rendering with A4-fit scale..."
            continue
        fi
    fi

    break
done

# ── Cleanup temp files ───────────────────────────────────────────────────────
if [[ "$WORK_COPY" != "$INPUT" ]]; then
    rm -f "$WORK_COPY"
fi
[[ -n "$CJK_COPY" ]] && [[ "$CJK_COPY" != "$WORK_COPY" ]] && rm -f "$CJK_COPY"

# ── Report ───────────────────────────────────────────────────────────────────
if $RENDER_OK; then
    echo ""
    echo "✅ Output: $OUTPUT_FILE"
    echo "$OUTPUT_FILE"
fi
