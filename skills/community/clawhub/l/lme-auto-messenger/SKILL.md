---
name: lme-auto-messenger
description: LME顧客にカテゴリー状況に基づいたパーソナライズメッセージを自動送信。スプレッドシート読み込み→カテゴリー分析→LME送信を完全自動化。
homepage: https://clawhub.com/skill/lme-auto-messenger
metadata:
  openclaw:
    emoji: 📨
    requires:
      bins: [gws]
      tools: [browser-relay]
---

# LME Auto Messenger

LME（LINE公式アカウント管理ツール）の顧客に、カテゴリー状況に基づいたパーソナライズメッセージを自動送信するスキル。

## 機能

- **スプレッドシート読み込み**: 顧客データとカテゴリー状況を取得
- **カテゴリー分析**: 各顧客の興味・状況を分析（カテゴリーは自由に設定可能）
- **パーソナライズメッセージ生成**: カテゴリー状況に基づいた最適なメッセージを生成
- **LME自動送信**: Browser Relay経由でLMEを操作し、メッセージを送信

## 前提条件

1. **gws（Google Workspace CLI）** が認証済みであること
2. **Browser Relay** が有効であること
3. **LME** にログイン済みであること
4. **スプレッドシート** に顧客データとカテゴリー状況が入力されていること

## スプレッドシート形式

| 列 | 内容 | 例 |
|----|------|-----|
| A | 追加日時 | 2025-10-19 |
| B | 最新メッセージ | 2025-11-06 |
| C | LINE登録名 | 顧客名 |
| D | システム表示名 | 表示名 |
| E | メールアドレス | example@email.com |
| F | ステップ配信状況 | 停止中 |
| G以降 | カテゴリー列 | 自由に設定 |

### カテゴリー記号

- `○` = 可能/興味あり（緑色）
- `×` = 不可/興味なし（赤色）
- `△` = まだやっていない（黄色）
- 空 = 未確認

## 使用方法

### 1. スプレッドシートIDを確認

```
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
```

### 2. 顧客データを取得

```bash
gws sheets spreadsheets values get \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"シート1!A:K"}' \
  --format json > customers.json
```

### 3. メッセージ生成と送信

Browser RelayでLMEを開き、各顧客にメッセージを送信。

## メッセージテンプレート例

### パターン1: カテゴリーA興味あり

```
○○様

カテゴリーAについてご興味ありがとうございます！
詳しくご説明します。

ご都合の良い日はありますか？
```

### パターン2: 複数興味あり

```
○○様

複数のカテゴリーにご興味ありますね！
まずはどちらから始めたいか教えていただけますか？

あなたに合った提案をさせていただきます。
```

## 自動化フロー

```
スプレッドシート
    ↓
gwsでデータ取得
    ↓
カテゴリー分析
    ↓
メッセージ生成
    ↓
Browser RelayでLME操作
    ↓
1:1チャット送信
```

## 注意事項

- **個人情報の取り扱い**: 顧客データは厳重に管理すること
- **送信頻度**: 短時間に大量送信するとスパム判定される可能性がある
- **メッセージ内容**: 丁寧で価値のある内容を心がけること
- **同意確認**: 事前に顧客の同意を得ていることを確認すること

## トラブルシューティング

### Browser Relayが繋がらない

1. ChromeでLMEにログイン済みか確認
2. `openclaw browser status --browser-profile chrome-relay` で状態確認

### gws認証エラー

1. `gws auth status` で認証状態確認
2. 必要に応じて `gws auth login` で再認証

### スプレッドシート読み込みエラー

1. スプレッドシートIDが正しいか確認
2. スプレッドシートの共有設定を確認
3. 範囲指定が正しいか確認

## 関連スキル

- `gog` - Google Workspace操作
- `notebooklm-content` - NotebookLM自動化

---

*Created: 2026-03-18*
