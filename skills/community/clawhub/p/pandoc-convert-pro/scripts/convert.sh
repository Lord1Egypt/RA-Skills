#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

show_help() {
    cat <<'EOF'
Usage: convert.sh <input-file> -o <output-file> [options]

Convert one document with pandoc and smart defaults.

Common options:
  -f, --from FORMAT           Input format override
  -t, --to FORMAT             Output format override
  -o, --output FILE           Output file
  -s, --standalone            Produce standalone document
      --toc                   Add table of contents
      --toc-depth N           Table of contents depth
      --number-sections       Number section headings
      --citeproc              Process citations
      --bibliography FILE     Bibliography file
      --csl FILE              Citation style file
      --reference-doc FILE    DOCX/ODT reference style document
      --template FILE         Pandoc template file
      --css FILE              CSS file for HTML/EPUB
      --pdf-engine ENGINE     PDF engine, e.g. xelatex
      --resource-path PATHS   Resource search paths separated by ':'
      --extract-media DIR     Extract embedded media when converting from DOCX/EPUB
      --metadata KEY=VALUE    Metadata value; can be repeated
EOF
}

fail() {
    echo "Error: $*" >&2
    exit 1
}

format_from_extension() {
    local path="$1"
    local ext="${path##*.}"
    [ "$ext" = "$path" ] && return 0
    ext="$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')"
    case "$ext" in
        md|markdown|mkd) echo "markdown" ;;
        html|htm) echo "html" ;;
        docx) echo "docx" ;;
        odt) echo "odt" ;;
        rtf) echo "rtf" ;;
        epub) echo "epub" ;;
        tex|latex) echo "latex" ;;
        typ) echo "typst" ;;
        rst) echo "rst" ;;
        adoc|asciidoc) echo "asciidoc" ;;
        org) echo "org" ;;
        ipynb) echo "ipynb" ;;
        txt) echo "markdown" ;;
        pdf) echo "pdf" ;;
        *) echo "" ;;
    esac
}

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
    show_help
    exit 0
fi

[ "$#" -gt 0 ] || { show_help; exit 1; }

input=""
output=""
from_format=""
to_format=""
pandoc_args=()
validate_args=()

while [ "$#" -gt 0 ]; do
    case "$1" in
        -o|--output)
            [ "$#" -ge 2 ] || fail "$1 requires a value"
            output="$2"
            pandoc_args+=("-o" "$2")
            validate_args+=("-o" "$2")
            shift 2
            ;;
        -o*)
            output="${1#-o}"
            pandoc_args+=("-o" "$output")
            validate_args+=("-o" "$output")
            shift
            ;;
        --output=*)
            output="${1#--output=}"
            pandoc_args+=("--output" "$output")
            validate_args+=("--output" "$output")
            shift
            ;;
        -f|--from)
            [ "$#" -ge 2 ] || fail "$1 requires a value"
            from_format="$2"
            pandoc_args+=("--from" "$2")
            validate_args+=("--from" "$2")
            shift 2
            ;;
        -t|--to)
            [ "$#" -ge 2 ] || fail "$1 requires a value"
            to_format="$2"
            if [ "$2" != "pdf" ]; then
                pandoc_args+=("--to" "$2")
            fi
            validate_args+=("--to" "$2")
            shift 2
            ;;
        --from=*|-f=*)
            from_format="${1#*=}"
            pandoc_args+=("--from" "$from_format")
            validate_args+=("--from" "$from_format")
            shift
            ;;
        --to=*|-t=*)
            to_format="${1#*=}"
            if [ "$to_format" != "pdf" ]; then
                pandoc_args+=("--to" "$to_format")
            fi
            validate_args+=("--to" "$to_format")
            shift
            ;;
        --standalone|-s|--toc|--table-of-contents|--number-sections|--citeproc|--embed-resources|--self-contained)
            pandoc_args+=("$1")
            validate_args+=("$1")
            shift
            ;;
        --toc-depth|--metadata|-M|--variable|-V|--bibliography|--csl|--reference-doc|--template|--css|--pdf-engine|--resource-path|--extract-media)
            [ "$#" -ge 2 ] || fail "$1 requires a value"
            pandoc_args+=("$1" "$2")
            validate_args+=("$1" "$2")
            shift 2
            ;;
        --toc-depth=*|--metadata=*|-M=*|--variable=*|-V=*|--bibliography=*|--csl=*|--reference-doc=*|--template=*|--css=*|--pdf-engine=*|--resource-path=*|--extract-media=*)
            pandoc_args+=("$1")
            validate_args+=("$1")
            shift
            ;;
        --)
            shift
            while [ "$#" -gt 0 ]; do
                pandoc_args+=("$1")
                shift
            done
            ;;
        --*)
            pandoc_args+=("$1")
            validate_args+=("$1")
            shift
            ;;
        *)
            if [ -z "$input" ]; then
                input="$1"
            else
                pandoc_args+=("$1")
            fi
            shift
            ;;
    esac
done

[ -n "$input" ] || fail "input file is required"
[ -n "$output" ] || fail "output file is required; pass -o <output-file>"

if [ -z "$from_format" ]; then
    inferred_from="$(format_from_extension "$input")"
    [ -n "$inferred_from" ] && pandoc_args=("--from" "$inferred_from" "${pandoc_args[@]}")
fi

if [ -z "$to_format" ]; then
    inferred_to="$(format_from_extension "$output")"
    if [ -n "$inferred_to" ] && [ "$inferred_to" != "pdf" ]; then
        pandoc_args+=("--to" "$inferred_to")
    fi
fi

bash "$SCRIPT_DIR/validate.sh" "$input" "${validate_args[@]}"
mkdir -p "$(dirname "$output")"
pandoc "$input" "${pandoc_args[@]}"
echo "Conversion successful: $output"
