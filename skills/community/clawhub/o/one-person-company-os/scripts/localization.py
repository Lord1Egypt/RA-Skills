#!/usr/bin/env python3
"""Localization helpers for One Person Company OS."""

from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any


SUPPORTED_LANGUAGES = ("zh-CN", "en-US")
DEFAULT_LANGUAGE = "zh-CN"

LANGUAGE_ALIASES = {
    "zh": "zh-CN",
    "zh-cn": "zh-CN",
    "zh_hans": "zh-CN",
    "zh-hans": "zh-CN",
    "cn": "zh-CN",
    "chinese": "zh-CN",
    "simplified-chinese": "zh-CN",
    "en": "en-US",
    "en-us": "en-US",
    "en_us": "en-US",
    "english": "en-US",
    "auto": "auto",
}

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def pick_text(language: str, zh: str, en: str) -> str:
    return zh if language == "zh-CN" else en


def contains_cjk(text: str) -> bool:
    return bool(CJK_RE.search(text))


def detect_language(*texts: object, default: str = DEFAULT_LANGUAGE) -> str:
    combined = " ".join(str(text) for text in texts if text)
    if not combined.strip():
        return default
    return "zh-CN" if contains_cjk(combined) else "en-US"


def normalize_language(value: str | None, *hints: object, default: str = DEFAULT_LANGUAGE) -> str:
    if value:
        key = value.strip().lower()
        normalized = LANGUAGE_ALIASES.get(key)
        if normalized and normalized != "auto":
            return normalized
        if normalized == "auto":
            return detect_language(*hints, default=default)
    return detect_language(*hints, default=default)


def format_list(items: Iterable[str], language: str) -> str:
    values = [item for item in items if item]
    fallback = pick_text(language, "无", "None")
    if not values:
        values = [fallback]
    return "\n".join(f"- {item}" for item in values)


def joined_text(values: Iterable[str], language: str) -> str:
    cleaned = [value for value in values if value]
    if not cleaned:
        return pick_text(language, "无", "None")
    separator = "；" if language == "zh-CN" else "; "
    return separator.join(cleaned)


def bool_label(value: bool, language: str) -> str:
    return pick_text(language, "是", "Yes") if value else pick_text(language, "否", "No")


def bool_audit_label(value: bool, language: str) -> str:
    return pick_text(language, "通过", "Pass") if value else pick_text(language, "未通过", "Fail")


STEP_CATALOG = {
    1: {
        "zh-CN": {"system": "模式判定", "human": "先判断这次要进入哪个流程"},
        "en-US": {"system": "Mode Selection", "human": "Decide which flow this run should enter"},
    },
    2: {
        "zh-CN": {"system": "preflight 与保存策略检查", "human": "先确认环境、保存条件和执行方式"},
        "en-US": {"system": "Preflight And Persistence Strategy Check", "human": "Confirm the environment, persistence conditions, and execution path"},
    },
    3: {
        "zh-CN": {"system": "草案 / 变更提议 / 当前状态装载", "human": "先装载现状，再准备草案或变更"},
        "en-US": {"system": "Draft / Proposed Change / Current State Load", "human": "Load the current state, then prepare the draft or proposed change"},
    },
    4: {
        "zh-CN": {"system": "执行与落盘", "human": "开始执行，并把结果写入工作区"},
        "en-US": {"system": "Execution And Persistence", "human": "Execute and write the result into the workspace"},
    },
    5: {
        "zh-CN": {"system": "验证与回报", "human": "核对结果、说明变化并给出回报"},
        "en-US": {"system": "Verification And Reporting", "human": "Verify the result, explain the changes, and report back"},
    },
}

STEP_ALIASES = {
    "模式判定": 1,
    "mode selection": 1,
    "环境检查": 2,
    "preflight 与保存策略检查": 2,
    "preflight and persistence strategy check": 2,
    "工作区检查": 3,
    "组装初始状态": 3,
    "加载当前状态": 3,
    "组装角色 brief": 3,
    "草案 / 变更提议 / 当前状态装载": 3,
    "draft / proposed change / current state load": 3,
    "保存策略判定": 4,
    "执行与落盘": 4,
    "execution and persistence": 4,
    "验证与回报": 5,
    "verification and reporting": 5,
}

MODE_LABELS = {
    "create-company": {"zh-CN": "创建公司", "en-US": "Create Company"},
    "init-business": {"zh-CN": "初始化经营系统", "en-US": "Initialize Business OS"},
    "start-round": {"zh-CN": "启动回合", "en-US": "Start Round"},
    "advance-round": {"zh-CN": "推进回合", "en-US": "Advance Round"},
    "calibrate-round": {"zh-CN": "校准回合", "en-US": "Calibrate Round"},
    "transition-stage": {"zh-CN": "切换阶段", "en-US": "Transition Stage"},
    "update-focus": {"zh-CN": "更新主焦点", "en-US": "Update Focus"},
    "advance-offer": {"zh-CN": "推进价值承诺", "en-US": "Advance Offer"},
    "advance-pipeline": {"zh-CN": "推进成交管道", "en-US": "Advance Pipeline"},
    "advance-product": {"zh-CN": "推进产品与上线", "en-US": "Advance Product"},
    "advance-delivery": {"zh-CN": "推进交付与回款", "en-US": "Advance Delivery"},
    "update-cash": {"zh-CN": "更新现金状态", "en-US": "Update Cash"},
    "record-asset": {"zh-CN": "记录资产沉淀", "en-US": "Record Asset"},
    "calibrate-business": {"zh-CN": "校准经营决策", "en-US": "Calibrate Business"},
    "migrate-workspace": {"zh-CN": "迁移工作区", "en-US": "Migrate Workspace"},
    "validate-system": {"zh-CN": "校验经营系统", "en-US": "Validate Business OS"},
    "build-agent-brief": {"zh-CN": "生成角色 Brief", "en-US": "Build Agent Brief"},
    "generate-artifact-document": {"zh-CN": "生成正式交付文档", "en-US": "Generate Formal Deliverable Document"},
    "save-checkpoint": {"zh-CN": "保存检查点", "en-US": "Save Checkpoint"},
    "preflight-check": {"zh-CN": "运行环境检查", "en-US": "Runtime Preflight Check"},
    "python-runtime": {"zh-CN": "Python 兼容恢复", "en-US": "Python Runtime Recovery"},
}

