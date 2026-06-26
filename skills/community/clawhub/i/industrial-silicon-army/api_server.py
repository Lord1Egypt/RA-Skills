#!/usr/bin/env python3
"""
产业互联网硅基军团 - API Server
FastAPI服务端，提供幕僚长任务调度与20个专业Agent的REST API接口
端口: 8080 | 文档: /docs
"""
import asyncio
import logging
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from industrial_agents import CHIEF, AGENTS, AGENT_REGISTRY, AGENT_CALL_LOG, TASK_ROUTING

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("silicon_army.api")

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="产业互联网硅基军团 API",
    description="幕僚长统一调度 + 20个制造业专业Agent，覆盖采购/生产/研发/销售/财务/合规全链路",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ───────────────────────────────────────────────────────────────────────
# CORS配置 - 仅允许特定来源，不允许credentialed请求以保护安全
ALLOWED_ORIGINS = [
    "https://cloudtrip.ai",
    "https://industrial-silicon-army.cloudtrip.ai",
    "http://localhost:3000",  # 本地开发
    "http://localhost:8080",  # 本地开发
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,  # 禁用credentialed请求以保护安全
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

# ── Pydantic Models ───────────────────────────────────────────────────────────
class ExecuteRequest(BaseModel):
    """执行任务请求"""
    task: str = Field(..., min_length=1, max_length=2000, description="自然语言任务描述")
    context: Optional[dict] = Field(default=None, description="额外上下文，透传给Agent")

    model_config = {"json_schema_extra": {
        "example": {
            "task": "本周原料库存不足，帮我分析一下行情并给出采购建议",
            "context": {"plant_id": "W01", "priority": "high"}
        }
    }}


class BatchItem(BaseModel):
    """批量任务中的单个任务"""
    task: str = Field(..., min_length=1, max_length=2000)
    context: Optional[dict] = None
    task_id: Optional[str] = Field(default=None, description="业务侧任务ID，用于关联结果")


class BatchRequest(BaseModel):
    """批量执行请求"""
    tasks: list[BatchItem] = Field(..., min_length=1, max_length=50)

    model_config = {"json_schema_extra": {
        "example": {
            "tasks": [
                {"task": "分析本月生产成本", "task_id": "cost-001"},
                {"task": "有客户投诉产品质量", "task_id": "cs-002"},
            ]
        }
    }}


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    agents_loaded: int
    routing_rules: int


class AgentInfo(BaseModel):
    id: str
    name: str
    emoji: str
    description: str
    capabilities: list[str]
    invoked_count: int = 0
    total_tokens: int = 0


class ExecuteResponse(BaseModel):
    chief: str
    input: str
    routed_agents: list[str]
    agent_count: int
    strategy: str
    results: dict
    total_tokens: int
    timestamp: str


class BatchResponse(BaseModel):
    total: int
    succeeded: int
    failed: int
    results: list[dict]


class StatsResponse(BaseModel):
    total_calls: int
    total_agents: int
    routing_rules: int
    top_agents: list[dict]
    recent_calls: list[dict]


# ── Helper ─────────────────────────────────────────────────────────────────────
def _safe_agent_info(agent_id: str) -> AgentInfo:
    reg = AGENT_REGISTRY.get(agent_id)
    agent = AGENTS.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    return AgentInfo(
        id=agent.agent_id,
        name=agent.name,
        emoji=agent.emoji,
        description=agent.description,
        capabilities=agent.capabilities,
        invoked_count=reg.get("invoked_count", 0) if reg else 0,
        total_tokens=reg.get("total_tokens", 0) if reg else 0,
    )


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/health", response_model=HealthResponse, tags=["系统"])
async def health_check():
    """服务健康检查"""
    logger.info("Health check called")
    return HealthResponse(
        status="ok",
        timestamp=datetime.now().isoformat(),
        agents_loaded=len(AGENTS),
        routing_rules=len(TASK_ROUTING),
    )


@app.post("/api/v1/execute", response_model=ExecuteResponse, tags=["核心接口"])
async def execute_task(payload: ExecuteRequest):
    """
    任务执行接口（幕僚长路由）

    幕僚长自动分析任务语义，将任务路由到最匹配的1-N个专业Agent并行执行。
    支持自然语言输入，自动调度全链路Agent协同作战。
    """
    # 注意：不记录任务内容，保护用户隐私
    logger.info("[execute] processing task...")
    try:
        result = await CHIEF.execute(payload.task, payload.context)
        return ExecuteResponse(**result)
    except Exception as exc:
        logger.exception(f"[execute] task failed: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/v1/agents", response_model=list[AgentInfo], tags=["核心接口"])
async def list_agents():
    """
    获取全部Agent列表

    返回20个专业Agent的元信息（不含实时调用统计）。
    实时统计请调用 GET /api/v1/stats。
    """
    logger.info("[agents] listing all agents")
    return [_safe_agent_info(aid) for aid in AGENTS]


@app.get("/api/v1/agents/{agent_id}", response_model=AgentInfo, tags=["核心接口"])
async def get_agent(agent_id: str):
    """
    获取单个Agent详情

    包含该Agent的调用统计（累计调用次数、累计Token消耗）。
    """
    logger.info(f"[agents] get agent_id={agent_id}")
    return _safe_agent_info(agent_id)


@app.get("/api/v1/stats", response_model=StatsResponse, tags=["监控"])
async def get_stats(limit: int = Query(default=20, ge=1, le=200, description="最近调用记录条数")):
    """
    获取系统调用统计

    - total_calls: 总调用次数
    - top_agents: 调用量排名前5的Agent
    - recent_calls: 仅返回调用元数据（不含任务内容），保护业务隐私
    """
    logger.info(f"[stats] limit={limit}")

    # Top agents
    sorted_agents = sorted(
        AGENT_REGISTRY.items(), key=lambda x: x[1].get("invoked_count", 0), reverse=True
    )
    top_agents = [
        {"agent_id": k, "name": v.get("name", k), "invoked_count": v.get("invoked_count", 0),
         "total_tokens": v.get("total_tokens", 0)}
        for k, v in sorted_agents[:5]
    ]

    # Recent calls - 仅返回元数据（不含任务内容），保护业务隐私
    recent = [
        {"agent": entry["agent"], "time": entry["time"]}
        for entry in AGENT_CALL_LOG[-limit:]
    ] if AGENT_CALL_LOG else []

    return StatsResponse(
        total_calls=len(AGENT_CALL_LOG),
        total_agents=len(AGENTS),
        routing_rules=len(TASK_ROUTING),
        top_agents=top_agents,
        recent_calls=recent,
    )


@app.post("/api/v1/batch", response_model=BatchResponse, tags=["核心接口"])
async def batch_execute(payload: BatchRequest):
    """
    批量执行任务

    并发执行多个任务，返回结果列表（顺序与请求顺序一致）。
    支持传入 task_id 关联业务侧ID。
    """
    logger.info(f"[batch] total={len(payload.tasks)}")

    async def run_task(item: BatchItem) -> dict:
        try:
            result = await CHIEF.execute(item.task, item.context)
            return {"task_id": item.task_id, "status": "success", "data": result}
        except Exception as exc:
            logger.warning(f"[batch] task_id={item.task_id} failed: {exc}")
            return {"task_id": item.task_id, "status": "failed", "error": str(exc)}

    results = await asyncio.gather(*[run_task(t) for t in payload.tasks])
    succeeded = sum(1 for r in results if r["status"] == "success")
    return BatchResponse(
        total=len(results),
        succeeded=succeeded,
        failed=len(results) - succeeded,
        results=list(results),
    )


# ── Global Exception Handler ──────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Internal server error: {str(exc)}"},
    )


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    logger.info("Starting 产业互联网硅基军团 API Server ...")
    logger.info(f"  → API Docs: http://localhost:8080/docs")
    logger.info(f"  → Agents loaded: {len(AGENTS)}")
    logger.info(f"  → Routing rules: {len(TASK_ROUTING)}")

    uvicorn.run(
        "api_server:app",
        host="127.0.0.1",  # 仅绑定本地接口，保护安全
        port=8080,
        reload=False,
        log_level="info",
        access_log=True,
    )
