#!/usr/bin/env node
/**
 * openclaw-healthcheck — check-crons.js
 * PROMPT GENERATOR ONLY — no outbound network requests.
 *
 * Usage:
 *   node scripts/check-crons.js
 *   node scripts/check-crons.js --lang en
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';

if (lang === 'en') {
  console.log(`=== openclaw-healthcheck — Cron Task Check ===

Run the following checks:

  # List openclaw cron tasks
  openclaw cron list 2>/dev/null || \\
    crontab -l 2>/dev/null | grep -i "openclaw\\|morning-push\\|daily-push" | cat || \\
    echo "NO_CRON_FOUND"

  # Check for duplicates
  crontab -l 2>/dev/null | sort | uniq -d

  # Check recent logs
  tail -30 ~/.openclaw/logs/cron.log 2>/dev/null || echo "NO_CRON_LOG"

For each task found, assess:
  → Duplicate lines (same schedule + command)  → DUPLICATE → run fix-crons.js --dedup
  → Last run timestamp overdue by >1 interval  → MISSED    → run fix-crons.js --restart
  → Non-zero exit code in logs                 → FAILED    → check the failing script
  → Everything looks normal                    → OK

Output each task as:
  { "id": "<name>", "schedule": "<cron>", "lastRun": "<ISO>",
    "status": "OK | MISSED | DUPLICATE | FAILED", "duplicateCount": 0 }
`);
} else {
  console.log(`=== openclaw-healthcheck — 定时任务检查 ===

运行以下检查：

  # 列出 openclaw 定时任务
  openclaw cron list 2>/dev/null || \\
    crontab -l 2>/dev/null | grep -i "openclaw\\|morning-push\\|daily-push" | cat || \\
    echo "NO_CRON_FOUND"

  # 检查重复条目
  crontab -l 2>/dev/null | sort | uniq -d

  # 检查最近日志
  tail -30 ~/.openclaw/logs/cron.log 2>/dev/null || echo "NO_CRON_LOG"

对每个发现的任务：
  → 重复行（相同调度 + 命令）    → DUPLICATE → 运行 fix-crons.js --dedup
  → 上次运行已超过一个完整周期   → MISSED    → 运行 fix-crons.js --restart
  → 日志中退出码非零             → FAILED    → 检查失败的脚本
  → 一切正常                     → OK

输出每个任务：
  { "id": "<名称>", "schedule": "<cron>", "lastRun": "<ISO>",
    "status": "OK | MISSED | DUPLICATE | FAILED", "duplicateCount": 0 }
`);
}
