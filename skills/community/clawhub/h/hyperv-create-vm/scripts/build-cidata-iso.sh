#!/bin/bash
# Build cloud-init ISO for Hyper-V VM
# Usage: VM_PASSWORD=<pass> ./build-cidata-iso.sh <vm-name> [ssh-public-key] [extra-packages]
# Or:    echo <pass> | ./build-cidata-iso.sh <vm-name> [ssh-public-key] [extra-packages]
#
# Password is read from VM_PASSWORD env var or stdin to avoid exposure
# in process lists and shell history.

set -euo pipefail

VM_NAME="${1:?Usage: VM_PASSWORD=<pass> $0 <vm-name> [ssh-public-key] [extra-packages]}"
SSH_KEY="${2:-$(cat ~/.ssh/id_ed25519.pub 2>/dev/null || echo 'NO_KEY')}"
EXTRA_PKGS="${3:-}"

# Read password from env var or stdin (never CLI args)
if [ -n "${VM_PASSWORD:-}" ]; then
  PASSWORD="$VM_PASSWORD"
elif [ ! -t 0 ]; then
  read -r PASSWORD
else
  read -rsp "VM password: " PASSWORD
  echo
fi

if [ -z "$PASSWORD" ]; then
  echo "ERROR: No password provided. Set VM_PASSWORD or pipe via stdin." >&2
  exit 1
fi
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORK_DIR="/tmp/${VM_NAME}-cidata"
OUTPUT="/tmp/${VM_NAME}-cidata.iso"

echo "Building cloud-init ISO for: $VM_NAME"

# Generate password hash
PASS_HASH=$(python3 -c "import crypt; print(crypt.crypt('${PASSWORD}', crypt.mksalt(crypt.METHOD_SHA512)))")

# Create working directory
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

# Generate user-data from template
sed \
  -e "s|VM_NAME_PLACEHOLDER|${VM_NAME}|g" \
  -e "s|PASSWORD_HASH_PLACEHOLDER|${PASS_HASH}|g" \
  -e "s|SSH_KEY_PLACEHOLDER|${SSH_KEY}|g" \
  "$SCRIPT_DIR/cloud-init-user-data.yaml" > "$WORK_DIR/user-data"

# Add extra packages if specified
if [ -n "$EXTRA_PKGS" ]; then
  for pkg in $(echo "$EXTRA_PKGS" | tr ',' ' '); do
    echo "  - $pkg" >> "$WORK_DIR/user-data"
  done
fi

# Generate meta-data from template
sed "s|VM_NAME_PLACEHOLDER|${VM_NAME}|g" \
  "$SCRIPT_DIR/cloud-init-meta-data.yaml" > "$WORK_DIR/meta-data"

# Copy network config
cp "$SCRIPT_DIR/cloud-init-network-config.yaml" "$WORK_DIR/network-config"

# Build ISO
genisoimage -output "$OUTPUT" -volid cidata -joliet -rock \
  "$WORK_DIR/user-data" "$WORK_DIR/meta-data" "$WORK_DIR/network-config"

echo "ISO created: $OUTPUT"
echo "SCP to Hyper-V host: scp $OUTPUT hyperv-host:C:/Users/youruser/Downloads/"
