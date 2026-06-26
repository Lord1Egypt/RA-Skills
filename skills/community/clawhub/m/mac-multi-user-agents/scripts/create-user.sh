#!/usr/bin/env bash
set -euo pipefail

USER_NAME=""
FULL_NAME=""
ADMIN="no"
SHELL_PATH="/bin/zsh"
PASSWORD_ENV=""
DRY_RUN="no"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --user) USER_NAME="${2:-}"; shift 2 ;;
    --full-name) FULL_NAME="${2:-}"; shift 2 ;;
    --admin) ADMIN="${2:-}"; shift 2 ;;
    --shell) SHELL_PATH="${2:-}"; shift 2 ;;
    --password-env) PASSWORD_ENV="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN="yes"; shift 1 ;;
    -h|--help)
      echo "usage: create-user.sh --user agent3 --full-name \"Agent 3\" --password-env ENVVAR [--admin yes|no] [--shell /bin/zsh] [--dry-run]"
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$USER_NAME" || -z "$FULL_NAME" || -z "$PASSWORD_ENV" ]]; then
  echo "missing required arguments" >&2
  exit 1
fi

PASSWORD="${!PASSWORD_ENV:-}"
if [[ -z "$PASSWORD" ]]; then
  echo "password env is empty: $PASSWORD_ENV" >&2
  exit 1
fi

if dscl . -read "/Users/$USER_NAME" >/dev/null 2>&1; then
  echo "user already exists: $USER_NAME" >&2
  exit 1
fi

create_cmd=(sudo sysadminctl -addUser "$USER_NAME" -fullName "$FULL_NAME" -shell "$SHELL_PATH" -password "$PASSWORD")

if [[ "$DRY_RUN" == "yes" ]]; then
  printf '%q ' "${create_cmd[@]}"
  echo
  if [[ "$ADMIN" == "yes" ]]; then
    echo "sudo dseditgroup -o edit -a \"$USER_NAME\" -t user admin"
  fi
  echo "sudo -u \"$USER_NAME\" mkdir -p \"/Users/$USER_NAME/.ssh\" \"/Users/$USER_NAME/.openclaw\""
  echo "sudo -u \"$USER_NAME\" chmod 700 \"/Users/$USER_NAME/.ssh\""
  echo "sudo -u \"$USER_NAME\" /bin/zsh -lc 'grep -q /opt/homebrew/bin ~/.zprofile 2>/dev/null || printf \"\\nexport PATH=/opt/homebrew/bin:/opt/homebrew/sbin:\\$PATH\\n\" >> ~/.zprofile'"
  exit 0
fi

"${create_cmd[@]}"

if [[ "$ADMIN" == "yes" ]]; then
  sudo dseditgroup -o edit -a "$USER_NAME" -t user admin
fi

sudo -u "$USER_NAME" mkdir -p "/Users/$USER_NAME/.ssh" "/Users/$USER_NAME/.openclaw"
sudo -u "$USER_NAME" chmod 700 "/Users/$USER_NAME/.ssh"
sudo -u "$USER_NAME" /bin/zsh -lc 'grep -q /opt/homebrew/bin ~/.zprofile 2>/dev/null || printf "\nexport PATH=/opt/homebrew/bin:/opt/homebrew/sbin:\$PATH\n" >> ~/.zprofile'

echo "created user: $USER_NAME"
