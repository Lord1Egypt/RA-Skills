#!/usr/bin/env bash
set -euo pipefail

export PATH=/usr/bin:/bin:/usr/sbin:/sbin

echo "=== remote login ==="
systemsetup -getremotelogin 2>/dev/null || echo "systemsetup unavailable"
echo
echo "=== sshd launchd ==="
launchctl print system/com.openssh.sshd 2>/dev/null | sed -n '1,40p' || echo "sshd launchd service not readable"
echo
echo "=== port 22 ==="
if nc -z 127.0.0.1 22 2>/dev/null; then
  echo "port 22 open"
else
  echo "port 22 closed"
fi
echo
echo "=== sftp binary ==="
command -v sftp
