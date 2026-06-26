#!/usr/bin/env bash
# OpenClaw Backup Script ☺️🌸
# Purpose: Sync .openclaw configuration and workspace to a Git-managed directory and push readable history.

set -euo pipefail

join_human() {
  local items=("$@")
  local count=${#items[@]}
  if [ "$count" -eq 0 ]; then
    printf ''
  elif [ "$count" -eq 1 ]; then
    printf '%s' "${items[0]}"
  elif [ "$count" -eq 2 ]; then
    printf '%s and %s' "${items[0]}" "${items[1]}"
  else
    local last="${items[$((count-1))]}"
    unset 'items[$((count-1))]'
    printf '%s, and %s' "$(IFS=', '; echo "${items[*]}")" "$last"
  fi
}

summarize_status() {
  local status_lines="$1"
  local lowered summary count
  local -a categories=()
  local -a details=()
  local -a skill_paths=()
  local skill_names='' skill_summary=''

  lowered=$(printf '%s\n' "$status_lines" | tr '[:upper:]' '[:lower:]')

  while IFS= read -r path; do
    [ -n "$path" ] && skill_paths+=("$path")
  done < <(printf '%s\n' "$lowered" | sed -n 's#.*workspace/skills/\([^/]*\)/.*#\1#p' | awk '!seen[$0]++')

  if [ ${#skill_paths[@]} -gt 0 ]; then
    skill_names=$(join_human "${skill_paths[@]}")
    if printf '%s\n' "$lowered" | grep -q 'workspace/skills/.*/scripts/'; then
      skill_summary="skills: update ${skill_names} scripts"
    else
      skill_summary="skills: update ${skill_names}"
    fi
  fi

  if printf '%s\n' "$lowered" | grep -qE '(^|[[:space:]])(openclaw\.json|identity/|devices/|cron/|extensions/|exec-approvals\.json|update-check\.json)'; then
    categories+=("config")
  fi

  if printf '%s\n' "$lowered" | grep -qE '(^|[[:space:]])(workspace/)'; then
    categories+=("workspace")
    if printf '%s\n' "$lowered" | grep -q 'workspace/archive/'; then
      details+=("archive")
    fi
  fi

  if printf '%s\n' "$lowered" | grep -qE '(^|[[:space:]])(memory/|memory\.sqlite)'; then
    categories+=("memory")
  fi

  if printf '%s\n' "$lowered" | grep -qE '(^|[[:space:]])(agents/|telegram/|delivery-queue/|canvas/|completions/)'; then
    categories+=("runtime")
  fi

  mapfile -t categories < <(printf '%s\n' "${categories[@]:-}" | awk 'NF && !seen[$0]++')
  mapfile -t details < <(printf '%s\n' "${details[@]:-}" | awk 'NF && !seen[$0]++')

  if [ -n "$skill_summary" ]; then
    printf '%s\n' "$skill_summary"
    return
  fi

  count=${#categories[@]}
  if [ "$count" -eq 0 ]; then
    summary="backup: update openclaw state"
  elif [ "$count" -eq 1 ]; then
    case "${categories[0]}" in
      workspace)
        if [ ${#details[@]} -gt 0 ]; then
          summary="workspace: update $(join_human "${details[@]}")"
        else
          summary="workspace: update workspace files"
        fi
        ;;
      config)
        summary="config: update runtime configuration"
        ;;
      memory)
        summary="memory: refresh memory data"
        ;;
      runtime)
        summary="runtime: update sessions and channel state"
        ;;
      *)
        summary="backup: update openclaw state"
        ;;
    esac
  else
    summary="backup: update $(join_human "${categories[@]}")"
  fi

  printf '%s\n' "$summary"
}

build_commit_body() {
  local status_lines="$1"
  local max_lines=12
  local count=0
  local extra=0
  local body=''
  local line code path rest old new action display

  while IFS= read -r line; do
    [ -z "$line" ] && continue
    code=$(printf '%s' "$line" | cut -c1-2)
    rest=$(printf '%s' "$line" | cut -c4-)
    action='updated'
    display="$rest"

    case "$code" in
      '??') action='added' ;;
      'A '|' A'|'AM'|'AA') action='added' ;;
      'M '|' M'|'MM'|'RM'|'MR') action='modified' ;;
      'D '|' D'|'MD'|'DM') action='deleted' ;;
      'R '|' R'|'RR')
        old=${rest%% -> *}
        new=${rest#* -> }
        action='renamed'
        if printf '%s' "$new" | grep -q '^workspace/archive/'; then
          action='archived'
          display="$old to $new"
        else
          display="$old to $new"
        fi
        ;;
      'C '|' C')
        old=${rest%% -> *}
        new=${rest#* -> }
        action='copied'
        display="$old to $new"
        ;;
      *) action='updated' ;;
    esac

    count=$((count+1))
    if [ "$count" -le "$max_lines" ]; then
      body+="- ${action} ${display}"$'\n'
    else
      extra=$((extra+1))
    fi
  done <<< "$status_lines"

  if [ "$extra" -gt 0 ]; then
    body+="- ... and ${extra} more changes"$'\n'
  fi

  body+=$'\n'
  body+="Backup run at $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
  printf '%s' "$body"
}

