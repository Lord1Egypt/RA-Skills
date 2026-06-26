#!/usr/bin/env bash
set -euo pipefail
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Text & Data Parser
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DATA_DIR="${HOME}/.local/share/parser-tool"
VERSION="3.0.2"

mkdir -p "$DATA_DIR"

# ── Helpers ──────────────────────────────────────────────────────────────────

die() { echo "Error: $*" >&2; exit 1; }

check_file() {
    local f="${1:-}"
    [[ -z "$f" ]] && die "No file specified"
    [[ -f "$f" ]] || die "File not found: $f"
    [[ -r "$f" ]] || die "File not readable: $f"
}

usage() {
    cat <<'EOF'
Parser Tool — Parse and extract data from various file formats

USAGE:
  parser json <file> [jq-path]
  parser csv <file> [column]
  parser xml <file> [xpath]
  parser yaml <file> [key]
  parser lines <file> [pattern]
  parser split <file> <delimiter>
  parser extract <file> <regex>
  parser stats <file>
  parser help

COMMANDS:
  json      Parse JSON files (uses jq if available, else built-in)
  csv       Parse CSV files, optionally extract a column by name or number
  xml       Parse XML files with optional XPath (requires python3)
  yaml      Parse YAML files with optional key path (requires python3)
  lines     Filter lines by pattern (grep-like, with context)
  split     Split file content by delimiter
  extract   Extract text matching a regex pattern
  stats     Show file statistics (lines, words, chars, encoding)
  help      Show this help message

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
EOF
}

# ── JSON Parsing ─────────────────────────────────────────────────────────────

cmd_json() {
    local file="${1:-}"
    local jq_path="${2:-.}"

    check_file "$file"

    # Validate JSON first
    if command -v jq &>/dev/null; then
        if ! jq empty "$file" 2>/dev/null; then
            die "Invalid JSON in $file"
        fi
        jq "$jq_path" "$file"
    else
        # Fallback: use python3 for JSON parsing
        if command -v python3 &>/dev/null; then
            FILE="$file" JQ_PATH="$jq_path" python3 << 'PYEOF'
import json, os
with open(os.environ["FILE"]) as f:
    data = json.load(f)
path = os.environ.get("JQ_PATH", ".")
if path == ".":
    print(json.dumps(data, indent=2))
else:
    parts = path.lstrip(".").split(".")
    current = data
    for p in parts:
        if not p:
            continue
        if isinstance(current, dict):
            current = current[p]
        elif isinstance(current, list):
            current = current[int(p)]
    print(json.dumps(current, indent=2) if isinstance(current, (dict, list)) else str(current))
PYEOF
        else
            # Ultra-fallback: just pretty-print-ish using sed
            echo "Warning: Neither jq nor python3 found. Showing raw content." >&2
            cat "$file"
        fi
    fi
}

# ── CSV Parsing ──────────────────────────────────────────────────────────────

cmd_csv() {
    local file="${1:-}"
    local col="${2:-}"

    check_file "$file"

    if [[ -z "$col" ]]; then
        # Display full CSV as formatted table
        _csv_table "$file"
        return
    fi

    # Check if col is a number or a header name
    if [[ "$col" =~ ^[0-9]+$ ]]; then
        _csv_extract_col_num "$file" "$col"
    else
        _csv_extract_col_name "$file" "$col"
    fi
}

_csv_table() {
    local file="$1"
    # Auto-detect delimiter
    local delim
    delim=$(_csv_detect_delim "$file")

    awk -F"$delim" '
    NR == 1 {
        for (i=1; i<=NF; i++) {
            headers[i] = $i
            maxw[i] = length($i)
        }
        ncols = NF
    }
    {
        for (i=1; i<=NF; i++) {
            data[NR][i] = $i
            if (length($i) > maxw[i]) maxw[i] = length($i)
        }
        nrows = NR
    }
    END {
        # Print header
        line = ""
        for (i=1; i<=ncols; i++) {
            if (i>1) line = line " | "
            line = line sprintf("%-*s", maxw[i], data[1][i])
        }
        print line

        # Print separator
        sep = ""
        for (i=1; i<=ncols; i++) {
            if (i>1) sep = sep "-+-"
            for (j=1; j<=maxw[i]; j++) sep = sep "-"
        }
        print sep

        # Print data
        for (r=2; r<=nrows; r++) {
            line = ""
            for (i=1; i<=ncols; i++) {
                if (i>1) line = line " | "
                line = line sprintf("%-*s", maxw[i], data[r][i])
            }
            print line
        }
        printf "\n(%d rows)\n", nrows - 1
    }
    ' "$file"
}