MODE_ALIASES = {
    "创建公司": "create-company",
    "create company": "create-company",
    "create-company": "create-company",
    "初始化经营系统": "init-business",
    "initialize business os": "init-business",
    "init-business": "init-business",
    "启动回合": "start-round",
    "start round": "start-round",
    "start-round": "start-round",
    "推进回合": "advance-round",
    "advance round": "advance-round",
    "advance-round": "advance-round",
    "校准回合": "calibrate-round",
    "calibrate round": "calibrate-round",
    "calibrate-round": "calibrate-round",
    "切换阶段": "transition-stage",
    "transition stage": "transition-stage",
    "transition-stage": "transition-stage",
    "更新主焦点": "update-focus",
    "update focus": "update-focus",
    "update-focus": "update-focus",
    "推进价值承诺": "advance-offer",
    "advance offer": "advance-offer",
    "advance-offer": "advance-offer",
    "推进成交管道": "advance-pipeline",
    "advance pipeline": "advance-pipeline",
    "advance-pipeline": "advance-pipeline",
    "推进产品与上线": "advance-product",
    "advance product": "advance-product",
    "advance-product": "advance-product",
    "推进交付与回款": "advance-delivery",
    "advance delivery": "advance-delivery",
    "advance-delivery": "advance-delivery",
    "更新现金状态": "update-cash",
    "update cash": "update-cash",
    "update-cash": "update-cash",
    "记录资产沉淀": "record-asset",
    "record asset": "record-asset",
    "record-asset": "record-asset",
    "校准经营决策": "calibrate-business",
    "calibrate business": "calibrate-business",
    "calibrate-business": "calibrate-business",
    "迁移工作区": "migrate-workspace",
    "migrate workspace": "migrate-workspace",
    "migrate-workspace": "migrate-workspace",
    "校验经营系统": "validate-system",
    "validate business os": "validate-system",
    "validate-system": "validate-system",
    "生成角色 brief": "build-agent-brief",
    "build agent brief": "build-agent-brief",
    "build-agent-brief": "build-agent-brief",
    "生成正式交付文档": "generate-artifact-document",
    "generate formal deliverable document": "generate-artifact-document",
    "generate-artifact-document": "generate-artifact-document",
    "保存检查点": "save-checkpoint",
    "save checkpoint": "save-checkpoint",
    "save-checkpoint": "save-checkpoint",
    "检查 One Person Company OS 的运行环境与保存状态。": "preflight-check",
    "运行环境检查": "preflight-check",
    "runtime preflight check": "preflight-check",
    "preflight-check": "preflight-check",
    "python 兼容恢复": "python-runtime",
    "python runtime recovery": "python-runtime",
    "python-runtime": "python-runtime",
}

PERSISTENCE_MODE_LABELS = {
    "script-execution": {"zh-CN": "模式 A：脚本执行", "en-US": "Mode A: Script Execution"},
    "script-execution-switch-python": {
        "zh-CN": "模式 A：脚本执行（切换兼容 Python）",
        "en-US": "Mode A: Script Execution (Switch To Compatible Python)",
    },
    "manual-persistence": {"zh-CN": "模式 B：手动落盘", "en-US": "Mode B: Manual Persistence"},
    "chat-only": {"zh-CN": "模式 C：纯对话推进", "en-US": "Mode C: Chat-Only Progression"},
}

PERSISTENCE_MODE_ALIASES = {
    "模式 a：脚本执行": "script-execution",
    "mode a: script execution": "script-execution",
    "模式 a：脚本执行（切换兼容 python）": "script-execution-switch-python",
    "mode a: script execution (switch to compatible python)": "script-execution-switch-python",
    "模式 b：手动落盘": "manual-persistence",
    "mode b: manual persistence": "manual-persistence",
    "模式 c：纯对话推进": "chat-only",
    "mode c: chat-only progression": "chat-only",
}

ROUND_STATUS_LABELS = {
    "undefined": {"zh-CN": "待定义", "en-US": "Undefined"},
    "planned": {"zh-CN": "已拆解", "en-US": "Planned"},
    "in-progress": {"zh-CN": "执行中", "en-US": "In Progress"},
    "needs-calibration": {"zh-CN": "待校准", "en-US": "Needs Calibration"},
    "needs-decision": {"zh-CN": "待决策", "en-US": "Needs Founder Decision"},
    "completed": {"zh-CN": "已完成", "en-US": "Completed"},
}

ROUND_STATUS_ALIASES = {
    "待定义": "undefined",
    "undefined": "undefined",
    "已拆解": "planned",
    "planned": "planned",
    "执行中": "in-progress",
    "in progress": "in-progress",
    "待校准": "needs-calibration",
    "needs calibration": "needs-calibration",
    "待决策": "needs-decision",
    "needs founder decision": "needs-decision",
    "已完成": "completed",
    "completed": "completed",
}

STAGE_ALIASES = {
    "validate": "validate",
    "validation": "validate",
    "验证": "validate",
    "验证期": "validate",
    "build": "build",
    "构建": "build",
    "构建期": "build",
    "launch": "launch",
    "上线": "launch",
    "上线期": "launch",
    "operate": "operate",
    "运营": "operate",
    "运营期": "operate",
    "grow": "grow",
    "增长": "grow",
    "增长期": "grow",
}

