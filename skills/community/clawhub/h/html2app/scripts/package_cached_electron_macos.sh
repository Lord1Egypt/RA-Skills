#!/usr/bin/env bash
set -euo pipefail

# Usage: package_cached_electron_macos.sh <project-dir> <electron-zip> <output-app>
project_dir="${1:?project directory is required}"
electron_zip="${2:?cached Electron zip is required}"
output_app="${3:?output .app path is required}"

[[ "$(uname -s)" == "Darwin" ]] || { echo "This fallback is macOS-only." >&2; exit 1; }
[[ -f "$electron_zip" ]] || { echo "Electron archive not found: $electron_zip" >&2; exit 1; }
[[ -f "$project_dir/package.json" ]] || { echo "Missing package.json in $project_dir" >&2; exit 1; }
[[ -f "$project_dir/main.cjs" || -f "$project_dir/main.js" ]] || { echo "Missing Electron main process." >&2; exit 1; }
[[ ! -e "$output_app" ]] || { echo "Refusing to overwrite: $output_app" >&2; exit 1; }

work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT
ditto -x -k "$electron_zip" "$work_dir"
runtime_app="$work_dir/Electron.app"
[[ -d "$runtime_app" ]] || { echo "Archive does not contain Electron.app." >&2; exit 1; }

app_name="$(node -p "const p=require(require('node:path').resolve(process.argv[1])); p.build?.productName || p.productName || p.name" "$project_dir/package.json")"
app_id="$(node -p "const p=require(require('node:path').resolve(process.argv[1])); p.build?.appId || 'com.local.' + p.name.replace(/[^a-z0-9]/gi, '').toLowerCase()" "$project_dir/package.json")"
app_version="$(node -p "require(require('node:path').resolve(process.argv[1])).version || '1.0.0'" "$project_dir/package.json")"

mkdir -p "$(dirname "$output_app")"
mv "$runtime_app" "$output_app"
mkdir -p "$output_app/Contents/Resources/app"
rsync -a \
  --exclude 'node_modules' \
  --exclude 'release' \
  --exclude '.git' \
  --exclude '.DS_Store' \
  "$project_dir/" "$output_app/Contents/Resources/app/"

if [[ -f "$project_dir/build/icon.icns" ]]; then
  cp "$project_dir/build/icon.icns" "$output_app/Contents/Resources/electron.icns"
fi

plist="$output_app/Contents/Info.plist"
/usr/libexec/PlistBuddy -c "Set :CFBundleDisplayName $app_name" "$plist"
/usr/libexec/PlistBuddy -c "Set :CFBundleName $app_name" "$plist"
/usr/libexec/PlistBuddy -c "Set :CFBundleIdentifier $app_id" "$plist"
/usr/libexec/PlistBuddy -c "Set :CFBundleShortVersionString $app_version" "$plist"
/usr/libexec/PlistBuddy -c "Set :CFBundleVersion $app_version" "$plist"
codesign --force --deep --sign - "$output_app"
codesign --verify --deep --strict --verbose=2 "$output_app"
echo "Created locally signed app: $output_app"
