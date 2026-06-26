# SKILLS_RULES

## 目的
釘死 `Arthur-OS/Skills/` 的邊界。

## 這份只管什麼
- 只管哪些內容算 `Skills/` 區該收的東西
- 不管 skill 內部 reference 怎麼分檔
- 不管 Arthur-OS 其他母區的總體落點，總體落點回到 `ARTHUR_OS_STRUCTURE.md`

## 1. 可以放進 `Skills/` 的東西
- 自製 skill 文件
- 而且要刻意保持在**重建等級**，不是只有摘要
- 要能從零開始重建
- skill 專屬的 rebuild / freeze / closure / spec 文件
- 最好至少有：主規格、重建手冊、必要 SOP、必要報告

## 為什麼要故意留下完整文件
Arthur 對 `Arthur-OS/Skills/` 的要求不是「留一份簡介」，而是留一份 **human-readable rebuild mirror**。

也就是說：
- 這裡不是拿來存短摘要
- 也不是只放 closure note
- 而是要保留足夠完整的 skill 資料

正式目的：
- 即使 workspace 內原始 skill 檔案整包消失
- 仍可依靠 `Arthur-OS/Skills/<skill-name>/` 內的內容
- 把該 skill 的主要結構、規則、references、scripts 角色與 rollout/acceptance 思路重建回來

所以 `Skills/<skill-name>/` 應優先保留：
- stable spec
- rebuild guide / rebuild handbook
- freeze / closure
- 必要 SOP
- 關鍵定案與高價值驗收紀錄

## 2. 不應放進 `Skills/` 的東西
- 一般 incident 筆記
- ops 歷史文件集
- 隨手 memo
- 只是「和 skill 有關」但本質不是 skill 的文件
- server / Docker 設定
- OpenClaw 維運 dossier（例如 `openclaw-ops` 類）

## 3. 判斷問題
問自己：
- 這是不是一個可重複調用的能力包？
- 這份資料能不能支撐另一隻龍蝦從零重建？
- 若不能，通常就不該進 `Skills/`

## 4. 典型案例
- `nubaby-comfyui` / `nubaby-whisper` / `nubaby-aidata` / `nubaby-obsidian`：適合放 `Skills/`
- `openclaw-ops` 類維運文件集：更適合 `OpenClaw/`

## 5. 命名遷移註記
- 若某 skill 正處於 family 重整或 rename 過渡期，可在規則文件中保留「現實名稱 + 規劃目標名」的雙名寫法。
- 規則文件的目標是維持可重建性與可辨識性，不是為了追求所有歷史名稱一次洗乾淨。
