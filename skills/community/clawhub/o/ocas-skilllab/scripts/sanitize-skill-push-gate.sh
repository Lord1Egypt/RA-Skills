#!/usr/bin/env bash
# Sanitize gate for a single skill (or plugin) directory.
# Companion to secret-scan.sh: that one looks for CREDENTIALS, this one looks for
# IDENTITY and HOST leaks — real names, personal email, absolute paths that expose
# the operator's machine layout, and bare host/IP addresses.
#
# This script lives in a PUBLIC repo, so it must not contain the very strings it
# hunts for. Operator-specific terms are read from a terms file kept OUTSIDE the
# repo (default: $HOME/.hermes/.sanitize-terms, one extended-regex per line,
# '#' comments allowed). Generic checks still run when that file is absent.
#
# Exits 0 if CLEAN, 1 if a potential leak is found, 2 if no .git present.
set -u

MODE="full"
case "${1:-}" in
  --help|-h)
    echo "Usage: sanitize-skill-push-gate.sh [--working-tree] <dir>"
    echo "Scans <dir> for identity/host leaks. Default: working tree + full git history."
    echo "  --working-tree : scan the working tree only — use to gate sync/publish of NEW changes."
    echo "Operator terms: \${SANITIZE_TERMS_FILE:-\$HOME/.hermes/.sanitize-terms}"
    echo "Exits 0 if CLEAN, 1 if a leak is found, 2 if no .git present."
    exit 0 ;;
  --working-tree) MODE="wt"; TARGET="${2:-.}";;
  *) MODE="full"; TARGET="${1:-.}";;
esac

[ -d "$TARGET/.git" ] || { echo "No .git in $TARGET — nothing to scan"; exit 2; }

SELF="$(basename "$0")"
TERMS_FILE="${SANITIZE_TERMS_FILE:-$HOME/.hermes/.sanitize-terms}"

# Absolute paths that reveal the host's layout, and bare host identifiers.
# Deliberately NOT matching /usr, /etc, /opt, /var — those are generic and appear
# in legitimate documentation.
PATH_RE='/root/[A-Za-z0-9._-]|/home/[a-z][A-Za-z0-9._-]+|/Users/[a-z][A-Za-z0-9._-]+'
HOST_RE='\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
EMAIL_RE='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

# Addresses and hosts that are meant to be public or are obvious placeholders.
# Addresses and hosts that are meant to be public or are obvious placeholders.
#
# NOTE (2026-08-22): this was written with backslash-newline continuations inside
# SINGLE quotes, where a backslash before a newline is literal -- so ALLOW_RE
# contained real newlines, `grep -P` rejected it with "the -P option only
# supports a single pattern", the email and IP pipelines produced EMPTY output,
# and report() returned early. Both checks silently passed everything for two
# weeks. A safety gate that fails OPEN is worse than no gate, because the green
# result is read as evidence. Kept on one line so it cannot regress the same way.
ALLOW_RE='\b(birchmantle|mossglade|cedarquill|fernwick)[.+@]|\b(noreply|no-reply|support|info|icons|admin|contact|hello|sales)@|\b[a-z]{1,2}@[a-z0-9.-]+\.[a-z]{2,}\b|@[A-Za-z0-9.-]*\.(test|invalid|localhost)\b|\b[a-z]{1,2}@[a-z]{1,2}\.(com|org|net)\b|\bmailto:[a-z]{1,2}@|/usr/local/lib/hermes-agent|[a-z]{2}\.[a-z]+#holiday@group\.v\.calendar\.google\.com|8\.8\.8\.8|8\.8\.4\.4|1\.1\.1\.1|1\.0\.0\.1|9\.9\.9\.9|@[A-Za-z0-9.-]*\.example\b|[A-Za-z0-9.-]*\.example\.(com|org|net)|john\.doe@|jane\.doe@|(Chrome|Safari|Firefox|AppleWebKit|Gecko)/[0-9.]+|your-agent@|your-email@|agent@email\.com|mx\.indigo\.karasu@gmail\.com|x-access-token:|@example\.(com|org|net)|noreply@|no-reply@|you@|user@|someone@|name@|<[a-z-]+>|127\.0\.0\.1|0\.0\.0\.0|localhost|1\.2\.3\.4|192\.0\.2\.|198\.51\.100\.|203\.0\.113\.'

EXC=(--exclude-dir=.git "--exclude=$SELF" --exclude=secret-scan.sh --exclude='*.lock')