_csv_detect_delim() {
    local file="$1"
    local head
    head=$(head -1 "$file")

    local comma_count tab_count semi_count pipe_count
    comma_count=$(echo "$head" | tr -cd ',' | wc -c)
    tab_count=$(echo "$head" | tr -cd '\t' | wc -c)
    semi_count=$(echo "$head" | tr -cd ';' | wc -c)
    pipe_count=$(echo "$head" | tr -cd '|' | wc -c)

    local max=$comma_count
    local delim=","
    if [[ $tab_count -gt $max ]]; then max=$tab_count; delim=$'\t'; fi
    if [[ $semi_count -gt $max ]]; then max=$semi_count; delim=";"; fi
    if [[ $pipe_count -gt $max ]]; then delim="|"; fi

    echo "$delim"
}

_csv_extract_col_num() {
    local file="$1" col_num="$2"
    local delim
    delim=$(_csv_detect_delim "$file")
    awk -F"$delim" -v c="$col_num" '{ print $c }' "$file"
}

_csv_extract_col_name() {
    local file="$1" col_name="$2"
    local delim
    delim=$(_csv_detect_delim "$file")

    awk -F"$delim" -v name="$col_name" '
    NR == 1 {
        for (i=1; i<=NF; i++) {
            gsub(/^[ \t"]+|[ \t"]+$/, "", $i)
            if (tolower($i) == tolower(name)) {
                col = i
                break
            }
        }
        if (!col) { print "Column not found: " name > "/dev/stderr"; exit 1 }
    }
    { print $col }
    ' "$file"
}

# ── XML Parsing ──────────────────────────────────────────────────────────────

cmd_xml() {
    local file="${1:-}"
    local xpath="${2:-}"

    check_file "$file"
    command -v python3 &>/dev/null || die "python3 is required for XML parsing"

    python3 - "$file" "$xpath" <<'PYEOF'
import sys, xml.etree.ElementTree as ET

file_path = sys.argv[1]
xpath = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else ""

try:
    tree = ET.parse(file_path)
    root = tree.getroot()
except ET.ParseError as e:
    print(f"XML Parse Error: {e}", file=sys.stderr)
    sys.exit(1)

def elem_to_str(elem, indent=0):
    """Pretty print an element."""
    prefix = "  " * indent
    tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
    attrs = " ".join(f'{k}="{v}"' for k, v in elem.attrib.items())
    line = f"{prefix}<{tag}"
    if attrs:
        line += f" {attrs}"
    text = (elem.text or "").strip()
    children = list(elem)
    if not children and not text:
        print(f"{line} />")
    elif not children:
        print(f"{line}>{text}</{tag}>")
    else:
        print(f"{line}>")
        if text:
            print(f"{prefix}  {text}")
        for child in children:
            elem_to_str(child, indent + 1)
        print(f"{prefix}</{tag}>")

if not xpath:
    elem_to_str(root)
else:
    try:
        results = root.findall(xpath)
    except SyntaxError:
        # Try with .// prefix
        results = root.findall(".//" + xpath)
    if not results:
        print(f"No elements matched: {xpath}", file=sys.stderr)
        sys.exit(1)
    for r in results:
        if r.text and not list(r):
            print(r.text.strip())
        else:
            elem_to_str(r)
PYEOF
}

# ── YAML Parsing ─────────────────────────────────────────────────────────────

