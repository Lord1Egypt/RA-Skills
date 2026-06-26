# VAULT_AND_PATHS

## 目的
釘死 Arthur-OS / OB 的 vault 判定方式，避免亂猜路徑、誤把 mirror 當正式本體。

## 先記住這 4 條
1. source of truth 先看 `obsidian-cli print-default --path-only`
2. 不行再看 `~/Library/Application Support/obsidian/obsidian.json`
3. **workspace mirror 路徑不等於正式可寫路徑**
4. 只有定位到實體 `.md` 檔後，才宣稱可以直接修改正式文件

## Source of truth
優先順序：
1. `obsidian-cli print-default --path-only`
2. `~/Library/Application Support/obsidian/obsidian.json`

## 路徑類型一定要分開
- `obsidian://...`：Obsidian URI，不是 shell 可直接寫入的檔案路徑
- `obsidian/Some/Note`：vault 內相對路徑，不保證已映射到目前 workspace
- `ob/...`：常常只是 workspace mirror / staging 區，不一定是正式本體
- 實體本體：通常是實際 vault 裡的 `.md` 檔，例如 iCloud Arthur-OS 路徑

## 實務判斷順序
1. 先確認 default vault 是不是 Arthur-OS
2. 再判斷使用者給的是 URI、vault 相對路徑、還是本機實體路徑
3. 若 workspace mirror 找不到本體，不要硬猜，改查實體 vault 位置
4. 定位到實體 `.md` 檔後，再修改正式文件

## Arthur-OS 常見實體路徑
僅示例，不要寫死：
- `/Users/arthur/Library/Mobile Documents/iCloud~md~obsidian/Documents/Arthur-OS`

## 何時要看 obsidian.json
- `obsidian-cli` 不可用
- default vault 不明
- 懷疑目前不是 Arthur-OS

## 實戰教訓
- 使用者給 `obsidian://open?vault=Arthur-OS&file=...` 或 `obsidian/Server/...` 時，不要直接假設 workspace 內有同名可寫目錄
- 這類情況應先回到 Arthur-OS 實體 vault 根去找
- 避免在 mirror / staging 路徑誤寫，或誤判「以前可以改、現在不能改」
