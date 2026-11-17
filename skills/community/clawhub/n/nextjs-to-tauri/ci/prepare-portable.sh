#!/usr/bin/env bash
set -euo pipefail
test -n "$APP_VERSION"
cp "src-tauri/target/release/<AppName>.exe" "<AppName>_${APP_VERSION}_x64_portable.exe"
echo "APP_VERSION=$APP_VERSION" >> "$GITHUB_ENV"
