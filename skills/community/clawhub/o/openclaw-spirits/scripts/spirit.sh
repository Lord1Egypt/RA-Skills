#!/usr/bin/env bash
# OpenClaw Spirits — CLI entry point
# No network calls. No env sniffing. Writes only to assets/.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPANION_FILE="$SCRIPT_DIR/../assets/companion.json"
LANG="zh"
CMD="show"
CMD_ARGS=()

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --lang) LANG="$2"; shift 2 ;;
    --lang=*) LANG="${1#*=}"; shift ;;
    summon|show|stats|rename) CMD="$1"; shift ;;
    *) CMD_ARGS+=("$1"); shift ;;
  esac
done

case "$CMD" in
  summon)
    if [[ -f "$COMPANION_FILE" ]]; then
      has_personality=$(node -e "const c=JSON.parse(require('fs').readFileSync('$COMPANION_FILE','utf8'));process.stdout.write(c.personality||'')" 2>/dev/null)
      if [[ -n "$has_personality" ]]; then
        echo "⚠️  Spirit already hatched. Use 'spirit show' to see it."
        exit 0
      fi
    else
      echo "❌ No companion file found. Run generate.js first to create bones."
      echo "   Then use soul.js prompt + save to complete the companion."
      exit 1
    fi

    echo ""
    echo "🥚 ..."
    echo "🥚 ... ..."
    echo "✨ A spirit emerges!"
    echo ""

    node "$SCRIPT_DIR/display.js" "$COMPANION_FILE" "$LANG"
    ;;

  show)
    if [[ ! -f "$COMPANION_FILE" ]]; then
      echo "❌ No spirit found. Complete the summoning flow first."
      exit 1
    fi
    node "$SCRIPT_DIR/display.js" "$COMPANION_FILE" "$LANG"
    ;;

  stats)
    if [[ ! -f "$COMPANION_FILE" ]]; then
      echo "❌ No spirit found."
      exit 1
    fi
    node -e "const c=JSON.parse(require('fs').readFileSync('$COMPANION_FILE','utf8'));Object.entries(c.stats).forEach(([k,v])=>console.log(k+': '+v))"
    ;;

  rename)
    if [[ ! -f "$COMPANION_FILE" ]]; then
      echo "❌ No spirit found."
      exit 1
    fi
    new_name="${CMD_ARGS[0]}"
    if [[ -z "$new_name" ]]; then
      echo "Usage: spirit rename <new-name>"
      exit 1
    fi
    node -e "
      const fs=require('fs');
      const c=JSON.parse(fs.readFileSync('$COMPANION_FILE','utf8'));
      c.name=$(printf '%q' "$new_name");
      fs.writeFileSync('$COMPANION_FILE',JSON.stringify(c,null,2));
    "
    echo "✅ Renamed to: $new_name"
    ;;

  *)
    echo "OpenClaw Spirits — Your companion spirit"
    echo ""
    echo "Commands:"
    echo "  spirit show          Show your spirit card"
    echo "  spirit summon        First-time hatching"
    echo "  spirit stats         Show detailed stats"
    echo "  spirit rename <name> Rename your spirit"
    echo ""
    echo "Options:"
    echo "  --lang zh|en         Display language (default: zh)"
    echo ""
    echo "Your spirit is deterministic and soul-bound."
    ;;
esac
