#!/bin/bash
# Memphis Cognitive Engine Wrapper
# Thin wrapper around Memphis CLI commands

set -e

MEMPHIS_CLI="memphis"

# Check if Memphis CLI is installed
if ! command -v $MEMPHIS_CLI &> /dev/null; then
    echo "❌ Error: Memphis CLI not found"
    echo "Install: npm install -g @elathoxu-crypto/memphis"
    exit 1
fi

# Pass all arguments to Memphis CLI
exec $MEMPHIS_CLI "$@"
