#!/bin/bash
# Full-text index management for offline search
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

case "$1" in
  fetch)
    shift
    parse_version_flag "$@"
    REF="$VERSION"
    [ "$VERSION" = "latest" ] && REF="main"

    echo "Downloading all docs..."

    DOCS_JSON_CACHE="${VERSION_CACHE_DIR}/docs.json"

    # Fetch docs.json if not cached or stale
    if ! is_cache_fresh "$DOCS_JSON_CACHE" "$DOC_TTL"; then
      if [[ "$SOURCE" == local:* ]]; then
        local_path="${SOURCE#local:}"
        if [ ! -f "${local_path}/docs.json" ]; then
          echo "Error: docs.json not found at ${local_path}/docs.json" >&2
          exit 1
        fi
        cp "${local_path}/docs.json" "$DOCS_JSON_CACHE"
      else
        if ! check_online; then
          echo "Offline: cannot reach GitHub" >&2
          exit 1
        fi
        src_url="$(resolve_source_raw "docs.json" "$REF")"
        if ! curl -sf --max-time 10 "$src_url" -o "$DOCS_JSON_CACHE" 2>/dev/null; then
          echo "Error: failed to fetch docs.json" >&2
          exit 1
        fi
      fi
    fi

    # Extract all doc paths from docs.json navigation tree
    PATHS=$(python3 - "$DOCS_JSON_CACHE" <<'PYEOF'
import sys, json

def collect_pages(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, list):
        for item in node:
            yield from collect_pages(item)
    elif isinstance(node, dict):
        if 'pages' in node:
            yield from collect_pages(node['pages'])
        else:
            for v in node.values():
                yield from collect_pages(v)

with open(sys.argv[1]) as f:
    data = json.load(f)

paths = sorted(set(
    p for p in collect_pages(data.get('navigation', {}))
    if isinstance(p, str) and '/' in p
))
for p in paths:
    print(p)
PYEOF
)

    if [ -z "$PATHS" ]; then
      echo "Error: Could not extract doc paths from docs.json" >&2
      exit 1
    fi

    total=$(printf '%s\n' "$PATHS" | wc -l)
    fetch_jobs="$FETCH_JOBS"
    if ! [[ "$fetch_jobs" =~ ^[0-9]+$ ]] || [ "$fetch_jobs" -le 0 ]; then
      fetch_jobs=8
    fi
    new=0
    fetch_sequential() {
      while IFS= read -r path; do
        [ -z "$path" ] && continue
        safe=$(echo "$path" | tr "/" "_")
        txt_file="${VERSION_CACHE_DIR}/doc_${safe}.txt"
        if [ ! -f "$txt_file" ] || ! is_cache_fresh "$txt_file" "$DOC_TTL"; then
          if fetch_markdown "$safe" "$REF"; then
            new=$((new + 1))
            echo "  [done] $path" >&2
          fi
          sleep 0.3
        fi
      done <<< "$PATHS"
    }

    if command -v xargs &>/dev/null; then
      MARKER_DIR=$(mktemp -d)
      trap 'rm -rf "$MARKER_DIR"' EXIT
      export OPENCLAW_SAGE_CACHE_DIR OPENCLAW_SAGE_SOURCE OPENCLAW_SAGE_DOC_TTL OPENCLAW_SAGE_LANGS
      export LIB_SH="$SCRIPT_DIR/lib.sh" MARKER_DIR VERSION_CACHE_DIR REF

      if echo "$PATHS" | tr '\n' '\0' | xargs -0 -n 1 -P "$fetch_jobs" bash -c '
          source "$LIB_SH"
          path="$1"
          [ -z "$path" ] && exit 0
          safe=$(echo "$path" | tr "/" "_")
          txt_file="${VERSION_CACHE_DIR}/doc_${safe}.txt"
          if [ ! -f "$txt_file" ] || ! is_cache_fresh "$txt_file" "$DOC_TTL"; then
            if fetch_markdown "$safe" "$REF"; then
              touch "${MARKER_DIR}/${safe}"
              echo "  [done] $path" >&2
            fi
            sleep 0.3
          fi
        ' --; then
        set -- "$MARKER_DIR"/*
        if [ -e "$1" ]; then
          new=$#
        fi
      else
        echo "xargs unavailable or failed; falling back to sequential fetch." >&2
        new=0
        fetch_sequential
      fi
      trap - EXIT
      rm -rf "$MARKER_DIR"
    else
      echo "xargs not available; falling back to sequential fetch." >&2
      fetch_sequential
    fi

    cached=$(ls "$VERSION_CACHE_DIR"/doc_*.txt 2>/dev/null | wc -l)
    echo "Done. $new new docs fetched, $cached total cached."
    echo "Next: run './scripts/build-index.sh build' to index them."
    ;;

  build)
    shift
    parse_version_flag "$@"
    INDEX_FILE="${VERSION_CACHE_DIR}/index.txt"
    META_FILE="${VERSION_CACHE_DIR}/index_meta.json"

    echo "Building search index..."
    if ! ls "$VERSION_CACHE_DIR"/doc_*.txt &>/dev/null 2>&1; then
      echo "No docs cached. Run: ./scripts/build-index.sh fetch first."
      exit 1
    fi

    TMP_INDEX=$(mktemp)
    CURRENT_PATHS=$(mktemp)
    CHANGED_PATHS=$(mktemp)
    UNCHANGED_PATHS=$(mktemp)
    INDEXED_PATHS=$(mktemp)
    trap 'rm -f "$TMP_INDEX" "$CURRENT_PATHS" "$CHANGED_PATHS" "$UNCHANGED_PATHS" "$INDEXED_PATHS"' EXIT

    append_doc_lines() {
      local doc_file="$1" out_file="$2" path
      path=$(basename "$doc_file" .txt | sed 's/^doc_//; s/_/\//g')
      grep -v '^[[:space:]]*$' "$doc_file" | while IFS= read -r line; do
        echo "${path}|${line}"
      done >> "$out_file"
    }

    doc_count=0
    changed_count=0
    index_exists=false
    [ -f "$INDEX_FILE" ] && index_exists=true
    if $index_exists; then
      index_mtime=$(get_mtime "$INDEX_FILE")
    fi

    for f in "$VERSION_CACHE_DIR"/doc_*.txt; do
      path=$(basename "$f" .txt | sed 's/^doc_//; s/_/\//g')
      echo "$path" >> "$CURRENT_PATHS"
      doc_count=$((doc_count + 1))
      if ! $index_exists || [ "$(get_mtime "$f")" -gt "$index_mtime" ]; then
        echo "$path" >> "$CHANGED_PATHS"
        changed_count=$((changed_count + 1))
      else
        echo "$path" >> "$UNCHANGED_PATHS"
      fi
    done

    removed_count=0
    if $index_exists; then
      awk -F'|' '!seen[$1]++ { print $1 }' "$INDEX_FILE" > "$INDEXED_PATHS"
      removed_count=$(awk '
        NR==FNR { current[$0]=1; next }
        !($0 in current) { removed++ }
        END { print removed + 0 }
      ' "$CURRENT_PATHS" "$INDEXED_PATHS")
    fi

    if $index_exists && [ "$changed_count" -eq 0 ] && [ "$removed_count" -eq 0 ]; then
      line_count=$(wc -l < "$INDEX_FILE")
      echo "Index already up to date: $doc_count docs, $line_count lines."
    else
      : > "$TMP_INDEX"
      if $index_exists && [ -s "$INDEX_FILE" ] && [ -s "$UNCHANGED_PATHS" ]; then
        awk -F'|' '
          NR==FNR { keep[$0]=1; next }
          ($1 in keep) { print }
        ' "$UNCHANGED_PATHS" "$INDEX_FILE" >> "$TMP_INDEX"
      fi

      for f in "$VERSION_CACHE_DIR"/doc_*.txt; do
        path=$(basename "$f" .txt | sed 's/^doc_//; s/_/\//g')
        if ! $index_exists || grep -Fxq "$path" "$CHANGED_PATHS"; then
          append_doc_lines "$f" "$TMP_INDEX"
        fi
      done

      mv "$TMP_INDEX" "$INDEX_FILE"
      line_count=$(wc -l < "$INDEX_FILE")
      echo "Index built: $doc_count docs, $line_count lines."
    fi

    if command -v python3 &>/dev/null; then
      echo "Building BM25 meta..." >&2
      python3 "$SCRIPT_DIR/bm25_search.py" build-meta "$INDEX_FILE" || {
        echo "Error: build-meta failed" >&2
        exit 1
      }
    fi

    echo "Location: $INDEX_FILE"
    echo "Search with: ./scripts/build-index.sh search <query>"
    ;;

  search)
    shift
    parse_version_flag "$@"
    set -- "${REMAINING_ARGS[@]}"
    INDEX_FILE="${VERSION_CACHE_DIR}/index.txt"

    MAX_RESULTS=10
    QUERY_ARGS=()
    while [ $# -gt 0 ]; do
      case "$1" in
        --max-results)
          shift
          if [ -z "$1" ] || ! [[ "$1" =~ ^[0-9]+$ ]] || [ "$1" -le 0 ]; then
            echo "Usage: build-index.sh search [--max-results N] <query>"
            exit 1
          fi
          MAX_RESULTS="$1"
          ;;
        *)
          QUERY_ARGS+=("$1")
          ;;
      esac
      shift
    done
    QUERY="${QUERY_ARGS[*]}"
    if [ -z "$QUERY" ]; then
      echo "Usage: build-index.sh search [--max-results N] <query>"
      exit 1
    fi

    if [ ! -f "$INDEX_FILE" ]; then
      echo "No index found. Run:"
      echo "  ./scripts/build-index.sh fetch"
      echo "  ./scripts/build-index.sh build"
      exit 1
    fi

    echo "Search results for: $QUERY"
    echo ""

    if command -v python3 &>/dev/null; then
      python3 "$SCRIPT_DIR/bm25_search.py" search "$INDEX_FILE" "$QUERY" "$MAX_RESULTS" \
        | while IFS='|' read -r score path excerpt; do
            score=$(echo "$score" | tr -d ' ')
            path=$(echo "$path" | tr -d ' ')
            excerpt=$(echo "$excerpt" | sed 's/^[[:space:]]*//')
            echo "  [$score] $path  ->  ${DOCS_BASE_URL}/$path"
            echo "          $excerpt"
            echo ""
          done
    else
      # grep fallback when python3 unavailable
      grep -i "$QUERY" "$INDEX_FILE" \
        | awk -F'|' -v base_url="$DOCS_BASE_URL" '
            {
              if ($1 != prev) {
                if (prev != "") print ""
                print "  [---] " $1 "  ->  " base_url "/" $1
                prev = $1
                count = 0
              }
              if (count < 4) {
                gsub(/^[[:space:]]+/, "", $2)
                print "        " $2
                count++
              }
            }
          ' \
        | head -"$((MAX_RESULTS * 4))"
      echo ""
      echo "Note: Install python3 for ranked BM25 results."
    fi

    match_count=$(grep -ic "$QUERY" "$INDEX_FILE" 2>/dev/null || echo 0)
    echo "($match_count matching lines across all docs)"
    ;;

  status)
    parse_version_flag "$@"
    doc_count=$(ls "$VERSION_CACHE_DIR"/doc_*.txt 2>/dev/null | wc -l)
    INDEX_FILE="${VERSION_CACHE_DIR}/index.txt"
    echo "Cached docs: $doc_count"
    if [ -f "$INDEX_FILE" ]; then
      line_count=$(wc -l < "$INDEX_FILE")
      echo "Index:       $line_count lines  ($INDEX_FILE)"
      META_FILE="${VERSION_CACHE_DIR}/index_meta.json"
      if [ -f "$META_FILE" ]; then
        echo "BM25 meta:   present"
      else
        echo "BM25 meta:   not built (run 'build' to generate)"
      fi
    else
      echo "Index:       not built"
    fi
    ;;

  *)
    echo "Usage: build-index.sh {fetch|build|search [--max-results N] <query>|status}"
    ;;
esac
