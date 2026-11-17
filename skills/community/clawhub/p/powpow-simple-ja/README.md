# PowPow Simple JA — 投稿とデジタルヒューマンを公開マップに発信

PowPowアシスタント日本語版（OpenClaw）: あなたの写真や素材を旅行記にまとめて
PowPowに公開する、あるいは人物・キャラクターをチャットできるデジタルヒューマンに
して、公開マップにピン留めする。

これは [powpow-simple](https://clawhub.ai/durenzidu/skills/powpow-simple) の日本語版です
（v5.7.3 と機能同等。スクリプトはバイト単位で同一）。

## インストール

```
openclaw skills install @durenzidu/powpow-simple-ja
```

## 動作環境

- Node.js 18+（スクリプトはグローバル `fetch` を使用。サードパーティ依存なし）
- PowPowアカウント: https://global.powpow.online/register

## ステートディレクトリ

スキルパッケージ本体は読み取り専用のまま運用します。ログイントークンとユーザー設定は
ステートディレクトリに保存されます:

- デフォルト: `~/.powpow/`
- 環境変数 `POWPOW_STATE_DIR` で上書き可能

プラットフォームのアドレスや Unsplash キーを変えたい場合は、`config.json` を
ステートディレクトリに置くだけで同梱のデフォルト値を上書きできます。

## 使用例

```
cd <スキルディレクトリ>
node scripts/doctor.js                                   # セルフチェック + セッション探活
node scripts/login.js <username>                         # ログイン（パスワードは stdin、保存されない）
node scripts/geocode.js "地坛公园" --limit 5              # 地名 → 座標
node scripts/match-digital-human.js "读书 作家" --limit 3  # デジタルヒューマンをマッチング
node scripts/compose.js --text-file post.txt --loc "地坛公园" --lng 116.408195 --lat 39.952372 --image @/abs/path/cover.jpg --out post-draft.html
node scripts/publish.js post-draft.html                  # 公開
node scripts/verify.js <post-id>                         # 公開後の検証
node scripts/delete-post.js <post-id>                    # 削除（テスト後片付け）
```

`--image` のローカルパスは**必ず絶対パス**で指定してください。

補足: プラットフォームの場所検索とデジタルヒューマンライブラリは現在中国語のデータが
最も充実しています。中国語圏以外のユーザーは、地名やテーマを現地語のまま入力して構いません。

## セキュリティ

- パッケージ内にプラットフォームの機密情報は一切含まれません。すべての操作は
  プラットフォームの公開 API + ユーザー自身の JWT で行われます。
- パスワードはログイン時に一度使うだけで、ディスクに保存されません。トークンの
  有効期限は約7日です。
- 詳細は `references/security.md` を参照。

## レビュアー向け注意事項 (SkillSpector / manual review)

- これは**命令型スキル**です: SKILL.md がマルチスクリプトのパイプラインを指揮します。
  `scripts/` 配下の各スクリプトは、公開ワークフロー（ログイン → セルフチェック →
  ジオコーディング → マッチング → 組み立て → 公開 → 検証）のドキュメント化された
  1ステップであり、独立した隠しツールではありません。
- `delete-post.js` はログインユーザー自身の投稿のみを削除します
  （`DELETE /api/posts/{id}`。JWTでスコープされ、サーバー側で強制されます）。
  テスト後片付けのために SKILL.md ステップ8でドキュメント化されています。
  この能力はスキルの description でも宣言されています。
- 機密情報は同梱されていません。`config.json` にはデフォルト値のみが含まれます。
  セッションJWTはユーザーのステートディレクトリ（`POWPOW_STATE_DIR`、デフォルト
  `~/.powpow/session.json`）に書かれ、スキルパッケージ内には決して入りません。
  パスワードは永続化されません。
- 使用する環境変数（`POWPOW_STATE_DIR`、`POWPOW_PASSWORD`、`UNSPLASH_ACCESS_KEY`）
  はすべて省略可能で、SKILL.md フロントマター（`metadata.openclaw.envVars`）で
  宣言されています。
- 本パッケージは `powpow-simple` の日本語版です。スクリプトは同パッケージ v5.7.3 と
  バイト単位で同一です（翻訳されているのはドキュメントとメタデータのみ）。

## ライセンス

MIT-0（ClawHub 全プラットフォーム共通ライセンス）。

## リンク

- 公式サイト: https://global.powpow.online
- 地図: https://global.powpow.online/map
- 中国語版: https://clawhub.ai/durenzidu/skills/powpow-simple
- 英語版: https://clawhub.ai/durenzidu/skills/powpow-simple-en
- ドイツ語版: https://clawhub.ai/durenzidu/skills/powpow-simple-de