STAGE_CONFIG = {
    "validate": {
        "label": {"zh-CN": "验证期", "en-US": "Validation"},
        "goal": {
            "zh-CN": "快速确认尖锐问题、目标用户和真实需求或付费信号。",
            "en-US": "Quickly confirm the sharp problem, target user, and real demand or willingness-to-pay signals.",
        },
        "exit_criteria": {
            "zh-CN": "拿到足够真实的用户证据，能明确首个最小可卖或可测方案。",
            "en-US": "Collect enough real user evidence to define the first minimum sellable or testable offer.",
        },
        "next_requirements": {
            "zh-CN": "用户、问题、价值主张和首个 MVP 范围都已收敛。",
            "en-US": "The user, problem, value proposition, and first MVP scope are all narrowed enough.",
        },
        "risks": {
            "zh-CN": ["把想象当用户证据", "研究太久还不动手", "问题范围太散"],
            "en-US": ["Treating imagination as user evidence", "Researching too long without shipping", "Keeping the problem space too broad"],
        },
    },
    "build": {
        "label": {"zh-CN": "构建期", "en-US": "Build"},
        "goal": {
            "zh-CN": "用最小成本做出可上线的 MVP，并跑通一个核心价值闭环。",
            "en-US": "Build the smallest launchable MVP and make one core value loop work end to end.",
        },
        "exit_criteria": {
            "zh-CN": "关键流程端到端可用，具备基础质量和最小上线条件。",
            "en-US": "The key path works end to end with a basic quality bar and minimum launch readiness.",
        },
        "next_requirements": {
            "zh-CN": "MVP 范围锁定、关键功能可用、验收与上线边界清晰。",
            "en-US": "Keep the MVP scope locked, the critical functionality usable, and acceptance plus launch boundaries clear.",
        },
        "risks": {
            "zh-CN": ["把 MVP 做成大而全产品", "技术实现脱离真实需求", "没有测试和验收证据"],
            "en-US": ["Turning the MVP into a full product too early", "Building detached from real demand", "Missing testing and acceptance evidence"],
        },
    },
    "launch": {
        "label": {"zh-CN": "上线期", "en-US": "Launch"},
        "goal": {
            "zh-CN": "把 MVP 快速推到一小批目标用户面前，并建立反馈闭环。",
            "en-US": "Put the MVP in front of a narrow set of target users quickly and establish a feedback loop.",
        },
        "exit_criteria": {
            "zh-CN": "真实用户已可访问，反馈、支持、部署和回滚路径都已跑通。",
            "en-US": "Real users can access the product, with feedback, support, deployment, and rollback paths all working.",
        },
        "next_requirements": {
            "zh-CN": "上线链路稳定、反馈可回收、关键问题和生产风险都有处理路径。",
            "en-US": "The launch path is stable, feedback is recoverable, and critical issues plus production risks have handling paths.",
        },
        "risks": {
            "zh-CN": ["信息不一致", "没有回滚就上线", "一开始铺太多渠道"],
            "en-US": ["Inconsistent messaging", "Launching without rollback", "Spreading across too many channels too early"],
        },
    },
    "operate": {
        "label": {"zh-CN": "运营期", "en-US": "Operate"},
        "goal": {
            "zh-CN": "围绕真实使用持续修产品，并保持反馈处理和生产稳定。",
            "en-US": "Improve the product around real usage while keeping feedback handling and production stability healthy.",
        },
        "exit_criteria": {
            "zh-CN": "问题处理、反馈回收和优先级判断进入稳定节奏。",
            "en-US": "Issue handling, feedback capture, and prioritization have settled into a stable rhythm.",
        },
        "next_requirements": {
            "zh-CN": "留存、稳定性和优化方向已有足够数据支撑。",
            "en-US": "Retention, stability, and optimization direction are now supported by enough data.",
        },
        "risks": {
            "zh-CN": ["问题积压", "只修小问题不修价值交付", "有数据但没有判断"],
            "en-US": ["Issue backlog growth", "Fixing only surface issues instead of value delivery", "Having data without judgment"],
        },
    },
    "grow": {
        "label": {"zh-CN": "增长期", "en-US": "Grow"},
        "goal": {
            "zh-CN": "在价值和留存被验证后，放大有效渠道、转化和收益模型。",
            "en-US": "Scale effective channels, conversion paths, and revenue models only after value and retention are proven.",
        },
        "exit_criteria": {
            "zh-CN": "已经找到可重复的增长动作，并能判断投入产出。",
            "en-US": "Find repeatable growth actions and develop a grounded view of return on effort and spend.",
        },
        "next_requirements": {
            "zh-CN": "实验机制可持续，现金流和产品稳定边界清晰。",
            "en-US": "Keep experimentation sustainable with clear cash-flow and product-stability boundaries.",
        },
        "risks": {
            "zh-CN": ["产品价值未稳就放大流量", "把噪音当增长", "忽视现金流和交付承载能力"],
            "en-US": ["Scaling traffic before the product value is stable", "Mistaking noise for growth", "Ignoring cash flow and delivery capacity"],
        },
    },
}

STAGE_REQUIRED_OUTPUTS = {
    "validate": {
        "zh-CN": [
            "必须留下真实用户问题证据、访谈纪要、预约或付费信号等验证材料。",
            "至少形成一份可继续复用的正式交付文档，而不是只有聊天摘要。",
        ],
        "en-US": [
            "Leave real validation evidence such as user-problem proof, interview notes, and payment or waitlist signals.",
            "Produce at least one formal deliverable document that can be reused downstream, not just a chat summary.",
        ],
    },
    "build": {
        "zh-CN": [
            "实际软件或实际非软件交付物必须至少有一项真实落盘。",
            "如果做软件，必须能看到代码、配置、脚本、接口或自动化资产中的至少一类产出。",
            "如果做非软件产品，必须能看到服务方案、培训材料、研究成果、销售资料或执行清单中的至少一类产出。",
            "必须同步保留测试或验收记录。",
        ],
        "en-US": [
            "At least one real software or non-software deliverable must be persisted.",
            "For software work, leave real code, configuration, scripts, interfaces, or automation assets.",
            "For non-software work, leave real service plans, training material, research output, sales collateral, or execution checklists.",
            "Keep test or acceptance records alongside the deliverable.",
        ],
    },
    "launch": {
        "zh-CN": [
            "必须同时看到对外可交付物和上线资料，不能只有发布文案。",
            "必须包含部署清单、回滚方案、生产观测/告警安排。",
            "必须包含上线公告、反馈回收路径和首轮支持安排，且优先小范围上线。",
        ],
        "en-US": [
            "Include both user-facing deliverables and launch materials, not just launch copy.",
            "Include deployment checklists, rollback plans, and production observability or alerting arrangements.",
            "Include launch announcement material, feedback collection paths, and first-line support plans, with a narrow launch first.",
        ],
    },
    "operate": {
        "zh-CN": [
            "必须持续更新生产运行资料、事故复盘和用户反馈处理记录。",
            "部署与生产类资料不能在产品上线后消失，必须继续维护，并支撑快速迭代判断。",
        ],
        "en-US": [
            "Keep production runbooks, incident reviews, and user-feedback handling records continuously updated.",
            "Deployment and production materials must remain maintained after launch and support fast iteration decisions.",
        ],
    },
    "grow": {
        "zh-CN": [
            "必须把增长实验、收入/成本复盘和运行稳定性资料一起保留。",
            "增长动作不能脱离真实交付、留存反馈和生产运行状态单独存在。",
        ],
        "en-US": [
            "Keep growth experiments, revenue or cost reviews, and runtime stability materials together.",
            "Growth work cannot exist independently from real deliverables, retention feedback, and production reality.",
        ],
    },
}

