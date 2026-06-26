#!/usr/bin/env node
/**
 * openclaw-healthcheck — fix-crons.js
 * PROMPT GENERATOR ONLY — no outbound network requests.
 * Guides agent through diagnosing and repairing openclaw cron tasks:
 * deduplication, restart failed tasks, verify push delivery.
 *
 * Usage:
 *   node scripts/fix-crons.js
 *   node scripts/fix-crons.js --lang en
 *   node scripts/fix-crons.js --dedup      # remove duplicate cron entries
 *   node scripts/fix-crons.js --restart    # restart all openclaw cron jobs
 *   node scripts/fix-crons.js --verify     # send test push for each active job
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';
const dedup = args.includes('--dedup');
const restart = args.includes('--restart');
const verify = args.includes('--verify');
const mode = dedup ? 'dedup' : restart ? 'restart' : verify ? 'verify' : 'full';

if (lang === 'en') {
  console.log(`=== openclaw-healthcheck — Fix Cron Tasks ===
Mode: ${mode === 'full' ? 'Full repair (list → dedup → restart → verify)' :
       mode === 'dedup' ? 'Deduplicate only' :
       mode === 'restart' ? 'Restart jobs only' : 'Verify push delivery only'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1 — List all openclaw cron tasks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # Try openclaw native cron manager first
  openclaw cron list 2>/dev/null

  # Fallback: read system crontab filtered to openclaw
  crontab -l 2>/dev/null | grep -i "openclaw\\|morning-push\\|daily-push\\|skill" | cat

  # Also check openclaw-specific cron config files
  ls ~/.openclaw/cron/ 2>/dev/null
  cat ~/.openclaw/cron/*.json 2>/dev/null | python3 -m json.tool 2>/dev/null

  For each task found, record:
    - Task ID / name
    - Schedule (cron expression)
    - Target channel (feishu / telegram / wechat)
    - Script or command being run
    - Last run timestamp (from logs if available)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${dedup || mode === 'full' ? `STEP 2 — Detect and remove duplicate entries
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A duplicate means: identical schedule + identical command appears 2+ times in crontab.
This causes the same message to be pushed multiple times.

  # Find exact duplicates in system crontab
  crontab -l 2>/dev/null | sort | uniq -d

  # Find near-duplicates (same script, different schedule spacing by <5 min)
  crontab -l 2>/dev/null | grep -i "openclaw\\|morning-push" | sort

If duplicates found:
  1. Show user the duplicate lines
  2. Confirm which to keep (usually the first one, or the one with the correct schedule)
  3. Remove duplicates:
     # Export, edit, reimport
     crontab -l > /tmp/crontab_backup.txt
     # Edit /tmp/crontab_backup.txt to remove duplicate lines
     # Review the diff:
     diff /tmp/crontab_backup.txt <(sort -u /tmp/crontab_backup.txt)

     ⚠️  PAUSE: Show the diff output to the user and ask:
       "I'm about to replace your crontab with the deduplicated version above.
        The following lines will be removed: [list duplicate lines].
        Do you confirm? (yes/no)"
     Only proceed after the user explicitly confirms.

     # Apply ONLY after explicit user confirmation:
     crontab /tmp/crontab_backup.txt
     # Verify:
     crontab -l | grep openclaw

  For openclaw native cron:
     openclaw cron remove <duplicate-task-id>

` : ''}${restart || mode === 'full' ? `STEP ${dedup || mode === 'full' ? '3' : '2'} — Restart failed or stalled jobs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # Check if openclaw daemon/cron is running
  pgrep -f "openclaw" | head -5
  openclaw status 2>/dev/null || echo "openclaw status not available"

  # Check cron daemon
  pgrep -x cron || pgrep -x crond || echo "CRON_DAEMON_NOT_RUNNING"

  If cron daemon is not running:
    # macOS:
    launchctl start com.vix.cron 2>/dev/null || sudo launchctl start com.vix.cron

  If openclaw push daemon is not running:
    openclaw push-on 2>/dev/null || openclaw cron restart 2>/dev/null
    # Verify restart:
    openclaw status

` : ''}${verify || mode === 'full' ? `STEP ${mode === 'full' ? '4' : dedup ? '2' : restart ? '2' : '2'} — Verify push delivery with test messages
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For each active push task, send a test message to its target channel:

  Feishu test:
    lark-cli im +messages-send --chat-id oc_xxx \\
      --text "🔧 openclaw cron health check — $(date)" --dry-run
    # Remove --dry-run when ready to send for real

  Telegram test:
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \\
      -d "chat_id=$TELEGRAM_CHAT_ID&text=🔧 openclaw cron health check — $(date)"

  → 200 OK + message_id returned = delivery confirmed
  → Error = channel still broken, re-run channel-specific fix script

` : ''}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT — Update data/health-report.json crons array
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For each task, update its entry:
  { "id": "<name>", "schedule": "<expr>", "status": "OK",
    "duplicateCount": 0, "lastFixed": "<ISO timestamp>" }

Summary line:
  "Cron repair complete. <N> duplicates removed. <M> jobs restarted. All delivery tests passed."
`);
} else {
  console.log(`=== openclaw-healthcheck — 修复定时任务 ===
模式：${mode === 'full' ? '完整修复（列出 → 去重 → 重启 → 验证）' :
       mode === 'dedup' ? '仅去重' :
       mode === 'restart' ? '仅重启任务' : '仅验证推送'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第 1 步 — 列出所有 openclaw 定时任务
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # 先尝试 openclaw 原生定时任务管理器
  openclaw cron list 2>/dev/null

  # 回退：读取系统 crontab 中的 openclaw 相关条目
  crontab -l 2>/dev/null | grep -i "openclaw\\|morning-push\\|daily-push\\|skill" | cat

  # 检查 openclaw 专属 cron 配置文件
  ls ~/.openclaw/cron/ 2>/dev/null
  cat ~/.openclaw/cron/*.json 2>/dev/null | python3 -m json.tool 2>/dev/null

  对每个发现的任务，记录：
    - 任务 ID / 名称
    - 调度表达式（cron expression）
    - 目标通道（飞书 / Telegram / 微信）
    - 执行的脚本或命令
    - 上次运行时间戳（从日志获取）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${dedup || mode === 'full' ? `第 2 步 — 检测并删除重复条目
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

重复定义：相同调度 + 相同命令在 crontab 中出现 2 次以上。
这会导致同一条消息被多次推送。

  # 在系统 crontab 中查找完全重复的行
  crontab -l 2>/dev/null | sort | uniq -d

  # 查找近似重复（相同脚本，调度时间差 <5 分钟）
  crontab -l 2>/dev/null | grep -i "openclaw\\|morning-push" | sort

如发现重复：
  1. 向用户展示重复的行
  2. 确认保留哪条（通常保留第一条，或有正确调度的那条）
  3. 删除重复条目：
     # 导出、编辑、重新导入
     crontab -l > /tmp/crontab_backup.txt
     # 编辑 /tmp/crontab_backup.txt，删除重复行
     # 查看差异：
     diff /tmp/crontab_backup.txt <(sort -u /tmp/crontab_backup.txt)

     ⚠️  暂停：将 diff 结果展示给用户，并询问：
       "我将用以上去重版本替换您的 crontab。
        以下行将被删除：[列出重复行]。
        您确认吗？（是/否）"
     仅在用户明确确认后才执行。

     # 仅在用户明确确认后应用：
     crontab /tmp/crontab_backup.txt
     # 验证：
     crontab -l | grep openclaw

  使用 openclaw 原生 cron：
     openclaw cron remove <重复的任务 ID>

` : ''}${restart || mode === 'full' ? `第 ${dedup || mode === 'full' ? '3' : '2'} 步 — 重启失败或卡住的任务
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # 检查 openclaw 守护进程是否在运行
  pgrep -f "openclaw" | head -5
  openclaw status 2>/dev/null || echo "openclaw status 命令不可用"

  # 检查系统 cron 守护进程
  pgrep -x cron || pgrep -x crond || echo "CRON_DAEMON_NOT_RUNNING"

  如果 cron 守护进程未运行：
    # macOS：
    launchctl start com.vix.cron 2>/dev/null || sudo launchctl start com.vix.cron

  如果 openclaw 推送守护进程未运行：
    openclaw push-on 2>/dev/null || openclaw cron restart 2>/dev/null
    # 验证重启：
    openclaw status

` : ''}${verify || mode === 'full' ? `第 ${mode === 'full' ? '4' : '2'} 步 — 发送测试消息验证推送
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

对每个活跃的推送任务，向目标通道发送测试消息：

  飞书测试：
    lark-cli im +messages-send --chat-id oc_xxx \\
      --text "🔧 openclaw cron 健康检查 — $(date)" --dry-run
    # 确认无误后去掉 --dry-run 发送真实消息

  Telegram 测试：
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \\
      -d "chat_id=$TELEGRAM_CHAT_ID&text=🔧 openclaw cron 健康检查 — $(date)"

  → 返回 200 OK + message_id = 投递确认
  → 报错 = 通道仍有问题，重新运行对应的通道修复脚本

` : ''}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
输出 — 更新 data/health-report.json crons 数组
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

对每个任务更新其条目：
  { "id": "<名称>", "schedule": "<表达式>", "status": "OK",
    "duplicateCount": 0, "lastFixed": "<ISO 时间戳>" }

总结：
  "定时任务修复完成。删除重复条目 <N> 个，重启任务 <M> 个，所有推送测试通过。"
`);
}
