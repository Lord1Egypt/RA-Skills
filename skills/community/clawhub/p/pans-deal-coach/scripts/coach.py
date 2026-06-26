#!/usr/bin/env python3
"""
pans-deal-coach: AI算力销售谈判教练
输入客户异议，输出专业应对话术和策略
"""

import argparse
import json
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ObjectionType(Enum):
    PRICE = "price"
    COMPETITOR = "competitor"
    TECH = "tech"
    PROCESS = "process"
    SECURITY = "security"


class ClientType(Enum):
    STARTUP = "startup"
    ENTERPRISE = "enterprise"
    GOV = "gov"


class StageType(Enum):
    DISCOVERY = "discovery"
    DEMO = "demo"
    NEGOTIATION = "negotiation"
    CLOSE = "close"


@dataclass
class ObjectionScenario:
    """异议场景定义"""
    id: str
    type: ObjectionType
    title: str
    description: str
    keywords: List[str]


@dataclass
class ResponseTemplate:
    """应对话术模板"""
    short: str      # 简短版（即时回复）
    detailed: str   # 详细版（电话/会议）
    email: str      # 邮件版（书面回复）


@dataclass
class CoachingResult:
    """教练输出结果"""
    objection_analysis: str
    responses: ResponseTemplate
    supporting_materials: List[str]
    warnings: List[str]
    next_steps: List[str]


# ============ 异议场景库 ============
OBJECTION_SCENARIOS: List[ObjectionScenario] = [
    # 价格异议
    ObjectionScenario("price_1", ObjectionType.PRICE, "价格太贵", 
        "客户认为产品/服务价格超出预算或预期", 
        ["贵", "太贵", "价格高", "预算", "便宜", "降价", "折扣"]),
    ObjectionScenario("price_2", ObjectionType.PRICE, "竞品更便宜", 
        "客户提到竞争对手价格更低", 
        ["竞品", "竞争对手", "便宜", "低价", "AWS", "阿里云", "华为云"]),
    ObjectionScenario("price_3", ObjectionType.PRICE, "没有预算", 
        "客户表示当前没有可用预算", 
        ["没预算", "没有预算", "预算不够", "预算不足", "明年预算"]),
    ObjectionScenario("price_4", ObjectionType.PRICE, "需要内部审批", 
        "价格需要内部多层审批", 
        ["审批", "领导审批", "走流程", "申请预算", "层层审批"]),
    
    # 竞品异议
    ObjectionScenario("comp_1", ObjectionType.COMPETITOR, "竞品功能更强", 
        "客户认为竞品功能更全面或更先进", 
        ["功能", "特性", "不如", "比不上", "更强"]),
    ObjectionScenario("comp_2", ObjectionType.COMPETITOR, "竞品市占率高", 
        "客户倾向于选择市场占有率高的品牌", 
        ["市占率", "市场份额", "大家都在用", "主流"]),
    ObjectionScenario("comp_3", ObjectionType.COMPETITOR, "已有供应商", 
        "客户已有长期合作的供应商", 
        ["已有供应商", "长期合作", "关系好", "习惯了"]),
    
    # 技术异议
    ObjectionScenario("tech_1", ObjectionType.TECH, "技术栈不兼容", 
        "担心与现有技术栈不兼容", 
        ["不兼容", "技术栈", "集成", "对接", "适配"]),
    ObjectionScenario("tech_2", ObjectionType.TECH, "担心稳定性", 
        "担心系统稳定性和可靠性", 
        ["稳定", "可靠", "宕机", "故障", "出问题"]),
    ObjectionScenario("tech_3", ObjectionType.TECH, "性能不满足", 
        "担心性能无法达到要求", 
        ["性能", "速度慢", "延迟", "吞吐量", "TPS"]),
    ObjectionScenario("tech_4", ObjectionType.TECH, "迁移成本高", 
        "担心从现有系统迁移的成本和风险", 
        ["迁移", "切换", "数据迁移", "业务中断"]),
    
    # 流程异议
    ObjectionScenario("proc_1", ObjectionType.PROCESS, "决策周期长", 
        "内部决策流程复杂，周期很长", 
        ["周期长", "决策慢", "流程长", "需要时间", "还没决定"]),
    ObjectionScenario("proc_2", ObjectionType.PROCESS, "需要POC", 
        "客户要求进行POC验证", 
        ["POC", "试点", "测试", "验证", "试用"]),
    ObjectionScenario("proc_3", ObjectionType.PROCESS, "多人决策", 
        "涉及多个部门和决策者", 
        ["多部门", "委员会", "集体决策", "要商量"]),
    
    # 安全异议
    ObjectionScenario("sec_1", ObjectionType.SECURITY, "数据安全顾虑", 
        "担心数据安全和隐私保护", 
        ["安全", "隐私", "数据泄露", "合规", "等保"]),
    ObjectionScenario("sec_2", ObjectionType.SECURITY, "合同条款问题", 
        "对合同条款有异议", 
        ["合同", "条款", "SLA", "赔偿", "违约"]),
    ObjectionScenario("sec_3", ObjectionType.SECURITY, "供应商资质", 
        "担心供应商资质和背景", 
        ["资质", "背景", "成立时间", "小公司", "没听过"]),
]


