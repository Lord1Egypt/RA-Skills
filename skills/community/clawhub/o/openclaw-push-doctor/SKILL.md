---
name: openclaw-push-doctor
description: |
  openclaw-healthcheck is a self-diagnostic skill that checks and repairs openclaw's communication channels and scheduled tasks. It diagnoses Feishu/lark-cli auth expiry, Telegram bot silence, WeChat bridge disconnects, and cron job failures — then guides the agent through targeted repairs without rebuilding everything from scratch.

  Trigger words: 飞书断了, 飞书没反应, telegram没反应, 微信断了, 定时任务没推送, cron没跑, 推送失败, 自检一下, 通讯检查, healthcheck, 检查通讯, 定时任务检查, 推送自检, 重连飞书, 重连telegram, 验证码失效, 配对码过期

keywords: openclaw healthcheck, 飞书自检, telegram修复, 定时任务检查, cron检查, 通讯自检, 推送失败修复, lark-cli auth, bot status, 连接诊断, 断联修复, 自定时任务, 推送验证, 配对码

requirements:
  node: ">=18"
  binaries:
    - name: curl
      required: true
      description: "Used for Telegram bot API health checks (getMe, getUpdates, sendMessage)."
    - name: python3
      required: true
      description: "Used to parse JSON responses from Telegram API and update config files."
    - name: pgrep
      required: true
      description: "Used to check if WeChat bridge process and openclaw daemon are running."
    - name: lark-cli
      required: false
      description: "Feishu/Lark CLI — required if using Feishu channel."
    - name: crontab
      required: false
      description: "Used to read, deduplicate, and repair system cron entries."
  env:
    - name: TELEGRAM_BOT_TOKEN
      required: false
      description: "Telegram bot token — required for Telegram channel checks and test sends."
    - name: TELEGRAM_CHAT_ID
      required: false
      description: "Telegram chat/group ID — used to send test push messages to verify delivery."
    - name: OPENCLAW_CONFIG_DIR
      required: false
      description: "Override path to openclaw config directory. Defaults to ~/.openclaw."
    - name: FEISHU_APP_ID
      required: false
      description: "Feishu App ID — used to verify config matches auth state."

metadata:
  openclaw:
    always: false
    disable-model-invocation: true
---

# openclaw-healthcheck — 通讯自检与修复工具

> 一键诊断飞书断联、Telegram 无响应、定时任务失效 — 精准修复，不用从头重配

---

## 何时使用

- 飞书消息推不进来，或 lark-cli 命令报 401/token expired
- Telegram bot 长时间无响应，或需要重新验证配对码
- 微信 bridge 断线
- 定时任务（cron/push）静默失败，或同一任务重复触发
- 例行自检 — 每天/每周确认所有通道都活着

---

## Scripts

| Script | 用途 |
|--------|------|
| `check-all.js` | 全量诊断：所有通道 + 所有 cron 任务，输出健康报告 |
| `check-feishu.js` | 飞书 lark-cli auth 状态、token 有效期、测试推送 |
| `check-telegram.js` | Telegram bot API 连通性、webhook 状态、测试推送 |
| `check-wechat.js` | 微信 bridge 进程状态、连接测试 |
| `check-crons.js` | 列出所有定时任务、检测失败/重复/超时未跑 |
| `fix-feishu.js` | 引导飞书 token 刷新或重新 OAuth 登录 |
| `fix-crons.js` | 去重、修复、重启失效的定时任务 |

---

## 快速用法

```bash
# 全量自检（推荐先跑这个）
node scripts/check-all.js

# 只查飞书
node scripts/check-feishu.js

# 只查 Telegram
node scripts/check-telegram.js

# 只查定时任务
node scripts/check-crons.js

# 修复飞书 auth
node scripts/fix-feishu.js

# 修复 cron 重复任务
node scripts/fix-crons.js --dedup
```

---

## 输出格式

每个 check 脚本输出一份健康报告写入 `data/health-report.json`：

```json
{
  "checkedAt": "<ISO 时间戳>",
  "channels": {
    "feishu":   { "status": "OK | EXPIRED | DISCONNECTED | NOT_CONFIGURED", "detail": "..." },
    "telegram": { "status": "OK | SILENT | TOKEN_INVALID | NOT_CONFIGURED", "detail": "..." },
    "wechat":   { "status": "OK | BRIDGE_DOWN | NOT_CONFIGURED", "detail": "..." }
  },
  "crons": [
    {
      "id": "morning-push",
      "schedule": "0 8 * * *",
      "lastRun": "<ISO>",
      "status": "OK | MISSED | DUPLICATE | FAILED",
      "duplicateCount": 0
    }
  ],
  "overallStatus": "HEALTHY | DEGRADED | CRITICAL",
  "actionsNeeded": ["fix-feishu", "dedup-crons"]
}
```

---

## 常见问题速查

| 症状 | 根因 | 修复命令 |
|------|------|---------|
| 飞书收不到推送 | lark-cli token 过期 | `node scripts/fix-feishu.js` |
| Telegram bot 无响应 | webhook 断开 / token 失效 | `node scripts/check-telegram.js` → 按提示操作 |
| 定时任务重复触发 | cron 条目重复注册 | `node scripts/fix-crons.js --dedup` |
| 定时任务静默不跑 | cron 进程崩溃 / 配置丢失 | `node scripts/check-crons.js` → 查看 MISSED 条目 |
| 配对码过期 | Telegram device code 超时 | `node scripts/check-telegram.js --reauth` |

---

*openclaw-healthcheck v1.0.0 — 用 Automatic Skill 流水线生成*
