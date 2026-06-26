---
name: notes-reminders
description: Manage quick notes and time-based reminders.
metadata:
  {
    "openclaw":
      {
        "emoji": "📌",
        "requires": { "scripts": ["scripts/notes.js", "scripts/reminders.js"] },
      },
  }
---

# notes-reminders

メモとリマインダーの管理。

## メモ

```bash
# メモ追加
node scripts/notes.js add --title="アイデア" --content="新機能のアイデア..."

# メモ検索
node scripts/notes.js search --query="アイデア" --limit=10
```

## リマインダー

```bash
# リマインダー追加
node scripts/reminders.js add \
  --message="ミーティング準備" \
  --remind_at="2026-02-25T10:00:00+09:00" \
  --channel=C0AHBLQ0P32

# 未発火リマインダー一覧
node scripts/reminders.js list

# 発火チェック（期限到来のリマインダーを取得）
node scripts/reminders.js check-and-fire
```

## リマインダー発火ワークフロー

`check-and-fire` の結果に fired リマインダーがあれば、該当チャネルにメッセージを送信:
`リマインダー: {message}`

## 時刻の扱い

ユーザーが「明日10時にリマインドして」等と言った場合:
- Asia/Tokyo タイムゾーンで解釈
- ISO 8601 形式に変換して --remind_at に渡す
