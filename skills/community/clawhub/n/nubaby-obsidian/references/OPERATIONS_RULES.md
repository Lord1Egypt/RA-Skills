# OPERATIONS_RULES

## 目的
補齊 Arthur-OS / OB 的操作層規則：create / move / rename / delete / 直接編輯 / vault 判定。

## 1. 先確認 vault
- 優先用：`obsidian-cli print-default --path-only`
- 若 default vault 不明或懷疑不對，再看：`~/Library/Application Support/obsidian/obsidian.json`
- 不要憑記憶硬猜 vault 路徑
- 若使用者提供的是 `obsidian://...` 或 `obsidian/...`，先判定那是 URI / vault 內相對路徑，不要直接當作本機可寫實體路徑
- 若 workspace 內的 `ob/...` 或其他 mirror 找不到正式文件本體，應進一步查 Arthur-OS 的實體 vault 路徑（常見為 iCloud Obsidian vault）

## 2. 建立新筆記：何時用 `obsidian-cli create`
適合用 `obsidian-cli create`：
- 需要透過 Obsidian URI 正常建新 note
- 想快速在既有 vault 內建立一篇標準筆記
- 路徑乾淨、不是 dot-folder

不適合用 `obsidian-cli create`：
- 目標在 hidden dot-folder
- 只是要批次產生一堆檔案骨架
- 只是在已知 markdown 路徑做單純文字寫入

## 3. 直接寫 `.md`：何時可接受
可直接寫 `.md`：
- 已確定落點
- 已定位到正式文件的實體 `.md` 路徑
- 只是要寫入 / 更新純文字內容
- 不涉及跨檔 refactor
- 不需要 Obsidian URI 幫忙開啟或建立

不可直接宣稱能改正式文件的情況：
- 只有 `obsidian://...` URI
- 只有 vault 內相對路徑，例如 `obsidian/Server/...`
- 只看到 workspace mirror 路徑，但尚未確認它是不是正式本體

## 4. 移動 / 改名：優先 `obsidian-cli move`
- note 改名或移動時，**優先用 `obsidian-cli move`，不要先用 shell `mv`**
- 原因：`obsidian-cli move` 會處理 wikilinks 與常見 Markdown links refactor
- 只有在你明確知道不需要 link refactor 時，才考慮直接檔案層搬移

### 4.1 link-safe refactor 判斷
以下情況幾乎都應優先 `obsidian-cli move`：
- note 已被其他筆記引用
- 目標是 `Skills/`、`OpenClaw/`、`Projects/` 等高連結密度區
- 檔名會改，且可能影響 wikilinks
- 路徑會改，且可能影響相對 Markdown links

以下情況才可考慮直接檔案層操作：
- 新建後幾乎沒被引用的單篇草稿
- 明確確認沒有 link refactor 需求
- 只是暫存區或非正式區的小範圍整理

### 4.2 批次 refactor 原則
- 批次改名 / 批次搬移前，先做小樣本驗證
- 先確認目標區是否為亞瑟自己管理目錄
- 不要對高價值目錄直接做大量 shell rename
- 若牽涉大量 link 更新，優先拆批處理，不一次梭哈

## 5. 刪除：小心使用 `obsidian-cli delete`
適合用 `obsidian-cli delete`：
- 要刪的是明確單篇 note
- 已確認不是亞瑟自己管理的重要內容
- 已確認不是大範圍誤刪風險

不適合直接刪：
- 一次刪整批而未驗證
- 對目錄主控權不清楚
- 對是否屬於亞瑟自己管理的區還有疑問

## 6. 大量整理原則
- 大範圍搬移、改名、刪除前，先做分類與小樣本驗證
- 若涉及 Arthur-OS 骨架或亞瑟自己管理的目錄，先停下來確認
- 龍蝦只主動整理自己主導建立、自己長出來的區

## 7. 目前常用操作指令
```bash
obsidian-cli print-default --path-only
obsidian-cli search "關鍵字"
obsidian-cli search-content "關鍵字"
obsidian-cli create "Folder/New note" --content "..."
obsidian-cli move "old/path/note" "new/path/note"
obsidian-cli delete "path/note"
```

## 8. 實務選擇準則
- 查路徑：`print-default`
- 搜名稱：`search`
- 搜內容：`search-content`
- 新建單篇 note：可考慮 `create`
- 單篇 note 改名 / 搬移：優先 `move`
- 純文字內容修改：可直接編輯 `.md`
- 刪單篇 note：審慎使用 `delete`
