#!/usr/bin/env bash
set -euo pipefail

export PATH=/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

echo "=== apache ==="
apachectl -v 2>/dev/null || /usr/sbin/httpd -v 2>/dev/null || echo "apache: missing"
echo
echo "=== apache config ==="
if [[ -f /etc/apache2/httpd.conf ]]; then
  grep -n '^#*Include /private/etc/apache2/extra/httpd-vhosts.conf\|^#*LoadModule php_module\|^DirectoryIndex' /etc/apache2/httpd.conf || true
else
  echo "/etc/apache2/httpd.conf missing"
fi
echo
echo "=== brew formulae ==="
for f in php mariadb nginx; do
  brew info "$f" 2>/dev/null | sed -n '1,26p' || echo "$f: not installed"
  echo
done
echo "=== brew services ==="
brew services list | egrep 'php|mariadb|nginx' || true
