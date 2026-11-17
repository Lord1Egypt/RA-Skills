# LINE 貼圖生成大師（line-sticker-master）

**LINE 貼圖生成大師**是一套供 Manus 使用的 LINE 貼圖製作 Skill。它將貼圖工作拆成角色設定、12 格套組腳本、4×3 網格圖提示詞、台灣繁體中文檢查、職場梗風險審核、切圖去背、預覽與 ZIP 匯出，適合搭配 [`line-sticker-factory`](https://github.com/qpooqp777/line-sticker-factory) 使用。

> 本 Skill 負責規劃、提示詞與品質檢查；`line-sticker-factory` 負責網格圖切割、去背、預覽與下載。它不假設任何特定圖像生成 API 已經啟用。

## 功能

| 功能 | 說明 |
| --- | --- |
| 角色一致性規劃 | 建立角色 bible，固定外觀、服裝、配件、色彩與禁止變更項目 |
| 12 格貼圖腳本 | 產生編號、文字、情緒、動作、特效與構圖留白 |
| 4×3 網格提示詞 | 產生可交給圖像生成模型的單一網格圖提示詞 |
| 台灣繁體中文審核 | 檢查繁簡混用、台灣慣用詞、語氣詞、標點、字數與文字可讀性 |
| 職場梗審核 | 區分同事、主管、客戶語境，檢查諷刺、自嘲、歧視、霸凌與洩密風險 |
| 專案整合 | 搭配 `line-sticker-factory` 執行切圖、色鍵去背、AI 去背、預覽與 ZIP 匯出 |

## 安裝到 Manus

### 方法一：使用 Skill 檔案安裝

下載本儲存庫中的 `SKILL.md` 與 `references/` 目錄，並將整個 Skill 目錄安裝至 Manus Skills 位置。核心檔案必須命名為 `SKILL.md`，且與 `references/` 位於同一個 Skill 目錄中。

```text
line-sticker-master/
├── SKILL.md
└── references/
    ├── line-sticker-factory.md
    └── zh-tw-copy-check.md
```

在支援 Skill 卡片的 Manus 介面中，也可以直接開啟 `SKILL.md` 附件，選擇 **Add to My Skills**。安裝後重新開始對話或重新載入 Skill 清單，讓系統讀取新的 Skill metadata。

### 方法二：從 GitHub 取得

```bash
git clone https://github.com/qpooqp777/line-sticker-master.git
cd line-sticker-master
```

接著將 `SKILL.md` 與 `references/` 放入你的 Manus Skills 目錄。若使用的是其他代理平台，請依該平台的 Skill/Agent instructions 安裝方式處理；本套件的入口檔固定為 `SKILL.md`。

## 使用方式

安裝後可以直接使用自然語言，例如：

```text
幫我用這個角色做一套 12 張台灣繁體中文日常 LINE 貼圖。
```

```text
規劃一套上班族職場梗貼圖，請避開冒犯主管、客戶、身心疾病與特定身分的表述。
```

```text
把「收到、辛苦了、我先下班、會議中、馬上改、薪水呢」整理成 12 格貼圖腳本，並檢查台灣用字與使用情境。
```

```text
我有一張 4×3 網格圖，請依照 LINE 貼圖生成大師流程檢查文字、切圖、去背與檔名。
```

建議的互動順序是先讓 Skill 產生角色 bible 與 12 格腳本，確認文字後再生成網格圖，最後將網格圖交給切圖工具處理。若只需要修改單格，應只重做該格並維持角色、畫風、背景色與排版規則不變。

## 繁體中文與職場梗檢查

製作日常或職場主題時，Skill 會按需讀取 [`references/zh-tw-copy-check.md`](references/zh-tw-copy-check.md)，並可進一步載入完整的 [`references/workplace-meme-catalog.md`](references/workplace-meme-catalog.md) 對照表。該文件包含台灣常用詞方向，例如「訊息、檔案、軟體、網路、影片、外送」，以及「收到、辛苦了、我處理、再確認一下、同步一下、先對一下、卡住了、準時下班」等日常與職場語料方向。另提供「又開會、需求又變了、先撐住、我先走、WFH 中、網路卡住、拉個會、腦袋當機、社畜模式、工具人上線」等台灣職場趣味用語的情境分類；每個梗都需依使用對象與公開程度檢查，並在必要時提供「我先確認需求範圍」「今天先到這」等安全替代句。完整對照表依類別、語氣、適用對象與 A–D 風險等級整理，新增語料時請沿用該文件的擴充格式。

職場文字會先依對象分級：同事間安全日常、熟同事的輕度自嘲、公開社群的敏感諷刺，以及涉及霸凌、歧視、威脅或洩密的高風險內容。對高風險文字，Skill 會改寫成不指涉特定個人或公司的安全版本，並保留原句、問題、建議句與適用情境，方便逐格審核。

工程師與遠端工作主題可進一步參考規則檔中的專屬對照表，涵蓋「在我電腦可以」「PR 等你看」「測試在哭」「部署翻車」「金鑰不要貼群組」「你靜音了」「畫面卡住了」等語句，並檢查是否誤用技術術語、洩漏金鑰或鼓勵跳過測試、審查與安全程序。

## 一鍵複製 Prompt 模板

完整的 Markdown Prompt 模板位於 [`templates/line-sticker-prompt-template.md`](templates/line-sticker-prompt-template.md)。請先上傳角色參考圖片，再複製模板中的單一 `text` code block，將 `[方括號]` 欄位替換為角色名稱、主題、12 句文案、動作、情緒、視角與手繪特效，即可貼入圖像生成模型。

模板固定包含角色一致性、臉部寫實與服裝手繪、二頭身比例、4×3 網格、1480×960 px、純綠色 `#00FF00`、粗白外框、台灣繁體中文、禁止 Emoji 與負面提示詞。若模型文字生成不穩定，模板也提供「保留文字留白、後製加字」的替代版本。

## 前十名文案與排版指南

[`references/top-10-sticker-copy-guide.md`](references/top-10-sticker-copy-guide.md) 以現有職場語料建立前 10 名優先製作建議，並為每張貼圖提供文字、情境、角色動作、文字位置、字數與安全替代句。排名是依跨情境性、回覆頻率、台灣職場辨識度、公開安全性與可讀性做的內容策展評分，不是實際下載量或市場調查；若有真實投票或使用數據，應另行更新排名依據。

使用指南時，先選擇適用對象與風險等級，再決定採用原始梗或安全替代句。所有文字生成結果都要逐格檢查，若圖像模型產生錯字，改用留白圖並後製加入文字。

## 搭配 line-sticker-factory

本 Skill 可搭配 [`qpooqp777/line-sticker-factory`](https://github.com/qpooqp777/line-sticker-factory) 使用。該專案可將 4 欄 × 3 列網格圖切成 12 張圖片，並提供瀏覽器端色鍵去背、可選的 Python `rembg` 後端、預覽及 ZIP 下載。

```bash
git clone https://github.com/qpooqp777/line-sticker-factory.git
cd line-sticker-factory
npm install
npm run dev
```

取得本機開發網址後，上傳 Skill 產生的 4×3 網格圖，選擇綠色、黑色或白色背景去背設定，再檢查 12 張輸出的文字、透明邊緣與安全邊界。若角色含毛髮、半透明物件或背景色與前景相近，應優先考慮 AI 去背或 `rembg` 後端。

## 小沙彌向善用語專區

本 Skill 另提供一個可直接瀏覽的向善語料網站：[小沙彌向善用語專區](https://qpooqp777.github.io/little-monk-kind-words-site/)。網站目前收錄 **12 個類別、144 筆語料**，每筆包含類別、貼圖文案、適合情境、小沙彌動作、表情、視角與手繪特效。

網站支援關鍵字搜尋、類別篩選、今日一句、單句完整 Prompt 複製，以及選定類別後的一鍵複製 12 格 Prompt。要製作單張貼圖時，使用「收下這句」；要製作完整套組時，先選擇單一類別，再使用「收下該類 12 格」。複製內容已依 12 格順序與真正換行整理，可直接貼入圖像生成模型。

網站原始碼與 GitHub Pages 工作流位於 [`qpooqp777/little-monk-kind-words-site`](https://github.com/qpooqp777/little-monk-kind-words-site)。網站是語料選擇層，不會取代本 Skill 的角色 bible、4×3 網格規格、繁體中文審核、去背檢查或 `line-sticker-factory` 處理流程。完整整合欄位與維護方式請參考 [`references/little-monk-kind-words-site.md`](references/little-monk-kind-words-site.md)。

## 自動化測試

本儲存庫附有不依賴第三方套件的 Python `unittest` 範例，會檢查必要檔案、`SKILL.md` frontmatter、4×3/12 格工作流、繁體中文與職場風險規則，以及 README 使用範例是否存在。

```bash
python -m unittest discover -s tests -v
```

測試檔案位於 [`tests/test_skill.py`](tests/test_skill.py)。若新增規則關鍵字、改變目錄結構或更新 Skill metadata，請同步更新測試。這些測試是結構與內容煙霧測試，不取代實際圖片生成、OCR、去背與人工審稿。

## 自動發布 Release

儲存庫新增 [`Publish Release`](.github/workflows/release.yml) 工作流。當推送符合 `v1.2.3` 格式的 Git tag 時，工作流會先執行完整 Python 測試，測試成功後才使用 GitHub Actions 內建權限自動建立 Release 並產生變更說明。

```bash
git tag v1.2.0
git push origin v1.2.0
```

也可以在 GitHub Actions 介面使用 `workflow_dispatch`，輸入一個已存在的 semver tag，例如 `v1.2.0`。工作流只接受 `v` 開頭的三段式版本號；不符合格式或測試失敗時，不會建立 Release。若要讓工作流運作，儲存庫的 Actions 權限需允許工作流寫入 repository contents；本專案工作流已宣告 `contents: write`。

## GitHub Actions

儲存庫可使用下列最小工作流，在每次 push 或 Pull Request 時執行測試：

```yaml
name: Skill checks

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python -m unittest discover -s tests -v
```

## 輸出檢查清單

在交付前，逐格確認以下項目：

| 項目 | 通過條件 |
| --- | --- |
| 數量與順序 | 共 12 張，依左至右、由上至下排序 |
| 文字 | 台灣繁體字正確，沒有生成模型錯字或簡繁混用 |
| 情境 | 使用者能理解何時使用，語氣與角色關係相符 |
| 職場風險 | 沒有針對真人、公司、身分或弱勢群體的攻擊與洩密內容 |
| 視覺一致性 | 角色外觀、服裝、畫風與主色維持一致 |
| 可讀性 | 文字有足夠對比、未被裁切、沒有遮住臉部或重要動作 |
| 去背 | 背景透明，沒有明顯色邊，也沒有誤刪角色細節 |
| 檔案 | 個別 PNG 排序穩定，並保留原始網格圖與 ZIP |

若要送審 LINE Creators Market，請另外依當時官方規範確認圖片尺寸、檔案大小、主圖、縮圖、版權與內容要求。本 Skill 與 `line-sticker-factory` 的預設值不代表所有市場規範。

## 目錄結構

```text
line-sticker-master/
├── README.md
├── SKILL.md
├── tests/
│   └── test_skill.py
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── release.yml
├── references/
│   ├── line-sticker-factory.md
│   ├── little-monk-kind-words-site.md
│   ├── top-10-sticker-copy-guide.md
│   ├── workplace-meme-catalog.md
│   └── zh-tw-copy-check.md
└── templates/
    └── line-sticker-prompt-template.md
```

`README.md` 是給使用者閱讀的文件；`SKILL.md` 是給 Manus 載入的核心指令；`references/` 只在需要專案整合或繁體中文文字審核時讀取。

## 授權與責任

使用真人、品牌、動漫角色或第三方素材前，請先確認肖像、商標與著作權授權。請不要把未公開的公司資料、客戶資料、帳號或密碼放入貼圖腳本或外部生成服務。公開販售前，請由內容擁有者自行完成法律、平台規範與商業使用審查。

## 來源

本 Skill 的整合設計參考 [`qpooqp777/line-sticker-factory`](https://github.com/qpooqp777/line-sticker-factory)。
