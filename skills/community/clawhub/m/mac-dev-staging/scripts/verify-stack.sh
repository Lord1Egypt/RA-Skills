#!/usr/bin/env bash
set -euo pipefail

export PATH=/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

echo "=== node / npm ==="
node -v
npm -v
echo
echo "=== php cli ==="
php -v | sed -n '1,2p'
echo
echo "=== php apache module ==="
ls -l /opt/homebrew/opt/php/lib/httpd/modules/libphp.so
echo
echo "=== mariadb ==="
if command -v mariadb >/dev/null 2>&1; then
  mariadb --version
else
  echo "mariadb client missing" >&2
  exit 1
fi
echo
echo "=== brew services ==="
brew services list | egrep 'php|mariadb|nginx' || true
echo
echo "=== apache local ==="
curl -Is http://127.0.0.1/ | sed -n '1,3p' || true
echo
echo "=== nginx local ==="
curl -Is http://127.0.0.1:8080/ | sed -n '1,3p' || true
echo
echo "=== expected ports ==="
"$(dirname "$0")/detect-ports.sh"
