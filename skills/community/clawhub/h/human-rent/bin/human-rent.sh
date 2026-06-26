#!/bin/bash
# Human-Rent CLI Wrapper
# This wrapper ensures ClawHub compatibility by providing a clear text-based entry point

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Execute the Node.js implementation
exec node "$SCRIPT_DIR/human-rent.js" "$@"
