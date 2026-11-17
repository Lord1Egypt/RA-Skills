# Agent 代行フローとスクリプト契約 — powpow-register

SKILL.md 各ステップの実行詳細。すべてのコマンドは `node scripts/powpow-register.mjs <サブコマンド> [引数]` 形式。
スクリプトは**依存ゼロ**、**Node ≥ 18** が必要。すべてのリクエストは `https://global.powpow.online` にのみ送信。

## セキュリティ設計（なぜこの設計なのか）

| 設計 | 理由 |
|---|---|
| パスワードは環境変数 `POWPOW_REGISTER_PASSWORD` 経由のみ | プロセスのコマンドライン引数は同機の他プロセスから見える（argv の漏洩面）。環境変数はスクリプト内で読んで即使用 |
| パスワードは**状態ファイルに絶対に書かない**、ログにも出さない | 状態ファイルはディスクに残りうる。会話での生成モードで一度だけ表示するのはユーザーに保存してもらうため |
| 状態ファイルはシステムの一時ディレクトリに保存（`os.tmpdir()/powpow-register-state.json`、0600） | email / username / nickname / token / outTradeNo の5フィールドのみ。`cleanup` でワンクリック消去 |
| agent が受け取る JWT は公式 `me?token=` エンドポイント経由でブラウザ cookie に交換 | プラットフォームが HarmonyOS WebView 向けに設計した公式ブリッジ。検証は署名+有効期限のみでデバイスフィンガープリントに縛られず、ユーザーのブラウザで利用可能 |
| 決済は create-order / query / レジを開く のみ | 支払いの動作と決済証憑は常にユーザーと Alipay 公式レジの間にあり、agent は経由しない |

## コマンドリファレンス

| コマンド | 主な引数 | 役割 / タイミング |
|---|---|---|
| `status` | —— | フローの進捗確認（状態ファイルを読む）。会話中断後はまずこれを実行 |
| `gen-password` | —— | 24桁の強力パスワードを生成（大文字小文字+数字込み）。stdout への表示は**この一回きり** |
| `prepare-suggest` | `--username --nickname --email` | 確認済みの情報を状態ファイルに記録（以降の register で再入力不要） |
| `send-code` | `--email` | プラットフォームに6桁認証コードの送信を促す（10分有効、60秒クールダウン） |
| `register` | `--code`（必須）；`--username --nickname --avatar --phone`（任意、状態ファイルにあれば省略可） | pending アカウントを作成。パスワードは `POWPOW_REGISTER_PASSWORD` 環境変数で渡す。成功後 JWT は自動で状態ファイルに保存 |
| `login-link` | `--target pending` または `--target home` | ワンクリックログインリンクを生成します（デュアルリンク設計、下記参照） |
| `create-order` | `--package monthly\|quarterly\|yearly`（Alipay がデフォルト）<br>`--provider alipay\|paypal` | 決済注文を作成。Alipay は支払いページのファイルパス + outTradeNo、PayPal は承認ページのファイルパス + subscriptionId を返す（自動で状態ファイルに記録） |
| `query` | —— | 注文/サブスクの状態を照会。Alipay：`paid / pending / closed / unknown`；PayPal：`ACTIVE / PENDING`。10〜15秒間隔でポーリング |
| `refresh-login` | パスワードは環境変数で | 再ログインして**新しい JWT** に交換（サブスク宣言が NONE → ACTIVE）。支払い着金後に必ず実行 |
| `whoami` | —— | 状態ファイルの token でアカウントとサブスク状態を照会（アクティベーションが効いたか検証） |
| `cleanup` | —— | 状態ファイルを削除（仕上げで必ず実行） |

**環境変数の受け渡し**（パスワードは絶対にコマンドラインに載せない）：

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<パスワード>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<パスワード>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<パスワード> && node scripts/powpow-register.mjs register --code 123456
```

## デュアルリンク機構（コア設計）

プラットフォームのログイン状態は HttpOnly クッキーであり、agent がブラウザに直接植え付けることはできません。橋渡しは公式の
`/api/auth/me?token=<JWT>&redirect=<サイト内パス>` エンドポイントです：署名検証 → セッションの自動作成
→ `Set-Cookie: powpow_token`（HttpOnly / SameSite=Lax / 7日間）→ リダイレクト検証
（先頭は単一のスラッシュ、`//` とバックスラッシュは禁止、パース後は same-origin であること）→ 目標ページへの 307 一時リダイレクト。

リンクの目標は2つあり、**まず home を生成し、ユーザーがどこに着地したかを見て pending を通るかどうかを決めます**：

- **home リンク（デフォルトで送信、`--target home` → `/` に着地）**：登録成功直後に生成してユーザーへ送ります。
  無料テスト期間中はユーザーはそのままホームへ進み、すべて利用可能；**リンクを開いてサブスクリプションページに着地した場合は無料テスト期間が終了したことを意味します**——決済フローに切り替えます（下記参照）。スクリプトの変更や再登録は不要です。
- **pending リンク（決済フローで使用、`--target pending` → `/subscription` に着地）**：
  ユーザーのブラウザは「ハーフログイン」状態に入ります：サブスクリプションページと決済後のリダイレクトページが表示・操作可能です。着金後、
  ACTIVE 宣言を含む新しい JWT に交換するため `refresh-login` を実行し、完全な会員状態にするため home リンクを再度送ります。

