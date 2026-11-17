# Pipeline Architecture — Cloudflare Workers 補充參考

> **本檔是補充，不是替代品。**
> 部署在 Cloudflare Workers 的專案要**同時讀** `references/typescript.md`（基礎實作）**與本檔**（Workers 專屬的偏離點與紅線）。
> 兩者衝突時以本檔為準，本檔沒提到的一律照 `typescript.md`。`typescript.md` 範例中的 `DB` 型別一律換成本檔的 `PipelineDb`。
>
> 適用範圍：Cloudflare Workers + Hono 4.x。資料庫限 **Hyperdrive + 外部 Postgres（預設）** 或 **D1**。

---

## 目錄

- [動手前：判斷專案用哪個資料庫](#動手前判斷專案用哪個資料庫)
- [資料庫相容性：為什麼預設 Hyperdrive + Postgres](#資料庫相容性為什麼預設-hyperdrive--postgres)
- [規劃階段檢查：選資料庫前必做](#規劃階段檢查選資料庫前必做)
- [共通：目錄結構與型別](#共通目錄結構與型別)
- [共通：Layer 1 — Route（Hono）](#共通layer-1--routehono)
- [共通：Workers 執行環境的紅線](#共通workers-執行環境的紅線)
- [Hyperdrive + Postgres 版](#hyperdrive--postgres-版)
- [D1 版](#d1-版)
- [常見錯誤](#常見錯誤)

---

## 動手前：判斷專案用哪個資料庫

本架構規定**一個專案只用一個業務資料庫**。看 `wrangler.jsonc`（或 `wrangler.toml`／`wrangler.json`）的 binding：

| wrangler 設定 | 變體 | 要讀的章節 |
|---|---|---|
| 有 `hyperdrive` binding | Hyperdrive + Postgres | 共通章節 + 「Hyperdrive + Postgres 版」 |
| 有 `d1_databases` binding | D1 | 共通章節 + 「D1 版」 |
| 兩者都有 | — | **停下來問維護者**，不要自己猜哪個是業務資料庫 |
| 兩者都沒有 | 尚未決定 | 先做「規劃階段檢查」 |

- `durable_objects` binding **不影響判斷**。Durable Objects 可以用在 WebSocket、限流、協調等用途，但不作為本架構的寫入目標（理由見下一節）。
- 專案的決策準則檔或 ADR 已經指定資料庫時，以其為準。但若指定的內容與本架構不相容（例如指定 DO 存業務資料，或 D1 專案出現 Batch Chain 處理不了的 workflow），要**指出來**，不要靜默照做，也不要靜默改掉。

---

## 資料庫相容性：為什麼預設 Hyperdrive + Postgres

| 資料庫 | 互動式 transaction | Atomic Chain | Batch Chain | Sequential Chain | 本架構的定位 |
|---|---|---|---|---|---|
| **Hyperdrive + 外部 Postgres** | ✅ 有 | ✅ | —（用 Atomic 即可） | ✅ | **預設** |
| **D1** | ❌ 只有 `batch()` | ❌ | ✅ 有限制 | ✅ | 規劃時確認沒有讀後寫、沒有「寫入 + 外部呼叫」一起成敗的需求才可使用 |
| **Durable Objects（SQLite）** | 僅單一實例內，且 callback 必須同步 | — | — | — | **不作為寫入目標** |

**D1 做不到 Atomic Chain。** D1 會拒絕 `BEGIN TRANSACTION`，唯一的原子單位是 `batch()`，而 batch 內的 statement 無法使用前一個 statement 的結果。Atomic Chain 需要「Pipeline 在 transaction 內讀取 → 寫入 → 下一個 Pipeline 讀得到上一個的寫入」，這在 D1 上沒有對應的機制。

D1 能做的是**能力較弱的 Batch Chain**：所有寫入收集到最後一次 `batch()`，一起成功或一起失敗，但後續 Pipeline 讀不到前面的寫入、沒有讀後寫保護、鏈中不能有外部呼叫。細節見「D1 版」的 Batch Chain 一節。

**DO 需要另一整套 Chain。** DO 的 `transactionSync()` 要求 callback 同步完成，但本架構的 Engine 與 Chain 是 async；transaction 範圍只到單一實例；外部呼叫無法放進 transaction；資料也無法跨實例查詢。要支援它等於重寫 Engine、Chain 與外部寫入的規則，本 Skill 目前未涵蓋。**業務資料必須放 DO 時，停下來與維護者確認。**

**預設選 Hyperdrive + Postgres 的理由：** SKILL.md 規定 Atomic Chain 是預設選項，而 Cloudflare 上只有它完整支援；`typescript.md` 的兩種 Chain 也幾乎可以原封不動使用。

> 這是本 Skill 唯一指定技術選型的地方。原因是 Atomic Chain 需要互動式 transaction，這是架構本身的硬性前提，不是偏好。

---

## 規劃階段檢查：選資料庫前必做

**適用時機：** 要在 Cloudflare 上開始一個採用本架構的新專案、資料庫還沒決定；或有人提議把既有專案改成 D1。

使用 AI 開發專案的人不一定知道 transaction 是什麼，所以**要用業務語言問**，不要問「需不需要 transaction」：

1. 有沒有哪個操作是「做到一半失敗就會出問題」的？例如建立帳號時，同時建立預設工作區與預設設定。
2. 有沒有「先檢查、再扣減」的數量？例如庫存、名額、額度、優惠券使用次數。
3. 有沒有「寫入資料」和「呼叫外部服務」必須一起成功或一起失敗的操作？例如建立訂單同時向金流扣款。
4. 就目前的規劃，之後可能加入第 2 或第 3 題那類功能嗎？（換資料庫等於整個專案重做，所以「之後可能會有」也算有。）

**判斷：**

- 第 2、3、4 題任一題回答「有」或「不確定」 → Hyperdrive + Postgres。
- 否則可以用 D1，但仍由使用者決定。第 1 題回答「有」的那些操作用 Batch Chain，其餘用 Sequential Chain。

**要向使用者說明的取捨**（不要只丟結論）：

| | Hyperdrive + Postgres | D1 |
|---|---|---|
| 本架構的支援度 | 完整（Atomic 與 Sequential） | Sequential 與 Batch Chain（沒有讀後寫保護，鏈中不能有外部呼叫） |
| 需要的服務 | 另一個 Postgres 服務商（多一個供應商與月費） | Cloudflare 內建 |
| 日後改變 | 不受影響 | 出現第 2、3 題的需求時要換資料庫 |

**紅線：**

- ❌ 使用者回答前，不得自行選 D1，也不得「先用 D1 寫 prototype 再說」。
- ❌ 不得替使用者回答上面四題。
- ✅ 決定後，把**結論與四題的回答**記進專案的決策紀錄（有 ADR 就寫成 ADR）。之後新增功能時，agent 才能檢查這個前提有沒有被打破。
- ✅ 專案若有 `technical-decision-policy`，資料庫選擇屬於難以回退的決策，照該 Skill 的升級程序處理。

---

## 共通：目錄結構與型別

```
project/
├── wrangler.jsonc
└── src/
    ├── index.ts              # Hono app 入口：只做 middleware 掛載與 app.route() 組裝
    ├── env.ts                # Bindings／Variables 型別
    ├── entrypoints/          # 非 HTTP 入口（Queue consumer、Cron、Cloudflare Workflows），性質等同 Route
    ├── routes/
    ├── services/
    ├── pipelines/
    ├── steps/
    ├── queries/
    ├── types/
    ├── core/
    │   ├── db.ts             # ← PipelineDb adapter，依資料庫變體不同（見各版）
    │   ├── types.ts          # 原樣照抄 typescript.md
    │   ├── engine.ts         # 原樣照抄，不因 Workers 修改
    │   ├── pipeline-chain.ts # Hyperdrive 版照抄；D1 版刪除 runAtomicChain、新增 runBatchChain
    │   ├── exceptions.ts
    │   └── protocols.ts
    └── persistence/
```

```typescript
// src/env.ts
import type { PipelineDb } from "./core/db";

export interface Env {
  // Hyperdrive 版（兩個設定，理由見「查詢快取」）
  HYPERDRIVE: Hyperdrive;                // 有快取：只給不經過 Pipeline 的純顯示讀取
  HYPERDRIVE_CACHE_DISABLED: Hyperdrive; // 無快取：PipelineDb 一律用這個
  // D1 版改成：DB: D1Database;
}

export interface Actor {
  id: string;
  role: string;
}

export type AppEnv = {
  Bindings: Env;
  Variables: { db: PipelineDb; actor: Actor };
};
```

---

## 共通：Layer 1 — Route（Hono）

本節取代 `typescript.md` 的 Express 範例。Route 的規則不變：只做 request 解析與呼叫 Service，不含 if、DB 呼叫、業務判斷。

```typescript
// src/routes/middleware.ts
import { createMiddleware } from "hono/factory";
import { connectPipelineDb } from "../core/db";
import type { AppEnv } from "../env";

/** 每個 request 建立一個 PipelineDb。不可放在模組層級。 */
export const withPipelineDb = createMiddleware<AppEnv>(async (c, next) => {
  c.set("db", await connectPipelineDb(c.env));
  await next();
});
```

```typescript
// src/routes/user-register.ts
import { Hono } from "hono";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";
import type { ContentfulStatusCode } from "hono/utils/http-status";
import { runWorkflow as runUserRegisterWorkflow } from "../services/user-register";
import type { AppEnv } from "../env";

const registerBody = z.object({ email: z.string().min(3), name: z.string().min(1) });

export const userRegisterRoute = new Hono<AppEnv>().post(
  "/users/register",
  zValidator("json", registerBody),
  async (c) => {
    const result = await runUserRegisterWorkflow({
      db: c.var.db,
      body: c.req.valid("json"),
      actor: c.var.actor,
    });
    return c.json({ data: result.output }, result.status as ContentfulStatusCode);
  },
);
```

```typescript
// src/index.ts
import { Hono } from "hono";
import { authenticate } from "./routes/auth";
import { withPipelineDb } from "./routes/middleware";
import { userRegisterRoute } from "./routes/user-register";
import type { AppEnv } from "./env";

const app = new Hono<AppEnv>();
app.use("/api/*", authenticate, withPipelineDb);
app.route("/api", userRegisterRoute);

export default app;
```

```typescript
// src/services/user-register.ts（只列出與 typescript.md 不同的部分）
export async function runWorkflow({
  db,
  body,
  actor,
}: {
  db: PipelineDb;
  body: RegisterInput;
  actor: Actor;
}): Promise<PersistenceResult> {
  return runAtomicChain({ // D1 版改用 runBatchChain（限制見 D1 版）或 runSequentialChain
    db,
    steps: [/* 同 typescript.md */],
    // actor 併入 initialInput → buildCtx 放進 ctx → StepCommit 用它填 performedBy
    initialInput: { ...body, actor },
  });
}
```

**規則：**

- **`PipelineDb` 在 middleware 內每個 request 建立。** Workers 不允許跨 request 的 I/O，放在模組層級的 client 會失效並拋錯。
- **執行期驗證用 validator middleware。** 格式錯誤的 400 由 middleware 回傳，不進 Service。這取代 `typescript.md` 結尾「Express 沒有執行期驗證」那段。
- **業務 4xx 用 `c.json(output, status)` 回傳，不要轉成 `HTTPException`。** 業務拒絕是回傳值，`HTTPException` 只留給系統層錯誤。
- **`as ContentfulStatusCode` 是刻意的。** `c.json` 的 status 型別比 `number` 窄，而 `PersistenceResult.status` 是 `number`，這個斷言不是可以省略的雜訊。
- **`performedBy` 來自 `c.var.actor`**，由認證 middleware 設定，經 initialInput 進入 ctx。

### 非 HTTP 入口

Queue consumer、Cron（`scheduled`）handler、Cloudflare Workflows 的 `run()` 在架構上等同 Route：

- 在 handler 內建立 `PipelineDb`（同樣不可放模組層級），然後呼叫 Service。
- `performedBy` 用明確的工作身分，例如 `cron:daily-settlement`、`queue:order-events`。不可用籠統的 `"system"`。
- 檔案放 `src/entrypoints/`，不要放進 `services/` 或 `steps/`。

---

## 共通：Workers 執行環境的紅線

### 🚨 `waitUntil` 是內建的 fire-and-forget

`c.executionCtx.waitUntil()` 讓工作在回應送出後繼續執行，Workers 的教學常用它發通知、打 webhook。這直接違反 SKILL.md「外部呼叫必須 `await`、禁止 fire-and-forget」：

- ❌ 任何經過 Persistence 的寫入，包含 intent log、result log、`external_api`，都**不得**放進 `waitUntil`。
- ✅ 可以放：不屬於稽核紀錄的觀測資料（例如送出 trace）。

### Cloudflare Queues／Workflows 不由 agent 自行引入

兩者都是「DB commit 之後才觸發」的現成機制，對應 `typescript.md`「未來擴展點：Compensate」的第 2 點。但本架構的既定做法是外部呼叫同步 `await`、放 chain 最後。**要不要改用它們是技術決策，先與維護者確認。**

### 🚨 撞名：Cloudflare Workflows 的 `step` 不是本架構的 Step

Cloudflare Workflows 的 API 有 `WorkflowEntrypoint`、`step.do()`、`step.sleep()`，和本架構的 `runWorkflow`、Step **毫無關係**。

- Cloudflare Workflow 的 `run()` 是入口（等同 Route）：可以在 `step.do()` 裡呼叫本架構的 Service。
- ❌ 不得把 Cloudflare 的 `step` 物件傳進本架構的 Step 或 ctx。
- ❌ 不得把 Cloudflare Workflow 類別放進 `services/` 或 `steps/`。

### `file`／`device` target

Workers 沒有本機檔案系統，`device` 也不適用。寫 R2、KV 雖然是 Cloudflare 自家服務，但**都不在資料庫 transaction 內**：

- 要對應成哪個 target、adapter 怎麼寫，屬於「新增 adapter」的技術決策，先與維護者確認。
- 決定之後，一律比照 `external_api`：放 chain 最後，並在 adapter 內以白名單列舉可寫入的 binding 與 key prefix。

### `Date.now()` 在純運算期間不會前進

Workers 只在 I/O 之後更新時間。Engine 記錄的純計算 Step 的 `durationMs` 會是 0。**這不是 bug，不要修改 Engine**（Engine 是共用基礎設施）。

---

## Hyperdrive + Postgres 版

### 與 typescript.md 的差異速查表

| 項目 | `typescript.md` | Hyperdrive + Postgres |
|---|---|---|
| DB 連線 | 由 middleware 注入 | 每個 request 一個 pg `Client`，連到**無快取**的 Hyperdrive 設定 |
| transaction 物件 | `db.beginTransaction()` 回傳 `tx` | 同左（adapter 在同一個 Client 上下 `BEGIN`／`COMMIT`／`ROLLBACK`） |
| Atomic 業務拒絕（4xx） | `tx.rollback()` 後 `return` | 同左（**提前 return 是安全的**） |
| SQL placeholder | `?` | `$1`、`$2`… |
| DB 自動產生的欄位 | — | 寫入時帶 `RETURNING *`，作為 `MutationResult.after` |
| Pipeline 的讀取 | — | 必須走關閉快取的 Hyperdrive 設定 |

> 🚨 **不要把 Python 版的 `_ChainAbort` 搬過來。** 本版是明確呼叫 `ROLLBACK`，提前 `return` 沒有 commit 陷阱。例外見下方「callback 式 transaction」。

### core/db.ts

```typescript
// src/core/db.ts（Hyperdrive + Postgres 版）
import { Client } from "pg"; // pg 8.13.0 以上
import type { Env } from "../env";

export interface Transaction {
  commit(): Promise<void>;
  rollback(): Promise<void>;
}

export interface PipelineDb {
  fetchOne(sql: string, params: unknown[]): Promise<Record<string, unknown> | null>;
  fetchAll(sql: string, params: unknown[]): Promise<Record<string, unknown>[]>;
  /** 寫入用，回傳 RETURNING 的資料列 */
  execute(sql: string, params: unknown[]): Promise<Record<string, unknown>[]>;
  beginTransaction(): Promise<Transaction>;
}

export async function connectPipelineDb(env: Env): Promise<PipelineDb> {
  // 一律用無快取的設定：Pipeline 的讀取結果會被 Step 拿來做決策。
  const client = new Client({
    connectionString: env.HYPERDRIVE_CACHE_DISABLED.connectionString,
  });
  await client.connect();
  // 不需要 client.end()：request 結束時 Workers 會自動清理連線。

  let inTransaction = false;
  const rows = async (sql: string, params: unknown[]) =>
    (await client.query(sql, params)).rows as Record<string, unknown>[];

  return {
    fetchOne: async (sql, params) => (await rows(sql, params))[0] ?? null,
    fetchAll: rows,
    execute: rows,
    async beginTransaction() {
      if (inTransaction) {
        throw new Error("同一個 request 只能有一條 Atomic Chain 在執行");
      }
      await client.query("BEGIN");
      inTransaction = true;
      return {
        async commit() {
          await client.query("COMMIT");
          inTransaction = false;
        },
        async rollback() {
          await client.query("ROLLBACK");
          inTransaction = false;
        },
      };
    },
  };
}
```

**同一個 request 共用一個 Client** 是這個 adapter 的關鍵：Atomic Chain 期間，Query 與 Persistence 走同一條連線、落在同一個 transaction 內，「Pipeline N+1 看得到 Pipeline N 的寫入」才會成立。

- `pipeline-chain.ts` 照抄 `typescript.md`，不需要改。`executeMutation` 的 `tx` 參數保留以符合原簽名；寫入是否在 transaction 內由共用的 Client 決定。
- ❌ 不要在同一個 request 內用 `Promise.all` 同時跑兩條 chain：它們共用一個 Client，statement 會交錯進同一個 transaction。

### 🚨 driver 或 ORM 只提供 callback 式 transaction 時

postgres.js 的 `sql.begin(async (sql) => …)`、Drizzle 的 `db.transaction(async (tx) => …)` 都是 callback 式：**callback 正常結束就 COMMIT**。如果把 Chain 包進這類 callback，業務拒絕時用 `return` 離開，會變成 commit —— 和 Python `async with`、Flutter drift 是同一個陷阱，而且沒有錯誤訊息。

- Chain 一律維持 `typescript.md` 的顯式寫法，由 adapter 提供 `BEGIN`／`COMMIT`／`ROLLBACK`（上面的 pg `Client` 可以直接做到）。
- 專案選用的 driver 做不到時，停下來與維護者確認。**不要自行把 Chain 改寫成 callback 式。**

### 🚨 查詢快取：Pipeline 一律走無快取設定

Hyperdrive 的查詢快取**預設開啟**：唯讀查詢會被快取 60 秒，過期後還會再提供最多 15 秒的舊資料；應用程式寫入資料庫時，快取**不會**失效。

對本架構的影響：Step 依據 Query 的結果做決策。`checkEmailNotTaken` 若讀到快取，可能在使用者剛註冊完的一分鐘內判斷「Email 沒被用過」。更麻煩的是，本機 `wrangler dev` 使用 `localConnectionString` 時**不會啟用快取**，這類 bug 開發時看不到，上線才出現。

**規則：Pipeline 裡的讀寫一律走關閉快取的設定；快取只給不經過 Pipeline 的純顯示讀取。** SKILL.md 本來就規定純顯示讀取不走 Pipeline，兩者剛好對齊。

```sh
# 同一個資料庫建兩個設定
npx wrangler hyperdrive create my-db       --connection-string="postgres://..."
npx wrangler hyperdrive create my-db-fresh --connection-string="postgres://..." --caching-disabled
```

```jsonc
// wrangler.jsonc
{
  "hyperdrive": [
    { "binding": "HYPERDRIVE", "id": "<有快取的設定 id>" },
    { "binding": "HYPERDRIVE_CACHE_DISABLED", "id": "<無快取的設定 id>" }
  ]
}
```

- 兩個設定連到同一個資料庫時，連線數要合計計算，不要各自設到資料庫上限。
- ❌ 不要用 SQL 註解、`NOW()` 之類的寫法「騙過」快取。要新鮮資料就走無快取設定。

### 🚨 讀後寫：開了 transaction 不等於安全

Postgres 預設的隔離等級是 READ COMMITTED。在 Atomic Chain 裡，Step 讀到的庫存在寫入之前**仍然可能被別的 request 改掉**，transaction 本身不會阻止這件事。

後續寫入依賴的讀取（庫存、名額、額度、餘額），Query 要加 `FOR UPDATE` 鎖住該列，直到 transaction 結束：

```typescript
// src/queries/inventory.ts
/** 會鎖列。只能在 Atomic Chain 內使用，否則鎖會立刻釋放、沒有意義。 */
export async function queryStockForUpdate(db: PipelineDb, productId: string) {
  return db.fetchOne("SELECT id, stock FROM products WHERE id = $1 FOR UPDATE", [productId]);
}
```

- `FOR UPDATE` 仍然是讀取，符合 Query 的職責；判斷邏輯留在 Step，Step 看到的值在 commit 前都有效。
- 會鎖列的 Query 以 `ForUpdate` 結尾命名，讓人一眼看出它只能用在 Atomic Chain。
- ❌ 不要改成在 Persistence 寫條件式 SQL（`WHERE stock >= $1`）來解決 —— 那會把業務判斷搬進 Persistence。

### 🚨 連線池：Atomic Chain 要短

Hyperdrive 採 transaction 模式的連線池：連線會被佔用到 transaction 結束。Cloudflare 建議 transaction 越短越好，並避免在 transaction 內呼叫外部 API。

這和 SKILL.md 的規則有張力：`external_api` 的 Pipeline 放在 Atomic Chain 最後、在 transaction 內 `await`，目的是讓外部呼叫失敗時 DB 能乾淨回滾。本檔**維持這條既定規則**，但加上以下要求：

1. **所有外部呼叫一律設逾時**，例如 `fetch(url, { signal: AbortSignal.timeout(5_000) })`。逾時就 throw、觸發 rollback。不設逾時的話，外部服務一卡住，連線就一直被佔住。
2. **Atomic Chain 內呼叫外部 API 的 Query 也會延長 transaction。** 能避免就避免；必須保留時在 Step 註解說明原因。
3. **尖峰時出現連線不足的錯誤，是該重新評估 outbox 的訊號。** 這屬於技術決策，向維護者提出，不要自行改架構。

### Persistence：database adapter

```typescript
// src/persistence/adapters/database.ts（節錄 create；update／delete 同理）
export async function applyDbMutation(
  db: PipelineDb,
  mutation: DataMutation,
  _tx?: Transaction,
): Promise<[Record<string, unknown> | null, Record<string, unknown> | null]> {
  const repo = resolveRepository(mutation.entity); // 白名單，未註冊就 throw
  if (mutation.operation === "create") {
    const [row] = await db.execute(repo.insertSql, repo.insertParams(mutation.after!));
    return [null, row]; // RETURNING * 的結果：含 id、created_at 等資料庫產生的欄位
  }
  // update：先 SELECT 取得 before，再 UPDATE ... RETURNING *
  // delete：DELETE ... RETURNING * 的結果即為 before，after 為 null
  throw new Error(`尚未實作的 operation: ${mutation.operation}`);
}
```

`MutationResult.after` 必須是 `RETURNING *` 的結果，不能用 `mutation.after` 代替 —— 這是 SKILL.md「真實寫入後的狀態」在 Postgres 上的實作方式。

---

## D1 版

### 與 typescript.md 的差異速查表

| 項目 | `typescript.md` | D1 |
|---|---|---|
| Atomic Chain | 有（預設選項） | **不存在**：`pipeline-chain.ts` 刪除 `runAtomicChain`，改用能力較弱的 `runBatchChain` |
| 寫入執行的時機 | StepCommit 後立即執行 | Sequential：立即；Batch Chain：整條鏈跑完才一次 `batch()` |
| transaction 物件 | `db.beginTransaction()` | 無，`PipelineDb` 刻意不提供 |
| 寫入入口簽名 | `executeMutation(db, mutation, tx?)` | `executeMutation(db, mutation)` |
| 套用寫入與 result log | 兩次獨立寫入 | **同一個 `batch()`**，中間夾一個守門 statement |
| 資料庫產生的欄位 | 可以依賴 | **禁止依賴**：id、時間戳由 adapter 產生 |
| SQL placeholder | `?` | `?`（相同） |

### 為什麼刪除 runAtomicChain，而不是讓它拋錯

`PipelineStep` 型別與 `runSequentialChain` 照抄 `typescript.md`（它本來就以 `executeMutation(db, mutation)` 呼叫，不帶 `tx`）。刪除 `runAtomicChain`，新增 `runBatchChain`（見下方 Batch Chain 一節）。

最危險的失敗方式是 agent 撞到「D1 沒有 transaction」之後，把 transaction 拿掉讓程式跑起來 —— Atomic Chain 就靜默變成 Sequential，業務拒絕時前面的寫入不會回滾，而且沒有任何錯誤訊息。

`core/pipeline-chain.ts` 不匯出 `runAtomicChain`，誤用會在**編譯期**失敗，而不是在稽核時才被發現。

**D1 專案需要多筆寫入一起成功或失敗時：** 先檢查能不能用 Batch Chain。三條限制都符合就用它；需要讀後寫保護、外部呼叫，或後續 Pipeline 必須讀到前面的寫入時，代表規劃階段的前提被打破了，停下來向維護者說明，由人決定是否改用 Hyperdrive + Postgres。

- ❌ 不得改用 Sequential Chain 代替。
- ❌ 不得臨時用 `batch()` 拼湊其他形式的原子寫入，只能用規範好的 `runBatchChain`。
- ❌ 不得在 Persistence 寫條件式 SQL 來補讀後寫的保護。

### core/db.ts

```typescript
// src/core/db.ts（D1 版）
import type { Env } from "../env";

export interface Statement {
  sql: string;
  params: unknown[];
}

export interface PipelineDb {
  fetchOne(sql: string, params: unknown[]): Promise<Record<string, unknown> | null>;
  fetchAll(sql: string, params: unknown[]): Promise<Record<string, unknown>[]>;
  /** 單一寫入（intent log、非 database target 的 result log）。Query 不得使用 */
  execute(sql: string, params: unknown[]): Promise<D1Result>;
  /** 原子執行：任一 statement 失敗，整批回滾 */
  batch(statements: Statement[]): Promise<D1Result[]>;
  // 刻意沒有 beginTransaction：D1 不支援互動式 transaction
}

export async function connectPipelineDb(env: Env): Promise<PipelineDb> {
  const d1 = env.DB;
  return {
    fetchOne: (sql, params) =>
      d1.prepare(sql).bind(...params).first<Record<string, unknown>>(),
    fetchAll: async (sql, params) =>
      (await d1.prepare(sql).bind(...params).all<Record<string, unknown>>()).results,
    execute: (sql, params) => d1.prepare(sql).bind(...params).run(),
    batch: (statements) =>
      d1.batch(statements.map((s) => d1.prepare(s.sql).bind(...s.params))),
  };
}
```

### Persistence：intent log 先寫，套用與 result log 同一個 batch

Sequential 與 Batch Chain 共用同一個編譯函式：`compileDbMutation` 寫入 intent log，並把 mutation 編譯成三個 statement，**但不執行**。

```typescript
// src/persistence/index.ts（D1 版）
export interface CompiledMutation {
  statements: Statement[]; // [套用, 守門, result log]
  result: MutationResult;  // after 是 adapter 組出的完整資料列
}

export async function compileDbMutation(
  db: PipelineDb,
  mutation: DataMutation,
): Promise<CompiledMutation> {
  if (mutation.target !== "database") {
    throw new Error(`只能編譯 database target，收到 ${mutation.target}`);
  }

  const intentLogId = crypto.randomUUID();
  await logIntent(db, intentLogId, mutation); // 單獨寫入，先於一切

  // 讀取 before，並由 repository 組出完整資料列（含 adapter 產生的 id、時間戳）
  const plan = await planDbMutation(db, mutation); // { before, after, statement }
  const diff = computeDiff(plan.before, plan.after);
  const resultLogId = crypto.randomUUID();

  return {
    statements: [
      plan.statement,
      // 守門：上一個 statement 沒有影響任何列時，這裡會插入 ok = 0，
      // 違反 CHECK 約束 → 整個 batch 回滾。影響到列時什麼都不插入。
      { sql: "INSERT INTO pipeline_batch_guard (ok) SELECT 0 WHERE changes() = 0", params: [] },
      {
        sql: `INSERT INTO mutation_results (result_id, intent_id, before, after, diff)
              VALUES (?, ?, ?, ?, ?)`,
        params: [
          resultLogId,
          intentLogId,
          JSON.stringify(plan.before),
          JSON.stringify(plan.after),
          JSON.stringify(diff),
        ],
      },
    ],
    result: { before: plan.before, after: plan.after, diff, intentLogId, resultLogId },
  };
}

/** Sequential Chain 用：編譯後立即執行。 */
export async function executeMutation(
  db: PipelineDb,
  mutation: DataMutation,
): Promise<MutationResult> {
  if (mutation.target !== "database") {
    return executeNonDbMutation(db, mutation); // 同 typescript.md：intent → 套用 → result
  }
  const compiled = await compileDbMutation(db, mutation);
  await db.batch(compiled.statements);
  return compiled.result;
}
```

```sql
-- migrations：守門表。永遠是空的 —— 只有守門失敗時才會嘗試插入，而那次插入必定違反 CHECK。
CREATE TABLE pipeline_batch_guard (ok INTEGER NOT NULL CHECK (ok = 1));
```

- **intent log 單獨先寫**：寫入失敗、被拒絕或 batch 回滾時，「有人打算做這件事」的紀錄仍然留著。
- **套用與 result log 在同一個 batch**：兩者一起成功或一起失敗，「有 result log = 真的寫入了」才會成立。
- **守門 statement 讓「影響 0 列」變成失敗**：SQLite 的 UPDATE／DELETE 沒有命中任何列時不算錯誤，batch 不會自己回滾。守門依賴 batch 內的 statement 依序在同一個 transaction 中執行（D1 文件保證依序、非併發）。導入時先在本機寫一個「套用影響 0 列」的測試，確認整個 batch 會回滾。

### Batch Chain：多筆寫入一起成功或失敗

Batch Chain 是 D1 上**能力較弱的原子寫入**：每個 Pipeline 的 StepCommit 照常產生 DataMutation，但 Persistence 只編譯、不執行；整條鏈跑完才一次送出 `batch()`。

| Atomic Chain 的承諾 | Atomic Chain（Postgres） | Batch Chain（D1） |
|---|---|---|
| 所有寫入一起成功或失敗 | ✅ | ✅ |
| 業務拒絕時不留下寫入 | ✅ rollback | ✅ 不送出 batch（提前 return 安全） |
| Pipeline N+1 的 Query 看得到 Pipeline N 的寫入 | ✅ | ❌ 寫入到最後才執行 |
| `mutationResult.after` 是真實寫入結果 | ✅ `RETURNING *` | ⚠️ adapter 組出的資料列（見「禁止依賴資料庫產生的欄位」） |
| 讀後寫的保護 | ✅ `FOR UPDATE` | ❌ 讀取在 batch 之外 |
| `external_api` 放鏈尾、失敗時 DB 回滾 | ✅ | ❌ 不能放進鏈 |

**三條限制，全部符合才能用 Batch Chain：**

1. **後續 Pipeline 的 Query 不得讀取前面 Pipeline 的寫入。** 需要的資料（例如剛建立的 id）一律經由 `buildCtx` 從 `mutationResult` 傳入。這是最危險的一條：違反時不會報錯，Step 只會安靜地根據舊資料做出錯的判斷。同理，**同一條鏈內不得對前面剛建立或修改的同一筆資料再做 update／delete** —— Persistence 讀取 `before` 時一樣讀不到。
2. **不得有讀後寫。** 庫存、名額、額度、餘額這類「先檢查再扣減」的流程，在 D1 上沒有保護。
3. **鏈中只能有 `database` target。** 約束錯誤（例如 Email 重複）要到最後送出 batch 時才會出現，外部呼叫若放在鏈中，會在 DB 失敗之前就已經發生。外部呼叫只能在 batch 成功之後另外執行，而「那之後外部呼叫失敗怎麼辦」本 Skill 尚未定案，出現這種需求時停下來問人。

**為什麼不沿用 `runAtomicChain` 這個名稱：** agent 看到 `runAtomicChain`，就會認定 SKILL.md 決策速查表裡的承諾都成立（包含「Pipeline N+1 看得到 Pipeline N 的寫入」）。同名但語意較弱，等於換個形式的靜默退化。

在 Service 使用 Batch Chain 時，加註解讓後來的人看得到限制：

```typescript
// src/services/account-create.ts
// ⚠️ Batch Chain：所有寫入在最後一次送出。
//    後續 Pipeline 不得查詢前面 Pipeline 寫入的資料，需要的值只能從 mutationResult 取得；
//    不得加入 external_api 或讀後寫的 Pipeline。
return runBatchChain({
  db,
  steps: [
    { makePipeline: makeUserCreatePipeline, buildCtx: /* ... */ },
    { makePipeline: makeWorkspaceCreatePipeline, buildCtx: /* 從 mutationResult.after 取 userId */ },
    { makePipeline: makeDefaultSettingsPipeline, buildCtx: /* 同上 */ },
  ],
  initialInput: { ...body, actor },
});
```

```typescript
// src/core/pipeline-chain.ts（D1 版，新增）
import { PipelineEngine } from "./engine";
import { compileDbMutation } from "../persistence";
import type { PipelineDb, Statement } from "./db";
import type { MutationResult, PersistenceResult, TraceSpan } from "./types";

export async function runBatchChain<TInput>({
  db,
  steps,
  initialInput,
}: {
  db: PipelineDb;
  steps: PipelineStep[];
  initialInput: TInput;
}): Promise<PersistenceResult> {
  const engine = new PipelineEngine();
  const allSpans: TraceSpan[] = [];
  const pending: Statement[] = [];
  let lastOutput: unknown = null;
  let lastStatus: number | null = null;
  let lastMutationResult: MutationResult | null = null;

  for (let i = 0; i < steps.length; i++) {
    const step = steps[i];
    const isFirst = i === 0;

    if (!isFirst && lastMutationResult === null && !step.alwaysRun) {
      continue;
    }

    const currentCtx = isFirst
      ? (step.buildCtx as FirstBuildCtxFn<TInput>)(db, initialInput)
      : (step.buildCtx as NextBuildCtxFn)(db, lastOutput, lastMutationResult);

    const result = await engine.execute(step.makePipeline(db), currentCtx);
    allSpans.push(...result.spans);
    lastOutput = result.output;
    lastStatus = result.status;

    if (!result.mutation) {
      if (result.status >= 400) {
        // 業務拒絕：丟掉收集到的 statement，什麼都不寫（intent log 已各自留下）
        return { output: result.output, status: result.status, spans: allSpans, mutationResult: null };
      }
      continue;
    }

    // 只編譯、不執行。compileDbMutation 遇到非 database target 會直接 throw。
    const compiled = await compileDbMutation(db, result.mutation);
    pending.push(...compiled.statements);
    lastMutationResult = compiled.result;
  }

  // 唯一的實際寫入點：任一 statement 失敗（含守門），整批回滾並 throw
  if (pending.length > 0) {
    await db.batch(pending);
  }

  return {
    output: lastOutput,
    status: lastStatus ?? 200,
    spans: allSpans,
    mutationResult: lastMutationResult,
  };
}
```

### 🚨 禁止依賴資料庫產生的欄位

D1 版的 `MutationResult.after` 是 adapter 在寫入前組出的完整資料列。它要等同 SKILL.md 所說的「真實寫入後的狀態」，前提是資料庫不會再自己加東西：

- id 由 adapter 用 `crypto.randomUUID()` 產生，不用 `AUTOINCREMENT`。
- 時間戳由 adapter 產生，不用 `DEFAULT CURRENT_TIMESTAMP`。
- Pipeline 會寫入的資料表不得有 trigger。

Step 仍然不產生 id 或時間戳，這些由 Persistence 的 adapter 負責，Step 維持純粹的決策與形狀對映。

---

## 常見錯誤

- ❌ 沒看 wrangler 設定就開始寫 → 先判斷是 Hyperdrive 版還是 D1 版，兩者的 `core/db.ts` 與 Persistence 不同
- ❌ 資料庫還沒決定就自行選 D1，或先用 D1 寫 prototype → 先做規劃階段檢查，由使用者決定
- ❌ 用「需不需要 transaction」問使用者 → 用業務語言問四個問題
- ❌ 把業務資料放進 Durable Objects → 本 Skill 未涵蓋，先與維護者確認
- ❌ 把 `PipelineDb` 或 pg client 放在模組層級 → Workers 不允許跨 request 的 I/O，會失效並拋錯
- ❌ 業務 4xx 丟 `HTTPException` → 用 `c.json(output, status)` 回傳
- ❌ 把寫入（含 intent／result log）放進 `waitUntil` → 等同 fire-and-forget
- ❌ agent 自行引入 Cloudflare Queues 或 Workflows 取代同步呼叫 → 技術決策，先與維護者確認
- ❌ 把 Cloudflare Workflows 的 `step` 傳進本架構的 Step → 兩者無關
- ❌ `performedBy` 在 Cron 或 Queue 入口填 `"system"` → 用明確的工作身分，例如 `cron:<job 名稱>`
- ❌ 以為純計算 Step 的 `durationMs` 為 0 是 bug 而去改 Engine → Workers 的時間只在 I/O 後前進
- ❌ （Hyperdrive）Pipeline 的讀取走有快取的設定 → Step 會用最多 75 秒前的資料做決策，而且本機測不出來
- ❌ （Hyperdrive）把 Chain 包進 `sql.begin()` 或 `db.transaction()` 的 callback → 業務拒絕的 `return` 會變成 commit
- ❌ （Hyperdrive）以為開了 transaction 讀後寫就安全 → 依賴的讀取要用 `FOR UPDATE`
- ❌ （Hyperdrive）外部呼叫不設逾時 → 外部服務一卡住，Hyperdrive 的連線就一直被佔住
- ❌ （Hyperdrive）用 `mutation.after` 當 `MutationResult.after` → 用 `RETURNING *` 的結果
- ❌ （D1）撞到沒有 transaction 就把它拿掉讓程式跑起來 → Atomic Chain 靜默變成 Sequential
- ❌ （D1）需要多筆寫入一起成功時改用 Sequential，或臨時用 `batch()` 拼湊 → 用規範好的 `runBatchChain`；超出它的限制就停下來問人
- ❌ （D1）把 `runBatchChain` 改名成 `runAtomicChain` → 語意較弱卻沿用強承諾的名稱，是另一種靜默退化
- ❌ （D1）Batch Chain 的後續 Pipeline 重新查詢前面寫入的資料 → 讀不到，Step 會安靜地做出錯的判斷
- ❌ （D1）在 Batch Chain 放 `external_api`、讀後寫的 Pipeline → 違反 Batch Chain 的限制
- ❌ （D1）拿掉守門 statement → 「影響 0 列」不會讓 batch 失敗，其他寫入照常 commit
- ❌ （D1）result log 與套用寫入分開執行 → 放進同一個 `batch()`
- ❌ （D1）資料表依賴 `AUTOINCREMENT`、`DEFAULT` 或 trigger → `MutationResult.after` 會與真實狀態不一致
