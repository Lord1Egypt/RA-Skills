#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'
# Add these lines to /etc/apache2/httpd.conf and restart Apache:

LoadModule php_module /opt/homebrew/opt/php/lib/httpd/modules/libphp.so

<FilesMatch \.php$>
    SetHandler application/x-httpd-php
</FilesMatch>

DirectoryIndex index.php index.html

# Also enable vhosts if you want per-site hostnames:
# Include /private/etc/apache2/extra/httpd-vhosts.conf
EOF
