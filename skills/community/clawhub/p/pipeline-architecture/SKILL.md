---
name: "pipeline-architecture"
description: "採用 Pipeline Architecture（先宣告意圖、後統一執行）的專案，其業務邏輯讀寫流程的結構規範。支援 Python/FastAPI、TypeScript/Node.js 與 Flutter/Dart 三種實作，並提供 Payload CMS 與 Cloudflare Workers 的專屬補充。當專案已採用此架構、且任務涉及業務邏輯流程時使用，包含：新增 API endpoint、設計資料寫入流程、實作權限檢查、多步驟資料處理、跨系統寫入（DB、外部 API、裝置變數）、審計日誌，或任何「先決策後執行」的 workflow。在 Flutter 專案中同樣適用於使用者觸發的業務寫入流程：UseCase、ViewModel 的 Command、本地資料庫寫入、呼叫後端 API、離線寫入與 outbox 同步。看到 pipeline、step、query、mutation、scratch、persistence、StepCommit、StepStop、DataMutation、run_workflow、make_pipeline、runWorkflow、makePipeline、outbox、離線同步 等本架構專有名詞，或要在既有 pipeline 專案中修改業務邏輯時，讀取此 Skill 並依專案語言載入對應的 references 檔案；專案若以 Payload CMS 為基底（存在 payload.config.ts、collections/、custom endpoints、collection hooks），額外載入 references/payload-cms.md；專案若部署在 Cloudflare Workers（存在 wrangler.toml 或 wrangler.jsonc），額外載入 references/cloudflare-workers.md，在 Cloudflare 上規劃採用本架構而要決定資料庫（Hyperdrive、D1、Durable Objects）時也要讀取；專案若是 Flutter（存在 pubspec.yaml 且依賴 flutter），載入 references/flutter.md。不適用於一次性腳本、prototype、資料分析、Widget 與純顯示邏輯，或專案尚未採用此架構的情況；使用者明確指示其他做法時，以使用者指示為準。"
---

# Pipeline Architecture

## 選擇語言參考檔（動手前先做這件事）

本檔案只描述**與語言無關的架構規則**。所有程式碼範例都放在 `references/` 底下。
寫任何程式碼之前，先判斷專案語言與基底框架，然後**只讀對應的那一列**：

| 判斷依據 | 語言 | 讀哪一份 |
|---|---|---|
| 有 `pyproject.toml` / `requirements.txt`，或要改的檔案是 `.py` | Python / FastAPI | `references/python.md` |
| 有 `package.json` / `tsconfig.json`，或要改的檔案是 `.ts` | TypeScript / Node.js | `references/typescript.md` |
| 上述 TypeScript 條件成立，**且**有 `payload.config.ts`（或 `package.json` 依賴 `payload`） | TypeScript on Payload CMS | `references/typescript.md` **與** `references/payload-cms.md`，兩份都讀 |
| 上述 TypeScript 條件成立，**且**有 `wrangler.toml`／`wrangler.jsonc`／`wrangler.json` | TypeScript on Cloudflare Workers | `references/typescript.md` **與** `references/cloudflare-workers.md`，兩份都讀 |
| 有 `pubspec.yaml` 且依賴 `flutter`，或要改的檔案是 `.dart` | Flutter / Dart（客戶端） | `references/flutter.md` |

所有 reference 描述的是**同一套架構**，本檔案的所有規則一律適用。同時符合 Payload 與 Cloudflare 兩列時，本 Skill 尚未涵蓋，先與維護者確認。

- ❌ **禁止混用命名慣例**：不要在 Python 專案裡寫出 `runWorkflow`，也不要在 TypeScript 或 Dart 專案裡寫出 `run_workflow`。
- ❌ **禁止跨語言混讀**：`python.md`、`typescript.md` 與 `flutter.md` 只讀專案實際使用的那一份，避免把另一種語言的寫法帶進來。
- ✅ **`payload-cms.md` 與 `cloudflare-workers.md` 是例外**：它們是 `typescript.md` 的**補充**而非替代，對應的專案必須兩份都讀。衝突時以補充檔為準；補充檔沒提到的一律照 `typescript.md`。
- ⚠️ **後端各份（`python.md`／`typescript.md`／`payload-cms.md`／`cloudflare-workers.md`）之間唯一的結構性差異是 transaction 邊界**（見下方「跨語言差異」一節），其餘都只是語法不同。
- 🚨 **`flutter.md` 是客戶端，偏離的地方比較多**：三種寫入模式、離線 outbox 與同步 runner、後端 4xx 的回傳路徑，都是後端版沒有的機制。在 Flutter 專案裡，本檔與 `flutter.md` 衝突時以 `flutter.md` 為準；`flutter.md` 沒提到的一律照本檔。**不要把 Flutter 的 outbox 機制搬回後端專案。**

---

## 適用範圍與邊界

**適用：** 專案**已經採用**本架構時，業務邏輯的讀寫流程（Route → Service → Pipeline → Engine → Step → Query → Persistence）。在本專案中，本 Skill 取代 python-design-patterns。

**不適用，不要硬套：**
- 一次性腳本、spike、prototype、資料遷移工具
- 建置設定、CI、資料分析腳本
- UI 元件本身：Widget／component、版面、動畫、導航，以及主題、上次開啟的分頁這類 UI 偏好的讀寫
- 純顯示用的讀取（資料 → UI 的方向由框架原本的機制負責，不經過 Pipeline）
- 沒有分支判斷、也沒有寫入的簡單查詢（不需要為了形式湊滿七層）
- 專案尚未採用本架構時 —— 先與維護者確認是否要導入，**不要自行改造既有程式碼結構**