REPO_URL=$(openclaw config get skills.entries.openclaw-backup-restore.env.OPENCLAW_BACKUP_REPO 2>/dev/null | tr -d '"')

if [ -z "$REPO_URL" ] || [ "$REPO_URL" = "null" ]; then
    echo "Error: OPENCLAW_BACKUP_REPO is not set in openclaw.json."
    echo 'Please set it via: openclaw config set skills.entries.openclaw-backup-restore.env.OPENCLAW_BACKUP_REPO "your-git-repo-url"'
    exit 1
fi

SOURCE="${HOME}/.openclaw/"
BACKUP_DIR="${HOME}/openclaw-backup/"
LOG_FILE="/tmp/openclaw-backup.log"

echo "[$(date)] Starting OpenClaw backup to ${REPO_URL}..." | tee -a "$LOG_FILE"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "Initializing backup directory at $BACKUP_DIR..."
    mkdir -p "$BACKUP_DIR"
    cd "$BACKUP_DIR"
    git init
    git remote add origin "$REPO_URL"
else
    cd "$BACKUP_DIR"
    git remote set-url origin "$REPO_URL" || true
fi

SKILL_DIR_SHARED="${HOME}/.openclaw/skills/openclaw-backup-restore"
SKILL_DIR_WORKSPACE="${HOME}/.openclaw/workspace/skills/openclaw-backup-restore"
SKILL_DIR=""
if [ -f "${SKILL_DIR_SHARED}/.gitignore" ]; then
    SKILL_DIR="$SKILL_DIR_SHARED"
elif [ -f "${SKILL_DIR_WORKSPACE}/.gitignore" ]; then
    SKILL_DIR="$SKILL_DIR_WORKSPACE"
fi

if [ ! -f "${BACKUP_DIR}/.gitignore" ] && [ -n "$SKILL_DIR" ] && [ -f "${SKILL_DIR}/.gitignore" ]; then
    echo "Copying .gitignore from skill directory..."
    cp "${SKILL_DIR}/.gitignore" "${BACKUP_DIR}/.gitignore"
fi

rsync -av --delete \
  --exclude-from="${BACKUP_DIR}/.gitignore" \
  --exclude=".git/" \
  --exclude=".gitignore" \
  "$SOURCE" "$BACKUP_DIR"

cd "$BACKUP_DIR"
STATUS=$(git status --short)
if [ -n "$STATUS" ]; then
    COMMIT_MSG=$(summarize_status "$STATUS")
    COMMIT_BODY=$(build_commit_body "$STATUS")
    git add .
    git commit -m "$COMMIT_MSG" -m "$COMMIT_BODY"
    git push origin main
    echo "[$(date)] Changes committed and pushed successfully: $COMMIT_MSG" | tee -a "$LOG_FILE"
else
    git push origin main || true
    echo "[$(date)] No changes detected, ensuring remote is synced." | tee -a "$LOG_FILE"
fi

echo "[$(date)] Backup complete! ☺️🌸" | tee -a "$LOG_FILE"
