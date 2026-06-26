#!/usr/bin/env bash
# wiki-lint.sh — Lint the wiki (all checks by default, --fix to auto-correct)
#
# Usage:
#   bash wiki-lint.sh <vault-path>          # check all (like eslint)
#   bash wiki-lint.sh <vault-path> --fix    # check all + auto-fix what's fixable
#                                            # (wikilink format, markdown structure,
#                                            #  and unlinked mentions via crosslink)
#   bash wiki-lint.sh <vault-path> --help
#
# Checks:
#   1. Frontmatter completeness
#   2. Broken wikilinks        [via wiki-lint-links.py — authoritative resolver]
#   3. Orphan pages            [via wiki-lint-links.py — authoritative resolver]
#   4. Stale pages
#   5. Tag drift
#   6. Wikilink format         [fixable via wiki-lint-links.py]
#   7. Markdown structure      [fixable via markdownlint-cli2]
#   8. Unlinked mentions      [advisory, via wiki-crosslink.py]
#
# No set -e: grep returns 1 on no-match which is normal control flow here.
set -o pipefail

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  echo "Usage: bash wiki-lint.sh <vault-path> [--fix]"
  echo "Lint the wiki. All checks run by default."
  echo "  --fix    Auto-correct fixable issues (wikilink format, markdown structure)"
  exit 0
fi

# Parse args
export LC_ALL=C
. "$(dirname "$0")/lib.sh"
FIX_MODE=false
VAULT=""
for arg in "$@"; do
  case "$arg" in
    --fix) FIX_MODE=true ;;
    --help|-h) echo "Usage: bash wiki-lint.sh <vault-path> [--fix]"; exit 0 ;;
    --*) echo "Error: unknown option '$arg'. Use --help for usage." >&2; exit 2 ;;
    *) [ -z "$VAULT" ] && VAULT="$arg" ;;
  esac
done
[ -z "$VAULT" ] && { echo "Usage: wiki-lint.sh <vault-path> [--fix]" >&2; exit 2; }

WIKI="$VAULT/wiki"
[ -d "$WIKI" ] || { echo "Error: $WIKI not found" >&2; exit 1; }
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Track skipped checks for honest summary
skipped_checks=""
mark_skipped() {
  skipped_checks="${skipped_checks:+$skipped_checks, }$1"
}

# Check python3 availability once
HAS_PYTHON3=false
command -v python3 >/dev/null 2>&1 && HAS_PYTHON3=true
$HAS_PYTHON3 || echo "Warning: python3 not found — some checks will be skipped" >&2

echo "=== Wiki Lint Report ==="
echo "Vault: $VAULT"
echo "Date:  $(date '+%Y-%m-%d %H:%M')"
echo ""

# Temp files used across checks
_lint_out=""
_lint_err=""
_mdl_tmp=""
STALE_LOG=$(mktemp)
DRIFT_LOG=$(mktemp)
CANONICAL_FILE=""
MDL_LOG=$(mktemp)

# --- Find wiki content pages (excludes index.md and log.md at wiki root) ---
CONTENT_PAGES=$(mktemp)
find "$WIKI" -type f -name '*.md' -print 2>/dev/null | grep -xFv "$WIKI/index.md" | grep -xFv "$WIKI/log.md" | sort > "$CONTENT_PAGES"
find_content_pages() { cat "$CONTENT_PAGES"; }

trap 'rm -f "$CONTENT_PAGES" "$_lint_out" "$_lint_err" "$_mdl_tmp" "$STALE_LOG" "$DRIFT_LOG" "$CANONICAL_FILE" "$MDL_LOG" "${_xl_out:-}" "${_xl_err:-}" 2>/dev/null' EXIT

