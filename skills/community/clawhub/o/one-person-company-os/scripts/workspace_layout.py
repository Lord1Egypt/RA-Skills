#!/usr/bin/env python3
"""Workspace path contracts for One Person Company OS."""

from __future__ import annotations

from pathlib import Path

from localization import normalize_language


INTERNAL_STATE_PATH_PARTS = (".opcos", "state", "current-state.json")
LEGACY_STATE_PATH_PARTS = (("自动化", "当前状态.json"),)

ROOT_DOC_KEYS = (
    "dashboard",
    "founder_constraints",
    "offer",
    "pipeline",
    "product_status",
    "delivery_cash",
    "cash_health",
    "assets_automation",
    "risks",
    "week_focus",
    "today_action",
    "collaboration_memory",
    "session_handoff",
)

CORE_WORKSPACE_FILE_KEYS = (
    "dashboard",
    "offer",
    "pipeline",
    "product_status",
    "delivery_cash",
)

USER_FILE_PATHS = {
    "dashboard": {
        "zh-CN": ("00-经营总盘.md",),
        "en-US": ("00-operating-dashboard.md",),
        "legacy": ("00-经营总盘.md",),
    },
    "founder_constraints": {
        "zh-CN": ("01-创始人约束.md",),
        "en-US": ("01-founder-constraints.md",),
        "legacy": ("01-创始人约束.md",),
    },
    "offer": {
        "zh-CN": ("02-价值承诺与报价.md",),
        "en-US": ("02-value-promise-and-pricing.md",),
        "legacy": ("02-价值承诺与报价.md",),
    },
    "pipeline": {
        "zh-CN": ("03-机会与成交管道.md",),
        "en-US": ("03-opportunity-and-revenue-pipeline.md",),
        "legacy": ("03-机会与成交管道.md",),
    },
    "product_status": {
        "zh-CN": ("04-产品与上线状态.md",),
        "en-US": ("04-product-and-launch-status.md",),
        "legacy": ("04-产品与上线状态.md",),
    },
    "delivery_cash": {
        "zh-CN": ("05-客户交付与回款.md",),
        "en-US": ("05-delivery-and-cash-collection.md",),
        "legacy": ("05-客户交付与回款.md",),
    },
    "cash_health": {
        "zh-CN": ("06-现金流与经营健康.md",),
        "en-US": ("06-cashflow-and-business-health.md",),
        "legacy": ("06-现金流与经营健康.md",),
    },
    "assets_automation": {
        "zh-CN": ("07-资产与自动化.md",),
        "en-US": ("07-assets-and-automation.md",),
        "legacy": ("07-资产与自动化.md",),
    },
    "risks": {
        "zh-CN": ("08-风险与关键决策.md",),
        "en-US": ("08-risks-and-key-decisions.md",),
        "legacy": ("08-风险与关键决策.md",),
    },
    "week_focus": {
        "zh-CN": ("09-本周唯一主目标.md",),
        "en-US": ("09-single-weekly-outcome.md",),
        "legacy": ("09-本周唯一主目标.md",),
    },
    "today_action": {
        "zh-CN": ("10-今日最短动作.md",),
        "en-US": ("10-shortest-action-today.md",),
        "legacy": ("10-今日最短动作.md",),
    },
    "collaboration_memory": {
        "zh-CN": ("11-协作记忆.md",),
        "en-US": ("11-collaboration-memory.md",),
        "legacy": ("11-协作记忆.md",),
    },
    "session_handoff": {
        "zh-CN": ("12-会话交接.md",),
        "en-US": ("12-session-handoff.md",),
        "legacy": ("12-会话交接.md",),
    },
    "record_snapshot": {
        "zh-CN": ("记录", "01-当前经营快照.md"),
        "en-US": ("records", "01-current-operating-snapshot.md"),
        "legacy": ("records", "01-当前经营快照.md"),
    },
    "sales_actions": {
        "zh-CN": ("销售", "01-成交动作清单.md"),
        "en-US": ("sales", "01-revenue-action-checklist.md"),
        "legacy": ("sales", "01-成交动作清单.md"),
    },
    "sales_landing": {
        "zh-CN": ("销售", "04-对外落地页文案.md"),
        "en-US": ("sales", "04-landing-page-copy.md"),
        "legacy": ("sales", "04-对外落地页文案.md"),
    },
    "sales_interview": {
        "zh-CN": ("销售", "05-访谈冲刺看板.md"),
        "en-US": ("sales", "05-interview-sprint-board.md"),
        "legacy": ("sales", "05-访谈冲刺看板.md"),
    },
    "sales_trial_application": {
        "zh-CN": ("销售", "06-试用申请问卷.md"),
        "en-US": ("sales", "06-trial-application-form.md"),
        "legacy": ("sales", "06-试用申请问卷.md"),
    },
    "product_checklist": {
        "zh-CN": ("产品", "01-MVP与上线清单.md"),
        "en-US": ("product", "01-mvp-and-launch-checklist.md"),
        "legacy": ("product", "01-MVP与上线清单.md"),
    },
    "product_demo_index": {
        "zh-CN": ("产品", "演示", "index.html"),
        "en-US": ("product", "demo", "index.html"),
        "legacy": ("product", "demo", "index.html"),
    },
    "delivery_tracker": {
        "zh-CN": ("交付", "01-客户交付追踪.md"),
        "en-US": ("delivery", "01-customer-delivery-tracker.md"),
        "legacy": ("delivery", "01-客户交付追踪.md"),
    },
    "delivery_directory": {
        "zh-CN": ("交付", "02-交付目录总览.md"),
        "en-US": ("delivery", "02-deliverable-directory-overview.md"),
        "legacy": ("delivery", "02-交付目录总览.md"),
    },
    "delivery_feedback": {
        "zh-CN": ("交付", "04-试用反馈回收表.md"),
        "en-US": ("delivery", "04-trial-feedback-capture.md"),
        "legacy": ("delivery", "04-试用反馈回收表.md"),
    },
    "ops_launch_checklist": {
        "zh-CN": ("运营", "01-上线检查清单.md"),
        "en-US": ("operations", "01-launch-checklist.md"),
        "legacy": ("ops", "01-上线检查清单.md"),
    },
    "assets_inventory": {
        "zh-CN": ("资产", "01-资产沉淀清单.md"),
        "en-US": ("assets", "01-asset-inventory.md"),
        "legacy": ("assets", "01-资产沉淀清单.md"),
    },
    "automation_notes": {
        "zh-CN": ("自动化", "01-状态说明.md"),
        "en-US": ("automation", "01-state-notes.md"),
        "legacy": ("automation", "01-状态说明.md"),
    },
    "role_index": {
        "zh-CN": ("角色智能体", "角色清单.md"),
        "en-US": ("roles", "role-index.md"),
        "legacy": ("角色智能体", "角色清单.md"),
    },
    "flow_bootstrap": {
        "zh-CN": ("流程", "创建公司流程.md"),
        "en-US": ("flows", "create-company-flow.md"),
        "legacy": ("流程", "创建公司流程.md"),
    },
    "flow_round": {
        "zh-CN": ("流程", "推进回合流程.md"),
        "en-US": ("flows", "advance-round-flow.md"),
        "legacy": ("流程", "推进回合流程.md"),
    },
    "flow_calibration": {
        "zh-CN": ("流程", "校准回合流程.md"),
        "en-US": ("flows", "calibration-flow.md"),
        "legacy": ("流程", "校准回合流程.md"),
    },
    "flow_stage": {
        "zh-CN": ("流程", "阶段切换流程.md"),
        "en-US": ("flows", "stage-transition-flow.md"),
        "legacy": ("流程", "阶段切换流程.md"),
    },
    "automation_reminders": {
        "zh-CN": ("自动化", "提醒规则.md"),
        "en-US": ("automation", "reminder-rules.md"),
        "legacy": ("自动化", "提醒规则.md"),
    },
    "automation_scheduler": {
        "zh-CN": ("自动化", "定时任务定义.md"),
        "en-US": ("automation", "scheduler-specification.md"),
        "legacy": ("自动化", "定时任务定义.md"),
    },
}