**規劃中的 Cloudflare 專案：** 使用者已決定採用本架構、正在規劃部署在 Cloudflare 的新專案時，本 Skill 適用於「選資料庫」這件事。先讀 `references/cloudflare-workers.md` 的「規劃階段檢查」，用業務語言提醒使用者，**不要自行選 D1**。

**客戶端（Flutter）的適用範圍：** 「純前端不適用」指的是 UI 元件本身，不是整個客戶端專案。使用者觸發的**業務寫入流程**（寫本地資料庫、呼叫後端 API、離線排入 outbox）一樣適用本架構，細節見 `references/flutter.md` 的「三種寫入模式」。

**使用者指示優先。** 若使用者明確要求不同做法，以使用者指示為準；但要主動說明這樣會偏離本架構的哪一條規則，讓使用者知道取捨。不要靜默套用架構，也不要靜默偏離。

**不要自行擴大適用範圍。** 本 Skill 只規範業務邏輯的**結構**，不取代 linter、不規範命名以外的程式碼風格、不決定技術選型（技術選型見 `technical-decision-policy`）、不決定文件格式（見 `software-spec-writing`）。唯一的例外是 Cloudflare 上的資料庫：Atomic Chain 需要互動式 transaction，這是架構本身的硬性前提，因此 `cloudflare-workers.md` 指定預設為 Hyperdrive + Postgres。專案的決策準則檔或 ADR 已另有指定時以其為準，但與本架構不相容時要指出來。

---

## 核心思想

**先說完所有意圖，再一次執行。**

Pipeline 執行期間只做兩件事：讀取世界的狀態（Query）、宣告想要改變什麼（Mutation）。
真正的寫入永遠發生在 Pipeline 結束之後，由 Persistence 層統一執行。

這讓整個 workflow 的意圖可以被記錄、被測試、被重播，副作用永遠可預期。

**「中繼資料」與「意圖」是兩件不同的事。** Step 之間為了做判斷而互相傳遞的暫存資料（例如查到的方案限制）稱為 **scratch**，它只是計算過程中的草稿；真正要交給 Persistence 執行的寫入意圖是 **DataMutation**，只能由 StepCommit 一次組裝完成。scratch 不會、也不能自動變成 mutation 的一部分 —— 詳見「Step 的三種回傳值」一節。

---

## 架構總覽

```mermaid
flowchart TD
    A["Route<br/>接收 HTTP request"] --> B["Service<br/>宣告 PipelineStep 清單 + initial input"]
    B --> C{"選擇 Chain 模式"}
    C -->|"多個寫入需一起成功／失敗"| D1[["Atomic Chain<br/>開啟 DB transaction"]]
    C -->|"各 Pipeline 獨立，部分失敗可接受"| D2[["Sequential Chain<br/>不開 transaction"]]

    D1 --> E
    D2 --> E

    subgraph LOOP["依序執行 steps 清單中的每個 PipelineStep"]
        direction TB
        E["build ctx<br/>建構本次 Ctx"] --> F["make pipeline<br/>取得 Step 清單"]
        F --> G["Engine 執行 Pipeline"]
        G --> H["依序執行 Step<br/>Step 呼叫 Query 純讀取"]
        H --> I{"Step 回傳"}
        I -->|"StepContinue<br/>累積 scratch"| H
        I -->|StepCommit| L["execute mutation<br/>→ Persistence Layer"]
        L --> M["MutationResult<br/>intent log + result log"]
        I -->|"StepStop 2xx<br/>純查詢結束，無 mutation"| N["跳過本次 Persistence"]
        M --> O["作為下一個 PipelineStep<br/>build ctx 的輸入"]
        N --> O
        O -.->|還有下一個 PipelineStep| E
    end

    I -->|"StepStop 4xx<br/>業務拒絕"| J{"Chain 模式"}
    J -->|Atomic| K1["rollback<br/>先前已寫入的內容一併回滾"]
    J -->|Sequential| K2["直接停止<br/>已 commit 的 Pipeline 不會回滾"]

    LOOP -->|"清單全部執行完"| P{"Chain 模式"}
    P -->|Atomic| Q1["commit<br/>整條鏈一起生效"]
    P -->|Sequential| Q2["每個 Pipeline 早已各自 commit"]

    K1 --> R["PersistenceResult"]
    K2 --> R
    Q1 --> R
    Q2 --> R
    R --> S["Route 回傳 HTTP Response"]
```

**圖中重點：**
- **Atomic Chain**：整條迴圈在同一個 DB transaction 內執行，任何 `StepStop(4xx)` 觸發 rollback 時，先前已經寫入的內容也會一起回滾；全部跑完才在最後統一 commit。
- **Sequential Chain**：沒有 transaction。每個 StepCommit 觸發的寫入是獨立、立即生效的 commit；中途若有 `StepStop(4xx)`，只是停止繼續往下跑，**已經 commit 的 Pipeline 不會被回滾**。
- 兩種模式共用同一套「迴圈內現場建構 ctx → 執行 Pipeline → 依 Step 回傳決定是否寫入」邏輯，差異只在 transaction 邊界與失敗時的回滾範圍。
- **客戶端（Flutter）沿用同一張圖**，只是 Route 換成 ViewModel 的 Command，而且鏈的結尾決定了這條 workflow 是「僅本地」「離線可用」還是「僅線上」。離線可用的鏈結尾會多一個把請求寫進 outbox 的 Pipeline，實際送出由同步 runner 在 commit 之後負責 —— 見 `references/flutter.md`。

