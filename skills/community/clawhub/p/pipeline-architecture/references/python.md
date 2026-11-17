# Pipeline Architecture — Python／FastAPI 實作參考

> 架構規則請看 `SKILL.md`。本檔只提供 Python 的程式碼範例。
> 若專案是 TypeScript，請改讀 `references/typescript.md`，不要混用。

**環境假設：** Python 3.11+、FastAPI、SQLAlchemy 2.x（async）、Pydantic v2、pytest + pytest-asyncio。

## 目錄

- [Python 端的五項設計決議](#python-端的五項設計決議)
- [目錄結構](#目錄結構)
- [core/types.py](#coretypespy)
- [Layer 1 — Route](#layer-1--route)
- [Layer 2 — Service](#layer-2--service)
- [Layer 3 — Pipeline Chain](#layer-3--pipeline-chain)
- [Layer 4 — Pipeline](#layer-4--pipeline)
- [Layer 5 — Engine](#layer-5--engine)
- [Layer 6 — Step](#layer-6--step)
- [Layer 7 — Query](#layer-7--query)
- [Layer 8 — Persistence](#layer-8--persistence)
- [測試](#測試)
- [Python 特有陷阱](#python-特有陷阱)

---

## Python 端的五項設計決議

這五項是 Python 與 TypeScript 語意本身不同、必須各自決定的地方。**已定案，不要重新發明：**

| 主題 | 決議 | 理由 |
|---|---|---|
| **三態回傳值** | `StepContinue` / `StepStop` / `StepCommit` 用 `@dataclass(frozen=True)`，**不加 `_tag` 欄位**，靠 `isinstance` narrowing；`DataMutation` 與 Route 層 schema 用 **Pydantic** | Python 是名義型別，執行期就有型別資訊，`_tag` 是 TypeScript 用來彌補結構型別的補丁，不該搬過來。Pydantic 只用在跨邊界、需要驗證與序列化的物件 |
| **測試邊界介面** | `typing.Protocol` + `async def __call__`，不用 `Callable[...]` | `Callable` 會丟失參數名稱；`Protocol` 保留參數名稱這層契約，也能寫 docstring |
| **同步／非同步** | 允許混用。純決策 Step 寫成一般 `def`，需要 I/O 的寫成 `async def`；Engine 用 `inspect.isawaitable` 判斷 | 大多數 Step 是純決策，強制全 async 會讓大量測試無謂地變成 async |
| **Transaction** | `execute_mutation(session, mutation)` **沒有 tx 參數**；Atomic 用 `async with session.begin()` + 私有 `_ChainAbort` 例外；Sequential 每個 Pipeline 後自己 `commit()` | `AsyncSession` 本身就是 unit of work，沒有獨立 tx 物件。**在 `async with` 內用 `return` 會誤觸發 commit**，必須用例外離開 |
| **Route 層** | FastAPI `APIRouter` + `Depends(get_session)`；用 `response.status_code` 動態設定狀態碼；**業務 4xx 不轉成 `HTTPException`** | 保留 OpenAPI 文件價值，同時維持「4xx 是回傳值不是例外」的架構語意 |

---

## 目錄結構

```
project/
├── routes/                 # HTTP 入口，薄層（FastAPI APIRouter）
├── services/               # Orchestrator：run_workflow（import 時用 as 加入 domain 名）
├── pipelines/              # 純宣告：make_pipeline（import 時用 as 加入 domain 名）
├── steps/
│   ├── {domain}.py         # 各 domain 的 steps
│   ├── common.py           # 跨 domain 共用的 steps（知道 ctx/scratch 介面）
│   └── utils.py            # 純工具函式（不知道任何 Step 或 domain 概念）
├── queries/                # 純讀取：依功能命名，不套用固定通用名稱
├── schemas/                # 各 domain 的 Request / Output / Failure / Ctx
├── core/
│   ├── engine.py           # PipelineEngine（不因業務修改）
│   ├── pipeline_chain.py   # run_atomic_chain / run_sequential_chain
│   ├── exceptions.py       # PipelineExecutionError
│   ├── protocols.py        # Protocol 定義
│   └── types.py            # StepContinue, StepStop, StepCommit, DataMutation …
├── persistence/            # 單一寫入層
└── tests/
    ├── steps/              # 單元測試：stub ctx + scratch，用 fake 實作
    ├── queries/            # 單元測試：用 in-memory DB 或 fake
    └── services/           # 整合測試：跑完整 pipeline chain
```

> ⚠️ **不要用 `types/` 當目錄名。** TypeScript 版用的是 `types/`，但在 Python 專案根目錄放一個 `types` 套件會遮蔽標準函式庫的 `types` 模組，造成難以除錯的 import 錯誤。Python 端一律用 **`schemas/`**。

---

## core/types.py

```python
# core/types.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Literal, Protocol

from pydantic import BaseModel, ConfigDict

# ── 意圖 Schema ───────────────────────────────────────────────────

MutationTarget = Literal["database", "file", "device", "external_api"]
MutationOperation = Literal["create", "update", "delete"]


class DataMutation(BaseModel):
    """寫入意圖。

    before/after 的語意：
    - create: before=None, after=新資料
    - update: before=變更前（由 Persistence 擷取）, after=變更後
    - delete: before=刪除前資料, after=None

    注意：Pipeline 內的 Step 宣告的是「意圖」。before 在宣告階段可能為 None，
    真正的 before 由 Persistence 在執行前擷取並記錄。

    DataMutation 是封閉的 schema：只包含以下欄位。StepCommit 組裝時不應該、
    也不能夾帶 schema 之外的暫存欄位（那些屬於 scratch 的職責）。
    用 Pydantic 而非 dataclass，是因為它會被寫進 intent log（需要序列化），
    且是跨層邊界的物件（需要驗證）。
    """

    model_config = ConfigDict(frozen=True)

    entity: str
    target: MutationTarget
    operation: MutationOperation
    before: dict[str, Any] | None
    after: dict[str, Any] | None
    changed_fields: list[str]
    performed_by: str
    reason: str


# ── Step 回傳值 ──────────────────────────────────────────────────
#
# 用 dataclass 而非 Pydantic：這三個型別從不離開行程、不需要驗證，
# 每個 Step 都會建立一次，不該為純控制流付驗證成本。
# 也不需要 _tag 欄位 —— Python 是名義型別，isinstance 就能完美 narrowing。


@dataclass(frozen=True)
class StepContinue:
    """繼續執行下一個 Step。

    scratch 是中繼資料，僅供後續 Step 讀取判斷之用。
    不是 DataMutation 的一部分，Engine 不會把它併入最終寫入意圖。
    """

    scratch: dict[str, Any] | None = None


@dataclass(frozen=True)
class StepStop:
    """終止 Pipeline，無寫入意圖。

    兩種情境：業務拒絕（4xx）、成功的純查詢結束（2xx）。
    """

    status: int
    output: Any


@dataclass(frozen=True)
class StepCommit:
    """終止 Pipeline，帶著完整寫入意圖。

    mutation 必須是完整且型別明確的 DataMutation，
    不會、也不能與先前 StepContinue 累積的 scratch 合併。
    """

    status: int
    output: Any
    mutation: DataMutation


StepResult = StepContinue | StepStop | StepCommit


# ── Step 函式型別 ────────────────────────────────────────────────


class Step(Protocol):
    """Pipeline 內的最小執行單元。

    可以是同步函式或 async 函式，Engine 會自動判斷（見 core/engine.py）。
    scratch 是目前為止 StepContinue 累積下來的中繼資料。
    """

    def __call__(
        self, ctx: Any, scratch: dict[str, Any]
    ) -> StepResult | Awaitable[StepResult]: ...


# ── Trace ─────────────────────────────────────────────────────────

TraceSpanStatus = Literal["continue", "stop", "commit", "error"]


@dataclass(frozen=True)
class TraceSpan:
    step: str
    status: TraceSpanStatus
    duration_ms: float
    started_at: float  # epoch 秒，用於與外部 log 對齊


# ── Pipeline 執行結果 ─────────────────────────────────────────────


@dataclass(frozen=True)
class PipelineResult:
    output: Any
    status: int
    spans: list[TraceSpan]
    mutation: DataMutation | None


# ── Persistence 執行結果 ──────────────────────────────────────────


@dataclass(frozen=True)
class MutationResult:
    """真實寫入後的結果。

    after 包含資料庫自動生成的欄位（id、created_at、version 等）。

    目前寫入失敗一律以例外處理（由 Chain 攔截並回滾），因此本型別只描述
    成功寫入後的結果，不包含 success 欄位。若未來需要區分「失敗但不拋例外」
    的情境（例如 Compensate 機制），屆時應以 discriminated union
    （MutationSuccess | MutationFailure）重新設計，而非加回一個布林旗標。
    """

    before: dict[str, Any] | None
    after: dict[str, Any] | None
    diff: dict[str, Any]
    intent_log_id: str
    result_log_id: str


@dataclass(frozen=True)
class PersistenceResult:
    output: Any
    status: int
    spans: list[TraceSpan]
    mutation_result: MutationResult | None
```

---

## Layer 1 — Route

```python
# routes/user_register.py
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from schemas.user_register import (
    RegisterFailure,
    RegisterOutput,
    UserRegisterRequest,
)
from services.user_register import run_workflow as run_user_register_workflow

router = APIRouter()


@router.post(
    "/users/register",
    response_model=RegisterOutput | RegisterFailure,
    responses={
        409: {"model": RegisterFailure, "description": "Email 已被註冊"},
        404: {"model": RegisterFailure, "description": "找不到方案"},
    },
)
async def register_user(
    body: UserRegisterRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> RegisterOutput | RegisterFailure:
    result = await run_user_register_workflow(session=session, body=body)
    # 動態狀態碼：注入 Response 物件改 status_code，
    # 這樣仍保留 response_model 與 OpenAPI 文件。
    response.status_code = result.status
    return result.output
```

**規則：**
- 只做 request 解析 + 呼叫 Service（import 時用 `as` 加入 domain 名稱）
- 不含任何 if、DB 呼叫、業務判斷
- request schema 用 Pydantic model，FastAPI 會自動驗證，格式錯誤直接回 422，進不到 Service
- ❌ **業務拒絕不要 `raise HTTPException`**。4xx 是 `StepStop` 的回傳**值**，改丟例外等於繞過 `PersistenceResult` 契約，`spans` 也會遺失
- ❌ 不回傳 ORM model，永遠回傳 Pydantic response schema

> **union response_model 的前提：** 成功與失敗的 schema 必須在欄位上可區分（例如 `RegisterOutput` 有 `user_id`、`RegisterFailure` 有 `code`）。若兩者形狀太接近，Pydantic 的 smart union 可能選錯 model —— 這時改用 `response_model=None` + 回傳 `JSONResponse`。

---

## Layer 2 — Service

### Atomic Chain 範例

```python
# services/user_register.py
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.pipeline_chain import PipelineStep, run_atomic_chain
from core.types import MutationResult, PersistenceResult
from pipelines.user_register import make_pipeline as make_user_register_pipeline
from pipelines.welcome_email import make_pipeline as make_welcome_email_pipeline
from pipelines.workspace_create import make_pipeline as make_workspace_create_pipeline
from schemas.user_register import RegisterCtx, UserRegisterRequest
from schemas.welcome_email import WelcomeCtx
from schemas.workspace_create import WorkspaceCtx


# ── ctx 建構函式 ──────────────────────────────────────────────────
# 第一個 Pipeline：(session, initial_input) -> Ctx


def build_register_ctx(
    session: AsyncSession,
    initial_input: UserRegisterRequest,
) -> RegisterCtx:
    return RegisterCtx(session=session, input=initial_input)


# 後續 Pipeline：(session, previous_output, mutation_result) -> Ctx


def build_workspace_ctx(
    session: AsyncSession,
    previous_output: Any,
    mutation_result: MutationResult | None,
) -> WorkspaceCtx:
    assert mutation_result is not None  # 前一個 Pipeline 必為 StepCommit
    return WorkspaceCtx(session=session, user=mutation_result.after)


def build_welcome_ctx(
    session: AsyncSession,
    previous_output: Any,
    mutation_result: MutationResult | None,
) -> WelcomeCtx:
    assert mutation_result is not None
    return WelcomeCtx(session=session, user=mutation_result.after)


# ── workflow ─────────────────────────────────────────────────────


async def run_workflow(
    session: AsyncSession,
    body: UserRegisterRequest,
) -> PersistenceResult:
    return await run_atomic_chain(
        session=session,
        steps=[
            PipelineStep(
                make_pipeline=make_user_register_pipeline,
                build_ctx=build_register_ctx,
            ),
            PipelineStep(
                make_pipeline=make_workspace_create_pipeline,
                build_ctx=build_workspace_ctx,
            ),
            PipelineStep(
                make_pipeline=make_welcome_email_pipeline,
                build_ctx=build_welcome_ctx,
            ),
        ],
        initial_input=body,
    )
```

### Sequential Chain 範例

```python
# services/audit_workflow.py
from sqlalchemy.ext.asyncio import AsyncSession

from core.pipeline_chain import PipelineStep, run_sequential_chain
from core.types import PersistenceResult
from pipelines.log_access import make_pipeline as make_log_access_pipeline
from pipelines.update_last_seen import make_pipeline as make_update_last_seen_pipeline
from schemas.audit import AuditInput


async def run_workflow(
    session: AsyncSession,
    body: AuditInput,
) -> PersistenceResult:
    return await run_sequential_chain(
        session=session,
        steps=[
            PipelineStep(
                make_pipeline=make_log_access_pipeline,
                build_ctx=build_log_ctx,
            ),
            PipelineStep(
                make_pipeline=make_update_last_seen_pipeline,
                build_ctx=build_last_seen_ctx,
            ),
        ],
        initial_input=body,
    )
```

**規則：**
- Service 永遠使用 `run_atomic_chain` 或 `run_sequential_chain`，不手動呼叫 Engine 或 Persistence
- `build_ctx` 寫成**具名函式**（不要用 lambda），簽名才看得清楚、也才能被型別檢查
- Service 不寫業務邏輯，只做 Pipeline 鏈的宣告與 `initial_input` 的傳遞

> ⚠️ **`build_ctx` 是同步函式，不能查 DB。** Ctx 的內容只能來自 `initial_input`、上一個 Pipeline 的 `mutation_result`，或其他同步來源。任何 DB 讀取都必須放進 Step，透過 Query 執行。

---

## Layer 3 — Pipeline Chain

```python
# core/pipeline_chain.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from core.engine import PipelineEngine
from core.types import MutationResult, PersistenceResult, Step, TraceSpan
from persistence import execute_mutation


# ── build_ctx 的兩種簽名 ─────────────────────────────────────────


class FirstBuildCtxFn(Protocol):
    """第一個 Pipeline 的 build_ctx 簽名。

    initial_input 是呼叫端傳給 chain 的原始輸入（尚未轉換成 Ctx）。
    """

    def __call__(self, session: AsyncSession, initial_input: Any) -> Any: ...


class NextBuildCtxFn(Protocol):
    """第二個及之後的 Pipeline 的 build_ctx 簽名。

    mutation_result 是上一個 Pipeline 的真實寫入結果；
    若上一個 Pipeline 為 StepStop（無 mutation），則為 None。
    """

    def __call__(
        self,
        session: AsyncSession,
        previous_output: Any,
        mutation_result: MutationResult | None,
    ) -> Any: ...


BuildCtxFn = FirstBuildCtxFn | NextBuildCtxFn


@dataclass(frozen=True)
class PipelineStep:
    """宣告一個 Pipeline 及其在鏈中的 ctx 建構方式。"""

    make_pipeline: Callable[[AsyncSession], list[Step]]
    # build_ctx 的簽名依本項在 steps 清單中的位置而定：
    # 第一個用 FirstBuildCtxFn，其餘用 NextBuildCtxFn。
    # 型別系統無法靜態驗證這件事，寫清單時要自己確認。
    build_ctx: BuildCtxFn
    # 即使前一個 Pipeline 為 StepStop（無 mutation），是否仍強制執行本 Pipeline。
    # 適用於稽核日誌等 side-effect。
    always_run: bool = False


class _ChainAbort(Exception):
    """僅供本檔案內部控制流使用，絕不外流到其他層。

    存在理由：`async with session.begin()` 只有在「以例外離開」時才 rollback，
    用 return 提前離開會被判定為正常結束而 COMMIT。業務拒絕（4xx）必須回滾，
    所以只能用拋例外的方式離開 with 區塊，再於外層攔截並轉回正常回傳值。
    """

    def __init__(self, result: PersistenceResult) -> None:
        super().__init__()
        self.result = result


def _build_ctx_for(
    step: PipelineStep,
    *,
    session: AsyncSession,
    is_first: bool,
    initial_input: Any,
    last_output: Any,
    last_mutation_result: MutationResult | None,
) -> Any:
    """在 Pipeline 即將執行前，現場建構它的 ctx。

    不預先建好一整串 ctx，也不在上一步結束時提前建構下一步的 ctx。
    """
    if is_first:
        return step.build_ctx(session, initial_input)
    return step.build_ctx(session, last_output, last_mutation_result)


# ── Atomic Chain ──────────────────────────────────────────────────


async def run_atomic_chain(
    session: AsyncSession,
    steps: list[PipelineStep],
    initial_input: Any,
) -> PersistenceResult:
    """所有 Pipeline 在同一個 session transaction 內執行。

    全部成功才 commit；任何失敗（業務拒絕或例外）則整條鏈 rollback。
    """
    engine = PipelineEngine()
    all_spans: list[TraceSpan] = []
    last_output: Any = None
    last_status: int | None = None
    last_mutation_result: MutationResult | None = None

    try:
        async with session.begin():
            for i, step in enumerate(steps):
                is_first = i == 0

                # 前一個 Pipeline 為 StepStop 且本步驟不是 always_run → 跳過
                if not is_first and last_mutation_result is None and not step.always_run:
                    continue

                ctx = _build_ctx_for(
                    step,
                    session=session,
                    is_first=is_first,
                    initial_input=initial_input,
                    last_output=last_output,
                    last_mutation_result=last_mutation_result,
                )

                result = await engine.execute(step.make_pipeline(session), ctx)

                if result.mutation is None:
                    # StepStop：Pipeline 決定終止但不寫入
                    last_output = result.output
                    last_status = result.status
                    all_spans.extend(result.spans)

                    if result.status >= 400:
                        # 業務拒絕 → 必須「拋例外」離開 async with 才會 rollback。
                        # 這裡若改成 return，SQLAlchemy 會判定為正常結束而 COMMIT。
                        raise _ChainAbort(
                            PersistenceResult(
                                output=result.output,
                                status=result.status,
                                spans=all_spans,
                                mutation_result=None,
                            )
                        )
                    # 成功但不需寫入（2xx），繼續下一個 Pipeline
                    continue

                # StepCommit：在同一個 transaction 內執行寫入
                last_mutation_result = await execute_mutation(session, result.mutation)
                all_spans.extend(result.spans)
                last_output = result.output
                last_status = result.status
        # 正常離開 async with → SQLAlchemy 自動 commit
    except _ChainAbort as abort:
        # 例外已使 async with 觸發 rollback，這裡只負責轉回正常回傳值
        return abort.result
    # 其他例外（含 PipelineExecutionError）同樣已觸發 rollback，直接往上拋

    return PersistenceResult(
        output=last_output,
        status=last_status if last_status is not None else 200,
        spans=all_spans,
        mutation_result=last_mutation_result,
    )


# ── Sequential Chain ──────────────────────────────────────────────


async def run_sequential_chain(
    session: AsyncSession,
    steps: list[PipelineStep],
    initial_input: Any,
) -> PersistenceResult:
    """每個 Pipeline 獨立 commit，失敗不影響已完成的 Pipeline。

    注意：沒有 transaction。中途失敗時，已 commit 的 Pipeline 不會回滾。
    """
    engine = PipelineEngine()
    all_spans: list[TraceSpan] = []
    last_output: Any = None
    last_status: int | None = None
    last_mutation_result: MutationResult | None = None

    for i, step in enumerate(steps):
        is_first = i == 0

        if not is_first and last_mutation_result is None and not step.always_run:
            continue

        ctx = _build_ctx_for(
            step,
            session=session,
            is_first=is_first,
            initial_input=initial_input,
            last_output=last_output,
            last_mutation_result=last_mutation_result,
        )

        result = await engine.execute(step.make_pipeline(session), ctx)

        if result.mutation is None:
            last_output = result.output
            last_status = result.status
            all_spans.extend(result.spans)

            if result.status >= 400:
                # 業務拒絕 → 停止執行後續 Pipeline。
                # 這裡用 return 是安全的：沒有 async with，不會誤觸發 commit。
                # 注意：已 commit 的 Pipeline 不會 rollback。
                return PersistenceResult(
                    output=result.output,
                    status=result.status,
                    spans=all_spans,
                    mutation_result=None,
                )
            continue

        # StepCommit：立即執行寫入並各自 commit
        last_mutation_result = await execute_mutation(session, result.mutation)
        await session.commit()
        all_spans.extend(result.spans)
        last_output = result.output
        last_status = result.status

    return PersistenceResult(
        output=last_output,
        status=last_status if last_status is not None else 200,
        spans=all_spans,
        mutation_result=last_mutation_result,
    )
```

> **`always_run` 為什麼不需要特別分支？** ctx 一律在迴圈開頭現場建構，`last_mutation_result` 本來就會是 `None`（前一個是 StepStop 時），`NextBuildCtxFn` 直接收到 `None`。不管前一步是成功寫入還是 StepStop，`build_ctx` 都會被正確呼叫。

---

## Layer 4 — Pipeline

```python
# pipelines/user_register.py
from sqlalchemy.ext.asyncio import AsyncSession

from core.types import Step
from queries.plan import query_plan_limits
from steps.user_register import (
    build_commit,
    check_email_not_taken,
    ensure_registration_allowed,
    make_fetch_plan_limits,
)


def make_pipeline(session: AsyncSession) -> list[Step]:
    return [
        check_email_not_taken,
        make_fetch_plan_limits(query_plan_limits),
        ensure_registration_allowed,
        build_commit,
    ]
```

**規則：** 只有 list。沒有 `if`、沒有 `await`、沒有業務邏輯。
用 `make_*` 工廠函式注入 Query 依賴進 Step。

---

## Layer 5 — Engine

```python
# core/engine.py
import inspect
import time
from typing import Any

from core.exceptions import PipelineExecutionError
from core.types import (
    PipelineResult,
    Step,
    StepCommit,
    StepResult,
    StepStop,
    TraceSpan,
)


class PipelineEngine:
    async def execute(self, steps: list[Step], ctx: Any) -> PipelineResult:
        # accumulated_scratch 只是 Step 之間傳遞的中繼資料，
        # 不是最終 DataMutation 的草稿。
        accumulated_scratch: dict[str, Any] = {}
        spans: list[TraceSpan] = []

        for step in steps:
            name = getattr(step, "__name__", None) or type(step).__name__
            started_at = time.time()
            t0 = time.perf_counter()

            try:
                result = await self._call(step, ctx, accumulated_scratch)
            except Exception as err:
                spans.append(
                    TraceSpan(
                        step=name,
                        status="error",
                        duration_ms=(time.perf_counter() - t0) * 1000,
                        started_at=started_at,
                    )
                )
                raise PipelineExecutionError(name, spans, err) from err

            duration_ms = (time.perf_counter() - t0) * 1000

            if isinstance(result, StepStop):
                spans.append(
                    TraceSpan(
                        step=name,
                        status="stop",
                        duration_ms=duration_ms,
                        started_at=started_at,
                    )
                )
                return PipelineResult(
                    output=result.output,
                    status=result.status,
                    spans=spans,
                    mutation=None,
                )

            if isinstance(result, StepCommit):
                # StepCommit 已經是完整、型別明確的 DataMutation，
                # 不與 accumulated_scratch 合併 —— 避免中繼資料（如 plan_limits）
                # 污染最終送進 Persistence 的寫入意圖。
                spans.append(
                    TraceSpan(
                        step=name,
                        status="commit",
                        duration_ms=duration_ms,
                        started_at=started_at,
                    )
                )
                return PipelineResult(
                    output=result.output,
                    status=result.status,
                    spans=spans,
                    mutation=result.mutation,
                )

            # StepContinue
            if result.scratch:
                # shallow merge：後宣告的 Step 覆蓋前面的值。
                # 這裡合併的是 scratch，僅供後續 Step 讀取判斷，不會流入 mutation。
                accumulated_scratch = {**accumulated_scratch, **result.scratch}
            spans.append(
                TraceSpan(
                    step=name,
                    status="continue",
                    duration_ms=duration_ms,
                    started_at=started_at,
                )
            )

        raise RuntimeError("Pipeline finished without StepStop or StepCommit")

    @staticmethod
    async def _call(step: Step, ctx: Any, scratch: dict[str, Any]) -> StepResult:
        """同時支援同步與 async Step。

        Python 的 await 不能用在非 awaitable 物件上（會拋 TypeError），
        所以這個判斷是必要的，不像 TypeScript 可以省略。
        """
        result = step(ctx, scratch)
        if inspect.isawaitable(result):
            return await result
        return result
```

```python
# core/exceptions.py
from core.types import TraceSpan


class PipelineExecutionError(Exception):
    def __init__(
        self,
        step_name: str,
        spans: list[TraceSpan],
        original_error: Exception,
    ) -> None:
        super().__init__(f"Step '{step_name}' failed: {original_error}")
        self.step_name = step_name
        self.spans = spans
        self.original_error = original_error
```

**規則：** 不因任何業務需求修改 Engine。`StepCommit.mutation` 已經是 `DataMutation`，Engine 不需要（也不應該）做任何型別轉換。

---

## Layer 6 — Step

### steps/common.py — 跨 domain 共用

```python
# steps/common.py
from typing import Any

from core.types import StepContinue, StepStop
from schemas.shared import PermissionFailure


def check_admin_permission(ctx: Any, scratch: dict[str, Any]) -> StepContinue | StepStop:
    """純決策 Step：不碰 I/O，寫成一般函式即可。"""
    if ctx.user.role != "admin":
        return StepStop(
            status=403,
            output=PermissionFailure(code="PERMISSION_DENIED", message="權限不足"),
        )
    return StepContinue()


def check_rate_limit(ctx: Any, scratch: dict[str, Any]) -> StepContinue | StepStop:
    if ctx.rate_limit.remaining <= 0:
        return StepStop(
            status=429,
            output=PermissionFailure(code="RATE_LIMIT_EXCEEDED", message="請求過於頻繁"),
        )
    return StepContinue()
```

### steps/utils.py — 純工具函式

```python
# steps/utils.py
from datetime import datetime, timezone


def format_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def truncate_string(s: str, max_len: int) -> str:
    return s[:max_len] if len(s) > max_len else s


def mask_email(email: str) -> str:
    local, _, domain = email.partition("@")
    return f"{local[0]}***@{domain}"
```

### schemas/{domain}.py — domain 型別與 Ctx

```python
# schemas/user_register.py
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


class UserRegisterRequest(BaseModel):
    """Route 層的 request schema，FastAPI 自動驗證。"""

    email: str
    name: str
    plan_id: str


class RegisterOutput(BaseModel):
    user_id: str
    message: str


class RegisterFailure(BaseModel):
    code: str
    message: str


@dataclass(frozen=True)
class RegisterCtx:
    """本 domain 的 Ctx，由 services 層的 build_ctx 建構。

    Ctx 用 dataclass 而非 Pydantic：它不跨行程邊界、不需要驗證，
    而且要放進 AsyncSession 這種不可序列化的物件。
    """

    session: AsyncSession
    input: UserRegisterRequest
    existing_user: dict[str, Any] | None = None
```

### steps/{domain}.py — Domain Step

```python
# steps/user_register.py
from typing import Any

from core.protocols import PlanQueryFn
from core.types import DataMutation, Step, StepCommit, StepContinue, StepStop
from schemas.user_register import RegisterCtx, RegisterFailure, RegisterOutput


def check_email_not_taken(
    ctx: RegisterCtx,
    scratch: dict[str, Any],
) -> StepContinue | StepStop:
    """純決策 Step：一般 def，測試不需要 async。"""
    if ctx.existing_user is not None:
        return StepStop(
            status=409,
            output=RegisterFailure(code="EMAIL_TAKEN", message="此 Email 已被註冊"),
        )
    return StepContinue()


def make_fetch_plan_limits(query_fn: PlanQueryFn) -> Step:
    """工廠函式：注入 Query 依賴。

    內層函式要取有意義的名字（不要叫 step 或用 lambda），
    Engine 讀 __name__ 產生 trace span，否則所有 span 都會叫同一個名字。
    """

    async def fetch_plan_limits(
        ctx: RegisterCtx,
        scratch: dict[str, Any],
    ) -> StepContinue | StepStop:
        limits = await query_fn(ctx.session, ctx.input.plan_id)
        if limits is None:
            return StepStop(
                status=404,
                output=RegisterFailure(code="PLAN_NOT_FOUND", message="找不到方案"),
            )
        # plan_limits 只是給下一個 Step 判斷用的中繼資料，
        # 放進 scratch，不是 DataMutation 的欄位。
        return StepContinue(scratch={"plan_limits": limits})

    return fetch_plan_limits


def ensure_registration_allowed(
    ctx: RegisterCtx,
    scratch: dict[str, Any],
) -> StepContinue | StepStop:
    limits: dict[str, int] = scratch.get("plan_limits") or {}
    max_users = limits.get("max_users", 0)
    current_users = limits.get("current_users", 0)
    if max_users <= current_users:
        return StepStop(
            status=422,
            output=RegisterFailure(
                code="PLAN_LIMIT_REACHED", message="已達方案人數上限"
            ),
        )
    return StepContinue()


def build_commit(ctx: RegisterCtx, scratch: dict[str, Any]) -> StepCommit:
    """mutation 是完整、乾淨的 DataMutation，只包含 schema 定義的欄位，
    不會夾帶 scratch 裡的 plan_limits 等中繼資料。
    """
    return StepCommit(
        status=201,
        output=RegisterOutput(user_id=ctx.input.email, message="註冊成功"),
        mutation=DataMutation(
            entity="user",
            target="database",
            operation="create",
            before=None,
            after={"email": ctx.input.email, "name": ctx.input.name},
            changed_fields=["email", "name"],
            performed_by="system",
            reason="user_self_register",
        ),
    )
```

**Step 規則：**
- Step 不直接呼叫 DB，只呼叫 Query 函式
- Step 不 import 其他 Step
- Step 不宣告 `next_pipeline`（Pipeline 串接由 Service 決定）
- 一個 Pipeline 通常只有一個 StepCommit，放在最後
- 純決策 Step 用一般 `def`；只有真的需要 `await` 才用 `async def`

---

## Layer 7 — Query

```python
# queries/user.py
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def query_by_email(session: AsyncSession, email: str) -> dict[str, Any] | None:
    row = (
        (
            await session.execute(
                text("SELECT id, email, name FROM users WHERE email = :email"),
                {"email": email},
            )
        )
        .mappings()
        .first()
    )
    return dict(row) if row is not None else None


async def query_by_id(session: AsyncSession, user_id: str) -> dict[str, Any] | None:
    row = (
        (
            await session.execute(
                text("SELECT id, email, name FROM users WHERE id = :user_id"),
                {"user_id": user_id},
            )
        )
        .mappings()
        .first()
    )
    return dict(row) if row is not None else None
```

```python
# core/protocols.py
from typing import Any, Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class UserQueryFn(Protocol):
    """依 email 查詢使用者。回傳 None 表示不存在。"""

    async def __call__(
        self, session: AsyncSession, email: str
    ) -> dict[str, Any] | None: ...


class PlanQueryFn(Protocol):
    """查詢方案限制。回傳 None 表示方案不存在。"""

    async def __call__(
        self, session: AsyncSession, plan_id: str
    ) -> dict[str, Any] | None: ...
```

**Query 可讀取的來源：** DB、runtime 變數（如 `time.time()`、`os.environ`）、外部 API（GET）、裝置狀態、純計算

**規則：**
- 不接受 `ctx` 或 `scratch`，只接受原始值
- 不回傳 Step 三態
- 絕對不執行任何寫入
- **回傳 `dict` 而不是 ORM model** —— 避免 ORM 物件穿透層邊界（在 SQLAlchemy 還有一個附帶好處：commit 後 ORM 物件會過期，dict 不會）

---

## Layer 8 — Persistence

### 結構選擇

**Domain 少於 5 種 → Option A（扁平結構）**

```
persistence/
├── __init__.py         # execute_mutation 入口，負責分派到各 target
├── database.py         # SQL / ORM 實作
├── file.py             # 本機檔案讀寫
├── device.py           # 裝置 / 主機變數
└── external_api.py     # 外部 API 呼叫
```

**Domain 超過 5 種 → Option B（加入 Repository 層）**

```
persistence/
├── __init__.py             # execute_mutation 入口
├── adapters/               # 各 target 的寫入實作
│   ├── database.py
│   ├── file.py
│   ├── device.py
│   └── external_api.py
└── repositories/           # 各 domain 的具體 SQL / schema 實作
    ├── user.py             # 知道 users table 的結構
    └── order.py
```

### 入口（兩個 Option 共用）

```python
# persistence/__init__.py
import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.types import DataMutation, MutationResult
from persistence.adapters.database import apply_db_mutation
from persistence.adapters.device import apply_device_mutation
from persistence.adapters.external_api import apply_api_mutation
from persistence.adapters.file import apply_file_mutation
from persistence.logs import log_intent, log_result


async def execute_mutation(
    session: AsyncSession,
    mutation: DataMutation,
) -> MutationResult:
    """執行一筆 DataMutation。

    mutation 已經是乾淨、型別明確的 DataMutation，不含任何 scratch 中繼資料。

    ⚠️ 本函式不負責 commit。transaction 邊界由 Chain 決定：
    - run_atomic_chain：整條鏈共用一個 session transaction，離開時統一 commit
    - run_sequential_chain：每個 Pipeline 執行完後自己 commit

    （TypeScript 版的簽名有第三個 tx 參數；Python 端不需要，
    因為 AsyncSession 本身就攜帶 transaction 狀態。）
    """
    intent_log_id = str(uuid.uuid4())
    await log_intent(session, intent_log_id, mutation)

    before, after = await _apply_mutation(session, mutation)

    diff = {
        key: value
        for key, value in (after or {}).items()
        if (before or {}).get(key) != value
    }

    result_log_id = str(uuid.uuid4())
    await log_result(session, result_log_id, intent_log_id, before, after, diff)

    return MutationResult(
        before=before,
        after=after,
        diff=diff,
        intent_log_id=intent_log_id,
        result_log_id=result_log_id,
    )


async def _apply_mutation(
    session: AsyncSession,
    mutation: DataMutation,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    match mutation.target:
        case "database":
            return await apply_db_mutation(session, mutation)
        case "file":
            return await apply_file_mutation(mutation)
        case "device":
            return await apply_device_mutation(mutation)
        case "external_api":
            return await apply_api_mutation(mutation)
        case _:
            raise ValueError(f"Unknown mutation target: {mutation.target}")
```

> **`MutationResult.after` 是真實寫入後的狀態**，包含資料庫自動生成的欄位（id、created_at、version 等）。Chain 把此值傳給下一個 Pipeline 作為 ctx 基礎，**不能**用 `DataMutation.after`（意圖中的 after）代替。

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

### 同步 Step —— 不需要 async

```python
# tests/steps/test_user_register.py
from core.types import StepContinue, StepStop
from schemas.user_register import RegisterCtx, UserRegisterRequest
from steps.user_register import check_email_not_taken, ensure_registration_allowed


def _make_ctx(**overrides) -> RegisterCtx:
    return RegisterCtx(
        session=None,  # type: ignore[arg-type]  # 純決策 Step 不碰 session
        input=UserRegisterRequest(email="a@b.com", name="A", plan_id="p1"),
        **overrides,
    )


def test_check_email_not_taken_stops_when_user_exists() -> None:
    result = check_email_not_taken(_make_ctx(existing_user={"id": "u1"}), {})
    assert isinstance(result, StepStop)
    assert result.status == 409


def test_ensure_registration_allowed_reads_scratch() -> None:
    scratch = {"plan_limits": {"max_users": 10, "current_users": 5}}
    result = ensure_registration_allowed(_make_ctx(), scratch)
    assert isinstance(result, StepContinue)
```

### async Step —— 用 fake 取代 Query

```python
# tests/steps/test_fetch_plan_limits.py
from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.types import StepContinue
from schemas.user_register import RegisterCtx, UserRegisterRequest
from steps.user_register import make_fetch_plan_limits


async def fake_plan_query(
    session: AsyncSession,
    plan_id: str,
) -> dict[str, Any] | None:
    """符合 PlanQueryFn 的 Protocol，不需要繼承任何東西。"""
    return {"max_users": 10, "current_users": 5}


@pytest.mark.asyncio
async def test_fetch_plan_limits_returns_scratch() -> None:
    step = make_fetch_plan_limits(fake_plan_query)
    ctx = RegisterCtx(
        session=None,  # type: ignore[arg-type]
        input=UserRegisterRequest(email="a@b.com", name="A", plan_id="p1"),
    )
    result = await step(ctx, {})
    assert isinstance(result, StepContinue)
    assert result.scratch == {"plan_limits": {"max_users": 10, "current_users": 5}}
```

---

## Python 特有陷阱

### 🚨 `async with session.begin()` 內不能用 return

這是整份文件最危險的一點。SQLAlchemy 的 transaction context manager 只有在**以例外離開**時才 rollback；用 `return` 提前離開會被判定為「正常結束」而執行 **commit**。

```python
# ❌ BAD：業務拒絕卻 COMMIT 了先前的寫入，而且完全沒有錯誤訊息
async with session.begin():
    ...
    if result.status >= 400:
        return PersistenceResult(...)   # 這裡會 commit！

# ✅ GOOD：用例外離開，觸發 rollback，外層再攔截轉回正常回傳值
async with session.begin():
    ...
    if result.status >= 400:
        raise _ChainAbort(PersistenceResult(...))
```

這就是 `run_atomic_chain` 存在 `_ChainAbort` 的唯一理由。它是 `pipeline_chain.py` 的私有實作，永遠不會離開該檔案，對其他層完全透明。

### `types/` 目錄會遮蔽標準函式庫

TypeScript 版用 `types/` 放 domain 型別，Python 不要照抄 —— 專案根目錄的 `types` 套件會遮蔽 stdlib 的 `types` 模組。一律用 `schemas/`。

### 工廠函式產生的 Step 要有名字

Engine 用 `step.__name__` 產生 trace span。如果工廠內層函式叫 `step` 或用 `lambda`，所有 span 都會是同一個名字。內層函式一律取有意義的名字：

```python
def make_fetch_plan_limits(query_fn: PlanQueryFn) -> Step:
    async def fetch_plan_limits(ctx, scratch):   # ✅ 有意義的名字
        ...
    return fetch_plan_limits
```

### `expire_on_commit` 與 ORM 物件

SQLAlchemy 預設 `expire_on_commit=True`，commit 後 ORM 物件的屬性會失效，再次存取會觸發新的查詢（在 async 情境下可能直接拋錯）。

本架構規定 Query 回傳 `dict`、Persistence 回傳 `MutationResult`（也是純資料），ORM 物件不穿透層邊界 —— 這條規則在 Python 端剛好順便擋掉了這個坑。**不要為了方便而讓 Query 回傳 ORM model。**

### 沒有 `_tag` 欄位

TypeScript 版的三態回傳值都有 `_tag: "StepStop"` 這種欄位，那是為了彌補結構型別在執行期沒有型別資訊。Python 是名義型別，`isinstance(result, StepStop)` 就能完美 narrowing，mypy 與 pyright 都認得。**不要把 `_tag` 帶進 Python 實作。**

### 業務 422 與 FastAPI 驗證 422 撞號

FastAPI 預設用 **422** 回報 request 驗證失敗。本架構的範例把「已達方案人數上限」也設為 422，兩者在 client 端會無法區分。若這對前端造成困擾，可考慮業務層改用 409 或 400，或自訂 FastAPI 的 `RequestValidationError` handler 改用其他狀態碼 —— 這是專案層級的決定，動手前先確認。
