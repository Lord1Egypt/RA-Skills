#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  render-vhost.sh --server-name NAME --docroot /absolute/docroot [--error-log PATH] [--access-log PATH]
EOF
}

SERVER_NAME=""
DOCROOT=""
ERROR_LOG=""
ACCESS_LOG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --server-name) SERVER_NAME="${2:-}"; shift 2 ;;
    --docroot) DOCROOT="${2:-}"; shift 2 ;;
    --error-log) ERROR_LOG="${2:-}"; shift 2 ;;
    --access-log) ACCESS_LOG="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

[[ -n "$SERVER_NAME" && -n "$DOCROOT" ]] || { usage; exit 1; }
[[ "$DOCROOT" = /* ]] || { echo "docroot must be absolute" >&2; exit 1; }

ERROR_LOG="${ERROR_LOG:-/private/var/log/apache2/${SERVER_NAME}_error.log}"
ACCESS_LOG="${ACCESS_LOG:-/private/var/log/apache2/${SERVER_NAME}_access.log}"

cat <<EOF
<VirtualHost *:80>
    ServerName ${SERVER_NAME}
    DocumentRoot "${DOCROOT}"

    <Directory "${DOCROOT}">
        AllowOverride All
        Options Indexes FollowSymLinks
        Require all granted
    </Directory>

    ErrorLog "${ERROR_LOG}"
    CustomLog "${ACCESS_LOG}" common
</VirtualHost>
EOF