CONTAINER_PATHS = {
    "sales": {
        "zh-CN": ("销售",),
        "en-US": ("sales",),
        "legacy": ("sales",),
    },
    "product": {
        "zh-CN": ("产品",),
        "en-US": ("product",),
        "legacy": ("product",),
    },
    "product_demo": {
        "zh-CN": ("产品", "演示"),
        "en-US": ("product", "demo"),
        "legacy": ("product", "demo"),
    },
    "delivery": {
        "zh-CN": ("交付",),
        "en-US": ("delivery",),
        "legacy": ("delivery",),
    },
    "ops": {
        "zh-CN": ("运营",),
        "en-US": ("operations",),
        "legacy": ("ops",),
    },
    "assets": {
        "zh-CN": ("资产",),
        "en-US": ("assets",),
        "legacy": ("assets",),
    },
    "records": {
        "zh-CN": ("记录",),
        "en-US": ("records",),
        "legacy": ("记录",),
    },
    "records_progress": {
        "zh-CN": ("记录", "推进日志"),
        "en-US": ("records", "progress-log"),
        "legacy": ("记录", "推进日志"),
    },
    "records_decision": {
        "zh-CN": ("记录", "决策记录"),
        "en-US": ("records", "decision-log"),
        "legacy": ("记录", "决策记录"),
    },
    "records_calibration": {
        "zh-CN": ("记录", "校准记录"),
        "en-US": ("records", "calibration-log"),
        "legacy": ("记录", "校准记录"),
    },
    "records_checkpoint": {
        "zh-CN": ("记录", "检查点"),
        "en-US": ("records", "checkpoints"),
        "legacy": ("记录", "检查点"),
    },
    "legacy_root": {
        "zh-CN": ("记录", "历史根目录"),
        "en-US": ("records", "legacy-root"),
        "legacy": ("records", "legacy-root"),
    },
    "roles": {
        "zh-CN": ("角色智能体",),
        "en-US": ("roles",),
        "legacy": ("角色智能体",),
    },
    "flows": {
        "zh-CN": ("流程",),
        "en-US": ("flows",),
        "legacy": ("流程",),
    },
    "automation": {
        "zh-CN": ("自动化",),
        "en-US": ("automation",),
        "legacy": ("自动化",),
    },
    "reading_root": {
        "zh-CN": ("阅读版",),
        "en-US": ("reading",),
        "legacy": ("阅读版",),
    },
    "visual_kit": {
        "zh-CN": ("视觉素材",),
        "en-US": ("visual-kit",),
        "legacy": ("视觉素材",),
    },
    "artifacts_root": {
        "zh-CN": ("产物",),
        "en-US": ("artifacts",),
        "legacy": ("产物",),
    },
    "artifact_delivery": {
        "zh-CN": ("产物", "01-实际交付"),
        "en-US": ("artifacts", "01-delivery"),
        "legacy": ("产物", "01-实际交付"),
    },
    "artifact_software": {
        "zh-CN": ("产物", "02-软件与代码"),
        "en-US": ("artifacts", "02-software-and-code"),
        "legacy": ("产物", "02-软件与代码"),
    },
    "artifact_business": {
        "zh-CN": ("产物", "03-非软件与业务"),
        "en-US": ("artifacts", "03-business-and-service"),
        "legacy": ("产物", "03-非软件与业务"),
    },
    "artifact_ops": {
        "zh-CN": ("产物", "04-部署与生产"),
        "en-US": ("artifacts", "04-deployment-and-production"),
        "legacy": ("产物", "04-部署与生产"),
    },
    "artifact_growth": {
        "zh-CN": ("产物", "05-上线与增长"),
        "en-US": ("artifacts", "05-launch-and-growth"),
        "legacy": ("产物", "05-上线与增长"),
    },
}

