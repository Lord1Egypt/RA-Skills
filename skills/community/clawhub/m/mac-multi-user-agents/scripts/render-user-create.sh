#!/usr/bin/env bash
set -euo pipefail

USER_NAME=""
FULL_NAME=""
ADMIN="no"
SHELL_PATH="/bin/zsh"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --user) USER_NAME="${2:-}"; shift 2 ;;
    --full-name) FULL_NAME="${2:-}"; shift 2 ;;
    --admin) ADMIN="${2:-}"; shift 2 ;;
    --shell) SHELL_PATH="${2:-}"; shift 2 ;;
    -h|--help)
      echo "usage: render-user-create.sh --user agent3 --full-name \"Agent 3\" [--admin yes|no] [--shell /bin/zsh]"
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$USER_NAME" || -z "$FULL_NAME" ]]; then
  echo "missing --user or --full-name" >&2
  exit 1
fi

cat <<EOF
# Create user
sudo sysadminctl -addUser "$USER_NAME" -fullName "$FULL_NAME" -shell "$SHELL_PATH" -password -

# Optional admin promotion
$( [ "$ADMIN" = "yes" ] && echo "sudo dseditgroup -o edit -a \"$USER_NAME\" -t user admin" || echo "# no admin promotion requested" )

# Bootstrap per-user runtime
sudo -u "$USER_NAME" mkdir -p "/Users/$USER_NAME/.ssh" "/Users/$USER_NAME/.openclaw"
sudo -u "$USER_NAME" chmod 700 "/Users/$USER_NAME/.ssh"

# Ensure shared toolchain PATH
sudo -u "$USER_NAME" /bin/zsh -lc 'grep -q /opt/homebrew/bin ~/.zprofile 2>/dev/null || printf "\\nexport PATH=/opt/homebrew/bin:/opt/homebrew/sbin:\\$PATH\\n" >> ~/.zprofile'
EOF
