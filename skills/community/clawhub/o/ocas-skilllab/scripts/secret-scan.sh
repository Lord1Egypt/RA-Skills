#!/usr/bin/env bash
# Secret-scan gate for a single skill (or plugin) directory.
# Scans: working tree, .git/config, and ENTIRE git history (all revisions).
# Output is masked — full secrets are never printed.
# Exits 0 if CLEAN, 1 if any potential secret is found (use to gate commit/publish).
set -u
MODE="full"
case "${1:-}" in
  --help|-h)
    TARGET="."
    echo "Usage: secret-scan.sh [--working-tree] <dir>"
    echo "Scans <dir> for secrets. Default: working tree, .git/config, and full git history."
    echo "  --working-tree : scan working tree + .git/config only (skip history) — use to gate sync/publish of NEW changes."
    echo "Exits 0 if CLEAN, 1 if a potential secret is found, 2 if no .git present."
    exit 0 ;;
  --working-tree) MODE="wt"; TARGET="${2:-.}";;
  *) MODE="full"; TARGET="${1:-.}";;
esac
if [ ! -d "$TARGET/.git" ]; then echo "No .git in $TARGET — nothing to scan"; exit 2; fi
RE='AKIA[0-9A-Z]{16}|gh[pousr]_[0-9A-Za-z]{36}|github_pat_[0-9A-Za-z_]{20,}|xox[baprs]-[0-9A-Za-z-]{10,}|sk-[0-9A-Za-z]{20,}|AIza[0-9A-Za-z_-]{35}|sk_live_[0-9A-Za-z]+|pk_live_[0-9A-Za-z]+|SK[0-9a-fA-F]{32}|eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.|BEGIN (RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY|ssh-rsa AAAAB3NzaC1|://[A-Za-z0-9_.-]+:[A-Za-z0-9_.-]{4,}@[A-Za-z0-9.-]+'
mask() { sed -E 's/([A-Za-z0-9_]{6})[A-Za-z0-9_-]{10,}([A-Za-z0-9_]{4})/\1***\2/g'; }
found=0
echo "=== Secret scan: $TARGET ==="
# Tracked files only, and honour the same inline marker the sanitize gate uses.
#
# Two false-positive sources blocked ocas-weave on 2026-08-23 while the tracked
# content was fine: (1) untracked scratch (*.bak-perpush, dropped by a cron
# mid-run) was scanned even though a push can never publish it, and (2) a
# synthetic test fixture -- classify_url("https://user:pass@example.com/me"),
# reserved domain, literal words "user"/"pass" -- read as a credential URL.
# A scanner that cries wolf on its own test corpus gets routed around, which is
# the failure mode this scanner exists to prevent.
if git -C "$TARGET" rev-parse --git-dir >/dev/null 2>&1; then
  # Exclude the scanners themselves at ANY depth and under EITHER spelling.
  # The pattern file necessarily contains secret-shaped strings, so a scanner
  # that does not exclude itself reports its own regex as a leak -- which is
  # exactly what blocked both monorepos when this moved to `git grep` and the
  # old --exclude=secret_scan.sh (underscore) was not carried across.
  wt=$(git -C "$TARGET" grep -I -n -P "$RE" -- . \
         ':(exclude,glob)**/secret-scan.sh' ':(exclude,glob)**/secret_scan.sh' \
         ':(exclude)secret-scan.sh' ':(exclude)secret_scan.sh' 2>/dev/null \
       | grep -vE 'secret-allow|sanitize-allow|pii-allow' | mask)
else
  wt=$(grep -rInP --exclude-dir=.git --exclude=secret-scan.sh --exclude='secret_scan.sh' "$RE" "$TARGET" 2>/dev/null \
       | grep -vE 'secret-allow|sanitize-allow|pii-allow' | mask)
fi
[ -n "$wt" ] && { echo "--- WORKING TREE ---"; echo "$wt"; found=1; }
cfg=$(grep -P "$RE" "$TARGET/.git/config" 2>/dev/null | mask)
[ -n "$cfg" ] && { echo "--- .git/config ---"; echo "$cfg"; found=1; }
revs=$(git -C "$TARGET" rev-list --all 2>/dev/null)
if [ "$MODE" = "full" ] && [ -n "$revs" ]; then
  hist=$(timeout 120 git -C "$TARGET" grep -I -n -P "$RE" $revs -- ':(exclude)scripts/secret-scan.sh' 2>/dev/null | mask)
  [ -n "$hist" ] && { echo "--- HISTORY ---"; echo "$hist"; found=1; }
fi
if [ "$found" -eq 0 ]; then echo "CLEAN: no secrets detected."; exit 0; fi
echo "SECRETS DETECTED — do NOT commit/publish until remediated."; exit 1