# Lines carrying an explicit inline marker are synthetic fixtures, not leaks:
# PII test corpora need realistic-LOOKING addresses and paths to test against.
# An inline marker is auditable in a diff, unlike widening the pattern set --
# it opts out one reviewed line rather than a whole class of real addresses.
ALLOW_MARK='sanitize-allow|pii-allow'
skip_noise() { grep -vE '(^|:|/)\.archive/|/(package-lock|yarn|pnpm-lock)\.(json|lock)|/node_modules/'; }
drop_marked() { grep -vE "$ALLOW_MARK"; }

found=0
echo "=== Sanitize scan: $TARGET ==="

report() { # label, payload
  [ -n "$2" ] || return 0
  echo "--- $1 ---"; echo "$2" | head -20; found=1
}

# 1. absolute host paths
# Tracked files only: the gate must judge what a push would actually publish.
# Untracked .bak.*/scratch copies dominated the findings while being unpushable,
# which hid the real leaks in tracked source behind dozens of false alarms.
report "HOST PATHS" "$(git -C "$TARGET" grep -I -n -P "$PATH_RE" -- . 2>/dev/null | skip_noise | drop_marked | grep -vP "$ALLOW_RE" | head -20)"

# 2. email addresses that are not placeholders
emails=$(git -C "$TARGET" grep -I -n -P "$EMAIL_RE" -- . 2>/dev/null \
         | skip_noise | drop_marked | grep -vP "$ALLOW_RE" | head -20)
report "EMAIL" "$emails"

# 3. IPv4 literals that are not loopback/documentation ranges
ips=$(git -C "$TARGET" grep -I -n -P "$HOST_RE" -- . 2>/dev/null \
      | skip_noise | drop_marked | grep -vP "$ALLOW_RE" | head -20)
report "IP ADDRESS" "$ips"

# 4. operator-specific terms, kept out of this repo on purpose
if [ -f "$TERMS_FILE" ]; then
  terms=$(grep -vE '^\s*(#|$)' "$TERMS_FILE" 2>/dev/null | paste -sd'|' -)
  if [ -n "$terms" ]; then
    hits=$(git -C "$TARGET" grep -I -n -i -E "$terms" -- . 2>/dev/null | skip_noise | drop_marked | head -20 \
           | sed -E 's/(.{100}).*/\1…/')
    report "OPERATOR IDENTITY" "$hits"
  fi
else
  echo "note: no terms file at $TERMS_FILE — generic checks only"
fi

# 5. History. Split by what refusing a push can actually PREVENT.
#
# Refusing today's push cannot unpublish a leak that is already on the remote --
# it only freezes the repo, and freezes out the very commits that would fix it.
# That is how the whole library ended up blocked: 24 repos flagged on history
# alone, so nothing could sync, including the remediation. Unpushed commits are
# still preventable and still block; published ones are reported as needing a
# history rewrite and do NOT block.
if [ "$MODE" = "full" ]; then
  upstream=$(git -C "$TARGET" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null)
  if [ -n "$upstream" ]; then
    unpushed=$(git -C "$TARGET" rev-list "$upstream"..HEAD 2>/dev/null | head -200)
    published=$(git -C "$TARGET" rev-list "$upstream" 2>/dev/null | head -200)
  else
    # No upstream: nothing has been published yet, so every commit is preventable.
    unpushed=$(git -C "$TARGET" rev-list --all 2>/dev/null | head -200)
    published=""
  fi
  if [ -n "$unpushed" ]; then
    hist=$(timeout 120 git -C "$TARGET" grep -I -n -P "$PATH_RE" $unpushed \
             -- ":(exclude)scripts/$SELF" 2>/dev/null | head -10)
    report "HISTORY (unpushed — still preventable)" "$hist"
  fi
  if [ -n "$published" ]; then
    phist=$(timeout 120 git -C "$TARGET" grep -I -n -P "$PATH_RE" $published \
              -- ":(exclude)scripts/$SELF" 2>/dev/null | head -5)
    if [ -n "$phist" ]; then
      echo "--- PUBLISHED HISTORY (needs scrub — NOT blocking) ---"
      echo "$phist"
      echo "note: already on the remote; blocking this push cannot unpublish it."
      echo "      remediate with a history rewrite + force-push INCLUDING TAGS."
    fi
  fi
fi

if [ "$found" -eq 0 ]; then echo "CLEAN: no identity/host leaks detected."; exit 0; fi
echo "LEAK DETECTED — do NOT publish until remediated."
exit 1
