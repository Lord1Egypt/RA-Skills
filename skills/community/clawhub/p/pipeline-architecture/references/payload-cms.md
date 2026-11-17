# Pipeline Architecture — Payload CMS 補充參考

> **本檔是補充，不是替代品。**
> Payload 專案要**同時讀** `references/typescript.md`（基礎實作）**與本檔**（Payload 專屬的偏離點與紅線）。
> 兩者衝突時以本檔為準，本檔沒提到的一律照 `typescript.md`。
>
> 適用版本：**Payload 3.x**。4.0 仍在 beta，本檔未涵蓋。

---

## 目錄

- [套用前必須先決定的事](#套用前必須先決定的事)
- [與 typescript.md 的差異速查表](#與-typescriptmd-的差異速查表)
- [目錄結構](#目錄結構)
- [層對應表](#層對應表)
- [core/payload-context.ts](#corepayload-contextts)
- [Layer 1 — Route（Payload custom endpoint）](#layer-1--routepayload-custom-endpoint)
- [Layer 2 — Service](#layer-2--service)
- [Layer 3 — Pipeline Chain（Payload transaction）](#layer-3--pipeline-chainpayload-transaction)
- [Layer 4／5 — Pipeline 與 Engine](#layer-45--pipeline-與-engine)
- [Layer 6 — Step](#layer-6--step)
- [Layer 7 — Query](#layer-7--query)
- [Layer 8 — Persistence](#layer-8--persistence)
- [稽核 log 的 collection](#稽核-log-的-collection)
- [Collection Hooks 的紅線](#collection-hooks-的紅線)
- [外部呼叫：同步 await，放 chain 最後](#外部呼叫同步-await放-chain-最後)
- [Payload 專屬注意事項](#payload-專屬注意事項)
- [常見錯誤](#常見錯誤)

---

## 套用前必須先決定的事

Payload 有**兩條寫入路徑**，本架構只能管住其中一條：

| 路徑 | 流程 | 是否經過 Pipeline |
|---|---|---|
| **A** | custom endpoint → Service → Chain → Persistence → Local API | ✅ 是 |
| **B** | Admin 後台／Payload 內建 REST／GraphQL → Local API | ❌ 完全繞過 |

如果業務規則只寫在 Step 裡，路徑 B 會整條繞過它們。**這不是可以事後補的問題，是套用架構前就要拍板的事。**

### 建議：分層對待 collection，不要全站套用

| Collection 類型 | 做法 |
|---|---|
| 內容型（Pages、Media、Posts、Categories） | **不套架構。** 用 Payload 原生 hooks／access 即可。這類編輯行為不是「先決策後執行」的 workflow，硬套只會製造樣板 |
| 業務型（Orders、Subscriptions、Ledger、Entitlements） | **套架構**，並在 collection 的 `access` 關掉後台的 create／update／delete，強制走路徑 A |

### 第三種選擇（屬於偏離，要先跟維護者確認）

在 `beforeChange` 掛一條「守衛 pipeline」，讓兩條路徑共用規則。這條 pipeline **只能回傳 `StepContinue` 或 `StepStop`**，永遠不會產生 `StepCommit`，實際寫入由 Payload 自己執行。

代價是該次寫入**沒有 intent log**，稽核鏈會斷。要用的話必須明確告知維護者這個取捨，不要靜默採用。

---

## 與 typescript.md 的差異速查表

| 項目 | `typescript.md` | Payload |
|---|---|---|
| `DB` 型別 | 資料庫連線物件 | `PipelineDb`（Payload instance + user + transactionID） |
| transaction 物件 | `db.beginTransaction()` 回傳獨立 `tx` | `payload.db.beginTransaction()` 回傳 **transaction id**（`string \| number \| null`） |
| transaction 如何傳遞 | 只傳給 `executeMutation` | **折進 `db`**，Query 與 Persistence 都必須帶上 |
| 寫入入口簽名 | `executeMutation(db, mutation, tx?)` | `executeMutation(db, mutation)`（**沒有 tx 參數**，同 Python 版） |
| Atomic 業務拒絕（4xx） | `tx.rollback()` 後 `return` | `payload.db.rollbackTransaction(id)` 後 `return`（**提前 return 是安全的**） |
| Route 授權 | middleware | **custom endpoint 不套 access control**，授權 Step 為必要 |
| 寫入實作 | 手寫 SQL／ORM | Payload Local API（`payload.create／update／delete`） |
| ORM model | 自行定義 | `payload-types.ts` 自動生成 |

> 🚨 **不要把 Python 版的 `_ChainAbort` 例外搬過來。** 那是為了繞過 SQLAlchemy `async with` 內 `return` 會誤觸 commit 的陷阱。Payload 是明確呼叫 `rollbackTransaction`，提前 `return` 沒有這個問題。

---

## 目錄結構

```
src/
├── payload.config.ts
├── payload-types.ts              # 自動生成 → 視同 ORM model，不得穿透層邊界
├── collections/                  # Payload schema 定義（= DB schema，不是架構的一層）
│   ├── Orders.ts                 # endpoints 欄位引用 server/routes/ 的 handler
│   ├── Users.ts
│   └── audit/
│       ├── MutationIntents.ts    # intent log
│       └── MutationResults.ts    # result log
├── app/
│   ├── (payload)/                # Payload 自帶，不要動
│   └── (frontend)/
└── server/                       # ← 架構的八層全部住這裡
    ├── core/
    │   ├── types.ts              # 原樣照抄 typescript.md
    │   ├── engine.ts             # 原樣照抄，不因 Payload 修改
    │   ├── pipeline-chain.ts     # ← 唯一需要為 Payload 改寫的 core 檔案
    │   ├── exceptions.ts
    │   ├── protocols.ts
    │   └── payload-context.ts    # ← Payload 專屬新增
    ├── routes/
    │   └── order-submit.ts       # PayloadHandler，薄層
    ├── services/
    │   └── order-submit.ts       # runWorkflow
    ├── pipelines/
    │   └── order-submit.ts       # makePipeline
    ├── steps/
    │   ├── order-submit.ts
    │   ├── common.ts             # 權限檢查住這裡（必要，見 Layer 1）
    │   └── utils.ts
    ├── queries/
    │   └── order.ts              # payload.find／findByID，唯讀
    ├── types/
    │   └── order-submit.ts
    └── persistence/
        ├── index.ts              # executeMutation
        ├── adapters/
        │   ├── database.ts       # Payload Local API 寫入
        │   ├── external-api.ts
        │   └── file.ts
        ├── repositories/
        │   ├── index.ts          # entity → repository 的白名單註冊表
        │   └── order.ts
        └── audit-log.ts
```

**為什麼 `server/` 放在 `src/app/` 之外：** App Router 目錄有路由語意，把非路由檔案塞進去只會增加誤解與意外暴露的風險。`collections/` 則維持 Payload 原生位置不動。

---

## 層對應表

| 架構層 | Payload 對應物 | 放在哪裡 |
|---|---|---|
| Route | Collection `endpoints` 的 `PayloadHandler` | `server/routes/` + `collections/*.ts` 的 `endpoints` 欄位 |
| Service | 純 TypeScript 函式 | `server/services/` |
| Pipeline Chain | 純 TypeScript + `payload.db.*Transaction` | `server/core/pipeline-chain.ts` |
| Pipeline | 純 TypeScript 函式 | `server/pipelines/` |
| Engine | 純 TypeScript class（Payload 無關） | `server/core/engine.ts` |
| Step | 純 TypeScript 函式（Payload 無關） | `server/steps/` |
| Query | `payload.find` / `payload.findByID` | `server/queries/` |
| Persistence | `payload.create` / `update` / `delete` | `server/persistence/` |
| （非本架構的層） | Collection schema 定義 | `src/collections/` |

**Engine 與 Step 完全不認識 Payload。** 它們只透過 `PipelineDb` 這個介面接觸外界，這也是測試能不啟動 Payload 就跑起來的原因。

---

## core/payload-context.ts

```typescript
// server/core/payload-context.ts
import type { Payload, PayloadRequest } from 'payload'

/**
 * 對應 typescript.md 中的 DB。所有層透過它接觸 Payload。
 *
 * transactionID 折進本物件（而非像 typescript.md 那樣當獨立參數），
 * 原因是 Payload 靠 req 物件把 transaction id 傳給 database adapter，
 * Query 也必須帶上同一個 id，否則後續 Pipeline 讀不到前面 Pipeline
 * 尚未 commit 的寫入 —— SKILL.md 的
 * 「Atomic Chain 中 Pipeline N+1 看得到 Pipeline N 的寫入」會失效。
 */
export interface PipelineDb {
  readonly payload: Payload
  /** 目前執行者，供 DataMutation.performedBy 與版本紀錄歸屬使用 */
  readonly user: PayloadRequest['user']
  /** Atomic Chain 進行中才有值；Sequential Chain 為 undefined */
  readonly transactionID?: number | string
}

/** 產生交給 Local API 的 req 片段。所有讀寫一律透過它取得 req。 */
export function reqOf(db: PipelineDb): Partial<PayloadRequest> {
  return { transactionID: db.transactionID, user: db.user }
}
```

**規則：** 任何一處呼叫 Local API 都必須帶 `req: reqOf(db)`。漏掉一次，那次操作就會落在 transaction 之外，Atomic Chain 的原子性在該處出現破洞，而且不會有任何錯誤訊息。

---

## Layer 1 — Route（Payload custom endpoint）

### 🚨 custom endpoint 不會套用 access control

Payload 的 custom endpoints **不會**自動執行 collection 的 access control，`req.user` 必須自己檢查。

這與 SKILL.md 一致（授權是 Step 的職責），但意思是 `steps/common` 的授權 Step **不是可選的**。漏掉就等於開了一個無授權的寫入入口。

```typescript
// server/routes/order-submit.ts
import type { PayloadHandler } from 'payload'
import { runWorkflow as runOrderSubmitWorkflow } from '../services/order-submit'

export const submitOrderHandler: PayloadHandler = async (req) => {
  const body = (await req.json?.()) ?? {}

  const result = await runOrderSubmitWorkflow({
    db: { payload: req.payload, user: req.user },
    body,
  })

  return Response.json({ data: result.output }, { status: result.status })
}
```

```typescript
// src/collections/Orders.ts
import type { CollectionConfig } from 'payload'
import { submitOrderHandler } from '../server/routes/order-submit'

export const Orders: CollectionConfig = {
  slug: 'orders',
  // 關掉路徑 B：後台與內建 REST 不能直接改動 orders
  access: {
    read: ({ req }) => Boolean(req.user),
    create: () => false,
    update: () => false,
    delete: () => false,
  },
  endpoints: [
    { path: '/submit', method: 'post', handler: submitOrderHandler }, // → POST /api/orders/submit
  ],
  hooks: {}, // 見「Collection Hooks 的紅線」
  fields: [
    /* ... */
  ],
}
```

**規則：**
- Route 不寫 `if (!req.user) return 401`，讓 `checkAuthenticated` step 回 `StepStop(401)`，維持「Route 不含業務邏輯」
- 不回傳 Payload 生成的 document 型別，一律轉成 Response schema
- 需要非 collection 形狀的入口時才用 Next.js Route Handler，並自行 `getPayload({ config })`；預設優先用 collection `endpoints`，因為 `req.user` 與 `req.payload` 是現成的

---

## Layer 2 — Service

與 `typescript.md` 完全相同，只有 `DB` 換成 `PipelineDb`。

```typescript
// server/services/order-submit.ts
import { runAtomicChain, type PipelineStep } from '../core/pipeline-chain'
import type { PipelineDb } from '../core/payload-context'
import { makePipeline as makeOrderValidatePipeline } from '../pipelines/order-validate'
import { makePipeline as makeOrderCreatePipeline } from '../pipelines/order-create'
import { makePipeline as makeInventoryReservePipeline } from '../pipelines/inventory-reserve'
import type { PersistenceResult } from '../core/types'
import type { OrderSubmitInput } from '../types/order-submit'

export async function runWorkflow({
  db,
  body,
}: {
  db: PipelineDb
  body: OrderSubmitInput
}): Promise<PersistenceResult> {
  return runAtomicChain({
    db,
    steps: [
      {
        makePipeline: makeOrderValidatePipeline,
        buildCtx: (db: PipelineDb, input: OrderSubmitInput) => buildValidateCtx(db, input),
      } as PipelineStep<OrderSubmitInput>,
      {
        makePipeline: makeOrderCreatePipeline,
        buildCtx: (db, output) => buildCreateCtx(db, output),
      },
      {
        makePipeline: makeInventoryReservePipeline,
        buildCtx: (db, _output, mutationResult) =>
          buildReserveCtx(db, { order: mutationResult!.after }),
      },
    ],
    initialInput: body,
  })
}
```

---

## Layer 3 — Pipeline Chain（Payload transaction）

這是唯一需要為 Payload 改寫的 core 檔案。與 `typescript.md` 的差異集中在 transaction 的取得與傳遞。

```typescript
// server/core/pipeline-chain.ts
import { PipelineEngine } from './engine'
import { executeMutation } from '../persistence'
import type { PipelineDb } from './payload-context'
import type { Ctx, MutationResult, PersistenceResult, Step, TraceSpan } from './types'

// ── PipelineStep 型別 ─────────────────────────────────────────────

export type FirstBuildCtxFn<TInput> = (db: PipelineDb, initialInput: TInput) => Ctx

export type NextBuildCtxFn = (
  db: PipelineDb,
  previousOutput: unknown,
  mutationResult: MutationResult | null,
) => Ctx

export type BuildCtxFn<TInput = unknown> = FirstBuildCtxFn<TInput> | NextBuildCtxFn

export interface PipelineStep<TInput = unknown> {
  makePipeline: (db: PipelineDb) => Step[]
  buildCtx: BuildCtxFn<TInput>
  alwaysRun?: boolean
}

// ── Atomic Chain ──────────────────────────────────────────────────

export async function runAtomicChain<TInput>({
  db,
  steps,
  initialInput,
}: {
  db: PipelineDb
  steps: PipelineStep[]
  initialInput: TInput
}): Promise<PersistenceResult> {
  const transactionID = await db.payload.db.beginTransaction()

  // 🚨 Mongo 未接 replica set、SQLite 未開啟、或 transactionOptions: false
  //    時會拿不到 transaction。少了這道檢查，Atomic Chain 會安靜地
  //    退化成 Sequential 語意，rollback 完全不生效。
  if (transactionID === null || transactionID === undefined) {
    throw new Error(
      'runAtomicChain 需要資料庫 transaction 支援，但 beginTransaction 未回傳 id。' +
        '請確認 Mongo 已連上 replica set，或 SQLite 已設定 transactionOptions: {}。',
    )
  }

  // transaction id 折進 db，讓 Query 與 Persistence 都落在同一個 transaction
  const txDb: PipelineDb = { ...db, transactionID }

  const engine = new PipelineEngine()
  const allSpans: TraceSpan[] = []
  let lastOutput: unknown = null
  let lastStatus: number | null = null
  let lastMutationResult: MutationResult | null = null

  try {
    for (let i = 0; i < steps.length; i++) {
      const step = steps[i]
      const isFirst = i === 0

      if (!isFirst && lastMutationResult === null && !step.alwaysRun) {
        continue
      }

      let currentCtx: Ctx
      if (isFirst) {
        currentCtx = (step.buildCtx as FirstBuildCtxFn<TInput>)(txDb, initialInput)
      } else if (step.alwaysRun && lastMutationResult === null) {
        currentCtx = (step.buildCtx as NextBuildCtxFn)(txDb, lastOutput, null)
      } else {
        currentCtx = (step.buildCtx as NextBuildCtxFn)(txDb, lastOutput, lastMutationResult)
      }

      const pipeline = step.makePipeline(txDb)
      const result = await engine.execute(pipeline, currentCtx)

      if (!result.mutation) {
        lastOutput = result.output
        lastStatus = result.status
        allSpans.push(...result.spans)

        if (result.status >= 400) {
          // 業務拒絕 → rollback。這裡直接 return 是安全的，
          // Payload 沒有 SQLAlchemy async with 的自動 commit 陷阱。
          await db.payload.db.rollbackTransaction(transactionID)
          return { output: result.output, status: result.status, spans: allSpans, mutationResult: null }
        }
        continue
      }

      // StepCommit：在同一個 transaction 內執行寫入（無 tx 參數）
      const mutationResult = await executeMutation(txDb, result.mutation)
      allSpans.push(...result.spans)
      lastOutput = result.output
      lastStatus = result.status
      lastMutationResult = mutationResult
    }

    await db.payload.db.commitTransaction(transactionID)
  } catch (err) {
    await db.payload.db.rollbackTransaction(transactionID)
    throw err
  }

  return {
    output: lastOutput,
    status: lastStatus ?? 200,
    spans: allSpans,
    mutationResult: lastMutationResult,
  }
}
```

### Sequential Chain

結構與 `typescript.md` 相同，差別只有：不呼叫 `beginTransaction`，全程使用原本的 `db`（`transactionID` 為 `undefined`）。

值得知道的是：即使沒有外層 transaction，**Payload 每次 Local API 寫入操作內部仍會自行開啟一次 transaction**，所以單筆 mutation 本身是原子的。Sequential Chain 失去的是「跨 Pipeline」的原子性，不是「單筆寫入」的原子性。

---

## Layer 4／5 — Pipeline 與 Engine

**完全照 `typescript.md`，一個字都不用改。** 它們不認識 Payload，只認識 `PipelineDb` 這個介面。

唯一的差異是型別標註：`makePipeline(db: PipelineDb): Step[]`。

---

## Layer 6 — Step

**完全照 `typescript.md`。** Step 不呼叫 `payload.*`，只呼叫注入進來的 Query 函式。

`steps/common.ts` 在 Payload 專案裡有一條額外的必要 Step：

```typescript
// server/steps/common.ts
import type { StepContinue, StepStop, Ctx } from '../core/types'
import type { AuthFailure } from '../types/shared'

/**
 * Payload 的 custom endpoint 不套用 access control，
 * 因此這道 Step 是必要的，不是可選的。
 */
export function checkAuthenticated(
  ctx: Ctx,
  _scratch: Record<string, unknown>,
): StepContinue | StepStop<AuthFailure> {
  if (!ctx.db.user) {
    return { _tag: 'StepStop', status: 401, output: { code: 'UNAUTHENTICATED', message: '未登入' } }
  }
  return { _tag: 'StepContinue' }
}
```

`DataMutation.performedBy` 一律填 `ctx.db.user.id`，**不要填 `"system"`**。

---

## Layer 7 — Query

```typescript
// server/queries/order.ts
import type { PipelineDb } from '../core/payload-context'
import { reqOf } from '../core/payload-context'

/** Query 自己宣告的 read model，不使用 payload-types.ts 的生成型別 */
export interface OrderRead {
  id: string
  status: string
  totalCents: number
  customerId: string
}

export async function queryOrderById(db: PipelineDb, orderId: string): Promise<OrderRead | null> {
  const doc = await db.payload.findByID({
    collection: 'orders',
    id: orderId,
    req: reqOf(db),      // ← 必須帶，否則讀不到同 transaction 內未 commit 的寫入
    depth: 0,            // ← 見下方說明
    overrideAccess: true,
    disableErrors: true, // 找不到時回 null，而不是 throw
  })
  if (!doc) return null

  return {
    id: String(doc.id),
    status: doc.status,
    totalCents: doc.totalCents,
    customerId: String(typeof doc.customer === 'object' ? doc.customer.id : doc.customer),
  }
}
```

**`depth: 0` 是刻意的。** Payload 預設會自動 populate relationship 欄位，把整棵關聯樹拉進記憶體，而且回傳型別會在 `string | Order` 之間搖擺。`depth: 0` 讓回傳形狀穩定、成本可預測；真的需要關聯資料時，寫成另一支獨立的 Query。

**`overrideAccess: true` 是刻意的。** 授權由 Step 負責（見下方 Persistence 的同一段說明），Query 不做權限判斷。

**規則：** Query 不接受 `ctx` 或 `scratch`，只接受 `db` 與原始值；絕對不呼叫 `payload.create／update／delete`。

---

## Layer 8 — Persistence

### 授權策略：`overrideAccess: true` + 強制授權 Step

Persistence 呼叫 Local API 時一律使用 `overrideAccess: true`。

理由：業務型 collection 的 `access` 已經對外關成 `() => false`（見「套用前必須先決定的事」）。若 Persistence 用 `overrideAccess: false`，就必須在 access 函式裡重寫一份業務規則來放行 pipeline 的寫入 —— 那正是本架構要消滅的重複，也違反「Persistence 不含業務邏輯」。

**代價要講清楚：這代表授權 100% 由 Step 負責，沒有第二道防線。** `steps/common` 的授權 Step 不可省略，而且必須有測試覆蓋。

### 入口

```typescript
// server/persistence/index.ts
import { randomUUID } from 'node:crypto'
import type { DataMutation, MutationResult } from '../core/types'
import type { PipelineDb } from '../core/payload-context'
import { applyDbMutation } from './adapters/database'
import { applyApiMutation } from './adapters/external-api'
import { applyFileMutation } from './adapters/file'
import { logIntent, logResult } from './audit-log'

export async function executeMutation(
  db: PipelineDb,
  mutation: DataMutation,
): Promise<MutationResult> {
  const intentLogId = randomUUID()
  await logIntent(db, intentLogId, mutation)

  const [before, after] = await applyMutation(db, mutation)

  const diff: Record<string, unknown> = {}
  for (const key of Object.keys(after ?? {})) {
    if ((before ?? {})[key] !== (after ?? {})[key]) diff[key] = (after ?? {})[key]
  }

  const resultLogId = randomUUID()
  await logResult(db, resultLogId, intentLogId, before, after, diff)

  return { before, after, diff, intentLogId, resultLogId }
}

async function applyMutation(
  db: PipelineDb,
  mutation: DataMutation,
): Promise<[Record<string, unknown> | null, Record<string, unknown> | null]> {
  switch (mutation.target) {
    case 'database':
      return applyDbMutation(db, mutation)
    case 'file':
      return applyFileMutation(db, mutation)
    case 'device':
      throw new Error('本專案未啟用 device target')
    case 'external_api':
      return applyApiMutation(db, mutation)
  }
}
```

### database adapter

```typescript
// server/persistence/adapters/database.ts
import type { DataMutation } from '../../core/types'
import type { PipelineDb } from '../../core/payload-context'
import { reqOf } from '../../core/payload-context'
import { resolveRepository } from '../repositories'

export async function applyDbMutation(
  db: PipelineDb,
  mutation: DataMutation,
): Promise<[Record<string, unknown> | null, Record<string, unknown> | null]> {
  const req = reqOf(db)
  const repo = resolveRepository(mutation.entity)
  const opts = { req, depth: 0, overrideAccess: true } as const

  switch (mutation.operation) {
    case 'create': {
      const after = await db.payload.create({
        collection: repo.collection,
        data: mutation.after ?? {},
        ...opts,
      })
      return [null, after as Record<string, unknown>]
    }

    case 'update': {
      const id = repo.extractId(mutation.after)
      const before = await db.payload.findByID({ collection: repo.collection, id, ...opts })
      const after = await db.payload.update({
        collection: repo.collection,
        id,
        // 只送 changedFields 列出的欄位，避免把 id 或未異動欄位一起覆寫回去
        data: pickFields(mutation.after, mutation.changedFields),
        ...opts,
      })
      return [before as Record<string, unknown>, after as Record<string, unknown>]
    }

    case 'delete': {
      const id = repo.extractId(mutation.before)
      const before = await db.payload.findByID({ collection: repo.collection, id, ...opts })
      await db.payload.delete({ collection: repo.collection, id, ...opts })
      return [before as Record<string, unknown>, null]
    }
  }
}

function pickFields(
  record: Record<string, unknown> | null,
  fields: string[],
): Record<string, unknown> {
  const out: Record<string, unknown> = {}
  for (const f of fields) {
    if (record && f in record) out[f] = record[f]
  }
  return out
}
```

### 🚨 DataMutation 沒有 `id` 欄位

`DataMutation` 是封閉 schema，**不得為了主鍵而加欄位**。update／delete 需要的 id 放在 `after`／`before` 的內容裡，由 repository 取出：

- `update`：`after: { id: 'xxx', status: 'paid' }`，`changedFields: ['status']`
- `delete`：`before: { id: 'xxx' }`

### repositories 是白名單

```typescript
// server/persistence/repositories/index.ts
import type { CollectionSlug } from 'payload'
import { orderRepository } from './order'

export interface Repository {
  readonly entity: string
  readonly collection: CollectionSlug
  readonly extractId: (record: Record<string, unknown> | null) => number | string
}

const REGISTRY: Record<string, Repository> = {
  [orderRepository.entity]: orderRepository,
}

/** entity 只能是註冊過的白名單，不接受 mutation 動態指定任意 collection slug。 */
export function resolveRepository(entity: string): Repository {
  const repo = REGISTRY[entity]
  if (!repo) throw new Error(`未註冊的 entity: ${entity}`)
  return repo
}
```

```typescript
// server/persistence/repositories/order.ts
import type { Repository } from './index'

export const orderRepository: Repository = {
  entity: 'order',
  collection: 'orders',
  extractId: (record) => {
    const id = record?.id
    if (typeof id !== 'string' && typeof id !== 'number') {
      throw new Error('order mutation 的 before/after 缺少 id')
    }
    return id
  },
}
```

**為什麼要白名單：** 沒有它，`mutation.entity` 就等於讓業務層動態指定要寫哪個 collection。SKILL.md 對 `file`／`device` 有白名單要求，在 Payload 裡 `database` target 同樣需要，因為 collection slug 是字串。

---

## 稽核 log 的 collection

```typescript
// src/collections/audit/MutationIntents.ts
import type { CollectionConfig } from 'payload'

export const MutationIntents: CollectionConfig = {
  slug: 'mutation-intents',
  access: {
    read: ({ req }) => req.user?.role === 'admin',
    create: () => false, // Persistence 用 overrideAccess: true 寫入
    update: () => false,
    delete: () => false,
  },
  hooks: {}, // 必須為空
  fields: [
    { name: 'intentId', type: 'text', required: true, index: true },
    { name: 'entity', type: 'text', required: true, index: true },
    { name: 'target', type: 'select', required: true, options: ['database', 'file', 'device', 'external_api'] },
    { name: 'operation', type: 'select', required: true, options: ['create', 'update', 'delete'] },
    { name: 'before', type: 'json' },
    { name: 'after', type: 'json' },
    { name: 'changedFields', type: 'json' },
    { name: 'performedBy', type: 'text', required: true, index: true },
    { name: 'reason', type: 'text', required: true },
  ],
}
```

### intent log 不隨 rollback 消失

**這是已定案的規則，不是取捨。**

- **Intent log 一律 `disableTransaction: true`** —— 它記的是「有人打算做這件事」，這個嘗試在回滾後**仍然是真的**，抹掉它等於在稽核紀錄上說謊。
- **Result log 一律留在 transaction 內** —— 它記的是「這件事做完了」，回滾後這句話變成假的，必須跟著消失。

```typescript
// server/persistence/audit-log.ts
import type { DataMutation } from '../core/types'
import type { PipelineDb } from '../core/payload-context'
import { reqOf } from '../core/payload-context'

/**
 * Intent log：脫離外層 transaction，寫入後立即 commit。
 * 目的是讓「被拒絕的意圖」也留下完整紀錄。
 * 失敗時直接 throw —— 稽核記不下來，這次寫入本來就不該執行。
 */
export async function logIntent(
  db: PipelineDb,
  intentId: string,
  mutation: DataMutation,
): Promise<void> {
  await db.payload.create({
    collection: 'mutation-intents',
    data: {
      intentId,
      entity: mutation.entity,
      target: mutation.target,
      operation: mutation.operation,
      before: mutation.before,
      after: mutation.after,
      changedFields: mutation.changedFields,
      performedBy: mutation.performedBy,
      reason: mutation.reason,
    },
    req: reqOf(db),
    overrideAccess: true,
    disableTransaction: true, // ← 走獨立連線，不受外層 rollback 影響
  })
}

/**
 * Result log：留在外層 transaction 內（不加 disableTransaction）。
 * 確保「有 result log = 真的寫入了」永遠成立。
 */
export async function logResult(
  db: PipelineDb,
  resultId: string,
  intentId: string,
  before: Record<string, unknown> | null,
  after: Record<string, unknown> | null,
  diff: Record<string, unknown>,
): Promise<void> {
  await db.payload.create({
    collection: 'mutation-results',
    data: { resultId, intentId, before, after, diff },
    req: reqOf(db),
    overrideAccess: true,
  })
}
```

`req: reqOf(db)` 兩邊都要帶。加了 `disableTransaction: true` 之後 `transactionID` 會被忽略，但 `user` 仍然有作用（版本紀錄歸屬），照帶不影響。

### 判讀方式

兩份 log 搭配起來就能還原每一次操作的結局：

| intent log | result log | 代表 |
|---|---|---|
| 有 | 有 | 真的寫入了 |
| 有 | 無 | 意圖被記錄，但回滾了（業務拒絕，或後續 Pipeline 失敗） |
| 無 | 有 | 不可能發生。出現代表程式有 bug |

### 🚨 intent log 的欄位不得使用 relationship

`disableTransaction` 的寫入走**獨立連線**，它看不到外層 transaction 尚未 commit 的資料。

若 `MutationIntents` 有 relationship 指向 `orders`，Payload 會建外鍵約束；而那筆訂單此刻只存在於外層未 commit 的狀態裡，外鍵檢查會直接失敗或卡在鎖上。

- entity id → `text`
- `before` / `after` / `changedFields` → `json`
- `performedBy` → `text`（不要指向 users，順便讓紀錄在使用者被刪除後仍完整）

### 🚨 寫入目標不得與外層 transaction 重疊

外層 transaction 若鎖住某一列，獨立連線又要寫同一列，就會互等到 timeout：外層在等這次呼叫回傳才能走到 commit，這次呼叫在等外層釋放鎖。

**規則：`disableTransaction` 的寫入目標必須是業務流程從不讀寫的專用 collection。** `mutation-intents` 這種只進不出的表正好符合。

同理，`disableTransaction` 的寫入跟任何東西都不是原子的。intent log 就是單一次 `create`，不要拆成多筆需要一起成立的寫入。

### `disableTransaction` 的適用準則

> **如果這筆寫入所記錄的事，在回滾之後仍然是真的，就用 `disableTransaction: true`。**

符合的還有：登入失敗次數與 rate limit 計數（嘗試確實發生過，跟著回滾等於讓攻擊者免費重試）、錯誤日誌（錯誤本身往往就是回滾的原因，跟著回滾等於銷毀證據）。

**任何業務資料一律不得使用。** 這是逃生口不是選項，每次使用都要有註解說明為什麼這筆紀錄不該回滾。

---

## Collection Hooks 的紅線

這是 Payload 專案最容易把架構弄壞的地方。

| Hook 用途 | 可否保留 |
|---|---|
| slug 生成、欄位格式化、denormalize **自身**欄位 | ✅ 可以，屬於資料形狀 |
| `beforeValidate` 做欄位層級驗證（格式、長度、必填） | ✅ 可以 |
| `afterRead` 做顯示用的欄位組合 | ✅ 可以 |
| **`afterChange` 去寫其他 collection** | ❌ 禁止 |
| **在 hook 裡做業務判斷並 throw** | ❌ 移到 Step |
| **在 hook 裡呼叫外部 API** | ❌ 移到 Pipeline 或 Job |

### 為什麼 `afterChange` 寫其他 collection 是致命的

Persistence 呼叫一次 `payload.update()`，hook 偷偷產生了第二、第三筆寫入。這些寫入**不會出現在 intent log 裡**，稽核紀錄會直接說謊 —— 而整套架構的價值就建立在「所有副作用都有 intent log 與 result log」上。

**規則：被 Persistence 寫入的 collection，不得有會執行寫入的 hook。** 那些連動寫入要拆成 chain 裡的下一個 Pipeline。

### 另一個 Payload 陷阱

Payload 文件明確警告：在 hook 裡用同一個 `req` 發出但**沒有 `await`** 的呼叫，可能在失敗時仍回傳成功的 response，而資料其實已被回滾。本架構下不會寫這種 hook，但既有專案遷移時要逐一檢查。

---

## 外部呼叫：同步 await，放 chain 最後

SKILL.md 已警告 Atomic Chain 的原子性不涵蓋外部系統。本專案的定案做法是**同步呼叫**，並用排序把風險窗口關到最小。

### 規則一：必須 `await`，禁止 fire-and-forget

這不是選擇。`executeMutation` 的合約要求回傳 `MutationResult`，裡面要有 `after` —— 沒等回應就沒有 `after` 可以填。

而且 fire-and-forget 比同步更危險：外部呼叫失敗時不會 throw、不會觸發 rollback，Chain 會照常 commit。DB 說已付款，金流那邊什麼都沒發生，**而且沒有任何人會知道**。

```typescript
// server/persistence/adapters/external-api.ts
import type { DataMutation } from '../../core/types'
import type { PipelineDb } from '../../core/payload-context'
import { resolveExternalClient } from './external-registry'

export async function applyApiMutation(
  db: PipelineDb,
  mutation: DataMutation,
): Promise<[Record<string, unknown> | null, Record<string, unknown> | null]> {
  const client = resolveExternalClient(mutation.entity) // 白名單，未註冊就 throw

  // 必須 await。回應值就是 after，也是後續 Pipeline 能拿到的東西。
  const response = await client.send({
    operation: mutation.operation,
    data: mutation.after,
    performedBy: mutation.performedBy,
    reason: mutation.reason,
  })

  // 失敗直接 throw：讓 Chain 捕捉並 rollback DB。
  // 注意 rollback 撤不回這通已送出的請求 —— 見「規則二」。
  return [null, response as Record<string, unknown>]
}
```

### 規則二：`external_api` 的 Pipeline 一律放 chain 最後

`rollbackTransaction` 只能叫資料庫忘掉寫入，它對外部系統毫無影響力。所以真正的危險不是「外部呼叫失敗」，而是**「外部呼叫成功了，但後面的 Pipeline 失敗」**：

```
Pipeline 1: 建立訂單     → DB 寫入
Pipeline 2: 呼叫金流扣款 → HTTP 200，客戶卡片扣了 3000 元
Pipeline 3: 扣減庫存     → 失敗
→ rollback：訂單消失了，3000 元還在金流公司那邊
```

**被回滾的是訂單，不是扣款。**這個不對稱只能靠排序避免：把外部呼叫放最後，它後面就沒有東西會失敗，也就不存在「事後才發現要撤銷」的窗口。外部呼叫本身失敗時直接 throw，此時 DB 還沒 commit，回滾是乾淨的，兩邊一致。

在 Service 定義 chain 時加註解，讓後來的人看得到：

```typescript
// server/services/order-submit.ts
return runAtomicChain({
  db,
  steps: [
    { makePipeline: makeOrderCreatePipeline, buildCtx: /* ... */ },
    { makePipeline: makeInventoryReservePipeline, buildCtx: /* ... */ },
    // ⚠️ 不可逆：呼叫金流。此節點之後不得再新增 Pipeline。
    //    後面若有任何步驟失敗，rollback 撤不回這筆扣款。
    { makePipeline: makePaymentChargePipeline, buildCtx: /* ... */ },
  ],
  initialInput: body,
})
```

**規則：`external_api` 之後不得再新增 Pipeline。** 這是最容易在半年後被破壞的一條 —— 有人會覺得某個步驟「邏輯上就該接在扣款之後」而直接加上去。註解就是寫給那個人看的。

### 被迫放中間時

只有在「外部系統的回應是後續步驟的輸入」時，才可以把它放中間。這種情況必須：

1. 在 Step 註解寫清楚為什麼放不了最後
2. 寫補償邏輯（refund／void／cancel API），並接受補償本身也可能失敗
3. 依賴 `disableTransaction: true` 的 intent log 作為人工對帳依據

補償不在 transaction 保護範圍內，它是額外的失敗點。**設計時優先考慮重排 chain，而不是寫補償。**

### 什麼訊號出現時該回頭考慮 outbox

Payload 的 `payload.jobs.queue()` 帶 `req` 呼叫時，job document 會跟著 transaction 一起 commit 或 rollback —— 這天然就是 transactional outbox：把「不可回滾的 HTTP」換成「可回滾的 DB 寫入」，真正的呼叫延到 commit 之後由 worker 執行。

代價是拿不到回應值（`MutationResult.after` 只能代表「已排入佇列」）、投遞是至少一次（外部 API 必須支援 idempotency key）、而且要有人負責跑 worker。

出現以下任一訊號再回頭評估，目前不需要：

1. 出現不需要回應值的呼叫（寄信、發 webhook、推播）
2. 同一條 chain 需要打兩個以上的外部 API（「放最後」只保護得了一個）
3. 第三方的穩定性開始影響成功率（同步呼叫會讓對方的抖動直接變成你的失敗）

---

## Payload 專屬注意事項

### `payload-types.ts` 的型別不要穿透

生成型別太好用，很容易直接從 Query 回傳到 Step、再回傳到 Route。它們是 ORM model，等同 `typescript.md` 說的「不洩漏內部型別」所指的東西。

- Query → Step 邊界：轉成 Query 自己宣告的 read model（如上方 `OrderRead`）
- Route 邊界：轉成 Response schema

### relationship 欄位的型別不穩定

Payload 的 relationship 在 `depth: 0` 時是 id，`depth >= 1` 時是完整物件，型別是 `string | Order` 這種 union。Query 一律用 `depth: 0` 並在 read model 裡固定成 `customerId: string`，讓上層不必處理這個 union。

### 上傳檔案不受 transaction 保護

Upload collection 的實體檔案寫入／刪除發生在檔案系統，是否隨 transaction 回滾**不要預設它會**。把它當成 `target: file` 的副作用看待，套用 SKILL.md 對非資料庫寫入的那組規則（授權 Step、白名單、放在 chain 最後）。實際行為請在專案的 storage adapter 上自行驗證後記錄。

### transaction 支援是環境相依的

- MongoDB 需要連上 replica set
- SQLite 預設關閉，需要傳 `transactionOptions: {}` 才會啟用
- 任何 adapter 傳 `transactionOptions: false` 會整個關掉

這代表**同一份程式碼在本機和正式環境可能有不同的原子性保證**。`runAtomicChain` 的 `beginTransaction` 回傳值檢查就是為了讓這件事在啟動時就炸掉，而不是在稽核時才發現。

### 測試

Step 與 Engine 的單元測試不需要啟動 Payload，因為它們只依賴 `PipelineDb` 介面與注入的 Query 函式：

```typescript
const fakeDb = { payload: {} as Payload, user: { id: 'u1', role: 'member' } } as PipelineDb
```

Query 與 Persistence 的測試才需要真實 Payload instance，用 `getPayload({ config })` 搭配測試資料庫。

---

## 常見錯誤

- ❌ 呼叫 Local API 時漏掉 `req: reqOf(db)` → 該次操作落在 transaction 外，原子性出現無聲破洞
- ❌ 只在 `executeMutation` 帶 transaction，Query 不帶 → 後續 Pipeline 讀不到前面未 commit 的寫入
- ❌ 把 `_ChainAbort` 之類的 Python 解法搬進來 → Payload 沒有 `async with` 的 commit 陷阱，提前 `return` 是安全的
- ❌ 沒檢查 `beginTransaction()` 是否回傳 `null` → Atomic Chain 安靜退化成 Sequential
- ❌ custom endpoint 沒有授權 Step → Payload 不會替 custom endpoint 套 access control
- ❌ Persistence 用 `overrideAccess: false` 並在 access 函式裡重寫業務規則 → 規則重複兩份
- ❌ 為了主鍵而在 `DataMutation` 加 `id` 欄位 → schema 是封閉的，id 放在 `before`／`after` 內容裡
- ❌ update 時把整個 `mutation.after` 送進 `payload.update` → 用 `changedFields` 篩選
- ❌ `resolveRepository` 直接把 `mutation.entity` 當 collection slug 用 → 必須走白名單
- ❌ 在 `afterChange` hook 寫其他 collection → 產生沒有 intent log 的隱形寫入
- ❌ intent log 忘記加 `disableTransaction: true` → 被拒絕的意圖隨 rollback 消失，稽核鏈斷掉
- ❌ result log 加了 `disableTransaction: true` → 出現「有 result log 但實際被回滾」的假紀錄
- ❌ intent log 的欄位用 relationship 指向業務 collection → 獨立連線看不到未 commit 的資料，外鍵檢查失敗或卡鎖
- ❌ `disableTransaction` 的寫入目標與外層 transaction 重疊 → 互等到 timeout
- ❌ 業務資料用 `disableTransaction: true` → 在原子性上開一個沒有錯誤訊息的破洞
- ❌ 外部呼叫沒有 `await`（fire-and-forget） → 失敗不會觸發 rollback，DB 與外部永久不一致且無人知曉
- ❌ 在 `external_api` 的 Pipeline 之後又加了 Pipeline → 那筆已送出的請求 rollback 撤不回來
- ❌ Query 不設 `depth: 0` → relationship 自動 populate，型別搖擺、成本不可預測
- ❌ 把 `payload-types.ts` 的型別回傳給 Step 或 Route → ORM model 穿透層邊界
- ❌ 假設 upload 的實體檔案會隨 transaction 回滾 → 當成 `file` target 的副作用處理
- ❌ 對內容型 collection（Pages、Posts）硬套七層 → SKILL.md 已說明不適用場景
- ❌ 只把業務規則寫進 Step，卻沒關掉後台的 create／update／delete → 路徑 B 整條繞過
