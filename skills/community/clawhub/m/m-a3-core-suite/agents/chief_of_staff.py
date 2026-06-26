"""
ChiefOfStaff — 幕僚长调度器
M-A3 Core Suite 核心组件

角色定位：任务入口 + 智能路由 + 结果整合

核心职责：
1. 接收自然语言任务
2. 识别任务类型和复杂度
3. 路由到最优执行 Agent
4. 整合结果返回用户
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime


class TaskComplexity(Enum):
    """任务复杂度等级"""
    TINY = "tiny"   # 单轮查询，无需 Agent
    SMALL = "small" # 单 Agent，5 分钟内完成
    MEDIUM = "medium" # 多 Agent，1 小时内完成
    LARGE = "large" # 全链路，跨 Agent 协作


class TaskType(Enum):
    """任务类型"""
    GEO = "GEO"
    SILICON = "SILICON"
    AMAZON = "AMAZON"
    CONTENT = "CONTENT"
    COLLAB = "COLLAB"
    DATA = "DATA"
    UNKNOWN = "UNKNOWN"


@dataclass
class Task:
    """任务数据模型"""
    task_id: str
    description: str
    task_type: TaskType = TaskType.UNKNOWN
    complexity: TaskComplexity = TaskComplexity.SMALL
    brand: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AgentInfo:
    """Agent 信息"""
    name: str
    role: str
    capabilities: List[str]
    keywords: List[str]  # 触发关键词
    complexity_range: tuple  # 能处理的复杂度范围
    category: str = ""  # 任务类型（与 TaskType 对应）


class ChiefOfStaff:
    """
    幕僚长调度器
    
    工作流程：
    1. receive() → 接收任务
    2. classify() → 识别类型和复杂度
    3. route() → 选择最优 Agent
    4. dispatch() → 分发任务
    5. integrate() → 整合结果
    """

    def __init__(self):
        self.agents = self._build_agent_registry()
        self.routing_keywords = self._build_routing_keywords()

    def _build_agent_registry(self) -> List[AgentInfo]:
        """构建 Agent 注册表"""
        return [
            AgentInfo(
                name="GEOStrategyAgent",
                role="GEO 运营策略",
                capabilities=["市场分析", "内容策略", "流量规划", "合规检查", "竞对分析"],
                keywords=["GEO", "AI可见性", "独立站", "外贸", "ChatGPT", "Claude",
                         "Perplexity", "SEO", "内容营销", "AI引用", "AI搜索"],
                complexity_range=(TaskComplexity.TINY, TaskComplexity.LARGE),
                category="GEO",
            ),
            AgentInfo(
                name="SiliconArmyAgent",
                role="产业互联网运营",
                capabilities=["采购分析", "生产调度", "销售决策", "财务建议",
                              "库存预警", "供应商管理", "合规审查"],
                keywords=["采购", "生产", "库存", "原材料", "供应商", "制造业",
                         "工厂", "硅基军团", "产业互联网", "工业"],
                complexity_range=(TaskComplexity.SMALL, TaskComplexity.LARGE),
                category="SILICON",
            ),
            AgentInfo(
                name="AmazonOpsAgent",
                role="跨境电商运营",
                capabilities=["选品分析", "Listing优化", "广告管理", "库存规划",
                              "定价策略", "差评处理", "跟卖检测", "VINE评价"],
                keywords=["亚马逊", "Amazon", "Listing", "ACOS", "FBA", "PPC",
                         "选品", "广告", "SP-API", "跨境电商", "跟卖"],
                complexity_range=(TaskComplexity.SMALL, TaskComplexity.LARGE),
                category="AMAZON",
            ),
            AgentInfo(
                name="ContentCreationAgent",
                role="内容创作",
                capabilities=["GEO内容", "营销文案", "技术文档", "多语言",
                              "小红书", "知乎", "LinkedIn", "Medium"],
                keywords=["内容", "文案", "文章", "写作", "创作", "SEO",
                         "小红书", "知乎", "多语言", "本地化"],
                complexity_range=(TaskComplexity.TINY, TaskComplexity.MEDIUM),
                category="CONTENT",
            ),
            AgentInfo(
                name="AgentWorldAgent",
                role="Agent World 社交",
                capabilities=["跨Agent协作", "Profile管理", "联盟互通",
                              "消息传递", "任务委派"],
                keywords=["协作", "社交", "联盟", "跨Agent", "Agent World",
                         "消息", "委派", "联合"],
                complexity_range=(TaskComplexity.SMALL, TaskComplexity.LARGE),
                category="COLLAB",
            ),
            AgentInfo(
                name="DataAnalysisAgent",
                role="数据分析",
                capabilities=["数据看板", "趋势分析", "异常检测", "报表生成"],
                keywords=["数据", "分析", "报表", "监控", "趋势", "异常", "看板"],
                complexity_range=(TaskComplexity.TINY, TaskComplexity.MEDIUM),
                category="DATA",
            ),
        ]

    def _build_routing_keywords(self) -> Dict[str, List[str]]:
        """构建关键词路由表"""
        return {
            "GEO": [
                "GEO", "AI可见性", "独立站", "外贸", "ChatGPT", "Claude",
                "Perplexity", "SEO", "内容营销", "AI引用", "AI搜索",
                "生成引擎", "Gemini", "Bing Copilot",
            ],
            "SILICON": [
                "采购", "生产", "库存", "原材料", "供应商", "制造业",
                "工厂", "硅基军团", "产业互联网", "工业", "排产",
            ],
            "AMAZON": [
                "亚马逊", "Amazon", "Listing", "ACOS", "FBA", "PPC",
                "选品", "广告", "SP-API", "跨境电商", "跟卖",
                "VINE", "差评", "BuyBox",
            ],
            "CONTENT": [
                "内容", "文案", "文章", "写作", "创作", "SEO",
                "小红书", "知乎", "多语言", "本地化",
            ],
            "COLLAB": [
                "协作", "社交", "联盟", "跨Agent", "Agent World",
                "消息", "委派", "联合",
            ],
            "DATA": [
                "数据", "分析", "报表", "监控", "趋势", "异常", "看板",
            ],
        }

    def receive(self, task_description: str, brand: Optional[str] = None, **context) -> Task:
        """接收并创建任务"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return Task(
            task_id=task_id,
            description=task_description,
            brand=brand,
            context=context,
        )

    def classify(self, task: Task) -> tuple[TaskType, TaskComplexity]:
        """识别任务类型和复杂度"""
        text = task.description.lower()

        # 关键词匹配 → 任务类型
        matched_types = []
        for task_type, keywords in self.routing_keywords.items():
            if any(kw.lower() in text for kw in keywords):
                matched_types.append(TaskType[task_type])

        task_type = matched_types[0] if matched_types else TaskType.UNKNOWN
        if len(matched_types) > 1:
            task_type = matched_types[0]  # 优先第一个匹配

        # 复杂度评估（关键词判断）
        complexity_indicators = {
            TaskComplexity.LARGE: ["分析", "计划", "策略", "全链路", "整套", "完整"],
            TaskComplexity.MEDIUM: ["优化", "方案", "报告", "监控"],
            TaskComplexity.SMALL: ["查询", "查一下", "告诉", "获取"],
        }

        detected_complexity = TaskComplexity.SMALL
        for level, indicators in complexity_indicators.items():
            if any(ind in task.description for ind in indicators):
                detected_complexity = level

        task.task_type = task_type
        task.complexity = detected_complexity

        return task_type, detected_complexity

    def route(self, task: Task) -> AgentInfo:
        """路由到最优 Agent"""
        task_type_value = task.task_type.value
        for agent in self.agents:
            if agent.category == task_type_value:
                return agent

        # 默认路由到 GEOStrategyAgent
        return self.agents[0]

    def execute(self, task_description: str, brand: Optional[str] = None, **context) -> Dict:
        """
        幕僚长执行主流程
        
        整合 receive → classify → route → dispatch
        """
        # 步骤 1：接收任务
        task = self.receive(task_description, brand, **context)

        # 步骤 2：分类识别
        task_type, complexity = self.classify(task)

        # 步骤 3：路由选择
        selected_agent = self.route(task)

        # 步骤 4：返回执行计划
        return {
            "task_id": task.task_id,
            "timestamp": task.created_at,
            "task_description": task.description,
            "brand": task.brand,
            "classification": {
                "type": task_type.value,
                "complexity": complexity.value,
            },
            "execution_plan": {
                "primary_agent": selected_agent.name,
                "primary_agent_role": selected_agent.role,
                "capabilities_used": selected_agent.capabilities,
            },
            "status": "ready_to_dispatch",
            "dispatch_instruction": self._generate_dispatch_instruction(selected_agent, task),
        }

    def _generate_dispatch_instruction(self, agent: AgentInfo, task: Task) -> str:
        """生成 Agent 执行指令"""
        return (
            f"调用 {agent.name}（{agent.role}）执行以下任务：\n"
            f"任务描述：{task.description}\n"
            f"涉及品牌：{task.brand or '未指定'}\n"
            f"上下文：{json.dumps(task.context, ensure_ascii=False)}\n"
            f"完成后整合结果并返回用户。"
        )


# ─────────────────────────────────────────────
# 单元测试
# ─────────────────────────────────────────────

if __name__ == "__main__":
    chief = ChiefOfStaff()

    # 测试用例
    test_cases = [
        ("帮我分析北美家具市场的GEO运营机会，我们是做家具出口的", "FurnitureBrand"),
        ("查询今天原材料行情，PVC价格上涨了", "PlasticFactory"),
        ("帮我优化这个亚马逊Listing：https://amazon.com/dp/B08XYZ", "AmazonStore"),
    ]

    print("=" * 60)
    print("ChiefOfStaff 路由测试")
    print("=" * 60)

    for desc, brand in test_cases:
        result = chief.execute(desc, brand)
        print(f"\n📋 任务：{desc[:30]}...")
        print(f"   品牌：{brand}")
        print(f"   类型：{result['classification']['type']} | 复杂度：{result['classification']['complexity']}")
        print(f"   Agent：{result['execution_plan']['primary_agent']}")
        print("-" * 40)
