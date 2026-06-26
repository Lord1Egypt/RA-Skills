"""
M-A3 Core Suite — API Server
幕僚长调度 Multi-Agent 运营系统 REST API

Usage:
    pip install -r requirements.txt
    python api_server.py
    # → http://localhost:8080
    # → API Docs: http://localhost:8080/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
import uvicorn
import yaml
import json

app = FastAPI(
    title="M-A3 Core Suite API",
    description="幕僚长驱动的 Multi-Agent 智能运营系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 全开放（生产环境建议限制）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# 数据模型
# ─────────────────────────────────────────────

class GEOTask(BaseModel):
    """GEO 运营任务"""
    brand: str = Field(..., description="品牌名称")
    product: str = Field(..., description="产品/服务")
    target_market: Literal["北美", "欧盟", "东南亚", "拉美", "中东"] = Field(
        ..., description="目标市场"
    )
    competitors: Optional[List[str]] = Field(default=[], description="竞品列表")
    goal: Optional[str] = Field(default="提升AI可见性", description="运营目标")


class SiliconArmyTask(BaseModel):
    """产业互联网硅基军团任务"""
    industry: str = Field(..., description="行业类型")
    scenario: Literal["采购", "生产", "销售", "财务", "合规", "运营"] = Field(
        ..., description="业务场景"
    )
    description: str = Field(..., description="任务描述")
    context: Optional[dict] = Field(default={}, description="额外上下文")


class AmazonOpsTask(BaseModel):
    """亚马逊运营任务"""
    action: Literal["选品", "Listing优化", "广告投放", "库存管理", "定价策略", "差评处理"] = Field(
        ..., description="运营动作"
    )
    marketplace: Literal["US", "EU", "JP"] = Field(default="US", description="目标站点")
    asin: Optional[str] = Field(default=None, description="ASIN（可选）")
    keywords: Optional[List[str]] = Field(default=[], description="关键词列表")
    description: str = Field(..., description="任务描述")


class CollaborationTask(BaseModel):
    """Agent World 协作任务"""
    target_agent: str = Field(..., description="目标 Agent ID 或用户名")
    action: Literal["query", "delegate", "share"] = Field(..., description="协作动作")
    message: str = Field(..., description="协作消息内容")
    context: Optional[dict] = Field(default={}, description="额外上下文")


class TaskResponse(BaseModel):
    """统一响应格式"""
    success: bool
    task_id: str
    timestamp: str
    agent: str
    result: dict
    next_steps: Optional[List[str]] = None


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def generate_task_id() -> str:
    """生成任务 ID"""
    return f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def load_agent_registry() -> dict:
    """加载 Agent 注册表"""
    try:
        with open("config/agent_registry.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {"agents": []}


def route_to_agent(task_type: str) -> str:
    """任务路由：根据任务类型选择最优 Agent"""
    routing_map = {
        "GEO": "GEOStrategyAgent",
        "SILICON": "SiliconArmyAgent",
        "AMAZON": "AmazonOpsAgent",
        "CONTENT": "ContentCreationAgent",
        "COLLAB": "AgentWorldAgent",
        "DATA": "DataAnalysisAgent",
    }
    return routing_map.get(task_type, "GEOStrategyAgent")


# ─────────────────────────────────────────────
# 健康检查
# ─────────────────────────────────────────────

@app.get("/health")
def health():
    """健康检查"""
    return {
        "status": "ok",
        "service": "m-a3-core-suite",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/")
def root():
    """根路径"""
    return {
        "service": "M-A3 Core Suite API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "agents": "/api/v1/agents",
    }


# ─────────────────────────────────────────────
# Agent 注册表
# ─────────────────────────────────────────────

@app.get("/api/v1/agents")
def list_agents():
    """列出所有可用 Agent"""
    registry = load_agent_registry()
    return {
        "total": len(registry.get("agents", [])),
        "agents": registry.get("agents", [
            {
                "name": "ChiefOfStaff",
                "role": "幕僚长（任务调度）",
                "capabilities": ["任务路由", "结果整合", "主动预警"],
            },
            {
                "name": "GEOStrategyAgent",
                "role": "GEO 运营策略",
                "capabilities": ["市场分析", "内容策略", "流量规划", "合规检查"],
            },
            {
                "name": "SiliconArmyAgent",
                "role": "产业互联网运营",
                "capabilities": ["采购分析", "生产调度", "销售决策", "财务建议"],
            },
            {
                "name": "AmazonOpsAgent",
                "role": "跨境电商运营",
                "capabilities": ["选品分析", "Listing优化", "广告管理", "库存规划"],
            },
            {
                "name": "ContentCreationAgent",
                "role": "内容创作",
                "capabilities": ["GEO内容", "营销文案", "技术文档", "多语言"],
            },
            {
                "name": "AgentWorldAgent",
                "role": "Agent World 社交",
                "capabilities": ["跨Agent协作", "Profile管理", "联盟互通"],
            },
        ]),
    }


# ─────────────────────────────────────────────
# GEO 运营 API
# ─────────────────────────────────────────────

@app.post("/api/v1/geo/strategy", response_model=TaskResponse)
def generate_geo_strategy(task: GEOTask):
    """
    生成 GEO 运营策略
    
    基于目标市场特点，分析品牌 AI 可见性，
    生成内容策略、流量方案和合规建议。
    """
    task_id = generate_task_id()
    agent = "GEOStrategyAgent"

    # TODO: 调用 geo-ops-agents 核心逻辑
    # result = geo_agent.execute(task)

    result = {
        "brand": task.brand,
        "product": task.product,
        "target_market": task.target_market,
        "goal": task.goal,
        "competitors": task.competitors,
        "strategy": {
            "market_analysis": {
                "market_size": "$120B（北美家具市场）",
                "growth_rate": "6.2%/年",
                "top_channels": ["官网", "亚马逊", "Wayfair", "Etsy"],
                "ai_platforms": ["ChatGPT", "Claude", "Perplexity", "Gemini"],
            },
            "content_strategy": {
                "priority_formats": ["FAQ", "对比评测", "选购指南", "定义"],
                "recommended_topics": [
                    "实木家具 vs 板材家具完整对比",
                    "2026年最流行的5种家具风格",
                    "如何鉴别优质家具（选购指南）",
                ],
                "target_keywords": [
                    "best furniture brands",
                    "solid wood vs engineered wood",
                    "furniture buying guide 2026",
                ],
            },
            "traffic_strategy": {
                "channels": ["官网", "LinkedIn", "Medium", "Pinterest"],
                "budget_allocation": {"官网": "50%", "社媒": "30%", "付费": "20%"},
            },
            "compliance_check": {
                "data_protection": ["CCPA合规", "消费者隐私保护"],
                "advertising": ["FTC代言披露", "广告标签规范"],
                "product_safety": ["CPSC合规", "材料认证"],
            },
        },
        "geo_score": 72,
        "priority_score": "HIGH",
    }

    return TaskResponse(
        success=True,
        task_id=task_id,
        timestamp=datetime.now().isoformat(),
        agent=agent,
        result=result,
        next_steps=[
            "1. 优先创建 FAQ 页面内容（高优先级）",
            "2. 同步更新官网 Schema.org 结构化数据",
            "3. 在 LinkedIn 发布行业深度文章",
            "4. 监控 30 天后的 AI 引用率变化",
        ],
    )


# ─────────────────────────────────────────────
# 硅基军团 API
# ─────────────────────────────────────────────

@app.post("/api/v1/silicon/task", response_model=TaskResponse)
def dispatch_silicon_task(task: SiliconArmyTask):
    """产业互联网硅基军团任务分发"""
    task_id = generate_task_id()
    agent = route_to_agent("SILICON")

    result = {
        "industry": task.industry,
        "scenario": task.scenario,
        "task_description": task.description,
        "recommendations": [
            {
                "agent": "原料采购Agent",
                "action": "分析原材料涨价对毛利率的影响",
                "priority": "HIGH",
                "expected_impact": "成本降低 5-8%",
            },
            {
                "agent": "配方研发Agent",
                "action": "寻找性价比更高的替代材料",
                "priority": "HIGH",
                "expected_impact": "材料成本降低 10-15%",
            },
            {
                "agent": "供应商管理Agent",
                "action": "重新评估供应商议价空间",
                "priority": "MEDIUM",
                "expected_impact": "采购成本降低 3-5%",
            },
        ],
        "risk_alerts": [
            "⚠️ 原材料涨价可能持续 2-3 个月，建议锁量 30 天",
            "⚠️ 关注汇率波动对进口原材料成本的影响",
        ],
    }

    return TaskResponse(
        success=True,
        task_id=task_id,
        timestamp=datetime.now().isoformat(),
        agent=agent,
        result=result,
        next_steps=[
            "1. 联系备选供应商获取最新报价",
            "2. 启动配方研发替代料评估",
            "3. 调整 30 天采购计划",
            "4. 通知销售团队调整报价策略",
        ],
    )


# ─────────────────────────────────────────────
# 亚马逊运营 API
# ─────────────────────────────────────────────

@app.post("/api/v1/amazon/ops", response_model=TaskResponse)
def dispatch_amazon_ops(task: AmazonOpsTask):
    """亚马逊运营任务分发"""
    task_id = generate_task_id()
    agent = "AmazonOpsAgent"

    result = {
        "action": task.action,
        "marketplace": task.marketplace,
        "asin": task.asin,
        "keywords": task.keywords,
        "description": task.description,
        "recommendations": _generate_amazon_recommendations(task),
    }

    return TaskResponse(
        success=True,
        task_id=task_id,
        timestamp=datetime.now().isoformat(),
        agent=agent,
        result=result,
        next_steps=["参考 recommendations 字段执行具体操作"],
    )


def _generate_amazon_recommendations(task: AmazonOpsTask) -> dict:
    """生成亚马逊运营建议"""
    action_map = {
        "选品": {
            "analysis_type": "选品可行性评估",
            "key_factors": ["市场竞争度", "利润空间", "差异化机会", "FBA成本"],
            "recommended_tools": ["Helium 10", "Jungle Scout", "Keepa"],
        },
        "Listing优化": {
            "focus": "A9算法优化",
            "title_checklist": ["核心关键词前置", "品牌名", "产品特点", "数量"],
            "bullet_points": ["每点1行", "含数据支撑", "含使用场景"],
            "description": "含品牌故事 + 差异化卖点",
        },
        "广告投放": {
            "campaign_types": ["SP自动", "SP手动", "SB", "SD"],
            "acos_target": "15-25%",
            "bidding_strategy": "动态竞价（仅降低）",
        },
        "库存管理": {
            "safety_stock_days": 30,
            "restock_alert": "剩余30天库存",
            "IPI_target": 700,
        },
        "定价策略": {
            "strategy": "竞品锚定 + 动态调价",
            "margin_target": "25%+",
        },
        "差评处理": {
            "response_time": "<24小时",
            "steps": ["分析差评原因", "联系买家", "申请移除"],
        },
    }
    return action_map.get(task.action, {})


# ─────────────────────────────────────────────
# Agent World 协作 API
# ─────────────────────────────────────────────

@app.post("/api/v1/agent-world/collab", response_model=TaskResponse)
def agent_world_collaboration(task: CollaborationTask):
    """Agent World 跨 Agent 协作"""
    task_id = generate_task_id()
    agent = "AgentWorldAgent"

    result = {
        "target_agent": task.target_agent,
        "action": task.action,
        "message": task.message,
        "context": task.context,
        "collaboration_status": "pending",
        "world_api_endpoint": "https://world.coze.site/api/v1",
    }

    return TaskResponse(
        success=True,
        task_id=task_id,
        timestamp=datetime.now().isoformat(),
        agent=agent,
        result=result,
        next_steps=[
            "1. 通过 Agent World API 发起协作请求",
            "2. 等待目标 Agent 响应",
            "3. 整合协作结果返回用户",
        ],
    )


# ─────────────────────────────────────────────
# 幕僚长任务分发（统一入口）
# ─────────────────────────────────────────────

@app.post("/api/v1/chief-of-staff/dispatch")
def chief_of_staff_dispatch(raw_task: dict):
    """
    幕僚长统一任务分发接口
    
    支持自然语言任务描述，由幕僚长自动路由到最合适的 Agent。
    
    请求示例：
    {
        "task": "帮我分析北美家具市场的GEO运营机会",
        "brand": "MyBrand",
        "context": {}
    }
    """
    task_id = generate_task_id()

    task_text = raw_task.get("task", "")
    brand = raw_task.get("brand", "Unknown")

    # 简单关键词路由（实际场景可接入 NLP 模型）
    if any(kw in task_text for kw in ["GEO", "AI可见性", "独立站", "外贸", "ChatGPT", "Claude"]):
        selected_agent = "GEOStrategyAgent"
        endpoint = "/api/v1/geo/strategy"
    elif any(kw in task_text for kw in ["亚马逊", "Amazon", "Listing", "ACOS", "FBA"]):
        selected_agent = "AmazonOpsAgent"
        endpoint = "/api/v1/amazon/ops"
    elif any(kw in task_text for kw in ["采购", "生产", "库存", "原材料", "供应商"]):
        selected_agent = "SiliconArmyAgent"
        endpoint = "/api/v1/silicon/task"
    else:
        selected_agent = "GEOStrategyAgent"
        endpoint = "/api/v1/geo/strategy"

    return {
        "success": True,
        "task_id": task_id,
        "timestamp": datetime.now().isoformat(),
        "chief_of_staff": {
            "task_understood": task_text,
            "brand": brand,
            "routed_to": selected_agent,
            "endpoint": endpoint,
            "routing_reason": f"关键词匹配 → {selected_agent}",
        },
        "next_action": f"POST {endpoint} with task details",
    }


# ─────────────────────────────────────────────
# 启动服务
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("M-A3 Core Suite API Server")
    print("=" * 50)
    print("Local:  http://localhost:8080")
    print("Docs:   http://localhost:8080/docs")
    print("Health: http://localhost:8080/health")
    print("=" * 50)
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
        log_level="info",
    )
