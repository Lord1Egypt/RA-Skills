#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prompt_registry.py — Prompt Registry 统一注册中心

灵感来源: AI-Novel-Writing-Assistant 的 Prompt Registry 模式
核心思想: 所有产品级 Prompt 强制走注册中心，含 id/version/taskType/mode/contextPolicy/outputSchema
         避免散落各处的内联 Prompt，支持版本管理和 Schema 校验。

用法:
  reg = PromptRegistry()
  prompt = reg.get("write_chapter", platform="番茄", genre="都市")
  reg.list_all()  # 查看所有注册的 Prompt
"""

import json, logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

_log = logging.getLogger("prompt_registry")

# ── Schema 定义 ──

@dataclass
class PromptEntry:
    """单个 Prompt 条目"""
    id: str                    # 唯一标识
    version: str = "1.0.0"     # 版本号
    task_type: str = ""        # 任务类型: generate/review/rewrite/plan/detect
    mode: str = "standard"     # 模式: standard/l3/quick/minimal
    context_policy: str = "full"  # 上下文策略: full/sliding/summary
    output_schema: Dict[str, Any] = field(default_factory=dict)  # 输出格式约束
    system: str = ""           # System Prompt
    user_template: str = ""    # User Prompt 模板
    variables: List[str] = field(default_factory=list)  # 模板变量列表
    category: str = "general"  # 分类: writing/review/planning/character/worldbuilding
    priority: int = 0          # 优先级（越大越优先）
    description: str = ""      # 描述
    source: str = "built-in"   # 来源: built-in/yaml/user


class PromptRegistry:
    """Prompt 统一注册中心"""

    def __init__(self, registry_path: str = ""):
        self._entries: Dict[str, PromptEntry] = {}
        self._categories: Dict[str, List[str]] = {}

        # 注册内置 Prompt
        self._register_builtins()

        # 加载外部注册表
        if registry_path:
            self._load_external(registry_path)
        else:
            default_path = Path(__file__).parent.parent / "templates" / "prompts" / "registry.json"
            if default_path.exists():
                self._load_external(str(default_path))

    def _register_builtins(self):
        """注册所有内置 Prompt"""
        self._add(PromptEntry(
            id="write_chapter",
            version="1.0.0",
            task_type="generate",
            mode="standard",
            context_policy="full",
            output_schema={"type": "text", "format": "纯文本章节正文", "min_chars": 1500},
            system="你扮演的身份——番茄小说网殿堂金番作家。熟知番茄小说网各个题材写作方法及技巧，更清楚番茄小说网读者的各个喜好。每章输出前严格执行写作规范。",
            user_template="【前情】{context}\n【章节】第{chapter}章\n【核心情节】{plot_points}\n【风格约束】{style_lock}\n【写作指导】{writing_notes}\n### 请写正文 ###",
            variables=["context", "chapter", "chapter_title", "plot_points", "style_lock", "writing_notes", "word_count", "key_scenes", "ending_hook", "new_hooks", "characters"],
            category="writing",
            priority=10,
            description="核心章节生成 Prompt",
        ))

        self._add(PromptEntry(
            id="write_chapter_l3",
            version="1.0.0",
            task_type="generate",
            mode="l3",
            context_policy="full",
            output_schema={"type": "text", "format": "三段温度震荡合成文本"},
            system="同上 + L3反AI约束（去痕/角色限定/思维暴露/自反驳/统计签名）",
            user_template="同 write_chapter + 分段标签（开头/中段/结尾）",
            variables=["context", "chapter", "chapter_title", "plot_points", "style_lock", "writing_notes", "word_count", "key_scenes", "ending_hook", "new_hooks", "characters", "genre", "platform"],
            category="writing",
            priority=8,
            description="L3 三段温度震荡 + 角色坍缩防护",
        ))

        self._add(PromptEntry(
            id="review_chapter",
            version="1.0.0",
            task_type="review",
            mode="standard",
            context_policy="full",
            output_schema={"type": "json", "fields": ["issues", "score", "verdict", "suggestions"]},
            system="你是资深网文编辑。对已完成章节进行逐章审查，检查语言、故事逻辑、角色一致性。",
            user_template="审查以下章节正文。列出所有需要修改的地方，然后输出修改后的版本。\n\n章节：第{chapter}章\n正文：{text}",
            variables=["chapter", "text"],
            category="review",
            priority=5,
            description="单章审查 Prompt",
        ))

        self._add(PromptEntry(
            id="rewrite_deai",
            version="1.0.0",
            task_type="rewrite",
            mode="standard",
            context_policy="sliding",
            output_schema={"type": "text", "format": "修改后的纯文本"},
            system="你是中文网文编辑，擅长消除AI痕迹。改写原则：用具体动作替代抽象情绪，用短句交替替代均匀节奏，用口语化表达替代书面语。",
            user_template="【原文】{text}\n【问题】{issues}\n请修改：",
            variables=["text", "issues"],
            category="writing",
            priority=6,
            description="去AI改写 Prompt",
        ))

        self._add(PromptEntry(
            id="review_outline",
            version="1.0.0",
            task_type="review",
            mode="standard",
            context_policy="summary",
            output_schema={"type": "json", "fields": ["sell_point", "one_liner", "drama_space", "causal_chain", "risks"]},
            system="你是有20年经验的网文总编辑。对大纲做全面审查。",
            user_template="审查以下大纲。回答：1)核心卖点 2)一句话概括 3)戏剧空间 4)因果线完整性 5)目标/计划/阻扰因素\n\n大纲：{outline_text}",
            variables=["outline_text"],
            category="review",
            priority=4,
            description="大纲审查 Prompt",
        ))

        self._add(PromptEntry(
            id="generate_outline",
            version="1.0.0",
            task_type="generate",
            mode="standard",
            context_policy="minimal",
            output_schema={"type": "text", "format": "分卷大纲"},
            system="你是网文大纲规划师。生成清晰的分卷大纲。",
            user_template="题材：{genre}\n平台：{platform}\n章节：{chapters}\n情绪：{emotion}\n\n生成大纲：",
            variables=["genre", "platform", "chapters", "emotion"],
            category="planning",
            priority=3,
            description="大纲生成 Prompt",
        ))

        self._add(PromptEntry(
            id="generate_character",
            version="1.0.0",
            task_type="generate",
            mode="standard",
            context_policy="minimal",
            output_schema={"type": "json", "fields": ["name", "identity", "appearance", "personality", "background", "goal", "flaw", "arc"]},
            system="生成结构化角色档案：姓名、身份、外貌、性格、背景、目标、缺陷、成长弧。",
            user_template="角色：{name}\n类型：{role_type}\n世界观：{world}\n\n生成档案：",
            variables=["name", "role_type", "world"],
            category="character",
            priority=3,
            description="角色生成 Prompt",
        ))

        self._add(PromptEntry(
            id="full_dimension_review",
            version="1.0.0",
            task_type="review",
            mode="standard",
            context_policy="summary",
            output_schema={"type": "text", "format": "全维度审查报告"},
            system="你是网文总编辑+反AI审查专家。对全书做全维度深层审查。",
            user_template="对以下项目做全维度深层审查：设定/世界观/主线/支线/人物一致性/伏笔埋设和回收/反派智商/ AI去痕/平台适配\n\n项目资料：{project_data}",
            variables=["project_data"],
            category="review",
            priority=2,
            description="全维度审查 Prompt",
        ))

        self._add(PromptEntry(
            id="hook_planning",
            version="1.0.0",
            task_type="plan",
            mode="standard",
            context_policy="sliding",
            output_schema={"type": "text", "format": "伏笔规划方案"},
            system="你是网文伏笔规划师。根据已写内容和待回收伏笔，规划下一阶段伏笔埋设方案。",
            user_template="已写章节范围：{written}\n大纲概要：{outline}\n待规划伏笔：{pending_hooks}\n\n请规划本阶段伏笔埋设方案：",
            variables=["written", "outline", "pending_hooks"],
            category="planning",
            priority=2,
            description="伏笔规划 Prompt",
        ))

        self._add(PromptEntry(
            id="chapter_acceptance",
            version="1.0.0",
            task_type="review",
            mode="standard",
            context_policy="sliding",
            output_schema={"type": "json", "fields": ["pass", "reason", "issues"]},
            system="你是严格的验收编辑。评估本章是否达到交付标准。",
            user_template="验收以下章节：第{chapter}章\n平台：{platform}\n题材：{genre}\n正文开头：{text}\n检测问题：{issues}\n\n请判断：通过或拒绝。",
            variables=["chapter", "platform", "genre", "text", "issues"],
            category="review",
            priority=3,
            description="章节验收 Prompt",
        ))

    def _add(self, entry: PromptEntry):
        self._entries[entry.id] = entry
        if entry.category not in self._categories:
            self._categories[entry.category] = []
        if entry.id not in self._categories[entry.category]:
            self._categories[entry.category].append(entry.id)

    def _load_external(self, path: str):
        """从 JSON 文件加载外部 Prompt 注册表"""
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            for item in data.get("prompts", []):
                entry = PromptEntry(**item)
                self._add(entry)
            _log.info(f"PromptRegistry: loaded {len(data.get('prompts', []))} external prompts")
        except Exception as e:
            _log.warning(f"PromptRegistry: failed to load external: {e}")

    def get(self, prompt_id: str) -> Optional[PromptEntry]:
        """获取指定 Prompt"""
        return self._entries.get(prompt_id)

    def get_by_category(self, category: str) -> List[PromptEntry]:
        """按分类获取 Prompt 列表"""
        ids = self._categories.get(category, [])
        return [self._entries[i] for i in ids if i in self._entries]

    def get_by_task_type(self, task_type: str) -> List[PromptEntry]:
        """按任务类型获取 Prompt 列表"""
        return [e for e in self._entries.values() if e.task_type == task_type]

    def list_all(self) -> List[Dict[str, Any]]:
        """列出所有 Prompt 摘要"""
        return [
            {
                "id": e.id,
                "version": e.version,
                "category": e.category,
                "task_type": e.task_type,
                "mode": e.mode,
                "priority": e.priority,
                "description": e.description,
                "variables": e.variables,
            }
            for e in sorted(self._entries.values(), key=lambda x: (-x.priority, x.id))
        ]

    def validate_variables(self, prompt_id: str, provided_vars: dict) -> List[str]:
        """校验提供的变量是否满足 Prompt 要求"""
        entry = self._entries.get(prompt_id)
        if not entry:
            return [f"Prompt '{prompt_id}' not found"]

        missing = []
        for var in entry.variables:
            if var not in provided_vars or not provided_vars[var]:
                missing.append(var)
        return missing

    def export_registry(self, path: str):
        """导出注册表到 JSON"""
        data = {
            "version": "1.0.0",
            "prompts": [
                {
                    "id": e.id,
                    "version": e.version,
                    "task_type": e.task_type,
                    "mode": e.mode,
                    "context_policy": e.context_policy,
                    "output_schema": e.output_schema,
                    "system": e.system,
                    "user_template": e.user_template,
                    "variables": e.variables,
                    "category": e.category,
                    "priority": e.priority,
                    "description": e.description,
                }
                for e in self._entries.values()
            ],
        }
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        _log.info(f"PromptRegistry: exported {len(self._entries)} prompts to {path}")


# 全局单例
_registry_instance: Optional[PromptRegistry] = None

def get_registry() -> PromptRegistry:
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = PromptRegistry()
    return _registry_instance
