#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  capture-window-by-keyword.sh <keyword> [output_path]
  capture-window-by-keyword.sh --list <keyword>
  capture-window-by-keyword.sh --index <n> <keyword> [output_path]

Options:
  --list       List matched windows only, do not capture
  --index <n>  Choose the nth matched window (1-based)

Notes:
  - Supports keyword aliases, e.g. weixin -> wechat, wx
  - Without --index, prefers the first shareable window (sharing = 1)
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

LIST_ONLY=0
INDEX=""
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --list)
      LIST_ONLY=1
      shift
      ;;
    --index)
      [[ $# -ge 2 ]] || { usage; exit 1; }
      INDEX="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

[[ ${#POSITIONAL[@]} -ge 1 ]] || { usage; exit 1; }
KEYWORD="${POSITIONAL[0]}"
OUTPUT_PATH="${POSITIONAL[1]:-}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

if [[ -z "$OUTPUT_PATH" && "$LIST_ONLY" -eq 0 ]]; then
  OUTPUT_DIR="$(pwd)/screenshots"
  mkdir -p "$OUTPUT_DIR"
  SAFE_KEYWORD="$(printf '%s' "$KEYWORD" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-')"
  OUTPUT_PATH="$OUTPUT_DIR/${SAFE_KEYWORD:-window}-${TIMESTAMP}.png"
elif [[ -n "$OUTPUT_PATH" ]]; then
  mkdir -p "$(dirname "$OUTPUT_PATH")"
fi

if ! command -v swift >/dev/null 2>&1; then
  echo "Error: swift not found." >&2
  echo "Install Xcode Command Line Tools manually:" >&2
  echo "  xcode-select --install" >&2
  exit 2
fi

MATCH_JSON="$(swift - "$KEYWORD" <<'SWIFT'
import CoreGraphics
import Foundation

let rawKeyword = (CommandLine.arguments.dropFirst().first ?? "").lowercased()
var terms: [String] = [rawKeyword]
let aliasMap: [String: [String]] = [
    "weixin": ["wechat", "wx"],
    "wechat": ["weixin", "wx"],
    "telegram": ["tg"],
    "chrome": ["google chrome"],
    "qq": ["tencent qq"]
]
if let aliases = aliasMap[rawKeyword] {
    terms.append(contentsOf: aliases)
}
terms = Array(Set(terms.filter { !$0.isEmpty }))

let options = CGWindowListOption(arrayLiteral: .optionOnScreenOnly, .excludeDesktopElements)
let windows = (CGWindowListCopyWindowInfo(options, kCGNullWindowID) as? [[String: Any]]) ?? []

let matches = windows.compactMap { w -> [String: Any]? in
    let owner = (w[kCGWindowOwnerName as String] as? String) ?? ""
    let name = (w[kCGWindowName as String] as? String) ?? ""
    let low = (owner + " " + name).lowercased()
    guard terms.contains(where: { low.contains($0) }) else { return nil }

    return [
        "id": w[kCGWindowNumber as String] ?? "",
        "owner": owner,
        "name": name,
        "sharing": w[kCGWindowSharingState as String] ?? "",
        "bounds": w[kCGWindowBounds as String] ?? ""
    ]
}

let data = try! JSONSerialization.data(withJSONObject: matches, options: [])
print(String(data: data, encoding: .utf8)!)
SWIFT
)"

if [[ -z "$MATCH_JSON" || "$MATCH_JSON" == "[]" ]]; then
  echo "Error: no on-screen window matched keyword '$KEYWORD'." >&2
  exit 3
fi

MATCH_JSON="$MATCH_JSON" python3 - <<'PY'
import os, json
arr = json.loads(os.environ['MATCH_JSON'])
for i, item in enumerate(arr, 1):
    print(f"[{i}] id={item.get('id')} sharing={item.get('sharing')} owner={item.get('owner')} name={item.get('name')} bounds={item.get('bounds')}")
PY

if [[ "$LIST_ONLY" -eq 1 ]]; then
  exit 0
fi

WINDOW_ID="$(MATCH_JSON="$MATCH_JSON" INDEX="$INDEX" python3 - <<'PY'
import os, json, sys
arr = json.loads(os.environ['MATCH_JSON'])
idx = os.environ.get('INDEX', '').strip()
if not arr:
    raise SystemExit(1)
if idx:
    n = int(idx)
    if n < 1 or n > len(arr):
        print(f'Error: index {n} out of range (1-{len(arr)}).', file=sys.stderr)
        raise SystemExit(2)
    print(arr[n-1]['id'])
else:
    arr.sort(key=lambda x: 0 if str(x.get('sharing')) == '1' else 1)
    print(arr[0]['id'])
PY
)"

if ! screencapture -x -l "$WINDOW_ID" "$OUTPUT_PATH"; then
  echo "Error: screencapture failed for window id $WINDOW_ID." >&2
  echo "Check Screen Recording permission for the host process in macOS Settings." >&2
  exit 4
fi

if [[ ! -f "$OUTPUT_PATH" ]]; then
  echo "Error: screenshot file was not created." >&2
  exit 5
fi

echo "$OUTPUT_PATH"