# ============ 应对策略库 ============
RESPONSE_STRATEGIES = {
    ObjectionType.PRICE: {
        "analysis": "客户对价格敏感，可能源于：1)预算确实紧张 2)对价值认知不足 3)采购习惯压价 4)竞品价格锚定",
        "strategies": ["ROI计算", "TCO对比", "分期付款", "阶梯报价", "价值重塑"],
        "short_template": "理解您的考虑。从TCO角度，我们的方案在3年周期内实际成本更低，且性能提升XX%。我们可以安排一次价值分析会议，详细展示ROI计算。",
        "detailed_template": """我完全理解您对价格的关注。让我从几个维度来说明：

1. **TCO对比**：虽然单价高20%，但我们的能效比提升40%，3年电费节省即可覆盖差价
2. **隐性成本**：我们的技术支持响应时间<15分钟，而行业平均是4小时，停机成本差异巨大
3. **性能溢价**：同价位下我们的算力密度高35%，意味着更少的机柜和运维人力

建议我们做一个定制化的ROI计算，用您的实际数据来呈现价值。""",
        "email_template": """您好，

关于价格问题，附件是我们为您准备的TCO对比分析报告。

核心结论：
- 首年投入：我们比竞品高18%
- 3年TCO：我们比竞品低12%（考虑电费、运维、扩容成本）
- 性能收益：训练时间缩短30%，更快上市意味着更早产生业务价值

此外，我们可以提供：
✓ 分期付款方案（降低现金流压力）
✓ 阶梯报价（根据用量增长调整）
✓ 以旧换新补贴（如有现有设备）

期待进一步沟通。""",
        "materials": ["TCO对比计算器", "ROI案例集", "分期付款方案", "客户成功故事"],
        "warnings": ["不要直接降价，而是增加价值", "避免陷入价格战", "确认对方是否有真实采购权限"],
    },
    ObjectionType.COMPETITOR: {
        "analysis": "客户在做比较，这是购买信号。需要：1)了解竞品具体是谁 2)找出差异化优势 3)避免贬低竞品",
        "strategies": ["性能对比", "服务优势", "迁移成本", "差异化定位", "客户证言"],
        "short_template": "感谢您对市场的了解。每家厂商都有各自优势，我们的差异化在于XX。能否告诉我您最看重竞品的哪一点？我可以针对性说明。",
        "detailed_template": """很高兴您在认真比较，这说明您是专业的采购方。我想客观分享几点：

**性能层面**：
- 在ResNet-50训练基准测试中，我们的速度比AWS p4d快23%
- 我们的网络延迟<5μs，对分布式训练至关重要

**服务层面**：
- 专属客户成功经理（竞品是工单制）
- 7×24中文技术支持（竞品是英文邮件）
- 本地化部署支持

**迁移层面**：
- 提供免费的迁移工具和专家支持
- 兼容主流框架，代码改动量<5%

我可以安排一个无偏向的技术对比会议，让您团队自己验证。""",
        "email_template": """您好，

附件是我们与主流竞品的详细对比分析，基于第三方基准测试数据。

关键差异点：
1. **性能**：训练吞吐量领先15-30%（附测试报告）
2. **服务**：专属CSM vs 工单系统，响应时间分钟级 vs 小时级
3. **成本**：隐性成本（停机、支持、迁移）更低

建议：
- 如果追求极致性价比且团队技术能力强，竞品也是不错的选择
- 如果需要稳定可靠的生产环境和企业级支持，我们的方案更合适

我们愿意提供POC环境，让您团队实测对比。""",
        "materials": ["竞品对比白皮书", "第三方Benchmark报告", "客户迁移案例", "服务SLA说明"],
        "warnings": ["不要贬低竞品，保持专业", "了解客户真实选择竞品的动机", "确认竞品是真实威胁还是压价手段"],
    },
    ObjectionType.TECH: {
        "analysis": "客户对技术实现有顾虑，需要：1)展示技术兼容性 2)提供迁移方案 3)建立技术信任",
        "strategies": ["兼容性说明", "技术支持", "迁移方案", "架构咨询", "POC验证"],
        "short_template": "技术兼容性确实是关键考虑。我们的方案支持主流框架（PyTorch/TensorFlow/JAX），且提供完整的迁移工具链。建议安排一次架构师交流，针对您的具体技术栈做评估。",
        "detailed_template": """技术兼容性和稳定性是生产环境的核心关切，让我详细说明：

**兼容性**：
- 支持CUDA、ROCm、OpenCL等主流计算框架
- 与Kubernetes、Slurm、OpenStack无缝集成
- 提供Python/C++/Java SDK

**迁移支持**：
- 免费迁移评估（评估现有代码改动量）
- 提供自动化迁移工具（代码转换脚本）
- 驻场迁移支持（前2周免费）

**稳定性保障**：
- 99.99% SLA承诺
- 双活架构设计
- 7×24监控和自动故障切换

我们可以先做一个技术可行性评估，零成本验证兼容性。""",
        "email_template": """您好，

关于技术兼容性顾虑，附件是详细的技术白皮书和迁移指南。

**兼容性矩阵**：
- 深度学习框架：PyTorch 1.9+, TensorFlow 2.6+, JAX 0.3+
- 容器编排：Kubernetes 1.20+, Docker 20.10+
- 调度系统：Slurm 20.02+, PBS Pro

**迁移保障**：
1. 免费技术评估（1-2个工作日）
2. 迁移工具包（代码扫描+自动转换）
3. 技术支持（迁移期间专属工程师跟进）

**稳定性承诺**：
- 99.99%可用性SLA
- 年度停机时间<52分钟
- 故障恢复时间<15分钟

建议先进行小规模POC验证。""",
        "materials": ["技术白皮书", "兼容性矩阵", "迁移指南", "架构最佳实践", "SLA协议"],
        "warnings": ["不要过度承诺技术能力", "确保技术团队能兑现承诺", "POC范围要可控"],
    },
    ObjectionType.PROCESS: {
        "analysis": "客户内部流程复杂，需要：1)了解决策链 2)提供决策支持材料 3)寻找加速突破口",
        "strategies": ["决策链分析", "加速方案", "支持材料", "高层接触", "试点切入"],
        "short_template": "理解贵司的决策流程。为了加速推进，我可以提供完整的决策支持材料包（ROI分析、风险评估、同行案例）。另外，是否可以安排一次与技术/业务负责人的直接交流？",
        "detailed_template": """大型组织的采购决策确实需要多方协调。让我看看如何帮您推进：

**决策支持材料**：
- 高管摘要（1页纸，适合C-level汇报）
- 技术评估报告（给CTO/架构团队）
- 财务分析（给CFO/采购）
- 风险评估与缓解方案（给合规/法务）

**加速建议**：
1. **试点先行**：申请一个部门的小规模试点，降低决策风险
2. **高层对齐**：我可以安排我们的VP与贵司VP级别交流
3. **同行背书**：安排与已采购的同行企业交流
4. **时间窗口**：了解贵司预算周期，在合适时机推进

您看哪种方式对当前阶段最有帮助？""",
        "email_template": """您好，

附件是完整的决策支持材料包，可直接用于内部汇报：

**材料清单**：
1. 高管摘要（1页，核心价值主张）
2. 技术评估报告（架构、性能、兼容性）
3. 财务分析（3年TCO、ROI计算）
4. 风险评估（风险点+缓解措施）
5. 同行案例（3家同行业客户证言）

**建议推进路径**：
- 第1周：技术团队POC验证
- 第2周：业务部门试用反馈
- 第3周：综合评估与决策
- 第4周：合同与交付

如需我们配合拜访任何决策相关方，请随时告知。""",
        "materials": ["高管摘要", "技术评估模板", "财务分析表", "风险评估矩阵", "同行案例库"],
        "warnings": ["了解真实的决策链和关键人", "识别流程拖延vs真实障碍", "不要绕过关键决策人"],
    },
    ObjectionType.SECURITY: {
        "analysis": "客户对安全和合规有顾虑，需要：1)展示安全认证 2)说明合规能力 3)提供审计支持",
        "strategies": ["安全认证", "合规说明", "审计支持", "数据主权", "合同协商"],
        "short_template": "安全和合规是我们最重视的方面。我们已通过等保三级、ISO27001、SOC2认证，支持私有化部署。我可以安排安全架构师与您详细交流。",
        "detailed_template": """数据安全和合规是AI基础设施的核心考量，我们完全理解：

**安全认证**：
- 等保三级（中国）
- ISO 27001信息安全管理
- SOC 2 Type II审计
- GDPR合规（欧盟客户）

**数据保护**：
- 端到端加密（传输+存储）
- 数据隔离（多租户架构）
- 审计日志完整记录
- 支持客户自带密钥（BYOK）

**部署灵活性**：
- 私有化部署（数据不出机房）
- 混合云架构
- 本地+云端协同

**合同保障**：
- 数据所有权归客户
- 明确的数据删除条款
- 安全事件响应SLA

我们可以签署NDA后提供更详细的安全白皮书。""",
        "email_template": """您好，

关于安全和合规顾虑，附件是详细的安全白皮书和认证证书。

**合规认证**：
- 网络安全等级保护（等保三级）
- ISO/IEC 27001:2013
- SOC 2 Type II
- 可信云认证

**数据安全措施**：
1. 物理安全：Tier IV数据中心，生物识别门禁
2. 网络安全：DDoS防护、WAF、入侵检测
3. 数据安全：AES-256加密、数据分级保护
4. 访问控制：RBAC、MFA、最小权限原则

**合同条款**：
- 我们愿意就SLA、赔偿、数据主权等条款进行协商
- 支持客户法务团队的安全审查

如需安排安全架构师交流或现场审计，请随时联系。""",
        "materials": ["安全白皮书", "合规认证证书", "渗透测试报告", "SLA协议模板", "数据安全协议"],
        "warnings": ["安全承诺必须有法律和认证支撑", "不要隐瞒已知的安全限制", "私有化部署成本要评估清楚"],
    },
}


