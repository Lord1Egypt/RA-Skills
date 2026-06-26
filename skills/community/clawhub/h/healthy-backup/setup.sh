#!/bin/bash
# healthy-backup setup.sh v1.3.0
# Interactive configurator. Flow: questions → config → cron → dry-run → summary.
# Dry-run is informational only — never fatal to setup.
set -euo pipefail

VERSION="1.3.0"
CFG_DIR="$HOME/.openclaw/config/healthy-backup"
CFG_FILE="$CFG_DIR/hb-config.json"
SD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$SD/healthy-backup.sh"

R='\033[0;31m' G='\033[0;32m' Y='\033[1;33m' B='\033[0;34m' BO='\033[1m' X='\033[0m'
log()    { echo -e "${B}[setup]${X} $*"; }
ok()     { echo -e "${G}  ✓${X} $*"; }
warn()   { echo -e "${Y}  ⚠${X} $*"; }
fail()   { echo -e "${R}  ✗${X} $*"; }
header() { echo -e "\n${BO}$*${X}"; }

prompt() {   # prompt <var> <question> <default>
    local v="$1" q="$2" d="$3"
    echo -e "${BO}  ?${X} $q"; [ -n "$d" ] && echo -e "    ${Y}(default: $d)${X}"
    read -r i; printf -v "$v" '%s' "${i:-$d}"
}

ask_yn() {   # ask_yn <question> <default n|y> → 0=yes 1=no
    local q="$1" d="${2:-n}"
    while true; do
        echo -e "${BO}  ?${X} $q"; echo -ne "    ${Y}[y/n, default: $d]${X} "
        read -r i; i="${i:-$d}"
        case "$i" in [Yy]*) return 0;; [Nn]*) return 1;; *) echo -e "    ${R}y or n${X}";; esac
    done
}

choose() {   # choose <var> <question> <opt1> <opt2> ...
    local v="$1" q="$2"; shift 2; local opts=("$@") i=1
    echo -e "${BO}  ?${X} $q"
    for o in "${opts[@]}"; do echo -e "    ${BO}$i)${X} $o"; (( i++ )); done
    while true; do
        read -r s; s="${s:-1}"
        [[ "$s" =~ ^[0-9]+$ ]] && [ "$s" -ge 1 ] && [ "$s" -le "${#opts[@]}" ] \
            && { printf -v "$v" '%s' "${opts[$(( s-1 ))]}"; break; }
        echo -e "    ${R}Enter 1–${#opts[@]}${X}"
    done
}

# ── Preflight ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${BO}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${X}"
echo -e "${BO}  healthy-backup setup — v${VERSION}     ${X}"
echo -e "${BO}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${X}"
echo ""
[ -f "$SCRIPT" ] || { fail "healthy-backup.sh not found at $SCRIPT"; exit 1; }
[ -f "$CFG_FILE" ] && warn "Existing config found" && ! ask_yn "Overwrite?" "n" \
    && { log "Cancelled — existing config kept."; exit 0; }

# ── Questions ─────────────────────────────────────────────────────────────────
header "━━━ 1. Tier"
echo -e "  ${Y}migratable${X}  ~/.openclaw + openclaw.json + dependency manifest (recommended)"
echo -e "  ${Y}minimal${X}     openclaw.json + secrets manifest only"
echo -e "  ${Y}full${X}        migratable + workspace + skills"
echo ""
choose TIER "Which tier?" "migratable (recommended)" "minimal" "full"
TIER="${TIER%% *}"

header "━━━ 2. Backup location"
prompt ROOT "Where should backups be stored?" "$HOME/openclaw-backups"
ROOT="${ROOT/#\~/$HOME}"

header "━━━ 3. Retention"
prompt MAX "How many healthy backups to keep?" "5"
[[ "$MAX" =~ ^[0-9]+$ ]] || { fail "Must be a number."; exit 1; }

header "━━━ 4. Disk threshold"
prompt MINDISK "Minimum free disk (MB) before backup?" "500"
[[ "$MINDISK" =~ ^[0-9]+$ ]] || { fail "Must be a number."; exit 1; }

header "━━━ 5. Cloud sync"
UPLOAD="local-only"; REMOTE=""
ask_yn "Enable rclone cloud sync?" "n" && {
    UPLOAD="rclone"
    prompt REMOTE "rclone destination (e.g. gdrive:openclaw-backups)" ""
    [ -z "$REMOTE" ] && { fail "Remote cannot be empty."; exit 1; }
}

header "━━━ 6. Dependency manifest"
C_OLL="false"; C_NPM="false"; C_CRON="false"
if [[ "$TIER" != "minimal" ]]; then
    ask_yn "Include Ollama model list?"               "y" && C_OLL="true"  || true
    ask_yn "Include npm global packages?"             "n" && C_NPM="true"  || true
    ask_yn "Include sanitised crontab? (values redacted)" "n" && C_CRON="true" || true
