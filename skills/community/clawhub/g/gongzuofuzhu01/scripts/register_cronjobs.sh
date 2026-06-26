#!/bin/bash
# ============================================================================
# Personal Assistant — Cronjob Registration Script
# ============================================================================
# Registers 5 scheduled tasks for the Personal Assistant skill:
#   1. Morning reminder   (9:00, weekdays)
#   2. Afternoon reminder (14:00, weekdays)
#   3. Evening review     (20:00, daily)
#   4. Recurring sync     (1:00, daily)
#   5. OKR sync           (10:00, every Monday)
#
# Usage:
#   bash scripts/register_cronjobs.sh
#
# Prerequisites:
#   - hermes CLI must be installed and in PATH
#   - personal-assistant skill must be available
# ============================================================================

set -euo pipefail

echo "=== Personal Assistant Cronjob Registration ==="
echo ""

# ---------------------------------------------------------------------------
# 1. Morning Reminder — Weekdays 9:00 AM
# ---------------------------------------------------------------------------
echo "[1/5] Registering morning reminder (工作日 9:00)..."
hermes cron create \
  --name "pa-morning-reminder" \
  --schedule "0 9 * * 1-5" \
  --prompt "加载 personal-assistant 技能，执行以下步骤：
1. 运行 task list --status todo,in_progress --limit 30 获取所有待办
2. 从结果中筛选今天截止的任务，列出每一项的具体名称+优先级+分类
3. 筛选明天截止的任务作为预告
4. 格式：☀️ 今日待办 — 逐项列出 → 📅 明日预告 — 逐项列出
5. 禁止使用'共N项'替代具体清单，必须逐项写出任务名称" \
  --skills personal-assistant 2>/dev/null && echo "  ✅ OK" || echo "  ⚠️  Already exists or failed"

# ---------------------------------------------------------------------------
# 2. Afternoon Reminder — Weekdays 14:00
# ---------------------------------------------------------------------------
echo "[2/5] Registering afternoon reminder (工作日 14:00)..."
hermes cron create \
  --name "pa-afternoon-reminder" \
  --schedule "0 14 * * 1-5" \
  --prompt "加载 personal-assistant 技能，执行以下步骤：
1. 运行 task list --status todo,in_progress --limit 30 获取所有待办
2. 筛选今天截止但未完成的任务，逐项列出（标注⚠️)
3. 筛选明天截止的任务作为预告
4. 格式：⚠️ 今日剩余 — 逐项列出 → 📅 明日预告 — 逐项列出
5. 禁止使用'共N项'替代具体清单，必须逐项写出任务名称" \
  --skills personal-assistant 2>/dev/null && echo "  ✅ OK" || echo "  ⚠️  Already exists or failed"

# ---------------------------------------------------------------------------
# 3. Evening Review — Daily 20:00
# ---------------------------------------------------------------------------
echo "[3/5] Registering evening review (每天 20:00)..."
hermes cron create \
  --name "pa-evening-reminder" \
  --schedule "0 20 * * *" \
  --prompt "加载 personal-assistant 技能，执行以下步骤，逐项输出，禁止省略：

## 步骤1：查询今日完成
运行 task list --status done 获取已完成任务。从中筛选今天完成的项目，逐项列出名称。如果为空则写'无'。

## 步骤2：查询逾期未完成
运行 task list --status todo,in_progress --limit 30 获取待办。逐项列出 deadline 在今天或之前的任务（标注🔴逾期），写出每条的名称和原定截止日期。

## 步骤3：明日预告
从步骤2的待办中筛选明天截止的P1/P2任务，逐项列出。

## 步骤4：组装报告
格式：
🌙 晚间回顾 · 日期
━━━
✅ 今日完成
· (逐项列出，空则写'今日无完成记录')
━━━
🔴 逾期未完成
· (逐项列出任务名+原定截止日期，空则写'无逾期')
━━━
📅 明日预告
· (逐项列出，空则写'明日无截止任务')

## 强制规则
- 禁止使用'共N项'概括，必须逐项写出每条任务的具体名称
- 禁止推测任务状态，必须以 task list CLI 的实际输出为准
- 发送前自检：每条任务名称是否都写出来了？" \
  --skills personal-assistant 2>/dev/null && echo "  ✅ OK" || echo "  ⚠️  Already exists or failed"

# ---------------------------------------------------------------------------
# 4. Recurring Task Sync — Daily 1:00 AM
# ---------------------------------------------------------------------------
echo "[4/5] Registering recurring task sync (每天 1:00)..."
hermes cron create \
  --name "pa-recurring-sync" \
  --schedule "0 1 * * *" \
  --prompt "加载 personal-assistant 技能，执行周期任务同步：检查所有 cycle 任务，生成到期实例。" \
  --skills personal-assistant 2>/dev/null && echo "  ✅ OK" || echo "  ⚠️  Already exists or failed"

# ---------------------------------------------------------------------------
# 5. OKR Sync — Every Monday 10:00 AM
# ---------------------------------------------------------------------------
echo "[5/5] Registering OKR sync (每周一 10:00)..."
hermes cron create \
  --name "pa-okr-sync" \
  --schedule "0 10 * * 1" \
  --prompt "加载 personal-assistant 技能，执行 OKR 同步：从飞书文档读取最新 OKR 并更新本地缓存。" \
  --skills personal-assistant 2>/dev/null && echo "  ✅ OK" || echo "  ⚠️  Already exists or failed"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "=== Registration complete ==="
echo ""
echo "Registered cronjobs:"
echo "  1. pa-morning-reminder   — 工作日 9:00"
echo "  2. pa-afternoon-reminder — 工作日 14:00"
echo "  3. pa-evening-reminder   — 每天 20:00"
echo "  4. pa-recurring-sync     — 每天 1:00"
echo "  5. pa-okr-sync           — 每周一 10:00"
echo ""
echo "Run 'hermes cron list' to verify."
