#!/bin/bash
# audit-session-bridge-and-share-fallback.sh
#
# 5/2 zhaobo 失忆 + 大文件兜底事故修复后的 2-week followup 审计脚本。
# 修复发布于：
#   - @huo15/openclaw-enhance v5.7.26（src/modules/session-bridge.ts）
#   - @huo15/wecom v2.8.15（src/share-fallback.ts）
# 配套 KB 复盘：~/knowledge/huo15/2026-05-02-zhaobo-amnesia-session-bridge-and-wecom-share-fallback.md
#
# 脚本职责：
#   1. 扫 ~/.openclaw/logs/gateway.log 看 session-bridge 触发情况
#   2. 扫 ~/.openclaw/share/manifest.json 看 wecom share-fallback 落盘情况
#   3. 没触发时进 ~/.openclaw/logs/gateway.err.log 找失败痕迹
#   4. 综合写报告到 ~/knowledge/huo15/<date>-session-bridge-and-share-fallback-2week-followup.md
#
# 使用：
#   - 由 LaunchAgent ai.huo15.openclaw.session-bridge-2week-followup 在 2026-05-16 09:30 +08 自动触发
#   - 内置日期 guard：只有 $TARGET_DATE 当天才真正跑（防 plist 残留误触发）
#   - 也可手动跑：FORCE=1 bash scripts/audit-session-bridge-and-share-fallback.sh
#
# 红线：纯只读 + 写自有 KB 路径，零 child_process（mac 默认 grep / jq / awk 都 ok）

set -uo pipefail

TARGET_DATE="${TARGET_DATE:-2026-05-16}"
TODAY="$(date +%Y-%m-%d)"
FORCE="${FORCE:-0}"

if [[ "$FORCE" != "1" && "$TODAY" != "$TARGET_DATE" ]]; then
  echo "[audit] skip: today=$TODAY != target=$TARGET_DATE (set FORCE=1 to override)" >&2
  exit 0
fi

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
GATEWAY_LOG="$OPENCLAW_HOME/logs/gateway.log"
GATEWAY_ERR_LOG="$OPENCLAW_HOME/logs/gateway.err.log"
SHARE_MANIFEST="$OPENCLAW_HOME/share/manifest.json"

KB_DIR="$HOME/knowledge/huo15"
KB_FILE="$KB_DIR/${TODAY}-session-bridge-and-share-fallback-2week-followup.md"

# 修复发布锚点（早于此时间戳的不算——避免老日志干扰）
ANCHOR_ISO="2026-05-02T00:00:00"
ANCHOR_EPOCH="$(date -j -f "%Y-%m-%dT%H:%M:%S" "$ANCHOR_ISO" "+%s" 2>/dev/null || echo 0)"

mkdir -p "$KB_DIR"

# 安全计数：mac 上 grep -c 没匹配会返回 1+stderr 0；包一层确保返回单行整数
safe_count() {
  local pattern="$1"
  local file="$2"
  if [[ ! -f "$file" ]]; then echo 0; return; fi
  local n
  n="$(grep -c "$pattern" "$file" 2>/dev/null | head -1 | tr -dc '0-9')"
  echo "${n:-0}"
}

# percentile：从 stdin 读一列数字，输出 p50/p95（mac awk 兼容）
percentile() {
  local pct="$1"   # 0.5 / 0.95
  sort -n | awk -v p="$pct" 'BEGIN{c=0} {a[c++]=$1} END{
    if(c==0) {print "?"; exit}
    i=int(c*p); if(i>=c) i=c-1
    print a[i]
  }'
}