fi

header "━━━ 7. Encryption password"
KF="$HOME/.openclaw/credentials/backup.key"
echo -e "  Recommended: ${BO}$KF${X} (chmod 600)\n"
if [ -f "$KF" ]; then
    ok "Key file found"
    p=$(stat -c "%a" "$KF" 2>/dev/null)
    [ "$p" = "600" ] && ok "Permissions OK (600)" || warn "Permissions $p — fix: chmod 600 $KF"
else
    warn "Key file not found"
    ask_yn "Create it now?" "y" && {
        echo -e "${BO}  ?${X} Password (hidden):"; read -rs PW; echo ""
        [ -z "$PW" ] && { fail "Cannot be empty."; exit 1; }
        mkdir -p "$(dirname "$KF")"; printf '%s' "$PW" > "$KF"; chmod 600 "$KF"; unset PW
        ok "Created $KF (chmod 600)"
    } || warn "Skipped — set BACKUP_PASSWORD env var before running."
fi

header "━━━ 8. Cron"
log "Recommended: 05:00 (after Total Recall dream cycle)"
echo ""
INSTALL_CRON=false; CH="5"; CM="0"
ask_yn "Install cron job?" "n" && {
    INSTALL_CRON=true
    prompt CH "Hour (0-23)?"   "5"
    prompt CM "Minute (0-59)?" "0"
}

# ── Write config ──────────────────────────────────────────────────────────────
header "━━━ Writing config"
mkdir -p "$CFG_DIR"
jq -n \
    --arg  tier  "$TIER"   --arg  root  "$ROOT"   --arg  mode  "$UPLOAD" \
    --argjson max "$MAX"   --argjson disk "$MINDISK" \
    --argjson oll "$C_OLL" --argjson npm "$C_NPM"   --argjson cron "$C_CRON" \
    '{backupTier:$tier, backupRoot:$root, uploadMode:$mode,
      maxBackups:$max,  minDiskMb:$disk,
      collectOllama:$oll, collectNpm:$npm, collectCrontab:$cron}' > "$CFG_FILE"
[ "$UPLOAD" = "rclone" ] && \
    jq --arg d "$REMOTE" '. + {remoteDest:$d}' "$CFG_FILE" > "$CFG_FILE.tmp" && mv "$CFG_FILE.tmp" "$CFG_FILE"
jq empty "$CFG_FILE" 2>/dev/null && ok "Config written and valid → $CFG_FILE" \
    || { fail "Config malformed."; exit 1; }

# ── Cron ──────────────────────────────────────────────────────────────────────
if [ "$INSTALL_CRON" = true ]; then
    header "━━━ Installing cron"
    LD="$HOME/.openclaw/logs"; mkdir -p "$LD"
    CL="$CM $CH * * * bash \"$SCRIPT\" >> \"$LD/healthy-backup.log\" 2>&1"
    ( crontab -l 2>/dev/null | grep -v "healthy-backup.sh"; echo "$CL" ) | crontab -
    ok "Installed: $CL"
    log "Verify: crontab -l | grep healthy-backup"
    log "Remove: crontab -l | grep -v healthy-backup.sh | crontab -"
fi

# ── Dry-run (never fatal) ─────────────────────────────────────────────────────
header "━━━ Dry run"
log "Confirming staging — nothing written..."
echo ""
bash "$SCRIPT" --dry-run || {
    echo ""; warn "Dry run reported issues (see above)."
    warn "Config saved. Fix issues then: bash \"$SCRIPT\" --dry-run"
}

# ── Summary ───────────────────────────────────────────────────────────────────
header "━━━ Done"
echo -e "\n  ${G}${BO}✓ healthy-backup v${VERSION} configured${X}\n"
echo -e "  Config:  $CFG_FILE"
echo -e "  Backups: $ROOT"
echo -e "  Tier:    $TIER  |  Retain: $MAX  |  Upload: $UPLOAD"
[ "$INSTALL_CRON" = true ] && echo -e "  Cron:    daily ${CH}:$(printf '%02d' "$CM")" \
                           || echo -e "  Cron:    not installed (re-run setup.sh to add)"
echo ""
echo -e "  Run:     ${Y}bash \"$SCRIPT\"${X}"
echo -e "  Verify:  ${Y}bash \"$SCRIPT\" --verify \"$ROOT\"${X}"
echo -e "  Reconf:  ${Y}bash \"$SD/setup.sh\"${X}"
echo ""

# END OF FILE — setup.sh v1.3.0
