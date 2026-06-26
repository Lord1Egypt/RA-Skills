#!/bin/bash
# healthy-backup v1.3.0
# Usage: healthy-backup.sh [--dry-run | --verify [path]]
#
# Config: ~/.openclaw/config/healthy-backup/hb-config.json (written by setup.sh)
# Falls back to env vars then built-in defaults.
#
# Secrets policy:
#   openclaw.json staged with sensitive field values SCRUBBED (jq walk)
#   shared/secrets/ credentials/ *.key *.pem *.env *.secret never rsynced
#   secrets-manifest: key names only — values never written
#   GPG passphrase: chmod-600 temp file, never on CLI, deleted on EXIT
set -euo pipefail

VERSION="1.3.0"
OC="$HOME/.openclaw"
OC_CFG="$OC/openclaw.json"
HB_CFG="$OC/config/healthy-backup/hb-config.json"
MODE="${1:-backup}"   # backup | --dry-run | --verify

# ── UI ────────────────────────────────────────────────────────────────────────
R='\033[0;31m' G='\033[0;32m' Y='\033[1;33m' B='\033[0;34m' BO='\033[1m' X='\033[0m'
log()    { echo -e "${B}[hb]${X} $*"; }
ok()     { echo -e "${G}  ✓${X} $*"; }
fail()   { echo -e "${R}  ✗${X} $*"; }
warn()   { echo -e "${Y}  ⚠${X} $*"; }
header() { echo -e "\n${BO}$*${X}"; }

# ── Cleanup ───────────────────────────────────────────────────────────────────
STAGING="" ARCHDIR="" PF=""
cleanup() { rm -rf "$STAGING" "$ARCHDIR"; [ -f "$PF" ] && rm -f "$PF"; }
trap cleanup EXIT

# ── Config ────────────────────────────────────────────────────────────────────
[ -f "$OC_CFG" ] || { fail "openclaw.json not found"; exit 1; }
HC=""; [ -f "$HB_CFG" ] && HC=$(cat "$HB_CFG" 2>/dev/null)
cfg() { local v=""; [ -n "$HC" ] && v=$(echo "$HC" | jq -r ".$1 // empty" 2>/dev/null)
        v="${v/#\~/$HOME}"; echo "${v:-${!2:-$3}}"; }

WORKSPACE=$(jq -r '.agents.defaults.workspace // empty' "$OC_CFG" 2>/dev/null)
WORKSPACE="${WORKSPACE:-$OC/workspace}"
SKILLS=$(cfg skillsDir  SKILLS_DIR  "$OC/skills")
ROOT=$(cfg   backupRoot BACKUP_ROOT "$HOME/openclaw-backups")
REMOTE=$(cfg remoteDest REMOTE_DEST "")
MODE_UP=$(cfg uploadMode UPLOAD_MODE "local-only")
TIER=$(cfg   backupTier BACKUP_TIER  "migratable")
MAX=$(cfg    maxBackups  MAX_BACKUPS  "5")
MINDISK=$(cfg minDiskMb MIN_DISK_MB  "500")
C_NPM=$(cfg  collectNpm     COLLECT_NPM     "false")
C_CRON=$(cfg collectCrontab COLLECT_CRONTAB "false")
C_OLL=$(cfg  collectOllama  COLLECT_OLLAMA  "true")
SECRETS="$OC/shared/secrets/openclaw-secrets.env"

PW="${BACKUP_PASSWORD:-$(cfg password BACKUP_PASSWORD "")}"
KF="$OC/credentials/backup.key"
[ -z "$PW" ] && [ -f "$KF" ] && PW=$(tr -d '\n' < "$KF")

EX=(--exclude=shared/secrets/ --exclude=credentials/
    --exclude='*.key' --exclude='*.pem' --exclude='*.env'
    --exclude='*.secret' --exclude='.env'
    --exclude='.git/' --exclude='node_modules/' --exclude='BACKUPS/')