ROLE_LOCALIZATION = {
    "en-US": {
        "control-tower": {
            "display_name": "Control Tower",
            "workspace_filename": "control-tower",
            "mission": "Maintain the current primary goal, bottleneck, operating arena, role switching, and shortest next move so the company keeps advancing through the business loop.",
            "owns": ["Primary-goal definition", "Operating-state maintenance", "Role activation and switching", "Trigger evaluation", "Primary-arena adjustment recommendations"],
            "inputs_required": ["Founder objective", "Current operating state", "Previous operating-push context", "Critical feedback or artifact"],
            "outputs_required": ["Operating-focus updates", "Role-assignment recommendations", "Calibration recommendations", "Primary-arena adjustment recommendations", "Shortest next move"],
            "do_not_do": ["Do not make strategic calls for the founder", "Do not advance multiple primary arenas at once", "Do not make the next action too big or too vague"],
            "approval_required_for": ["Company-direction changes", "New budget commitments", "High-risk external actions"],
        },
        "customer-success": {
            "display_name": "Customer Success",
            "workspace_filename": "customer-success",
            "mission": "Maintain feedback loops, onboarding quality, and continued-usage signals.",
            "owns": ["User onboarding", "Issue follow-up", "Feedback synthesis", "Retention signals"],
            "inputs_required": ["User feedback", "Current product status", "Common issues", "Growth and support context"],
            "outputs_required": ["Feedback summary", "Feedback collection checklist", "Onboarding recommendations", "Issue severity triage", "Retention risk notes"],
            "do_not_do": ["Do not promise product capabilities without approval", "Do not ignore repeated user issues"],
            "approval_required_for": ["Large-scale customer outreach", "Compensation or refund policy changes"],
        },
        "data-analyst": {
            "display_name": "Data Analyst",
            "workspace_filename": "data-analyst",
            "mission": "Turn behavioral data and outcome signals into actionable judgment.",
            "owns": ["Metric definition", "Data interpretation", "Anomaly assessment", "Decision support"],
            "inputs_required": ["Tracking data", "Business goals", "Growth or operations results", "Historical comparison"],
            "outputs_required": ["Key-metrics summary", "Anomaly explanation", "Action recommendations"],
            "do_not_do": ["Do not confuse noise with conclusions", "Do not report numbers without interpretation"],
            "approval_required_for": ["Core metric-definition changes"],
        },
        "designer": {
            "display_name": "Design Lead",
            "workspace_filename": "design-lead",
            "mission": "Turn product goals into clear information architecture, interaction design, and visual expression.",
            "owns": ["Information architecture", "Interaction design", "Interface expression", "Brand consistency"],
            "inputs_required": ["Product goals", "Current critical artifact", "Target-user context", "Brand constraints"],
            "outputs_required": ["Page structure", "Key-interface notes", "Copy and visual recommendations"],
            "do_not_do": ["Do not optimize for looks while ignoring conversion", "Do not make large changes detached from the current primary goal"],
            "approval_required_for": ["Brand-direction resets", "Core user-path changes"],
        },
        "devops-sre": {
            "display_name": "DevOps / SRE",
            "workspace_filename": "devops-sre",
            "mission": "Keep infrastructure, deployment, observability, and incident-response boundaries clear.",
            "owns": ["Environment readiness", "Deployment path", "Monitoring and alerting", "Production risk boundaries"],
            "inputs_required": ["Launch goal", "System architecture", "Critical dependencies", "Quality-risk notes"],
            "outputs_required": ["Deployment checklist", "Rollback plan", "Observability recommendations", "Stability-risk notes"],
            "do_not_do": ["Do not push high-risk launches without rollback readiness", "Do not ignore critical monitoring"],
            "approval_required_for": ["Production changes", "New infrastructure budget"],
        },
        "engineer-tech-lead": {
            "display_name": "Engineering Lead",
            "workspace_filename": "engineering-lead",
            "mission": "Turn product judgment into a deliverable implementation path, technical plan, and execution cadence.",
            "owns": ["Technical solution", "Implementation order", "Delivery feasibility", "Technical risk"],
            "inputs_required": ["Current primary goal", "Requirement scope", "Existing code context", "Launch constraints"],
            "outputs_required": ["Code-change checklist", "Runnable implementation or scripts", "Implementation plan", "Technical breakdown", "Risk notes", "Critical delivery path"],
            "do_not_do": ["Do not promise unrealistic delivery dates", "Do not hide technical risk", "Do not skip minimum acceptance criteria"],
            "approval_required_for": ["Major stack changes", "New infrastructure cost", "Shortcuts that may impact production stability"],
        },
        "finance": {
            "display_name": "Finance",
            "workspace_filename": "finance",
            "mission": "Maintain basic health across cash flow, pricing, and return-on-effort judgment.",
            "owns": ["Cash-flow assessment", "Pricing sanity checks", "Revenue and cost watchpoints"],
            "inputs_required": ["Revenue data", "Cost data", "Growth targets", "Pricing plan"],
            "outputs_required": ["Financial alerts", "Pricing-risk notes", "Return-on-effort judgment"],
            "do_not_do": ["Do not treat unvalidated revenue assumptions as facts"],
            "approval_required_for": ["New budget", "Core pricing changes"],
        },
        "founder-ceo": {
            "display_name": "Founder",
            "workspace_filename": "founder",
            "mission": "Set direction, priorities, budget, and risk boundaries, and give final approval on high-impact actions.",
            "owns": ["Direction setting", "Priority decisions", "Budget boundaries", "Risk boundaries", "Final approval"],
            "inputs_required": ["Current operating state", "Calibration findings", "Critical risks", "Critical artifact summary"],
            "outputs_required": ["Decision outcome", "Priority changes", "Primary-arena approval", "Budget and risk authorization"],
            "do_not_do": ["Do not mistake vague preference for strategy", "Do not force a decision without key facts"],
            "approval_required_for": ["Launches", "Pricing changes", "Spending money", "Large customer-facing actions", "Compliance and legal claims"],
        },
        "growth-sales": {
            "display_name": "Growth Lead",
            "workspace_filename": "growth-lead",
            "mission": "Bring the product to target users and build loops across traffic, conversion, and feedback.",
            "owns": ["Distribution paths", "Acquisition actions", "Conversion copy", "Feedback collection"],
            "inputs_required": ["Product positioning", "Target user", "Current primary goal", "Available channels"],
            "outputs_required": ["Channel-action checklist", "Launch announcement or sales collateral", "Conversion copy", "Feedback logs", "Growth-experiment recommendations"],
            "do_not_do": ["Do not spread across too many channels at once", "Do not trade away target-user accuracy for traffic"],
            "approval_required_for": ["Advertising budget", "Public-facing campaigns", "Core pricing-message changes"],
        },
        "legal-compliance": {
            "display_name": "Legal / Compliance",
            "workspace_filename": "legal-compliance",
            "mission": "Identify high-risk legal, compliance, and external-communication boundaries.",
            "owns": ["Risk-boundary alerts", "Sensitive wording review", "Compliance notes"],
            "inputs_required": ["External-facing copy", "Pricing and terms details", "Customer promises", "Business context"],
            "outputs_required": ["Risk alerts", "Items needing confirmation", "Sensitive-language revision recommendations"],
            "do_not_do": ["Do not present draft suggestions as formal legal advice"],
            "approval_required_for": ["Legal commitments", "Compliance statements", "Terms changes"],
        },
        "product-strategist": {
            "display_name": "Product Strategist",
            "workspace_filename": "product-strategist",
            "mission": "Turn user problems and business goals into clear product judgment, scope, and artifacts.",
            "owns": ["Problem definition", "Target-user clarification", "Scope narrowing", "Product tradeoffs", "Critical artifact definition"],
            "inputs_required": ["Founder objective", "User feedback", "Market signals", "Engineering constraints"],
            "outputs_required": ["Product positioning", "Product-push goal definition", "Requirement scope", "Critical artifact notes"],
            "do_not_do": ["Do not turn every idea into scope", "Do not fabricate user evidence", "Do not hide product tradeoffs"],
            "approval_required_for": ["Large-scope changes", "Core target-user changes", "Core value-proposition changes"],
        },
        "qa-reliability": {
            "display_name": "QA / Reliability",
            "workspace_filename": "qa-reliability",
            "mission": "Ensure the current critical artifact reaches a minimum verifiable quality bar and has clear risk boundaries.",
            "owns": ["Acceptance criteria", "Testing focus", "Regression risk", "Pre-launch quality judgment"],
            "inputs_required": ["Current primary goal", "Implementation notes", "Critical path", "Existing issue log"],
            "outputs_required": ["Acceptance checklist", "Test record", "Testing recommendations", "Quality-risk notes"],
            "do_not_do": ["Do not bury quality issues in footnotes", "Do not skip critical-path testing"],
            "approval_required_for": ["Launching with known high-risk conditions"],
        },
    }
}

