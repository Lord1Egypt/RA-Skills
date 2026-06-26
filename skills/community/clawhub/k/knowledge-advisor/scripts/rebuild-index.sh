#!/usr/bin/env bash
# Rebuild knowledge base index files from existing book directories.
# Regenerates: _index.md, _health.json, _domains.json
# Does NOT regenerate: _cross-references.md (requires LLM for semantic analysis)
#
# Usage: rebuild-index.sh [knowledge-base-directory]
# Default: ./knowledge-base
#
# Use cases:
#   - After importing a book folder from another instance
#   - After manually editing meta.json files
#   - To fix index drift or corruption

set -euo pipefail

TARGET="${1:-./knowledge-base}"
TODAY=$(date +%Y-%m-%d)

if [ ! -d "$TARGET" ]; then
    echo "ERROR: Knowledge base directory not found: $TARGET"
    exit 1
fi

echo "Rebuilding index files from book directories in $TARGET..."
echo ""

# --- Collect book data ---

BOOK_COUNT=0
TOTAL_FRAMEWORKS=0
TOTAL_PRINCIPLES=0
TOTAL_MENTAL_MODELS=0
TOTAL_ANTI_PATTERNS=0
TOTAL_CASE_STUDIES=0
TOTAL_BOOK_WORDS=0
LARGEST_BOOK_WORDS=0
LARGEST_BOOK=""
LANGUAGES=""
ALL_DOMAINS=""

INDEX_TABLE=""
DOMAIN_JSON_ENTRIES=""

for book_dir in "$TARGET"/*/; do
    [ -d "$book_dir" ] || continue
    book_slug=$(basename "$book_dir")
    [[ "$book_slug" == .* ]] && continue

    meta="$book_dir/meta.json"
    if [ ! -f "$meta" ]; then
        echo "  SKIP: $book_slug (no meta.json)"
        continue
    fi

    BOOK_COUNT=$((BOOK_COUNT + 1))

    # Extract fields from meta.json using grep/sed (no jq dependency)
    title=$(grep -o '"title": *"[^"]*"' "$meta" | head -1 | sed 's/"title": *"\(.*\)"/\1/' || echo "Unknown")
    authors=$(grep -o '"authors": *\[[^]]*\]' "$meta" | sed 's/"authors": *\[//;s/\]//;s/"//g;s/,/, /g' | xargs || echo "Unknown")
    language=$(grep -o '"language": *"[^"]*"' "$meta" | sed 's/"language": *"\(.*\)"/\1/' || echo "en")
    domains=$(grep -o '"domains": *\[[^]]*\]' "$meta" | sed 's/"domains": *\[//;s/\]//;s/"//g;s/ //g' || echo "")
    domains_display=$(echo "$domains" | tr ',' ', ')

    fw_count=$(grep -o '"framework_count": *[0-9]*' "$meta" | grep -o '[0-9]*' || echo 0)
    pr_count=$(grep -o '"principle_count": *[0-9]*' "$meta" | grep -o '[0-9]*' || echo 0)
    mm_count=$(grep -o '"mental_model_count": *[0-9]*' "$meta" | grep -o '[0-9]*' || echo 0)
    ap_count=$(grep -o '"anti_pattern_count": *[0-9]*' "$meta" | grep -o '[0-9]*' || echo 0)
    cs_count=$(grep -o '"case_study_count": *[0-9]*' "$meta" | grep -o '[0-9]*' || echo 0)

    TOTAL_FRAMEWORKS=$((TOTAL_FRAMEWORKS + fw_count))
    TOTAL_PRINCIPLES=$((TOTAL_PRINCIPLES + pr_count))
    TOTAL_MENTAL_MODELS=$((TOTAL_MENTAL_MODELS + mm_count))
    TOTAL_ANTI_PATTERNS=$((TOTAL_ANTI_PATTERNS + ap_count))
    TOTAL_CASE_STUDIES=$((TOTAL_CASE_STUDIES + cs_count))

    # Calculate book word count
    BOOK_WORDS=0
    for file in "$book_dir"/*.md "$book_dir"/*.json; do
        [ -f "$file" ] || continue
        WORDS=$(wc -w < "$file" 2>/dev/null || echo 0)
        BOOK_WORDS=$((BOOK_WORDS + WORDS))
    done
    TOTAL_BOOK_WORDS=$((TOTAL_BOOK_WORDS + BOOK_WORDS))

    if [ "$BOOK_WORDS" -gt "$LARGEST_BOOK_WORDS" ]; then
        LARGEST_BOOK_WORDS=$BOOK_WORDS
        LARGEST_BOOK=$book_slug
    fi

    # Track languages
    if ! echo "$LANGUAGES" | grep -q "$language"; then
        if [ -n "$LANGUAGES" ]; then
            LANGUAGES="$LANGUAGES, $language"
        else
            LANGUAGES="$language"
        fi
    fi

    # Build index table row
    INDEX_TABLE="${INDEX_TABLE}| ${title} (${authors}) | ${domains_display} | ${fw_count} | ${language} |\n"

    # Collect domains for _domains.json
    IFS=',' read -ra DOMAIN_ARRAY <<< "$domains"
    for d in "${DOMAIN_ARRAY[@]}"; do
        d=$(echo "$d" | xargs)
        [ -z "$d" ] && continue
        ALL_DOMAINS="${ALL_DOMAINS}${d}=${title}\n"
    done

    echo "  OK: $book_slug ($title)"
done

echo ""

if [ "$BOOK_COUNT" -eq 0 ]; then
    echo "No books found. Index files will reflect an empty knowledge base."
fi

# --- Rebuild _index.md ---

LANG_LIST=$(echo "$LANGUAGES" | sed 's/^ *//')
[ -z "$LANG_LIST" ] && LANG_LIST="none"

