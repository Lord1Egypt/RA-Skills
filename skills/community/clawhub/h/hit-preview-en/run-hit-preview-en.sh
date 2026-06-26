#!/bin/bash
# Hit Preview v2.0.0 EN - Quick run script
DIR="$(cd "$(dirname "$0")" && pwd)"
node "$DIR/bundle-en.js" "$@"
