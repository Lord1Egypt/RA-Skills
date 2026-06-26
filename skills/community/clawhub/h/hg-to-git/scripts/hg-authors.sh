#!/bin/bash
# hg-authors.sh - Extract and map Mercurial authors to Git format
# Usage: hg-authors.sh <hg-repo-path> [output-file]

set -e

HG_REPO="${1:-}"
OUTPUT="${2:-authors.map}"

if [ -z "$HG_REPO" ]; then
    echo "Usage: $0 <hg-repo-path> [output-file]"
    exit 1
fi

if [ ! -d "$HG_REPO/.hg" ]; then
    echo "Error: $HG_REPO is not a valid Mercurial repository"
    exit 1
fi

cd "$HG_REPO"

echo "Extracting authors from Mercurial repository..."
echo "Output: $OUTPUT"
echo ""

# Get unique authors and format for git
echo "# Mercurial to Git author mapping" > "$OUTPUT"
echo "# Format: \"Hg Author\"=\"Git Author <email>\"" >> "$OUTPUT"
echo "" >> "$OUTPUT"

hg log --template "{author}\n" | sort -u | while read author; do
    # Skip empty lines
    [ -z "$author" ] && continue
    
    # Try to extract email if present
    if [[ "$author" =~ <.*> ]]; then
        # Already has email format
        echo "\"$author\"=\"$author\"" >> "$OUTPUT"
    else
        # No email, create placeholder
        email="$(echo "$author" | tr '[:upper:]' '[:lower:]' | tr ' ' '.')@example.com"
        echo "\"$author\"=\"$author <$email>\"" >> "$OUTPUT"
    fi
done

echo "Author map created: $OUTPUT"
echo ""
echo "Please review and edit $OUTPUT before conversion."
echo "Change the email addresses to real ones."
echo ""
cat "$OUTPUT"
