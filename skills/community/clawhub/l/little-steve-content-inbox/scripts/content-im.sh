#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INBOX="$BASE_DIR/scripts/inbox.sh"
INPUT="${*:-}"

trim() {
  echo "$1" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g'
}

extract_id() {
  echo "$1" | sed -nE 's/.*#?([0-9]+).*/\1/p'
}

msg="$(trim "$INPUT")"

if [[ -z "$msg" ]]; then
  echo "Usage: content-im.sh \"未读列表|更多|收藏 #3|收录 <url/text>\"" >&2
  exit 1
fi

case "$msg" in
  "未读列表"|"unread"|"unread list")
    bash "$INBOX" list --status unread ;;
  "已读列表"|"read"|"read list")
    bash "$INBOX" list --status read ;;
  "收藏列表"|"starred"|"starred list")
    bash "$INBOX" list --status starred ;;
  "内容列表"|"列表"|"all"|"all list"|"收件箱"|"inbox")
    bash "$INBOX" list --status all ;;
  "更多"|"more")
    bash "$INBOX" more ;;
  *)
    # status updates: 已读 #3, read #3
    if [[ "$msg" =~ ^(已读|read)[[:space:]]*#?[0-9]+$ ]]; then
      bash "$INBOX" status --id "$(extract_id "$msg")" --status read
    elif [[ "$msg" =~ ^(未读|unread)[[:space:]]*#?[0-9]+$ ]]; then
      bash "$INBOX" status --id "$(extract_id "$msg")" --status unread
    elif [[ "$msg" =~ ^(收藏|star)[[:space:]]*#?[0-9]+$ ]]; then
      bash "$INBOX" status --id "$(extract_id "$msg")" --status starred
    elif [[ "$msg" =~ ^(取消收藏|unstar)[[:space:]]*#?[0-9]+$ ]]; then
      bash "$INBOX" status --id "$(extract_id "$msg")" --status unread
    # view: 查看 #3, view #3
    elif [[ "$msg" =~ ^(查看|view)[[:space:]]*#?[0-9]+$ ]]; then
      bash "$INBOX" view --id "$(extract_id "$msg")"
    # delete: 删除 #3, remove #3
    elif [[ "$msg" =~ ^(删除|remove|delete)[[:space:]]*#?[0-9]+$ ]]; then
      bash "$INBOX" delete --id "$(extract_id "$msg")"
    # add: 收录 <url or text>
    elif [[ "$msg" =~ ^(收录|add)[[:space:]]+(.+)$ ]]; then
      payload="${BASH_REMATCH[2]}"
      url=$(echo "$payload" | grep -oE 'https?://[^ ]+' | head -n1 || true)
      if [[ -n "$url" ]]; then
        title=$(echo "$payload" | sed "s|$url||" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')
        [[ -z "$title" ]] && title="$url"
        bash "$INBOX" add --type link --title "$title" --url "$url"
      else
        title=$(echo "$payload" | awk '{print substr($0,1,80)}')
        bash "$INBOX" add --type note --title "$title" --content "$payload"
      fi
    else
      echo "UNSUPPORTED_COMMAND: $msg" >&2
      echo "Try: 未读列表 | 已读列表 | 收藏列表 | 内容列表 | 更多 | 收藏 #3 | 已读 #3 | 查看 #3 | 删除 #3 | 收录 <url/text>" >&2
      exit 2
    fi
    ;;
esac
