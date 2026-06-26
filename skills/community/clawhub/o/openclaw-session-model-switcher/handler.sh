#!/usr/bin/env bash
set -euo pipefail

INPUT="${*:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
SWITCH_SCRIPT="$WORKSPACE_DIR/scripts/switch-model.sh"
STATUS_SCRIPT="$WORKSPACE_DIR/scripts/model-status.sh"
LIST_SCRIPT="$WORKSPACE_DIR/scripts/list-models.sh"

if [ -z "$INPUT" ]; then
  echo "Please provide a request such as: switch to qianwen / current model / list models / restore default model"
  exit 1
fi

chmod +x "$SWITCH_SCRIPT" "$STATUS_SCRIPT" "$LIST_SCRIPT"
LOWER_INPUT="$(printf '%s' "$INPUT" | tr '[:upper:]' '[:lower:]')"

if printf '%s' "$LOWER_INPUT" | grep -Eq '当前模型|模型状态|model status|status'; then
  printf 'Run this command to check the current session model:\n%s\n' "$($STATUS_SCRIPT)"
  exit 0
fi

if printf '%s' "$LOWER_INPUT" | grep -Eq '有哪些模型|列出.*模型|看看.*模型|可用模型|available models|list models'; then
  FILTER="$(node -e '
const input = process.argv[1] || "";
const map = ["gpt", "openai", "claude", "anthropic", "qwen", "qianwen", "通义千问", "minimax"];
const found = map.find((item) => input.includes(item.toLowerCase()));
process.stdout.write(found || "");
' "$LOWER_INPUT")"
  if [ -n "$FILTER" ]; then
    "$LIST_SCRIPT" "$FILTER"
  else
    "$LIST_SCRIPT"
  fi
  exit 0
fi

if ! printf '%s' "$LOWER_INPUT" | grep -Eq '切换|切到|换成|换到|switch|model|恢复默认|取消模型切换|用回默认|default|reset'; then
  echo "I could not detect a model-switching request. Try: switch to gpt / what model am I using now / what models are available."
  exit 1
fi

SELECTION="$(node -e '
const raw = process.argv[1] || "";
let text = raw.trim();
text = text.replace(/^(请)?(帮我)?(切换到|切到|换成|换到|切换|switch to|switch)\s*/i, "");
text = text.replace(/\s*(模型)?\s*$/i, "");
process.stdout.write(text || raw.trim());
' "$INPUT")"

RESOLUTION="$($SWITCH_SCRIPT "$SELECTION")"
STATUS="$(printf '%s' "$RESOLUTION" | node -e 'const fs = require("fs"); const data = JSON.parse(fs.readFileSync(0, "utf8")); process.stdout.write(data.status || "");')"

case "$STATUS" in
  ok)
    COMMAND="$(printf '%s' "$RESOLUTION" | node -e 'const fs = require("fs"); const data = JSON.parse(fs.readFileSync(0, "utf8")); process.stdout.write(data.command || "");')"
    MODEL="$(printf '%s' "$RESOLUTION" | node -e 'const fs = require("fs"); const data = JSON.parse(fs.readFileSync(0, "utf8")); process.stdout.write(data.model || "default");')"
    if [ "$COMMAND" = "/model default" ]; then
      echo "Run this command to restore the default session model:"
      echo "$COMMAND"
      echo
      echo "Note: this clears the current session override and affects only the current session."
    else
      echo "Run this command to switch the current session model:"
      echo "$COMMAND"
      echo
      printf 'Note: this switches the current session to %s only.\n' "$MODEL"
    fi
    ;;
  ambiguous)
    PROVIDER="$(printf '%s' "$RESOLUTION" | node -e 'const fs = require("fs"); const data = JSON.parse(fs.readFileSync(0, "utf8")); process.stdout.write(data.provider || "");')"
    if [ -n "$PROVIDER" ]; then
      printf 'You can switch to these %s models:\n' "$PROVIDER"
    else
      echo "You can switch to these models:"
    fi
    printf '%s' "$RESOLUTION" | node -e '
const fs = require("fs");
const data = JSON.parse(fs.readFileSync(0, "utf8"));
(data.options || []).forEach((item, index) => {
  console.log(`${index + 1}. ${item}`);
});
'
    echo "Reply with the model name or a number."
    ;;
  error)
    SELECTION="$(printf '%s' "$RESOLUTION" | node -e 'const fs = require("fs"); const data = JSON.parse(fs.readFileSync(0, "utf8")); process.stdout.write(data.selection || "");')"
    printf 'No configured model matches "%s".\n' "$SELECTION"
    echo "I can list the models currently available in your configuration."
    exit 1
    ;;
  *)
    echo "The model switch result could not be parsed."
    exit 1
    ;;
esac