EN_TEMPLATE_OVERRIDES = {
    "artifact-delivery-index-template.md": """# {{ARTIFACT_TITLE}}

Updated At: {{UPDATED_AT}}

- Company: {{COMPANY_NAME}}
- Product: {{PRODUCT_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Operating Surface: {{CURRENT_ROUND_NAME}}
- Status: {{ARTIFACT_STATUS}}
- File Path: {{ARTIFACT_FILE_PATH}}

## Progress Summary

- {{ARTIFACT_PROGRESS_SUMMARY}}

## Required Outputs For This Business Loop

{{CURRENT_STAGE_REQUIRED_OUTPUTS}}

## Registry Rules

- Formal deliverables use a two-digit numbered `.docx` file name.
- File names use the final deliverable name directly instead of carrying status markers.
- Do not mark a deliverable complete without a file path, repository link, demo link, or acceptance evidence.

## Suggested Registry Fields

- Deliverable ID
- Deliverable Name
- Deliverable Type
- File Path Or Link
- Owner
- Status
- Acceptance Result

## Current Gaps

{{ARTIFACT_MISSING_ITEMS}}

## Next Action

- {{ARTIFACT_NEXT_ACTION}}
""",
    "artifact-deployment-template.md": """# {{ARTIFACT_TITLE}}

Updated At: {{UPDATED_AT}}

- Company: {{COMPANY_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Operating Surface: {{CURRENT_ROUND_NAME}}
- Owner: {{ARTIFACT_OWNER}}

## Deployment Objective

- Objective: {{ARTIFACT_OBJECTIVE}}
- Summary: {{ARTIFACT_SUMMARY}}

## Deployment Checklist

{{ARTIFACT_DEPLOYMENT_ITEMS}}

## Evidence

{{ARTIFACT_EVIDENCE}}

## Risks And Confirmations

{{ARTIFACT_RISKS}}

## Next Action

- {{ARTIFACT_NEXT_ACTION}}
""",
    "artifact-docx-ready-template.md": """# {{ARTIFACT_TITLE}}

Updated At: {{UPDATED_AT}}

## Context

- Company: {{COMPANY_NAME}}
- Product: {{PRODUCT_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Operating Surface: {{CURRENT_ROUND_NAME}}
- Operating Goal: {{ROUND_GOAL}}
- Operating Status: {{ROUND_STATUS}}
- Artifact Type: {{ARTIFACT_TYPE}}
- Owner: {{ARTIFACT_OWNER}}
- Document Maturity: {{ARTIFACT_STATUS}}
- File Path: {{ARTIFACT_FILE_PATH}}

## Progress Summary

- {{ARTIFACT_PROGRESS_SUMMARY}}

## Missing Items

{{ARTIFACT_MISSING_ITEMS}}

## Objective

- {{ARTIFACT_OBJECTIVE}}

## Summary

- {{ARTIFACT_SUMMARY}}

## In Scope

{{ARTIFACT_SCOPE_IN}}

## Out Of Scope

{{ARTIFACT_SCOPE_OUT}}

## Deliverables

{{ARTIFACT_DELIVERABLES}}

## Software Outputs

{{ARTIFACT_SOFTWARE_OUTPUTS}}

## Non-Software Outputs

{{ARTIFACT_NON_SOFTWARE_OUTPUTS}}

## Evidence And Acceptance Paths

{{ARTIFACT_EVIDENCE}}

## Deployment Materials

{{ARTIFACT_DEPLOYMENT_ITEMS}}

## Production Materials

{{ARTIFACT_PRODUCTION_ITEMS}}

## Changes This Run

{{ARTIFACT_CHANGES}}

## Key Decisions

{{ARTIFACT_DECISIONS}}

## Risks And Confirmations

{{ARTIFACT_RISKS}}

## Next Action

- {{ARTIFACT_NEXT_ACTION}}
""",
    "artifact-growth-template.md": """# {{ARTIFACT_TITLE}}

Updated At: {{UPDATED_AT}}

- Company: {{COMPANY_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Operating Surface: {{CURRENT_ROUND_NAME}}
- Owner: {{ARTIFACT_OWNER}}

## Growth Objective

- Objective: {{ARTIFACT_OBJECTIVE}}
- Summary: {{ARTIFACT_SUMMARY}}

## Growth Deliverables

{{ARTIFACT_DELIVERABLES}}

## Evidence

{{ARTIFACT_EVIDENCE}}

## Changes And Decisions

{{ARTIFACT_CHANGES}}

{{ARTIFACT_DECISIONS}}

## Next Action

- {{ARTIFACT_NEXT_ACTION}}
""",
    "artifact-internal-draft-template.md": """# {{ARTIFACT_TITLE}}

Updated At: {{UPDATED_AT}}

- Company: {{COMPANY_NAME}}
- Product: {{PRODUCT_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Operating Surface: {{CURRENT_ROUND_NAME}}
- Owner: {{ARTIFACT_OWNER}}

## Draft Objective

- {{ARTIFACT_OBJECTIVE}}

## Draft Summary

- {{ARTIFACT_SUMMARY}}

## In Scope

{{ARTIFACT_SCOPE_IN}}

## Out Of Scope

{{ARTIFACT_SCOPE_OUT}}

## Proposed Deliverables

{{ARTIFACT_DELIVERABLES}}

## Risks

{{ARTIFACT_RISKS}}

## Next Action

- {{ARTIFACT_NEXT_ACTION}}
""",
    "artifact-launch-feedback-template.md": """# {{ARTIFACT_TITLE}}

Updated At: {{UPDATED_AT}}

- Company: {{COMPANY_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Operating Surface: {{CURRENT_ROUND_NAME}}
- Owner: {{ARTIFACT_OWNER}}

## Launch And Feedback Objective

- Objective: {{ARTIFACT_OBJECTIVE}}
- Summary: {{ARTIFACT_SUMMARY}}

## Launch Deliverables

{{ARTIFACT_DELIVERABLES}}

## Feedback Paths

{{ARTIFACT_EVIDENCE}}

## Decisions And Risks

{{ARTIFACT_DECISIONS}}

{{ARTIFACT_RISKS}}

## Next Action

- {{ARTIFACT_NEXT_ACTION}}
""",
    "artifact-non-software-delivery-template.md": """# {{ARTIFACT_TITLE}}

Updated At: {{UPDATED_AT}}

- Company: {{COMPANY_NAME}}
- Product: {{PRODUCT_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Operating Surface: {{CURRENT_ROUND_NAME}}
- Owner: {{ARTIFACT_OWNER}}
- Status: {{ARTIFACT_STATUS}}
- File Path: {{ARTIFACT_FILE_PATH}}

## Progress Summary

- {{ARTIFACT_PROGRESS_SUMMARY}}

## Objective

- {{ARTIFACT_OBJECTIVE}}

## Non-Software Outputs

{{ARTIFACT_NON_SOFTWARE_OUTPUTS}}

## Deliverables

{{ARTIFACT_DELIVERABLES}}

## Evidence

{{ARTIFACT_EVIDENCE}}

## Changes And Decisions

{{ARTIFACT_CHANGES}}

{{ARTIFACT_DECISIONS}}

## Missing Items

{{ARTIFACT_MISSING_ITEMS}}

## Next Action

- {{ARTIFACT_NEXT_ACTION}}
""",
    "artifact-output-guide-template.md": """# Deliverable Map

Updated At: {{UPDATED_AT}}

## Output Contract

- Formal deliverables under `产物/` should be numbered `.docx` files.
- Software work must leave real code, configuration, scripts, interfaces, or automation evidence.
- Non-software work must leave real deliverables instead of chat-only summaries.
- Launch and post-launch work must include deployment and production materials.

## Business-Loop Requirement

- Operating Model: {{STAGE_LABEL}}
- Required Outputs For This Business Loop:

{{CURRENT_STAGE_REQUIRED_OUTPUTS}}

## Directory Intent

- `01-实际交付`: delivery indexes and primary deliverables for the current operating action
- `02-软件与代码`: code, functionality, quality, and test deliverables
- `03-非软件与业务`: research, services, sales, training, and other non-software outputs
- `04-部署与生产`: deployment, rollback, production, and incident materials
- `05-上线与增长`: launch collateral, feedback loops, and growth experiments

## Rules

- Each artifact must include owner, objective, real outputs, evidence, risks, and the next action.
- Do not count chat-only output as a completed deliverable.
- When the operating focus changes, refresh the default artifact pack before continuing the next action.
""",
    "artifact-production-template.md": """# {{ARTIFACT_TITLE}}

Updated At: {{UPDATED_AT}}

- Company: {{COMPANY_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Operating Surface: {{CURRENT_ROUND_NAME}}
- Owner: {{ARTIFACT_OWNER}}
- Status: {{ARTIFACT_STATUS}}
- File Path: {{ARTIFACT_FILE_PATH}}

## Production Objective

- Objective: {{ARTIFACT_OBJECTIVE}}
- Summary: {{ARTIFACT_SUMMARY}}

## Progress Summary

- {{ARTIFACT_PROGRESS_SUMMARY}}

## Production Checklist

{{ARTIFACT_PRODUCTION_ITEMS}}

## Evidence

{{ARTIFACT_EVIDENCE}}

## Risks And Confirmations

{{ARTIFACT_RISKS}}

## Missing Items

{{ARTIFACT_MISSING_ITEMS}}

## Next Action

- {{ARTIFACT_NEXT_ACTION}}
""",
    "artifact-quality-template.md": """# {{ARTIFACT_TITLE}}

Updated At: {{UPDATED_AT}}

- Company: {{COMPANY_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Operating Surface: {{CURRENT_ROUND_NAME}}
- Owner: {{ARTIFACT_OWNER}}
- Status: {{ARTIFACT_STATUS}}
- File Path: {{ARTIFACT_FILE_PATH}}

## Quality Objective

- Objective: {{ARTIFACT_OBJECTIVE}}
- Summary: {{ARTIFACT_SUMMARY}}

## Progress Summary

- {{ARTIFACT_PROGRESS_SUMMARY}}

## Deliverables

{{ARTIFACT_DELIVERABLES}}

## Evidence

{{ARTIFACT_EVIDENCE}}

## Risks

{{ARTIFACT_RISKS}}

## Missing Items

{{ARTIFACT_MISSING_ITEMS}}

## Next Action

- {{ARTIFACT_NEXT_ACTION}}
""",
    "artifact-software-delivery-template.md": """# {{ARTIFACT_TITLE}}

Updated At: {{UPDATED_AT}}

- Company: {{COMPANY_NAME}}
- Product: {{PRODUCT_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Operating Surface: {{CURRENT_ROUND_NAME}}
- Owner: {{ARTIFACT_OWNER}}
- Status: {{ARTIFACT_STATUS}}
- File Path: {{ARTIFACT_FILE_PATH}}

## Progress Summary

- {{ARTIFACT_PROGRESS_SUMMARY}}

## Objective

- {{ARTIFACT_OBJECTIVE}}

## Software Outputs

{{ARTIFACT_SOFTWARE_OUTPUTS}}

## Deliverables

{{ARTIFACT_DELIVERABLES}}

## Evidence

{{ARTIFACT_EVIDENCE}}

## Missing Items

{{ARTIFACT_MISSING_ITEMS}}

## Next Action

- {{ARTIFACT_NEXT_ACTION}}
""",
    "artifact-standard-spec-template.md": """# {{ARTIFACT_TITLE}}

Updated At: {{UPDATED_AT}}

- Company: {{COMPANY_NAME}}
- Product: {{PRODUCT_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Operating Surface: {{CURRENT_ROUND_NAME}}
- Owner: {{ARTIFACT_OWNER}}

## Objective

- {{ARTIFACT_OBJECTIVE}}

## Scope

{{ARTIFACT_SCOPE_IN}}

## Out Of Scope

{{ARTIFACT_SCOPE_OUT}}

## Deliverables

{{ARTIFACT_DELIVERABLES}}

## Risks

{{ARTIFACT_RISKS}}

## Next Action

- {{ARTIFACT_NEXT_ACTION}}
""",
    "artifact-validate-evidence-template.md": """# {{ARTIFACT_TITLE}}

Updated At: {{UPDATED_AT}}

- Company: {{COMPANY_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Operating Surface: {{CURRENT_ROUND_NAME}}
- Owner: {{ARTIFACT_OWNER}}

## Validation Objective

- Objective: {{ARTIFACT_OBJECTIVE}}
- Summary: {{ARTIFACT_SUMMARY}}

## Evidence Pack

{{ARTIFACT_EVIDENCE}}

## Deliverables

{{ARTIFACT_DELIVERABLES}}

## Next Action

- {{ARTIFACT_NEXT_ACTION}}
""",
    "bootstrap-flow-template.md": """# Company Creation Flow

1. Ask for the founder idea in one sentence, or let the founder pick a direction
2. Turn that lightweight input into a proposed company direction, current bottleneck, and shortest action today
3. Keep the reply burden low and the output easy to scan
4. Wait for founder approval
5. Create the standardized workspace and the first set of final-named deliverable documents
6. Generate the starter role set and enter the operating cockpit
""",
    "calibration-flow-template.md": """# Calibration Flow

1. Record the trigger and current blocker
2. Identify the practical finding
3. Narrow the next shortest action
4. Confirm whether founder approval is required
5. Write the calibration record back into the workspace
""",
    "calibration-rules-template.md": """# Calibration Rules

Updated At: {{UPDATED_AT}}

## When To Calibrate

- When the current operating action stalls around the same blocker for too long
- When the current owner no longer fits the operating action
- When new evidence invalidates the previous assumption
- When a key artifact is completed and the next move should be re-scoped
- Before launch, pricing, customer-facing, or other high-risk actions

## Calibration Output

- Trigger reason
- Finding
- Adjusted owner
- Shortest next action
- Whether founder approval is required
""",
    "company-overview-template.md": """# {{COMPANY_NAME}} Company Overview

Updated At: {{UPDATED_AT}}

- Product Name: {{PRODUCT_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Current Company Goal: {{COMPANY_GOAL}}
- Current Bottleneck: {{CURRENT_BOTTLENECK}}
- Operating Surface: {{CURRENT_ROUND_NAME}}
- Shortest Next Action: {{CURRENT_NEXT_ACTION}}

## Active Roles

{{ACTIVE_ROLE_LIST}}

## Current Focus

- Keep the visible workflow on promise -> buyer -> product -> delivery -> cash -> learning -> asset
- Use the operating model only to explain the current bottleneck and next action
- Ask the founder for approval on budget, launch, customer-facing, or compliance-sensitive actions

## Quick Paths

- Operating Cockpit: `reading/00-operating-cockpit.html`
- Deliverable Directory Overview: `artifacts/01-delivery/01-actual-deliverables-index.docx`
- Visual Kit: `visual-kit/business-loop.svg`
- Formal Deliverables: `产物/`
""",
    "current-round-template.md": """# Current Operating Push

Updated At: {{UPDATED_AT}}

- Push ID: {{ROUND_ID}}
- Push Name: {{ROUND_NAME}}
- Operating Model: {{STAGE_LABEL}}
- Operating Status: {{ROUND_STATUS}}
- Owner: {{ROUND_OWNER}}
- Push Goal: {{ROUND_GOAL}}
- Key Artifact: {{ROUND_ARTIFACT}}
- Current Blocker: {{ROUND_BLOCKER}}
- Shortest Next Action: {{ROUND_NEXT_ACTION}}
- Success Criteria: {{ROUND_SUCCESS_CRITERIA}}
- Started At: {{ROUND_STARTED_AT}}
- Last Updated At: {{ROUND_UPDATED_AT}}
""",
    "current-stage-deliverable-template.md": """# Current Operating Deliverable Requirements

Updated At: {{UPDATED_AT}}

- Operating Model: {{STAGE_LABEL}}
- Primary Goal: {{STAGE_GOAL}}
- Exit Criteria: {{STAGE_EXIT_CRITERIA}}

## Required Outputs For This Business Loop

{{CURRENT_STAGE_REQUIRED_OUTPUTS}}

## Review Order

- Start from the operating cockpit to confirm the primary goal, bottleneck, and shortest action.
- Read the deliverable directory overview to see which formal DOCX files already exist and which one to improve next.
- Read the current revenue pipeline to confirm product, delivery, and cash are connected in one loop.
- Then complete the matching files under `artifacts/`.

## Risks

{{STAGE_RISKS}}

## Next-Action Readiness

- {{NEXT_STAGE_REQUIREMENTS}}

## Deliverable Rules

- Formal files under `产物/` use numbered `.docx` names.
- File names use the final deliverable name directly instead of carrying status markers.
- Software work must leave real code, scripts, interfaces, config, or automation outputs.
- Non-software work must leave formal business deliverables instead of chat-only summaries.
""",
    "current-stage-template.md": """# Current Operating State

Updated At: {{UPDATED_AT}}

- Operating Model: {{STAGE_LABEL}}
- Primary Goal: {{STAGE_GOAL}}
- Exit Criteria: {{STAGE_EXIT_CRITERIA}}
- Next-Action Requirements: {{NEXT_STAGE_REQUIREMENTS}}

## How To Read This Operating State

- This state marks the current dominant bottleneck, not a heavy bureaucracy phase.
- Keep each key action small enough to move the business loop forward quickly.
- Adjust the primary arena when the bottleneck changes, not because a ceremony says so.
""",
    "execution-rules-template.md": """# Execution Rules

Updated At: {{UPDATED_AT}}

## AI-Era Fast Loop

- Narrow one user pain first
- Validate demand with real evidence
- Ship the smallest useful MVP
- Launch narrowly and capture feedback
- Improve the product before scaling growth

## Core Rules

- Advance only one primary operating arena at a time
- Keep the shortest next action practical and small
- Do not skip founder approval on high-risk actions
- Prefer script execution, then manual persistence, then chat-only progression
- Treat the operating model as a bottleneck label, not as a reason to slow down

## Current Focus

- Operating model: {{STAGE_LABEL}}
- Operating surface: {{CURRENT_ROUND_NAME}}
- Active roles: {{ACTIVE_ROLE_INLINE}}
""",
    "organization-template.md": """# Organization Structure

Updated At: {{UPDATED_AT}}

## Current Active Roles

{{ACTIVE_ROLE_LIST}}

## Available Roles

{{AVAILABLE_ROLE_LIST}}

## Design Notes

- Start with a minimum role set
- Keep one clear primary owner for the current operating arena
- Activate launch, support, and production roles when the company needs launch, delivery, or customer feedback work
""",
    "product-positioning-template.md": """# Product Positioning

Updated At: {{UPDATED_AT}}

- Product Name: {{PRODUCT_NAME}}
- Product Pitch: {{PRODUCT_PITCH}}
- Target User: {{TARGET_USER}}
- Core Problem: {{CORE_PROBLEM}}
- Operating Model: {{STAGE_LABEL}}
- Company Goal: {{COMPANY_GOAL}}

## Current Product Focus

- Solve the sharpest pain first instead of designing the full company at once.
- Use the current bottleneck to narrow the MVP and the next proof point.
""",
    "reminder-rules-template.md": """# Reminder Rules

- Remind the team to update the current operating focus before context is lost
- Trigger calibration when the blocker persists for too long
- Ask for founder approval before risky external actions
""",
    "role-brief-template.md": """# Role Brief: {{ROLE_NAME}}

## Mission

- {{ROLE_MISSION}}

## Owns

{{ROLE_OWNS}}

## Inputs

{{ROLE_INPUTS}}

## Outputs

{{ROLE_OUTPUTS}}

## Guardrails

{{ROLE_GUARDRAILS}}

## Approval Gates

{{ROLE_APPROVALS}}

## Default Handoff Targets

{{ROLE_HANDOFFS}}
""",
    "role-index-template.md": """# Role Index

Updated At: {{UPDATED_AT}}

## Current Active Roles

{{ACTIVE_ROLE_LIST}}

## Notes

- Activate the minimum role set first
- Keep only one primary owner for the current operating arena
- Activate ops and customer roles when launch, delivery, or customer feedback work needs them
- Add other roles when the current bottleneck or trigger signals require them
""",
    "round-flow-template.md": """# Operating Push Flow

1. Define the current primary goal, bottleneck, and owner
2. Clarify the artifact and shortest next action
3. Execute one practical step
4. Update the operating state and blocker
5. Decide whether to finish, calibrate, or continue
""",
    "scheduler-spec-template.md": """# Scheduler Specification

- Operating model: {{STAGE_LABEL}}
- Operating surface: {{CURRENT_ROUND_NAME}}
- Current owner: {{ACTIVE_ROLE_INLINE}}

## Scheduler Intent

- Use reminders to keep the current operating action moving
- Use triggers to enter calibration only when needed
""",
    "stage-flow-template.md": """# Primary Arena Adjustment Flow

1. Confirm whether the current bottleneck has changed
2. Decide whether the next operating action belongs to sales, product, delivery, cash, or assets
3. Refresh the default active roles
4. Define the shortest action for the adjusted arena
5. Update deliverable requirements and artifact packs
""",
    "stage-role-deliverable-matrix-template.md": """# Stage Role And Deliverable Matrix

Updated At: {{UPDATED_AT}}

This matrix describes the current bottleneck state, not a heavy mandatory process.
Use it to understand which roles and outputs matter right now.

## Validation

- Default Roles:

{{VALIDATE_DEFAULT_ROLES}}

- Optional Roles:

{{VALIDATE_OPTIONAL_ROLES}}

- Required Outputs:

{{VALIDATE_REQUIRED_OUTPUTS}}

## Build

- Default Roles:

{{BUILD_DEFAULT_ROLES}}

- Optional Roles:

{{BUILD_OPTIONAL_ROLES}}

- Required Outputs:

{{BUILD_REQUIRED_OUTPUTS}}

## Launch

- Default Roles:

{{LAUNCH_DEFAULT_ROLES}}

- Optional Roles:

{{LAUNCH_OPTIONAL_ROLES}}

- Required Outputs:

{{LAUNCH_REQUIRED_OUTPUTS}}

## Operate

- Default Roles:

{{OPERATE_DEFAULT_ROLES}}

- Optional Roles:

{{OPERATE_OPTIONAL_ROLES}}

- Required Outputs:

{{OPERATE_REQUIRED_OUTPUTS}}

## Grow

- Default Roles:

{{GROW_DEFAULT_ROLES}}

- Optional Roles:

{{GROW_OPTIONAL_ROLES}}

- Required Outputs:

{{GROW_REQUIRED_OUTPUTS}}
""",
}


