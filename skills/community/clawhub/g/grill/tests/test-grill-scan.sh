#!/usr/bin/env bash
# test-grill-scan.sh - deterministic unit tests for scripts/grill-scan.sh.
# Plain bash, no model in the loop. Runs anywhere; exits non-zero on failure.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCAN="$HERE/../scripts/grill-scan.sh"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

FAILURES=0

# expect <label> <expected-exit> <grep-pattern|- for no check> -- <args...>
expect() {
  local label="$1" want_exit="$2" pattern="$3"
  shift 3
  [ "$1" = "--" ] && shift
  local out got_exit
  out="$("$SCAN" "$@" 2>&1)"
  got_exit=$?
  if [ "$got_exit" -ne "$want_exit" ]; then
    echo "[fail] $label: exit $got_exit, wanted $want_exit"
    printf '%s\n' "$out" | sed 's/^/    /'
    FAILURES=$((FAILURES + 1))
    return
  fi
  if [ "$pattern" != "-" ] && ! printf '%s\n' "$out" | grep -qF "$pattern"; then
    echo "[fail] $label: output missing $pattern"
    printf '%s\n' "$out" | sed 's/^/    /'
    FAILURES=$((FAILURES + 1))
    return
  fi
  echo "[ok] $label"
}

expect_absent() { # <label> <pattern> <args...>
  local label="$1" pattern="$2"
  shift 2
  local out
  out="$("$SCAN" "$@" 2>&1)"
  if printf '%s\n' "$out" | grep -qF "$pattern"; then
    echo "[fail] $label: unexpected $pattern in output"
    printf '%s\n' "$out" | sed 's/^/    /'
    FAILURES=$((FAILURES + 1))
    return
  fi
  echo "[ok] $label"
}

# Usage error: no arguments is an operator error, exit 2.
expect "no arguments exits 2 with usage" 2 "usage: grill-scan.sh" --

# Clean prose: exit 0 and the clean banner.
cat >"$TMP/clean.md" <<'EOF'
The migration finished on Tuesday and the error rate stayed flat.
We kept the old endpoint alive for one release and removed it the next.
EOF
expect "clean prose passes" 0 "clean: no mechanical flags" -- "$TMP/clean.md"

# Slop vocabulary.
cat >"$TMP/slop.md" <<'EOF'
Let's delve into this robust tapestry of seamless synergy.
EOF
expect "slop vocabulary flagged" 1 "### AI-slop vocabulary" -- "$TMP/slop.md"

# Empty hedges.
cat >"$TMP/hedge.md" <<'EOF'
It's worth noting that the cache was warm during the benchmark.
EOF
expect "empty hedge flagged" 1 "### Empty hedges / filler" -- "$TMP/hedge.md"

# Unsourced authority claims.
cat >"$TMP/authority.md" <<'EOF'
Studies show this layout is faster, and experts agree.
EOF
expect "authority claim flagged" 1 "### Unsourced authority claims" -- "$TMP/authority.md"

# Em dashes are forbidden by house style.
printf 'The deploy worked - mostly - after the retry.\n' >"$TMP/emdash-src.md"
sed -i 's/ - /\xE2\x80\x94/g' "$TMP/emdash-src.md"
expect "em dash flagged" 1 "### Em dashes" -- "$TMP/emdash-src.md"

# Bare tilde in prose is a markdown strikethrough footgun.
cat >"$TMP/tilde.md" <<'EOF'
The import took ~40 minutes on the slow link.
EOF
expect "bare tilde flagged" 1 "Markdown footgun" -- "$TMP/tilde.md"

# Tildes inside fenced code or inline code spans are not prose.
cat >"$TMP/tilde-code.md" <<'EOF'
Set the path to `~/.config/tool` and reload.

```bash
cp ~/.config/tool/defaults.yml ./defaults.yml
```
EOF
expect "tilde in code spans ignored" 0 "clean: no mechanical flags" -- "$TMP/tilde-code.md"

# The rhythmic motivational tic at sentence start.
cat >"$TMP/tic.md" <<'EOF'
The pipeline stalled twice before lunch. That is the job. We fixed it by noon.
EOF
expect "rhythmic tic flagged" 1 "### Possible rhythmic tic" -- "$TMP/tic.md"

# Unresolved fact markers must not survive to publish.
cat >"$TMP/confirm.md" <<'EOF'
The base edition costs [CONFIRM: current list price] per month.
EOF
expect "unresolved CONFIRM flagged" 1 "### Unresolved [CONFIRM] markers" -- "$TMP/confirm.md"

# Missing files are skipped without failing the run.
expect "missing file skipped, exit 0" 0 "skip (not a file)" -- "$TMP/does-not-exist.md"

# A clean file mixed with a missing file still passes.
expect "clean plus missing file passes" 0 "clean: no mechanical flags" -- "$TMP/does-not-exist.md" "$TMP/clean.md"

# Fence-aware tilde check still flags prose tildes around code blocks.
cat >"$TMP/tilde-mixed.md" <<'EOF'
```
echo ~ > /dev/null
```
The backup took ~3 hours overnight.
EOF
expect_absent "fenced tilde not flagged in mixed file" "1:echo ~" "$TMP/tilde-mixed.md"
expect "prose tilde flagged in mixed file" 1 "4:The backup took ~3 hours overnight." -- "$TMP/tilde-mixed.md"

if [ "$FAILURES" -ne 0 ]; then
  echo ">> $FAILURES grill-scan unit test(s) failed" >&2
  exit 1
fi
echo "[ok] grill-scan unit tests passed"
