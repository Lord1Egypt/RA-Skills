#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
one-novel-skill 引擎注册表

引擎发现、懒加载、生命周期管理。
新增引擎只需注册即可，调度中心自动发现。
"""

import importlib


_REGISTRY = {}
_CALL_COUNTS = {}

# 引擎状态: ready / skeleton / dead
#   ready   — 完整可用的引擎
#   skeleton — 有基础实现，核心逻辑待补充（见文件名 [SKELETON] 标记）
#   dead    — 未调用/废弃（保留供参考，不纳入活跃计数）
_ENGINE_STATES = {"ready": 0, "skeleton": 1, "dead": 2}


def _warn_unused():
    """输出从未被 get() 调用的引擎警告。在 summary() 中自动执行。"""
    unused = [k for k, v in _REGISTRY.items()
              if k not in _CALL_COUNTS and v.get("state", "ready") != "dead"]
    if unused:
        import logging
        logging.warning(f"Registry: {len(unused)} engines never called: {', '.join(unused)}")


def register(name: str, module: str, cls: str, desc: str = "", state: str = "ready"):
    if state not in _ENGINE_STATES:
        state = "ready"
    _REGISTRY[name] = {
        "module": module, "class": cls, "desc": desc,
        "loaded": False, "instance": None, "state": state
    }


def get(name: str, **kw):
    info = _REGISTRY.get(name)
    if not info:
        raise KeyError(f"未知引擎: {name}，可用: {list(_REGISTRY.keys())}")
    if info.get("state") == "dead":
        raise KeyError(f"引擎 {name} 标记为 [DEAD CODE] — 已废弃不调用")
    # 跟踪调用次数
    _CALL_COUNTS[name] = _CALL_COUNTS.get(name, 0) + 1
    if not info["loaded"]:
        mod = importlib.import_module(info["module"])
        cl = getattr(mod, info["class"])
        info["instance"] = cl(**kw) if kw else cl()
        info["loaded"] = True
    return info["instance"]


def list_all() -> dict:
    statuses = {}
    for k, v in sorted(_REGISTRY.items()):
        state = v.get("state", "ready")
        call_count = _CALL_COUNTS.get(k, 0)
        statuses[k] = {
            "desc": v["desc"],
            "loaded": v["loaded"],
            "state": state,
            "calls": call_count,
        }
    _warn_unused()
    return statuses


def summary() -> dict:
    """输出引擎摘要: 总数/活跃/骨架/废弃/调用统计"""
    counts = {"ready": 0, "skeleton": 0, "dead": 0, "loaded": 0, "called": 0, "uncalled": 0}
    for k, v in _REGISTRY.items():
        state = v.get("state", "ready")
        if state in counts:
            counts[state] += 1
        if v["loaded"]:
            counts["loaded"] += 1
        if _CALL_COUNTS.get(k, 0) > 0:
            counts["called"] += 1
        elif state != "dead":
            counts["uncalled"] += 1
    counts["total"] = len(_REGISTRY)
    counts["active"] = counts["ready"] + counts["skeleton"]
    _warn_unused()
    return counts


# 公共接口定义（BaseEngine 替代: 统一方法签名约定）
# 所有 ready/skeleton 引擎应支持以下最小方法集:
#   analyze(text: str, **kwargs) -> dict
# 对于不需要 analyze 的引擎（如 Scheduler/NovelState），提供各自专用接口
BASE_ENGINE_METHODS = ["analyze"]


def validate_signatures(quiet=False):
    """验证所有 ready/skeleton 引擎的方法签名。"""
    import logging, importlib
    failed = []
    for name, info in _REGISTRY.items():
        if info.get("state") == "dead":
            continue
        try:
            mod = importlib.import_module(info["module"])
            cls = getattr(mod, info["class"])
        except (ImportError, AttributeError):
            failed.append((name, f"cannot import {info['module']}.{info['class']}"))
            continue
        for method in BASE_ENGINE_METHODS:
            if not hasattr(cls, method):
                if name in ("scheduler","state","generator","detector","reference","orchestrator"):
                    continue
                failed.append((name, f"missing method: {method}"))
    if failed and not quiet:
        for name, reason in failed:
            logging.warning(f"Engine validate: {name} - {reason}")
    return failed

validate_signatures(quiet=True)
# 核心
register("timeline","engine.engines_timeline","TimelineEngine","时间线追踪引擎")
register("scheduler","engine.scheduler","Scheduler","统一调度引擎(10阶段/31引擎)")
register("state",       "engine.novel_state",      "NovelState",       "JSON 状态机")
register("generator",   "engine.generator",         "TextGenerator",    "LLM 生成器")
register("detector",    "engine.detector_wrapper",  "DetectorWrapper",  "AI 检测封装")
register("reference",   "engine.reference_engine",  "ReferenceEngine",  "参考文献引擎")
# crawler engine removed — module engine.crawler does not exist
# register("crawler",     "engine.crawler",           "CrawlerEngine",    "[DEAD CODE] 网络爬虫引擎（stdlib替代可用）", state="dead")
register("worldbuilder","engine.worldbuilder",      "WorldBuilder",     "蓝图生成器")
register("scoring",     "engine.worldbuilder",      "Scoring",          "评分系统")
register("orchestrator","engine.orchestrator",      "Orchestrator",     "[DEPRECATED] 旧编排器 — 请用 application.orchestrator.ChapterOrchestrator")

# 扩展引擎（全部有实现代码）
register("manager",    "engine.engines_manager",    "ManagerEngine",    "管理引擎 — 项目队列/KDP策略/有声书参数 [未接入管线]", state="skeleton")
register("logic",      "engine.engines_logic",      "LogicEngine",      "逻辑引擎 — 规则推理/设定一致性/矛盾检测")
register("reasoning",  "engine.engines_reasoning",  "ReasoningEngine",  "推理引擎 — 因果推理/伏笔调度/情节推演")
register("algorithm",  "engine.engines_algorithm",  "AlgorithmEngine",  "算法引擎 — 文本模式匹配/N元词频/重复度检测")
register("psychology", "engine.engines_psychology", "PsychologyEngine", "心理引擎 — 读者心理/情绪弧/驱动力分析")
register("nlp",        "engine.engines_nlp",        "NLPEngine",        "自然语言引擎 — 描写质量/句式/感官检测")
register("statistics", "engine.engines_utils",      "StatisticsEngine", "统计引擎 — 分布/百分位/基线匹配")
register("literature", "engine.engines_literature",   "LiteratureEngine",     "文学引擎")
register("architecture","engine.engines_architecture","ArchitectureEngine",   "架构引擎")
register("tension",    "engine.engines_tension",      "TensionEngine",        "张力校准引擎")
register("dialogue",   "engine.engines_dialogue",     "DialogueEngine",       "对话质量引擎")

# skeleton 引擎分类（第五轮审查）:
#   接入管线: clarify, user_prefs — 有价值且无功能重叠
#   功能重叠(归档): entity_extr→CharacterStateEngine, multi_review→StoryGate,
#                  spec_valid→SpecBuilder, task_decomp→ArcManager,
#                  timeline_bld→TimelineEngine, learnings→SessionState
register("clarify",      "engine.clarify_questions",   "ClarifyAnswers",      "三层递进问答 [待接入管线]", state="skeleton")
register("entity_extr",  "engine.entity_extractor",    "EntityExtractor",     "实体提取器 [归档: 与CharacterStateEngine重叠]", state="skeleton")
register("multi_review", "engine.multi_view_review",   "ReviewReportStructure","多视角审查 [归档: 与StoryGate重叠]", state="skeleton")
register("spec_valid",   "engine.spec_validator",      "SpecValidator",       "规格校验器 [归档: 与SpecBuilder重叠]", state="skeleton")
register("task_decomp",  "engine.task_decomposer",     "ChapterTask",         "任务分解器 [归档: 与ArcManager重叠]", state="skeleton")
register("timeline_bld", "engine.timeline_builder",    "Timeline",            "时间线构建器 [归档: 与TimelineEngine重叠]", state="skeleton")
register("user_prefs",   "engine.user_preferences",    "PreferenceManager",   "用户偏好管理 [待接入管线]", state="skeleton")
register("learnings",    "engine.writing_learnings",   "LearningsManager",    "写作教训追踪 [归档: 与SessionState重叠]", state="skeleton")

# 写作拓展
register("writing",    "engine.engines_writing",      "WritingEngine",       "写作引擎")
register("learning",   "engine.engines_utils",        "LearningEngine",      "学习引擎")
register("planning",   "engine.engines_planning",     "PlanningEngine",      "决策与规划引擎")
register("data",       "engine.engines_utils",        "DataEngine",          "数据引擎")
register("simulation", "engine.simulation",           "SimulationEngine",    "模拟仿真引擎")
register("digital",    "engine.engines_utils",        "DigitalEngine",       "数字引擎")
register("analysis",   "engine.engines_analysis",     "AnalysisEngine",      "分析引擎")
register("screenplay", "engine.engines_screenplay",   "ScreenplayEngine",    "剧本/场景引擎")
register("inspiration","engine.engines_inspiration",  "InspirationEngine",   "创意灵感引擎")
register("development","engine.engines_development",  "DevelopmentEngine",   "故事发展引擎")

# 新增引擎 — SKILL.md 声明功能补全
register("narrative_structure", "engine.narrative_structure", "NarrativeStructureEngine", "叙事结构增强 — 八段式/反直觉追问/升番逻辑/情绪置换")
register("chapter_contract",    "engine.chapter_contract",    "ChapterContractEngine",    "章节契约系统 — 独立契约+确认流程+归档")
register("prewriting",          "engine.prewriting_analyzer",  "PrewritingAnalyzer",       "写前分析预览 — 前文摘要/角色快照/风险标记")
register("semantic_review",     "engine.semantic_review",     "SemanticReviewEngine",     "L3-L4语义层审查 — 六条连续性法则+阅读体验")
register("short_story",         "engine.short_story_mode",    "ShortStoryModeEngine",     "短故事模式 — SS0/SS1/SS2三阶段+红线检查")
register("platform_article",    "engine.platform_article",    "PlatformArticleEngine",    "平台文章模式 — A0选题/A1正文+格式校验")
register("memory_hierarchy",    "engine.memory_hierarchy",    "MemoryHierarchyEngine",    "四层记忆消歧 — 宪法/治理/运行/工作+触发学习")
register("triggered_learning",  "engine.memory_hierarchy",    "TriggeredLearningEngine",  "触发学习引擎 — 显式纠正/三次重复/记住这个")
register("multi_agent_collab",  "engine.multi_agent_collaboration", "MultiAgentCollaborationEngine", "多智能体协作 — 串行/并行/团队模式")

# Phase 0-3 重构新增模块
register("event_bus",       "engine.event_bus",        "EventBus",              "统一事件总线 — 串联93引擎输出")
register("global_rollback", "engine.global_rollback",   "SideEffectTracker",     "全局回滚 — 副作用追踪+自动回滚")
