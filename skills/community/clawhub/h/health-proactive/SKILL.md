---
name: health-proactive
description: Proactive health alerts — detect missed meals, low hydration, and overdue tasks.
metadata:
  {
    "openclaw":
      {
        "emoji": "⚠️",
        "requires": { "scripts": ["scripts/health_proactive.js"] },
      },
  }
---

# health-proactive

健康関連のプロアクティブ通知。食事未記録・水分不足・タスク期限超過を検出。

## Script

```bash
node scripts/health_proactive.js check
```

## アラート種別

| アラート | 条件 | メッセージ例 |
|----------|------|-------------|
| missed_lunch | 14時以降で今日の食事記録0件 | 🍴 14時ですが、今日の食事記録がまだないよ！写真を送るだけでOK |
| missed_dinner | 20時以降で今日の食事記録2件未満 | 🍴 20時で食事記録1件。夕食を記録してね! |
| low_hydration | 18時以降で水分1500ml未満 | 💧 18時で水分500ml。目標1500ml以上！水を飲もう |
| overdue_tasks | 期限切れタスクあり（エージェントがタスクデータを提供） | ⚠️ 期限切れタスクが3件あります |

## 重複防止

各アラートは1日1回のみ発火。状態は `state/mention_image_analyzer_state.json` の `proactive` セクションで管理。

## 投稿先

アラートは `#pj_openclaw` (`C0AHBLQ0P32`) に投稿。

```
⚠️ *期限切れタスク（3件）*
• タスク名（期限: 2026-02-20）
• ...

🤖 OpenClaw プロアクティブ通知
```
