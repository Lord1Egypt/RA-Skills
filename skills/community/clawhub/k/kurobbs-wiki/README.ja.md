# 🌊 kurobbs-wiki — クルミナルストリート鳴潮 WIKI 検索 + 編成アシスタント

**Agent Skill オープン標準**（SKILL.md）に準拠した汎用スキルです。クルミナルストリート（kurobbs）の公開 API を直接叩いて、鳴潮（Wuthering Waves）の図鑑・攻略・キャラクター資料を検索できます。さらに**メカニズム解析 + 編成エンジン**を内蔵しており、自分のクルミナルストリートアカウントにログインして実際のキャラクターでパーティ編成も可能です。Agent Skill を読み込める任意の AI（Claude、Cursor、Copilot、Gemini、OpenClaw など）で利用できます。

> このプロジェクトは、日々の鳴潮プレイ中に「キャラ攻略や編成を調べるのに毎回 Web を開くのが面倒」という課題から着想を得て、1 つの skill にすれば会話の中でそのまま質問できるようにしたものです。

---

## ✨ 機能一覧

| モジュール | コマンド | 説明 |
|------|------|------|
| 🔍 カタログ/一覧 | `tree` / `list` | 分類カタログツリー（170+ ノード）+ 分類ごとの項目 |
| 📖 項目詳細 | `detail` | キャラ/武器/アイテム/攻略の詳細。`--render` で Markdown 整形、`--section` でセクションを正確に抽出 |
| 🔎 名前検索 | `search` | 分類をまたいで検索、3 階層のサブカテゴリを自動で走査 |
| 🖼️ コミュニティ投稿メディア | `post` | WAF を迂回して画像・表紙・m3u8 動画を取得 |
| 🧠 メカニズム解析 | `probe` | 6 次元のメカニズムプロファイル（エフェクト/バフ/流派/スキル/エコー/武器） |
| 🤝 ペア編成エンジン | `pair` / `team` | 2 キャラの 5 次元互換スコア、プール選択編成、全 60 人列挙、攻略クロス検証によるプール補完 |
| 🎯 LLM 精査 | `candidates` + `--profile` | ルールによる粗選別候補 + LLM による編成ごとの精査（最も精度が高い編成） |
| 👤 マイアカウント | `my` | クルミナルストリートにログイン、実際のキャラを確認、自分のキャラで編成、token 更新 |

---

## 📦 インストール

### 方法 1：ローカルディレクトリからインストール（最も簡単）

本リポジトリの `kurobbs-wiki/` ディレクトリを、あなたの AI の skills ディレクトリ（Claude Code、Cursor、Copilot などが対応）に置きます。対応する agent の場合は次のようにします：

```bash
# SKILL_DIR を本リポジトリのルートの絶対パスに指定
# Windows の例
set SKILL_DIR=D:\tools\kurobbs-wiki

# macOS / Linux の例
export SKILL_DIR=~/tools/kurobbs-wiki
```

### 方法 2：npx skills 経由（マーケットに収録された後）

```bash
npx skills add Alphamancer/kurobbs-wiki
```

> 公開後はマーケットからワンクリックでインストールできます。詳しくは後述の「公開と収録」をご覧ください。

### 依存関係

- **Python 3.8+**（標準ライブラリのみ、`wikiquery.py` にサードパーティ依存はありません）
- **Playwright**（`post` でコミュニティ投稿のメディアを取得するときのみ必要）
  ```bash
  pip install playwright && playwright install chromium
  ```
- **ffmpeg**（任意、`--download-video` で m3u8 動画を mp4 としてダウンロードするときに使用）

---

## 🚀 クイックスタート

```bash
cd $SKILL_DIR

# 1. カタログツリーを初期化（~/.kurobbs-wiki-cache/ にキャッシュ）
python -X utf8 -u scripts/wikiquery.py tree

# 2. キャラクターを検索
python -X utf8 -u scripts/wikiquery.py search 穗穗 --preview --limit 3

# 3. 攻略本文の一部の節を取得
python -X utf8 -u scripts/wikiquery.py detail <previewEntryId> --section "編隊&隊伍軸推薦"

# 4. メカニズム解析 + 編成
python -X utf8 -u scripts/wikiquery.py probe 穗穗
python -X utf8 -u scripts/wikiquery.py team 穗穗 --pool 洛瑟菈,今汐,秧秧 --top 3

# 5. アカウントにログインして、実際のキャラで編成
python -X utf8 -u scripts/wikiquery.py my login    # ブラウザで電話番号入力→スライダー→認証コード入力
python -X utf8 -u scripts/wikiquery.py my roles
python -X utf8 -u scripts/wikiquery.py my team 穗穗 --guide-pool --top 5
```

> 💡 **ヒント**：すべてのコマンドは skill ディレクトリ内で実行し、`-X utf8 -u` を付けてください（Windows で中文/emoji を出力するために必要）。

---

## 🧠 編成エンジンの使い方

### 2 キャラのスコアリング

```bash
python -X utf8 -u scripts/wikiquery.py pair 穗穗 洛瑟菈
```

5 次元それぞれ 20 点：エフェクト協同 / アウトロスキル一致 / 役割の補完 / エコー連携 / 発動サイクル。80 以上で高い相性。

### キャラクタープールから編成

