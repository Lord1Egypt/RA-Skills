# SEARCH_RULES

## 目的
統一 Arthur-OS / OB 的搜尋方式。

## 先記住這 5 條
1. 預設先用本機 `obsidian-cli`
2. 跨節點 / LAN 查詢才用 read-only gateway
3. 不再依賴舊的 `obsidian-search` HTTP 服務
4. 搜尋只負責找到內容，不負責決定要不要改
5. 搜到結果後，下一步交給 `POST_SEARCH_DECISION_RULES.md`

## 常用指令
### 找筆記名稱
```bash
obsidian-cli search "關鍵字"
```

### 搜內容
```bash
obsidian-cli search-content "關鍵字"
```

### 看預設 vault 路徑
```bash
obsidian-cli print-default --path-only
```

## Helper script
可用：`scripts/ob_search.sh`

用法：
```bash
bash scripts/ob_search.sh path
bash scripts/ob_search.sh name 關鍵字
bash scripts/ob_search.sh content 關鍵字
bash scripts/ob_search.sh skill 關鍵字
```

## 跨節點 / LAN 搜尋
- 現行 canonical 入口是 `27133`
- gateway host / token / `/health` 規則，不在這份重複展開
- 一律看：`READONLY_GATEWAY_BOUNDARIES.md`

## 搜尋後銜接
- 搜尋只是第一步
- 搜到結果後，下一步判斷交給 `POST_SEARCH_DECISION_RULES.md`

## 關鍵字提醒
- `OB` = `Obsidian`
- 使用者若說「查 OB」＝ 查 Arthur-OS / Obsidian vault
- 若是落點判斷，優先先想：`Skills / Prompts / OldNotes / Server / OpenClaw / Projects / Library / AIout / 根目錄`