cat > "$TARGET/_index.md" << EOF
# Knowledge Base Index

Last updated: $TODAY | Books: $BOOK_COUNT | Frameworks: $TOTAL_FRAMEWORKS | Languages: $LANG_LIST

## Books

| Title | Domains | Frameworks | Lang |
|-------|---------|------------|------|
$(echo -e "$INDEX_TABLE")
## Application Trigger Index

<!-- Run the skill's 'sync' action to rebuild trigger index from book content -->
<!-- Or manually add triggers following the format below -->
<!-- ### [situation phrase] -->
<!-- → [Framework] ([Book]), [Principle] ([Book]) -->
EOF

echo "  Written: _index.md"

# --- Rebuild _health.json ---

if [ "$BOOK_COUNT" -gt 0 ]; then
    AVG_BOOK_TOKENS=$((TOTAL_BOOK_WORDS * 13 / 10 / BOOK_COUNT))
    LARGEST_BOOK_TOKENS=$((LARGEST_BOOK_WORDS * 13 / 10))
else
    AVG_BOOK_TOKENS=0
    LARGEST_BOOK_TOKENS=0
fi

INDEX_WORDS=$(wc -w < "$TARGET/_index.md" 2>/dev/null || echo 0)
INDEX_TOKENS=$((INDEX_WORDS * 13 / 10))

DOMAIN_COUNT=$(echo -e "$ALL_DOMAINS" | sed '/^$/d' | cut -d= -f1 | sort -u | wc -l)

LANG_JSON=$(echo "$LANGUAGES" | sed 's/^ *//;s/ *$//' | tr ',' '\n' | sed 's/^ *//;s/ *$//' | sed 's/.*/"&"/' | tr '\n' ',' | sed 's/,$//')
[ -z "$LANG_JSON" ] && LANG_JSON=""

# Determine scaling warnings
SCALING_WARNINGS="[]"
SCALING_PHASE="V1"
if [ "$BOOK_COUNT" -ge 50 ]; then
    SCALING_PHASE="V1.5"
    SCALING_WARNINGS='["Reached V1.5 limit. Upgrade to V2 (SQLite search layer)."]'
elif [ "$BOOK_COUNT" -ge 30 ]; then
    SCALING_PHASE="V1"
    SCALING_WARNINGS='["Reached V1 recommended max. Upgrade to V1.5 (domain sub-indexes)."]'
elif [ "$BOOK_COUNT" -ge 25 ]; then
    SCALING_WARNINGS='["Approaching V1 limit. Plan for V1.5 soon."]'
fi

cat > "$TARGET/_health.json" << EOF
{
  "last_check": "$TODAY",
  "book_count": $BOOK_COUNT,
  "total_frameworks": $TOTAL_FRAMEWORKS,
  "total_principles": $TOTAL_PRINCIPLES,
  "index_estimated_tokens": $INDEX_TOKENS,
  "avg_book_tokens": $AVG_BOOK_TOKENS,
  "largest_book_tokens": $LARGEST_BOOK_TOKENS,
  "largest_book": "$LARGEST_BOOK",
  "domains": $DOMAIN_COUNT,
  "languages": [$LANG_JSON],
  "scaling_phase": "$SCALING_PHASE",
  "scaling_warnings": $SCALING_WARNINGS,
  "last_ingestion": "$TODAY"
}
EOF

echo "  Written: _health.json"

# --- Rebuild _domains.json ---

{
    echo "{"
    echo '  "domains": {'

    FIRST_DOMAIN=true
    while read -r domain; do
        [ -z "$domain" ] && continue
        books=$(echo -e "$ALL_DOMAINS" | grep "^${domain}=" | cut -d= -f2 | sort -u | sed 's/.*/"&"/' | tr '\n' ',' | sed 's/,$//')
        count=$(echo -e "$ALL_DOMAINS" | grep "^${domain}=" | cut -d= -f2 | sort -u | wc -l)

        if [ "$FIRST_DOMAIN" = true ]; then
            FIRST_DOMAIN=false
        else
            echo ","
        fi
        printf '    "%s": {\n      "books": [%s],\n      "count": %d\n    }' "$domain" "$books" "$count"
    done < <(echo -e "$ALL_DOMAINS" | sed '/^$/d' | cut -d= -f1 | sort -u)

    echo ""
    echo "  }"
    echo "}"
} > "$TARGET/_domains.json"

echo "  Written: _domains.json"

# --- Summary ---

echo ""
echo "=============================="
echo "Rebuild complete"
echo "Books: $BOOK_COUNT"
echo "Frameworks: $TOTAL_FRAMEWORKS | Principles: $TOTAL_PRINCIPLES"
echo "Domains: $DOMAIN_COUNT | Languages: $LANG_LIST"
echo "Index: ~$INDEX_TOKENS estimated tokens"
echo ""
echo "NOTE: _cross-references.md was NOT rebuilt (requires LLM analysis)."
echo "NOTE: Application Trigger Index in _index.md has placeholder comments."
echo "Run the skill's 'sync' action to rebuild triggers and cross-references."
