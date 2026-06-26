#!/usr/bin/env bash
# Validate the structure and integrity of a knowledge-advisor knowledge base.
# Usage: validate-kb.sh [knowledge-base-directory]
# Default: ./knowledge-base

set -euo pipefail

TARGET="${1:-./knowledge-base}"
ERRORS=0
WARNINGS=0

echo "Validating knowledge base at $TARGET..."
echo ""

# Check KB exists
if [ ! -d "$TARGET" ]; then
    echo "ERROR: Knowledge base directory not found: $TARGET"
    exit 1
fi

# Check required root files
for file in _index.md _health.json _domains.json _cross-references.md; do
    if [ ! -f "$TARGET/$file" ]; then
        echo "ERROR: Missing required file: $file"
        ERRORS=$((ERRORS + 1))
    else
        echo "  OK: $file"
    fi
done

echo ""

# Check each book directory
BOOK_COUNT=0
for book_dir in "$TARGET"/*/; do
    [ -d "$book_dir" ] || continue
    book_name=$(basename "$book_dir")

    # Skip hidden directories
    [[ "$book_name" == .* ]] && continue

    BOOK_COUNT=$((BOOK_COUNT + 1))
    echo "Book: $book_name"

    # Check meta.json
    if [ ! -f "$book_dir/meta.json" ]; then
        echo "  ERROR: Missing meta.json"
        ERRORS=$((ERRORS + 1))
    else
        echo "  OK: meta.json"

        # Check required fields in meta.json
        for field in title authors language domains extraction_date; do
            if ! grep -q "\"$field\"" "$book_dir/meta.json"; then
                echo "  WARNING: meta.json missing field: $field"
                WARNINGS=$((WARNINGS + 1))
            fi
        done
    fi

    # Check content files
    for file in frameworks.md principles.md; do
        if [ ! -f "$book_dir/$file" ]; then
            echo "  WARNING: Missing $file (expected for most books)"
            WARNINGS=$((WARNINGS + 1))
        else
            # Check file is not empty
            if [ ! -s "$book_dir/$file" ]; then
                echo "  WARNING: $file is empty"
                WARNINGS=$((WARNINGS + 1))
            else
                echo "  OK: $file"
            fi
        fi
    done

    # Check optional files
    for file in mental-models.md anti-patterns.md case-studies.md; do
        if [ -f "$book_dir/$file" ]; then
            echo "  OK: $file"
        fi
    done

    # Check file sizes (warn if too large)
    TOTAL_WORDS=0
    for file in "$book_dir"/*.md "$book_dir"/*.json; do
        [ -f "$file" ] || continue
        WORDS=$(wc -w < "$file" 2>/dev/null || echo 0)
        TOTAL_WORDS=$((TOTAL_WORDS + WORDS))
    done

    EST_TOKENS=$((TOTAL_WORDS * 13 / 10))
    if [ "$EST_TOKENS" -gt 8000 ]; then
        echo "  WARNING: Book exceeds 8,000 estimated tokens ($EST_TOKENS). Consider condensing."
        WARNINGS=$((WARNINGS + 1))
    elif [ "$EST_TOKENS" -gt 6000 ]; then
        echo "  INFO: Book is large ($EST_TOKENS estimated tokens)."
    fi

    echo ""
done

# Check index size
if [ -f "$TARGET/_index.md" ]; then
    INDEX_WORDS=$(wc -w < "$TARGET/_index.md")
    INDEX_TOKENS=$((INDEX_WORDS * 13 / 10))
    echo "Index: ~$INDEX_TOKENS estimated tokens"
    if [ "$INDEX_TOKENS" -gt 3000 ]; then
        echo "  WARNING: Index exceeds 3,000 tokens. Consider domain sub-indexes (V1.5)."
        WARNINGS=$((WARNINGS + 1))
    elif [ "$INDEX_TOKENS" -gt 2500 ]; then
        echo "  INFO: Index approaching token limit."
    fi
fi

# Check encoding (UTF-8)
NON_UTF8=$(find "$TARGET" -type f \( -name "*.md" -o -name "*.json" \) -exec file {} \; | grep -v "UTF-8\|ASCII\|empty" | head -5)
if [ -n "$NON_UTF8" ]; then
    echo ""
    echo "WARNING: Non-UTF-8 files detected:"
    echo "$NON_UTF8"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "=============================="
echo "Validation complete"
echo "Books: $BOOK_COUNT"
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"

if [ "$ERRORS" -gt 0 ]; then
    echo "STATUS: FAILED — fix errors before using the knowledge base"
    exit 1
elif [ "$WARNINGS" -gt 0 ]; then
    echo "STATUS: PASSED with warnings"
    exit 0
else
    echo "STATUS: PASSED"
    exit 0
fi
