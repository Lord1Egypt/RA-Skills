# openclaw-usage-manager

> Real-time usage dashboard & auto-switcher for dual Claude Max accounts on OpenClaw.
>
> Claude Max（Anthropic）の2アカウント（C1/C2）の使用量をリアルタイム監視し、80%超えで自動切り替えするツール。OpenClawユーザー向け。

---

## Background / 背景

**The problem:**
If you run Claude Max on two accounts, there's no built-in way to see both accounts' remaining capacity at once. You have to log into each account separately on claude.ai to check.

**問題:**
Claude Maxを2アカウントで運用していると、片方のアカウントでclaude.aiを開いても、もう片方の残量がわからない。確認するには毎回ログインし直す必要がある。

This tool was built to solve that. See the original post:
https://x.com/5dmgmt/status/2032770037728113118

---

## Table of Contents / 目次

1. [Overview / 概要](#overview--概要)
2. [Prerequisites / 前提条件](#prerequisites--前提条件)
3. [What is C1/C2? / C1/C2とは](#what-is-c1c2--c1c2とは)
4. [Getting Your Tokens / トークン取得方法](#getting-your-tokens--トークン取得方法)
5. [Installation / インストール](#installation--インストール)
6. [Usage: Dashboard / ダッシュボードの使い方](#usage-dashboard--ダッシュボードの使い方)
7. [Usage: Auto-Switcher / 自動切り替えの設定](#usage-auto-switcher--自動切り替えの設定)
8. [Verification / 動作確認](#verification--動作確認)
9. [Manual Switch / 強制切り替え](#manual-switch--強制切り替え)
10. [Security / セキュリティ](#security--セキュリティ)
11. [How It Works / 仕組み](#how-it-works--仕組み)
12. [License & Author / ライセンス・作者](#license--author--ライセンス作者)

---

## Overview / 概要

This repository provides two tools for managing dual Claude Max accounts through OpenClaw:

このリポジトリは、OpenClaw経由でClaude Max 2アカウントを管理するための2つのツールを提供します。

### 1. Usage Dashboard（使用量ダッシュボード）

A browser-based real-time dashboard showing both accounts side-by-side.

ブラウザでC1/C2両アカウントの使用量をリアルタイム表示するダッシュボード。

- **Session remaining** — 5-hour utilization with countdown / 5時間セッション残量（カウントダウン付き）
- **Weekly utilization** — 7-day usage for all models / 全モデル週間使用率
- **Sonnet-only usage** — Sonnet model weekly utilization / Sonnetモデル単体の週間使用率
- **Reset countdown** — When each window resets / リセット日時のカウントダウン
- Color-coded bars: green (<60%), amber (60–80%), red (>=80%)

### 2. Auto-Switcher（自動切り替え）

A CLI script that checks usage and switches to the other account when either the 5-hour or 7-day utilization exceeds 80%.

5時間 or 週間使用率が80%を超えたら、もう一方のアカウントに自動で切り替えるCLIスクリプト。

- Designed to run as an OpenClaw cron job every 3 hours / OpenClaw cronで3時間ごとに実行
- Security-audited (Claude Code + Codex) / セキュリティ監査済み

```
C1: {5h: 7%, 7d: 43%}
C2: {5h: 4%, 7d: 69%} ← switches to C1 when C2 crosses 80%
```

### File structure / ファイル構成

```
openclaw-usage-manager/
├── usage-dashboard/
│   ├── server.mjs        # Dashboard server (Node.js, zero dependencies)
│   └── index.html         # Dashboard UI (dark theme, responsive)
├── usage-switch/
│   ├── check.mjs               # Usage checker & auto-switcher
│   ├── setup-tokens.sh         # One-time setup (1Password → tokens.json)
│   └── setup-tokens-simple.sh  # One-time setup (interactive, no 1Password)
├── .gitignore             # Excludes tokens.json, *.env
└── README.md
```

---

## Prerequisites / 前提条件

| Requirement | Notes |
|---|---|
| [OpenClaw](https://openclaw.ai) | Installed and configured / インストール・設定済み |
| Claude Max x 2 accounts | Two separate Anthropic subscriptions (C1 and C2) / 2つのAnthropicサブスクリプション |
| Node.js >= 18 | Required for `fetch()` API / `fetch()` APIのため |
| [1Password CLI](https://developer.1password.com/docs/cli/) (`op`) | **Optional** — `op` command recommended, not required / セキュアなトークン管理（推奨だが必須ではない） |

> **Why Node.js only?** This project has zero npm dependencies. It uses only Node.js built-in modules (`http`, `fs`, `crypto`). No `npm install` required.
>
> **なぜNode.jsだけ？** npm依存パッケージはゼロ。Node.js組み込みモジュールのみ使用。`npm install` は不要です。

---

## What is C1/C2? / C1/C2とは

### Why two accounts? / なぜ2アカウントが必要か

Claude Max has usage limits that reset on a rolling schedule: a **5-hour session window** and a **7-day weekly window**. When either limit is hit, you're rate-limited until the window resets.

Claude Maxには、**5時間セッション枠**と**7日間の週間枠**の使用制限があります。どちらかに達するとリセットまでレート制限されます。

By subscribing with **two separate accounts** (C1 and C2), you can switch to the other account when one is throttled — effectively doubling your available capacity.

**2つのアカウント**（C1とC2）を持つことで、片方が制限に達したらもう片方に切り替えられます。実質的に利用可能な容量が倍になります。

```
Account C1: resets on Friday   → heavy use Mon–Thu
Account C2: resets on Tuesday  → heavy use Fri–Mon

When C1 is at 85%, switch to C2 (still at 30%).
C1が85%に達したら、まだ30%のC2に切り替え。
```

> **Tip:** This approach is most effective when the two accounts have **different reset days** (e.g., C1 resets on Friday, C2 resets on Tuesday). If both reset on the same day, the benefit is reduced.
>
> **ヒント:** 2つのアカウントの**リセット日が異なる**場合に最も効果的です（例: C1=金曜リセット、C2=火曜リセット）。同じ日にリセットされると効果は薄くなります。

---

## Getting Your Tokens / トークン取得方法

You need an Anthropic API token (`sk-ant-...`) for each account. There are two ways to manage them.

各アカウントのAnthropic APIトークン（`sk-ant-...`）が必要です。管理方法は2通りあります。

### Option A: 1Password CLI (Recommended / 推奨)

**Why:** Tokens are never stored in plaintext on disk. 1Password handles encryption and access control. The dashboard fetches tokens from 1Password on each request.

**理由:** トークンがディスク上に平文で保存されません。1Passwordが暗号化とアクセス制御を行います。ダッシュボードはリクエストごとに1Passwordからトークンを取得します。

#### Step 1: Install 1Password CLI / 1Password CLIのインストール

```bash
# macOS (Homebrew)
brew install --cask 1password-cli

# Verify installation
op --version
```

#### Step 2: Save your tokens in 1Password / トークンを1Passwordに保存

Create two items in your 1Password vault — one for each account. The token field value must start with `sk-ant`.

1Passwordのボールトに2つのアイテムを作成します。トークンフィールドの値は `sk-ant` で始まる必要があります。

```bash
# Example: create items named "Anthropic C1" and "Anthropic C2"
# The important thing is that the field value starts with "sk-ant"
```

#### Step 3: Find your 1Password item IDs / アイテムIDを確認

```bash
# List items containing "anthropic"
op item list | grep -i anthropic

# Get the item ID (26-character string)
op item get "Anthropic C1" --format=json | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])"
# Output example: abcdefghijklmnopqrstuvwxyz
```

#### Step 4: Run setup script / セットアップスクリプト実行

The setup script reads tokens from 1Password and saves them to `tokens.json` (used by the auto-switcher).

セットアップスクリプトは1Passwordからトークンを読み取り、`tokens.json`に保存します（自動切り替え用）。

```bash
# Edit the item IDs in setup-tokens.sh first (see Installation step 3)
~/.openclaw/workspace/tools/usage-switch/setup-tokens.sh

# You'll be prompted for TouchID / biometric authentication
# TouchID／生体認証を求められます
```

Expected output:
```
🔑 1Passwordからトークンを取得中...
✅ tokens.json に保存完了
✅ セットアップ完了
```

### Option B: Direct token entry (Simple / シンプル)

**Why:** Quick setup without 1Password. Suitable for single-user machines with full-disk encryption.

**理由:** 1Passwordなしで素早くセットアップ。フルディスク暗号化されたシングルユーザーマシンに適しています。

> **Warning:** This method stores tokens in plaintext. Make sure the file is not committed to git and has restrictive permissions.
>
> **注意:** この方法ではトークンが平文で保存されます。gitにコミットされないこと、パーミッションが制限されていることを確認してください。

#### Step 1: Get your tokens / トークンの取得

Use the `claude setup-token` command in your terminal. This is a built-in Claude CLI command that guides you through the OAuth flow and outputs your API token.

ターミナルで `claude setup-token` コマンドを実行します。これはClaude CLI組み込みのコマンドで、OAuthフローを案内し、APIトークンを出力します。

```bash
# For account C1 — log in to your first Anthropic account
claude setup-token
# 1. A browser window opens with the Anthropic OAuth page
# 2. Log in with your C1 account credentials
# 3. Authorize the application
# 4. The terminal displays your token (starts with sk-ant-...)
# 5. Copy this token — you'll need it in Step 2

# For account C2 — log in to your second Anthropic account
# Use a different browser profile or incognito window to avoid session conflicts
claude setup-token
# Same flow as above, but log in with your C2 credentials
# Copy the second token
```

#### Step 2: Create tokens.json manually / tokens.jsonを手動作成

```bash
# Create the directory if it doesn't exist
mkdir -p ~/.openclaw/workspace/tools/usage-switch

# Write tokens.json with your actual tokens
cat > ~/.openclaw/workspace/tools/usage-switch/tokens.json << 'EOF'
{
  "c1": "sk-ant-your-c1-token-here",
  "c2": "sk-ant-your-c2-token-here"
}
EOF

# Set restrictive permissions (owner read/write only)
# Why: prevents other users on the system from reading your API tokens
# パーミッションを制限（所有者のみ読み書き可）— 他のユーザーからの読み取りを防止
chmod 600 ~/.openclaw/workspace/tools/usage-switch/tokens.json
```

> **Note for dashboard:** If using Option B, you'll need to modify `server.mjs` to read tokens from `tokens.json` instead of 1Password. The default dashboard uses 1Password CLI directly.
>
> **ダッシュボードの注意:** Option Bの場合、`server.mjs`を修正して`tokens.json`からトークンを読む必要があります。デフォルトのダッシュボードは1Password CLIを直接使用します。

---

## Installation / インストール

### Step 1: Clone the repository / リポジトリをクローン

```bash
git clone https://github.com/Takao-Mochizuki/openclaw-usage-manager.git
cd openclaw-usage-manager
```

### Step 2: Copy files to OpenClaw workspace / ファイルを配置

**Why this path?** OpenClaw expects user tools under `~/.openclaw/workspace/tools/`. This makes them accessible to OpenClaw agents and cron jobs.

**なぜこのパス？** OpenClawはユーザーツールを `~/.openclaw/workspace/tools/` 配下に配置する規約です。これによりOpenClawのエージェントやcronからアクセス可能になります。

```bash
# Create directories
mkdir -p ~/.openclaw/workspace/tools/usage-dashboard
mkdir -p ~/.openclaw/workspace/tools/usage-switch

# Copy all files
cp usage-dashboard/server.mjs ~/.openclaw/workspace/tools/usage-dashboard/
cp usage-dashboard/index.html ~/.openclaw/workspace/tools/usage-dashboard/
cp usage-switch/check.mjs ~/.openclaw/workspace/tools/usage-switch/
cp usage-switch/setup-tokens.sh ~/.openclaw/workspace/tools/usage-switch/
cp usage-switch/setup-tokens-simple.sh ~/.openclaw/workspace/tools/usage-switch/

# Make setup scripts executable
chmod +x ~/.openclaw/workspace/tools/usage-switch/setup-tokens.sh
chmod +x ~/.openclaw/workspace/tools/usage-switch/setup-tokens-simple.sh
```

### Step 3: Configure tokens / トークンを設定

#### 方法A: 対話式入力（推奨・1Password不要）
#### Method A: Interactive input (recommended, no 1Password needed)

トークンは `claude setup-token` コマンドで取得できます。
Run `claude setup-token` to get your token.

```bash
chmod +x ~/.openclaw/workspace/tools/usage-switch/setup-tokens-simple.sh
~/.openclaw/workspace/tools/usage-switch/setup-tokens-simple.sh
# プロンプトに従いC1・C2のトークンを入力
# Follow the prompts to enter your C1 and C2 tokens
```

#### 方法B: 1Password CLI（セキュリティ重視）
#### Method B: 1Password CLI (for security-conscious users)

Replace the hardcoded item IDs in these files:

以下のファイルのアイテムIDを自分のものに書き換えます。

**`setup-tokens.sh`** — lines 5–6:
```bash
# Find and replace the item IDs:
C1_TOKEN=$(op item get your-c1-item-id ...)
C2_TOKEN=$(op item get your-c2-item-id ...)
```

**`server.mjs`** — the `ACCOUNTS` object near the top:
```javascript
const ACCOUNTS = {
  c1: { label: "C1", opItemId: "your-c1-item-id" },
  c2: { label: "C2", opItemId: "your-c2-item-id" },
};
```

Then run the 1Password setup script:

```bash
~/.openclaw/workspace/tools/usage-switch/setup-tokens.sh
```

### Step 4: Update file paths (if needed) / パスの確認

The auto-switcher (`check.mjs`) reads and writes OpenClaw's `auth-profiles.json`. The default paths are:

自動切り替え（`check.mjs`）はOpenClawの`auth-profiles.json`を読み書きします。デフォルトのパス:

```javascript
// check.mjs — update these if your OpenClaw installation differs
const AUTH_FILE   = '/Users/<you>/.openclaw/agents/main/agent/auth-profiles.json';
const TOKENS_FILE = '/Users/<you>/.openclaw/workspace/tools/usage-switch/tokens.json';
```

**Why:** These are absolute paths because the script runs as a cron job, where `~` may not expand correctly.

**理由:** cronジョブとして実行されるため、`~` が正しく展開されない可能性があり、絶対パスを使用しています。

Find your actual path:
```bash
find ~/.openclaw -name "auth-profiles.json" 2>/dev/null
```

---

## Usage: Dashboard / ダッシュボードの使い方

### Quick launch / 起動

```bash
node ~/.openclaw/workspace/tools/usage-dashboard/server.mjs
# Output: Usage Dashboard: http://localhost:18800
```

Then open http://localhost:18800 in your browser.

ブラウザで http://localhost:18800 を開きます。

### Set up the `usage` alias / `usage` エイリアスの設定

**Why an alias?** It kills any existing dashboard process, starts a fresh server, and opens the browser — all in one command.

**なぜエイリアス？** 既存のダッシュボードプロセスを停止し、新しいサーバーを起動し、ブラウザを開く — これを1コマンドで実行します。

Add to `~/.zshrc`:

```bash
alias usage='lsof -ti:18800 | xargs kill -9 2>/dev/null; sleep 0.5; node ~/.openclaw/workspace/tools/usage-dashboard/server.mjs & sleep 1 && open http://localhost:18800'
```

Then reload your shell:

```bash
source ~/.zshrc
```

Now just type `usage` to launch the dashboard.

これで `usage` と入力するだけでダッシュボードが起動します。

### Dashboard features / ダッシュボードの機能

| Feature | Details |
|---|---|
| **Auto-refresh** | Polls every 60 seconds (toggle via checkbox) / 60秒ごとに自動更新（チェックボックスで切り替え） |
| **Manual refresh** | Click the Refresh button / Refreshボタンで手動更新 |
| **30-second cache** | Prevents excessive API calls / 30秒キャッシュでAPI呼び出しを抑制 |
| **Localhost only** | Binds to `127.0.0.1:18800` — not accessible from the network / ネットワークからアクセス不可 |
| **Dark theme** | Responsive grid layout, color-coded progress bars / レスポンシブグリッド、色分けプログレスバー |

---

## Usage: Auto-Switcher / 自動切り替えの設定

### Manual run / 手動実行

```bash
node ~/.openclaw/workspace/tools/usage-switch/check.mjs
```

Example output:
```json
{
  "c1": {"5h": 7, "7d": 43, "over": false},
  "c2": {"5h": 4, "7d": 69, "over": false},
  "current": "C2",
  "needSwitch": false,
  "switched": null,
  "bothOver": false
}
```

### Output fields / 出力フィールド

| Field | Description |
|---|---|
| `c1.5h` / `c2.5h` | 5-hour session utilization (%) / 5時間セッション使用率 |
| `c1.7d` / `c2.7d` | 7-day weekly utilization (%) / 7日間週間使用率 |
| `over` | `true` if 5h OR 7d >= 80% / 5hまたは7dが80%以上で`true` |
| `current` | Currently active account / 現在のアクティブアカウント |
| `needSwitch` | `true` if a switch was needed and performed / 切り替えが必要で実行された場合`true` |
| `switched` | e.g., `"C2→C1"` if switched, `null` otherwise / 切り替え実行時の遷移 |
| `bothOver` | `true` if both accounts >= 80% — requires manual intervention / 両方80%超えで手動対応が必要 |

### OpenClaw cron setup / OpenClaw cronの設定

**Why every 3 hours?** The 5-hour window means checking every 3 hours catches approaching limits before they're hit. More frequent checks would increase API calls unnecessarily.

**なぜ3時間ごと？** 5時間枠があるため、3時間ごとのチェックで制限到達前に検知できます。より頻繁なチェックはAPI呼び出しを不必要に増やします。

Configure a cron job in OpenClaw:

OpenClawのcronに以下を設定します。

```
Schedule: 0 */3 * * * (Asia/Tokyo)
```

Prompt for the cron job / cronジョブのプロンプト:

```
Run: node ~/.openclaw/workspace/tools/usage-switch/check.mjs

Parse the JSON output:
- If needSwitch is true → run `openclaw gateway restart` and notify #your-channel
- If bothOver is true → post a manual intervention request to #your-channel
- Otherwise → do nothing (silent)
```

---

## Verification / 動作確認

After installation, verify everything works:

インストール後、以下で動作を確認します。

### 1. Check usage / 使用率確認

```bash
node ~/.openclaw/workspace/tools/usage-switch/check.mjs
```

**Expected:** JSON output with `c1` and `c2` objects showing percentages.

**期待結果:** `c1`と`c2`の使用率を含むJSON出力。

**If you see an error / エラーが出た場合:**

```json
{"error":"tokens.json not found. Run setup-tokens.sh first."}
```

Re-run the setup script. See [Getting Your Tokens](#getting-your-tokens--トークン取得方法).

セットアップスクリプトを再実行してください。[トークン取得方法](#getting-your-tokens--トークン取得方法)を参照。

### 2. Launch dashboard / ダッシュボード起動

```bash
node ~/.openclaw/workspace/tools/usage-dashboard/server.mjs
```

**Expected output:**
```
Usage Dashboard: http://localhost:18800
```

Open http://localhost:18800 — you should see two cards (C1 and C2) with progress bars showing session and weekly utilization.

http://localhost:18800 を開くと、C1とC2の2枚のカードにプログレスバーが表示されます。

### 3. Verify 1Password access (if using Option A) / 1Passwordアクセス確認

```bash
op item get your-c1-item-id --reveal --format=json | python3 -c "
import json, sys
d = json.load(sys.stdin)
f = next((x for x in d.get('fields', []) if str(x.get('value', '')).startswith('sk-ant')), None)
print('OK: token found' if f else 'ERROR: no sk-ant field found')
"
```

**Expected:** `OK: token found`

---

## Manual Switch / 強制切り替え

For testing or emergencies, you can force-switch accounts without waiting for the auto-switcher.

テストや緊急時に、自動切り替えを待たずに手動でアカウントを切り替えられます。

### Switch to C1 / C1に切り替え

```bash
node -e "
const fs = require('fs');
const AUTH = process.env.HOME + '/.openclaw/agents/main/agent/auth-profiles.json';
const TOKENS = process.env.HOME + '/.openclaw/workspace/tools/usage-switch/tokens.json';
const auth = JSON.parse(fs.readFileSync(AUTH));
const tokens = JSON.parse(fs.readFileSync(TOKENS));
auth.profiles['anthropic:default'].token = tokens.c1;
fs.writeFileSync(AUTH, JSON.stringify(auth, null, 2));
console.log('Switched to C1');
"
```

### Switch to C2 / C2に切り替え

```bash
node -e "
const fs = require('fs');
const AUTH = process.env.HOME + '/.openclaw/agents/main/agent/auth-profiles.json';
const TOKENS = process.env.HOME + '/.openclaw/workspace/tools/usage-switch/tokens.json';
const auth = JSON.parse(fs.readFileSync(AUTH));
const tokens = JSON.parse(fs.readFileSync(TOKENS));
auth.profiles['anthropic:default'].token = tokens.c2;
fs.writeFileSync(AUTH, JSON.stringify(auth, null, 2));
console.log('Switched to C2');
"
```

### After switching — restart the gateway / 切り替え後 — gatewayの再起動

**Important:** Always restart the gateway after switching tokens. The running OpenClaw process caches the token in memory.

**重要:** トークン切り替え後は必ずgatewayを再起動してください。実行中のOpenClawプロセスはトークンをメモリにキャッシュしています。

```bash
openclaw gateway restart
```

---

## Security / セキュリティ

This project has been security-audited using Claude Code and Codex. Key measures:

このプロジェクトはClaude CodeとCodexによるセキュリティ監査済みです。主な対策:

### Token handling / トークンの取り扱い

| Measure | Details |
|---|---|
| **1Password integration** | Dashboard reads tokens from 1Password on each request — no plaintext storage for the dashboard / ダッシュボードは毎回1Passwordからトークンを取得、平文保存なし |
| **tokens.json permissions** | Created with `chmod 600` (owner read/write only) / 所有者のみ読み書き可で作成 |
| **git exclusion** | `tokens.json` and `*.env` are in `.gitignore` / `.gitignore`で除外済み |
| **Injection prevention** | `setup-tokens.sh` passes tokens via environment variables to Python, preventing shell injection / 環境変数経由でPythonに渡し、シェルインジェクションを防止 |

### Dashboard security / ダッシュボードのセキュリティ

| Measure | Details |
|---|---|
| **Localhost binding** | Server binds to `127.0.0.1` only — not accessible from the network / `127.0.0.1`のみバインド、ネットワークからアクセス不可 |
| **CSRF protection** | Random 32-byte hex token required in `x-dashboard-csrf` header / ランダム32バイトCSRFトークンをAPIリクエストに要求 |
| **Host validation** | Only accepts requests from `localhost:18800` or `127.0.0.1:18800` / ローカルホストからのリクエストのみ受付 |
| **Origin validation** | Checks `Origin` header to prevent cross-origin attacks / `Origin`ヘッダーを検証しクロスオリジン攻撃を防止 |
| **POST-only API** | Usage endpoint only accepts POST — prevents data leaks via GET / 使用量エンドポイントはPOSTのみ |
| **No innerHTML** | Dashboard UI builds DOM elements programmatically — no XSS risk / DOM要素をプログラム的に構築、XSSリスクなし |

### Auto-switcher security / 自動切り替えのセキュリティ

| Measure | Details |
|---|---|
| **Atomic writes** | Token switch uses temp file + `renameSync` to prevent corruption / 一時ファイル + リネームのアトミック操作で破損を防止 |
| **Minimal API payload** | Sends `max_tokens: 1` with content `"."` — minimal cost and exposure / 最小限のペイロードでコストと露出を低減 |
| **Request limits** | Server configures `headersTimeout`, `requestTimeout`, `keepAliveTimeout`, and `maxRequestsPerSocket` / タイムアウトと最大リクエスト数を設定 |

---

## How It Works / 仕組み

### The Anthropic rate-limit headers / Anthropicのレートリミットヘッダー

Both tools work by sending a **minimal API request** to the Anthropic Messages API and reading the **response headers**. No actual conversation is generated — the request uses `max_tokens: 1` with a single-character message.

両ツールとも、Anthropic Messages APIに**最小限のリクエスト**を送信し、**レスポンスヘッダー**を読み取ります。実際の会話は生成されません — `max_tokens: 1` で1文字のメッセージを送信します。

**Request sent:**
```http
POST https://api.anthropic.com/v1/messages
Authorization: Bearer sk-ant-...
anthropic-version: 2023-06-01
anthropic-beta: claude-code-20250219,oauth-2025-04-20
Content-Type: application/json

{"model":"claude-sonnet-4-20250514","max_tokens":1,"messages":[{"role":"user","content":"."}]}
```

**Key response headers:**

| Header | Description |
|---|---|
| `anthropic-ratelimit-unified-5h-utilization` | 5-hour session utilization (0.0–1.0+) / 5時間セッション使用率 |
| `anthropic-ratelimit-unified-5h-reset` | Unix timestamp when 5h window resets / 5時間枠リセット時刻（Unixタイムスタンプ） |
| `anthropic-ratelimit-unified-7d-utilization` | 7-day weekly utilization (0.0–1.0+) / 7日間週間使用率 |
| `anthropic-ratelimit-unified-7d-reset` | Unix timestamp when 7d window resets / 7日間枠リセット時刻 |
| `anthropic-ratelimit-unified-7d_sonnet-utilization` | Sonnet-specific weekly utilization / Sonnet専用週間使用率 |
| `anthropic-ratelimit-unified-status` | `"allowed"` or `"rejected"` / 許可 or 拒否 |
| `anthropic-ratelimit-unified-overage-utilization` | Overage pool utilization / 超過プール使用率 |
| `anthropic-ratelimit-unified-fallback-percentage` | Fallback pool percentage / フォールバックプール割合 |

### Auto-switch logic / 自動切り替えロジック

```
1. Fetch usage for C1 and C2 in parallel
   C1とC2の使用率を並行取得

2. For each account: mark as "over" if 5h >= 80% OR 7d >= 80%
   5hまたは7dが80%以上なら「超過」とマーク

3. If current account is "over" AND alternate is NOT "over":
   → Switch token in auth-profiles.json (atomic write)
   現在のアカウントが超過 かつ 代替が未超過の場合
   → auth-profiles.jsonのトークンを切り替え（アトミック書き込み）

4. If BOTH accounts are "over":
   → Do NOT switch. Report bothOver: true for manual intervention.
   両方超過の場合 → 切り替えない。bothOver: trueを報告し手動対応を要求。
```

---

## License & Author / ライセンス・作者

**License:** MIT

**Author:** [@5dmgmt](https://x.com/5dmgmt) — 五次元経営株式会社 / 5th Dimension Management, Inc.

Website: [5dmgmt.com](https://5dmgmt.com)
