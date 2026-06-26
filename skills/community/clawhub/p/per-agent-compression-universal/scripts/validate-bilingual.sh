#!/bin/bash
# Bilingual Completeness Validator for CHANGELOG.md
# Part of SKILL_RELEASE_SOP.md

set -e

CHANGELOG="CHANGELOG.md"

if [ ! -f "$CHANGELOG" ]; then
  echo "❌ CHANGELOG.md not found in current directory"
  exit 1
fi

echo "🔍 Validating bilingual completeness in $CHANGELOG..."

# Count English version entries (lines starting with ## [X.Y.Z])
en_count=$(grep -cE '^## \[[0-9.]+' "$CHANGELOG" || echo 0)
# Count Chinese section markers ( ( Chinese ) )
zh_count=$(grep -c "( Chinese )" "$CHANGELOG" || echo 0)

if [ "$en_count" -ne "$zh_count" ]; then
  echo "❌ Mismatch: $en_count English version entries, $zh_count Chinese sections"
  exit 1
fi

echo "✅ Entry count matches: $en_count English, $zh_count Chinese"

# Validate each Chinese section has substantial content (> 100 chars)
failed=0
current_version=""
in_chinese_section=0
content=""

while IFS= read -r line; do
  # Detect start of English version entry
  if [[ $line =~ ^\[.*\]$ ]] || [[ $line =~ ^##\ \[[0-9.]+ ]]; then
    # Process previous section if we were in one
    if [ $in_chinese_section -eq 1 ] && [ -n "$content" ]; then
      len=${#content}
      if [ "$len" -lt 100 ]; then
        echo "❌ Chinese section for $current_version is too short ($len chars). Likely incomplete translation."
        failed=1
      fi
    fi
    # Reset for new section
    current_version=$(echo "$line" | grep -oE '\[[0-9.]+\]' | tr -d '[]')
    in_chinese_section=0
    content=""
    continue
  fi

  # Detect Chinese section marker
  if [[ $line == *"( Chinese )"* ]] || [[ $line =~ ^\(+\s*Chinese\s*\)+$ ]]; then
    in_chinese_section=1
    content=""
    continue
  fi

  # If we're inside a Chinese section, accumulate content
  if [ $in_chinese_section -eq 1 ]; then
    # Stop if we hit another section header
    if [[ $line =~ ^##\ \[ ]] || [[ $line =~ ^\[.*\]$ ]]; then
      in_chinese_section=0
      continue
    fi
    content+="$line"$'\n'
  fi
done < "$CHANGELOG"

# Check last section if still in Chinese
if [ $in_chinese_section -eq 1 ] && [ -n "$content" ]; then
  len=${#content}
  if [ "$len" -lt 100 ]; then
    echo "❌ Chinese section for $current_version is too short ($len chars). Likely incomplete translation."
    failed=1
  fi
fi

if [ $failed -eq 0 ]; then
  echo "✅ All Chinese sections exceed minimum length threshold (100 chars)"
  exit 0
else
  exit 1
fi