def resolve_step_id(value: str | int) -> int:
    if isinstance(value, int):
        return value
    key = value.strip().lower()
    return STEP_ALIASES.get(key, STEP_ALIASES.get(value, 0))


def step_meta(step_id: int, language: str) -> dict[str, str]:
    return STEP_CATALOG.get(step_id, {}).get(language, {})


def normalize_mode(value: str, language: str | None = None) -> str:
    key = value.strip().lower()
    resolved = MODE_ALIASES.get(key)
    if resolved:
        return resolved
    if value == "":
        return "create-company"
    return value


def mode_label(value: str, language: str) -> str:
    key = MODE_ALIASES.get(value.strip().lower(), value)
    if key in MODE_LABELS:
        return MODE_LABELS[key][language]
    return value


def normalize_persistence_mode(value: str) -> str:
    return PERSISTENCE_MODE_ALIASES.get(value.strip().lower(), value)


def persistence_mode_label(value: str, language: str) -> str:
    key = normalize_persistence_mode(value)
    if key in PERSISTENCE_MODE_LABELS:
        return PERSISTENCE_MODE_LABELS[key][language]
    return value


def normalize_round_status(value: str) -> str:
    return ROUND_STATUS_ALIASES.get(value.strip().lower(), ROUND_STATUS_ALIASES.get(value, value))


