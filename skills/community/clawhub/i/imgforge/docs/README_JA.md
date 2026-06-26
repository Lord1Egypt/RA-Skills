# zimage — 無料AI画像生成スキル

<p align="center">
  <img src="../icon.png" alt="Z-Image Skill" width="128" height="128">
</p>

<p align="center">
  <strong>AIコーディングアシスタントから、テキストで無料で画像を生成。</strong><br>
  Claude Code · OpenClaw · Codex · Antigravity · Paperclip 対応
</p>

<p align="center">
  <a href="../README.md">English</a> ·
  <a href="./README_TW.md">繁體中文</a> ·
  <a href="./README_JA.md">日本語</a> ·
  <a href="./README_KO.md">한국어</a> ·
  <a href="./README_ES.md">Español</a> ·
  <a href="./README_DE.md">Deutsch</a> ·
  <a href="./README_FR.md">Français</a> ·
  <a href="./README_IT.md">Italiano</a>
</p>

---

## 概要

**zimage** は、AIアシスタントにテキストから画像を生成する機能を追加するスキルです。Alibaba Tongyi-MAIチームが開発したオープンソースモデル [Z-Image-Turbo](https://github.com/Tongyi-MAI/Z-Image)（60億パラメータ）を、ModelScopeの無料APIを通じて利用します。

```
あなた：  図書館で本を読んでいるキツネの画像を作って
AI：     送信中: 図書館で本を読んでいるキツネ
         タスク 91204 — 結果を待っています…
         保存完了 → fox_library.jpg
```

### 比較

|  | zimage | DALL-E 3 | Midjourney |
|--|--------|----------|------------|
| 料金 | **無料** | $0.04–0.08 / 枚 | $10+/月〜 |
| オープンソース | Apache 2.0 | いいえ | いいえ |
| セットアップ時間 | 約5分 | 課金設定が必要 | Discordが必要 |

> **無料枠：** 1日合計2,000回、モデルごとに500回/日。制限は動的に調整される場合があります。（[公式制限](https://modelscope.ai/docs/model-service/API-Inference/limits)）

---

## セットアップ

### ステップ1 — Alibaba Cloudアカウント（無料）

こちらから登録：**https://www.alibabacloud.com/campaign/benefits?referral_code=A9242N**

登録時に電話番号の認証と支払い方法の登録が必要です。**Z-Image自体は無料で課金されません**が、Alibaba Cloudはアカウントに支払い情報の登録を求めます。

### ステップ2 — ModelScopeアカウント + 連携

1. **https://modelscope.ai/register?inviteCode=futurizerush&invitorName=futurizerush&login=true&logintype=register** でアカウント登録（GitHubログイン対応）
2. **設定 → Bind Alibaba Cloud Account** からステップ1のアカウントを連携

### ステップ3 — APIトークン取得

1. **https://modelscope.ai/my/access/token** にアクセス
2. **Create Your Token** をクリック
3. トークンをコピー（形式：`ms-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）

---

## インストール

<details>
<summary><b>Claude Code</b></summary>

Claude Codeで次のように伝えてください：

```
Install the zimage skill from https://github.com/FuturizeRush/zimage-skill
```

続いて：

```
Set my MODELSCOPE_API_KEY environment variable to ms-あなたのトークン
```

Claude Codeを再起動してください。
</details>

<details>
<summary><b>OpenClaw / ClawHub</b></summary>

```bash
openclaw skills install zimage
# または
npx clawhub@latest install zimage
```

```bash
export MODELSCOPE_API_KEY="ms-あなたのトークン"
```
</details>

<details>
<summary><b>Codex / Antigravity / Paperclip / その他</b></summary>

```bash
git clone https://github.com/FuturizeRush/zimage-skill.git
cd zimage-skill
pip install Pillow  # オプション（フォーマット変換用）
export MODELSCOPE_API_KEY="ms-あなたのトークン"
```

```bash
python3 imgforge.py "海に沈む夕日" sunset.jpg
```
</details>

---

## 使い方

### AIアシスタント経由

自然言語で指示するだけ：

```
おしゃれなカフェの画像を作って、暖かい照明、映画のような雰囲気
炎を吐くドット絵のドラゴンを描いて
ミニマルなロゴを作って、青のグラデーション
```

### CLI直接実行

```bash
# 基本
python3 imgforge.py "火星の宇宙飛行士"

# カスタムサイズ（横長）
python3 imgforge.py "ゴールデンアワーの山のパノラマ" -o panorama.jpg -W 2048 -H 1024

# JSON出力
python3 imgforge.py "抽象アート" --json
```

### CLIフラグ

| フラグ | デフォルト | 説明 |
|--------|-----------|------|
| `prompt` | *（必須）* | 生成する画像の説明 |
| `-o` / `--out` | `output.jpg` | 出力パス |
| `-W` / `--width` | `1024` | 幅、512–2048 px |
| `-H` / `--height` | `1024` | 高さ、512–2048 px |
| `--json` | オフ | JSON形式で出力 |

---

## トラブルシューティング

| 問題 | 解決方法 |
|------|---------|
| `MODELSCOPE_API_KEY is not set` | 上記の[セットアップ](#セットアップ)を完了してください |
| `401 Unauthorized` | **modelscope.ai**（.cnではなく）を使用。Alibaba Cloud連携を確認。トークンを再生成。 |
| タイムアウト | API負荷が高い — 1分後に再試行 |
| コンテンツモデレーション | プロンプトを変更してください |

---

## 技術情報

- **外部依存なし** — Python標準ライブラリの `urllib.request` を使用。Pillowはオプション。
- 512×512 から 2048×2048 までのカスタムサイズに対応。
- モデル：[Tongyi-MAI/Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo)（Apache 2.0）
- API：ModelScope International（`api-inference.modelscope.ai`）

---

## ライセンス

MIT-0 — 自由に使えます。帰属表示不要。
