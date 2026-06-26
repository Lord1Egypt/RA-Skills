#!/usr/bin/env bash
# Builds a compressed persona.md per legend by extracting only the sections
# that drive voice fidelity in office-hours sessions:
#   - Identity: first paragraph only (one-line bio)
#   - Soul: beliefs, frustrations, heuristics, what excites (skip intros)
#   - Skills: lenses, pattern recognition, analogies (skip domain lists)
#   - Voice: signature phrases, cadence, criticism/praise, opening line
#
# Biographical background, public presence, and track-record fluff are dropped
# because they don't change how the legend talks in a session.
#
# Run from repo root: bash scripts/build-persona.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PERSONAS="$ROOT/personas"

# Extract everything from a "## <heading>" line until the next "## " or EOF.
# Args: $1=file, $2=heading pattern (regex, case-insensitive)
extract_section() {
  local file="$1" pattern="$2"
  awk -v pat="$pattern" '
    BEGIN { IGNORECASE = 1; printing = 0 }
    /^## / {
      if ($0 ~ pat) { printing = 1; print; next }
      else if (printing) { printing = 0 }
    }
    printing { print }
  ' "$file"
}

# First non-empty, non-heading paragraph (for identity one-liner).
first_paragraph() {
  awk '
    /^#/ { next }
    /^[[:space:]]*$/ { if (found) exit; else next }
    { found=1; print }
  ' "$1"
}

compress_legend() {
  local dir="$1" name="$2" out="$dir/persona.md"
  {
    printf '# %s\n\n' "$name"

    if [ -f "$dir/identity.md" ]; then
      first_paragraph "$dir/identity.md"
      printf '\n'
    fi

    if [ -f "$dir/soul.md" ]; then
      extract_section "$dir/soul.md" '(beliefs|frustrat|heuristic|excite|cares)'
    fi

    if [ -f "$dir/skills.md" ]; then
      extract_section "$dir/skills.md" '(lens|pattern|analog)'
    fi

    if [ -f "$dir/voice.md" ]; then
      extract_section "$dir/voice.md" '(signature|cadence|criticism|praise|opening|never|humor)'
    fi

    # Collapse >1 blank lines into 1
    :
  } | awk 'BEGIN{blank=0} /^[[:space:]]*$/{blank++; if(blank<=1)print; next} {blank=0; print}' > "$out"
}

printf '%-24s %8s  %8s  %s\n' legend full lite reduction
printf '%-24s %8s  %8s  %s\n' ------ ---- ---- ---------
for dir in "$PERSONAS"/*/; do
  name="$(basename "$dir")"
  [ "$name" = "_TEMPLATE" ] && continue

  full=$(cat "$dir"identity.md "$dir"soul.md "$dir"skills.md "$dir"voice.md 2>/dev/null | wc -c)
  compress_legend "$dir" "$name"
  lite=$(wc -c < "$dir/persona.md")
  pct=$(( (full - lite) * 100 / full ))
  printf '%-24s %8d  %8d  -%d%%\n' "$name" "$full" "$lite" "$pct"
done