---

## 層與職責

| 層 | 職責 | 關鍵限制 |
|---|---|---|
| **Route** | 接收 HTTP request，呼叫 Service | 不含業務邏輯 |
| **Service** | 宣告 Pipeline 鏈；協調跨域流程 | 不含業務邏輯 |
| **Pipeline Chain** | 依序執行 Pipeline；Atomic 模式管理 transaction | 共用基礎設施，不因業務修改 |
| **Pipeline** | 宣告 step 清單；注入依賴 | 只有 list，無條件判斷、無 I/O |
| **Engine** | 執行 steps；累積 scratch；收集 spans | 共用基礎設施，不因業務修改 |
| **Step** | 決策與資料形狀對映 | 不直接碰 DB；呼叫 Query |
| **Query** | 純讀取：DB、API、runtime 變數、純計算 | 不寫入；不知道 ctx／scratch |
| **Persistence** | 執行 mutation；記錄 intent／result log | 單一寫入入口，不含業務邏輯 |

---

## 命名規則

每個層的函式在**檔案內部**使用固定的通用名稱。
呼叫端在 **import 時加入 domain 名稱**區分不同 domain（TypeScript 用 `as`，Python 用 `as`）。

Query 和 Persistence 函式依照功能命名，不套用固定通用名稱。

### 跨語言命名對照

| 概念 | TypeScript | Python | Dart / Flutter |
|---|---|---|---|
| Service 入口 | `runWorkflow` | `run_workflow` | `runWorkflow`（UseCase 類別的方法） |
| Pipeline 工廠 | `makePipeline` | `make_pipeline` | `makePipeline` |
| commit step | `buildCommit` | `build_commit` | `buildCommit` |
| Chain 函式 | `runAtomicChain` / `runSequentialChain` | `run_atomic_chain` / `run_sequential_chain` | `runAtomicChain` / `runSequentialChain` |
| ctx 建構 | `buildCtx` | `build_ctx` | `buildCtx` |
| 寫入入口 | `executeMutation` | `execute_mutation` | `executeMutation` |
| 強制執行旗標 | `alwaysRun` | `always_run` | `alwaysRun` |
| 檔名慣例 | kebab-case（`pipeline-chain.ts`） | snake_case（`pipeline_chain.py`） | snake_case（`pipeline_chain.dart`） |
| schema 欄位 | camelCase（`changedFields`） | snake_case（`changed_fields`） | camelCase（`changedFields`） |
| domain 型別目錄 | `types/` | `schemas/`（避開 stdlib `types` 衝突） | `domain/models/`（Flutter 官方用語） |
| Service 層的目錄 | `services/` | `services/` | `domain/use_cases/`（Flutter 的 `services/` 已是 API client） |
| import 前綴 | `as` + camelCase | `as` + snake_case | `as` + lowercase_with_underscores（Dart 慣例） |

---

## Step 的三種回傳值

每個 Step 只能回傳三種值之一：

| 回傳值 | 語意 | 攜帶的資料 | Engine 行為 |
|---|---|---|---|
| **StepContinue** | 繼續，附帶部分中繼資料 | `scratch`（暫存，供後續 Step 判斷用） | 合併進累積的 scratch，執行下一個 Step |
| **StepStop** | 終止，無寫入意圖 | 無 | 直接回傳 output，不觸碰 Persistence |
| **StepCommit** | 終止，帶著完整 Mutation | `mutation`（完整、型別明確的 DataMutation） | 回傳 output + mutation，交給 Persistence |

**StepStop 的兩種情境：**
- 業務拒絕（403 權限不足、404 找不到資源、422 條件不符）
- 成功的純查詢結束（200，有 output 但沒有任何寫入意圖）

**StepCommit 是唯一帶著 Mutation 離開 Pipeline 的方式。**
Step 不宣告下一步要做什麼。Pipeline 之間的串接由 Service 層的 Pipeline Chain 決定。

> **設計轉向說明：** 本版本刻意以「Service 端的 PipelineStep 清單」取代早期版本中「由 StepCommit 宣告 `next_pipelines`（可預測／不可預測世界）」的機制。所有 Pipeline 串接一律收斂到 Service 層宣告，StepCommit 不再包含任何後續流程的欄位。若對照舊版設計文件發現 `next_pipelines` 相關描述，以本版本為準。

### scratch 與 mutation 不會混在一起

`StepContinue` 的 scratch 是 Step 之間傳遞的中繼資料（例如查詢結果、暫存的判斷依據），型別是自由的字典／map，單純方便後續 Step 讀取。它**不是** DataMutation 的草稿，Engine 也**不會**把 scratch 自動併入最終送進 Persistence 的 mutation。

真正的寫入意圖必須由 StepCommit 自己組裝成一份完整、符合 DataMutation schema 的物件 —— 通常會讀取 ctx 或先前累積的 scratch 來決定內容，但輸出的 mutation 本身必須是乾淨、只包含 DataMutation 定義欄位的物件，不會殘留 `plan_limits` 這類判斷用的暫存資料。

**因此 StepCommit 的 mutation 欄位在兩種語言都被宣告為明確的 DataMutation 型別**（而非自由字典），讓型別系統直接擋掉污染，不需要任何強制轉型。

---

## DataMutation（意圖 Schema）

DataMutation 是**封閉的 schema**：只包含以下欄位。StepCommit 組裝時不應該、也不能夾帶 schema 之外的暫存欄位（那些屬於 scratch 的職責）。

