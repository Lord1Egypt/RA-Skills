---
name: github-monitor
description: Monitor one or more GitHub repositories and send low-noise alerts with configurable policy modes (major_only, balanced, verbose). Use when setting up recurring repo watch, release/security monitoring, PR merge tracking, and daily digest workflows via OpenClaw cron.
---

# GitHub Monitor

Build one-cron multi-repo monitoring with deduplication, severity routing, and low-noise notifications.

## Quick setup

Collect:

- `repos`: list of `owner/repo`
- `policy_mode`: `major_only` | `balanced` | `verbose`
- `check_interval`: recommended 2h
- `timezone`: e.g. `America/New_York`
- `daily_digest_time`: e.g. `21:00`
- `notify_target`: user/channel id
- `state_file`: e.g. `/root/.openclaw/workspace/memory/repo-watch/multi-repos.json`

Use one isolated cron job to monitor all repos.

## Data sources per repo

Check with GitHub public APIs each run:

1. Latest release
2. Recent commits (last 50, filtered by run window)
3. Recently merged PRs (filtered by run window)

## Policy modes

### 1) major_only

- Notify only P0 events
- Skip P1/P2 notifications

P0 signals:
- New release
- PR keyword hit: `breaking|migration|security|auth`

### 2) balanced (default)

- P0/P1 immediate notify
- P2 daily digest

P1 keyword examples:
- `gateway|config schema|tooling|memory|cron|session|channel|provider|search|index|install|auth flow`

### 3) verbose

- P0/P1 immediate
- P2 also immediate (or short-window batched)

## Severity scoring recommendations

Do not rely on title keyword only; combine signals:

- Title/body keyword hit
- Label hit
- Changed paths weighting:
  - higher weight: `core/`, `gateway/`, `agent/`, `runtime/`
  - lower weight: `docs/`, `tests/`, `examples/`

## Baseline + notification window (critical)

Track notification cursors in state to avoid backfilling old events:

- `installed_at`: skill first-run time
- `last_checked_at`: last successful scan time
- `last_notified_at`: last time user was notified

Rules:

1. On first install/run, initialize all three to `now` and **do not send historical events**.
2. Each run only evaluates events in `(last_checked_at, now]`.
3. Notify only for events newer than `last_notified_at`.
4. After sending any alert/digest, set `last_notified_at = now`.
5. After successful scan, set `last_checked_at = now`.

## Noise control

- Dedup fingerprint: `repo + event_type + event_id/hash`
- Silent when no new events
- Merge same-run alerts into one message grouped by repo
- Keep digest queue for P2 in state (`pending_daily`)

## Reliability

- Retry transient API failures with exponential backoff
- If repeated failures, send one degradation alert
- Send one recovery alert when healthy again
- Persist state at end of successful run

## Suggested OpenClaw cron behavior

- One job for all repos (easy scaling)
- Add/remove repos by editing list only
- Preserve one state file for dedup across restarts

## Output mode (default: brief impact summary)

Default output must be concise and decision-oriented, not event-by-event long list.

Use this fixed structure:

1. 本窗口结论（是否有关键变化）
2. 对用户可能影响（3-5 条，按优先级）
3. 建议动作（最多 3 条）
4. 详情入口：回复“看详情”再展开事件清单

Impact-first grouping (preferred):

- 配置/兼容性风险（breaking、config schema、auth、gateway）
- 通知/渠道行为变化（telegram/slack/feishu/discord/channel）
- 会话与路由变化（session/dispatch/provider/tools）
- 稳定性/性能修复（timeout、race、retry）
- 文档/测试类（低优先）

## Detailed mode (on-demand)

Only when the user explicitly asks “看详情/展开/给清单”, output event-level details with links.
