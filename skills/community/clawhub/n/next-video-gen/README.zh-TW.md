# Next Video Gen 下一代影片生成

<p align="center">
  <strong>AI 圖片/影片生成 via 火山引擎方舟平台 — 文生圖、文生影片、圖生影片、素材生影片，由 Seedance 2.0 驅動。</strong>
</p>

<p align="center">
  <a href="#功能介紹">功能</a> •
  <a href="#安裝">安裝</a> •
  <a href="#取得-api-key">API Key</a>
</p>

<p align="center">
  <strong>語言：</strong>
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a>
</p>

---

## 功能介紹

適用於 AI 編程助手（Claude Code、Cursor 等）的圖片/影片生成技能，基於火山引擎方舟平台的 Seedance 2.0 模型。

| 技能 | 描述 | 模型 |
|------|------|------|
| **Next Video Gen** | 文生圖、文生影片、圖生影片、素材生影片 | Seedance 2.0 |

---

## 安裝

### 快速安裝

```bash
openclaw skills add https://github.com/vennduan/next-video-gen
```

### 手動安裝

```bash
git clone https://github.com/vennduan/next-video-gen.git
cd next-video-gen
openclaw skills add .
```

---

## 取得 API Key

1. 在 [console.volcengine.com/ark](https://console.volcengine.com/ark) 註冊
2. 進入 API Keys 建立新金鑰
3. 設定環境變數：

```bash
export DOUBAO_API_KEY=your_key_here
```

---

## 能力詳情

- **文生圖** — 文字描述生成高品質圖片（PNG/JPEG/WebP）
- **文生影片** — 文字描述生成無聲影片
- **文生影片（音畫）** — 描述場景+聲音，生成同步音視訊（預設）
- **圖生影片** — 圖片 + 文字描述，生成無聲影片
- **圖生影片（音畫）** — 圖片 + 描述，生成帶聲音的影片（提供圖片時預設）
- **素材生影片** — 影片 + 文字描述，基於已有影片素材生成新影片
- **多解析度** — 圖片：2K / 1K / HD；影片：480p / 720p / 1080p
- **彈性時長** — 影片 4–12 秒
- **多寬高比** — 圖片：1:1 / 16:9 / 9:16；影片：16:9 / 9:16 / 1:1

### 使用範例

直接和代理對話：

> 「生成一張未來城市日落的圖片」

> 「生成一個 5 秒的貓彈鋼琴影片」

> 「創建電影級海上日落畫面，720p，16:9」

> 「用這張圖生成 8 秒的動畫影片」

> 「把這個影片處理成更鮮艷的色彩，加快節奏」

> 「生成一個有歡快背景音樂和鳥叫聲的影片」

代理會引導你補充缺失資訊並處理生成。

### 系統需求

- 系統已安裝 `curl` 和 `jq`
- 已設定 `DOUBAO_API_KEY` 環境變數

### 腳本參考

技能包含 `scripts/seedance-gen.sh` 供命令列直接使用：

```bash
# 文生圖
./scripts/seedance-gen.sh "未來城市日落，霓虹燈閃爍" --mode txt2img

# 文生大圖
./scripts/seedance-gen.sh "抽象艺术，鲜艳色彩" --mode txt2img --quality 2K

# 文生音畫（預設，帶聲音）
./scripts/seedance-gen.sh "一隻貓在草地上奔跑，陽光明媚，有鳥叫" --mode txt2video --duration 5

# 文生影片（無音訊）
./scripts/seedance-gen.sh "海上日落縮時攝影" --mode txt2video --no-audio

# 圖生音畫（預設，帶聲音）
./scripts/seedance-gen.sh "鏡頭緩慢推進，貓咪轉身看向鏡頭" --mode img2video --image "https://example.com/cat.jpg"

# 圖生影片（無音訊）
./scripts/seedance-gen.sh "圖片動起來" --mode img2video --image "https://example.com/img.jpg" --no-audio

# 素材生影片
./scripts/seedance-gen.sh "色彩更鮮艷，加快節奏" --mode vid2video --video "https://example.com/input.mp4"

# 指定解析度和時長
./scripts/seedance-gen.sh "無人機航拍山谷" --mode txt2video --duration 8 --quality 1080p

# 豎版影片
./scripts/seedance-gen.sh "瀑布流淌" --mode txt2video --aspect-ratio 9:16

# 關閉浮水印
./scripts/seedance-gen.sh "抽象藝術動畫" --mode txt2video --watermark false
```

內容儲存至 `~/Videos/next-video-gen/`（可透過 `NEXT_VIDEO_GEN_OUTPUT_DIR` 設定）。

### API 參數

完整 API 文件見 [references/api-params.md](references/api-params.md)。

---

## 檔案結構

```
.
├── README.md                    # English
├── README.zh-CN.md              # 簡體中文
├── README.zh-TW.md              # 本文件（繁體中文）
├── SKILL.md                     # 技能定義
├── _meta.json                   # 技能元數據
├── references/
│   └── api-params.md            # 完整 API 參數文件
└── scripts/
    └── seedance-gen.sh          # 生成腳本
```

---

## 常見問題

| 問題 | 解決方案 |
|------|---------|
| `jq: command not found` | 安裝 jq：`apt install jq` / `brew install jq` |
| `401 Unauthorized` | 檢查 `DOUBAO_API_KEY`，前往 [console.volcengine.com/ark](https://console.volcengine.com/ark) 確認 |
| `403 Forbidden` | 在火山引擎主控台檢查 API 金鑰權限 |
| `429 Too Many Requests` | 請求頻率過高，稍等後重試 |
| 內容被攔截 | 修改提示詞後重試 |
| 生成逾時 | 影片通常需 1–3 分鐘，圖片通常 5–15 秒 |

---

## 授權條款

MIT
