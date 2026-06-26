#!/bin/bash
# Kindle Claude Monitor — uninstall script
# 停 launchd、删 plist、从 settings.json 移除 7 个 kindle 钩子。
# 不删 ~/.claude/kindle-monitor/events.jsonl 历史日志。

set -e

RUNTIME_DIR="$HOME/.claude/kindle-monitor"
PLIST_DST="$HOME/Library/LaunchAgents/com.user.kindle-monitor.plist"
SETTINGS="$HOME/.claude/settings.json"

echo "==> 停止 launchd 服务"
launchctl unload "$PLIST_DST" 2>/dev/null || true

echo "==> 删除 plist"
rm -f "$PLIST_DST"

echo "==> 从 settings.json 移除 kindle 钩子"
if [ -f "$SETTINGS" ]; then
  cp "$SETTINGS" "$SETTINGS.bak.$(date +%Y%m%d-%H%M%S)"
  python3 <<PY
import json
p = "$SETTINGS"
with open(p) as f:
    cfg = json.load(f)
hooks = cfg.get("hooks", {})
removed = 0
for cat, entries in list(hooks.items()):
    new_entries = []
    for entry in entries:
        new_hooks = [h for h in entry.get("hooks", [])
                     if "kindle-monitor/notify.sh" not in (h.get("command") or "")]
        if new_hooks:
            new_entries.append({**entry, "hooks": new_hooks})
        elif entry.get("hooks"):
            removed += len(entry["hooks"])
    if new_entries:
        hooks[cat] = new_entries
    else:
        del hooks[cat]
with open(p, "w") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
print(f"    移除 {removed} 个 hook entry")
PY
fi

echo "==> 删除运行时文件"
rm -f "$RUNTIME_DIR/server.py" "$RUNTIME_DIR/notify.sh"
echo "    保留: $RUNTIME_DIR/events.jsonl (历史日志)"

cat <<EOF

==================================================
✅ Kindle Claude Monitor 已卸载

仍保留:
  - $RUNTIME_DIR/events.jsonl  (历史事件日志)
  - settings.json 备份         (自动建)

如需彻底清理:
  rm -rf $RUNTIME_DIR
==================================================
EOF