# ── 1. session-bridge 触发统计 ──────────────────────────────────────────────
section_session_bridge() {
  local total=0
  local sample=""
  local sessionkey_count=""
  local idle_p50="?" idle_p95="?"
  local msgcount_p50="?" msgcount_p95="?"
  local char_p50="?" char_p95="?"

  if [[ ! -f "$GATEWAY_LOG" ]]; then
    echo "**状态**：未找到 \`$GATEWAY_LOG\`（openclaw 可能没启动过 / 日志被清理）"
    return
  fi

  total="$(safe_count '\[enhance-session-bridge\] 桥接 prior=' "$GATEWAY_LOG")"
  if [[ "$total" -eq 0 ]]; then
    echo "**状态**：自部署以来 **0 次触发**"
    echo ""
    echo "可能原因排查："
    echo "- idle 阈值 75min 太严？默认 \`bridgeIdleMinutes=75\`，可调到 30"
    echo "- chat_id 匹配失败？看 \`$GATEWAY_LOG\` 是否有 \`[enhance] session-bridge 已加载\` 行"
    echo "- fresh size 200KB 太严？wecom DM 重连后第一条进来时 jsonl 已经超过 200KB 就不会触发"
    echo "- 日志的 \`debug=true\` 没开：默认 debug 不打日志，只有命中才 logger.info"
    echo ""
    echo "**建议下一步**：临时打开 \`enhance.sessionBridge.debug=true\` 观察一周，再看是否调阈值。"
    return
  fi

  sample="$(grep '\[enhance-session-bridge\] 桥接 prior=' "$GATEWAY_LOG" | tail -10)"
  sessionkey_count="$(grep '\[enhance-session-bridge\] 桥接 prior=' "$GATEWAY_LOG" \
    | grep -oE 'sessionKey=[^ ]+' \
    | sort | uniq -c | sort -rn | head -10)"

  # idle 与 msg count 用 awk 统计 p50 / p95
  local stats
  stats="$(grep '\[enhance-session-bridge\] 桥接 prior=' "$GATEWAY_LOG" \
    | awk '{
        match($0, /\(([0-9]+) msg, ([0-9]+) 字符\)/, a);
        match($0, /idle=([0-9]+)min/, b);
        if (a[1] != "" && b[1] != "") print a[1], a[2], b[1]
      }')"

  if [[ -n "$stats" ]]; then
    msgcount_p50="$(echo "$stats" | awk '{print $1}' | sort -n | awk 'BEGIN{c=0} {a[c++]=$1} END{if(c){print a[int(c*0.5)]}}')"
    msgcount_p95="$(echo "$stats" | awk '{print $1}' | sort -n | awk 'BEGIN{c=0} {a[c++]=$1} END{if(c){print a[int(c*0.95)]}}')"
    idle_p50="$(echo "$stats" | awk '{print $3}' | sort -n | awk 'BEGIN{c=0} {a[c++]=$1} END{if(c){print a[int(c*0.5)]}}')"
    idle_p95="$(echo "$stats" | awk '{print $3}' | sort -n | awk 'BEGIN{c=0} {a[c++]=$1} END{if(c){print a[int(c*0.95)]}}')"
  fi

  echo "**状态**：触发 **$total 次**"
  echo ""
  echo "**统计**："
  echo "- msg count（注入了多少条消息）p50=$msgcount_p50, p95=$msgcount_p95（max=8）"
  echo "- idle（距上次会话 reset 的分钟数）p50=${idle_p50}min, p95=${idle_p95}min"
  echo ""
  echo "**sessionKey 分布（Top 10）**："
  echo '```'
  echo "$sessionkey_count"
  echo '```'
  echo ""
  echo "**最近 10 次触发 sample**："
  echo '```'
  echo "$sample"
  echo '```'
}

