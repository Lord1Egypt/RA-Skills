#!/usr/bin/env bash
set -euo pipefail

export PATH=/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

DEFAULT_PORTS=(22 80 443 3306 8080 18789 18800 28789 3000 5173)
PORTS=("${DEFAULT_PORTS[@]}")

if [ "$#" -gt 0 ]; then
  PORTS+=("$@")
fi

deduped_ports=()
seen=" "
for port in "${PORTS[@]}"; do
  case "$port" in
    ''|*[!0-9]*)
      echo "invalid port: $port" >&2
      exit 1
      ;;
  esac
  if [[ "$seen" != *" $port "* ]]; then
    deduped_ports+=("$port")
    seen="$seen$port "
  fi
done

printf "%-8s %-10s %s\n" "PORT" "STATE" "DETAIL"
for port in "${deduped_ports[@]}"; do
  if command -v lsof >/dev/null 2>&1; then
    detail="$(lsof -nP -iTCP:"$port" -sTCP:LISTEN 2>/dev/null | awk 'NR>1 {print $1 " pid=" $2 " user=" $3}' | paste -sd '; ' -)"
  else
    detail="$(netstat -anv -p tcp 2>/dev/null | awk -v p=".$port" '$4 ~ p && $6 == "LISTEN" {print $4}' | paste -sd '; ' -)"
  fi

  if [ -n "$detail" ]; then
    printf "%-8s %-10s %s\n" "$port" "IN_USE" "$detail"
  else
    printf "%-8s %-10s %s\n" "$port" "FREE" "-"
  fi
done
