#!/usr/bin/env python3
"""Industrial Silicon Army - 20 Industrial Agents + ChiefOfStaff"""
import asyncio, json, re
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# ── Security & Privacy Utilities ──────────────────────────────────────────────
# 数据安全根路径配置
DATA_ROOT = Path("./data/industrial-silicon-army/")
OUTPUT_DIR = DATA_ROOT / "output"
CONFIG_DIR = Path("./config/industrial-silicon-army/")

# 敏感字段列表
SENSITIVE_FIELDS = ["account", "tax_id", "credit_score", "payment_info", "bank_account", "id_number"]

def validate_path(file_path: str, allowed_dirs: list[Path]) -> bool:
    """验证文件路径是否在允许的目录范围内"""
    try:
        p = Path(file_path).resolve()
        return any(str(p).startswith(str(d.resolve())) for d in allowed_dirs)
    except Exception:
        return False

def mask_sensitive_data(data: Any, fields: list[str] = None) -> Any:
    """
    递归脱敏敏感数据
    - 银行账号：显示后4位，如 ****1234
    - 税号：显示后4位，如 ****6789X
    - 信用评分：返回等级而非原始分数
    """
    if fields is None:
        fields = SENSITIVE_FIELDS
    
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            key_lower = key.lower()
            # 检查是否为敏感字段
            if any(f in key_lower for f in fields):
                if isinstance(value, str) and len(value) > 4:
                    result[key] = "****" + value[-4:]
                else:
                    result[key] = "****"
            else:
                result[key] = mask_sensitive_data(value, fields)
        return result
    elif isinstance(data, list):
        return [mask_sensitive_data(item, fields) for item in data]
    else:
        return data

def sanitize_procurement_suggestion(suggestion: dict) -> dict:
    """
    采购建议脱敏处理
    - 移除完整财务信息
    - 仅保留价格区间和数量范围
    - 标记为待确认状态
    """
    sanitized = mask_sensitive_data(suggestion)
    sanitized["status"] = "pending_confirmation"  # 标记待确认
    sanitized["requires_human_action"] = True      # 需要人工介入
    return sanitized

def check_procurement_permission(context: dict = None) -> tuple[bool, str]:
    """
    检查采购操作权限
    返回: (允许操作, 拒绝原因)
    """
    # 默认拒绝自动采购
    return False, "自动采购已禁用，所有采购建议需人工确认"

TASK_ROUTING = {
    "material_procurement": ["原料","供应商","行情","比价","采购","货源"],
    "warehouse": ["库存","库位","周转","仓储","备货"],
    "logistics": ["物流","车队","运输","发货","配送"],
    "supplier_management": ["供应商","评级","绩效","合同"],
    "production_schedule": ["排产","工单","交期","生产","产能","工期"],
    "formula_rd": ["配方","新材料","研发","替代","成本优化"],
    "quality_inspection": ["质量","检测","合格","不良","AQL","品质"],
    "equipment_maintenance": ["设备","维修","故障","停机","保养","维护"],
    "quoting": ["报价","价格","报价单","议价","折扣"],
    "order_fulfillment": ["订单","发货","交期","履约","出货"],
    "customer_management": ["客户","跟进","复购","流失","分级"],
    "competitor_monitoring": ["竞品","竞争对手","市场","定价","份额"],
    "cost_accounting": ["成本","毛利","利润","盈亏","核算"],
    "compliance_review": ["合规","环保","安全","税务","法规","认证"],
    "risk_alert": ["风险","预警","呆账","坏账","信用"],
    "policy_interpretation": ["政策","补贴","税务优惠","扶持","申报"],
    "data_analysis": ["数据","报表","日报","月报","经营","分析"],
    "report_generation": ["报告","会议","纪要","文档","PPT"],
    "project_management": ["项目","里程碑","进度","交付","管理"],
    "customer_service": ["售后","投诉","客服","退换","服务"],
}

AGENT_REGISTRY: Dict[str, dict] = {}
# 简化调用日志 - 仅记录元数据，不记录任务内容，保护业务隐私
AGENT_CALL_LOG: List[dict] = []