def round_status_label(value: str, language: str) -> str:
    key = normalize_round_status(value)
    if key in ROUND_STATUS_LABELS:
        return ROUND_STATUS_LABELS[key][language]
    return value


def normalize_stage(value: str) -> str:
    key = value.strip().lower()
    if key not in STAGE_ALIASES:
        raise ValueError(f"unknown stage: {value}")
    return STAGE_ALIASES[key]


def stage_label(stage_id: str, language: str) -> str:
    return STAGE_CONFIG[stage_id]["label"][language]


def stage_meta(stage_id: str, language: str) -> dict[str, Any]:
    config = STAGE_CONFIG[stage_id]
    return {
        "label": config["label"][language],
        "goal": config["goal"][language],
        "exit_criteria": config["exit_criteria"][language],
        "next_requirements": config["next_requirements"][language],
        "risks": list(config["risks"][language]),
    }


def stage_required_outputs(stage_id: str, language: str) -> list[str]:
    return list(STAGE_REQUIRED_OUTPUTS[stage_id][language])


def localized_role_spec(spec: dict[str, Any], language: str) -> dict[str, Any]:
    if language != "en-US":
        return spec
    override = ROLE_LOCALIZATION.get(language, {}).get(spec["role_id"], {})
    if not override:
        return spec
    merged = dict(spec)
    merged.update(override)
    return merged


def template_text(template_name: str, template_dir: Path, language: str) -> str:
    if language == "en-US" and template_name in EN_TEMPLATE_OVERRIDES:
        return EN_TEMPLATE_OVERRIDES[template_name]
    return (template_dir / template_name).read_text(encoding="utf-8")
