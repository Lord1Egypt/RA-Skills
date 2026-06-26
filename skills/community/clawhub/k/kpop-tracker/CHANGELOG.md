# Changelog

## v2.1.0 (2026-04-13) 🎉 重大功能更新

### ✨ 新功能
- **3階段搜尋架構**：官方帳號 → 新聞媒體 → 台灣粉絲團
- **中國成員微博監控**：自動檢查中國成員微博動態
- **智能來源標註系統**：🏢官方/📰媒體/🇺🇳微博/🇹🇼台灣
- **最終分類整理**：按內容性質而非來源分類

### 🔄 架構變更
- Config 新增 `chinese_members` 欄位
- `fan_accounts` 重命名為 `taiwan_fan_sources`
- 新增 `youtube` 欄位到 sources
- 更新搜尋優先順序和方式

### 🛠️ 技術改進
- 更穩定的瀏覽器操作流程
- 優化錯誤處理和 fallback 機制
- 改善 DuckDuckGo 被擋時的處理方式

### 📊 測試驗證
- 成功抓取 I-DLE 7月回歸重大消息
- 薇娟和米妮個人活動更新確認
- 雨琦微博檢查機制運作正常

### 📚 文檔更新
- 全新 references/config_examples.md
- 更新 scripts/add_artist.py 支援新架構
- 新增版本控制和 changelog

## v2.0.0 (2026-04-02)
- 6 固定輸出類別重構
- IVE Starship US 簽名專輯監控
- 所有藝人 YouTube 頻道支援

## v1.x (2026-03-31)
- 初版 kpop-tracker
- 基本官方帳號監控功能