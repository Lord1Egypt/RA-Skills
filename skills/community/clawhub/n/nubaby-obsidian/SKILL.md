---
name: nubaby-obsidian
description: "Arthur-OS / OB (Obsidian) governance skill for deciding where notes, reports, project docs, server docs, OpenClaw docs, AIout outputs, Library references, Prompts, OldNotes, root notes, and skill-specific rebuild/freeze/closure docs should live. Use when working with Arthur-OS, when the user says Obsidian or OB, when deciding whether something belongs in Skills, OpenClaw, AIout, Library, Server, Projects, Prompts, OldNotes, or the root of the vault, when creating or editing notes, or when searching the vault with obsidian-cli."
---

# nubaby-obsidian

把這個 skill 當成 **Arthur-OS / OB 的治理入口**。它回答三件事：
1. 這篇東西應該放哪裡
2. 要怎麼找
3. 找到後下一步該讀、改、搬、還是新開一篇

它不是一般 Obsidian 教學，也不是任意 multi-vault 控制器。

## 先記住這 8 條就夠了
1. `OB` = `Obsidian`
2. **Arthur-OS = 唯一 canonical vault**，Node Local OB 可以存在，但成熟內容要回流 Arthur-OS
3. **不要猜 vault 路徑**，先 `obsidian-cli print-default --path-only`，不行再看 `obsidian.json`
4. **不要先發明新資料夾**，先對到既有結構
5. `Skills/` 只放自製技能文件，而且要維持 rebuild-grade mirror
6. 跨節點 / LAN 查 OB 時，**read-only gateway 只用來查，不用來寫**
7. Arthur-OS 根目錄筆記規則固定：檔名 `YYYY-MM-DD title.md`，內文首行 `修改時間：YYYY-MM-DD HH:MM:SS`
8. 主線對話要 **summary-forward**，不要把整篇筆記全文倒進聊天

## 快速路由
先看超短索引：`references/QUICK_INDEX.md`

### 你現在是在做哪一類事？
- 要確認 vault / 實體路徑 → `references/VAULT_AND_PATHS.md`
- 要判斷內容該放哪裡 → `references/ARTHUR_OS_STRUCTURE.md`
- 要查 OB / 搜尋筆記 / 用 helper script → `references/SEARCH_RULES.md`
- 要處理跨節點 / LAN read-only gateway → `references/READONLY_GATEWAY_BOUNDARIES.md`
- 搜到之後，不知道該讀 / 改 / 搬 / 新開 → `references/POST_SEARCH_DECISION_RULES.md`
- 要 create / move / rename / delete / direct edit → `references/OPERATIONS_RULES.md`
- 要建立筆記、調整命名、確認開頭格式 → `references/WRITING_RULES.md`
- 要判斷 `Skills/` 區內容該怎麼治理 → `references/SKILLS_RULES.md`
- 要處理多 vault / 回流問題 → `references/MULTI_VAULT_ROUTING.md`
- 要看舊方案與歷史脈絡 → `references/NETWORK_SEARCH_DESIGN_HISTORY.md`

## 高頻硬規則
- 高優先母區：`Skills / Prompts / OldNotes / Server / OpenClaw / Projects / Library / AIout / 根目錄`
- 報告路由：`OpenClaw/Reports` = OpenClaw 系統 / 維運 / 修復 / 事故 / 節點治理；`AIout/Reports` = AI 流程 / 產出 / 匯出 / workflow 結果
- 同一主題預設收斂成 **1 份主文件 + 最多 1 份正式報告**
- 改名 / 搬移優先 `obsidian-cli move`，不要先 `mv`
- Arthur-OS / OB 採 `Backup/` 與 `Trash/` 雙目錄保護；備份與刪除都維持 `.md` 結尾
- 跨節點 / LAN 的 Obsidian 查詢只允許 read-only

## Context hygiene
- 搜尋或讀取筆記時，先定位，再定向讀取，不要預設把大篇全文搬進主線
- 長筆記、長報告、大量摘錄，優先留在 OB / report 檔中
- 回主線時預設只帶：結論、筆記路徑、必要摘錄、下一步