| 欄位 | 語意 |
|---|---|
| `entity` | 實體名稱（如 `user`、`order`） |
| `target` | `database` / `file` / `device` / `external_api` |
| `operation` | `create` / `update` / `delete` |
| `before` | 變更前資料 |
| `after` | 變更後資料 |
| `changed_fields` | 異動欄位清單 |
| `performed_by` | 執行者 |
| `reason` | 異動原因（寫進 audit log） |

**before／after 的語意：**
- `create`：before = null，after = 新資料
- `update`：before = 變更前（由 Persistence 擷取），after = 變更後
- `delete`：before = 刪除前資料，after = null

Step 宣告的是「意圖」，`before` 在宣告階段可能為 null，真正的 before 由 Persistence 在執行前擷取並記錄。

### 非資料庫寫入的額外要求

Persistence 是唯一的寫入入口，讓所有副作用都有 intent log 與 result log 可稽核。但**可稽核不等於已授權**。`target` 為 `device`、`file`、`external_api` 的 mutation 會改動資料庫以外的系統狀態，額外遵守以下規則：

- **授權檢查是 Step 的職責。** 任何非 `database` 的寫入，Pipeline 中必須有明確的授權 Step（例如 `steps/common` 的權限檢查），不能只靠 Persistence 層把關 —— Persistence 不含業務邏輯，它不知道誰有權限做什麼。
- **`performed_by` 必須是真實執行者身分**，來自 ctx 中的認證資訊。範例中的 `"system"` 只是佔位字串，不要照抄進正式程式碼。
- **`device` 與 `file` 的可寫入目標必須在 adapter 內以白名單列舉。** 不接受由 mutation 動態指定任意主機路徑、系統變數或裝置位址 —— 否則等於把任意檔案寫入的能力開放給業務層。
- **外部呼叫必須 `await`，禁止 fire-and-forget。** `execute_mutation` 的合約要求回傳 `MutationResult`，沒等回應就沒有 `after` 可填。更關鍵的是：未 await 的呼叫失敗時不會拋例外、不會觸發 rollback，chain 會照常 commit，導致 DB 與外部系統永久不一致且無人察覺。
- **新增 target 或 adapter 屬於技術決策，不由 agent 自行拍板。** 要在 `persistence/adapters/` 底下新增會改動主機、裝置或外部系統狀態的實作，先與維護者確認範圍（見 `technical-decision-policy`）。
- 🚨 **客戶端的授權 Step 不是授權。** 在 Flutter／行動端，程式碼可被逆向、請求可被偽造、`performed_by` 可被竄改。客戶端的授權 Step 只是提前擋下以改善體驗，**每一個服務客戶端的後端 endpoint 都必須自己再跑一次授權**。詳見 `references/flutter.md`。

---

## MutationResult（真實寫入結果）

Persistence 執行完一筆 mutation 後回傳的結果，包含：`before`、`after`、`diff`、`intent_log_id`、`result_log_id`。

**`after` 是真實寫入後的狀態**，包含資料庫自動生成的欄位（id、created_at、version 等）。Chain 將此值傳遞給下一個 Pipeline 作為 ctx 基礎，**不能**用 `DataMutation.after`（意圖中的 after）代替。

**沒有 `success` 欄位。** 目前寫入失敗一律以例外處理（由 Chain 攔截並回滾），因此 MutationResult 只描述成功寫入後的結果。若未來需要區分「失敗但不拋例外」的情境（例如 Compensate 機制），屆時應以 discriminated union（`MutationSuccess | MutationFailure`）重新設計，而非加回一個布林旗標。

---

## Pipeline Chain 的兩種模式

| 模式 | 行為 | 適用場景 |
|---|---|---|
| **Atomic Chain** | 所有 Pipeline 在同一 DB transaction 內執行，全部成功才 commit，任何失敗則 rollback | 多個寫入必須一起成功或一起失敗（**預設選項**） |
| **Sequential Chain** | 每個 Pipeline 獨立 commit，失敗不影響已完成的 Pipeline | 每個 Pipeline 獨立，部分失敗可接受 |

> **Cloudflare D1 專案沒有 Atomic Chain**，改用能力較弱的第三種模式 **Batch Chain**（`runBatchChain`）：所有寫入收集到最後一次 `batch()`，一起成功或失敗，但後續 Pipeline 讀不到前面的寫入、沒有讀後寫保護、鏈中不能有外部呼叫。細節見 `references/cloudflare-workers.md`。

兩者呼叫端介面一致：都接收 **PipelineStep 清單**與 **initial input**（傳給第一個 Pipeline 的 ctx 建構函式的原始輸入），**不是**已經建好的 Ctx。

> 🚨 **Atomic Chain 的原子性只涵蓋資料庫。** 若 chain 中有 `target` 為 `external_api`、`file`、`device` 的 mutation，rollback 時這些副作用**不會**被撤銷：資料已送達第三方且對方會留存、簡訊已發、款已扣、檔案已寫、裝置設定已變更。重跑整條 chain 時 DB 會乾淨重來，但外部呼叫會**第二次發生**。詳細後果與因應方式見 references 的「未來擴展點：Compensate」一節，動手前務必讀過。

**因應排序規則：非資料庫寫入的 Pipeline 一律放 chain 最後，且其後不得再新增 Pipeline。**

真正的危險不是「外部呼叫失敗」，而是「外部呼叫成功了，但後面的 Pipeline 失敗」—— 被回滾的是 DB，不是那通已送出的請求。放最後，它後面就沒有東西會失敗；外部呼叫自己失敗時直接 throw，此時 DB 尚未 commit，回滾是乾淨的，兩邊一致。