# ── 1. Missing / Incomplete Frontmatter ───────────────────
echo "## Frontmatter"
fm_count=0
while IFS= read -r file; do
  first=$(head -1 "$file" 2>/dev/null | tr -d '\r' || true)
  if [ "$first" != "---" ]; then
    echo "  ⚠️  ${file#"$VAULT"/} — no frontmatter"
    fm_count=$((fm_count + 1))
  else
    fm=$(get_frontmatter "$file")
    for field in title type tags sources created updated; do
      if ! echo "$fm" | grep -q "^${field}:"; then
        echo "  ⚠️  ${file#"$VAULT"/} — missing field: $field"
        fm_count=$((fm_count + 1))
      fi
    done
    # Validate type value (only if type field exists — absence already reported above)
    _type=$(get_field "$file" type)
    if [ -n "$_type" ]; then
      case "$_type" in
        entity|concept|synthesis|source|report|index|log) ;;
        *) echo "  ⚠️  ${file#"$VAULT"/} — invalid type: $_type"; fm_count=$((fm_count + 1)) ;;
      esac
    fi
  fi
done < <(find_content_pages)
[ "$fm_count" -eq 0 ] && echo "  ✅ All pages have complete frontmatter"
echo ""

# ── 2–3 & 6. Broken links, Orphans, Wikilink format ──────
# All three checks use the authoritative resolver in wiki-lint-links.py.
# This eliminates the old heuristic shell-side resolution that diverged on
# aliases and lossy normalization.
echo "## Broken Wikilinks"
broken_count=0
orphan_count=0
fmt_count=0

LINK_SCRIPT="$SKILL_DIR/scripts/wiki-lint-links.py"
if $HAS_PYTHON3 && [ -f "$LINK_SCRIPT" ]; then
  _lint_args="--lint"
  $FIX_MODE && _lint_args="--lint --fix"

  _lint_out=$(mktemp)
  _lint_err=$(mktemp)
  # shellcheck disable=SC2086
  python3 "$LINK_SCRIPT" "$VAULT" $_lint_args > "$_lint_out" 2>"$_lint_err"
  _lint_rc=$?
  [ -s "$_lint_err" ] && sed 's/^/  /' "$_lint_err" >&2

  _resolver_failed=false
  if [ "$_lint_rc" -eq 2 ]; then
    echo "  ❌ wiki-lint-links.py failed (exit 2)"
    head -20 "$_lint_out" | sed 's/^/  /'
    broken_count=1
    _resolver_failed=true
  fi

  # Collect results from structured output
  _broken_lines=""
  _orphan_lines=""
  _format_lines=""
  _ambig_lines=""
  _ambig_count=0
  _fmt_fixed=0
  _fmt_remaining=0
  _dup_count=0
  while IFS= read -r line; do
    case "$line" in
      BROKEN:*)
        _file="${line#BROKEN:}"
        _target="${_file#*	}"
        _file="${_file%%	*}"
        _broken_lines="${_broken_lines}  🔗 $_file → [[$_target]]
"
        broken_count=$((broken_count + 1))
        ;;
      ORPHAN:*)
        _orphan_lines="${_orphan_lines}  🏝️  ${line#ORPHAN:}
"
        orphan_count=$((orphan_count + 1))
        ;;
      FORMAT:*)
        _format_lines="${_format_lines}  WOULD REWRITE: ${line#FORMAT:}
"
        _fmt_remaining=$((_fmt_remaining + 1))
        ;;
      FIXED:*)
        _format_lines="${_format_lines}  REWRITTEN: ${line#FIXED:}
"
        _fmt_fixed=$((_fmt_fixed + 1))
        ;;
      DUPLICATE:*)
        _format_lines="${_format_lines}  ⚠️  DUPLICATE BASENAME: ${line#DUPLICATE:}
"
        _dup_count=$((_dup_count + 1))
        ;;
      AMBIG:*)
        _ambig_lines="${_ambig_lines}  ⚠️  AMBIGUOUS: ${line#AMBIG:}
