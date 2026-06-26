# ARTHUR_OS_STRUCTURE

## 目的
回答：Arthur-OS 裡的東西到底該放哪裡。

## 這份只管什麼
- 只管「內容落點 / 母區判斷」
- 不管 vault 實體路徑
- 不管搜尋方式
- 不管跨節點 gateway
- 不管 create / rename / move / delete 的具體操作步驟

## 根規則
- 不要先發明新目錄。
- 先把內容對到現有結構。
- 小細節由龍蝦自行收斂；大結構、會影響亞瑟使用習慣的才再問。
- **不要亂動亞瑟自己管理的目錄**；只主動整理龍蝦自己主導建立、自己長出來的區。
- 亞瑟明確在意的高優先判斷目錄是：`Skills / Prompts / OldNotes / Server / OpenClaw / Projects / Library / AIout / 根目錄`。
- `assets` 保留在結構裡，但不用當高優先 trigger 重點；其使用主要由外掛處理。

## 正式主骨架
- `Skills/`
- `Prompts/`
- `OldNotes/`
- `Server/`
- `OpenClaw/`
- `Projects/`
- `Library/`
- `AIout/`
- `assets/`
- 根目錄（隨手記）

---

## 1. `Skills/`
- 只放自製技能文件
- 要非常完整
- 要能從零開始重建
- skill 專屬的 spec / rebuild / closure / freeze 文件，也優先放在 `Skills/<skill-name>/` 專用目錄
- 不放 incident 筆記
- 不放隨手 memo
- 不放只是相關、但本質不是 skill 的 ops 文件集

## 2. `Prompts/`
- 放各種 n8n AI agent system prompt / 系統指令
- 子目錄主要放各類圖片生成指令
- `Prompts/Nails/` 為 nail / 美甲相關 prompt 主區
- `Training/` 已取消；原先 training 內容併入 `Prompts/Nails/`
- 先維持單層簡單，不再往下硬開 `References/`

## 3. `OldNotes/`
- 原 `apple-notes-old/`
- Apple Notes 搬來的舊筆記區
- 偏歷史資料，不是新規則主要落點

## 4. `Server/`
- 原 `server-setup/`
- 各種 server / docker / infra / deploy / config 文件
- server / service / compose / tunnel / repair / setup 類文件優先放這裡

## 5. `OpenClaw/`
- OpenClaw 專屬主題母區
- 放 incident / repair / rollout / migration / reports / playbooks / ops bundle
- 內部分層方向：
  - `Incidents/`
  - `Reports/`
  - `Playbooks/`
  - `openclaw-ops/`
  - `_bak/`
- 根層只留少量 summary / note / 過渡性總文件
- `OpenClaw/Memory_Daily/` 是正式 daily 記錄區

## 6. `Projects/`
- 放長期專案文件
- 需求、規格、會議紀錄、里程碑、專案型輸出

## 7. `Library/`
- 收窄成：summary / memory / 歷史參考區
- 適合：
  - `Daily_Summaries/`
  - `Long-Term-Memory/`
  - 長期累積型參考
- 不再混 active playbook / OpenClaw daily memory
- `Library/Infra/Update_Sources.md` 保留作為更新來源 / 升級通知 / 變更摘要的知識基底

## 8. `AIout/`
- 收窄成：AI 產出 / 匯出 / raw mirror / archive 區
- 直接用兩層結構，不再包 `Text/`
- 目前可接受子區：
  - `Archive/`
  - `Playbook/`
  - `Reports/`
- 根層可保留少量單篇 AI 匯出文件
- 不把它當一般治理文件總桶

## 9. `assets/`
- 放筆記用圖片、附件、非 markdown 配套素材
- 圖、附件、引用素材優先放這裡

## 10. 根目錄
- 亞瑟隨手記的內容預設放這裡
- 適合短 memo、臨時筆記、快速落地內容
