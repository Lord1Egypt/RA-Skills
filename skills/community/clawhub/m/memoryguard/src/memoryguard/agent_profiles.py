"""v3.1 §3.5 声明式 AgentProfile 加载与校验。

首版 Profile 必须是数据文件，不允许执行脚本。内置四个 Profile：
- Claude Code：CLAUDE.md 项目/用户/目录层级 + .claude/ 配置与会话历史
- Codex：AGENTS.md 目录作用域
- Cursor：.cursor/rules 项目规则 + ~/.cursor/ 全局配置 + GUI-only Memories
- Windsurf：全局/工作区 Rules 位置 + AGENTS.md 规则引擎

安全边界（v3.1 §3.3）：
- 只探测 Profile 声明的固定路径
- 不递归扫描用户主目录
- 候选阶段不读取正文
- 没有 fixture 时只能 detect_only / export_only
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schema_v3 import (
    AgentProfile, AgentInstance, MemorySurface,
    SourceCategory, IngestionPolicy, Ownership, TargetRole,
    TargetCapability, SurfaceStatus,
)


# ---------------------------------------------------------------------------
# 内置 Profile（数据，不执行脚本）
# ---------------------------------------------------------------------------


def _claude_code_profile() -> AgentProfile:
    """Claude Code Profile（v3.1 §14.2 官方文档依据）。

    Claude Code 的本地数据按作用域分三层：
    - 全局/用户级（~/.claude/）：跨项目的用户偏好、会话历史、命令历史
    - 项目级（<workspace>/）：项目指令、项目本地覆盖
    - 目录级（<workspace>/.claude/）：项目本地配置与会话

    官方文档：https://docs.anthropic.com/zh-CN/docs/claude-code/memory
    """
    surfaces = [
        # ---- 项目级 ----
        MemorySurface(
            surface_id="claude_project_md",
            path_template="%WORKSPACE%/CLAUDE.md",
            surface_role="control_surface",
            scope="project", load_order=10,
            loader_evidence="https://docs.anthropic.com/zh-CN/docs/claude-code/memory",
            classification_confidence=0.95,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="claude_project_local_md",
            path_template="%WORKSPACE%/CLAUDE.local.md",
            surface_role="control_surface",
            scope="project", load_order=11,
            loader_evidence="https://docs.anthropic.com/zh-CN/docs/claude-code/memory",
            classification_confidence=0.80,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="claude_project_config",
            path_template="%WORKSPACE%/.claude",
            surface_role="control_surface",
            scope="project", load_order=12,
            loader_evidence="https://docs.anthropic.com/zh-CN/docs/claude-code/memory",
            classification_confidence=0.70,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        # ---- 用户级（~/.claude/）----
        MemorySurface(
            surface_id="claude_user_md",
            path_template="%HOME%/.claude/CLAUDE.md",
            surface_role="control_surface",
            scope="user", load_order=20,
            loader_evidence="https://docs.anthropic.com/zh-CN/docs/claude-code/memory",
            classification_confidence=0.95,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="claude_user_settings",
            path_template="%HOME%/.claude/settings.json",
            surface_role="control_surface",
            scope="user", load_order=21,
            loader_evidence="https://docs.anthropic.com/zh-CN/docs/claude-code/memory",
            classification_confidence=0.90,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="claude_user_projects_history",
            path_template="%HOME%/.claude/projects",
            surface_role="conversation_history",
            scope="user", load_order=22,
            loader_evidence="https://docs.anthropic.com/zh-CN/docs/claude-code/memory",
            classification_confidence=0.85,
            category=SourceCategory.CONVERSATION_HISTORY,
            ingestion_policy=IngestionPolicy.EVIDENCE_ONLY,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="claude_user_todos",
            path_template="%HOME%/.claude/todos",
            surface_role="runtime_evidence",
            scope="user", load_order=23,
            loader_evidence="https://docs.anthropic.com/zh-CN/docs/claude-code/memory",
            classification_confidence=0.70,
            category=SourceCategory.RUNTIME_EVIDENCE,
            ingestion_policy=IngestionPolicy.EVIDENCE_ONLY,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="claude_user_command_history",
            path_template="%HOME%/.claude/history.jsonl",
            surface_role="runtime_evidence",
            scope="user", load_order=24,
            loader_evidence="https://docs.anthropic.com/zh-CN/docs/claude-code/memory",
            classification_confidence=0.70,
            category=SourceCategory.RUNTIME_EVIDENCE,
            ingestion_policy=IngestionPolicy.EVIDENCE_ONLY,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.NONE,
        ),
    ]
    return AgentProfile(
        profile_id="claude-code@profile-1",
        product="claude-code",
        profile_version="1",
        supported_platforms=["windows", "macos", "linux"],
        verified_product_versions=[],  # 首版无真实 fixture
        detection_rules=[],
        surfaces=surfaces,
        target_capability=TargetCapability.EXPORT_ONLY,  # 无 Loader fixture，只能 export
        evidence_urls=["https://docs.anthropic.com/zh-CN/docs/claude-code/memory"],
    )


def _codex_profile() -> AgentProfile:
    """Codex Profile（v3.1 §14.1 官方文档依据）。"""
    surfaces = [
        MemorySurface(
            surface_id="codex_agents_md",
            path_template="%WORKSPACE%/AGENTS.md",
            surface_role="control_surface",
            scope="project", load_order=10,
            loader_evidence="https://openai.com/index/introducing-codex/",
            classification_confidence=0.90,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="codex_parent_agents_md",
            path_template="%WORKSPACE_PARENT%/AGENTS.md",
            surface_role="control_surface",
            scope="project", load_order=5,
            loader_evidence="https://openai.com/index/introducing-codex/",
            classification_confidence=0.70,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
    ]
    return AgentProfile(
        profile_id="codex@profile-1",
        product="codex",
        profile_version="1",
        supported_platforms=["windows", "macos", "linux"],
        verified_product_versions=[],
        detection_rules=[],
        surfaces=surfaces,
        target_capability=TargetCapability.EXPORT_ONLY,
        evidence_urls=["https://openai.com/index/introducing-codex/"],
    )


def _cursor_profile() -> AgentProfile:
    """Cursor Profile（v3.1 §14.3 官方文档依据）。

    官方页面没有给出稳定的本地 Memories 文件路径，只能发现公开项目 Rules。
    但 ~/.cursor/ 目录下有全局配置和插件，可作为控制面发现。
    """
    surfaces = [
        # ---- 项目级 ----
        MemorySurface(
            surface_id="cursor_project_rules",
            path_template="%WORKSPACE%/.cursor/rules",
            surface_role="control_surface",
            scope="project", load_order=10,
            loader_evidence="https://docs.cursor.com/context/rules",
            classification_confidence=0.90,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        # ---- 用户级 ----
        MemorySurface(
            surface_id="cursor_global_config",
            path_template="%HOME%/.cursor",
            surface_role="control_surface",
            scope="user", load_order=20,
            loader_evidence="https://docs.cursor.com/context/rules",
            classification_confidence=0.70,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="cursor_global_skills",
            path_template="%HOME%/.cursor/skills-cursor",
            surface_role="skill_surface",
            scope="user", load_order=21,
            loader_evidence="https://docs.cursor.com/context/rules",
            classification_confidence=0.60,
            category=SourceCategory.SKILL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="cursor_memories_gui_only",
            path_template="gui-only://cursor/settings/memories",
            surface_role="native_memory",
            scope="user", load_order=30,
            loader_evidence="https://docs.cursor.com/en/context/memories",
            classification_confidence=0.30,
            category=SourceCategory.NATIVE_MEMORY,
            ingestion_policy=IngestionPolicy.EXTRACT_CANDIDATES,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
    ]
    return AgentProfile(
        profile_id="cursor@profile-1",
        product="cursor",
        profile_version="1",
        supported_platforms=["windows", "macos", "linux"],
        verified_product_versions=[],
        detection_rules=[],
        surfaces=surfaces,
        target_capability=TargetCapability.EXPORT_ONLY,
        evidence_urls=[
            "https://docs.cursor.com/context/rules",
            "https://docs.cursor.com/en/context/memories",
        ],
    )


def _windsurf_profile() -> AgentProfile:
    """Windsurf Profile（v3.1 §14.4 官方文档依据）。

    Windsurf 全局配置在 ~/.codeium/windsurf/，工作区规则在 .windsurf/rules/。
    """
    surfaces = [
        # ---- 项目级 ----
        MemorySurface(
            surface_id="windsurf_workspace_rules",
            path_template="%WORKSPACE%/.windsurf/rules",
            surface_role="control_surface",
            scope="project", load_order=10,
            loader_evidence="https://docs.windsurf.com/zh/windsurf/cascade/memories",
            classification_confidence=0.85,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="windsurf_agents_md",
            path_template="%WORKSPACE%/AGENTS.md",
            surface_role="control_surface",
            scope="project", load_order=11,
            loader_evidence="https://docs.windsurf.com/zh/windsurf/cascade/memories",
            classification_confidence=0.75,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        # ---- 用户级 ----
        MemorySurface(
            surface_id="windsurf_global_config",
            path_template="%HOME%/.codeium/windsurf",
            surface_role="control_surface",
            scope="user", load_order=20,
            loader_evidence="https://docs.windsurf.com/zh/windsurf/cascade/memories",
            classification_confidence=0.70,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="windsurf_global_memories",
            path_template="%HOME%/.codeium/windsurf/memories",
            surface_role="native_memory",
            scope="user", load_order=21,
            loader_evidence="https://docs.windsurf.com/zh/windsurf/cascade/memories",
            classification_confidence=0.60,
            category=SourceCategory.NATIVE_MEMORY,
            ingestion_policy=IngestionPolicy.EXTRACT_CANDIDATES,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.TAKEOVER_INPUT,
        ),
    ]
    return AgentProfile(
        profile_id="windsurf@profile-1",
        product="windsurf",
        profile_version="1",
        supported_platforms=["windows", "macos", "linux"],
        verified_product_versions=[],
        detection_rules=[],
        surfaces=surfaces,
        target_capability=TargetCapability.EXPORT_ONLY,
        evidence_urls=["https://docs.windsurf.com/zh/windsurf/cascade/memories"],
    )


def _trae_profile() -> AgentProfile:
    """TRAE Profile（字节跳动，v3.2 调研依据）。

    TRAE 是字节跳动的 AI 原生 IDE，四大核心功能：
    - Memory（记忆）：~/.trae-cn/memory/user_profile.md + projects/<encoded-path>/
    - Rules（规则）：~/.trae-cn/user_rules/*.md
    - Skills（技能）：~/.trae-cn/skills/<skill-name>/
    - MCP：~/.trae-cn/mcps/<server-id>/

    本机实测目录结构（2026-07）：
    ~/.trae-cn/
      memory/
        user_profile.md       # 用户偏好（类 CLAUDE.md）
        projects/             # 项目级记忆（路径编码为目录名）
        .cleanup/ .tmp/
      user_rules/
        rule-*.md             # 用户规则文件
      skills/
        algorithmic-art/ figma/ frontend-skill/ graphify/
        react-best-practices/ security-best-practices/
      mcps/
        s_<server-id>/        # MCP 服务器配置
      plugins/
        trae-remote-official/
      work/
        <session-id>/         # 工作区会话
      builtin/ builtin_skills/ design_libraries/ extensions/ toolhost/ worktrees/

    官方教程：TRAE Memory / Rules / Skills / MCP 四大核心功能
    """
    surfaces = [
        # ---- 用户级 Memory ----
        MemorySurface(
            surface_id="trae_user_profile",
            path_template="%HOME%/.trae-cn/memory/user_profile.md",
            surface_role="native_memory",
            scope="user", load_order=10,
            loader_evidence="https://www.trae.com/ide/memory",
            classification_confidence=0.95,
            category=SourceCategory.NATIVE_MEMORY,
            ingestion_policy=IngestionPolicy.EXTRACT_CANDIDATES,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.TAKEOVER_INPUT,
        ),
        MemorySurface(
            surface_id="trae_memory_projects",
            path_template="%HOME%/.trae-cn/memory/projects",
            surface_role="native_memory",
            scope="user", load_order=11,
            loader_evidence="https://www.trae.com/ide/memory",
            classification_confidence=0.85,
            category=SourceCategory.NATIVE_MEMORY,
            ingestion_policy=IngestionPolicy.EXTRACT_CANDIDATES,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.TAKEOVER_INPUT,
        ),
        # ---- 用户级 Rules ----
        MemorySurface(
            surface_id="trae_user_rules",
            path_template="%HOME%/.trae-cn/user_rules",
            surface_role="control_surface",
            scope="user", load_order=20,
            loader_evidence="https://www.trae.com/ide/rules",
            classification_confidence=0.90,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        # ---- 用户级 Skills ----
        MemorySurface(
            surface_id="trae_skills",
            path_template="%HOME%/.trae-cn/skills",
            surface_role="skill_surface",
            scope="user", load_order=30,
            loader_evidence="https://www.trae.com/ide/skills",
            classification_confidence=0.85,
            category=SourceCategory.SKILL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        # ---- 用户级 MCP 配置 ----
        MemorySurface(
            surface_id="trae_mcps",
            path_template="%HOME%/.trae-cn/mcps",
            surface_role="control_surface",
            scope="user", load_order=40,
            loader_evidence="https://www.trae.com/ide/mcp",
            classification_confidence=0.80,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        # ---- 工作区会话 ----
        MemorySurface(
            surface_id="trae_work_sessions",
            path_template="%HOME%/.trae-cn/work",
            surface_role="conversation_history",
            scope="user", load_order=50,
            loader_evidence="https://www.trae.com/ide/work",
            classification_confidence=0.70,
            category=SourceCategory.CONVERSATION_HISTORY,
            ingestion_policy=IngestionPolicy.EVIDENCE_ONLY,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.NONE,
        ),
        # ---- 项目级 Rules（AGENTS.md 兼容）----
        MemorySurface(
            surface_id="trae_project_agents_md",
            path_template="%WORKSPACE%/AGENTS.md",
            surface_role="control_surface",
            scope="project", load_order=5,
            loader_evidence="https://www.trae.com/ide/rules",
            classification_confidence=0.75,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
    ]
    return AgentProfile(
        profile_id="trae@profile-1",
        product="trae",
        profile_version="1",
        supported_platforms=["windows", "macos", "linux"],
        verified_product_versions=[],
        detection_rules=[],
        surfaces=surfaces,
        target_capability=TargetCapability.EXPORT_ONLY,
        evidence_urls=["https://www.trae.com/ide/memory"],
    )


def _zcode_profile() -> AgentProfile:
    """zcode Profile（CLI 型 Agent，v3.2 调研依据）。

    本机实测目录结构（2026-07）：
    ~/.zcode/
      cli/
        agents/<session-id>/    # 会话
        db/db.sqlite            # 数据库
        rollout/*.jsonl         # 模型 IO 日志
        log/*.jsonl             # 运行日志
        plugins/
        exec/
      v2/
        config.json             # 配置
        setting.json            # 设置
        credentials.json        # 凭据（不读）
        tasks-index.sqlite      # 任务索引
        checkpoints/
        logs/
    """
    surfaces = [
        MemorySurface(
            surface_id="zcode_v2_config",
            path_template="%HOME%/.zcode/v2/config.json",
            surface_role="control_surface",
            scope="user", load_order=10,
            loader_evidence="zcode CLI local config",
            classification_confidence=0.85,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="zcode_v2_setting",
            path_template="%HOME%/.zcode/v2/setting.json",
            surface_role="control_surface",
            scope="user", load_order=11,
            loader_evidence="zcode CLI local settings",
            classification_confidence=0.80,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="zcode_agents",
            path_template="%HOME%/.zcode/cli/agents",
            surface_role="conversation_history",
            scope="user", load_order=20,
            loader_evidence="zcode CLI sessions",
            classification_confidence=0.75,
            category=SourceCategory.CONVERSATION_HISTORY,
            ingestion_policy=IngestionPolicy.EVIDENCE_ONLY,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="zcode_rollout",
            path_template="%HOME%/.zcode/cli/rollout",
            surface_role="runtime_evidence",
            scope="user", load_order=21,
            loader_evidence="zcode CLI model IO logs",
            classification_confidence=0.65,
            category=SourceCategory.RUNTIME_EVIDENCE,
            ingestion_policy=IngestionPolicy.EVIDENCE_ONLY,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="zcode_cli_log",
            path_template="%HOME%/.zcode/cli/log",
            surface_role="runtime_evidence",
            scope="user", load_order=22,
            loader_evidence="zcode CLI runtime logs",
            classification_confidence=0.60,
            category=SourceCategory.RUNTIME_EVIDENCE,
            ingestion_policy=IngestionPolicy.EVIDENCE_ONLY,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.NONE,
        ),
    ]
    return AgentProfile(
        profile_id="zcode@profile-1",
        product="zcode",
        profile_version="1",
        supported_platforms=["windows", "macos", "linux"],
        verified_product_versions=[],
        detection_rules=[],
        surfaces=surfaces,
        target_capability=TargetCapability.EXPORT_ONLY,
        evidence_urls=["zcode CLI local observation"],
    )


def _lingma_profile() -> AgentProfile:
    """通义灵码 Profile（阿里，v3.2 调研依据）。

    本机未安装，但根据公开文档：
    - ~/.lingma/rules/ 目录下建规则文件
    - ~/.lingma/index/meta/v4/index.db 索引数据库
    - 支持 AGENTS.md 项目规则
    """
    surfaces = [
        MemorySurface(
            surface_id="lingma_user_rules",
            path_template="%HOME%/.lingma/rules",
            surface_role="control_surface",
            scope="user", load_order=10,
            loader_evidence="https://lingma.aliyun.com/docs/rules",
            classification_confidence=0.85,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="lingma_config",
            path_template="%HOME%/.lingma",
            surface_role="control_surface",
            scope="user", load_order=11,
            loader_evidence="https://lingma.aliyun.com/",
            classification_confidence=0.65,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="lingma_project_agents_md",
            path_template="%WORKSPACE%/AGENTS.md",
            surface_role="control_surface",
            scope="project", load_order=5,
            loader_evidence="https://lingma.aliyun.com/docs/rules",
            classification_confidence=0.70,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
    ]
    return AgentProfile(
        profile_id="lingma@profile-1",
        product="lingma",
        profile_version="1",
        supported_platforms=["windows", "macos", "linux"],
        verified_product_versions=[],
        detection_rules=[],
        surfaces=surfaces,
        target_capability=TargetCapability.EXPORT_ONLY,
        evidence_urls=["https://lingma.aliyun.com/"],
    )


def _openclaw_profile() -> AgentProfile:
    """OpenClaw Profile（开源 AI 智能体，v3.2 调研依据）。

    OpenClaw 是一个开源 AI 智能体框架，所有配置集中在 ~/.openclaw/。
    本机已安装（部分），实测目录：
    ~/.openclaw/
      plugins/           # 插件（installs.json）
    根据官方文档，完整结构：
    ~/.openclaw/
      workspace/
        AGENTS.md        # 总控规则（行为方式和运行规则）
        SOUL.md          # 人格设定
        USER.md          # 用户档案
        IDENTITY.md      # 身份
        TOOLS.md         # 工具配置
        HEARTBEAT.md     # 心跳配置
        MEMORY.md        # 记忆
        memory/          # 记忆目录
      cron/              # 定时任务
      skills/            # 自定义斜杠命令
      plugins/           # 插件

    与 MemoryGuard 模型最接近：有独立的 MEMORY.md 和 memory/ 目录。
    """
    surfaces = [
        # ---- workspace 核心文件 ----
        MemorySurface(
            surface_id="openclaw_memory_md",
            path_template="%HOME%/.openclaw/workspace/MEMORY.md",
            surface_role="native_memory",
            scope="user", load_order=10,
            loader_evidence="https://www.runoob.com/ai-agent/openclaw-setup.html",
            classification_confidence=0.95,
            category=SourceCategory.NATIVE_MEMORY,
            ingestion_policy=IngestionPolicy.EXTRACT_CANDIDATES,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.TAKEOVER_INPUT,
        ),
        MemorySurface(
            surface_id="openclaw_memory_dir",
            path_template="%HOME%/.openclaw/workspace/memory",
            surface_role="native_memory",
            scope="user", load_order=11,
            loader_evidence="https://www.runoob.com/ai-agent/openclaw-setup.html",
            classification_confidence=0.90,
            category=SourceCategory.NATIVE_MEMORY,
            ingestion_policy=IngestionPolicy.EXTRACT_CANDIDATES,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.TAKEOVER_INPUT,
        ),
        MemorySurface(
            surface_id="openclaw_agents_md",
            path_template="%HOME%/.openclaw/workspace/AGENTS.md",
            surface_role="control_surface",
            scope="user", load_order=20,
            loader_evidence="https://www.runoob.com/ai-agent/openclaw-setup.html",
            classification_confidence=0.95,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="openclaw_soul_md",
            path_template="%HOME%/.openclaw/workspace/SOUL.md",
            surface_role="control_surface",
            scope="user", load_order=21,
            loader_evidence="https://www.runoob.com/ai-agent/openclaw-setup.html",
            classification_confidence=0.90,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="openclaw_user_md",
            path_template="%HOME%/.openclaw/workspace/USER.md",
            surface_role="native_memory",
            scope="user", load_order=12,
            loader_evidence="https://www.runoob.com/ai-agent/openclaw-setup.html",
            classification_confidence=0.85,
            category=SourceCategory.NATIVE_MEMORY,
            ingestion_policy=IngestionPolicy.EXTRACT_CANDIDATES,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.TAKEOVER_INPUT,
        ),
        MemorySurface(
            surface_id="openclaw_identity_md",
            path_template="%HOME%/.openclaw/workspace/IDENTITY.md",
            surface_role="control_surface",
            scope="user", load_order=22,
            loader_evidence="https://www.runoob.com/ai-agent/openclaw-setup.html",
            classification_confidence=0.80,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="openclaw_tools_md",
            path_template="%HOME%/.openclaw/workspace/TOOLS.md",
            surface_role="control_surface",
            scope="user", load_order=23,
            loader_evidence="https://www.runoob.com/ai-agent/openclaw-setup.html",
            classification_confidence=0.75,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        # ---- skills / cron / plugins ----
        MemorySurface(
            surface_id="openclaw_skills",
            path_template="%HOME%/.openclaw/skills",
            surface_role="skill_surface",
            scope="user", load_order=30,
            loader_evidence="https://www.runoob.com/ai-agent/openclaw-setup.html",
            classification_confidence=0.85,
            category=SourceCategory.SKILL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="openclaw_plugins",
            path_template="%HOME%/.openclaw/plugins",
            surface_role="control_surface",
            scope="user", load_order=31,
            loader_evidence="https://www.runoob.com/ai-agent/openclaw-setup.html",
            classification_confidence=0.70,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        MemorySurface(
            surface_id="openclaw_cron",
            path_template="%HOME%/.openclaw/cron",
            surface_role="runtime_evidence",
            scope="user", load_order=32,
            loader_evidence="https://www.runoob.com/ai-agent/openclaw-setup.html",
            classification_confidence=0.65,
            category=SourceCategory.RUNTIME_EVIDENCE,
            ingestion_policy=IngestionPolicy.EVIDENCE_ONLY,
            ownership=Ownership.AGENT_MANAGED,
            target_role=TargetRole.NONE,
        ),
    ]
    return AgentProfile(
        profile_id="openclaw@profile-1",
        product="openclaw",
        profile_version="1",
        supported_platforms=["windows", "macos", "linux"],
        verified_product_versions=[],
        detection_rules=[],
        surfaces=surfaces,
        target_capability=TargetCapability.EXPORT_ONLY,
        evidence_urls=["https://www.runoob.com/ai-agent/openclaw-setup.html"],
    )


def _qoder_profile() -> AgentProfile:
    """Qoder Profile（AI IDE，v3.2 调研依据）。

    Qoder 是一个 AI IDE，规则和技能存储在项目级 .qoder/ 目录：
    - .qoder/rules/    # 项目规则
    - .qoder/skills/   # 技能（SKILL.md）

    用户级配置通过 GUI 面板管理，无文件路径。
    本机未安装。
    """
    surfaces = [
        # ---- 项目级 Rules ----
        MemorySurface(
            surface_id="qoder_project_rules",
            path_template="%WORKSPACE%/.qoder/rules",
            surface_role="control_surface",
            scope="project", load_order=10,
            loader_evidence="https://docs.qoder.com/zh/plugins/introduction",
            classification_confidence=0.90,
            category=SourceCategory.CONTROL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
        # ---- 项目级 Skills ----
        MemorySurface(
            surface_id="qoder_project_skills",
            path_template="%WORKSPACE%/.qoder/skills",
            surface_role="skill_surface",
            scope="project", load_order=11,
            loader_evidence="https://docs.qoder.com/zh/plugins/introduction",
            classification_confidence=0.85,
            category=SourceCategory.SKILL_SURFACE,
            ingestion_policy=IngestionPolicy.GOVERN_ONLY,
            ownership=Ownership.EXTERNAL_READ_ONLY,
            target_role=TargetRole.NONE,
        ),
    ]
    return AgentProfile(
        profile_id="qoder@profile-1",
        product="qoder",
        profile_version="1",
        supported_platforms=["windows", "macos", "linux"],
        verified_product_versions=[],
        detection_rules=[],
        surfaces=surfaces,
        target_capability=TargetCapability.EXPORT_ONLY,
        evidence_urls=["https://docs.qoder.com/zh/plugins/introduction"],
    )


_BUILTIN_PROFILES: list[AgentProfile] = []


def _load_builtins() -> None:
    global _BUILTIN_PROFILES
    if _BUILTIN_PROFILES:
        return
    _BUILTIN_PROFILES = [
        _claude_code_profile(),
        _codex_profile(),
        _cursor_profile(),
        _windsurf_profile(),
        _trae_profile(),
        _zcode_profile(),
        _lingma_profile(),
        _openclaw_profile(),
        _qoder_profile(),
    ]


# ---------------------------------------------------------------------------
# AgentProfileRegistry
# ---------------------------------------------------------------------------


class AgentProfileRegistry:
    """Profile 注册表：内置 + 外部 .memoryguard/agent-profiles/*.json。"""

    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()
        self.profiles_dir = self.workspace / ".memoryguard" / "agent-profiles"
        _load_builtins()

    def list_profiles(self) -> list[AgentProfile]:
        profiles = list(_BUILTIN_PROFILES)
        # 加载外部 Profile（如果存在）
        if self.profiles_dir.exists():
            for f in self.profiles_dir.glob("*.json"):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    profiles.append(AgentProfile.from_dict(data))
                except (OSError, ValueError, KeyError):
                    continue  # 损坏 Profile 静默跳过
        return profiles

    def get_profile(self, profile_id: str) -> AgentProfile | None:
        for p in self.list_profiles():
            if p.profile_id == profile_id:
                return p
        return None

    def save_profile(self, profile: AgentProfile) -> Path:
        """保存外部 Profile 到 .memoryguard/agent-profiles/。"""
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        fname = profile.profile_id.replace("@", "_").replace("/", "_") + ".json"
        path = self.profiles_dir / fname
        path.write_text(
            json.dumps(profile.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path

    def validate(self, profile: AgentProfile) -> list[str]:
        """校验 Profile，返回错误列表（空列表表示通过）。"""
        errors: list[str] = []
        if not profile.profile_id:
            errors.append("profile_id 必填")
        if not profile.product:
            errors.append("product 必填")
        if not profile.surfaces:
            errors.append("至少要有一个 surface")
        for s in profile.surfaces:
            if not s.surface_id:
                errors.append(f"surface 缺少 surface_id: {s.path_template}")
            if not s.path_template:
                errors.append(f"surface 缺少 path_template: {s.surface_id}")
            # v3.1 §3.5：无 fixture 时只能 detect_only / export_only
            if profile.target_capability == TargetCapability.NATIVE_TAKEOVER:
                if not profile.verified_product_versions:
                    errors.append(
                        f"native_takeover 需要真实 fixture，"
                        f"profile {profile.profile_id} 没有 verified_product_versions"
                    )
        return errors


def expand_path(template: str, *, home: str | Path | None = None,
                workspace: str | Path | None = None,
                appdata: str | Path | None = None) -> Path:
    """展开 path_template 中的占位符。

    %HOME% / %APPDATA% / %WORKSPACE% / %WORKSPACE_PARENT%
    """
    import os
    home_str = str(home) if home else os.path.expanduser("~")
    appdata_str = str(appdata) if appdata else os.environ.get("APPDATA", home_str)
    ws_str = str(workspace) if workspace else str(Path.cwd())
    ws_parent = str(Path(ws_str).parent)
    result = template
    result = result.replace("%HOME%", home_str)
    result = result.replace("%APPDATA%", appdata_str)
    result = result.replace("%WORKSPACE%", ws_str)
    result = result.replace("%WORKSPACE_PARENT%", ws_parent)
    return Path(result)


def detect_surface(surface: MemorySurface, *, home: str | Path | None = None,
                   workspace: str | Path | None = None,
                   appdata: str | Path | None = None) -> tuple[SurfaceStatus, str]:
    """探测单个 surface，返回 (status, resolved_path)。

    v3.1 §3.3 安全边界：只做 exists/lstat，不读正文。
    """
    if surface.path_template.startswith("gui-only://"):
        return SurfaceStatus.UNSUPPORTED, surface.path_template
    try:
        path = expand_path(surface.path_template, home=home, workspace=workspace, appdata=appdata)
    except (OSError, ValueError) as e:
        return SurfaceStatus.UNSUPPORTED, f"expand failed: {e}"
    resolved = str(path)
    try:
        if path.exists():
            return SurfaceStatus.FOUND, resolved
        # 父目录存在但目标不存在 -> missing
        if path.parent.exists():
            return SurfaceStatus.MISSING, resolved
        return SurfaceStatus.MISSING, resolved
    except OSError as e:
        return SurfaceStatus.PERMISSION_DENIED, f"{resolved}: {e}"