在 Service 定義 chain 的該節點處加註解說明「此節點之後不得再新增 Pipeline」—— 這條規則最常在數月後被無意破壞，因為新來的人會覺得某個步驟「邏輯上就該接在這之後」。

只有在「外部系統的回應是後續步驟的輸入」時才能放中間，此時必須在 Step 註解寫明原因並實作補償邏輯（補償本身也可能失敗，不在 transaction 保護範圍內）。**優先重排 chain，而不是寫補償。**

### PipelineStep 的三個欄位

| 欄位 | 說明 |
|---|---|
| `make_pipeline` | Pipeline 工廠函式，回傳 Step 清單 |
| `build_ctx` | ctx 建構函式（簽名依位置不同，見下方） |
| `always_run` | 即使前一個 Pipeline 為 StepStop（無 mutation），是否仍強制執行本 Pipeline。適用於稽核日誌等 side-effect |

### build_ctx 的呼叫慣例

`build_ctx` 有兩種簽名，**由 PipelineStep 在清單中的位置決定**：

| 位置 | 簽名 |
|---|---|
| 第一個 Pipeline | `(db, initial_input) → Ctx` |
| 第二個及之後 | `(db, previous_output, mutation_result) → Ctx` |

`mutation_result` 是上一個 Pipeline 的真實寫入結果；若上一個 Pipeline 為 StepStop（無 mutation），則為 null。

⚠️ **這是靠位置約定、而非型別系統強制的。** Chain 是用陣列索引判斷「這是不是第一個」，然後以對應簽名呼叫 `build_ctx`。如果把非第一個位置的 `build_ctx` 寫成第一種簽名，型別檢查**不會報錯**，但執行期會拿到錯的參數。寫 PipelineStep 清單時必須自己確認簽名與位置相符。

### 執行順序重點

每個 Pipeline 的 ctx 都是在**該 Pipeline 即將執行前**，由 Chain 在迴圈內現場呼叫對應的 `build_ctx` 建構出來的。Chain 不會預先建好一整串 ctx，也不會在上一步結束時「提前」建構下一步的 ctx。

---

## 跨語言差異：Transaction 邊界

這是兩種語言在**結構上**唯一不同的地方（其餘都只是語法差異），寫程式前務必確認：

| | TypeScript | Python（SQLAlchemy） |
|---|---|---|
| transaction 物件 | `db.beginTransaction()` 回傳獨立的 `tx` 物件 | `AsyncSession` 本身就是 unit of work，沒有獨立 tx 物件 |
| 寫入入口簽名 | `executeMutation(db, mutation, tx?)` | `execute_mutation(session, mutation)`（**沒有 tx 參數**） |
| Atomic 成功時 | 明確呼叫 `tx.commit()` | 離開 `async with session.begin()` 自動 commit |
| Atomic 業務拒絕（4xx）| 呼叫 `tx.rollback()` 後直接 return | **必須用例外離開 `async with`** 才會 rollback |

> 🚨 **Python 端的致命陷阱：** 在 `async with session.begin()` 區塊內用 `return` 提前離開，SQLAlchemy 會判定為「正常結束」而執行 **commit**，不是 rollback。這會讓「業務拒絕時應該回滾」的語意徹底反轉，而且沒有任何錯誤訊息。Python 版因此使用一個私有的 `_ChainAbort` 例外來承載提前中止的結果 —— 細節見 `references/python.md`。

**Payload CMS 屬於第三種邊界。** 它的 transaction 是一個 **id**（由 `payload.db.beginTransaction()` 取得），必須透過 `req` 物件同時傳給讀與寫，因此 `executeMutation` 沒有 `tx` 參數（形狀接近 Python 版），但提前 `return` 是安全的（沒有 SQLAlchemy 的 commit 陷阱，不要把 `_ChainAbort` 搬過去）。完整說明見 `references/payload-cms.md`。

**Cloudflare Workers 的邊界取決於資料庫，而且一個專案只能選一個。**

| | Hyperdrive + Postgres（預設） | D1 | Durable Objects |
|---|---|---|---|
| Atomic Chain | ✅ 同 TypeScript 版（顯式 `BEGIN`／`COMMIT`／`ROLLBACK`，提前 `return` 安全） | ❌ **不存在**，`runAtomicChain` 不匯出 | — |
| Batch Chain | —（用 Atomic 即可） | ✅ 有限制：後續 Pipeline 讀不到前面的寫入、無讀後寫保護、只能有 `database` target | — |
| Sequential Chain | ✅ | ✅（套用寫入與 result log 放同一個 `batch()`） | — |
| 定位 | 預設 | 規劃時確認沒有讀後寫、沒有「寫入 + 外部呼叫」一起成敗的需求才可使用 | 不作為寫入目標 |

> 🚨 **D1 沒有互動式 transaction。** agent 撞到這點時最常見的「修法」是把 transaction 拿掉，Atomic Chain 就靜默變成 Sequential。D1 專案需要多筆寫入一起成功時用 Batch Chain；超出 Batch Chain 的限制，代表規劃前提被打破，停下來問人。另外 Hyperdrive 的查詢快取預設開啟，Pipeline 的讀取必須走關閉快取的設定。完整說明見 `references/cloudflare-workers.md`。

**Flutter 客戶端屬於第四種邊界，而且有兩層。**