# ── --verify subcommand ───────────────────────────────────────────────────────
if [ "$MODE" = "--verify" ]; then
    TARGET="${2:-$ROOT}"
    echo -e "\n${BO}━━━ VERIFY${X} — $TARGET\n"
    PASS=0 FAIL=0 SKIP=0
    chk_archive() {
        local a="$1" cs="$1.sha256"
        echo -e "${BO}$(basename "$a")${X}"
        if [ ! -f "$cs" ]; then warn "No .sha256 — skip"; SKIP=$((SKIP+1)); return; fi
        sha256sum --check "$cs" --status 2>/dev/null \
            && { ok "SHA256 OK"; PASS=$((PASS+1)); } \
            || { fail "SHA256 MISMATCH"; FAIL=$((FAIL+1)); }
        gpg --batch --list-packets "$a" &>/dev/null \
            && ok "GPG envelope intact" \
            || { fail "GPG envelope damaged"; FAIL=$((FAIL+1)); }
        echo ""
    }
    if   [ -f "$TARGET" ]; then chk_archive "$TARGET"
    elif [ -d "$TARGET" ]; then
        shopt -s nullglob; archives=("$TARGET"/healthy-backup-*.tgz.gpg)
        [ "${#archives[@]}" -eq 0 ] && { echo "No archives in $TARGET"; exit 0; }
        for a in "${archives[@]}"; do chk_archive "$a"; done
    else echo -e "${R}Not a file or directory:${X} $TARGET"; exit 1; fi
    echo -e "${BO}━━━ RESULT${X}  ${G}OK:$PASS${X}  ${Y}Skip:$SKIP${X}  ${R}Fail:$FAIL${X}\n"
    [ "$FAIL" -gt 0 ] && exit 1; exit 0
fi

# ── Health audit ──────────────────────────────────────────────────────────────
HFAIL=0 RPT=()
chk_ok()   { ok   "$1"; RPT+=("PASS: $1"); }
chk_fail() { fail "$1"; RPT+=("FAIL: $1"); HFAIL=1; }
chk_warn() { warn "$1"; RPT+=("WARN: $1"); }
perms()    { local p; p=$(stat -c "%a" "$1" 2>/dev/null || stat -f "%OLp" "$1" 2>/dev/null)
             [ "$p" = "600" ] && chk_ok "$2 perms OK (600)" || chk_fail "$2 perms $p — chmod 600 $1"; }

header "━━━ HEALTH AUDIT ━━━"

header "0. Setup"
[ -f "$HB_CFG" ] && jq empty "$HB_CFG" 2>/dev/null \
    && chk_ok "hb-config.json valid" \
    || chk_warn "No config — run setup.sh (using defaults)"

header "1. Binaries"
for cmd in tar jq gpg rsync; do
    command -v "$cmd" &>/dev/null && chk_ok "$cmd" || chk_fail "$cmd not found"
done
[ "$MODE_UP" = "rclone" ] && { command -v rclone &>/dev/null && chk_ok "rclone" || chk_fail "rclone not found"; }

header "2. Config"
jq empty "$OC_CFG" 2>/dev/null && chk_ok "openclaw.json valid" || chk_fail "openclaw.json corrupt"
n=$(jq '.agents.entries | length' "$OC_CFG" 2>/dev/null || echo 0)
[ "$n" -gt 0 ] && chk_ok "$n agent(s)" || chk_warn "No agents defined (may be intentional)"

header "3. Directories"
[ -d "$OC" ]        && chk_ok "openclaw dir"  || chk_fail "openclaw dir missing: $OC"
[ -d "$WORKSPACE" ] && chk_ok "workspace"     || chk_fail "workspace missing: $WORKSPACE"
[ -d "$SKILLS" ]    && chk_ok "skills ($(find "$SKILLS" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' '))" \
                    || chk_warn "skills dir not found"

header "4. Disk"
avail=$(df -m "$HOME" | awk 'NR==2{print $4}')
[ "$avail" -ge "$MINDISK" ] && chk_ok "${avail}MB free" || chk_fail "Low disk — ${avail}MB free, need ${MINDISK}MB"

header "5. Encryption"
[ -n "$PW" ] && chk_ok "Password found" || chk_fail "No password — create $KF (chmod 600)"
[ -f "$KF" ] && perms "$KF" "backup.key"
pw_inline=$(jq -r '.skills.entries["healthy-backup"].config.password // empty' "$OC_CFG" 2>/dev/null)
[ -n "$pw_inline" ] && chk_warn "Inline password in openclaw.json — move to $KF"

