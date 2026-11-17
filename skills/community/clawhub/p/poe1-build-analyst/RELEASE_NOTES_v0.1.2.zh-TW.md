# poe1-build-analyst v0.1.2

## 發布日期

2026-08-20

## 版本概述

`poe1-build-analyst` v0.1.2 是 Path of Exile 1 BD 分析 skill 的文件與發布 metadata 更新版本。本版讓儲存庫能自我描述版本，完成英文、繁體中文與簡體中文 README 的章節對齊，並保留 v0.1.1 建立的安全加固 PoB 分析流程。

本版本已準備於公開 GitHub 儲存庫的 [`73c1385`](https://github.com/qpooqp777/poe1-build-analyst/commit/73c1385) commit。ClawHub registry 在 v0.1.2 明確發布前仍維持 v0.1.1。

## 主要更新

### 儲存庫版本 metadata

新增輕量的 [`VERSION`](https://github.com/qpooqp777/poe1-build-analyst/blob/master/VERSION) 檔案，記錄儲存庫目前的發布候選版本為 `0.1.2`。這為儲存庫檢查與發布自動化提供簡單的版本來源，不需要額外引入套件 manifest。

### 三語文件完全對齊

英文版 [`README.md`](https://github.com/qpooqp777/poe1-build-analyst/blob/master/README.md)、繁體中文版 [`README.zh-TW.md`](https://github.com/qpooqp777/poe1-build-analyst/blob/master/README.zh-TW.md) 與簡體中文版 [`README.zh-CN.md`](https://github.com/qpooqp777/poe1-build-analyst/blob/master/README.zh-CN.md) 現在都包含相同的九個主要章節。中文版本已補上終局角色 code 命令、可選的被動樹研究工具、輸出 schema、內含資源、參考資料與儲存庫版本說明。

### 延續 v0.1.1 的安全基線

本版保留 v0.1.1 的安全加固，包括移除任意 PoB 執行檔選擇、限制只能使用由 `PATH` 解析的可信 `pob` 執行檔、加入執行 timeout 與輸出大小上限、驗證 JSON object，並在輸入無效或輸出過量時 fail closed。Skill 不會上傳角色資料，且將 `pob share --dry-run` 與公開 `pobb.in` 發布保持分離。

## 驗證結果

本發布候選已通過 skill-creator 驗證與 Markdown 一致性檢查。三份 README 的主要章節數一致，GitHub 上的 `VERSION` 檔案內容正好是 `0.1.2`。

PoB 整合回歸測試使用從 ClawHub 安裝的 v0.1.1 套件執行；該套件包含與本 v0.1.2 文件／metadata 候選相同的 runtime scripts。測試使用 LuaJIT 與 Path of Building Community headless core，成功解碼 PoB character code、保留匯入 BD、執行 `pob analyze` 與 `pob calc`、選取 `Vortex`、辨識 `3_29` 天賦樹版本，並回傳 `status: verified` 與 782 個官方 scalar 欄位。

| 驗證項目 | 結果 |
| --- | --- |
| Skill 結構驗證 | 通過 |
| README 語言與章節對齊 | 通過；每份 README 均有 9 個主要章節 |
| 儲存庫 VERSION metadata | 通過；內容為 `0.1.2` |
| PoB character code 解碼 | 通過 |
| 官方 `pob analyze` 整合 | 通過 |
| 官方 `pob calc` 整合 | 通過 |
| 僅限終局工作流程契約 | 通過；只輸出 `stages.endgame` |
| 公開角色資料上傳 | 未執行 |

## 相容性與需求

Skill 的結構處理需要 Python 3。官方 PoB 計算需要 LuaJIT 與相容的 Path of Building Community 原始碼。終局角色 code 工作流程需要完整的 PoB character code，不接受短的 `pobb.in/<id>` 網址。若 PoB root、LuaJIT runtime、XML schema 或技能 metadata 不可用，流程必須標示 blocked 或 failed，不得自行捏造指標。

## 升級注意事項

從 GitHub 安裝時，請確認 `VERSION` 顯示 `0.1.2`，且三份本地化 README 均存在。從 ClawHub 安裝時，請另外確認 registry 版本；在 registry 顯示 v0.1.2 的版本與安全稽核前，不應視為 ClawHub 已完成發布。

本版本不會建立公開的 `pobb.in` URL。角色 code 產生與公開上傳仍是兩個分離操作，公開分享必須先取得使用者明確確認。

## 貢獻者

由 Manus AI 為 `qpooqp777/poe1-build-analyst` 儲存庫整理。

## 參考資料

- [GitHub 儲存庫](https://github.com/qpooqp777/poe1-build-analyst)
- [ClawHub skill](https://clawhub.ai/qpooqp777/skills/poe1-build-analyst)
- [qpooqp777/pob-cli](https://github.com/qpooqp777/pob-cli)
- [Path of Building Community Fork](https://github.com/PathOfBuildingCommunity/PathOfBuilding)
