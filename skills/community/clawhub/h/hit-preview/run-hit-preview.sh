#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
node "$DIR/bundle.js" "$@"
