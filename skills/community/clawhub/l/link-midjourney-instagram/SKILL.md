---
name: link-midjourney-instagram
description: >-
  Runs the linkmidjourneyinstagram automation — generate four Midjourney images in Chromium via Playwright,
  then post each PNG as its own Instagram web post with per-image captions from captions.txt, the Midjourney prompt,
  or Gemini/OpenAI vision. Use when working in this repository, or when the user asks for Midjourney-to-Instagram
  automation, MJ→IG posting, or Playwright-based MJ/IG flows without official APIs.
metadata: {"openclaw":{"requires":{"bins":["python"]}}}
---

# Midjourney → Instagram（linkmidjourneyinstagram）

## 專案根目錄

自動化程式在 **repository root**（與 `skills/` 同層、含有 `main.py` 的那個資料夾）。  
透過 `exec` 執行指令時，**必須**先 `cd` 到該目錄；不要只在 `{baseDir}`（此 skill 資料夾）底下跑 `python main.py`。

## 何時用這份 skill

- 使用者要「從 Midjourney 產圖 → 自動發四則 IG 貼文」。
- 需要選擇 caption 來源：`captions.txt`、與 MJ 相同的 prompt、或 vision API。
- Troubleshooting：首次登入、Playwright、HEADLESS、POST_DELAY、Gemini 區域限制等。

## 前置條件

- Python 3.10+，`python` 在 PATH。
- Midjourney 有效訂閱（Google / Discord OAuth，由瀏覽器手動完成首次登入）。
- Instagram 帳號；`.env` 內需 `INSTAGRAM_USERNAME`、`INSTAGRAM_PASSWORD`（見 `.env.example`）。
- 依賴：`pip install -r requirements.txt`，並執行 `python -m playwright install chromium`。

## 安裝與設定（一次性）

於 **repository root**：

```bash
python -m venv .venv
```

啟用 venv 後（Windows：`.venv/Scripts/activate`；macOS/Linux：`source .venv/bin/activate`）：

```bash
pip install -r requirements.txt
python -m playwright install chromium
cp .env.example .env
```

編輯 `.env` 填入 IG 帳密；其餘選項見 `.env.example` 註解。

## 首次執行（務必可視瀏覽器）

- 維持 `HEADLESS=false`（預設），讓 Chromium 視窗開著。
- Midjourney：完成 Google/Discord 登入與驗證；session 會存到 `browser_data/midjourney/`。
- Instagram：完成網頁登入與可能的 2FA；session 會存到 `browser_data/instagram/`。
- 之後可視需求改 `HEADLESS=true`。

## 執行 pipeline（給 agent 用 `exec`）

預設讀取 `prompt.txt` 與 `captions.txt`：

```bash
python main.py
```

常用選項：

```bash
python main.py --prompt "your midjourney prompt here"
python main.py --skip-instagram
python main.py --headless
python main.py --post-delay 60
python main.py --use-prompt-caption
python main.py --use-vision-caption
```

行為摘要：

| 模式 | 條件 |
|------|------|
| Vision caption | `--use-vision-caption` 或 `.env` 中 `INSTAGRAM_USE_VISION_CAPTION`；若設了 `GEMINI_API_KEY`/`GOOGLE_API_KEY` 且未明確關閉，預設會開 vision |
| Prompt 當 caption | `--use-prompt-caption` 或 `INSTAGRAM_USE_PROMPT_CAPTION=true`（vision 開啟時會被蓋過） |
| `captions.txt` | 上述皆否時，依 `---` 分區塊，每張圖一則；區塊不足則用最後一則重複 |

Vision：`GEMINI_API_KEY` / `GOOGLE_API_KEY`，或 `VISION_CAPTION_PROVIDER=openai` 搭配 `OPENAI_API_KEY`。詳見 `.env.example`。

## 編輯輸入檔

**`prompt.txt`**：以 `# `（井號+空白）或單獨 `#` 開頭的行為註解並忽略；`#midjourney` 這類標籤保留。非註解行會用空白串成一句送進 Midjourney。

**`captions.txt`**：四個（或多個）區塊，區塊之間一行 `---`。註解規則同 `prompt.txt`。

## 輸出與安全

- 圖片：`outputs/mj_<timestamp>/image_1.png` … `image_4.png`。
- **勿** commit `.env`、`browser_data/`（含 session cookie）；已應在 `.gitignore`。
- 自動發文可能觸發平台風控；善用 `--post-delay`（預設對應 `POST_DELAY_S`），勿過度密集發送。

## OpenClaw 載入後

必要時請使用者 `/new` 或重啟 gateway；可用 `openclaw skills list` 確認 skill 名稱 `link-midjourney-instagram` 已載入。