header "6. Secrets"
[ -f "$SECRETS" ] && { chk_ok "Secrets file (excluded from staging)"; perms "$SECRETS" "Secrets"; } \
                  || chk_warn "No secrets file at $SECRETS (may be optional)"

[ "$MODE_UP" = "rclone" ] && {
    header "7. Cloud"
    [ -z "$REMOTE" ] && chk_fail "uploadMode=rclone but remoteDest not set" || {
        rclone listremotes 2>/dev/null | grep -q "^${REMOTE%%:*}:" \
            && chk_ok "rclone remote '${REMOTE%%:*}' found" \
            || chk_fail "rclone remote '${REMOTE%%:*}' not found — rclone config"
    }
}

header "8. Ollama"
command -v ollama &>/dev/null && {
    m=$(ollama list 2>/dev/null | tail -n +2 | awk '{print $1}' | tr '\n' ' ')
    [ -n "$m" ] && chk_ok "Models: $m" || chk_warn "Ollama installed, no models loaded"
} || chk_warn "Ollama not found (skip if unused)"

header "━━━ AUDIT RESULT ━━━"
printf "  ${G}Pass:${X} %s  ${Y}Warn:${X} %s  ${R}Fail:${X} %s\n" \
    "$(printf '%s\n' "${RPT[@]}" | grep -c '^PASS:')" \
    "$(printf '%s\n' "${RPT[@]}" | grep -c '^WARN:')" \
    "$(printf '%s\n' "${RPT[@]}" | grep -c '^FAIL:')"

[ "$HFAIL" -eq 1 ] && { echo -e "\n${R}${BO}✗ Audit failed — backup aborted.${X}\n"; exit 1; }
echo -e "\n${G}${BO}✓ Rig healthy${X}\n"

# ── Dry-run ───────────────────────────────────────────────────────────────────
if [ "$MODE" = "--dry-run" ]; then
    header "━━━ DRY RUN ━━━"
    log "Tier: $TIER  →  $ROOT/"
    dry_sync() { rsync -a --dry-run --out-format="  %n" "${EX[@]}" "$@" /dev/null 2>/dev/null || true; }
    echo "  [config] openclaw.json (scrubbed)"
    [ -f "$SECRETS" ] && echo "  [config] secrets-manifest.txt (names only)"
    [[ "$TIER" == "migratable" || "$TIER" == "full" ]] && {
        echo "  [openclaw]"; dry_sync --exclude='logs/' --exclude='media/' --exclude='browser/' "$OC/"; }
    [[ "$TIER" == "full" ]] && {
        [ -d "$WORKSPACE" ] && { echo "  [workspace]"; dry_sync --exclude='canvas/' "$WORKSPACE/"; }
        [ -d "$SKILLS" ]   && { echo "  [skills]";    dry_sync --exclude='.venv/' "$SKILLS/"; }
    }
    echo -e "\n${Y}${BO}Nothing written.${X} Remove --dry-run to execute.\n"; exit 0
fi

# ── Backup ────────────────────────────────────────────────────────────────────
PF=$(mktemp); chmod 600 "$PF"; printf '%s' "$PW" > "$PF"; unset PW
TS=$(date +%Y%m%d-%H%M%S)
ANAME="healthy-backup-${TS}-${TIER}.tgz"
ENAME="${ANAME}.gpg"
STAGING=$(mktemp -d); ARCHDIR=$(mktemp -d)
mkdir -p "$ROOT"

header "━━━ BACKUP [${TIER}] ━━━"
log "Staging..."

sync_dir() { local s="$1" d="$STAGING/$2"; shift 2; mkdir -p "$d"; rsync -a "${EX[@]}" "$@" "$s/" "$d/"; }

stage_config() {
    mkdir -p "$STAGING/config"
    jq 'walk(if type=="object" then with_entries(
        if (.key|test("password|token|secret|key";"i")) then .value="<redacted>" else . end) else . end
    )' "$OC_CFG" > "$STAGING/config/openclaw.json"
    ok "openclaw.json (scrubbed)"
    [ -f "$SECRETS" ] && {
        grep -oE '^[A-Za-z_][A-Za-z0-9_]*' "$SECRETS" > "$STAGING/config/secrets-manifest.txt" 2>/dev/null || true
        ok "secrets-manifest.txt (names only)"; }
}

