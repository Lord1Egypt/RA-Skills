# PoE1 資料與命令參考

## pob-cli 基本需求

`pob-cli` 面向 PoE1 PC Build。純 XML 解析需要 Python；官方 PoB 數值需要 LuaJIT 與 Path of Building Community Fork 原始碼，並以 `POB_ROOT` 或 `--pob-root` 指向 PoB 根目錄。工具不應自行重寫 PoB 傷害／防禦公式。

## 建議命令

```bash
# 先確認主技能與技能組
pob skills BUILD.xml --format json
pob skills BUILD.xml --details --pob-root "$POB_ROOT" --format json

# 讀取天賦與裝備
pob tree BUILD.xml --all
pob items BUILD.xml

# 官方分析與計算
pob analyze BUILD.xml --pob-root "$POB_ROOT" --skill "Creeping Frost" --format json
pob calc BUILD.xml --pob-root "$POB_ROOT" --skill "Creeping Frost" --format json

# 候選天賦驗證
pob optimize-tree BUILD.xml --pob-root "$POB_ROOT" --skill "Creeping Frost" --remove-node NODE_ID --format json
pob optimize-tree-matrix BUILD.xml candidates.json --pob-root "$POB_ROOT" --skill "Creeping Frost" --format json

# 產生但不公開分享 code
pob share BUILD.xml --dry-run
```

若 `pob skills` 找不到主技能，先檢查技能名稱、版本、PoB XML 是否完整。若 `pob calc` 失敗，保留 stderr、PoB commit、Tree 版本與 XML，不要把估算值標成官方數據。

## Ninja 資料策略

PoE Ninja 建構頁使用動態前端；應使用合法的公開 JSON、資料匯出、使用者提供的角色頁或 PoB code。推薦資料最少應包含 league、class/ascendancy、main skill、level、items、skill links、passives 或 keystones，以及資料擷取時間。若來源只提供統計比例，不能推導單一角色的完整天賦與裝備。

技能腳本接受陣列，或包含 `builds`、`results`、`characters`、`data`、`rows` 其中一個陣列欄位的 JSON。它會保留原始候選資料，並按可用的 `score`、`dps`、`totalDps`、`TotalDPS` 或 `rank` 欄位做初步排序；這不是最終推薦評分，最終必須結合防禦、成本、可取得性與使用者條件。

## 角色 code 安全規則

`pob share --dry-run` 只產生 code；不要自動執行實際上傳。`pobb.in` 連結公開後可被讀取，因此只有在使用者明確確認後才可進行公開分享。JSON 中要保存 `uploaded: false` 或實際狀態，不得把 code 是否產生與是否已公開混為一談。
