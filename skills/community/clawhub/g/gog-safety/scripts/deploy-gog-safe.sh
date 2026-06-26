#!/usr/bin/env bash
#
# deploy-gog-safe.sh — Deploy a safety-profiled gog binary to a remote host
#
# Usage:
#   ./deploy-gog-safe.sh <host> <binary-path> [--verify]
#
# Examples:
#   ./deploy-gog-safe.sh spock /tmp/gogcli-safety-build/bin/gog-l1-safe
#   ./deploy-gog-safe.sh spock /tmp/gogcli-safety-build/bin/gog-l1-safe --verify
#
set -euo pipefail

HOST=""
BINARY=""
VERIFY=false

usage() {
  echo "Usage: $0 <ssh-host> <binary-path> [--verify]"
  echo ""
  echo "Deploys a gog binary to the remote host:"
  echo "  1. Backs up existing binary as gog-backup (or gog-full)"
  echo "  2. Uploads and installs the new binary"
  echo "  3. Verifies version output"
  echo "  4. Optionally runs verification tests"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --verify) VERIFY=true; shift ;;
    -h|--help) usage ;;
    *)
      if [[ -z "$HOST" ]]; then HOST="$1"
      elif [[ -z "$BINARY" ]]; then BINARY="$1"
      else echo "Unknown argument: $1"; usage; fi
      shift ;;
  esac
done

if [[ -z "$HOST" ]] || [[ -z "$BINARY" ]]; then
  echo "Error: host and binary path required"
  usage
fi

if [[ ! -f "$BINARY" ]]; then
  echo "Error: binary not found: $BINARY"
  exit 1
fi

echo "=== Deploying gog to $HOST ==="
echo "Binary: $BINARY"
echo ""

# Step 1: Check current version
echo "Current version on $HOST:"
ssh "$HOST" "gog --version 2>/dev/null || echo '(not installed)'"
echo ""

# Step 2: Upload
echo "Uploading binary..."
scp "$BINARY" "$HOST:/tmp/gog-safe-new"
echo "Upload complete."

# Step 3: Backup and swap
echo "Backing up and installing..."
ssh "$HOST" '
  if [ -f /usr/local/bin/gog ]; then
    if [ -f /usr/local/bin/gog-backup ]; then
      sudo rm -f /usr/local/bin/gog-backup
    fi
    sudo mv /usr/local/bin/gog /usr/local/bin/gog-backup
  fi
  sudo mv /tmp/gog-safe-new /usr/local/bin/gog
  sudo chmod +x /usr/local/bin/gog
'
echo "Installed."

# Step 4: Verify version
echo ""
echo "New version on $HOST:"
ssh "$HOST" "gog --version"

# Step 5: Optional verification
if $VERIFY; then
  echo ""
  echo "=== Running verification ==="

  # Test that blocked commands don't exist
  echo "Checking blocked commands..."
  BLOCKED_CMDS=("gmail send" "gmail drafts send" "chat messages send" "chat dm send")
  ALL_PASS=true

  for cmd in "${BLOCKED_CMDS[@]}"; do
    if ssh "$HOST" "gog $cmd --help 2>/dev/null" >/dev/null 2>&1; then
      echo "  FAIL: 'gog $cmd' should be blocked but exists!"
      ALL_PASS=false
    else
      echo "  OK: 'gog $cmd' is blocked"
    fi
  done

  # Test that allowed commands work
  echo "Checking allowed commands..."
  ALLOWED_CMDS=("gmail drafts create --help" "gmail labels list --help" "gmail search --help")

  for cmd in "${ALLOWED_CMDS[@]}"; do
    if ssh "$HOST" "gog $cmd 2>/dev/null" >/dev/null 2>&1; then
      echo "  OK: 'gog $cmd' is available"
    else
      echo "  FAIL: 'gog $cmd' should be available but isn't!"
      ALL_PASS=false
    fi
  done

  echo ""
  if $ALL_PASS; then
    echo "=== All verification checks passed ==="
  else
    echo "=== SOME CHECKS FAILED — review output above ==="
    exit 1
  fi
fi

echo ""
echo "=== Deployment complete ==="
echo "Backup at: /usr/local/bin/gog-backup"
echo "To rollback: ssh $HOST 'sudo mv /usr/local/bin/gog-backup /usr/local/bin/gog'"
