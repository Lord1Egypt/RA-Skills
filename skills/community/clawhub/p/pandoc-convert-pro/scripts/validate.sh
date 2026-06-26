#!/usr/bin/env bash
set -euo pipefail

show_help() {
    cat <<'EOF'
Usage: validate.sh <input-file> -o <output-file> [options]

Checks that pandoc conversion prerequisites are available before converting.
Common options checked: --to, --pdf-engine, --bibliography, --csl,
--reference-doc, --template, --css, --resource-path, --extract-media.
EOF
}

fail() {
    echo "Error: $*" >&2
    exit 1
}

warn() {
    echo "Warning: $*" >&2
}

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
    show_help
    exit 0
fi

if ! command -v pandoc >/dev/null 2>&1; then
    fail "pandoc is not installed or not found in PATH. Install it from https://pandoc.org/installing.html, or run this skill's optional installer: bash \"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)/install_pandoc.sh\""
fi

input=""
output=""
to_format=""
pdf_engine=""
resource_paths=""
files_to_check=""

while [ "$#" -gt 0 ]; do
    case "$1" in
        -o|--output)
            [ "$#" -ge 2 ] || fail "$1 requires a value"
            output="$2"
            shift 2
            ;;
        -o*)
            output="${1#-o}"
            shift
            ;;
        --output=*)
            output="${1#--output=}"
            shift
            ;;
        --to|-t|--from|-f|--pdf-engine|--bibliography|--csl|--reference-doc|--template|--css|--resource-path|--extract-media)
            [ "$#" -ge 2 ] || fail "$1 requires a value"
            case "$1" in
                --to|-t) to_format="$2" ;;
                --pdf-engine) pdf_engine="$2" ;;
                --bibliography|--csl|--reference-doc|--template|--css) files_to_check="$files_to_check
$2" ;;
                --resource-path) resource_paths="$2" ;;
            esac
            shift 2
            ;;
        --to=*|-t=*)
            to_format="${1#*=}"
            shift
            ;;
        --pdf-engine=*)
            pdf_engine="${1#--pdf-engine=}"
            shift
            ;;
        --bibliography=*|--csl=*|--reference-doc=*|--template=*|--css=*)
            files_to_check="$files_to_check
${1#*=}"
            shift
            ;;
        --resource-path=*)
            resource_paths="${1#--resource-path=}"
            shift
            ;;
        --metadata|-M|--variable|-V|--toc-depth)
            [ "$#" -ge 2 ] || fail "$1 requires a value"
            shift 2
            ;;
        --metadata=*|-M=*|--variable=*|-V=*|--toc-depth=*)
            shift
            ;;
        --standalone|-s|--toc|--table-of-contents|--number-sections|--citeproc|--embed-resources|--self-contained)
            shift
            ;;
        --)
            shift
            break
            ;;
        --*)
            shift
            ;;
        *)
            if [ -z "$input" ]; then
                input="$1"
            fi
            shift
            ;;
    esac
done

[ -n "$input" ] || fail "input file is required"
[ -f "$input" ] || fail "input file does not exist: $input"
[ -n "$output" ] || fail "output file is required; pass -o <output-file>"

output_ext="${output##*.}"
if [ "$output_ext" = "$output" ]; then
    output_ext=""
fi

if [ "$to_format" = "pdf" ] || [ "$output_ext" = "pdf" ]; then
    if [ -n "$pdf_engine" ] && ! command -v "$pdf_engine" >/dev/null 2>&1; then
        fail "PDF engine not found: $pdf_engine. Install it or choose another engine. For Chinese documents, xelatex is recommended when available."
    fi
    if [ -z "$pdf_engine" ]; then
        warn "PDF output requested without --pdf-engine. Pandoc will use its default PDF engine, which may require a LaTeX installation."
    fi
fi

if [ -n "$resource_paths" ]; then
    old_ifs="$IFS"
    IFS=':'
    for path_item in $resource_paths; do
        [ -z "$path_item" ] && continue
        [ -d "$path_item" ] || fail "resource path does not exist or is not a directory: $path_item"
    done
    IFS="$old_ifs"
fi

printf '%s
' "$files_to_check" | while IFS= read -r checked_file; do
    [ -z "$checked_file" ] && continue
    [ -f "$checked_file" ] || fail "referenced file does not exist: $checked_file"
done

echo "Validation passed"