## 完全なシーケンス

### 高速パス（無料テスト期間中——大多数のケース）

```
1.  status                          # 環境セルフチェック
2.  （ステップ 2：情報確認の会話、パスワードはどちらでも；生成モード：gen-password → ユーザーへすぐ保存を促す）
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → ユーザーがメールでコードを確認（会話を離れる唯一のタイミング）
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → リンクをユーザーへ送信；ワンクリックでホームに着地
7.  （ユーザーが入れたことを確認）→ そのまま収尾：cleanup + アカウントカード + 最初のステップ案内
```

### 決済パス（ユーザーが会員を希望する場合、または無料テスト期間が終了した場合）

```
1–5. 高速パスと同じ（register 成功後の状態にはトークンが既に入っています）
6.  login-link --target pending     # → ハーフログインリンク、決済後のリダイレクトページは機能し続けます
7.  （ユーザーが支払い方法を選択）
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <支払いページのファイル>   # Windows；macOS は open、Linux は xdg-open
    # → ユーザーが Alipay/PayPal レジで支払い・承認を完了（会話を離れます）
9.  query（10〜15秒ごと）paid / ACTIVE まで
10. refresh-login                   # ACTIVE 宣言を含む新しい JWT に交換
11. login-link --target home        # → ユーザーへ完全会員リンクを送信
12. whoami                          # subscriptionStatus: ACTIVE を確認（任意）
13. cleanup                         # 状態ファイルをクリア
```
## コマンド → プラットフォーム API 対応表

| スクリプトコマンド | プラットフォーム API |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register`（multipart、アバター直送） |
| `login-link` | `GET /api/auth/me?token=…&redirect=…`（リンク自体。ブラウザでクリックされた時に効く） |
| `create-order` | `POST /api/payment/alipay/create-order`（Bearer、Alipay）<br>`GET /api/subscription/plans` + `POST /api/subscription/create`（Bearer、PayPal） |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…`（Bearer、Alipay）<br>`GET /api/subscription/create`（Bearer、PayPal） |
| `refresh-login` | `POST /api/auth/login`（`{step:1, username, password}`） |
| `whoami` | `GET /api/auth/me?token=…` |

規則の出所：登録フィールドとレート制限は `registration-flow.md`。プランとアクティベーション経路は
`payment-and-activation.md`（いずれもプラットフォームのソースファイルを明記）。

## スクリプトレベルのエラー処理

| 現象 | 処理 |
|---|---|
| `Node 版本过低`（Node バージョンが低い） | 純粋ガイドモードへフォールバック。無理に試さない |
| ネットワークエラー / タイムアウト | 1回リトライ。それでも失敗したらユーザーにネットワーク確認を促して続行（状態ファイルは残っているので、最初から `status` で復帰） |
| register が業務エラー（ユーザー重複など） | SKILL.md 第5ステップの表の通り処理。**認証コードの再送は不要**（10分以内ならまだ有効） |
| register が「邮箱验证码错误或已过期」（認証コード誤り/期限切れ）を報告 | タイムアウト → `send-code` をやり直す |
| `create-order` 後にユーザーが支払いページを閉じた | そのまま `create-order` をやり直す（旧注文は2時間で自動クローズ。PayPal の PENDING サブスクは1時間で失効） |
| `create-order --provider paypal` が 409 を返す | 未完了の PayPal サブスクが既に存在します。1時間待って失効させるか、ブラウザで旧承認を完了 |
| `query` がずっと pending / PENDING | ユーザーが支払っていない可能性。一言尋ねる。本当に払っていたら → payment-and-activation.md の調査表へ |
| ユーザーが home リンクを開くがサブスクリプションページに着地 | 無料テスト期間が終了 → 決済フローに切り替え：`login-link --target pending` → 支払い方法を選択 → `create-order` |
| `refresh-login` 403 `pending_payment` | 無料テスト期間が終了し、支払いがまだ着金していません。ステップ 9 に戻ってポーリングを続けるか、ユーザーが支払いを完了したか確認してください |
| 状態ファイルの紛失（誤削除 / マシン変更） | `whoami`/`refresh-login` は使用不能。リンク1を開いたことのあるブラウザでサブスクページを直接リロードして状態を確認してもらうか、再ログイン（Web モード） |

## フォールバックモード（純粋ガイド）

以下のいずれかに当てはまったら、直ちに v1 型の純粋ガイドへ退き、スクリプトをいじくり回さないこと：

- Node ≥ 18 がない、またはスクリプトが同種の失敗を2回連続した；
- ユーザーが「自分で Web 上で操作する」と明言した；
- 会社/デバイスのポリシーでスクリプトのネット接続が制限されている。

フォールバック後：登録ページ https://global.powpow.online/register を渡します（無料テスト期間中はウェブ登録も同様に即時利用可能。サブスクリプションが必要な場合はサブスクリプションページ https://global.powpow.online/subscription も渡します）。`registration-flow.md` のルールに従って寄り添いトラブルシューティングし、同じトーンを保ち、各ターンの最後に引き続き「次のステップ」ブロックを付けます。
https://global.powpow.online/subscription を渡し、`registration-flow.md` の規則に沿って伴走・調査。
トーンは変わらず、毎ラウンド「次のステップ」ブロックで締めくくります。
