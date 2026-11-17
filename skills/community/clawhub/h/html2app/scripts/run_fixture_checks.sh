#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "$0")/.." && pwd)"
work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

static_dir="$work_dir/static-multi-page"
storage_dir="$work_dir/local-storage"
remote_dir="$work_dir/remote-backend"
mkdir -p "$static_dir/assets" "$storage_dir" "$remote_dir"

printf '%s\n' '<link rel="stylesheet" href="assets/site.css"><a href="about.html">About</a>' > "$static_dir/index.html"
printf '%s\n' '<a href="index.html">Home</a><script src="assets/site.js"></script>' > "$static_dir/about.html"
printf '%s\n' 'body { color: #173; }' > "$static_dir/assets/site.css"
printf '%s\n' 'console.log("local asset loaded")' > "$static_dir/assets/site.js"

printf '%s\n' '{"name":"local-notes","main":"main.cjs"}' > "$storage_dir/package.json"
printf '%s\n' "const { app } = require('electron'); const db = app.getPath('userData') + '/notes.json';" > "$storage_dir/main.cjs"
printf '%s\n' "contextBridge.exposeInMainWorld('notes', { list: () => ipcRenderer.invoke('notes:list') });" > "$storage_dir/preload.cjs"

printf '%s\n' '<script>fetch("https://api.example.test/notes")</script>' > "$remote_dir/index.html"

static_out="$($skill_dir/scripts/inspect_web_app.sh "$static_dir")"
storage_out="$($skill_dir/scripts/inspect_web_app.sh "$storage_dir")"
remote_out="$($skill_dir/scripts/inspect_web_app.sh "$remote_dir")"

grep -q 'index.html' <<< "$static_out"
grep -q 'about.html' <<< "$static_out"
! grep -q 'https\?://' <<< "$static_out"
grep -q 'userData' "$storage_dir/main.cjs"
grep -q 'contextBridge' "$storage_dir/preload.cjs"
grep -q 'https://api.example.test' <<< "$remote_out"

printf '%s\n' 'PASS static-multi-page'
printf '%s\n' 'PASS local-persistent-storage'
printf '%s\n' 'PASS remote-backend-detected'