```bash
python -X utf8 -u scripts/wikiquery.py team 穗穗 --pool 洛瑟菈,今汐,秧秧 --top 3   # プールを指定
python -X utf8 -u scripts/wikiquery.py team 穗穗 --all --top 5                    # 全 60 人を列挙
python -X utf8 -u scripts/wikiquery.py team 穗穗 --guide-pool --top 5             # 攻略クロス検証で自動補完
```

各編成には出所が付記されます：🟢 攻略で裏付け / 🟡 混合 / 🔵 エンジン推定。確認用に 📚 攻略 URL も付きます。

### LLM 精査（最も精度が高い編成）

```bash
# ステップ 1：ルールで候補プールを粗選別（秒単位）
python -X utf8 -u scripts/wikiquery.py candidates 绯雪 --guide-pool

# ステップ 2：候補編成 + 3 キャラの 6 次元完全プロファイルを取得（出力が大きいのでファイルにリダイレクト）
python -X utf8 -u scripts/wikiquery.py team 绯雪 --pool 千咲,维里奈,穗穗 --profile --top 10 > %TEMP%\team_profile.txt
```

Claude が実際のプロファイルデータに基づいて編成ごとに 6 次元で精査し、「機制拐」「協奏副C」などルールでは判断しにくい役割を識別します。

---

## 🔐 プライバシーとデータについて

> ⚠️ **必ずお読みください** —— 本 skill にはアカウントデータを読み取るログイン機能が含まれています。

- **WIKI 検索（`tree`/`list`/`detail`/`search`/`probe`/`pair`/`team`）**：すべて**公開・認証なし**の API を使用します。**ログイン不要**で、個人データには一切関与しません。
- **「マイアカウント」機能（`my login`/`my roles`/`my team`/`my sync`）**：ブラウザでクルミナルストリートにログインする操作があなたの側で必要です。ログイン後、以下のデータは**あなたのローカル** `~/.kurobbs-wiki-cache/` に保存されます：
  - `account.json` — ログイン token + あなたのキャラリスト
  - `role_details/` — 各キャラの共鳴チェーン解放、実際の武器/エコー、スキルレベル、ステータス
- **これらのデータはローカルにのみ保存され、サーバーへは一切アップロードされません**。token は約 45 分で期限切れになり、`my renew` で更新できます。
- 本 skill は、未ログイン時にあなたのアカウントキャラを推測・偽装することは**ありません**。また、第三者にアカウントデータを送信することもありません。

**完全にオフライン/非ログインで使いたい場合**：`tree`/`search`/`detail`/`probe`/`pair`/`team` だけを使えばよく、`my` 系コマンドはまったく不要です。

---

## 📚 ディレクトリ構成

```
kurobbs-wiki/
├── SKILL.md               # Skill の指示（トリガー条件、コマンド早見表、ワークフロー、重要ポイント）
├── README.md              # 本ファイル（利用者向け）
├── PUBLISHING.md          # 公開手順リスト（作者用。利用者は読む必要なし）
├── _meta.json             # skill のメタデータ
├── references/
│   └── catalogue-map.md   # 分類 ID 対応早見表（170+ ノード）
└── scripts/
    ├── wikiquery.py       # メイン CLI（tree/list/detail/search/probe/pair/team/candidates/my）標準ライブラリのみ
    ├── post_fetch.py      # コミュニティ投稿メディアの取得（Playwright で WAF を迂回）
    └── kuro_login.py      # クルミナルストリートへのログイン（ブラウザ操作）
```

---

## ⚠️ 既知の制限

- **プライベート API、公式ドキュメントなし**：フィールド構造はクルミナルストリートの改版で変化する可能性があります。エラー時はまず `tree --refresh` でカタログツリーを引き直してください。
- **低頻度の利用を推奨**：公開・認証なしのインターフェースのため、頻繁なリクエストはリスク管理に引っかかる可能性があります。スクリプトには 0.05 秒のレート制限が組み込まれています。
- **カテゴリは動的に変化**：ゲーム更新で新しいバージョンアクティビティカテゴリが追加されます。新コンテンツが見つからないときは `list <カテゴリ> --refresh` または `tree --refresh` を実行してください。
- **攻略項目は「プレースホルダーカード」**：`detail <5桁のID>` は 2031 を返すことがあります。その場合は `search --preview` で埋め込まれた実際の entryId を取得してください（これは構造であり、バグではありません）。
- **Windows では `-X utf8 -u` を必ず付ける**：付けないと中文/emoji の出力が GBK エンコーディングでクラッシュします。

---

## 🧾 ライセンス

[MIT](LICENSE)

---

## 🙏 気に入ったら、もっと多くの人に届けてください

この skill が役に立つと思ったら、鳴潮をプレイしている友人に共有するか、あなたの skill マーケットに収録してください。

インストールコマンド：

```bash
npx skills add Alphamancer/kurobbs-wiki
```

---

## 🤝 コントリビューション

issue と PR を歓迎します。開発時には次の点に注意してください：

- 修正後は `python -X utf8 -c "import py_compile; py_compile.compile('scripts/wikiquery.py', doraise=True)"` で文法チェックを実行
- `wikiquery.py` は標準ライブラリのみを維持（`post` サブコマンドを除く）。検索のメイン処理にサードパーティ依存を追加しない
- SKILL.md の「重要ポイント」と「既知の詰まりどころ早見表」の規約を遵守