cmd_yaml() {
    local file="${1:-}"
    local key="${2:-}"

    check_file "$file"
    command -v python3 &>/dev/null || die "python3 is required for YAML parsing"

    python3 - "$file" "$key" <<'PYEOF'
import sys, json

file_path = sys.argv[1]
key_path = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else ""

try:
    import yaml
    with open(file_path) as f:
        data = yaml.safe_load(f)
except ImportError:
    # Fallback: simple YAML-ish parser for basic key:value files
    data = {}
    current = data
    indent_stack = [(0, data)]
    with open(file_path) as f:
        for line in f:
            stripped = line.rstrip()
            if not stripped or stripped.startswith('#'):
                continue
            indent = len(line) - len(line.lstrip())
            if ':' in stripped:
                k, _, v = stripped.partition(':')
                k = k.strip().strip('"').strip("'")
                v = v.strip().strip('"').strip("'")
                # Pop back to correct indent level
                while len(indent_stack) > 1 and indent <= indent_stack[-1][0]:
                    indent_stack.pop()
                parent = indent_stack[-1][1]
                if v:
                    parent[k] = v
                else:
                    parent[k] = {}
                    indent_stack.append((indent + 1, parent[k]))
except yaml.YAMLError as e:
    print(f"YAML Parse Error: {e}", file=sys.stderr)
    sys.exit(1)

if not key_path:
    print(json.dumps(data, indent=2, default=str))
else:
    parts = key_path.split('.')
    current = data
    for p in parts:
        if isinstance(current, dict):
            if p not in current:
                print(f"Key not found: {p} in path {key_path}", file=sys.stderr)
                sys.exit(1)
            current = current[p]
        elif isinstance(current, list):
            try:
                current = current[int(p)]
            except (ValueError, IndexError):
                print(f"Invalid index: {p}", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Cannot traverse into: {type(current).__name__}", file=sys.stderr)
            sys.exit(1)
    if isinstance(current, (dict, list)):
        print(json.dumps(current, indent=2, default=str))
    else:
        print(current)
PYEOF
}

# ── Line Filtering ───────────────────────────────────────────────────────────

cmd_lines() {
    local file="${1:-}"
    local pattern="${2:-}"

    check_file "$file"

    if [[ -z "$pattern" ]]; then
        # Show all lines with line numbers
        nl -ba "$file"
        echo ""
        echo "$(wc -l < "$file") total lines"
    else
        # Grep with context and line numbers
        local count
        count=$(grep -c "$pattern" "$file" 2>/dev/null || echo 0)
        echo "Pattern: $pattern"
        echo "Matches: $count"
        echo "━━━━━━━━━━━━━━━━━━━━"
        if [[ "$count" -gt 0 ]]; then
            grep -n --color=never -C 2 "$pattern" "$file" || true
        fi
    fi
}

# ── Split ────────────────────────────────────────────────────────────────────

cmd_split() {
    local file="${1:-}"
    local delimiter="${2:-}"

    check_file "$file"
    [[ -z "$delimiter" ]] && die "Usage: parser split <file> <delimiter>"

    echo "Split by: '$delimiter'"
    echo "━━━━━━━━━━━━━━━━━━━━"

    local line_num=0
    while IFS= read -r line; do
        ((line_num++))
        echo "Line $line_num:"
        local idx=0
        while IFS= read -r part; do
            ((idx++))
            echo "  [$idx] $part"
        done <<< "$(echo "$line" | awk -v d="$delimiter" '
            BEGIN { FS=d }
            { for(i=1;i<=NF;i++) print $i }
        ')"
    done < "$file"
}

# ── Extract ──────────────────────────────────────────────────────────────────

cmd_extract() {
    local file="${1:-}"
    local regex="${2:-}"

    check_file "$file"
    [[ -z "$regex" ]] && die "Usage: parser extract <file> <regex>"

    echo "Regex: $regex"
    echo "━━━━━━━━━━━━━━━━━━━━"

    local matches
    matches=$(grep -oP "$regex" "$file" 2>/dev/null || grep -oE "$regex" "$file" 2>/dev/null || true)

    if [[ -z "$matches" ]]; then
        echo "No matches found."
        return 1
    fi

    local count
    count=$(echo "$matches" | wc -l)
    echo "$matches"
    echo ""
    echo "($count matches)"
}

# ── File Stats ───────────────────────────────────────────────────────────────

cmd_stats() {
    local file="${1:-}"
    check_file "$file"

    local lines words chars bytes
    lines=$(wc -l < "$file")
    words=$(wc -w < "$file")
    chars=$(wc -m < "$file")
    bytes=$(wc -c < "$file")

    local file_type
    file_type=$(file -b "$file" 2>/dev/null || echo "unknown")

    local mime
    mime=$(file -b --mime-type "$file" 2>/dev/null || echo "unknown")

    # Encoding detection
    local encoding
    encoding=$(file -b --mime-encoding "$file" 2>/dev/null || echo "unknown")

    # Line ending detection
    local line_endings="Unix (LF)"
    if grep -qP '\r\n' "$file" 2>/dev/null; then
        line_endings="Windows (CRLF)"
    elif grep -qP '\r[^\n]' "$file" 2>/dev/null; then
        line_endings="Classic Mac (CR)"
    fi

    # Longest/shortest line
    local longest shortest
    longest=$(awk '{ if (length > max) max = length } END { print max }' "$file")
    shortest=$(awk 'NR==1 || length < min { min = length } END { print min }' "$file")

    # Blank lines
    local blank_lines
    blank_lines=$(grep -c '^[[:space:]]*$' "$file" 2>/dev/null || echo "0")

    echo "File Statistics: $(basename "$file")"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Type:           $file_type"
    echo "MIME:           $mime"
    echo "Encoding:       $encoding"
    echo "Line endings:   $line_endings"
    echo "Size:           $(numfmt --to=iec "$bytes" 2>/dev/null || echo "${bytes} bytes")"
    echo "Lines:          $lines"
    echo "Words:          $words"
    echo "Characters:     $chars"
    echo "Blank lines:    $blank_lines"
    echo "Longest line:   $longest chars"
    echo "Shortest line:  $shortest chars"
    echo "Avg line:       $(( chars / (lines > 0 ? lines : 1) )) chars"
}

# ── Main ─────────────────────────────────────────────────────────────────────

main() {
    local cmd="${1:-help}"
    shift 2>/dev/null || true

    case "$cmd" in
        json)    cmd_json "$@" ;;
        csv)     cmd_csv "$@" ;;
        xml)     cmd_xml "$@" ;;
        yaml)    cmd_yaml "$@" ;;
        lines)   cmd_lines "$@" ;;
        split)   cmd_split "$@" ;;
        extract) cmd_extract "$@" ;;
        stats)   cmd_stats "$@" ;;
        help|--help|-h) usage ;;
        version) echo "parser-tool v${VERSION}" ;;
        *)       die "Unknown command: $cmd. Run 'parser help' for usage." ;;
    esac
}

main "$@"