| | Flutter（本地資料庫） | Flutter（後端 API） |
|---|---|---|
| transaction 物件 | callback 形式（drift 以 zone 綁定、sqflite 傳入 `Transaction`），折進 `PipelineDb` | 沒有。原子性是**後端 endpoint 的職責** |
| 寫入入口簽名 | `executeMutation(db, mutation)`（**沒有 tx 參數**） | 同左 |
| Atomic 成功時 | callback 正常結束即 commit | 不適用 |
| Atomic 業務拒絕（4xx） | **必須拋例外離開 callback** 才會 rollback（沿用 Python 版的 `_ChainAbort`） | 後端回 4xx → adapter 丟 `RemoteRejection` → Chain 轉成 4xx 的 `PersistenceResult` |

> 🚨 **drift／sqflite 的 transaction callback 正常結束就 COMMIT**，和 SQLAlchemy 的 `async with` 是同一個陷阱。**不要**把 Payload 版「提前 `return` 是安全的」搬進 Dart。另外 drift 用 zone 綁定 transaction，callback 內**所有**查詢都必須 `await`，否則會在 transaction 關閉後才執行。

> **客戶端的鏈最多一個 `external_api` 寫入，且放最後。** 需要多筆寫入一起成功或失敗時，把它做成一個後端 endpoint，由後端的 Pipeline 負責原子性 —— 不要在客戶端用多個 API 呼叫模擬 transaction。完整說明見 `references/flutter.md`。

---

## 程式碼品質原則

### 不洩漏內部型別

每一層只暴露自己定義的型別。ORM model、DB row、第三方 API response 不能直接穿透層邊界傳給上層。

- Route 邊界：不回傳 ORM model，轉成 Response schema
- Query → Step 邊界：Query 回傳的是原始 dict／object，Step 負責轉成 mutation schema 的形狀
- scratch → mutation 邊界：scratch 是內部判斷用的暫存形狀，StepCommit 負責把最終決定轉換成乾淨的 DataMutation，不能讓 scratch 的形狀直接穿透變成 mutation 的欄位

### 函式大小準則

出現以下任一狀況就拆分：

- 超過 **30 行**（不含空行與註解）
- 巢狀超過 **3 層**
- 需要用「然後」才能描述它做的事（代表它做了超過一件事）

一個 Step 只做一件事：驗證是一個 Step，查詢是一個 Step，計算是一個 Step。

### Rule of Three（抽象的時機）

看到重複的程式碼，先忍住。等到**第三次**出現才抽象。過早抽象比重複更難維護。

例外：如果重複的程式碼已經造成 bug（改一處忘了改另一處），不需要等到第三次，立刻抽象。

### 用介面定義測試邊界

當 Step 或 Query 依賴外部系統時，用介面描述依賴的**簽名**（參數型別 + 回傳型別），讓測試可以換成假實作，不需要真實連線。

- TypeScript：`interface` 或 function type alias
- Python：`typing.Protocol` 搭配 `async def __call__`（保留參數名稱，比 `Callable` 更精確）

---

## 目錄結構

兩種語言的層次完全相同，只有檔名慣例與少數目錄名不同：

| 用途 | TypeScript | Python |
|---|---|---|
| HTTP 入口 | `routes/` | `routes/` |
| Orchestrator | `services/` | `services/` |
| Pipeline 宣告 | `pipelines/` | `pipelines/` |
| Step | `steps/{domain}.ts` + `common.ts` + `utils.ts` | `steps/{domain}.py` + `common.py` + `utils.py` |
| Query | `queries/` | `queries/` |
| domain 型別 | `types/` | `schemas/` |
| 共用基礎設施 | `core/` | `core/` |
| 寫入層 | `persistence/` | `persistence/` |
| 測試 | `tests/` | `tests/` |

**steps/ 的三種檔案：**
- `{domain}` — 各 domain 專屬的 steps
- `common` — 跨 domain 共用的 steps（知道 ctx／scratch 介面）
- `utils` — 純工具函式（不知道任何 Step 或 domain 概念，只接受原始值）

**Persistence 結構：** domain 少於 5 種用扁平結構；超過 5 種時加入 `adapters/`（各 target 的寫入實作）+ `repositories/`（各 domain 的具體 SQL／schema）。

**框架已佔用目錄時：** 若基底框架本身就規定了目錄語意（例如 Payload CMS 的 `src/app/`、`src/collections/`），把上述八層集中放進一個獨立目錄（例如 `src/server/`），不要塞進框架保留的目錄，也不要改動框架自己的結構。Payload 的完整配置見 `references/payload-cms.md`。

**Flutter 同理，且名稱有衝突。** Flutter 官方架構的 `ui/`（View、ViewModel）與 `data/`（Repository、Service）維持原樣，本架構的其餘各層集中放進 `lib/domain/pipeline/`，Service 層則對應 `lib/domain/use_cases/`。注意 Flutter 的 `services/` 指的是 API client，**不是**本架構的 Service 層。完整配置見 `references/flutter.md`。

---

## 決策速查表

