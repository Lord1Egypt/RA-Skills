English | [中文](README.zh-TW.md)

# NotebookLM Studio Skill

Google NotebookLM 的 AI agent skill — 匯入來源（URL、YouTube、檔案、文字），自動生成 podcast、影片、報告、測驗、單字卡、心智圖、簡報、資訊圖表和數據表。

支援 **Claude Code**、**OpenClaw**、**Codex**，以及任何支援 [Agent Skills](https://agentskills.io) 規範的 agent。

![Full Flow Demo](assets/demo-full-flow.png)

## 功能

- **9 種產物類型**：audio、video、report、quiz、flashcards、mind-map、slide-deck、infographic、data-table
- **所有來源類型**：URL、YouTube、文字筆記、PDF、Word、音訊、圖片、Google Drive
- **多語言輸出**：支援 30+ 語言（預設：繁體中文）
- **跨平台**：任何讀取 SKILL.md 的 AI agent 都能使用
- **Telegram 送達**：兩輪交付，即時狀態追蹤（透過 OpenClaw）
- **音訊壓縮**：ffmpeg 後處理，符合 Telegram 50MB 檔案大小限制
- **CLI 驅動**：直接使用 `notebooklm` CLI，無需自訂 Python 封裝

## 使用方式

直接跟 AI agent 說你要什麼，不需要了解 CLI 操作。

**從 URL 產生學習教材包：**
> 用這篇文章產生 report、quiz 和 flashcards
> https://example.com/deep-learning-intro

**把 YouTube 影片轉成 podcast 和簡報：**
> 用辯論格式幫我把這個影片做成 podcast 和簡報
> https://youtube.com/watch?v=dQw4w9WgXcQ

**從 PDF 製作資訊圖表：**
> 用手繪風格幫我把這篇論文做成 infographic
> *(附上 file.pdf)*

**完整學習包 via Telegram（OpenClaw）：**
> 幫我用這篇文章做一份完整的學習包，包含 report、quiz、flashcards、podcast 和簡報
> https://example.com/article

Agent 會自動處理所有步驟：建立筆記本、加入來源、產生產物、下載結果並送達給你。

## 運作原理

```
你 ──────── "幫我用這個 URL 產生 report 和簡報"
                │
                ▼
        AI Agent（Claude Code / OpenClaw / Codex）
                │  讀取 SKILL.md → 10 步驟 workflow
                ▼
        notebooklm CLI
                │  建立筆記本 → 加入來源 → 產生 → 下載
                ▼
        ./output/<topic>/
            ├── report.md
            ├── slides.pdf
            ├── podcast.mp3
            └── ...
                │
                ▼（選用，OpenClaw）
        Telegram ── 每完成一個產物即送達
```

## 產物類型

| 類型 | CLI 指令 | 預估時間 | 輸出格式 |
|------|----------|----------|----------|
| 音訊（Podcast） | `generate audio` | 5-30 分鐘 | MP3 |
| 影片 | `generate video` | 5-30 分鐘 | MP4 |
| 報告 | `generate report` | 1-2 分鐘 | Markdown |
| 測驗 | `generate quiz` | 1-2 分鐘 | JSON/MD/HTML |
| 單字卡 | `generate flashcards` | 1-2 分鐘 | JSON/MD/HTML |
| 心智圖 | `generate mind-map` | 即時 | JSON |
| 簡報 | `generate slide-deck` | 2-10 分鐘 | PDF/PPTX |
| 資訊圖表 | `generate infographic` | 2-5 分鐘 | PNG |
| 數據表 | `generate data-table` | 1-2 分鐘 | CSV |

完整 CLI 選項請參閱 `references/artifacts.md`。

## 安裝

### 前置需求

- **Python 3.10+**
- **ffmpeg**（音訊壓縮用）
- **OS**：macOS、Linux（Ubuntu 20.04+）或 Windows

### 1. 安裝 skill

**方式 A — ClawHub（推薦）：**
```bash
npm i -g clawhub        # 安裝 ClawHub CLI（僅需一次）
clawhub install notebooklm-studio
```

**方式 B — Git clone：**
```bash
git clone --recurse-submodules https://github.com/jasontsaicc/notebooklm-studio-skill.git
cd notebooklm-studio-skill
```

### 2. 安裝 notebooklm CLI

> **不論選擇方式 A 或 B，以下步驟 2–5 都必須完成。**

Skill 需要 `notebooklm` CLI 工具，這是獨立的依賴項。

```bash
pip install "notebooklm-py[browser]"
playwright install chromium
```

**Ubuntu/Debian** — 另需安裝 Chromium 系統依賴：
```bash
playwright install-deps chromium
```

### 3. 安裝 ffmpeg

**macOS：**
```bash
brew install ffmpeg
```

**Ubuntu/Debian：**
```bash
sudo apt update && sudo apt install -y ffmpeg
```

### 4. 認證

**有瀏覽器的機器（Mac/Windows/Linux 桌面）：**
```bash
notebooklm login
```

**無頭伺服器（如 Ubuntu VPS）：**

先在本地機器登入，再將憑證傳到伺服器：
```bash
# 本地機器 — 登入並驗證
notebooklm login
notebooklm auth check

# 傳送到伺服器
ssh user@server "mkdir -p ~/.notebooklm"
scp ~/.notebooklm/storage_state.json user@server:~/.notebooklm/storage_state.json
ssh user@server "chmod 600 ~/.notebooklm/storage_state.json"
```

### 5. 驗證

```bash
notebooklm auth check --test
```

預期結果：所有檢查通過，token fetch 成功。

### 6. 安裝為 agent skill（僅方式 B）

如果使用 ClawHub 安裝，請跳過此步驟。Git clone 使用者：

**Claude Code：**
```bash
ln -s "$(pwd)" ~/.claude/skills/notebooklm-studio
```

**OpenClaw：**
```bash
ln -s "$(pwd)" /path/to/openclaw/skills/notebooklm-studio
```

**其他 agent：** 將此目錄放置或建立 symlink 到 agent 的 skill 目錄。

## 快速測試（CLI）

安裝完成後，不透過 AI agent 直接測試：

```bash
# 建立筆記本
notebooklm create "Test Notebook $(date +%Y%m%d)"
notebooklm use <notebook_id>    # 使用上方輸出的 ID

# 加入來源
notebooklm source add "https://en.wikipedia.org/wiki/Feynman_technique"

# 產生報告（最快的產物，約 1 分鐘）
notebooklm generate report --format study-guide --wait

# 下載
mkdir -p output/feynman-technique
notebooklm download report ./output/feynman-technique/report.md

# 查看結果
cat ./output/feynman-technique/report.md
```

如果成功，安裝就完成了。AI agent 會透過 SKILL.md 自動執行相同的流程。

## 專案結構

```
notebooklm-studio-skill/
├── SKILL.md                         # Agent skill 定義（10 步驟 workflow）
├── README.md
├── LICENSE
├── notebooklm-py/                   # git submodule（notebooklm CLI）
├── references/
│   ├── artifacts.md                 # 9 種產物類型 + CLI 選項
│   ├── artifact-options.md          # ASK/OFFER/SILENT 選項優先級
│   ├── source-types.md              # 來源類型與偵測規則
│   ├── output-contracts.md          # 輸出格式規格
│   └── telegram-delivery.md         # Telegram 交付合約
├── scripts/
│   ├── compress_audio.sh            # ffmpeg 音訊壓縮
│   └── recover_tier2_delivery.sh    # Tier 2 產物 cron 恢復腳本
└── assets/                          # 截圖與展示媒體
```

## OpenClaw 超時與恢復設定

Tier 2 產物（podcast、影片、簡報）需要 5–40 分鐘產生。如果 agent 在完成前超時，產物會在 NotebookLM 伺服器上生成完成，但不會被下載或送達。本節設定自動恢復機制。

### 1. Agent 超時設定

在 OpenClaw 設定中為 notebooklm agent 設定 `timeoutSeconds: 1800`（30 分鐘）：

```json
{
  "agents": {
    "list": [
      {
        "id": "notebooklm",
        "timeoutSeconds": 1800
      }
    ]
  }
}
```

這涵蓋大部分 Tier 2 產物。如果使用 cinematic 影片（Veo 3，約 40 分鐘），建議設為 `2400`。

### 2. Tier 2 恢復排程（每 5 分鐘）

如果 agent 在交付中途超時，`delivery-status.json` 會追蹤待處理的項目。恢復腳本會自動輪詢、下載並更新狀態。

```bash
# crontab -e
*/5 * * * * cd /path/to/notebooklm-studio-skill && bash scripts/recover_tier2_delivery.sh ./output >> /var/log/notebooklm-recovery.log 2>&1
```

腳本功能：
- 掃描 `output/*/delivery-status.json` 中 `"status": "pending"` 的產物
- 透過 `notebooklm artifact poll <task_id>` 輪詢每個產物
- `completed` → 下載、壓縮音訊、更新狀態
- `failed` → 標記為失敗
- `processing` → 跳過（下次執行時重試）

### 3. 健康檢查排程（每 30 分鐘）

在恢復被阻擋前捕捉過期的 session：

```bash
# crontab -e
*/30 * * * * notebooklm auth check --test --json | python3 -c "import json,sys; d=json.load(sys.stdin); exit(0 if d['status']=='ok' else 1)" || echo "$(date): AUTH EXPIRED — run notebooklm login" >> /var/log/notebooklm-health.log
```

### 疑難排解

**「Tier 2 產物已生成但未送達」**

當 agent 在 `artifact wait` 期間超時就會發生。檢查並恢復：

```bash
# 查看待處理項目
python3 -c "
import json, glob
for f in glob.glob('output/*/delivery-status.json'):
    data = json.load(open(f))
    pending = [a for a in data['artifacts'] if a['status'] == 'pending']
    if pending:
        print(f'{f}: {len(pending)} pending')
        for a in pending:
            print(f'  {a[\"type\"]} — task_id: {a[\"task_id\"]}')
"

# 手動恢復
bash scripts/recover_tier2_delivery.sh ./output
```

**「Auth check failed」出現在恢復日誌中**

Session 過期。重新登入後，恢復會在下次排程時自動繼續：

```bash
notebooklm login
notebooklm auth check --test   # 驗證
```

**「恢復執行了但產物仍然 pending」**

產物可能仍在生成中。手動檢查：

```bash
notebooklm artifact poll <task_id> --json
```

如果是 `processing` → 等待。如果卡超過 60 分鐘 → 直接到 [NotebookLM 網頁版](https://notebooklm.google.com) 確認。

## 更新 notebooklm-py

```bash
pip install --upgrade "notebooklm-py[browser]"
```

## 技術支持

- [notebooklm-py](https://github.com/teng-lin/notebooklm-py) — Google NotebookLM 非官方 Python API 與 CLI

## 授權

MIT
