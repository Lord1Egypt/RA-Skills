# MULTI_VAULT_ROUTING.md

目的：把「多 vault 分流」寫成 **Arthur-OS 治理的硬規則**，避免每次都重新討論。

## 這份只管什麼
- 只管 Arthur-OS、Node Local OB、回流三者之間的分流關係
- 不管單一筆記的母區落點，母區落點回到 `ARTHUR_OS_STRUCTURE.md`
- 不管 gateway host / token / health，gateway 細節回到 `READONLY_GATEWAY_BOUNDARIES.md`

## 定義
- **Arthur-OS**：主治理 vault（canonical / source of truth）。
- **Node Local OB**：每個節點各自的本地工作 vault（work-in-progress）。
- **回流（Return / Promote）**：把已確認、可長期沉澱的內容，整理後搬回 Arthur-OS。

## 核心分流規則（拍板）
1) **Arthur-OS = 主治理 vault（唯一 canonical）**
   - 所有「正式知識、可被長期引用的結論、可重複使用的 SOP、治理規則」最後都要在 Arthur-OS。

2) **各節點自有 OB = 本地工作 vault（WIP）**
   - 當下工作、暫存、實驗、節點私有上下文，先寫在 Node Local OB。
   - Node Local OB 不要求結構與 Arthur-OS 完全一致；但若是未來要回流，建議從一開始就用 Arthur-OS 的命名/格式以降低搬運成本。

3) **正式知識一定要回流 Arthur-OS**
   - 判斷「要回流」的常見訊號：
     - 之後還會再用（可複用）
     - 能清楚描述「決策／原則／流程／排錯／設定」
     - 需要跨節點共享或供 gateway 查詢
   - 回流時，目標位置仍依 `ARTHUR_OS_STRUCTURE.md` 的治理落點規則。

4) **read-only gateway 只查 Arthur-OS，不做多 vault 協調**
   - gateway 僅提供對 Arthur-OS 的查詢/讀取。
   - 不跨 vault 聚合、不做「在多 vault 間搜尋後合併」的行為。
   - 原則：降低誤寫/越權風險，避免把治理邏輯塞進 gateway。

## 實務路由（最小可操作版）
- 需要「正式落盤」→ 直接寫 Arthur-OS。
- 需要「先想/先亂寫/先試」→ 寫 Node Local OB；當內容成熟，再回流 Arthur-OS。
- gateway 查不到你本地的內容 → 不是 bug，是規格。

## 未涵蓋（刻意不管）
- 不在本 skill 內定義各節點 Node Local OB 的目錄結構（那是節點自由）。
- 不在本 skill 內定義同步/備份/協作機制（避免把 skill 變成維運手冊）。
