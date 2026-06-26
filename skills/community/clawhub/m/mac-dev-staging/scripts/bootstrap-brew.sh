#!/usr/bin/env bash
set -euo pipefail

export PATH=/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

brew update
brew install node php mariadb nginx

echo
echo "Installed formulae:"
brew info node php mariadb nginx | sed -n '1,160p'