# ============ 客户类型适配 ============
CLIENT_ADAPTATIONS = {
    ClientType.STARTUP: {
        "tone": "灵活、敏捷、成长导向",
        "focus": ["快速上线", "按需付费", "技术支持", "成长陪伴"],
        "pricing": "推荐按需付费、阶梯定价、成长套餐",
        "materials": ["快速启动指南", "创业公司案例", "灵活的付款方案"],
    },
    ClientType.ENTERPRISE: {
        "tone": "专业、稳健、风险可控",
        "focus": ["稳定性", "合规性", "TCO优化", "长期合作"],
        "pricing": "推荐多年合约、批量折扣、定制化方案",
        "materials": ["企业级白皮书", "行业标杆案例", "完整的合规文档"],
    },
    ClientType.GOV: {
        "tone": "合规、安全、国产化",
        "focus": ["等保合规", "国产化适配", "数据主权", "长期服务"],
        "pricing": "推荐预算内报价、分年付款、国产化方案",
        "materials": ["等保测评报告", "国产化适配证明", "政府案例", "长期服务承诺"],
    },
}


# ============ 销售阶段适配 ============
STAGE_ADAPTATIONS = {
    StageType.DISCOVERY: {
        "approach": "以倾听和诊断为主，了解真实需求",
        "goal": "建立信任，明确客户痛点",
        "next_action": "安排深度需求调研会议",
    },
    StageType.DEMO: {
        "approach": "展示价值，解答技术疑问",
        "goal": "让客户看到解决方案的可行性",
        "next_action": "安排POC或技术验证",
    },
    StageType.NEGOTIATION: {
        "approach": "聚焦商务条款，寻找双赢方案",
        "goal": "就核心条款达成一致",
        "next_action": "推进合同签署",
    },
    StageType.CLOSE: {
        "approach": "消除最后顾虑，促成签约",
        "goal": "完成交易",
        "next_action": "启动交付流程",
    },
}


