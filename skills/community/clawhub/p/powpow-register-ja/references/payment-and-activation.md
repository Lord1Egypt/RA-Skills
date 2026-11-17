# サブスクリプションのアクティベーションと決済 — powpow-register

## 結論（先に答え）
> **無料テスト期間（2026-10-18 開始；プラットフォームの実際の動作を優先）**：この期間中は登録済みアカウントがすべての機能を直接利用でき、**サブスクリプションは要件ではなく任意のアップグレード**です——ユーザーが自主的に会員を望む場合にのみ、このファイルのフローに従ってください。テスト期間が終了すると、未購読のアカウントがコンテンツページを訪れるとサブスクリプションページへリダイレクトされます。このファイルに従ってサブスクリプションを完了すれば問題ありません。


**Alipay と PayPal のサブスクはどちらも、agent が発注と着金トラッキングを代行できます。**
Alipay は一括買い切りで自動更新なし。中国国内 / Alipay を持っているユーザー向け。PayPal は月次の自動更新でいつでも解約可能、
海外 / Alipay を持たないユーザー向けです。WeChat スキャン（手動確認）と華為 IAP も残っていますが、skill は代行しません。

決済における責任の境界：agent ができるのは**注文の作成、レジを開くこと、着金の確認**まで。**絶対に**ユーザーの Alipay / PayPal
アカウント/決済証憑には触れず、「代行支払い」も約束しません。支払いの動作は常にユーザー本人が公式レジで行います。

## Alipay チャネル（vibepay、主力）

一括買い切り制：1回の支払いで対応する期間が開通し、**自動更新なし**。プランは
`src/lib/alipay-vibepay.ts`（`ALIPAY_PACKAGES`）に固定で書かれています：

| key | planId | 名称 | 価格 | 期間 |
|---|---|---|---|---|
| `monthly` | alipay-monthly | 月間会員 | ¥6.99 | 30日 |
| `quarterly` | alipay-quarterly | 四半期会員 | ¥19.99 | 90日 |
| `yearly` | alipay-yearly | 年間会員 | ¥69.99 | 365日 |

### インターフェース契約（skill スクリプトが既にラップ済み。agent が直接リクエストを組み立てることはない）

| API | メソッド | 説明 |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | `Authorization: Bearer <JWT>` が必要（pending ユーザーで可）。body `{package}` → `{paymentHtml, outTradeNo, amount, planName}` を返す。`paymentHtml` は Alipay ゲートウェイへ自動送信されるフォームページ |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | 同じく Bearer 認証。`paid` / `pending` / `closed` / `unknown` を返す |
| `/api/payment/alipay/notify` | POST（Alipay サーバーのコールバック） | 5要素の署名検証（署名、app_id、金額一致、TRADE_SUCCESS/TRADE_FINISHED、加盟店の一意性）→ **冪等**で注文を更新 + サブスク作成 + アカウントを有効化。skill はこの API には絶対に触れない |
| `/payment/alipay/return` | ブラウザの戻りページ | 公開パス。支払い後に「支払い成功」を表示し、ページ内でバックエンドの実際の状態をポーリング |

- 未支払いの注文は **2時間で自動クローズ**。ユーザーが途中で辞めたら → そのまま `create-order` をやり直し。旧注文は放置でOK。
- スクリプトは `paymentHtml` を一時 HTML ファイルに書き出し、agent がシステムコマンドで開けば Alipay のレジに入れます
  （QR スキャンか、Alipay 内ログインで支払い）。

### アクティベーション経路（自動、人工不要）

notify の署名検証を通過 → `paymentOrders` を支払い済みにマーク → `user_subscriptions` を作成/順延
（`planId`、`currentPeriodEnd` は durationDays から計算。更新は元の満了日に順延）→
`users.accountStatus: active` + `subscriptionStatus: ACTIVE` → 戻りページが paid をポーリングして成功表示。

### 支払い後に必ず新しいログイン状態へ交換（重要）

JWT にはサブスク宣言が入っています（pending アカウントは `NONE`）。**支払いの着金は DB だけを更新し、発行済みの
JWT は書き換えません**——古い token の宣言は NONE のままで、それでログインリンクを生成すると「会員じゃない」ように見えます。
そこで skill は `paid` / PayPal の `ACTIVE` を確認した後、まず `refresh-login` を実行し（再ログインで新しい JWT に交換、宣言が ACTIVE になる）、
それからリンク2を生成します。これは設計上の挙動で、脆弱性の修正ではありません。

## PayPal サブスクチャネル（skill が代行、Web 版かつ非 HarmonyOS）

プランは Premium Monthly の1つのみ（約 $1/月、`/api/subscription/plans` の返り値に準拠）。**月次の自動更新**で、
ユーザーはいつでも PayPal 側で解約できます。

### インターフェース契約（skill スクリプトがラップ済み。agent が直接リクエストを組み立てることはない）