| 問題 | 答案 |
|---|---|
| 業務邏輯在哪裡？ | Step |
| DB 查詢在哪裡？ | Query |
| 純計算在哪裡？ | Query |
| 跨 domain 共用的 Step 放哪裡？ | `steps/common` |
| 純工具函式放哪裡？ | `steps/utils` |
| 誰決定要寫什麼？ | Step（在 StepCommit 組裝 mutation schema） |
| 誰真正執行寫入？ | Persistence，由 Pipeline Chain 呼叫 |
| 誰決定 Pipeline 之間的串接？ | Service，透過 PipelineStep 清單宣告 |
| 純查詢結束用什麼？ | StepStop（status 200，無 mutation） |
| 業務拒絕用什麼？ | StepStop（status 4xx，無 mutation） |
| 有寫入意圖的終止用什麼？ | StepCommit（status 2xx，有 mutation） |
| 何時用 Atomic Chain？ | 多個寫入必須一起成功或一起失敗（預設選項） |
| 何時用 Sequential Chain？ | 每個 Pipeline 獨立，部分失敗可接受 |
| Atomic Chain 中 Pipeline N+1 看得到 Pipeline N 的寫入嗎？ | ✅ 是（同一個 DB transaction 內可見） |
| Chain 的呼叫端要傳已建好的 Ctx 嗎？ | ❌ 不要。傳 initial input，ctx 由第一個 PipelineStep 的 `build_ctx` 建構 |
| 第一個 Pipeline 的 `build_ctx` 何時被呼叫？ | 由 Chain 在執行第一個 Pipeline 前現場呼叫 |
| `mutation_result.after` 是什麼？ | **真實寫入後的狀態**（含 DB 自動生成欄位），不是意圖中的 after |
| StepContinue 累積的中繼資料叫什麼？ | `scratch`，型別是自由的字典 |
| scratch 和 mutation 是同一份資料嗎？ | ❌ 不是。Engine 不會把 scratch 併入 mutation，StepCommit 必須自己組出完整、乾淨的 DataMutation |
| MutationResult 有 `success` 欄位嗎？ | ❌ 沒有，已移除。失敗一律拋例外 |
| Step 可以宣告 `next_pipeline` 嗎？ | ❌ 不行。串接由 Service 的 PipelineStep 清單決定 |
| Step 可以呼叫另一個 Step 嗎？ | ❌ 不行 |
| Query 可以接收 ctx 或 scratch 嗎？ | ❌ 不行，只接受原始值 |
| Pipeline 可以有條件判斷嗎？ | ❌ 不行，branching 在 Step 裡 |
| Engine 可以為業務修改嗎？ | ❌ 不行，共用基礎設施 |
| 外部 API／裝置寫入也要走 Persistence 嗎？ | ✅ 是，target 設為對應類型 |
| ORM model 可以直接回傳給 Route 嗎？ | ❌ 不行，轉成 Response schema |
| 看到重複程式碼要馬上抽象嗎？ | ❌ 等第三次出現再抽象（除非已造成 bug） |
| 函式超過 30 行怎麼辦？ | 拆分成更小的函式或獨立的 step |
| 外部依賴如何讓測試容易替換？ | 用介面定義簽名，fake 實作注入 |
| （Cloudflare）預設用哪個資料庫？ | Hyperdrive + 外部 Postgres。D1 只在規劃時確認沒有讀後寫、沒有「寫入 + 外部呼叫」一起成敗的需求才可使用 |
| （Cloudflare）資料庫還沒決定怎麼辦？ | 用業務語言問使用者四個問題，見 `cloudflare-workers.md` 的「規劃階段檢查」 |
| （Cloudflare）D1 專案可以用 Atomic Chain 嗎？ | ❌ 沒有。多筆寫入要一起成功時用 `runBatchChain`，不能用 Sequential 代替；超出 Batch Chain 的限制時停下來問人 |
| （Cloudflare）Batch Chain 中 Pipeline N+1 看得到 Pipeline N 的寫入嗎？ | ❌ 看不到。需要的值一律經由 `buildCtx` 從 `mutationResult` 傳入 |
| （Cloudflare）Batch Chain 可以放 `external_api` 嗎？ | ❌ 不行，鏈中只能有 `database` target |
| （Cloudflare）業務資料可以放 Durable Objects 嗎？ | ❌ 本 Skill 未涵蓋，先與維護者確認 |
| （Cloudflare）寫入可以放進 `waitUntil` 嗎？ | ❌ 不行，那是 fire-and-forget |
| （Cloudflare）Pipeline 的 Query 可以走 Hyperdrive 快取嗎？ | ❌ 不行，一律走關閉快取的設定 |
| （Flutter）Route 層是什麼？ | ViewModel 的 Command；View 只呼叫它 |
| （Flutter）ViewModel 可以直接呼叫 Repository 寫入嗎？ | ❌ 不行。讀取可以，寫入一律走 UseCase → Chain → Persistence |
| （Flutter）一條 workflow 怎麼決定寫入模式？ | 問「後端幾小時後才拒絕，能不能接受」；不能就是僅線上。見 `flutter.md` |
| （Flutter）離線寫入怎麼處理？ | 業務資料 + outbox 紀錄寫在同一個本地 transaction，之後由同步 runner 推送 |
| （Flutter）後端回 4xx 怎麼回到 UI？ | adapter 丟 `RemoteRejection` → Chain 轉成 4xx 的 `PersistenceResult`（不是 `Result.error`） |
| （Flutter）Repository 更新快取算 mutation 嗎？ | ❌ 不算。那是讀取端的職責，不走 Pipeline |

---

## 常見錯誤

