#!/usr/bin/env bash
set -euo pipefail

password="${RBW_REMOTE_UNLOCK_PASSWORD-}"
password_fifo="${PASSWORD_FIFO:-/tmp/rbw-remote-unlock-password.fifo}"

assuan_escape() {
  local s="${1-}"
  s=${s//%/%25}
  s=${s//$'\r'/%0D}
  s=${s//$'\n'/%0A}
  printf '%s' "$s"
}

reply_ok() {
  printf 'OK\n'
}

reply_err() {
  local code="${1:-83886179}"
  local message="${2:-Operation cancelled}"
  printf 'ERR %s %s\n' "$code" "$message"
}

printf 'OK pinentry replacement ready\n'

while IFS= read -r line; do
  cmd=${line%% *}
  arg=""
  if [[ "$line" == *" "* ]]; then
    arg=${line#* }
  fi

  case "$cmd" in
    GETPIN)
      if [[ -z "$password" && -p "$password_fifo" ]]; then
        IFS= read -r -t 10 password < "$password_fifo" || true
      fi

      if [[ -n "$password" ]]; then
        printf 'D %s\n' "$(assuan_escape "$password")"
        reply_ok
      else
        reply_err 83886179 'No password available for pinentry'
      fi
      ;;
    GETINFO)
      case "$arg" in
        pid)
          printf 'D %s\n' "$$"
          reply_ok
          ;;
        version)
          printf 'D rbw-remote-unlock-pinentry 1.0\n'
          reply_ok
          ;;
        flavor)
          printf 'D pinentry\n'
          reply_ok
          ;;
        ttyinfo)
          printf 'D not-a-tty\n'
          reply_ok
          ;;
        *)
          reply_err 67109144 "Unknown GETINFO key"
          ;;
      esac
      ;;
    OPTION|SETDESC|SETPROMPT|SETTITLE|SETOK|SETNOTOK|SETCANCEL|SETERROR|SETREPEAT|SETREPEATERROR|SETTIMEOUT|SETQUALITYBAR|SETQUALITYBAR_TT|SETGENPIN|SETGENPIN_TT|SETKEYINFO)
      reply_ok
      ;;
    CONFIRM|MESSAGE)
      reply_ok
      ;;
    BYE)
      reply_ok
      exit 0
      ;;
    *)
      # Be permissive: some clients send extra pinentry commands.
      # Treat unknown commands as OK to avoid breaking the unlock flow.
      reply_ok
      ;;
  esac
done
