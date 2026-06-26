#!/bin/bash
# enable_ssh.sh - Enable SSH for remote management
# Turns this Mac into a remotely manageable AI compute node

set -e

echo "=============================="
echo "  SSH Remote Access Setup"
echo "=============================="
echo ""

# Check current SSH status
echo "Checking current SSH status..."
ssh_status=$(sudo systemsetup -getremotelogin 2>/dev/null || echo "Unknown")
echo "Current: $ssh_status"
echo ""

# Enable SSH
echo "Enabling Remote Login (SSH)..."
if sudo systemsetup -setremotelogin on 2>/dev/null; then
    echo "  -> SSH enabled successfully"
else
    echo "  -> Failed to enable SSH (needs sudo)"
    echo "  -> You can enable manually: System Settings > General > Sharing > Remote Login"
    exit 1
fi

# Get connection info
echo ""
echo "--- Connection Info ---"

# Get username
USERNAME=$(whoami)
echo "Username: $USERNAME"

# Get IP addresses
echo ""
echo "Local IP addresses:"
ifconfig 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | awk '{print "  " $2}'

# Get hostname
HOSTNAME=$(hostname)
echo ""
echo "Hostname: $HOSTNAME"

echo ""
echo "--- Connect with ---"
echo ""

# Show all possible connection strings
for ip in $(ifconfig 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}'); do
    echo "  ssh ${USERNAME}@${ip}"
done
echo "  ssh ${USERNAME}@${HOSTNAME}"

echo ""
echo "--- For AI Node Cluster ---"
echo ""
echo "Add this to your control machine's ~/.ssh/config:"
echo ""
echo "  Host mac-ai-node"
echo "    HostName $(ifconfig 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | head -1)"
echo "    User ${USERNAME}"
echo "    ForwardAgent yes"

echo ""
echo "=============================="
echo "  SSH setup complete"
echo "=============================="