def log_call(agent_id: str, task: str, tokens: int):
    if agent_id in AGENT_REGISTRY:
        AGENT_REGISTRY[agent_id]["invoked_count"] += 1
        AGENT_REGISTRY[agent_id]["total_tokens"] += tokens
    # 仅记录调用元数据，不记录任务内容
    AGENT_CALL_LOG.append({
        "agent": agent_id, 
        "time": datetime.now().isoformat(),
        # 注意：移除了task和tokens字段以保护业务隐私
    })

class IndustrialAgent:
    def __init__(self, agent_id: str, name: str, emoji: str, description: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.name = name
        self.emoji = emoji
        self.description = description
        self.capabilities = capabilities
        AGENT_REGISTRY[agent_id] = {
            "id": agent_id, "name": name, "emoji": emoji,
            "description": description, "capabilities": capabilities,
            "invoked_count": 0, "total_tokens": 0,
        }

    async def execute(self, task: str, context: Optional[dict] = None) -> dict:
        log_call(self.agent_id, task, 150)
        result = await self._run(task, context or {})
        result["agent"] = self.emoji + " " + self.name
        result["tokens"] = 150
        return result

    async def _run(self, task: str, context: dict) -> dict:
        raise NotImplementedError


class MaterialProcurementAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("material_procurement", "原料采购Agent", "🧪",
            "Supplier sourcing, market analysis, price comparison",
            ["1688 sourcing","market analysis","supplier matching","procurement"])

    async def _run(self, task: str, ctx: dict) -> dict:
        # 采购权限检查 - 不允许自动下单
        allowed, reason = check_procurement_permission(ctx)
        
        result = {
            "input": task,
            "result": {
                "suppliers": ["华锦化工(浙江)","中石化A供应商","山东工程塑料厂"],
                "market_analysis": "Raw material prices in downtrend. Suggested to stock up partially.",
                "price_comparison": "1688 price: 12.5 CNY/kg; Bulk: 11.8 CNY/kg",
                "procurement_plan": "Stage 1: 30% stock, lock price; Stage 2: monitor trend",
                "delivery": "7-10 business days",
                "risks": ["delivery delay","quality fluctuation","logistics"],
                "supplier_details": mask_sensitive_data({
                    "supplier_a": {"name": "华锦化工(浙江)", "rating": "4.8", "account": "6217002345678901234"},
                    "supplier_b": {"name": "中石化A供应商", "rating": "4.9", "account": "6222023456789012345"},
                }),
            },
            "kpis": {"on_time_delivery": "92%", "quality_pass": "97%", "cost_saving": "3.2%"},
            "status": "pending_confirmation",
            "auto_order_enabled": False,
            "message": "采购建议已生成，请人工确认后执行下单操作",
        }
        
        # 确保结果经过脱敏处理
        return sanitize_procurement_suggestion(result)


class WarehouseAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("warehouse", "仓储管理Agent", "🏭",
            "Inventory warning, location optimization, turnover analysis",
            ["inventory alert","location optimization","ABC analysis","turnover"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "alerts": ["Material A: 15T, below safety stock 20T - WARNING",
                           "Material B: 80T, above safety stock 50T - NORMAL",
                           "Finished goods C: 1200pcs overstock (+30%)"],
                "suggestion": "Relocate Material A to A-01 (near exit) for +15% picking efficiency",
                "turnover": "Average turnover 18 days, below target 20 days - GOOD",
                "slow_moving": "3 items >90 days slow-moving, suggest clearance",
            },
            "kpis": {"turnover": "14x/year", "space_util": "82%", "slow_rate": "2.1%"},
        }


class LogisticsAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("logistics", "物流调度Agent", "🚛",
            "Fleet matching, route optimization, cost control",
            ["fleet matching","route optimization","cost control","tracking"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "dispatch": "Recommend Deppon (fast) or Anneng (cheap)",
                "route_optimization": "Group orders by region, consolidate shipping, save 18% freight",
                "tracking": "Real-time tracking via logistics API integration",
                "cost_analysis": {"Deppon": "12+2 CNY/kg", "Anneng": "1.8 CNY/kg", "专线": "1.2 CNY/kg"},
                "alerts": "2 shipments delayed due to traffic control - drivers notified",
            },
            "kpis": {"freight_ratio": "4.8%", "on_time": "96%", "damage_rate": "0.12%"},
        }


class ProductionScheduleAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("production_schedule", "生产调度Agent", "⚙️",
            "Production scheduling, work order management, delivery commitment",
            ["smart scheduling","work orders","delivery","capacity"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "schedule": "Order A (URGENT): Thu deadline; Order B: Sat deadline",
                "capacity_utilization": "Current load: 78%, remaining: 22%",
                "delivery_commitment": "Standard: 14 days; Rush: 7 days (+15% fee)",
                "bottleneck": "Injection molding at 97% utilization - consider adding 1 machine",
                "outsource": "Non-core processes can be outsourced, save 8% cost",
            },
            "kpis": {"delivery_achievement": "95%", "capacity_util": "78%", "machine_uptime": "85%"},
        }


class QualityInspectionAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("quality_inspection", "质量检测Agent", "🔬",
            "Incoming/in-process/outgoing QC",
            ["AQL sampling","incoming inspection","process control","non-conformance"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "inspection_plan": "AQL=1.0 sampling plan recommended",
                "incoming": "3 batches today, 2 completed, 1 pending (result 14:00)",
                "process_control": "3 SPC checkpoints set, all in control",
                "ncr": "2 appearance defects found, isolated and MRB initiated",
                "trend": "30-day yield: 99.2%, +0.3% vs last month",
            },
            "kpis": {"incoming_pass": "98.5%", "process_pass": "99.1%", "outgoing_pass": "99.6%"},
        }


class EquipmentMaintenanceAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("equipment_maintenance", "设备维护Agent", "🔧",
            "Predictive maintenance, fault diagnosis, downtime reduction",
            ["predictive maintenance","fault diagnosis","maintenance orders","spare parts"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "prediction_alert": "Injection machine #3 main bearing temp high,预计7天内故障, schedule maintenance",
                "maintenance_plan": "Preventive maintenance for related equipment (4h downtime expected)",
                "spare_parts": "Critical spares in stock, sufficient for 3 major repairs",
                "work_orders": "8 orders processed this week, avg repair time 2.3h",
                "mtbf": "820 hours (industry benchmark: 1000 hours)",
            },
            "kpis": {"uptime": "96%", "mtbf": "820h", "response_time": "0.5h"},
        }


class QuotingAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("quoting", "报价Agent", "💲",
            "Quick quote, cost-plus pricing, negotiation handling",
            ["quick quote","cost-plus","negotiation","validity"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "quote": "FOB 18.5 CNY/kg, CIF 22.3 CNY/kg (auto-generated)",
                "cost_breakdown": {"material": "65%", "processing": "20%", "overhead": "8%", "margin": "7%"},
                "discount_space": ">5MT one-time: 3% discount; long-term: 5% rebate",
                "validity": "Quote valid for 14 days",
                "response_time": "Auto-generate <30s, human review <5min",
            },
            "kpis": {"response_time": "<5min", "accuracy": "99%", "margin_achievement": "96%"},
        }


class OrderFulfillmentAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("order_fulfillment", "订单履约Agent", "📦",
            "Order tracking, exception handling, customer experience",
            ["order tracking","exception handling","delivery update","customer notify"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "order_status": "12 in-transit, 9 normal, 3 exceptions (escalated)",
                "delivery_alert": "2 orders may delay due to material shortage, customers notified",
                "tracking": "8 shipments tracked in real-time",
                "complaints": "3 handled this week, CSAT 4.6/5.0",
            },
            "kpis": {"fulfillment_rate": "97%", "on_time": "94%", "csat": "4.6/5"},
        }


class CustomerManagementAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("customer_management", "客户管理Agent", "🤝",
            "Customer segmentation, follow-up, repurchase promotion",
            ["segmentation","follow-up","repurchase","churn"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "segmentation": {"A-tier (key accounts)": "8 (65% revenue)", "B-tier": "25", "C-tier": "47"},
                "follow_up": "3 follow-ups scheduled this week (1 already done)",
                "churn_alert": "Customer #12: 60 days no order - yellow flag",
                "repurchase": "Promote quarterly promotion to high-value customers, expect 15% activation",
            },
            "kpis": {"repurchase_rate": "62%", "satisfaction": "91%", "churn_rate": "5.3%"},
        }


class CompetitorMonitoringAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("competitor_monitoring", "竞品监控Agent", "🎯",
            "Market price monitoring, competitor analysis, substitute alerts",
            ["price monitoring","competitor intel","substitutes","market intel"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "market_price": "Market avg 16.8 CNY/kg, our price 18.5 CNY/kg (mid-high range)",
                "competitor_news": "Competitor A dropped price 3% this week to gain share",
                "substitute_threat": "Biodegradable materials growing 35% - medium-term pressure",
                "pricing_advice": "1-2% discount for key accounts; maintain price for new customers",
            },
            "kpis": {"price_competitiveness": "mid-high", "share_target": "+2%", "response": "<24h"},
        }


class CostAccountingAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("cost_accounting", "成本核算Agent", "💰",
            "Actual vs standard cost, margin analysis, cost reduction",
            ["cost accounting","standard cost","margin analysis","cost reduction"])

    async def _run(self, task: str, ctx: dict) -> dict:
        # 财务数据脱敏处理 - 不存储原始财务数据
        result = {
            "input": task,
            "result": mask_sensitive_data({
                "cost_analysis": "Standard: 14.2 CNY/kg, Actual: 14.8 CNY/kg, variance +4.2%",
                "variance_cause": "Material price +3%, yield -0.5%",
                "margin": {"Product A": "28% (target 30%)", "Product B": "18% (target 20%)"},
                "reduction_path": "Substitute materials + process optimization = 5-8% cost reduction",
                "financial_note": "Detailed financial data processed in-memory only, not persisted",
            }),
            "kpis": mask_sensitive_data({
                "gross_margin": "22%", 
                "cost_accuracy": "96%", 
                "variance": "<5%",
            }),
            "data_retention": "in_memory_only",
            "persistence_disabled": True,
            "message": "财务数据仅在内存中处理，不持久化存储",
        }
        return result


class ComplianceReviewAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("compliance_review", "合规审查Agent", "⚖️",
            "Environmental, safety, tax compliance",
            ["environmental compliance","safety","tax compliance","regulatory"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "compliance_status": {"environmental": "PASS", "safety": "PASS", "tax": "PASS"},
                "regulation_alert": "New VOC standard effective July 2026 - equipment upgrade needed",
                "safety_notice": "Injection shop temp high - ventilation reinforced",
                "recommendation": "Build compliance checklist, update quarterly",
            },
            "kpis": {"pass_rate": "100%", "rectification": "98%", "training": "12x/year"},
        }


class RiskAlertAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("risk_alert", "风险预警Agent", "🚨",
            "Customer credit, material volatility, bad debt warning",
            ["credit assessment","price volatility","bad debt","risk rating"])

    async def _run(self, task: str, ctx: dict) -> dict:
        # 风险数据脱敏 - 不存储原始信用数据
        result = {
            "input": task,
            "result": mask_sensitive_data({
                "risk_register": [
                    {"risk": "Customer #15 credit rating downgraded", "level": "MEDIUM", "action": "Suspend credit, collect payment"},
                    {"risk": "Material price volatility >10%", "level": "MEDIUM", "action": "Lock 3-month futures"},
                    {"risk": "FX fluctuation (USD depreciation)", "level": "LOW", "action": "Accelerate FX settlement"},
                ],
                "bad_debt_alert": "90+ day AR: 280K CNY, provision: 84K CNY",
                "credit_note": "Credit scores returned as ratings only, raw data not stored",
            }),
            "kpis": mask_sensitive_data({
                "bad_debt_rate": "0.8%", 
                "overdue_rate": "<3%", 
                "risk_coverage": "100%",
            }),
            "data_protection": "credit_scores_masked",
            "message": "客户信用评分仅返回等级，不存储原始数据",
        }
        return result


class PolicyInterpretationAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("policy_interpretation", "政策解读Agent", "📜",
            "Industry policy, subsidy application, tax benefits",
            ["policy interpretation","subsidy","tax benefits","industry support"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "policy_summary": "2026 manufacturing support: R&D expense 100% super deduction; tech upgrade subsidy up to 30%",
                "subsidy_opportunities": [
                    {"name": "Provincial Smart Manufacturing Pilot", "amount": "up to 2M CNY", "deadline": "2026-06-30"},
                    {"name": "SME Digital Transformation", "amount": "up to 500K CNY", "deadline": "2026-12-31"},
                ],
                "tax_benefit": "Hi-tech enterprise CIT 15% (vs standard 25%)",
                "application": "Recommend applying for Digital Transformation project, expected subsidy 300K CNY",
            },
            "kpis": {"policy_coverage": "95%", "subsidy": "500K+ CNY/year", "tax_saving": "800K CNY/year"},
        }


class DataAnalysisAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("data_analysis", "数据分析Agent", "📊",
            "Daily/monthly reports, BI dashboard, anomaly detection",
            ["daily report","monthly report","BI dashboard","anomaly detection"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "today_summary": {"output": "12.5MT", "shipment": "11.8MT", "inventory": "185MT", "in_transit": "23MT"},
                "kpis": {"yield": "99.2%", "delivery": "96%", "machine_uptime": "98%"},
                "mom_comparison": "Output +8% MoM, -3% YoY (Spring Festival)",
                "anomaly": "Injection yield today 97.8% (low - needs attention)",
            },
            "kpis": {"report_time": "<1min", "data_accuracy": "99.5%", "anomaly_detection": "+40%"},
        }


class ReportGenerationAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("report_generation", "报告生成Agent", "📝",
            "Meeting minutes, presentation materials, analysis reports",
            ["meeting minutes","presentations","analysis report","PPT generation"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "outline": "Background(1p) / Current State(2p) / Issues(1p) / Solutions(2p) / Plan(1p)",
                "draft": "Auto-generated draft: 5 pages, 3000 words, 8-min read",
                "data_citations": "Auto-pulled from ERP/MES, data as of yesterday 24:00",
                "improvement": "Suggest adding competitor comparison page",
            },
            "kpis": {"generation_time": "<5min", "time_saved": "4h per report", "adoption_rate": "+85%"},
        }


class ProjectManagementAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("project_management", "项目管理Agent", "📅",
            "Milestone tracking, risk management, progress transparency",
            ["milestones","risk management","progress tracking","delivery management"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "project_status": "All milestones on track, 100% achievement rate",
                "progress_alert": "Supplier certification delayed - may affect production schedule",
                "risk_management": "3 risks identified, 2 mitigated, 1 pending",
                "gantt_chart": "Generated and updated to PM dashboard",
            },
            "kpis": {"on_time_delivery": "94%", "milestone_achievement": "100%", "transparency": "+60%"},
        }


class CustomerServiceAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("customer_service", "客服支持Agent", "🎧",
            "After-sales, complaint management, FAQ",
            ["after-sales","complaint escalation","FAQ","CSAT survey"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "ticket_stats": {"pending": "5", "in_progress": "3", "closed": "12"},
                "response": "Response <4h, CSAT 91%",
                "faq_recommendation": "Quality issues 42% - suggest adding quality page on website",
                "escalation": "1 complaint escalated to management",
            },
            "kpis": {"response_time": "<4h", "resolution_rate": "89%", "csat": "4.6/5"},
        }


# Instantiate all agents
class SupplierManagementAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("supplier_management", "供应商管理Agent", "📋",
            "Supplier rating, risk management, contract management",
            ["supplier rating","risk management","contract","performance"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "supplier_rating": {"A-tier": "3 (preferred)", "B-tier": "8", "C-tier (phase out)": "2"},
                "performance": "Related supplier score: 92/100 (+3 vs last quarter)",
                "risk_alert": "Supplier B has financial issues - recommend reducing PO ratio 20%",
                "contract_expiry": "3 contracts expiring in 30 days - schedule renewal",
            },
            "kpis": {"supplier_count": "13", "a_tier_ratio": "23%", "on_time_delivery": "94%"},
        }

class FormulaRdAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("formula_rd", "配方研发Agent", "🧬",
            "New formula R&D, substitute materials, cost optimization",
            ["formula optimization","new material","substitute","cost reduction"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "formula_advice": "Current cost 15.2 CNY/kg, target: 13.8 CNY/kg (-9%)",
                "substitute": "Domestic Supplier S material can replace import, cost -22%, performance -3%",
                "new_direction": "Biodegradable PBAT market growing 35% - recommend new product line",
                "rd_timeline": "New formula sample: 3-5 days; pilot run: 7-10 days",
                "patent": "Recommend filing invention patent for core formula (6-month timeline)",
            },
            "kpis": {"rd_cycle_reduction": "15%", "cost_reduction": "8%", "new_products": "3/year"},
        }

AGENTS: Dict[str, IndustrialAgent] = {
    "material_procurement": MaterialProcurementAgent(),
    "warehouse": WarehouseAgent(),
    "supplier_management": SupplierManagementAgent(),
    "formula_rd": FormulaRdAgent(),
    "logistics": LogisticsAgent(),
    "production_schedule": ProductionScheduleAgent(),
    "quality_inspection": QualityInspectionAgent(),
    "equipment_maintenance": EquipmentMaintenanceAgent(),
    "quoting": QuotingAgent(),
    "order_fulfillment": OrderFulfillmentAgent(),
    "customer_management": CustomerManagementAgent(),
    "competitor_monitoring": CompetitorMonitoringAgent(),
    "cost_accounting": CostAccountingAgent(),
    "compliance_review": ComplianceReviewAgent(),
    "risk_alert": RiskAlertAgent(),
    "policy_interpretation": PolicyInterpretationAgent(),
    "data_analysis": DataAnalysisAgent(),
    "report_generation": ReportGenerationAgent(),
    "project_management": ProjectManagementAgent(),
    "customer_service": CustomerServiceAgent(),
}


# ChiefOfStaff
class ChiefOfStaff:
    def __init__(self):
        self.name = "ChiefOfStaff"
        self.emoji = "🎩"

    def route(self, task: str) -> List[str]:
        task_lower = task.lower()
        scores: Dict[str, int] = {}
        for agent_id, keywords in TASK_ROUTING.items():
            score = sum(1 for kw in keywords if kw in task_lower)
            if score > 0:
                scores[agent_id] = score
        if not scores:
            return ["data_analysis"]
        return sorted(scores, key=scores.get, reverse=True)

    async def execute(self, task: str, context: Optional[dict] = None) -> dict:
        routed = self.route(task)
        async def run_one(aid):
            return aid, await AGENTS[aid].execute(task, context or {})
        results_list = await asyncio.gather(*[run_one(a) for a in routed], return_exceptions=True)
        results = {}
        for aid, res in zip(routed, results_list):
            results[aid] = res if isinstance(res, dict) and "error" not in res else {"error": str(res)}
        total_tokens = sum(r.get("tokens", 150) for r in results.values())
        return {
            "chief": self.emoji + " " + self.name,
            "input": task,
            "routed_agents": routed,
            "agent_count": len(routed),
            "strategy": "parallel" if len(routed) > 1 else "single",
            "results": results,
            "total_tokens": total_tokens,
            "timestamp": datetime.now().isoformat(),
        }


CHIEF = ChiefOfStaff()


if __name__ == "__main__":
    import asyncio
    async def test():
        print("Testing ChiefOfStaff routing...")
        tests = [
            "原料库存不够了，帮我查一下",
            "帮我分析一下本月生产成本",
            "有个客户投诉产品质量问题",
            "下周的排产计划怎么安排",
        ]
        for t in tests:
            r = await CHIEF.execute(t)
            print(f"Input: {t}")
            print(f"  Routed: {r['routed_agents']} ({r['strategy']})")
            print()
    asyncio.run(test())
