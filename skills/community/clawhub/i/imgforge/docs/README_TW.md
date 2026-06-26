# zimage — 免費 AI 圖片生成技能

<p align="center">
  <img src="../icon.png" alt="Z-Image Skill" width="128" height="128">
</p>

<p align="center">
  <strong>在 AI 編程助手裡，用一句話免費生成精美圖片。</strong><br>
  支援 Claude Code · OpenClaw · Codex · Antigravity · Paperclip
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

## 簡介

**zimage** 讓你的 AI 助手能夠根據文字描述生成圖片。背後使用阿里巴巴通義 MAI 團隊開發的開源模型 [Z-Image-Turbo](https://github.com/Tongyi-MAI/Z-Image)（60 億參數），透過 ModelScope 的免費 API 呼叫。

```
你：   幫我生成一隻狐狸在圖書館看書的圖片
AI：   正在提交：一隻狐狸在圖書館看書
       任務 91204 — 等待結果中…
       已儲存 → fox_library.jpg
```

### 比較

|  | zimage | DALL-E 3 | Midjourney |
|--|--------|----------|------------|
| 費用 | **免費** | $0.04–0.08 / 張 | $10+/月起 |
| 開源 | Apache 2.0 | 否 | 否 |
| 設定時間 | 約 5 分鐘 | 需綁定付款 | 需要 Discord |

> **免費額度：** 每日共 2,000 次 API 呼叫，單一模型上限 500 次/天。額度可能動態調整。（[官方限額說明](https://modelscope.ai/docs/model-service/API-Inference/limits)）

---

## 設定

### 第一步 — 阿里雲帳號（免費）

到這裡註冊：**https://www.alibabacloud.com/campaign/benefits?referral_code=A9242N**

註冊時需要驗證手機號碼並綁定付款方式。**Z-Image 本身免費，不會向你收費**，但阿里雲帳號要求綁定付款資訊才能使用。

### 第二步 — ModelScope 帳號 + 綁定

1. 到 **https://modelscope.ai/register?inviteCode=futurizerush&invitorName=futurizerush&login=true&logintype=register** 註冊（支援 GitHub 登入）
2. 進入 **設定 → Bind Alibaba Cloud Account**，綁定第一步建立的阿里雲帳號

> ⚠️ 請使用 **modelscope.ai**（國際站），不是 modelscope.cn（中國站）。

### 第三步 — 取得 API Token

1. 前往 **https://modelscope.ai/my/access/token**
2. 點擊 **Create Your Token**
3. 複製 Token（格式：`ms-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）

---

## 安裝

<details>
<summary><b>Claude Code</b></summary>

在 Claude Code 裡說：

```
幫我安裝 zimage skill，來源是 https://github.com/FuturizeRush/zimage-skill
```

然後：

```
幫我設定環境變數 MODELSCOPE_API_KEY，值是 ms-你的token
```

重新啟動 Claude Code 即可。
</details>

<details>
<summary><b>OpenClaw / ClawHub</b></summary>

```bash
openclaw skills install zimage
# 或
npx clawhub@latest install zimage
```

```bash
export MODELSCOPE_API_KEY="ms-你的token"
```
</details>

<details>
<summary><b>Codex / Antigravity / Paperclip / 其他</b></summary>

```bash
git clone https://github.com/FuturizeRush/zimage-skill.git
cd zimage-skill
pip install Pillow  # 選用，用於格式轉換
export MODELSCOPE_API_KEY="ms-你的token"
```

```bash
python3 imgforge.py "海邊的日落" sunset.jpg
```
</details>

---

## 使用方式

### 透過 AI 助手

直接用自然語言描述：

```
生成一張溫馨咖啡廳的圖片，溫暖燈光，電影感
畫一隻噴火的像素風格龍
做一個極簡風格的 logo，藍色漸層
```

### 直接 CLI

```bash
# 基本用法
python3 imgforge.py "太空人在火星上"

# 自訂尺寸（橫幅）
python3 imgforge.py "黃金時刻的山景全景" -o panorama.jpg -W 2048 -H 1024

# JSON 輸出
python3 imgforge.py "抽象藝術" --json
```

### CLI 參數

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `prompt` | *（必填）* | 圖片描述 |
| `-o` / `--out` | `output.jpg` | 輸出路徑 |
| `-W` / `--width` | `1024` | 寬度，512–2048 px |
| `-H` / `--height` | `1024` | 高度，512–2048 px |
| `--json` | 關閉 | JSON 格式輸出 |

---

## 常見問題

| 問題 | 解決方式 |
|------|---------|
| `MODELSCOPE_API_KEY is not set` | 請完成上方[設定](#設定)步驟 |
| `401 Unauthorized` | 確認用的是 **modelscope.ai**（不是 .cn）。確認已綁定阿里雲。重新產生 Token。 |
| 逾時 | API 負載較高，請稍後再試 |
| 內容審核錯誤 | 修改描述內容後重試 |

---

## 技術資訊

- **零必要依賴** — 使用 Python 標準庫 `urllib.request`。Pillow 為選用（僅用於格式轉換）。
- 支援 512×512 到 2048×2048 自訂尺寸。
- `--json` 可與其他工具串接。
- 模型：[Tongyi-MAI/Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo)（Apache 2.0）
- API：ModelScope 國際站（`api-inference.modelscope.ai`）

---

## 授權

MIT-0 — 自由使用，無需署名。
