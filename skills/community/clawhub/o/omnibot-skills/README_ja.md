<div align="center">

# 🤖 Omnibot

### AIエージェントのためのブラウザインフラ

[![Version](https://img.shields.io/badge/version-2.4.0-blue?style=flat-square)](./SKILL.md)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)]()

[![SkillHub](https://img.shields.io/badge/SkillHub-omnibot-00A8E0?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNOCAwTDAgNFYxMkw4IDE2TDE2IDEyVjRMOCAwWiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=)](https://skillhub.cn/skills/omnibot)
[![ClawHub](https://img.shields.io/badge/ClawHub-omnibot--skills-FF6B35?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNOCAxQzQuMTMgMSAxIDQuMTMgMSA4QzEgMTEuODcgNC4xMyAxNSA4IDE1QzExLjg3IDE1IDE1IDExLjg3IDE1IDhDMTUgNC4xMyAxMS44NyAxIDggMVpNOCAzQzkuNjYgMyAxMSA0LjM0IDExIDZDMTEgNy42NiA5LjY2IDkgOCA5QzYuMzQgOSA1IDcuNjYgNSA2QzUgNC4zNCA2LjM0IDMgOCAzWiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=)](https://clawhub.ai/dennisjcy/skills/omnibot-skills)

[![Chrome ウェブストア](https://img.shields.io/badge/Chrome%20ウェブストア-ブラウザ拡張機能-4285F4?style=flat-square&logo=google-chrome&logoColor=white)](https://chromewebstore.google.com/detail/fojlpefamkmjbboafmjkkaejohagbdgn)

**AIエージェントを本物のChromiumブラウザに接続します。**<br>
ページを読む。ボタンをクリック。フォームに入力。ナビゲート。コンテンツを抽出。証拠を収集。<br>
ローカルデーモンとCLIを通じてすべてを実現——ヘッドレスハックなし、脆弱なセレクタなし。

[クイックスタート](#-クイックスタート) · [仕組み](#-仕組み) · [機能](#-機能) · [ドキュメント](#-ドキュメント)

🌐 **[English](./README.md)** · **[中文](./README_zh.md)** · **[한국어](./README_ko.md)** · **[Español](./README_es.md)** · **[Français](./README_fr.md)** · **[Deutsch](./README_de.md)**

</div>

---

## 🚀 Omnibotとは？

Omnibotは、AIエージェントと実ウェブのギャップを埋めます。**Hermes**、**Claude Code**、**Codex**、**OpenCode**などのエージェントに、生きているChromiumブラウザを見て操作する能力を与えます——人間と同じように。

```
┌──────────────┐         ┌──────────────┐         ┌──────────────────┐
│   AI Agent   │ ──CLI──▶│  Omnibot     │ ──WS──▶ │  Chromium        │
│  (Hermes,    │         │  デーモン    │         │  拡張機能        │
│   Claude...) │         │  :18765      │         │  (本物ブラウザ)  │
└──────────────┘         └──────────────┘         └──────────────────┘
```

Puppeteerなし。Playwrightなし。本物ふりのヘッドレスブラウザなし。<br>
**本物のブラウザ。本物のCookie。本物の拡張機能。本物のユーザーセッション。**

## 🎬 デモ動画

<table>
<tr>
<td width="50%" align="center" valign="top">

### WeChat公式アカウント分析
**HermesがWeChatバックエンドデータとトレンドを自動分析**

[![WeChat分析](https://img.youtube.com/vi/xZ-_0TInCRE/maxresdefault.jpg)](https://youtu.be/xZ-_0TInCRE)

*HermesエージェントがWeChat公式アカウントバックエンドに自動ログインし、ユーザー成長、記事閲覧、ユーザー層を抽出して完全なデータ分析レポートを生成します。*

</td>
<td width="50%" align="center" valign="top">

### X（Twitter）AIニュース収集
**HermesがXで最新AIニュースを自動取得**

[![X AIニュース](https://img.youtube.com/vi/PknnOhAE6bI/maxresdefault.jpg)](https://youtu.be/PknnOhAE6bI)

*HermesエージェントがX（Twitter）を自動ブラウジングし、最新のAIニュースを検索・フィルタリングして構造化されたニュース速報に整理します。*

</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">

### 裁判文書分析
**Hermesが殺人事件の判決文を検索・分析**

[![裁判分析](https://img.youtube.com/vi/PQQNDbzgXgQ/maxresdefault.jpg)](https://youtu.be/PQQNDbzgXgQ)

*Hermesエージェントが裁判文書サイトで殺人事件を検索し、8件の全文を精読して、犯罪者プロファイル、動機分析、犯行特徴を含む完全な分析レポートを生成します。*

</td>
<td width="50%" align="center" valign="top">

### Toutiao自動投稿
**Hermesが記事をToutiaoに自動公開**

[![Toutiao投稿](https://img.youtube.com/vi/elUxHLp1C4Q/maxresdefault.jpg)](https://youtu.be/elUxHLp1C4Q)

*HermesエージェントがToutiaoに自動ログインし、タイトル、本文を入力して画像を挿入、カバーと広告収益を設定し、プレビュー後にワンクリックで記事を公開します。*

</td>
</tr>
</table>

<div align="center">

**さらに多くのユースケースがあなたを待っています！**

</div>

## ✨ 機能

<table>
<tr>
<td width="50%" valign="top">

### 🔍 観察
- レンダリングされたページコンテンツをクリーンなテキスト/Markdownとして読み取り
- インタラクティブ参照付きの完全なアクセシビリティツリーをスナップショット
- 全ページまたは特定の視覚領域のスクリーンショットをキャプチャ
- コンソールログ、ネットワークトラフィック、DOM状態を検査

</td>
<td width="50%" valign="top">

### 🎯 操作
- セマンティックロール、プレースホルダー、またはアクセシビリティ参照で要素をクリック
- フォームに入力、オプションを選択、チェックボックスをチェック——イベントディスパッチ付き
- ページ間をナビゲート、タブとタブグループを管理
- ドラッグ、スクロール、タイプ、キー押下——人間のようなインタラクション

</td>
</tr>
<tr>
<td width="50%" valign="top">

### ✅ 検証
- 条件を待機：URL変更、要素の可視性、テキストの出現
- 要素状態をアサーション：有効、可視、チェック済み、値
- ネットワークログとAPI証拠をキャプチャ
- 観察 → 操作 → 検証ループによる多段階検証

</td>
<td width="50%" valign="top">

### 🛡️ 信頼性
- セッショントークンワークフロー分離
- タブ指定コマンド——予期しないクロスタブ変更なし
- セマンティックから生CDPまでの7段階フォールバックチェーン
- 組み込みのアンチパターンガードとセーフティルール

</td>
</tr>
</table>

## ⚡ クイックスタート

### 1. CLIをインストール

npm経由でOmnibot CLIをグローバルにインストール（推奨）：

```bash
npm install -g @omniaibot/omnibot
```

プラットフォームを自動検出し、対応するバイナリをインストールします。インストール後、`omnibot doctor`を実行して確認してください。

### 2. ブラウザ拡張機能を読み込む

- [Chrome Web StoreのOmnibot拡張機能ページ](https://chromewebstore.google.com/detail/fojlpefamkmjbboafmjkkaejohagbdgn)を開きます
- 「Chromeに追加」をクリックしてインストールを完了します
- ブラウザの右上にあるOmnibot拡張機能アイコンをクリックします
- 拡張機能に**接続済み**と表示されていることを確認するか、ポップアップからマシンコードをコピーしてアクティベーションコードを購入します

デフォルトでは、拡張機能はローカルWebSocketサービス`127.0.0.1:18765`に接続します。

拡張機能ポップアップ設定：
- **WebSocketアドレス**：`ws://127.0.0.1:18765`
- 接続ステータスは自動更新されます
- 接続に失敗した場合は、まず`omnibot doctor`を実行してデーモンステータスを確認してください

### 3. 接続を確認

デーモンを手動で起動する必要はありません。任意のブラウザコマンドを実行すると、omnibot CLIがローカルデーモンを自動起動し、ブラウザ拡張機能がWebSocket経由で`127.0.0.1:18765`に接続します。

```bash
omnibot doctor
omnibot tabs
```

`doctor`はデーモンと拡張機能のステータスをチェックします。`tabs`は利用可能なブラウザタブを一覧表示します。

`doctor`が拡張機能が接続されていないと表示した場合は、Chrome/Edgeを開き、ブラウザ拡張機能を読み込むか再読み込みし、少なくとも1つのHTTP/HTTPSタブを開いたままにしてください。

### 4. エージェントスキルをインストール

Omnibot v2はMCPプロンプトインジェクションの代わりにスキルを使用します：

```bash
omnibot skills install --agent hermes --profile nuwa
omnibot skills install --agent opencode
omnibot skills install --agent claude
omnibot skills install --agent codex
```

組み込みスキルのパスを表示：

```bash
omnibot skills path
```

Omnibotには、人気のあるAIエージェントのスキル設定が組み込まれています。クイックスタートページからエージェントを選択して、インストールコマンドを取得してください。

## 🔄 仕組み

すべてのブラウザ操作は規律あるループに従います：

```
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │  観察    │ ───▶ │  操作    │ ───▶ │  検証    │──┐
  │          │      │ (1回)    │      │          │  │
  └──────────┘      └──────────┘      └──────────┘  │
       ▲                                              │
       └──────────── 失敗時はフォールバック ──────────┘
```

1. **観察** — ページをスナップショット、コンテンツを読み取り、現在の状態をチェック
2. **操作** — 利用可能な最良のパターンを使用して1回の操作を実行
3. **検証** — 証拠で期待される状態変化を確認

検証が失敗した場合、エージェントは再観察し、次のフォールバックティアを試みます。盲目のリトライなし。推測なし。

## 🧩 ネイティブコマンドルーター

Omnibotは常にジョブに最も狭いネイティブコマンドを選択します：

| 意図 | ネイティブコマンド | これではない |
|------|------------------|-------------|
| ページコンテンツを読み取り | `read`, `get text` | ~~`execute-js`~~ |
| ボタンをクリック | `find --action click`, `click @eN` | ~~`querySelector().click()`~~ |
| フォームに入力 | `fill`, `type` | ~~`element.value = "..."`~~ |
| 状態を待機 | `wait` | ~~`sleep 3`~~ |
| スクロール | `scroll`, `scrollintoview` | ~~`window.scrollTo()`~~ |

**ネイティブが最初。JavaScriptはフォールバックであり、近道ではありません。**

## 🏗️ アーキテクチャ

```
Agent Skill (SKILL.md)
    │
    ▼
omnibot CLI  ──────────────────────────────┐
    │                                       │
    ▼                                       ▼
ローカルデーモン (:18765)           Chromium拡張機能
    │                                       │
    ├── セッション管理                      ├── DOMアクセス
    ├── コマンドルーティング                ├── アクセシビリティツリー
    ├── タブ追跡                            ├── ネットワークインターセプト
    └── ワークフロー分離                    └── 視覚領域検出
```

**主要な設計原則：**
- **信頼性 > 便利性** — すべての操作が検証される
- **明示的状態 > 暗黙的状態** — 隠れた仮定なし
- **パターン > コマンド** — APIではなくタスクから始める
- **フォールバックは許可されるが、最初ではない**

## 📚 ドキュメント

| リソース | 説明 |
|---------|------|
| [SKILL.md](./SKILL.md) | 完全なエージェント実行仕様 |
| [コマンドリファレンス](./references/command-reference.md) | 完全なCLIコマンドルックアップ |
| [操作パターン](./references/operation-patterns.md) | 読み取り、クリック、入力、スクロール、ナビゲート、待機、抽出、バッチ |
| [アンチパターン](./references/anti-patterns.md) | よくある間違いと回避方法 |
| [デバッグと証拠](./references/debugging-and-evidence.md) | スクリーンショット、ネットワークログ、トレース、記録/再生 |
| [セッションとタブ](./references/session-and-tabs.md) | ワークフロー分離とタブ指定 |
| [フォールバック操作](./references/fallback-operations.md) | 7段階フォールバックチェーンの説明 |

## 🤝 互換性のあるエージェント

Omnibotは、CLIコマンドを実行できる任意のエージェントシステムで動作します：

- 🧠 **Hermes** — ネイティブ統合
- 🟠 **Claude Code** — スキルファイルを介して
- 📦 **Codex** — スキルファイルを介して
- 🔓 **OpenCode** — スキルファイルを介して
- 🔧 **CLI対応のエージェント** — `omnibot`コマンドを介して

## 📋 ワークフロー例

```bash
# ワークフローコンテキストを設定
export OMNIBOT_SESSION_TOKEN=research

# 新しいタブを開く
omnibot open "https://github.com"

# インタラクティブ参照付きでページをスナップショット
omnibot snapshot -i --tab-id $TAB_ID

# 検索ボックスをクリックして入力
omnibot find placeholder "Search GitHub" --action type \
  --action-value "omnibot" --tab-id $TAB_ID

# Enterを押す
omnibot press Enter --tab-id $TAB_ID

# 結果を待機
omnibot wait --text "repositories" --tab-id $TAB_ID

# 結果を読み取り
omnibot read --tab-id $TAB_ID
```

## 📄 ライセンス

独占的。詳細はLICENSEを参照してください。

---

<div align="center">

**ウェブを「見る」必要があるエージェントのために——単にフェッチするだけでなく。**

[⭐ GitHubでスター](https://github.com/DennisJcy/Omnibot-skills) · [📖 スキル仕様を読む](./SKILL.md)

</div>