# ── 2. wecom share-fallback 落盘统计 ────────────────────────────────────────
section_share_fallback() {
  if [[ ! -f "$SHARE_MANIFEST" ]]; then
    echo "**状态**：未找到 \`$SHARE_MANIFEST\`（说明 enhance bot-share 模块从未生成过任何分享，无论是 LLM 主动调还是 wecom 兜底）"
    echo ""
    echo "**建议下一步**：手动测试一次——在 wecom DM 给 zhaobo 发一个 30MB 的视频文件，看是否触发 share-fallback。"
    return
  fi

  if ! command -v jq >/dev/null 2>&1; then
    echo "**状态**：jq 未安装；只能给 raw 统计。"
    local entry_count
    entry_count="$(safe_count '"token"' "$SHARE_MANIFEST")"
    echo "- manifest 总 entry 数（含 enhance 自己生成的）：约 $entry_count"
    echo ""
    echo "**建议下一步**：\`brew install jq\` 后重跑 FORCE=1 bash $0"
    return
  fi

  local total wecom_total wecom_recent
  total="$(jq '.entries | length' "$SHARE_MANIFEST" 2>/dev/null || echo 0)"
  wecom_total="$(jq '[.entries[] | select(.sourcePath | tostring | startswith("[wecom-fallback"))] | length' "$SHARE_MANIFEST" 2>/dev/null || echo 0)"
  wecom_recent="$(jq --arg anchor "$ANCHOR_ISO" \
    '[.entries[] | select(.sourcePath | tostring | startswith("[wecom-fallback")) | select(.createdAt >= $anchor)]' \
    "$SHARE_MANIFEST" 2>/dev/null || echo "[]")"
  local wecom_recent_count
  wecom_recent_count="$(echo "$wecom_recent" | jq 'length' 2>/dev/null || echo 0)"

  echo "**状态**：manifest 共 **$total** 条 entry；其中 wecom 兜底 **$wecom_total** 条；自 5/2 以来 **$wecom_recent_count** 条"
  echo ""

  if [[ "$wecom_recent_count" -eq 0 ]]; then
    echo "**warning**：自部署以来 wecom 兜底 0 次。可能原因："
    echo "- 这两周没人发过 > 20MB 文件"
    echo "- size 检查路径走的不是 bot-ws/media.ts（可能走 agent-api/core.ts，目前 v2.8.15 没接）"
    echo "- shareFallback 写盘失败（看 err log 章节）"
    echo ""
  else
    echo "**最近兜底文件**："
    echo "$wecom_recent" | jq -r '.[] | "- \(.createdAt) · \(.label // .filename) · \(.sizeBytes / 1024 / 1024 | round)MB · expire \(.expireAt)"' 2>/dev/null || echo "(jq 解析失败)"
    echo ""

    local total_mb
    total_mb="$(echo "$wecom_recent" | jq '[.[] | .sizeBytes] | add / 1024 / 1024 | round' 2>/dev/null || echo "?")"
    echo "**累计兜底字节**：约 ${total_mb} MB"
  fi
}

# ── 3. 失败痕迹（仅当 share-fallback 没新增条目时检查）──────────────────────
section_err_traces() {
  if [[ ! -f "$GATEWAY_ERR_LOG" ]]; then
    echo "**状态**：未找到 \`$GATEWAY_ERR_LOG\`"
    return
  fi
  local count
  count="$(safe_count 'share 兜底也失败' "$GATEWAY_ERR_LOG")"
  if [[ "$count" -eq 0 ]]; then
    echo "**状态**：err log 没有 \`share 兜底也失败\` 字样（说明没有 fallback 写盘失败的反例）"
    return
  fi
  echo "**状态**：err log 有 **$count** 次 \`share 兜底也失败\`"
  echo ""
  echo "**最近 5 条**："
  echo '```'
  grep 'share 兜底也失败' "$GATEWAY_ERR_LOG" | tail -5
  echo '```'
}

# ── 4. 写报告 ──────────────────────────────────────────────────────────────
write_kb() {
  cat > "$KB_FILE" <<EOF
---
date: $TODAY
tags: [openclaw-enhance, wecom, session-bridge, share-fallback, followup-audit]
status: auto-generated
related:
  - 2026-05-02-zhaobo-amnesia-session-bridge-and-wecom-share-fallback.md
versions_audited:
  - "@huo15/openclaw-enhance@5.7.26"
  - "@huo15/wecom@2.8.15"
---

# 5/2 失忆事故 + 大文件兜底 — 两周后审计

> 由 \`scripts/audit-session-bridge-and-share-fallback.sh\` 在 $TARGET_DATE 自动生成。
> 数据源：\`$GATEWAY_LOG\` / \`$GATEWAY_ERR_LOG\` / \`$SHARE_MANIFEST\`。
> 锚点时间：$ANCHOR_ISO（修复发布日；早于此的旧日志不计）。

## 1. session-bridge 触发情况（enhance v5.7.26）

$(section_session_bridge)

## 2. wecom share-fallback 落盘情况（wecom v2.8.15）

$(section_share_fallback)

## 3. 失败痕迹（err log）

$(section_err_traces)

## 4. 综合判断

> 这里需要人工判断（脚本只给数据，不下结论）。打开本文件后请补：

- [ ] session-bridge 触发频率是否符合预期？（1/天 ≈ 健康；0 = 阈值太严或没人重连；>10/天 = dedup 失效要查）
- [ ] share-fallback 是否真的兜了大文件？（看 §2 累计字节数和文件类型）
- [ ] 5/2 zhaobo 那次失忆复发了吗？（去 wecom 问下用户体感）
- [ ] 大文件失败的 UX 改善了吗？（用户是否还报告"文件发不出去"）

### 是否需要 v5.7.27 / v2.8.16

- [ ] enhance: 调 \`bridgeIdleMinutes\` / \`freshSessionMaxBytes\` 阈值？
- [ ] enhance: \`getLastActivityMs\` 改为 session 级 max（避免 agent-级 memory 写入压制 recap）？
- [ ] wecom: 把 \`agent-api/core.ts\` 的 \`uploadMedia\` 也接上 share-fallback（active push 路径）？
- [ ] wecom: \`BOT_BASE_URL\` 兜底是否需要从 enhance http-route-bridge 自动检测？

## 5. 自卸载提醒

如果 §4 判断不需要继续监控，跑这条命令卸掉 LaunchAgent：

\`\`\`bash
launchctl unload "\$HOME/Library/LaunchAgents/ai.huo15.openclaw.session-bridge-2week-followup.plist"
rm "\$HOME/Library/LaunchAgents/ai.huo15.openclaw.session-bridge-2week-followup.plist"
\`\`\`
EOF
  echo "[audit] 报告已写入：$KB_FILE" >&2
}

write_kb

# 5/16 跑完后留个面包屑给用户：
osascript -e 'display notification "session-bridge + share-fallback 审计完成，详见 ~/knowledge/huo15/" with title "huo15 自动审计"' 2>/dev/null || true

exit 0
