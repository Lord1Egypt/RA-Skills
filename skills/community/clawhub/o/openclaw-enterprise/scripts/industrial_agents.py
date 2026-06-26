#!/usr/bin/env python3
"""Industrial Silicon Army - 20 Industrial Agents + ChiefOfStaff"""
import asyncio, json
from datetime import datetime
from typing import Dict, Any, List, Optional

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
    "competitor_monitoring": ["同行","同行对手","市场","定价","份额"],
    "cost_accounting": ["成本","毛利","利润","盈亏","核算"],
    "compliance_review": ["合规","环保","安全","税务","法规","认证"],
    "risk_alert": ["风险","提醒","呆账","坏账","信用"],
    "policy_interpretation": ["政策","补贴","税务优惠","扶持","申报"],
    "data_analysis": ["数据","报表","日报","月报","经营","分析"],
    "report_generation": ["报告","会议","纪要","文档","PPT"],
    "project_management": ["项目","里程碑","进度","交付","管理"],
    "customer_service": ["售后","投诉","客服","退换","服务"],
}

AGENT_REGISTRY: Dict[str, dict] = {}
AGENT_CALL_LOG: List[dict] = []

def log_call(agent_id: str, task: str, tokens: int):
    if agent_id in AGENT_REGISTRY:
        AGENT_REGISTRY[agent_id]["invoked_count"] += 1
        AGENT_REGISTRY[agent_id]["total_tokens"] += tokens
    AGENT_CALL_LOG.append({"agent": agent_id, "task": task, "tokens": tokens, "time": datetime.now().isoformat()})

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
            "Procurement planning, market analysis, price reference",
            ["supplier recommendations","market analysis","price reference","procurement planning"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "suppliers": ["华锦化工(浙江)","中石化A供应商","山东工程塑料厂"],
                "market_analysis": "Raw material prices trending. Suggested to consider partial stock-up planning.",
                "price_comparison": "Reference price: 12.5 CNY/kg; Bulk reference: 11.8 CNY/kg",
                "procurement_plan": "Stage 1: 30% stock consideration; Stage 2: continue monitoring trend",
                "delivery": "Reference delivery: 7-10 business days",
                "risks": ["delivery considerations","quality factors","logistics planning"],
            },
            "kpis": {"on_time_delivery": "92%", "quality_pass": "97%", "cost_saving": "3.2%"},
        }


class WarehouseAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("warehouse", "仓储管理Agent", "🏭",
            "Inventory planning, location optimization, turnover analysis",
            ["inventory planning","location optimization","ABC analysis","turnover"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "alerts": ["Material A: 15T, below safety level 20T - attention needed",
                           "Material B: 80T, above safety level 50T - normal range",
                           "Finished goods C: 1200pcs overstock (+30%) - review suggested"],
                "suggestion": "Relocate Material A to A-01 (near exit) for +15% picking efficiency",
                "turnover": "Average turnover 18 days, reference target 20 days - good",
                "slow_moving": "3 items >90 days slow-moving, clearance consideration suggested",
            },
            "kpis": {"turnover": "14x/year", "space_util": "82%", "slow_rate": "2.1%"},
        }


class LogisticsAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("logistics", "物流调度Agent", "🚛",
            "Fleet matching, route optimization, cost control",
            ["fleet matching","route optimization","cost control","shipping planning"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "dispatch": "Reference: Deppon (fast) or Anneng (cost-effective)",
                "route_optimization": "Group orders by region, consolidate shipping, potential 18% freight savings",
                "tracking": "Shipping reference through logistics planning",
                "cost_analysis": {"Deppon": "12+2 CNY/kg", "Anneng": "1.8 CNY/kg", "专线": "1.2 CNY/kg"},
                "alerts": "2 shipments may face delays due to traffic - driver notification suggested",
            },
            "kpis": {"freight_ratio": "4.8%", "on_time": "96%", "damage_rate": "0.12%"},
        }


class ProductionScheduleAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("production_schedule", "生产调度Agent", "⚙️",
            "Production scheduling, work order planning, delivery reference",
            ["smart scheduling","work orders","delivery","capacity"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "schedule": "Order A (URGENT): Thu deadline; Order B: Sat deadline",
                "capacity_utilization": "Current load: 78%, remaining: 22%",
                "delivery_commitment": "Standard: 14 days; Rush: 7 days (+15% fee)",
                "bottleneck": "Injection molding at 97% utilization - adding 1 machine consideration suggested",
                "outsource": "Non-core processes can be outsourced, potential 8% cost savings",
            },
            "kpis": {"delivery_achievement": "95%", "capacity_util": "78%", "machine_uptime": "85%"},
        }


class QualityInspectionAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("quality_inspection", "质量检测Agent", "🔬",
            "Quality planning, inspection recommendations, control suggestions",
            ["AQL sampling","incoming inspection","process control","quality planning"])

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
            "Maintenance planning, fault prediction, downtime prevention",
            ["predictive maintenance","fault diagnosis","maintenance planning","spare parts"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "prediction_alert": "Injection machine #3 main bearing temp high, potential issue within 7 days, maintenance scheduling suggested",
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
            "Quote generation, cost-plus pricing reference, negotiation support",
            ["quote generation","cost-plus","negotiation","validity"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "quote": "FOB 18.5 CNY/kg, CIF 22.3 CNY/kg (reference generated)",
                "cost_breakdown": {"material": "65%", "processing": "20%", "overhead": "8%", "margin": "7%"},
                "discount_space": ">5MT one-time: 3% discount; long-term: 5% rebate",
                "validity": "Quote reference valid for 14 days",
                "response_time": "Generate reference <30s, human review <5min",
            },
            "kpis": {"response_time": "<5min", "accuracy": "99%", "margin_achievement": "96%"},
        }


class OrderFulfillmentAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("order_fulfillment", "订单履约Agent", "📦",
            "Order coordination, exception handling recommendations, customer experience",
            ["order coordination","exception handling","delivery planning","customer notify"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "order_status": "12 in-transit, 9 normal, 3 exceptions (escalated)",
                "delivery_alert": "2 orders may face delays due to material considerations, customer notification suggested",
                "tracking": "8 shipments tracked",
                "complaints": "3 handled this week, CSAT 4.6/5.0",
            },
            "kpis": {"fulfillment_rate": "97%", "on_time": "94%", "csat": "4.6/5"},
        }


class CustomerManagementAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("customer_management", "客户管理Agent", "🤝",
            "Customer segmentation, follow-up planning, repurchase recommendations",
            ["segmentation","follow-up planning","repurchase","customer engagement"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "segmentation": {"A-tier (key accounts)": "8 (65% revenue)", "B-tier": "25", "C-tier": "47"},
                "follow_up": "3 follow-ups scheduled this week (1 already done)",
                "churn_alert": "Customer #12: 60 days no order - attention recommended",
                "repurchase": "Promote quarterly promotion to high-value customers, expect 15% activation",
            },
            "kpis": {"repurchase_rate": "62%", "satisfaction": "91%", "churn_rate": "5.3%"},
        }


class CompetitorMonitoringAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("competitor_monitoring", "同行关注Agent", "🎯",
            "Market trend analysis, competitor insights, pricing strategy recommendations",
            ["market trends","competitor insights","substitutes","market planning"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "market_trends": "Product A: price stable; Product B: slight increase 2%",
                "competitor_intel": "Competitor X launched new model, targeting mid-range",
                "substitute_alerts": "Alternative material Y price down 5%, worth evaluating",
                "pricing_strategy": "Current pricing competitive, slight adjustment may increase margin",
            },
            "kpis": {"market_share": "23%", "pricing_alignment": "98%", "trend_accuracy": "87%"},
        }


class CostAccountingAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("cost_accounting", "成本核算Agent", "🧮",
            "Cost analysis, margin planning, profitability recommendations",
            ["cost analysis","margin planning","profitability","standard cost"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "actual_cost": "18.2 CNY/kg (vs standard 18.5 CNY/kg)",
                "margin_analysis": "Product A: 23%; Product B: 31%",
                "variance": "Material cost +3%, labor cost -2% vs last month",
                "profitability": "Top 3 profitable: A, C, E; Bottom 3: B, D, F",
            },
            "kpis": {"cost_accuracy": "98%", "margin_achievement": "96%", "variance": "2.1%"},
        }


class ComplianceReviewAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("compliance_review", "合规审查Agent", "⚖️",
            "Compliance planning, regulation interpretation, risk prevention",
            ["compliance planning","regulation","safety","tax planning"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "compliance_check": "ISO 9001 renewal due in 60 days, preparation checklist ready",
                "environmental": "New emission standards effective Jan 2026, upgrade needed",
                "safety": "Quarterly safety audit scheduled, 3 minor issues from last audit resolved",
                "tax": "R&D expense add-back policy update, potential 50K savings",
            },
            "kpis": {"compliance_rate": "100%", "audit_score": "98%", "penalty_avoidance": "0"},
        }


class RiskAlertAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("risk_alert", "风险提醒Agent", "🚨",
            "Risk assessment, credit evaluation, loss prevention",
            ["risk assessment","credit evaluation","loss prevention","credit monitoring"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "credit_alerts": ["Customer #8: payment 45 days overdue, collection suggested",
                                  "Customer #15: credit limit exceeded, approval needed"],
                "material_risks": "Raw material price volatility medium, hedging recommended",
                "bad_debt_provision": "Current provision 2.5%, recommendation: maintain",
                "supplier_risks": "Supplier C capacity concerns, alternative sourcing suggested",
            },
            "kpis": {"bad_debt_ratio": "0.8%", "credit_utilization": "72%", "risk_coverage": "95%"},
        }


class PolicyInterpretationAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("policy_interpretation", "政策解读Agent", "📜",
            "Policy interpretation, subsidy applications, tax benefit planning",
            ["policy interpretation","subsidy applications","tax benefits","regulations"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "policy_alerts": "New energy subsidy policy, potential 200K annual benefit",
                "subsidy_application": "Tech innovation fund application window opens next month",
                "tax_benefits": "High-tech enterprise renewal saves ~500K/year",
                "industry_trends": "Government encouraging smart manufacturing, relevant subsidies available",
            },
            "kpis": {"subsidy_amount": "1.2M", "tax_savings": "800K", "policy_utilization": "85%"},
        }


class DataAnalysisAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("data_analysis", "数据分析Agent", "📊",
            "Data aggregation, report generation, trend analysis",
            ["data aggregation","report generation","trend analysis","BI planning"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "daily_report": "Sales +5% vs last week, production on track",
                "monthly_summary": "Revenue 12.5M, gross margin 28.3%, meeting targets",
                "trends": "Online sales growing 15% MoM, recommended focus area",
                "kpi_dashboard": "12 metrics updated, 3 need attention",
            },
            "kpis": {"report_accuracy": "99%", "timeliness": "100%", "coverage": "100%"},
        }


class ReportGenerationAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("report_generation", "报告生成Agent", "📝",
            "Document generation, meeting minutes, presentation materials",
            ["document generation","meeting minutes","presentation","content creation"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "document_type": "Quarterly business review",
                "sections": ["Executive summary", "Performance analysis", "Challenges", "Next quarter plan"],
                "format": "PowerPoint + Word report generated",
                "meeting_minutes": "3 meetings transcribed, action items extracted",
            },
            "kpis": {"generation_time": "5min", "quality_score": "4.5/5", "revision_rate": "15%"},
        }


class ProjectManagementAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("project_management", "项目管理Agent", "📅",
            "Project planning, milestone tracking, risk assessment",
            ["project planning","milestone tracking","risk assessment","delivery planning"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "project_status": "Phase 2 in progress, 65% complete",
                "milestones": "3 completed on time, 1 delayed (2 weeks)",
                "risks": "Resource shortage risk medium, mitigation plan ready",
                "next_steps": ["Testing next week", "Client review scheduled", "Go-live planning"],
            },
            "kpis": {"on_time_delivery": "75%", "budget_utilization": "68%", "risk_exposure": "medium"},
        }


class CustomerServiceAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("customer_service", "客服支持Agent", "🎧",
            "Support planning, complaint handling, FAQ generation",
            ["support planning","complaint handling","FAQ","service quality"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "open_tickets": "12 pending, avg response time 2.3h",
                "complaint_resolution": "8 complaints this week, 6 resolved, 2 escalated",
                "faq_suggestions": "Top 3 issues: delivery time, product quality, pricing",
                "satisfaction_trend": "CSAT 4.5/5, +0.1 vs last month",
            },
            "kpis": {"response_time": "2.3h", "resolution_rate": "85%", "csat": "4.5/5"},
        }


class SupplierManagementAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("supplier_management", "供应商管理Agent", "🤝",
            "Supplier evaluation, contract planning, performance assessment",
            ["supplier evaluation","contract planning","performance assessment","supplier KPI"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "supplier_ratings": {"A-tier": 5, "B-tier": 12, "C-tier": 8},
                "performance": "Top performer: Supplier X (98% on-time); Underperformer: Supplier Y",
                "contract_review": "3 contracts expiring in 60 days, renewal planning needed",
                "risk_assessment": "1 supplier capacity at risk, alternative recommended",
            },
            "kpis": {"supplier_quality": "94%", "on_time_delivery": "91%", "cost_competitiveness": "96%"},
        }


class FormulaRdAgent(IndustrialAgent):
    def __init__(self):
        super().__init__("formula_rd", "配方研发Agent", "🧪",
            "New material research, substitute planning, cost optimization",
            ["new material research","substitute planning","cost optimization","R&D planning"])

    async def _run(self, task: str, ctx: dict) -> dict:
        return {
            "input": task,
            "result": {
                "new_materials": "3 new materials tested, 1 approved for trial production",
                "substitute_options": "Material A substitute available, 12% cost reduction potential",
                "formula_optimization": "Current formula efficiency 85%, target 90%",
                "R&D_pipeline": "5 projects in progress, 2 near completion",
            },
            "kpis": {"R&D_success": "65%", "cost_reduction": "8%", "time_to_market": "6months"},
        }