"
        ;;
      ERROR:*)
        echo "  ❌ ${line#ERROR:}"
        ;;
      STATS:*)
        _ambig_count=$(echo "$line" | sed 's/.*ambig=\([0-9]*\).*/\1/')
        _ambig_count=${_ambig_count:-0}
        case "$_ambig_count" in *[!0-9]*) _ambig_count=0 ;; esac
        ;;
      MAP:*) ;;
    esac
  done < "$_lint_out"

  # Print broken wikilinks
  if [ -n "$_broken_lines" ]; then
    printf '%s' "$_broken_lines"
  elif ! $_resolver_failed; then
    echo "  ✅ All wikilinks resolve"
  fi
  echo ""

  # Print orphans
  echo "## Orphan Pages"
  if [ -n "$_orphan_lines" ]; then
    printf '%s' "$_orphan_lines"
  elif ! $_resolver_failed; then
    echo "  ✅ No orphan pages"
  fi
  echo ""

  # Print wikilink format
  echo "## Wikilink Format"
  if [ -n "$_ambig_lines" ]; then
    printf '%s' "$_ambig_lines"
  fi
  if [ -n "$_format_lines" ]; then
    printf '%s' "$_format_lines"
  fi
  if $_resolver_failed; then
    echo "  ❌ Resolver failed — results incomplete"
    fmt_count=1
  else
    # fmt_count = remaining issues (not fixed ones)
    fmt_count=$((_fmt_remaining + _dup_count + _ambig_count))
    if [ "$fmt_count" -eq 0 ] && [ "$_fmt_fixed" -eq 0 ]; then
      echo "  ✅ All wikilinks correctly formatted"
    else
      [ "$_fmt_fixed" -gt 0 ] && echo "  🔧 Fixed $_fmt_fixed wikilink issue(s)"
      [ "$_dup_count" -gt 0 ] && echo "  ⚠️  $_dup_count duplicate basename(s) (resolve manually)"
      [ "$_ambig_count" -gt 0 ] && echo "  ⚠️  $_ambig_count ambiguous link(s) skipped (resolve manually)"
      [ "$_fmt_remaining" -gt 0 ] && echo "  ⚠️  $_fmt_remaining format issue(s) remaining"
    fi
  fi
else
  mark_skipped "broken-links"
  mark_skipped "orphans"
  mark_skipped "wikilink-format"
  echo "  ⏭️  Skipped (python3 or wiki-lint-links.py not found)"
fi
echo ""

# ── 4. Stale Pages ────────────────────────────────────────
echo "## Stale Pages"
stale_count=0
if $HAS_PYTHON3; then
  cutoff=$(python3 -c "from datetime import datetime,timedelta;print((datetime.now()-timedelta(days=30)).strftime('%Y-%m-%d'))" 2>/dev/null || echo "")
  if [ -n "$cutoff" ]; then
    while IFS= read -r file; do
      updated=$(get_field "$file" updated)
      if [ -n "$updated" ]; then
        # Validate YYYY-MM-DD format
        case "$updated" in
          [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) ;;
          *) echo "  ⚠️  ${file#"$VAULT"/} — malformed date: $updated"; stale_count=$((stale_count + 1)); continue ;;
        esac
        [ "$updated" \< "$cutoff" ] && {
          echo "  ⏰ ${file#"$VAULT"/} — last updated $updated"
          echo "x" >> "$STALE_LOG"
        }
      fi
    done < <(find_content_pages)
    stale_count=$(( stale_count + $(wc -l < "$STALE_LOG" 2>/dev/null | tr -d ' ') ))
    [ "$stale_count" -eq 0 ] && echo "  ✅ No stale pages"
  else
    mark_skipped "stale"
    echo "  ⏭️  Skipped (python3 date comparison failed)"
  fi
else
  mark_skipped "stale"
  echo "  ⏭️  Skipped (python3 required for date comparison)"
fi
echo ""

# ── 5. Tag Drift ──────────────────────────────────────────
echo "## Tag Drift"
drift_count=0
taxonomy="$VAULT/_meta/taxonomy.md"
if [ -f "$taxonomy" ]; then
  CANONICAL_FILE=$(mktemp)
  grep -E '^- `[^`]+`' "$taxonomy" 2>/dev/null | sed 's/^- `//;s/`.*//' > "$CANONICAL_FILE"
  while IFS= read -r file; do
    tags_line=$(get_frontmatter "$file" | sed -n '/^tags:/{s/^tags: *\[//;s/\].*//; p; q;}')
    [ -z "$tags_line" ] && continue
    echo "$tags_line" | tr ',' '\n' | sed 's/^ *//;s/ *$//' | while IFS= read -r tag; do
      [ -z "$tag" ] && continue
      if ! grep -qx "$tag" "$CANONICAL_FILE" 2>/dev/null; then
        echo "  🏷️  ${file#"$VAULT"/} — unknown tag: $tag"
        echo "x" >> "$DRIFT_LOG"
      fi
    done
  done < <(find_content_pages)
  drift_count=$(wc -l < "$DRIFT_LOG" 2>/dev/null | tr -d ' ')
  rm -f "$CANONICAL_FILE"
  CANONICAL_FILE=""
  [ "$drift_count" -eq 0 ] && echo "  ✅ All tags in taxonomy"