class DealCoach:
    """销售谈判教练主类"""
    
    def __init__(self, lang: str = "zh"):
        self.lang = lang
    
    def detect_objection_type(self, objection_text: str, hint_type: Optional[str] = None) -> ObjectionType:
        """检测异议类型"""
        if hint_type:
            return ObjectionType(hint_type)
        
        text_lower = objection_text.lower()
        scores = {t: 0 for t in ObjectionType}
        
        # 基于关键词匹配
        price_keywords = ["贵", "便宜", "价格", "预算", "钱", "费用", "成本", "aws", "阿里云", "华为云", "竞品", "竞争"]
        comp_keywords = ["竞品", "竞争", "对手", "别家", "其他", "market", "share", "市占率", "功能"]
        tech_keywords = ["技术", "兼容", "集成", "稳定", "性能", "迁移", "架构", "bug", "问题"]
        proc_keywords = ["流程", "审批", "决策", "poc", "试点", "测试", "试用", "周期", "时间"]
        sec_keywords = ["安全", "合规", "隐私", "数据", "合同", "条款", "sla", "资质", "认证"]
        
        for kw in price_keywords:
            if kw in text_lower:
                scores[ObjectionType.PRICE] += 1
        for kw in comp_keywords:
            if kw in text_lower:
                scores[ObjectionType.COMPETITOR] += 1
        for kw in tech_keywords:
            if kw in text_lower:
                scores[ObjectionType.TECH] += 1
        for kw in proc_keywords:
            if kw in text_lower:
                scores[ObjectionType.PROCESS] += 1
        for kw in sec_keywords:
            if kw in text_lower:
                scores[ObjectionType.SECURITY] += 1
        
        return max(scores, key=scores.get)
    
    def get_response(self, objection_text: str, obj_type: ObjectionType, 
                     client_type: ClientType, stage: StageType) -> CoachingResult:
        """生成应对策略"""
        strategy = RESPONSE_STRATEGIES.get(obj_type, RESPONSE_STRATEGIES[ObjectionType.PRICE])
        client_adapt = CLIENT_ADAPTATIONS[client_type]
        stage_adapt = STAGE_ADAPTATIONS[stage]
        
        # 构建分析
        analysis = f"【异议类型】{obj_type.value}\n"
        analysis += f"【客户背景】{client_type.value} - {client_adapt['tone']}\n"
        analysis += f"【销售阶段】{stage.value} - {stage_adapt['approach']}\n\n"
        analysis += f"【深度分析】{strategy['analysis']}\n\n"
        analysis += f"【推荐策略】{', '.join(strategy['strategies'])}\n"
        analysis += f"【客户关注点】{', '.join(client_adapt['focus'])}"
        
        # 构建话术（根据客户类型微调）
        short = strategy['short_template']
        detailed = strategy['detailed_template']
        email = strategy['email_template']
        
        # 根据客户类型添加个性化内容
        if client_type == ClientType.STARTUP:
            short += "\n\n另外，针对创业公司我们有特别的成长支持计划，包括灵活的付款方式。"
        elif client_type == ClientType.GOV:
            short += "\n\n我们完全理解政府项目的合规要求，可以提供全套的等保和国产化适配文档。"
        
        responses = ResponseTemplate(short, detailed, email)
        
        # 合并支持材料
        materials = strategy['materials'] + client_adapt['materials']
        
        # 构建注意事项
        warnings = strategy['warnings'][:]
        warnings.append(f"当前阶段目标：{stage_adapt['goal']}")
        
        # 下一步行动
        next_steps = [
            stage_adapt['next_action'],
            "记录客户反馈，更新CRM",
            "准备相应的支持材料",
            "安排下次跟进时间"
        ]
        
        return CoachingResult(analysis, responses, materials, warnings, next_steps)
    
    def list_scenarios(self) -> str:
        """列出所有异议场景"""
        result = "🎯 常见异议场景库（共{}个）\n".format(len(OBJECTION_SCENARIOS))
        result += "=" * 50 + "\n\n"
        
        current_type = None
        for scenario in OBJECTION_SCENARIOS:
            if scenario.type != current_type:
                current_type = scenario.type
                result += f"\n【{current_type.value.upper()}】\n"
            result += f"  • {scenario.title}: {scenario.description}\n"
        
        return result
    
    def format_output(self, result: CoachingResult, objection_text: str) -> str:
        """格式化输出"""
        output = []
        output.append("=" * 60)
        output.append("🤖 AI算力销售谈判教练")
        output.append("=" * 60)
        output.append("")
        output.append(f"📌 客户异议: {objection_text}")
        output.append("")
        output.append("-" * 60)
        output.append("🎯 异议分析")
        output.append("-" * 60)
        output.append(result.objection_analysis)
        output.append("")
        output.append("-" * 60)
        output.append("💡 应对话术")
        output.append("-" * 60)
        output.append("")
        output.append("【简短版 - 即时回复】")
        output.append(result.responses.short)
        output.append("")
        output.append("【详细版 - 电话/会议】")
        output.append(result.responses.detailed)
        output.append("")
        output.append("【邮件版 - 书面回复】")
        output.append(result.responses.email)
        output.append("")
        output.append("-" * 60)
        output.append("📊 支持材料建议")
        output.append("-" * 60)
        for i, material in enumerate(result.supporting_materials, 1):
            output.append(f"  {i}. {material}")
        output.append("")
        output.append("-" * 60)
        output.append("⚠️ 注意事项")
        output.append("-" * 60)
        for i, warning in enumerate(result.warnings, 1):
            output.append(f"  {i}. {warning}")
        output.append("")
        output.append("-" * 60)
        output.append("🚀 下一步行动")
        output.append("-" * 60)
        for i, step in enumerate(result.next_steps, 1):
            output.append(f"  {i}. {step}")
        output.append("")
        output.append("=" * 60)
        
        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="AI算力销售谈判教练 - 输入客户异议，输出专业应对话术",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --objection "你们比AWS贵30%%" --type price --client enterprise
  %(prog)s --objection "需要内部审批" --type process --client gov --stage negotiation
  %(prog)s --list
        """
    )
    parser.add_argument("--objection", "-o", help="客户异议内容")
    parser.add_argument("--type", "-t", 
                       choices=[t.value for t in ObjectionType],
                       help="异议类型 (price/competitor/tech/process/security)")
    parser.add_argument("--client", "-c",
                       choices=[t.value for t in ClientType],
                       default="enterprise",
                       help="客户背景 (startup/enterprise/gov)，默认enterprise")
    parser.add_argument("--stage", "-s",
                       choices=[t.value for t in StageType],
                       default="discovery",
                       help="销售阶段 (discovery/demo/negotiation/close)，默认discovery")
    parser.add_argument("--list", "-l", action="store_true",
                       help="列出所有异议场景")
    parser.add_argument("--lang",
                       choices=["zh", "en"],
                       default="zh",
                       help="输出语言 (zh/en)，默认zh")
    parser.add_argument("--json", action="store_true",
                       help="以JSON格式输出")
    
    args = parser.parse_args()
    
    coach = DealCoach(lang=args.lang)
    
    if args.list:
        print(coach.list_scenarios())
        return
    
    if not args.objection:
        parser.error("请提供客户异议内容 (--objection)，或使用 --list 查看场景列表")
    
    # 检测异议类型
    obj_type = coach.detect_objection_type(args.objection, args.type)
    client_type = ClientType(args.client)
    stage = StageType(args.stage)
    
    # 生成应对策略
    result = coach.get_response(args.objection, obj_type, client_type, stage)
    
    if args.json:
        output = {
            "objection": args.objection,
            "type": obj_type.value,
            "client": client_type.value,
            "stage": stage.value,
            "analysis": result.objection_analysis,
            "responses": asdict(result.responses),
            "materials": result.supporting_materials,
            "warnings": result.warnings,
            "next_steps": result.next_steps
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(coach.format_output(result, args.objection))


if __name__ == "__main__":
    main()
