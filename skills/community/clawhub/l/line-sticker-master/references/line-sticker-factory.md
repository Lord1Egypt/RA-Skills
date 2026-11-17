# line-sticker-factory 整合參考

來源：[qpooqp777/line-sticker-factory](https://github.com/qpooqp777/line-sticker-factory)

## 專案定位

這是一個 React + Vite + Tailwind CSS 前端工具，將一張 4 欄 × 3 列網格圖切成 12 張貼圖，並提供去背、預覽與 ZIP 下載。它不是完整的圖像生成服務；圖像生成應由外部模型、使用者上傳或其他可用的媒體生成流程完成。

## 主要元件

| 元件 | 作用 |
| --- | --- |
| `src/App.jsx` | 串接上傳、選擇、切圖、預覽與下載的應用層 |
| `src/components/PromptGenerator.jsx` | 提供主題、文字語言、畫風、尺寸與排版選項，並輸出套組提示詞 |
| `src/components/GridImageUploader.jsx` | 上傳 4x3 網格圖 |
| `src/components/GridSlicer.jsx` | 按列與欄切圖、縮放、置中、色鍵去背與進度回報 |
| `src/components/Preview.jsx` | 檢視個別貼圖與網格結果 |
| `src/components/DownloadPanel.jsx` | 個別/主圖/分頁圖與 ZIP 輸出 |
| `backend/rembg_server.py` | FastAPI `rembg` 去背服務，支援單張與批次處理 |

## 切圖與尺寸

`GridSlicer` 使用 `GRID_CONFIG.columns` 與 `GRID_CONFIG.rows`，依照 row-major 順序編號 1 至 12。每格會先取原始網格的等分區域，再繪製到工作畫布；程式中的工作尺寸為 740×640。README 同時列出 1480×960、1200×896、2560×1664 等可選網格尺寸，實際使用前應以目前版本 `src/i18n.js` 和元件程式碼為準，不要只依賴 README。

## 色鍵去背參數

瀏覽器端 Web Worker 以目標色與 RGB 歐氏距離計算透明度，主要參數為 `targetColor`、`tolerance`、`smoothness`、`despill`。內建預設包含：綠色 `#00FF00`、容差 30、柔化 2、去綠色溢出；黑色 `#000000`、容差 15、柔化 1；白色 `#FFFFFF`、容差 20、柔化 2。綠色去背時，若前景也含大量綠色，可能被誤刪，應改用其他背景色或 AI 去背。

## Python 去背

`backend/rembg_server.py` 提供：

```text
GET  /
POST /remove-bg
POST /remove-bg-batch
```

服務將上傳圖片轉成 RGBA，呼叫 `rembg.remove`，再回傳 PNG data URL。它需要安裝 `backend/requirements.txt` 的依賴，且模型首次使用可能需要下載或暖機。此後端適合毛髮、半透明邊緣等色鍵難以處理的圖片，但不應在未經使用者同意下把私人圖片上傳到外部服務。

## 修改專案的建議

若要把 Skill 直接整合進此專案，新增獨立的腳本資料結構或匯入器，格式可採：`characterBible`、`visualStyle`、`backgroundKey`、`language`、`panels[12]`。讓 `GridSlicer` 只負責圖像處理，讓 `PromptGenerator` 或新的 `StickerPlanImporter` 負責腳本與提示詞。所有生成結果都要在切圖後逐格驗證，避免把錯字、裁切或角色不一致帶入 ZIP。