else
  mark_skipped "tag-drift"
  echo "  ⏭️  Skipped (taxonomy file not found: _meta/taxonomy.md)"
fi
echo ""

# ── 7. Markdown Structure (via markdownlint-cli2) ────────
echo "## Markdown Structure"
mdl_count=0
MDL_CONFIG="$SKILL_DIR/markdownlint-cli2.json"
# Find npx: PATH, then Volta, then NVM, then nix-profile
NPX_BIN=""
if command -v npx >/dev/null 2>&1; then
  NPX_BIN="npx"
elif [ -x "${VOLTA_HOME:-$HOME/.volta}/bin/npx" ]; then
  NPX_BIN="${VOLTA_HOME:-$HOME/.volta}/bin/npx"
elif [ -x "${NVM_DIR:-$HOME/.nvm}/current/bin/npx" ]; then
  NPX_BIN="${NVM_DIR:-$HOME/.nvm}/current/bin/npx"
elif [ -d "${NVM_DIR:-$HOME/.nvm}/versions/node" ]; then
  _nvm_latest=$(/bin/ls -1d "${NVM_DIR:-$HOME/.nvm}/versions/node/"v* 2>/dev/null | sed 's/.*\/v//' | sort -t. -k1,1n -k2,2n -k3,3n | tail -1)
  _nvm_latest="${NVM_DIR:-$HOME/.nvm}/versions/node/v$_nvm_latest"
  [ -x "$_nvm_latest/bin/npx" ] && NPX_BIN="$_nvm_latest/bin/npx"
elif [ -x "$HOME/.nix-profile/bin/npx" ]; then
  NPX_BIN="$HOME/.nix-profile/bin/npx"
fi
if [ -n "$NPX_BIN" ] && [ -f "$MDL_CONFIG" ]; then
  _mdl_opts=()
  $FIX_MODE && _mdl_opts+=(--fix)
  _mdl_tmp=$(mktemp)
  find "$WIKI" -type f -name '*.md' ! -path "$WIKI/index.md" ! -path "$WIKI/log.md" -print0 2>/dev/null | xargs -0 "$NPX_BIN" --yes markdownlint-cli2 "${_mdl_opts[@]}" --config "$MDL_CONFIG" > "$_mdl_tmp" 2>&1
  _mdl_rc=$?
  if [ "$_mdl_rc" -ne 0 ] && [ "$_mdl_rc" -ne 1 ]; then
    echo "  ❌ markdownlint-cli2 failed (exit $_mdl_rc)"
    head -20 "$_mdl_tmp" | sed 's/^/  /'
    mdl_count=1
  else
    while IFS= read -r line; do
      [ -z "$line" ] && continue
      case "$line" in
        *"npm "*|*"npx "*|*"Finding"*|*"markdownlint-cli2 "*v*|*"Linting:"*|*"Summary:"*) continue ;;
      esac
      echo "  $line"
      echo "x" >> "$MDL_LOG"
    done < "$_mdl_tmp"
    mdl_count=$(wc -l < "$MDL_LOG" 2>/dev/null | tr -d ' ')
  fi
  if [ "$mdl_count" -eq 0 ]; then
    echo "  ✅ No markdown structure issues"
  elif $FIX_MODE; then
    echo "  🔧 Reported $mdl_count issue(s) (fixable ones auto-corrected)"
  fi