| インターフェース | メソッド | 説明 |
|---|---|---|
| `/api/subscription/plans` | GET | Bearer 認証。利用可能なプラン一覧を返す（現在は1つのみ） |
| `/api/subscription/create` | POST | body `{planId}` → `{subscriptionId, approveUrl, status}` を返す。`status` は通常 `APPROVAL_PENDING` |
| `/api/subscription/create` | GET | Bearer 認証。`{activeSubscription, allSubscriptions}` を返す。agent は `activeSubscription.subscription.status === 'ACTIVE'` をポーリング |
| `/api/subscription/verify` | POST | 成功ページが自動呼び出し（cookie 付き）。webhook 未着時に PayPal API で直接アクティベート |
| `/subscription/success` | ブラウザの戻りページ | PayPal 承認後の着地ページ。verify を自動ポーリングし、アクティベート後にホーム/元のページへ戻る |
| `/subscription/cancel` | ブラウザページ | ユーザーがキャンセルまたは失敗した場合の着地ページ。やり直し可能 |

### 代行フロー

```
create-order --provider paypal  # → approveUrl を返し、ローカル HTML ファイルに書き込む
HTML ファイルを開く             # → ブラウザが PayPal 承認ページへ遷移
query（10〜15秒ごと）            # → ACTIVE になるまでポーリング
refresh-login                   # → 新しい JWT に交換（サブスク宣言が ACTIVE）
login-link --target home        # → 正式なログインリンクを生成
```

- 1時間以内に完了しなかった PENDING サブスクはバックエンドが自動クリーンアップします。やり直せばOK。
- ユーザーが `create-order` を繰り返した場合、バックエンドは仍有効な `APPROVAL_PENDING` サブスクを再利用し、409 を回避します。
- Alipay と同じく：支払いの着金は DB を更新するだけで、古い JWT は自動的に更新されません。ホームページのリンクを送る前に**必ず** `refresh-login` を実行してください。

## サブスクページの4チャネル

サブスクページ `src/app/(public)/subscription/page.tsx` は実行環境に応じて表示を切り替えます：

| チャネル | 環境 | 仕組み | アクティベーション方式 |
|---|---|---|---|
| **Alipay（主力）** | Web 版 | `AlipayPaymentSection` が vibepay API を使用（上の表） | notify によるサーバー自動アクティベーション、秒単位 |
| PayPal サブスク | Web 版（非 HarmonyOS） | `/api/subscription/create` → PayPal 認可へ遷移。月次の自動更新で、いつでも解約可能（`/api/subscription/manage`） | PayPal Webhook（`BILLING.SUBSCRIPTION.*`）で自動的に active へ |
| WeChat スキャンサブスク | Web 版（非 HarmonyOS） | ページ下部の「WeChat スキャンでサブスク」：QR で送金 | **手動確認**。着金が遅れることがあります。支払った直後に失敗と決めつけないこと |
| 華為アプリ内課金 | HarmonyOS アプリ内 | ネイティブ `NativeBridge.purchaseSubscription()` | `/api/subscription/activate-huawei` が華為の注文を検証してから有効化 |

PayPal のプランと価格は `/api/subscription/plans` から動的に読み込み。ページの固定文言：Auto-renews. Cancel anytime.

## 状態と遷移

- Alipay の支払い完了 → 戻りページに成功表示。PayPal 成功 → `/subscription/success` → アカウントが active →
  `next` パラメータが指定する元のページへ自動で戻ります（なければホーム）。
- 既にサブスク中のユーザーがサブスクページを開く → "You're All Set!" と表示され、3秒後に自動でホームへ。
- 支払い失敗/キャンセル（PayPal）→ `/subscription/cancel`。再発行できます。

## 調査

| 現象 | 対処 |
|---|---|
| Alipay で支払ったのに `query` が pending のまま | notify が遅れることはまれにあります。30秒待ってもう一度照会。それでもダメならユーザーにブラウザの戻りページの状態を見てもらい、それでもダメならプラットフォームサポート（dongtao@outlook.com）へ `outTradeNo` を添えて連絡 |
| Alipay で支払ったのに、リンク2で入ってもまだ弾かれる | `refresh-login` が抜けている（古い JWT の宣言が未更新）——先に `refresh-login`、それから `login-link` |
| PayPal の `query` がずっと PENDING | ユーザーが PayPal での承認を完了していません。ブラウザで承認リンクが開かれたか確認を。承認済みなのに PENDING なら webhook 遅延の可能性あり。成功ページで数秒待つか再読み込みしてもらう |
| PayPal の `query` が 409 を返す | 未完了の PENDING サブスクが既に存在します。1時間待てば自動失効。またはブラウザで旧リンクの承認を完了 |
| PayPal で支払ったのに、リンク2で入ってもまだ弾かれる | Alipay と同じ：先に `refresh-login`、それから `login-link` |
| 支払ったのにまだ 403（PayPal） | Webhook に遅延が出ることがあります。再ログインで状態を更新 |
| WeChat で払ったのに開通しない | 手動確認は非同期です。数時間経っても開通しなければプラットフォームサポートへ |
| サブスクページに "No subscription plans available" と表示 | `/api/subscription/plans` に利用可能な PayPal プランがなく、プラットフォーム側の設定問題。中国国内のユーザーは Alipay を使えばOK |

## 歴史的備考

コードにはもう一セット**古い** Alipay ウェブ決済（`src/lib/alipay.ts`、`/api/payment/create-order`、
¥9.90/¥99 の一括買い切り、サンドボックスで鍵未設定時に模擬決済へダウングレード）がありますが、常にサブスクページ UI には接続されておらず、vibepay とは
無関係です。skill はこれに一切触れません。現行チャネルは `alipay-vibepay.ts` です。
