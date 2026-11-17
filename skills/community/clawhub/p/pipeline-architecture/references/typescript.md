# Pipeline Architecture — TypeScript 實作參考

> 架構規則請看 `SKILL.md`。本檔只提供 TypeScript／Node.js 的程式碼範例。
> 若專案是 Python，請改讀 `references/python.md`，不要混用。
>
> **若專案基底是 Payload CMS，本檔仍然適用，但必須再讀 `references/payload-cms.md`。**
> 該檔記載 Payload 的 transaction 邊界、collection hooks 紅線與兩條寫入路徑等偏離點，
> 與本檔衝突時以 `payload-cms.md` 為準。
>
> **若專案部署在 Cloudflare Workers（存在 `wrangler.toml`／`wrangler.jsonc`），本檔仍然適用，但必須再讀 `references/cloudflare-workers.md`。**
> 該檔記載資料庫相容性（D1 沒有 Atomic Chain）、Hono 的 Route 寫法、Hyperdrive 快取與 `waitUntil` 等紅線，
> 與本檔衝突時以 `cloudflare-workers.md` 為準。

## 目錄

- [目錄結構](#目錄結構)
- [core/types.ts](#coretypests)
- [Layer 1 — Route](#layer-1--route)
- [Layer 2 — Service](#layer-2--service)
- [Layer 3 — Pipeline Chain](#layer-3--pipeline-chain)
- [Layer 4 — Pipeline](#layer-4--pipeline)
- [Layer 5 — Engine](#layer-5--engine)
- [Layer 6 — Step](#layer-6--step)
- [Layer 7 — Query](#layer-7--query)
- [Layer 8 — Persistence](#layer-8--persistence)
- [測試](#測試)
- [TypeScript 特有注意事項](#typescript-特有注意事項)

---

## 目錄結構

```
project/
├── routes/               # HTTP 入口，薄層
├── services/             # Orchestrator：runWorkflow（import 時用 as 加入 domain 名）
├── pipelines/            # 純宣告：makePipeline（import 時用 as 加入 domain 名）
├── steps/
│   ├── {domain}.ts       # 各 domain 的 steps
│   ├── common.ts         # 跨 domain 共用的 steps（知道 ctx/scratch 介面）
│   └── utils.ts          # 純工具函式（不知道任何 Step 或 domain 概念）
├── queries/              # 純讀取：依功能命名，不套用固定通用名稱
├── types/                # 各 domain 的 Input / Output / Failure / Response 型別
├── core/
│   ├── engine.ts         # PipelineEngine（不因業務修改）
│   ├── pipeline-chain.ts # runAtomicChain / runSequentialChain
│   ├── exceptions.ts     # PipelineExecutionError
│   ├── protocols.ts      # interface 定義
│   └── types.ts          # StepContinue, StepStop, StepCommit, DataMutation …
├── persistence/          # 單一寫入層
└── tests/
    ├── steps/            # 單元測試：stub ctx + scratch，用 fake 實作
    ├── queries/          # 單元測試：用 in-memory DB 或 fake
    └── services/         # 整合測試：跑完整 pipeline chain
```

---

## core/types.ts

```typescript
// core/types.ts

// ── Step 函式型別 ────────────────────────────────────────────────

/**
 * Step 是 Pipeline 內的最小執行單元。
 * scratch 是目前為止 StepContinue 累積下來的中繼資料，
 * 僅供 Step 之間傳遞判斷依據使用，不會流入最終的 DataMutation。
 */
export type Step<TOutput = unknown> = (
  ctx: Ctx,
  scratch: Record<string, unknown>,
) => StepResult<TOutput> | Promise<StepResult<TOutput>>;

// ── Step 回傳值 ──────────────────────────────────────────────────

export interface StepContinue {
  readonly _tag: "StepContinue";
  /**
   * 中繼資料（scratch），僅供後續 Step 讀取判斷之用。
   * 不是 DataMutation 的一部分，Engine 不會把它併入最終寫入意圖。
   */
  readonly scratch?: Record<string, unknown>;
}

export interface StepStop<TOutput = unknown> {
  readonly _tag: "StepStop";
  readonly status: number;
  readonly output: TOutput;
}

export interface StepCommit<TOutput = unknown> {
  readonly _tag: "StepCommit";
  readonly status: number;
  readonly output: TOutput;
  /**
   * 完整且型別明確的寫入意圖。StepCommit 必須自己組出完整的 DataMutation，
   * 不會、也不能與先前 StepContinue 累積的 scratch 合併。
   */
  readonly mutation: DataMutation;
}

export type StepResult<TOutput = unknown> =
  | StepContinue
  | StepStop<TOutput>
  | StepCommit<TOutput>;

// ── Pipeline 執行結果 ─────────────────────────────────────────────

export interface PipelineResult<TOutput = unknown> {
  readonly output: TOutput;
  readonly status: number;
  readonly spans: TraceSpan[];
  readonly mutation: DataMutation | null;
}

// ── 意圖 Schema ───────────────────────────────────────────────────

export type MutationTarget = "database" | "file" | "device" | "external_api";
export type MutationOperation = "create" | "update" | "delete";

/**
 * DataMutation 的 before/after 語意：
 * - create: before=null, after=新資料
 * - update: before=變更前（由 Persistence 擷取）, after=變更後
 * - delete: before=刪除前資料, after=null
 *
 * 注意：Pipeline 內的 Step 宣告的是「意圖」。
 * before 在 Step 宣告階段可能為 null，
 * 真正的 before 會由 Persistence 在執行前擷取並記錄。
 *
 * DataMutation 是封閉的 schema：只包含以下欄位。StepCommit 組裝時
 * 不應該、也不能夾帶 schema 之外的暫存欄位（那些屬於 scratch 的職責）。
 */
export interface DataMutation {
  readonly entity: string;
  readonly target: MutationTarget;
  readonly operation: MutationOperation;
  readonly before: Record<string, unknown> | null;
  readonly after: Record<string, unknown> | null;
  readonly changedFields: string[];
  readonly performedBy: string;
  readonly reason: string;
}

// ── Persistence 執行結果 ──────────────────────────────────────────

/**
 * 真實寫入後的結果。after 包含資料庫自動生成的欄位
 * （id、created_at、version 等）。
 *
 * 目前寫入失敗一律以 throw 處理（見 Pipeline Chain 的 try/catch），
 * 因此本型別只描述成功寫入後的結果，不包含失敗狀態欄位。
 * 若未來需要區分「失敗但不 throw」的情境（例如 Compensate 機制），
 * 屆時應以 discriminated union（例如 MutationSuccess | MutationFailure）
 * 重新設計，而非加回一個 success: boolean。
 */
export interface MutationResult {
  readonly before: Record<string, unknown> | null;
  readonly after: Record<string, unknown> | null;
  readonly diff: Record<string, unknown>;
  readonly intentLogId: string;
  readonly resultLogId: string;
}

export interface PersistenceResult<TOutput = unknown> {
  readonly output: TOutput;
  readonly status: number;
  readonly spans: TraceSpan[];
  readonly mutationResult: MutationResult | null;
}

// ── Trace ─────────────────────────────────────────────────────────

export type TraceSpanStatus = "continue" | "stop" | "commit" | "error";

export interface TraceSpan {
  readonly step: string;
  readonly status: TraceSpanStatus;
  readonly durationMs: number;
  readonly startedAt: number;
}
```

---

## Layer 1 — Route

```typescript
// routes/user-register.ts
import { Router, Request, Response } from "express";
import { runWorkflow as runUserRegisterWorkflow } from "../services/user-register";

const router = Router();

interface UserRegisterRequest {
  email: string;
  name: string;
}

router.post("/users/register", async (req: Request, res: Response) => {
  const body = req.body as UserRegisterRequest;
  const db = req.db; // 由 middleware 注入
  const result = await runUserRegisterWorkflow({ db, body });
  res.status(result.status).json({ data: result.output });
});

export default router;
```

**規則：**
- 只做 request 解析 + 呼叫 Service（import 時用 `as` 加入 domain 名稱）
- 不含任何 if、DB 呼叫、業務判斷
- 不把 ORM model 直接回傳，永遠轉成 Response schema

---

## Layer 2 — Service

### Atomic Chain 範例

```typescript
// services/user-register.ts
import { PipelineStep, runAtomicChain } from "../core/pipeline-chain";
import { makePipeline as makeUserRegisterPipeline } from "../pipelines/user-register";
import { makePipeline as makeWorkspaceCreatePipeline } from "../pipelines/workspace-create";
import { makePipeline as makeWelcomeEmailPipeline } from "../pipelines/welcome-email";
import type { PersistenceResult } from "../core/types";

interface RegisterInput {
  email: string;
  name: string;
}

export async function runWorkflow({
  db,
  body,
}: {
  db: DB;
  body: RegisterInput;
}): Promise<PersistenceResult> {
  return runAtomicChain({
    db,
    steps: [
      {
        makePipeline: makeUserRegisterPipeline,
        buildCtx: (db: DB, input: RegisterInput) => buildRegisterCtx(db, input),
      } as PipelineStep<RegisterInput>,
      {
        makePipeline: makeWorkspaceCreatePipeline,
        buildCtx: (_db, _output, mutationResult) =>
          buildWorkspaceCtx(db, { user: mutationResult!.after }),
      },
      {
        makePipeline: makeWelcomeEmailPipeline,
        buildCtx: (_db, _output, mutationResult) =>
          buildWelcomeCtx(db, { user: mutationResult!.after }),
      },
    ],
    initialInput: body,
  });
}
```

### Sequential Chain 範例

```typescript
// services/audit-workflow.ts
import { PipelineStep, runSequentialChain } from "../core/pipeline-chain";
import { makePipeline as makeLogAccessPipeline } from "../pipelines/log-access";
import { makePipeline as makeUpdateLastSeenPipeline } from "../pipelines/update-last-seen";
import type { PersistenceResult } from "../core/types";

export async function runWorkflow({
  db,
  body,
}: {
  db: DB;
  body: AuditInput;
}): Promise<PersistenceResult> {
  return runSequentialChain({
    db,
    steps: [
      {
        makePipeline: makeLogAccessPipeline,
        buildCtx: (db: DB, input: AuditInput) => buildLogCtx(db, input),
      } as PipelineStep<AuditInput>,
      {
        makePipeline: makeUpdateLastSeenPipeline,
        buildCtx: (_db, _output, mutationResult) =>
          buildLastSeenCtx(db, { data: mutationResult!.after }),
      },
    ],
    initialInput: body,
  });
}
```

**規則：**
- Service 永遠使用 `runAtomicChain` 或 `runSequentialChain`，不手動呼叫 Engine 或 Persistence
- Service 不寫業務邏輯，只做 Pipeline 鏈的宣告與 `initialInput` 的傳遞；ctx 的建構一律交給各 Pipeline 自己的 `buildCtx`，Service 不預先呼叫它

---

## Layer 3 — Pipeline Chain

```typescript
// core/pipeline-chain.ts
import { PipelineEngine } from "./engine";
import { executeMutation } from "../persistence";
import {
  type MutationResult,
  type PersistenceResult,
  type Step,
  type TraceSpan,
} from "./types";

// ── PipelineStep 型別 ─────────────────────────────────────────────

/** 第一個 Pipeline 的 buildCtx 簽名 */
export type FirstBuildCtxFn<TInput> = (db: DB, initialInput: TInput) => Ctx;

/** 後續 Pipeline 的 buildCtx 簽名 */
export type NextBuildCtxFn = (
  db: DB,
  previousOutput: unknown,
  mutationResult: MutationResult | null,
) => Ctx;

export type BuildCtxFn<TInput = unknown> =
  | FirstBuildCtxFn<TInput>
  | NextBuildCtxFn;

/** 宣告一個 Pipeline 及其在鏈中的 ctx 建構方式。 */
export interface PipelineStep<TInput = unknown> {
  /** Pipeline 工廠函式，簽名為 (db: DB) => Step[] */
  makePipeline: (db: DB) => Step[];
  /** ctx 建構函式。簽名依本項在 steps 陣列中的位置而定。 */
  buildCtx: BuildCtxFn<TInput>;
  /**
   * 即使前一個 Pipeline 為 StepStop（無 mutation），
   * 是否仍強制執行本 Pipeline。適用於稽核日誌等 side-effect。
   */
  alwaysRun?: boolean;
}

// ── Atomic Chain ──────────────────────────────────────────────────

export async function runAtomicChain<TInput>({
  db,
  steps,
  initialInput,
}: {
  db: DB;
  steps: PipelineStep[];
  /** 傳給第一個 Pipeline 的 buildCtx 的原始輸入 */
  initialInput: TInput;
}): Promise<PersistenceResult> {
  const engine = new PipelineEngine();
  const allSpans: TraceSpan[] = [];
  let lastOutput: unknown = null;
  let lastStatus: number | null = null;
  let lastMutationResult: MutationResult | null = null;

  const tx = await db.beginTransaction();

  try {
    for (let i = 0; i < steps.length; i++) {
      const step = steps[i];
      const isFirst = i === 0;

      // 前一個 Pipeline 為 StepStop 且本步驟不是 alwaysRun → 跳過
      if (!isFirst && lastMutationResult === null && !step.alwaysRun) {
        continue;
      }

      // 建構當前 Pipeline 的 ctx
      let currentCtx: Ctx;
      if (isFirst) {
        // 第一個 Pipeline：用 FirstBuildCtxFn 從 initialInput 建構 ctx
        currentCtx = (step.buildCtx as FirstBuildCtxFn<TInput>)(db, initialInput);
      } else if (step.alwaysRun && lastMutationResult === null) {
        // alwaysRun + 前一個無 mutation：傳 null
        currentCtx = (step.buildCtx as NextBuildCtxFn)(db, lastOutput, null);
      } else {
        // 一般後續 Pipeline：傳上一個的 output 和 mutationResult
        currentCtx = (step.buildCtx as NextBuildCtxFn)(
          db,
          lastOutput,
          lastMutationResult,
        );
      }

      const pipeline = step.makePipeline(db);
      const result = await engine.execute(pipeline, currentCtx);

      if (!result.mutation) {
        // StepStop：Pipeline 決定終止但不寫入
        lastOutput = result.output;
        lastStatus = result.status;
        allSpans.push(...result.spans);

        if (result.status >= 400) {
          // 業務拒絕 → rollback 先前已執行的 mutation
          await tx.rollback();
          return {
            output: result.output,
            status: result.status,
            spans: allSpans,
            mutationResult: null,
          };
        }
        // 成功但不需寫入（status 2xx），繼續下一個 Pipeline
        continue;
      }

      // StepCommit：在 transaction 內執行寫入
      const mutationResult = await executeMutation(db, result.mutation, tx);
      allSpans.push(...result.spans);
      lastOutput = result.output;
      lastStatus = result.status;
      lastMutationResult = mutationResult;
    }

    // 全部成功 → commit
    await tx.commit();
  } catch (err) {
    await tx.rollback();
    throw err;
  }

  return {
    output: lastOutput,
    status: lastStatus ?? 200,
    spans: allSpans,
    mutationResult: lastMutationResult,
  };
}

// ── Sequential Chain ──────────────────────────────────────────────

export async function runSequentialChain<TInput>({
  db,
  steps,
  initialInput,
}: {
  db: DB;
  steps: PipelineStep[];
  /** 傳給第一個 Pipeline 的 buildCtx 的原始輸入 */
  initialInput: TInput;
}): Promise<PersistenceResult> {
  const engine = new PipelineEngine();
  const allSpans: TraceSpan[] = [];
  let lastOutput: unknown = null;
  let lastStatus: number | null = null;
  let lastMutationResult: MutationResult | null = null;

  for (let i = 0; i < steps.length; i++) {
    const step = steps[i];
    const isFirst = i === 0;

    // 前一個 Pipeline 為 StepStop 且本步驟不是 alwaysRun → 跳過
    if (!isFirst && lastMutationResult === null && !step.alwaysRun) {
      continue;
    }

    // 建構當前 Pipeline 的 ctx
    let currentCtx: Ctx;
    if (isFirst) {
      currentCtx = (step.buildCtx as FirstBuildCtxFn<TInput>)(db, initialInput);
    } else if (step.alwaysRun && lastMutationResult === null) {
      currentCtx = (step.buildCtx as NextBuildCtxFn)(db, lastOutput, null);
    } else {
      currentCtx = (step.buildCtx as NextBuildCtxFn)(
        db,
        lastOutput,
        lastMutationResult,
      );
    }

    const pipeline = step.makePipeline(db);
    const result = await engine.execute(pipeline, currentCtx);

    if (!result.mutation) {
      lastOutput = result.output;
      lastStatus = result.status;
      allSpans.push(...result.spans);

      if (result.status >= 400) {
        // 業務拒絕 → 停止執行後續 Pipeline
        // 注意：已 commit 的 Pipeline 不會 rollback
        return {
          output: result.output,
          status: result.status,
          spans: allSpans,
          mutationResult: null,
        };
      }
      continue;
    }

    // StepCommit：立即執行寫入並 commit
    const mutationResult = await executeMutation(db, result.mutation);
    allSpans.push(...result.spans);
    lastOutput = result.output;
    lastStatus = result.status;
    lastMutationResult = mutationResult;
  }

  return {
    output: lastOutput,
    status: lastStatus ?? 200,
    spans: allSpans,
    mutationResult: lastMutationResult,
  };
}
```

---

## Layer 4 — Pipeline

```typescript
// pipelines/user-register.ts
import {
  checkEmailNotTaken,
  makeFetchPlanLimits,
  ensureRegistrationAllowed,
  buildCommit,
} from "../steps/user-register";
import { queryPlanLimits } from "../queries/plan";
import type { Step } from "../core/types";

export function makePipeline(db: DB): Step[] {
  return [
    checkEmailNotTaken,
    makeFetchPlanLimits(queryPlanLimits),
    ensureRegistrationAllowed,
    buildCommit,
  ];
}
```

**規則：** 只有 array。沒有 `if`、沒有 `await`、沒有業務邏輯。
用 `make*` 工廠函式注入 Query 依賴進 Step。

---

## Layer 5 — Engine

```typescript
// core/engine.ts
import {
  type Step,
  type StepResult,
  type PipelineResult,
  type TraceSpan,
} from "./types";
import { PipelineExecutionError } from "./exceptions";

export class PipelineEngine {
  async execute(steps: Step[], ctx: Ctx): Promise<PipelineResult> {
    // accumulatedScratch 只是 Step 之間傳遞的中繼資料，
    // 不是最終的 DataMutation 草稿。
    let accumulatedScratch: Record<string, unknown> = {};
    const spans: TraceSpan[] = [];

    for (const step of steps) {
      const name = step.name || "anonymous";
      const startedAt = Date.now();

      let result: StepResult;
      try {
        result = await this.call(step, ctx, accumulatedScratch);
      } catch (err) {
        spans.push({
          step: name,
          status: "error",
          durationMs: Date.now() - startedAt,
          startedAt,
        });
        throw new PipelineExecutionError(name, spans, err as Error);
      }

      const durationMs = Date.now() - startedAt;

      if (result._tag === "StepStop") {
        spans.push({ step: name, status: "stop", durationMs, startedAt });
        return {
          output: result.output,
          status: result.status,
          spans,
          mutation: null,
        };
      }

      if (result._tag === "StepCommit") {
        // StepCommit 已經是完整、型別明確的 DataMutation，
        // 不與 accumulatedScratch 合併 —— 避免中繼資料（如 planLimits）
        // 污染最終送進 Persistence 的寫入意圖。
        spans.push({ step: name, status: "commit", durationMs, startedAt });
        return {
          output: result.output,
          status: result.status,
          spans,
          mutation: result.mutation,
        };
      }

      // StepContinue
      if (result.scratch) {
        // shallow merge：後宣告的 Step 覆蓋前面的值。
        // 這裡合併的是 scratch，僅供後續 Step 讀取判斷，不會流入 mutation。
        accumulatedScratch = { ...accumulatedScratch, ...result.scratch };
      }
      spans.push({ step: name, status: "continue", durationMs, startedAt });
    }

    throw new Error("Pipeline finished without StepStop or StepCommit");
  }

  private async call(
    step: Step,
    ctx: Ctx,
    scratch: Record<string, unknown>,
  ): Promise<StepResult> {
    const result = step(ctx, scratch);
    if (result instanceof Promise) {
      return result;
    }
    return result;
  }
}
```

```typescript
// core/exceptions.ts
import type { TraceSpan } from "./types";

export class PipelineExecutionError extends Error {
  public readonly stepName: string;
  public readonly spans: TraceSpan[];
  public readonly originalError: Error;

  constructor(stepName: string, spans: TraceSpan[], originalError: Error) {
    super(`Step '${stepName}' failed: ${originalError.message}`);
    this.name = "PipelineExecutionError";
    this.stepName = stepName;
    this.spans = spans;
    this.originalError = originalError;
  }
}
```

**規則：** 不因任何業務需求修改 Engine。`StepCommit.mutation` 已經是型別明確的 `DataMutation`，Engine 不再需要（也不允許）用 `as DataMutation` 之類的方式強制轉型。

---

## Layer 6 — Step

### steps/common.ts — 跨 domain 共用

```typescript
// steps/common.ts
import type { StepContinue, StepStop } from "../core/types";
import type { PermissionFailure } from "../types/shared";

export function checkAdminPermission(
  ctx: Ctx,
  _scratch: Record<string, unknown>,
): StepContinue | StepStop<PermissionFailure> {
  if (ctx.user.role !== "admin") {
    return {
      _tag: "StepStop",
      status: 403,
      output: { code: "PERMISSION_DENIED", message: "權限不足" },
    };
  }
  return { _tag: "StepContinue" };
}

export function checkRateLimit(
  ctx: Ctx,
  _scratch: Record<string, unknown>,
): StepContinue | StepStop<PermissionFailure> {
  if (ctx.rateLimit.remaining <= 0) {
    return {
      _tag: "StepStop",
      status: 429,
      output: { code: "RATE_LIMIT_EXCEEDED", message: "請求過於頻繁" },
    };
  }
  return { _tag: "StepContinue" };
}
```

### steps/utils.ts — 純工具函式

```typescript
// steps/utils.ts

export function formatTimestamp(ts: number): string {
  return new Date(ts).toISOString();
}

export function truncateString(s: string, maxLen: number): string {
  return s.length > maxLen ? s.slice(0, maxLen) : s;
}

export function maskEmail(email: string): string {
  const [local, domain] = email.split("@");
  return `${local[0]}***@${domain}`;
}
```

### steps/{domain}.ts — Domain Step

```typescript
// steps/user-register.ts
import type {
  StepContinue,
  StepStop,
  StepCommit,
  Step,
} from "../core/types";
import type { RegisterFailure, RegisterOutput } from "../types/user-register";
import type { PlanQueryFn } from "../core/protocols";

export function checkEmailNotTaken(
  ctx: Ctx,
  _scratch: Record<string, unknown>,
): StepContinue | StepStop<RegisterFailure> {
  if (ctx.existingUser) {
    return {
      _tag: "StepStop",
      status: 409,
      output: { code: "EMAIL_TAKEN", message: "此 Email 已被註冊" },
    };
  }
  return { _tag: "StepContinue" };
}

export function makeFetchPlanLimits(queryFn: PlanQueryFn): Step {
  return async (
    ctx: Ctx,
    _scratch: Record<string, unknown>,
  ): Promise<StepContinue | StepStop<RegisterFailure>> => {
    const limits = await queryFn(ctx.db, ctx.input.planId);
    if (!limits) {
      return {
        _tag: "StepStop",
        status: 404,
        output: { code: "PLAN_NOT_FOUND", message: "找不到方案" },
      };
    }
    // planLimits 只是給下一個 Step 判斷用的中繼資料，
    // 放進 scratch，不是 DataMutation 的欄位。
    return { _tag: "StepContinue", scratch: { planLimits: limits } };
  };
}

export function ensureRegistrationAllowed(
  _ctx: Ctx,
  scratch: Record<string, unknown>,
): StepContinue | StepStop<RegisterFailure> {
  const limits = scratch.planLimits as Record<string, number> | undefined;
  const maxUsers = limits?.maxUsers ?? 0;
  const currentUsers = limits?.currentUsers ?? 0;
  if (maxUsers <= currentUsers) {
    return {
      _tag: "StepStop",
      status: 422,
      output: { code: "PLAN_LIMIT_REACHED", message: "已達方案人數上限" },
    };
  }
  return { _tag: "StepContinue" };
}

export function buildCommit(
  ctx: Ctx,
  _scratch: Record<string, unknown>,
): StepCommit<RegisterOutput> {
  // mutation 是完整、乾淨的 DataMutation，只包含 schema 定義的欄位，
  // 不會夾帶 _scratch 裡的 planLimits 等中繼資料。
  return {
    _tag: "StepCommit",
    status: 201,
    output: { userId: ctx.input.email, message: "註冊成功" },
    mutation: {
      entity: "user",
      target: "database",
      operation: "create",
      before: null,
      after: { email: ctx.input.email, name: ctx.input.name },
      changedFields: ["email", "name"],
      performedBy: "system",
      reason: "user_self_register",
    },
  };
}
```

---

## Layer 7 — Query

```typescript
// queries/user.ts

export async function queryByEmail(
  db: DB,
  email: string,
): Promise<Record<string, unknown> | null> {
  const row = await db.fetchOne(
    "SELECT id, email, name FROM users WHERE email = ?",
    [email],
  );
  return row ? { ...row } : null;
}

export async function queryById(
  db: DB,
  userId: string,
): Promise<Record<string, unknown> | null> {
  const row = await db.fetchOne(
    "SELECT id, email, name FROM users WHERE id = ?",
    [userId],
  );
  return row ? { ...row } : null;
}
```

```typescript
// core/protocols.ts
export interface UserQueryFn {
  (db: DB, email: string): Promise<Record<string, unknown> | null>;
}

export interface PlanQueryFn {
  (db: DB, planId: string): Promise<Record<string, unknown> | null>;
}
```

**規則：** 不接受 `ctx` 或 `scratch`，只接受原始值；不回傳 Step 三態；絕對不執行任何寫入。

---

## Layer 8 — Persistence

### 結構選擇

**Domain 少於 5 種 → Option A（扁平結構）**

```
persistence/
├── index.ts          # executeMutation 入口，負責分派到各 target
├── database.ts       # SQL / ORM 實作
├── file.ts           # 本機檔案讀寫
├── device.ts         # 裝置 / 主機變數
└── external-api.ts   # 外部 API 呼叫
```

**Domain 超過 5 種 → Option B（加入 Repository 層）**

```
persistence/
├── index.ts              # executeMutation 入口
├── adapters/             # 各 target 的寫入實作
│   ├── database.ts
│   ├── file.ts
│   ├── device.ts
│   └── external-api.ts
└── repositories/         # 各 domain 的具體 SQL / schema 實作
    ├── user.ts           # 知道 users table 的結構
    └── order.ts
```

### 入口（兩個 Option 共用）

```typescript
// persistence/index.ts
import { v4 as uuid } from "uuid";
import type { DataMutation, MutationResult } from "../core/types";
import { applyDbMutation } from "./adapters/database";
import { applyFileMutation } from "./adapters/file";
import { applyDeviceMutation } from "./adapters/device";
import { applyApiMutation } from "./adapters/external-api";

/**
 * 執行一筆 DataMutation。
 *
 * @param db - 資料庫連線
 * @param mutation - 要執行的意圖（已經是乾淨、型別明確的 DataMutation，
 *                   不含任何 scratch 中繼資料）
 * @param tx - 可選的 transaction 物件。若提供，寫入在該 transaction 內執行。
 *             用於 Atomic Chain 中多個 Pipeline 共享 transaction 的場景。
 */
export async function executeMutation(
  db: DB,
  mutation: DataMutation,
  tx?: Transaction,
): Promise<MutationResult> {
  const intentLogId = uuid();
  await logIntent(db, intentLogId, mutation, tx);

  const [before, after] = await applyMutation(db, mutation, tx);

  const diff: Record<string, unknown> = {};
  for (const key of Object.keys(after ?? {})) {
    if ((before ?? {})[key] !== (after ?? {})[key]) {
      diff[key] = (after ?? {})[key];
    }
  }

  const resultLogId = uuid();
  await logResult(db, resultLogId, intentLogId, before, after, diff, tx);

  return { before, after, diff, intentLogId, resultLogId };
}

async function applyMutation(
  db: DB,
  mutation: DataMutation,
  tx?: Transaction,
): Promise<[Record<string, unknown> | null, Record<string, unknown> | null]> {
  switch (mutation.target) {
    case "database":
      return applyDbMutation(db, mutation, tx);
    case "file":
      return applyFileMutation(mutation);
    case "device":
      return applyDeviceMutation(mutation);
    case "external_api":
      return applyApiMutation(mutation);
  }
}
```

### 未來擴展點：Compensate

> 🚨 **Atomic Chain 的原子性只涵蓋資料庫，不涵蓋外部系統。**

當 chain 中包含 `target` 為 `external_api`、`file`、`device` 的 mutation 時，這些寫入不受 DB transaction 控制。若後續 Pipeline 失敗觸發 rollback，DB 會回滾，但這些已經發生的副作用**不會**，而且通常不可逆：

- **資料已離開系統。** 送給第三方的個資與內容已完成傳輸並被對方留存，rollback 不會讓對方刪除。這同時是資料外洩與合規（GDPR、個資法）的風險面 —— 「交易失敗了所以資料沒出去」是錯的。
- **副作用已生效。** 簡訊已發出、款項已扣、webhook 已觸發、檔案已寫入、裝置設定已變更。
- **重試會重複執行。** 整條 chain 重跑時 DB 乾淨重來，但外部呼叫會第二次發生。外部呼叫必須自帶 idempotency key，否則會產生重複扣款、重複通知。
- **跨系統狀態不一致。** DB 認為這筆資料不存在，第三方系統卻已經有了，而且沒有任何機制會自動收斂。

**在 Compensate 機制實作之前，請遵守：**

1. 把 `external_api` / `file` / `device` 的 mutation 放在 chain 的**最後一個** Pipeline，減少「它之後還有東西會失敗」的機會。
2. 不可逆或高風險的外部呼叫（付款、發送個資、實體裝置控制）**不要放進 Atomic Chain**；改由獨立的 workflow 在 DB 確定 commit 之後才觸發。
3. 若流程本質上就沒有跨系統原子性，改用 Sequential Chain，明確承認這件事，不要用 Atomic Chain 製造「有被保護」的錯覺。
4. 所有外部呼叫都要能安全重試（idempotency key 或去重機制）。

Compensate Pipeline（執行反向操作，例如發送「註冊失敗」通知）為未來擴展點，將在後續版本中實作。**在它完成之前，上面四點是唯一的保護。**

---

## 測試

```typescript
// tests/steps/user-register.test.ts
import { makeFetchPlanLimits } from "../../steps/user-register";
import type { Ctx } from "../../core/types";
import type { PlanQueryFn } from "../../core/protocols";

const fakePlanQuery: PlanQueryFn = async (_db, _planId) => ({
  maxUsers: 10,
  currentUsers: 5,
});

test("fetchPlanLimits should return StepContinue with scratch", async () => {
  const step = makeFetchPlanLimits(fakePlanQuery);
  const ctx: Ctx = { db: {} as DB, input: { planId: "p1" } };
  const result = await step(ctx, {});
  expect(result._tag).toBe("StepContinue");
  expect(result.scratch).toEqual({
    planLimits: { maxUsers: 10, currentUsers: 5 },
  });
});
```

---

## TypeScript 特有注意事項

### `_tag` 欄位是必要的

TypeScript 是結構型別（structural typing），`interface` 編譯後不存在，執行期沒有任何東西可以判斷「這個物件是不是 StepStop」。因此三態回傳值都需要一個字串字面量的 `_tag` 欄位，靠 `result._tag === "StepStop"` 讓編譯器做 narrowing。

> Python 版**沒有**這個欄位（名義型別可直接用 `isinstance` narrowing）。不要把 `_tag` 帶進 Python 實作。

### `buildCtx` 的 `as` 轉型是刻意的

`PipelineStep.buildCtx` 的型別是兩種簽名的 union，但 Chain 是用陣列位置判斷該用哪一種簽名呼叫，型別系統無法靜態驗證。程式碼中的 `as FirstBuildCtxFn<TInput>` / `as NextBuildCtxFn` 是必要的斷言，不是可以省略的雜訊。

寫 Service 的 steps 陣列時，第一個元素通常需要 `as PipelineStep<TInput>` 才能讓 TS 接受兩參數的 `buildCtx`。

### 同步／非同步可以自由混用

`await` 一個非 Promise 的值在 JavaScript 完全合法，直接回傳該值。因此 Step 可以是同步函式或 async 函式，Engine 的 `instanceof Promise` 檢查其實可以省略；保留它只是為了讓意圖明確。

### Express 沒有執行期驗證

`req.body as UserRegisterRequest` 只是編譯期斷言，執行期不做任何檢查。如果需要驗證，得自己加 middleware（zod、class-validator 等）。

> FastAPI 版本則是自動驗證的，這是兩者的實質差異之一。
