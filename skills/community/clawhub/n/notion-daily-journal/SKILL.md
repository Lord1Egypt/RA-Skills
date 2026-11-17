# notion-daily-journal

1日の終わりに「今日やったこと」を Notion ページに記録するスキル。

## 発動条件

- 毎日 22:00 JST の定期実行
- オーナーから「日報書いて」「今日のまとめ Notion に書いて」「Notion に記録して」等の依頼

## 手順

### 1. 今日の活動を収集

以下のソースから今日（JST 当日）の活動を集める:

**Linear** (環境変数 `LINEAR_API_KEY`):
- 今日ステータスが変わったチケット
- 今日コメントが追加されたチケット
- 今日完了（Done/Canceled）になったチケット

**Slack** (`slack_search_public_and_private`):
- 今日自分が送ったメッセージ・参加したスレッド（`from:me after:today`）
- 今日決まったこと・アクションアイテム

**DM チャット** (`aachat_read_messages`):
- `dm:phase1demo.p-take55` の今日のやりとり（朝のブリーフィング内容・追加の依頼・完了報告）

### 2. 今日の Notion ページを特定または作成

環境変数 `NOTION_DAILY_JOURNAL_PAGE_ID` が設定されていればその親ページ（またはデータベース）を使う。未設定なら `notion-search` で "日報" や "Daily Log" を検索して特定する。

その日の日報ページが既にあれば `notion-update-page` で追記、なければ `notion-create-pages` で新規作成:
- タイトル: `{YYYY-MM-DD} 日報`
- 親: 上で特定したページまたはデータベース

### 3. Notion ページに書き込む

以下のフォーマットで記録する:

```
## 今日やったこと

- {完了したタスク・貢献・対応した問い合わせ}

## 決めたこと・重要な判断

- {意思決定・方針確定・承認したもの}

## 明日に持ち越し

- {未完了・次のアクション・フォローアップ必要なもの}

## メモ

{気になったこと・参考情報・雑多なメモ}
```

活動が少ない日も「動きなし」とは書かず、朝のブリーフィングで取り上げた情報や調査したことを記録する。

### 4. DM に完了を通知

`aachat_send_message` で `dm:phase1demo.p-take55` に投稿:

```
Notion 日報を更新しました: {YYYY-MM-DD}
{Notion ページ URL}
```

## 注意事項

- Notion の読み書きには `claude_ai_Notion` MCP ツールを使う
- 日報の親ページ ID は環境変数 `NOTION_DAILY_JOURNAL_PAGE_ID` で管理する（未設定なら `notion-search` で探す）
- Slack・DM のプライベートな内容も個人ノート扱いで Notion に書いてよい
- 要約は箇条書き・簡潔に。長文は避ける