- ❌ 沒先判斷專案語言就開始寫 → 先看副檔名／設定檔，只讀對應的 reference
- ❌ 在 Payload CMS 專案只讀 `typescript.md` → 必須加讀 `references/payload-cms.md`，否則會漏掉 transaction 傳遞與 hooks 紅線
- ❌ 在 Cloudflare Workers 專案只讀 `typescript.md` → 必須加讀 `references/cloudflare-workers.md`，否則會漏掉資料庫相容性與 Workers 紅線
- ❌ 在 Python 專案用 camelCase 命名（或反之）→ 命名是契約，依語言慣例
- ❌ Service 的入口函式不用統一名稱 → 統一命名，呼叫端 import 時用 `as` 加 domain 名區分
- ❌ 在 Service 手動呼叫 Engine 或 Persistence → 一律使用 Atomic／Sequential Chain
- ❌ 傳已建好的 Ctx 給 Chain → 一律傳 initial input，ctx 由第一個 PipelineStep 的 `build_ctx` 建構
- ❌ 在 Step 裡宣告 `next_pipeline` → Step 不包含此欄位，串接由 Service 決定
- ❌ 在 Step 裡寫 SQL → 移到 Query
- ❌ 在 Query 裡接收 ctx 或 scratch → Query 只接受原始值
- ❌ 在 Pipeline 裡寫條件判斷 → branching 屬於 Step 的決策
- ❌ 在 Step 裡直接執行寫入 → Mutation 只能被宣告，不能在 Step 裡執行
- ❌ 在 Service 裡寫業務邏輯 → Service 只做 Pipeline 鏈宣告與 ctx 建構
- ❌ 用 StepStop 帶 mutation → StepStop 永遠沒有 mutation，有意圖用 StepCommit
- ❌ 把 StepContinue 的中繼資料欄位當成 mutation 使用 → 那是 scratch，和 DataMutation 是不同容器
- ❌ 期待 Engine 把 scratch 自動併入最終 DataMutation → 不會合併，StepCommit 必須自己組出完整、乾淨的 DataMutation
- ❌ 用強制轉型把自由字典塞進 StepCommit 的 mutation → mutation 欄位型別就是 DataMutation，不需要也不允許轉型
- ❌ 跨 domain 共用邏輯放進 domain step 檔案 → 移到 `steps/common`
- ❌ 把純工具函式寫成接收 ctx 的形狀 → 移到 `steps/utils`，只接受原始值
- ❌ 用 `DataMutation.after` 當作下一個 Pipeline 的輸入 → 用 `MutationResult.after`（真實寫入結果）
- ❌ 外部 API 或裝置的寫入繞過 Persistence → 所有寫入都必須有 intent log 和 result log
- ❌ 以為 Atomic Chain 的 rollback 能撤銷外部 API／檔案／裝置的寫入 → 只有 DB 會回滾，其餘副作用已經發生且通常不可逆
- ❌ 把非資料庫寫入的 Pipeline 放在 chain 中間 → 後面任何一個 Pipeline 失敗，那筆副作用就撤不回來
- ❌ 外部呼叫沒有 await → 失敗不會觸發 rollback，chain 照常 commit，不一致且無人知曉
- ❌ 非 `database` 的寫入沒有搭配授權 Step → Persistence 不含業務邏輯，擋不了未授權的寫入
- ❌ `performed_by` 硬編碼成 `"system"` → 必須填真實執行者身分，範例中的字串只是佔位
- ❌ 讓 mutation 動態指定任意檔案路徑或系統變數 → adapter 內要用白名單列舉可寫入目標
- ❌ agent 自行新增會改動主機／裝置／外部系統的 adapter → 屬於技術決策，先與維護者確認
- ❌ ORM model 直接穿透層邊界 → 在邊界明確轉換成該層自己的型別
- ❌ 看到兩個相似的函式就立刻抽象 → 等第三個出現，確認共同結構後再抽象
- ❌ 測試需要真實 DB 連線才能跑 → 用介面 + fake 實作隔離外部依賴
- 🚨 ❌ **（Python 限定）在 `async with session.begin()` 內用 return 提前離開** → 會誤觸發 commit，必須拋例外才會 rollback
- 🚨 ❌ **（Flutter 限定）在本地 transaction 的 callback 內用 return 處理業務拒絕** → 同樣會誤觸發 commit，必須拋 `_ChainAbort`
- 🚨 ❌ **（Cloudflare 限定）D1 撞到沒有 transaction，就把它拿掉讓程式跑起來** → Atomic Chain 靜默變成 Sequential。改用 `runBatchChain`，超出它的限制就停下來問人
- ❌ （Cloudflare）Batch Chain 的後續 Pipeline 重新查詢前面寫入的資料 → 讀不到，Step 會安靜地做出錯的判斷
- ❌ （Cloudflare）資料庫還沒決定就自行選 D1 → 先做規劃階段檢查，由使用者決定
- ❌ （Cloudflare）把寫入放進 `waitUntil` → 等同 fire-and-forget
- ❌ （Cloudflare）Pipeline 的讀取走 Hyperdrive 有快取的設定 → Step 會用舊資料做決策，而且本機測不出來
- ❌ （Cloudflare）把 Cloudflare Workflows 的 `step` 當成本架構的 Step → 兩者無關
- ❌ （Flutter）把 Flutter 的 `services/` 當成本架構的 Service 層 → Service 層在 Flutter 叫 UseCase，放 `domain/use_cases/`
- ❌ （Flutter）ViewModel 直接呼叫 Repository 的寫入方法或自己組 `DataMutation` → 寫入一律走 UseCase → Chain → Persistence
- ❌ （Flutter）在 `domain/pipeline/` 底下 import Flutter，或把 `BuildContext` 放進 ctx → 這層必須是純 Dart
- ❌ （Flutter）把後端的 4xx 當成 `Result.error` → 業務拒絕是回傳值，`Result.error` 只留給系統故障
- ❌ （Flutter）把付款、扣庫存、唯一性宣告做成「離線可用」→ 這些必須是僅線上模式
- ❌ （Flutter）outbox 送的是 `DataMutation`，或沒有 idempotency key → 前者讓客戶端繞過後端規則，後者造成重複建單
- ❌ （Flutter）以為客戶端的授權 Step 就是授權 → 後端必須自己再檢查一次