else
  if [ -z "$NPX_BIN" ]; then
    mark_skipped "markdown (npx not found)"
    echo "  ⏭️  Skipped (npx not found)"
  else
    mark_skipped "markdown (config missing: $MDL_CONFIG)"
    echo "  ⏭️  Skipped (config missing)"
  fi
fi
echo ""

# ── 8. Unlinked Mentions (advisory, non-blocking) ───────────
echo "## Unlinked Mentions (advisory)"
if $HAS_PYTHON3; then
  CROSSLINK_SCRIPT="$SKILL_DIR/scripts/wiki-crosslink.py"
  if [ -f "$CROSSLINK_SCRIPT" ]; then
    _xl_out=$(mktemp)
    _xl_err=$(mktemp)
    _xl_args=""
    $FIX_MODE && _xl_args="--fix"
    python3 "$CROSSLINK_SCRIPT" "$VAULT" $_xl_args > "$_xl_out" 2>"$_xl_err"
    _xl_rc=$?
    if [ "$_xl_rc" -eq 2 ]; then
      echo "  ❌ wiki-crosslink.py failed (exit 2)"
      [ -s "$_xl_err" ] && head -5 "$_xl_err" | sed 's/^/  /'
      rm -f "$_xl_out" "$_xl_err"
    else
      _xl_unlinked=0
      _xl_stats_line=""
      while IFS= read -r line; do
        case "$line" in
          UNLINKED:*)
            _xl_file="${line#UNLINKED:}"
            _xl_target="${_xl_file##*	}"
            _xl_mention="${_xl_file#*	}"
            _xl_mention="${_xl_mention%	*}"
            _xl_file="${_xl_file%%	*}"
            echo "  💡 $_xl_file — \"$_xl_mention\" → [[$_xl_target]]"
            ;;
          STATS:*)
            _xl_unlinked=$(echo "$line" | sed 's/.*unlinked=\([0-9]*\).*/\1/')
            _xl_unlinked=${_xl_unlinked:-0}
            _xl_stats_line="$line"
            ;;
        esac
      done < "$_xl_out"
      rm -f "$_xl_out" "$_xl_err"
      if [ "${_xl_unlinked:-0}" -eq 0 ]; then
        echo "  ✅ No unlinked mentions found"
      elif $FIX_MODE; then
        _xl_fixed=$(echo "$_xl_stats_line" | sed 's/.*fixed=\([0-9]*\).*/\1/')
        echo "  🔧 ${_xl_fixed:-0} mention(s) auto-linked. ${_xl_unlinked} total detected."
      else
        echo "  ℹ️  ${_xl_unlinked} unlinked mention(s) found. Run wiki-crosslink.py --fix to add wikilinks."
      fi
    fi  # end of _xl_rc check
  else
    echo "  ⏭️  Skipped (wiki-crosslink.py not found)"
  fi
else
  echo "  ⏭️  Skipped (python3 not found)"
fi
echo ""

# ── Summary ───────────────────────────────────────────────
total=$(( fm_count + broken_count + orphan_count + stale_count + drift_count + fmt_count + mdl_count ))
echo "=== Summary ==="
printf "  %-14s %d\n" "Frontmatter:" "$fm_count"
printf "  %-14s %d\n" "Wikilinks:" "$broken_count"
printf "  %-14s %d\n" "Orphans:" "$orphan_count"
printf "  %-14s %d\n" "Stale:" "$stale_count"
printf "  %-14s %d\n" "Tag drift:" "$drift_count"
printf "  %-14s %d\n" "Link format:" "$fmt_count"
printf "  %-14s %d\n" "Markdown:" "$mdl_count"
printf "  %-14s %d\n" "Total:" "$total"
echo "  (Unlinked mentions are advisory only — not counted in total)"
if [ -n "$skipped_checks" ]; then
  echo "  ⚠️  Skipped:    $skipped_checks"
fi
echo ""
if [ "$total" -eq 0 ]; then
  if [ -n "$skipped_checks" ]; then
    echo "No issues found in executed checks (some checks were skipped)."
  else
    echo "🎉 Wiki is healthy!"
  fi
else
  echo "Run fixes or ask the agent to resolve issues."
fi
exit $(( total > 125 ? 125 : total ))