READING_START_FILENAMES = {
    "zh-CN": "00-经营驾驶舱.html",
    "en-US": "00-operating-cockpit.html",
    "legacy": "00-经营驾驶舱.html",
}


def _normalized_language(language: str | None) -> str:
    return normalize_language(language)


def user_file_parts(key: str, language: str) -> tuple[str, ...]:
    return USER_FILE_PATHS[key][_normalized_language(language)]


def user_container_parts(key: str, language: str) -> tuple[str, ...]:
    return CONTAINER_PATHS[key][_normalized_language(language)]


def user_file_path(company_dir: Path, key: str, language: str) -> Path:
    return company_dir.joinpath(*user_file_parts(key, language))


def user_container_path(company_dir: Path, key: str, language: str) -> Path:
    return company_dir.joinpath(*user_container_parts(key, language))


def legacy_user_file_path(company_dir: Path, key: str) -> Path:
    return company_dir.joinpath(*USER_FILE_PATHS[key]["legacy"])


def legacy_container_path(company_dir: Path, key: str) -> Path:
    return company_dir.joinpath(*CONTAINER_PATHS[key]["legacy"])


def artifact_category_path(company_dir: Path, category: str, language: str) -> Path:
    return user_container_path(company_dir, f"artifact_{category}", language)


def record_dir_path(company_dir: Path, record_kind: str, language: str) -> Path:
    return user_container_path(company_dir, f"records_{record_kind}", language)


def role_brief_path(company_dir: Path, filename: str, language: str) -> Path:
    return user_container_path(company_dir, "roles", language) / f"{filename}.md"


def state_path(company_dir: Path) -> Path:
    return company_dir.joinpath(*INTERNAL_STATE_PATH_PARTS)


def reading_root_path(company_dir: Path, language: str) -> Path:
    return user_container_path(company_dir, "reading_root", language)


def reading_start_path(company_dir: Path, language: str) -> Path:
    return reading_root_path(company_dir, language) / READING_START_FILENAMES[_normalized_language(language)]


def legacy_state_paths(company_dir: Path) -> list[Path]:
    return [company_dir.joinpath(*parts) for parts in LEGACY_STATE_PATH_PARTS]


def existing_state_path(company_dir: Path) -> Path:
    current = state_path(company_dir)
    if current.is_file():
        return current
    for path in legacy_state_paths(company_dir):
        if path.is_file():
            return path
    return current


def candidate_user_file_paths(company_dir: Path, key: str) -> list[Path]:
    seen: list[Path] = []
    for layout_key in ("zh-CN", "en-US", "legacy"):
        path = company_dir.joinpath(*USER_FILE_PATHS[key][layout_key])
        if path not in seen:
            seen.append(path)
    return seen


def candidate_container_paths(company_dir: Path, key: str) -> list[Path]:
    seen: list[Path] = []
    for layout_key in ("zh-CN", "en-US", "legacy"):
        path = company_dir.joinpath(*CONTAINER_PATHS[key][layout_key])
        if path not in seen:
            seen.append(path)
    return seen