stage_deps() {
    { echo "# Dependencies — healthy-backup v${VERSION} — $(date)"
      echo; echo "## Binaries"
      for c in tar gpg jq rsync rclone ollama node npm python3; do
          command -v "$c" &>/dev/null && echo "- \`$c\`: $($c --version 2>&1 | head -1)" \
                                      || echo "- \`$c\`: not installed"; done
      echo; echo "## OS"; uname -a
      echo; echo "## npm globals"
      [ "$C_NPM"  = "true" ] && npm list -g --depth=0 2>/dev/null | tail -n +2 || echo "(opt-in off)"
      echo; echo "## Ollama"
      [ "$C_OLL"  = "true" ] && ollama list 2>/dev/null | tail -n +2            || echo "(opt-in off)"
      echo; echo "## Cron (values redacted)"
      [ "$C_CRON" = "true" ] && crontab -l 2>/dev/null \
          | sed 's/\([A-Za-z_][A-Za-z0-9_]*\)=[^ ]*/\1=<REDACTED>/g'           || echo "(opt-in off)"
    } > "$STAGING/DEPENDENCIES.md"
    ok "DEPENDENCIES.md"
}

case "$TIER" in
    minimal)
        stage_config ;;
    migratable)
        stage_config
        sync_dir "$OC" openclaw --exclude='logs/' --exclude='media/' --exclude='browser/'
        ok "~/.openclaw"; stage_deps ;;
    full)
        stage_config
        sync_dir "$OC" openclaw --exclude='logs/' --exclude='media/' --exclude='browser/'
        ok "~/.openclaw"; stage_deps
        [ -d "$WORKSPACE" ] && { sync_dir "$WORKSPACE" workspace --exclude='canvas/'; ok "workspace"; } || warn "workspace not found"
        [ -d "$SKILLS" ]    && { sync_dir "$SKILLS"    skills    --exclude='.venv/';  ok "skills"; }    || warn "skills not found" ;;
    *) fail "Unknown tier '$TIER'"; exit 1 ;;
esac

printf "healthy-backup v%s\nTimestamp: %s\nTier: %s\nUpload: %s\n\n%s\n" \
    "$VERSION" "$(date)" "$TIER" "$MODE_UP" "$(printf '%s\n' "${RPT[@]}")" > "$STAGING/HEALTH_REPORT.txt"

log "Compressing..."; tar -czf "$ARCHDIR/$ANAME" -C "$STAGING" .; ok "$(du -sh "$ARCHDIR/$ANAME" | cut -f1)"
log "Encrypting...";  gpg --batch --yes --passphrase-file "$PF" --symmetric --cipher-algo AES256 \
                          -o "$ARCHDIR/$ENAME" "$ARCHDIR/$ANAME"

mv "$ARCHDIR/$ENAME" "$ROOT/"
sha256sum "$ROOT/$ENAME" > "$ROOT/$ENAME.sha256"
ok "Saved → $ROOT/$ENAME"

log "Pruning..."
mapfile -t ALL < <(ls -t "$ROOT"/healthy-backup-*.tgz.gpg 2>/dev/null)
[ "${#ALL[@]}" -gt "$MAX" ] && for f in "${ALL[@]:$MAX}"; do rm -f "$f" "$f.sha256"; warn "Pruned: $(basename "$f")"; done
ok "${#ALL[@]} archive(s), max $MAX"

[ "$MODE_UP" = "rclone" ] && [ -n "$REMOTE" ] && {
    header "━━━ SYNC ━━━"; rclone sync "$ROOT" "$REMOTE" --include "*.gpg" --progress; ok "→ $REMOTE"; }

header "━━━ DONE ━━━"
echo -e "${G}${BO}✓ Complete${X}  $ROOT/$ENAME"
echo -e "  Tier: $TIER  |  Retained: $MAX  |  Script: $(sha256sum "$0" | awk '{print $1}')"
[ "$MODE_UP" = "rclone" ] && echo -e "  Cloud: $REMOTE"
echo ""

# END OF FILE — healthy-backup.sh v1.3.0
