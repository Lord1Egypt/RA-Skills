<div align="center">

<h1 style="border-bottom: none">
  <b><a href="https://tourmind.com/skills">Hotel Booking AI</a></b><br />
  <strong>パーソナル AI ホテル検索・予約アシスタント</strong>
</h1>

<a href="https://auth.journione.ai/">
  <img alt="Hotel Booking AI — AI エージェントでホテルを検索、比較、予約" src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/hero/tourmind-booking-skills.png" style="width: 100%" />
</a>

<br />

<p align="center">
  より良い滞在先を見つけ、リアルタイム料金を比較し、安心して予約。
</p>

<br />

<div align="center">
  <a href="https://tourmind.com/skills">製品ページ</a> |
  <span>ライブデモ</span> |
  <a href="https://tourmind.com">会社情報</a>
</div>

<br />

[![ClawHub ダウンロード](https://img.shields.io/badge/ClawHub_downloads-1.6k-F97316)](https://clawhub.ai/tourmind/skills/hotel-booking-ai)
[![Skill バージョン](https://img.shields.io/badge/Skill_version-1.0.8-2563EB)](SKILL.md)
[![ライセンス](https://img.shields.io/github/license/tourmind-com/Hotel-Booking-AI)](LICENSE)

</div>

<br />

<div align="center">
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.es.md">Español</a>
</div>

<br />

AI エージェントをパーソナルなホテル予約アシスタントに変えます。Hotel Booking AI は世界中のホテルを検索し、主要 OTA とホテルサプライヤーのリアルタイム客室料金を比較し、写真やキャンセル条件を表示します。最終料金を再確認し、同じ会話の中で予約、決済、キャンセル、注文照会までサポートします。

ホテル検索、ホテル・客室詳細、リアルタイム料金、空室確認は公開機能です。予約する段階までアカウントやログインは必要ありません。

## デモ

### 1. リアルタイムの空室があるホテルを検索

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif" alt="Hotel Booking AI リアルタイムホテル検索デモ" width="720" />
  </a>
</div>

### 2. 客室、写真、料金を比較

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif" alt="Hotel Booking AI 客室・料金比較デモ" width="720" />
  </a>
</div>

### 3. 最終料金を再確認して安全に決済

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif" alt="Hotel Booking AI 予約・決済デモ" width="720" />
  </a>
</div>

## 1つのチャットで滞在を計画・予約

- 都市、ホテル、ランドマーク、駅、住所、スキー場などを、座標を推測せずに検索します。
- 最大 20 件のホテル候補を比較し、リアルタイム客室商品が確認できた中から上位 5 件を提示します。
- 実際の1泊料金と滞在合計、ホテル・客室写真、ベッド、食事、税金、キャンセル条件、在庫状態を確認できます。
- 予算、距離、星、朝食、設備、客室タイプ、無料キャンセルなどの希望条件で絞り込めます。
- 一般的なおすすめではなく、各ホテルが旅行条件に合う根拠を確認できます。
- 予約確定前に、選択した客室の正確な料金と空室状況を再確認します。
- 同じ会話で予約を作成し、Stripe、WeChat Pay、Alipay で決済、注文照会、対象予約のキャンセルができます。

## 対応 AI クライアント

| クライアント | 利用方法 |
|---|---|
| OpenClaw | ClawHub から直接インストール、または個人 Skills ディレクトリにこのリポジトリをクローン |
| WorkBuddy | このリポジトリをユーザー Skill としてインストールまたはインポート |
| OpenAI Codex | Skills 画面、または現在のバージョンが対応するローカル Skills ディレクトリからインストール |
| Claude Code | `~/.claude/skills` に個人 Skill としてインストール |
| Agent Skills 互換クライアント | ルートの `SKILL.md` を読み込み、HTTPS `POST` リクエストを送信できる場合に利用可能 |
| MCP 対応 AI クライアント | 付属の [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) を使用 |

## 1分でインストール

### 方法1：ClawHub からインストール

```bash
openclaw skills install @tourmind/hotel-booking-ai
openclaw gateway restart
```

### 方法2：GitHub からインポート

AI クライアントの Skills 画面で次のリポジトリをインストールまたはインポートします。

```text
https://github.com/tourmind-com/Hotel-Booking-AI.git
```

クライアントがファイルシステムから Skill を読み込む場合は、個人 Skills ディレクトリにクローンします。

```bash
CLIENT_SKILLS_DIR="<クライアントの Skills ディレクトリ>"
mkdir -p "$CLIENT_SKILLS_DIR"
git clone https://github.com/tourmind-com/Hotel-Booking-AI.git "$CLIENT_SKILLS_DIR/hotel-booking-ai"
```

主な個人 Skill ディレクトリ：

| クライアント | ディレクトリ |
|---|---|
| OpenClaw | `~/.openclaw/skills` |
| WorkBuddy | `~/.workbuddy/skills` |
| OpenAI Codex | Skills 画面、または現在の Codex バージョンが対応するローカルディレクトリ |
| Claude Code | `~/.claude/skills` |

Skills を再読み込みするか AI クライアントを再起動して、ホテルの希望を伝えてください。ローカル MCP サーバーは不要です。Hotel Booking AI は HTTPS で TourMind API を直接呼び出します。

## まず検索、予約時だけログイン

ホテル検索、ホテル・客室詳細、リアルタイム料金比較、空室確認に `user_key` は必要ありません。

予約の作成、照会、キャンセル、決済を行うとき：

1. [auth.journione.ai](https://auth.journione.ai) で Google ログインします。
2. `user_key` をコピーし、インストール済みの `hotel-booking-ai` フォルダー内に `user_key.txt` として保存します。注文操作を始めると、AI エージェントからもこの手順が案内されます。
3. macOS または Linux ではファイルのアクセス権を制限します。

   ```bash
   chmod 600 user_key.txt
   ```

`user_key.txt` はコミットしないでください。`.gitignore` の対象であり、自分の端末内だけに保存してください。

## プロンプト例

```text
2027年4月3日から4月7日まで、家族4人で東京に滞在します。駅に近く、東京ディズニーランドへ行きやすく、朝食と無料キャンセルがあり、合計12万円以内の1室を探してください。リアルタイムで予約可能な上位5件について、写真、客室タイプ、ベッド構成、1泊料金、合計料金、移動面の違い、キャンセル期限を比較してください。まだ予約しないでください。
```

```text
2番目のホテルで現在予約できる客室を見せてください。客室写真、ベッドタイプ、食事、キャンセル条件、1泊料金、滞在合計、即時予約可能かどうかを含め、最もお得なものを提案してください。選ぶまでは進めないでください。
```

```text
朝食付きキングルームを選びます。正確な料金、空室、税金、キャンセル条件、現地で発生する可能性のある料金を再確認してください。最終予約内容を表示し、予約作成や決済の前に私の明示的な確認を待ってください。
```

## Hotel Booking AI の仕組み

```text
目的地、日程、宿泊者情報
  → 都市、ホテル、または POI を解決
  → 最大 20 件のホテル候補を検索
  → 条件に合うリアルタイム客室を照会
  → 検証済み上位 5 件を並べて表示
  → ホテル詳細、客室写真、現在の料金を表示
  → 選択した客室の料金と空室を再確認
  → 明示的な確認後にのみ予約を作成
  → 必要に応じて決済、照会、キャンセル
```

最初のホテル検索に表示される価格は候補選定用の目安です。比較用の価格は条件に合うリアルタイム客室商品から取得し、最終予約には空室確認で返された最新料金を使用します。

## プライバシー、予約、決済

- 公開ホテル検索とリアルタイム料金比較はログイン不要です。
- 注文操作ではローカルの `user_key.txt` に保存された `user_key` を使用します。プロンプト、スクリーンショット、ログ、URL、コミット、Issue に含めないでください。
- Hotel Booking AI が宿泊者の法的氏名と連絡先メールアドレスを求めるのは、確認済み予約を作成する直前だけです。電話番号は収集しません。
- 予約、キャンセル、決済は明示的な操作です。エージェントは関連情報を表示し、確認を待ってから実行します。
- TourMind の客室料金には税金が含まれます。一部の地域ではチェックイン時に都市税や宿泊税が別途徴収されることがあり、返された必須料金は個別に表示されます。
- Stripe を選択すると 3.5% の決済手数料が加算されます。WeChat Pay と Alipay にも対応します。
- 読み取り専用結果リンクではホテルと客室情報のみ表示でき、予約、決済、キャンセル、アカウント・財務ページへのアクセスはできません。

## 最適な TourMind 連携を選択

| 対象 | 連携方式 | 認証モデル | 製品・リポジトリ |
|---|---|---|---|
| 消費者 / ToC | HTTP 直接接続 Skill | 検索と空室確認は公開、注文操作のみ `user_key` が必要 | **[Hotel-booking-ai](https://github.com/tourmind-com/Hotel-Booking-AI)** |
| 法人 / ToB | HTTP 直接接続 Skill | すべての API 呼び出しに Skill Token が必要 | [Tourmind-booking-skill](https://github.com/tourmind-com/Tourmind-Booking-Skills) |
| 消費者 / ToC | MCP + 付属 Skill | 公開 MCP 接続、注文操作のみ `user_key` が必要 | [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) |
| 法人 / ToB | MCP + 付属 Skill | Bearer 認証 MCP 接続 | [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) |

## API とサポート

**API ベース URL：** `https://api.tourmind.com`

| エンドポイント | 用途 | ログイン |
|---|---|---|
| `POST /skill/toc/check_skill_update` | Skill の更新確認 | 不要 |
| `POST /skill/toc/search_location` | 地域、POI、ホテルの解決 | 不要 |
| `POST /skill/toc/search_hotels` | ホテル候補の検索 | 不要 |
| `POST /skill/toc/get_hotel_detail` | ホテル詳細と画像の取得 | 不要 |
| `POST /skill/toc/query_room_rates` | リアルタイム客室と料金の取得 | 不要 |
| `POST /skill/toc/check_room_availability` | 選択料金と在庫の再確認 | 不要 |
| `POST /skill/toc/create_booking` | 確認後の予約作成 | 必要 |
| `POST /skill/toc/query_booking` | 注文の照会 | 必要 |
| `POST /skill/toc/cancel_booking` | 確認後の対象注文キャンセル | 必要 |
| `POST /skill/toc/pay_order` | 確認後の決済開始 | 必要 |

- リクエスト項目、レスポンス契約、ランキング、画像、税金、予約ルール：[references/parameter_guide.md](references/parameter_guide.md)
- ClawHub からインストール：[Hotel Booking AI](https://clawhub.ai/tourmind/skills/hotel-booking-ai)
- GitHub サポート：[Issue を作成](https://github.com/tourmind-com/Hotel-Booking-AI/issues)
- TourMind カスタマーサービス：`+86-755 3665 4666`
- ホテルサポート：`hotel@tourmind.com`
- AI 製品に関する提携：`ai@tourmind.com`

## ライセンス

[MIT](LICENSE) © 2026 TourMind
