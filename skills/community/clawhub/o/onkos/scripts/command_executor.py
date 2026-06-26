#!/usr/bin/env python3
"""
命令执行器 - OnKos 统一命令入口
架构: 直接调用Python函数，无subprocess/param_map映射层
引擎实例缓存复用，消除进程启动开销和参数名映射bug
"""

import sys
import json
import importlib
from pathlib import Path
from typing import Dict, Any


class CommandExecutor:
    """命令执行器 - 统一命令入口"""

    SCRIPTS_DIR = Path(__file__).parent

    # 英文别名 / 中文别名 → COMMAND_MAP 中的正式命令名
    ALIAS_MAP = {
        # 英文别名
        "help": "help", "write": "store-chapter", "store": "store-scene",
        "search": "search", "audit": "audit", "progress": "arc-progress",
        "suggest": "suggest-next", "status": "status",
        "fact": "get-fact", "check": "check-continuity",
        "stats": "mem-stats", "revise": "analyze-revision", "style": "analyze-style",
        "continue": "for-creation",
        "engagement": "engagement-trend", "pacing": "pacing-report", "debt": "debt-report",
        # 中文别名
        "帮助": "help", "指令列表": "help", "命令列表": "help",
        "写": "store-chapter", "续写": "for-creation",
        "存储": "store-scene", "搜索": "search", "检索": "search",
        "查事实": "get-fact", "检查": "check-continuity",
        "审计": "audit", "进度": "arc-progress",
        "建议": "suggest-next", "统计": "mem-stats",
        "修订": "analyze-revision", "分析风格": "analyze-style",
        "状态": "status", "创建项目": "init",
        "创建角色": "create-character", "创建阶段": "create-phase",
        "创建弧线": "create-arc-am",
        "导入设定": "import-settings", "预览设定": "preview-settings",
        "更新设定": "update-settings", "删除设定": "delete-settings",
        "提取实体": "extract-entities", "录入事实": "set-fact",
        "种伏笔": "plant-hook", "回收伏笔": "resolve-hook",
        "放弃伏笔": "abandon-hook", "更新摘要": "store-summary",
        "完成章节": "chapter-complete", "完成弧线": "complete-arc",
        "列出角色": "list-chars", "列出伏笔": "list-hooks",
        "列出弧线": "list-arcs", "列出节点": "list-nodes",
        "OOC检测": "check-ooc", "角色提示词": "char-prompt",
        "添加节点": "add-node", "添加关系": "add-edge",
        "查节点": "find-node", "查路径": "find-path", "查邻居": "get-neighbors",
        "相关事实": "relevant-facts", "伏笔统计": "hook-stats",
        "伏笔": "overdue-hooks", "矛盾": "detect-contradictions",
        "覆盖检查": "context-hierarchy", "预算": "budget-report",
        "获取上下文": "for-creation",
        "添加情节": "add-plot", "创建支线": "create-branch",
        "检查支线": "check-branches", "情节时间线": "plot-timeline",
        "比较风格": "compare-style",
        "更新事实": "set-fact", "归档事实": "archive-facts",
        "查所有事实": "list-all-facts", "图谱统计": "kg-stats",
        "指令详情": "help",
        "检测事实变更": "detect-fact-changes",
        "评分": "score-chapter", "追读力": "engagement-trend", "节奏": "pacing-report", "债务": "debt-report",
        "score": "score-chapter",
        # 特殊符号
        "?": "help",
    }

    # 命令 → 模块/类/动作 映射
    # module: 脚本文件名(不含.py), class: 类名, action: execute_action的action参数
    COMMAND_MAP = {
        # 系统
        "help": {"module": "_builtin", "action": "help"},

        # 项目管理
        "init": {"module": "project_initializer", "class": "ProjectInitializer", "action": "init"},
        "status": {"module": "project_initializer", "class": "ProjectInitializer", "action": "status"},
        "import-settings": {"module": "settings_importer", "class": "SettingsImporter", "action": "import"},
        "preview-settings": {"module": "settings_importer", "class": "SettingsImporter", "action": "dry-run"},
        "update-settings": {"module": "settings_importer", "class": "SettingsImporter", "action": "update"},
        "delete-settings": {"module": "settings_importer", "class": "SettingsImporter", "action": "delete"},

        # 记忆引擎
        "store-chapter": {"module": "memory_engine", "class": "MemoryEngine", "action": "store-chapter"},
        "store-scene": {"module": "memory_engine", "class": "MemoryEngine", "action": "store-scene"},
        "delete-chapter-scenes": {"module": "memory_engine", "class": "MemoryEngine", "action": "delete-chapter-scenes"},
        "search": {"module": "memory_engine", "class": "MemoryEngine", "action": "search"},
        "store-summary": {"module": "memory_engine", "class": "MemoryEngine", "action": "store-summary"},
        "mem-stats": {"module": "memory_engine", "class": "MemoryEngine", "action": "stats"},
        "create-arc": {"module": "memory_engine", "class": "MemoryEngine", "action": "create-arc"},
        "list-arcs": {"module": "memory_engine", "class": "MemoryEngine", "action": "list-arcs"},
        "chapter-complete": {"module": "memory_engine", "class": "MemoryEngine", "action": "chapter-complete"},

        # 事实引擎
        "set-fact": {"module": "fact_engine", "class": "FactEngine", "action": "set-fact"},
        "get-fact": {"module": "fact_engine", "class": "FactEngine", "action": "get-fact"},
        "get-facts": {"module": "fact_engine", "class": "FactEngine", "action": "get-facts"},
        "relevant-facts": {"module": "fact_engine", "class": "FactEngine", "action": "relevant-facts"},
        "list-all-facts": {"module": "fact_engine", "class": "FactEngine", "action": "get-facts"},
        "get-relevant-facts": {"module": "fact_engine", "class": "FactEngine", "action": "relevant-facts"},
        "archive-facts": {"module": "fact_engine", "class": "FactEngine", "action": "archive-facts"},
        "supersede-chapter-facts": {"module": "fact_engine", "class": "FactEngine", "action": "supersede-chapter-facts"},
        "detect-contradictions": {"module": "fact_engine", "class": "FactEngine", "action": "detect-contradictions"},
        "fact-history": {"module": "fact_engine", "class": "FactEngine", "action": "fact-history"},

        # 知识图谱
        "add-node": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "add-node"},
        "add-edge": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "add-edge"},
        "delete-edge": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "delete-edge"},
        "find-edge-by-names": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "find-edge-by-names"},
        "find-node": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "find-node"},
        "get-neighbors": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "get-neighbors"},
        "find-path": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "find-path"},
        "list-nodes": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "list-nodes"},
        "kg-stats": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "stats"},

        # 伏笔追踪
        "plant-hook": {"module": "hook_tracker", "class": "HookTracker", "action": "plant"},
        "resolve-hook": {"module": "hook_tracker", "class": "HookTracker", "action": "resolve"},
        "partial-resolve": {"module": "hook_tracker", "class": "HookTracker", "action": "partial-resolve"},
        "hint-hook": {"module": "hook_tracker", "class": "HookTracker", "action": "hint"},
        "update-hook-strength": {"module": "hook_tracker", "class": "HookTracker", "action": "update-strength"},
        "abandon-hook": {"module": "hook_tracker", "class": "HookTracker", "action": "abandon"},
        "abandon-chapter-hooks": {"module": "hook_tracker", "class": "HookTracker", "action": "abandon-chapter"},
        "list-hooks": {"module": "hook_tracker", "class": "HookTracker", "action": "list-open"},
        "overdue-hooks": {"module": "hook_tracker", "class": "HookTracker", "action": "overdue"},
        "forgotten-hooks": {"module": "hook_tracker", "class": "HookTracker", "action": "forgotten"},
        "hook-stats": {"module": "hook_tracker", "class": "HookTracker", "action": "stats"},

        # 追读力
        "score-chapter": {"module": "engagement_tracker", "class": "EngagementTracker", "action": "score"},
        "engagement-trend": {"module": "engagement_tracker", "class": "EngagementTracker", "action": "trend"},
        "pacing-report": {"module": "engagement_tracker", "class": "EngagementTracker", "action": "pacing"},
        "debt-report": {"module": "engagement_tracker", "class": "EngagementTracker", "action": "debt"},

        # 弧线管理
        "create-phase": {"module": "arc_manager", "class": "ArcManager", "action": "create-phase"},
        "create-arc-am": {"module": "arc_manager", "class": "ArcManager", "action": "create-arc"},
        "complete-arc": {"module": "arc_manager", "class": "ArcManager", "action": "complete-arc"},
        "arc-progress": {"module": "arc_manager", "class": "ArcManager", "action": "progress"},
        "suggest-next": {"module": "arc_manager", "class": "ArcManager", "action": "suggest-next"},

        # 角色管理
        "create-character": {"module": "character_simulator", "class": "CharacterSimulator", "action": "create"},
        "check-ooc": {"module": "character_simulator", "class": "CharacterSimulator", "action": "check-ooc"},
        "char-prompt": {"module": "character_simulator", "class": "CharacterSimulator", "action": "generate-prompt"},
        "list-chars": {"module": "character_simulator", "class": "CharacterSimulator", "action": "list"},

        # 质量审计
        "audit": {"module": "quality_auditor", "class": "QualityAuditor", "action": "audit"},

        # 连续性检查
        "check-continuity": {"module": "continuity_checker", "class": "ContinuityChecker", "action": "check-chapter"},
        "analyze-revision": {"module": "continuity_checker", "class": "ContinuityChecker", "action": "analyze-revision"},

        # 风格分析
        "analyze-style": {"module": "style_learner", "class": "StyleLearner", "action": "analyze"},
        "compare-style": {"module": "style_learner", "class": "StyleLearner", "action": "compare"},

        # 实体提取
        "extract-entities": {"module": "entity_extractor", "class": "EntityExtractor", "action": "extract"},

        # 情节管理
        "add-plot": {"module": "plot_brancher", "class": "PlotBrancher", "action": "add-node"},
        "create-branch": {"module": "plot_brancher", "class": "PlotBrancher", "action": "create-branch"},
        "plot-timeline": {"module": "plot_brancher", "class": "PlotBrancher", "action": "timeline"},
        "check-branches": {"module": "plot_brancher", "class": "PlotBrancher", "action": "check-health"},

        # 上下文检索
        "for-creation": {"module": "context_retriever", "class": "ContextRetriever", "action": "for-creation"},
        "context-hierarchy": {"module": "context_retriever", "class": "ContextRetriever", "action": "hierarchy"},
        "budget-report": {"module": "context_retriever", "class": "ContextRetriever", "action": "budget-report"},

        # 内置命令
        "clear-chapter": {"module": "_builtin", "action": "clear-chapter"},
        "detect-fact-changes": {"module": "_builtin", "action": "detect-fact-changes"},
    }

    # 命令级参数重映射：command_executor API参数名 → 底层execute_action参数名
    PARAM_MAP = {
        "extract-entities": {"content": "text"},
        "plant-hook": {"desc": "description"},
        "resolve-hook": {"how": "resolution", "chapter": "resolved_chapter"},
        "check-ooc": {"character": "name", "content": "behavior"},
        "get-relevant-facts": {"chapter": "chapter"},
        "overdue-hooks": {"chapter": "current_chapter"},
        "forgotten-hooks": {"chapter": "current_chapter"},
        "list-hooks": {"chapter": "current_chapter"},
        "create-branch": {"name": "title", "parent_node": "from_node"},
        "debt-report": {"chapter": "current_chapter"},
        "analyze-revision": {"original_content": "old_content", "revised_content": "new_content"},
    }

    # 引擎构造参数：不同模块的初始化参数不同
    ENGINE_INIT_PARAMS = {
        "project_initializer": {"key": "project_path", "class": "ProjectInitializer"},
        "settings_importer": {"key": "project_path", "class": "SettingsImporter"},
        "memory_engine": {"key": "db_path", "class": "MemoryEngine", "extra": {"project_path": "{project_path}"}},
        "fact_engine": {"key": "db_path", "class": "FactEngine", "extra": {"project_path": "{project_path}"}},
        "knowledge_graph": {"key": "db_path", "class": "KnowledgeGraph"},
        "hook_tracker": {"key": "db_path", "class": "HookTracker"},
        "engagement_tracker": {"key": "db_path", "class": "EngagementTracker"},
        "arc_manager": {"key": "db_path", "class": "ArcManager", "extra": {"project_path": "{project_path}"}},
        "character_simulator": {"key": "characters_dir", "class": "CharacterSimulator"},
        "quality_auditor": {"key": "project_path", "class": "QualityAuditor"},
        "continuity_checker": {"key": "project_path", "class": "ContinuityChecker"},
        "style_learner": {"key": "style_path", "class": "StyleLearner"},
        "entity_extractor": {"key": "project_path", "class": "EntityExtractor"},
        "plot_brancher": {"key": "plot_path", "class": "PlotBrancher"},
        "context_retriever": {"key": "db_path", "class": "ContextRetriever", "extra": {"project_path": "{project_path}"}},
    }

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self._engine_cache = {}   # 引擎实例缓存
        self._module_cache = {}   # 模块缓存

    def _get_db_path(self) -> str:
        return str(self.project_path / "data" / "novel_memory.db")

    def _resolve_extra_kwargs(self, extra: dict) -> dict:
        """解析extra中的模板变量"""
        resolved = {}
        for k, v in extra.items():
            if isinstance(v, str) and v == "{project_path}":
                resolved[k] = str(self.project_path)
            else:
                resolved[k] = v
        return resolved

    def _get_engine(self, module_name: str):
        """获取引擎实例（懒加载+缓存）"""
        if module_name in self._engine_cache:
            return self._engine_cache[module_name]

        # 动态import模块
        if module_name not in self._module_cache:
            self._module_cache[module_name] = importlib.import_module(module_name)
        module = self._module_cache[module_name]

        # 获取类名
        class_name = self.ENGINE_INIT_PARAMS[module_name].get("class")
        if not class_name:
            # 从模块中自动查找第一个非私有、非typing类型的类
            import typing
            typing_attrs = set(dir(typing))
            for attr_name in dir(module):
                obj = getattr(module, attr_name)
                if (isinstance(obj, type) and not attr_name.startswith('_')
                        and attr_name not in typing_attrs
                        and hasattr(obj, '__module__')
                        and obj.__module__ != 'typing'):
                    class_name = attr_name
                    break
        cls = getattr(module, class_name)

        # 构造参数
        init_config = self.ENGINE_INIT_PARAMS[module_name]
        init_key = init_config["key"]
        init_kwargs = self._resolve_extra_kwargs(init_config.get("extra", {}))

        if init_key == "db_path":
            instance = cls(self._get_db_path(), **init_kwargs)
        elif init_key == "project_path":
            instance = cls(str(self.project_path), **init_kwargs)
        elif init_key == "characters_dir":
            instance = cls(str(self.project_path / "data" / "characters"), **init_kwargs)
        elif init_key == "style_path":
            instance = cls(str(self.project_path / "data" / "style_profile.json"), **init_kwargs)
        elif init_key == "plot_path":
            instance = cls(str(self.project_path / "data" / "plot_graph.json"), **init_kwargs)
        else:
            instance = cls(**init_kwargs)

        self._engine_cache[module_name] = instance
        return instance

    def _infer_chapter(self) -> int:
        """从事实引擎推断最新章节"""
        try:
            engine = self._get_engine("fact_engine")
            chapter = engine.get_latest_chapter()
            return chapter if chapter > 0 else 1
        except Exception:
            return 1

    def execute(self, command: str, args: Dict[str, Any] = None) -> Dict[str, Any]:
        # 去除命令前缀斜杠（/help → help）
        if command.startswith("/"):
            command = command[1:]

        # 别名解析
        command = self.ALIAS_MAP.get(command, command)

        # 命令查找
        cmd_info = self.COMMAND_MAP.get(command)
        if not cmd_info:
            return {"error": f"未知命令: {command}", "available": list(self.COMMAND_MAP.keys())}

        # 内置命令
        if cmd_info["module"] == "_builtin":
            if cmd_info["action"] == "help":
                return self._help_output(args)
            if cmd_info["action"] == "clear-chapter":
                return self._clear_chapter(args)
            if cmd_info["action"] == "detect-fact-changes":
                return self._detect_fact_changes(args)
            return {"error": f"未知内置命令: {command}"}

        # 获取引擎实例并直接调用
        args = args or {}
        module_name = cmd_info["module"]
        action = cmd_info["action"]

        # 命令级参数重映射
        if command in self.PARAM_MAP:
            for from_key, to_key in self.PARAM_MAP[command].items():
                if from_key in args and to_key not in args:
                    args[to_key] = args.pop(from_key)

        try:
            engine = self._get_engine(module_name)
        except Exception as e:
            return {"error": f"引擎初始化失败: {str(e)}", "module": module_name}

        try:
            result = engine.execute_action(action, args)
            return result
        except ValueError as e:
            return {"error": str(e), "command": command}
        except TypeError as e:
            return {"error": f"参数错误: {str(e)}", "command": command}
        except Exception as e:
            return {"error": f"执行失败: {str(e)}", "command": command}

    def close(self):
        """释放所有缓存的引擎实例"""
        for engine in self._engine_cache.values():
            if hasattr(engine, 'close'):
                try:
                    engine.close()
                except Exception:
                    pass
        self._engine_cache.clear()

    def list_commands(self) -> Dict[str, str]:
        return {cmd: info.get("action", "") for cmd, info in self.COMMAND_MAP.items()}

    def _clear_chapter(self, args: Dict[str, Any] = None) -> Dict[str, Any]:
        """清理指定章节的旧数据（场景+事实+伏笔）"""
        args = args or {}
        chapter = args.get("chapter")
        if chapter is None:
            return {"error": "缺少 chapter 参数"}

        result = {"chapter": chapter}

        # 使用缓存的引擎实例
        try:
            me = self._get_engine("memory_engine")
            deleted_scenes = me.delete_chapter_scenes(int(chapter))
            result["deleted_scenes"] = deleted_scenes
        except Exception as e:
            result["deleted_scenes"] = f"错误: {e}"

        try:
            fe = self._get_engine("fact_engine")
            superseded_facts = fe.supersede_chapter_facts(int(chapter))
            result["superseded_facts"] = superseded_facts
        except Exception as e:
            result["superseded_facts"] = f"错误: {e}"

        try:
            ht = self._get_engine("hook_tracker")
            abandoned_hooks = ht.abandon_chapter_hooks(int(chapter))
            result["abandoned_hooks"] = abandoned_hooks
        except Exception as e:
            result["abandoned_hooks"] = f"错误: {e}"

        return result

    def _detect_fact_changes(self, args: Dict[str, Any] = None) -> Dict[str, Any]:
        """从章节内容自动检测事实变更

        整合实体提取和事实检索，返回结构化数据供智能体分析。
        智能体对比章节内容与现有事实，识别: 新事实、更新事实、冲突事实。
        """
        args = args or {}
        content = args.get("content")
        chapter = args.get("chapter")
        genre = args.get("genre", "fantasy")

        if not content:
            return {"error": "缺少 content 参数（章节内容）"}
        if chapter is None:
            chapter = self._infer_chapter()
            if chapter <= 0:
                chapter = 1

        # 1. 提取实体
        entity_names = []
        try:
            extractor = self._get_engine("entity_extractor")
            entities_result = extractor.execute_action("extract", {"text": content, "genre": genre})
            for entity_type in ["characters", "locations", "items"]:
                for e in entities_result.get(entity_type, []):
                    name = e.get("name", "") if isinstance(e, dict) else str(e)
                    if name:
                        entity_names.append(name)
        except Exception as e:
            entities_result = {"error": str(e)}

        # 2. 获取相关事实
        current_facts = []
        try:
            fe = self._get_engine("fact_engine")
            if entity_names:
                facts_result = fe.execute_action("relevant-facts", {
                    "chapter": int(chapter),
                    "entity": ",".join(entity_names),
                })
                current_facts = facts_result.get("facts", [])
            else:
                facts_result = fe.execute_action("relevant-facts", {
                    "chapter": int(chapter),
                })
                current_facts = facts_result.get("facts", [])
        except Exception as e:
            current_facts = []
            facts_result = {"error": str(e)}

        # 3. 构建对比结构
        facts_by_entity = {}
        for f in current_facts:
            ent = f.get("entity", "unknown")
            if ent not in facts_by_entity:
                facts_by_entity[ent] = []
            facts_by_entity[ent].append({
                "attribute": f.get("attribute"),
                "value": f.get("value"),
                "importance": f.get("importance"),
                "chapter": f.get("chapter"),
            })

        return {
            "chapter": int(chapter),
            "extracted_entities": entity_names,
            "current_facts_by_entity": facts_by_entity,
            "total_entities": len(entity_names),
            "total_facts": len(current_facts),
            "analysis_hint": (
                "对比章节内容与现有事实，识别三类变更: "
                "1)新事实 - 章节中出现但事实库无记录的实体/属性/值; "
                "2)更新事实 - 章节中同一属性值已变化(如境界提升、位置转移); "
                "3)冲突事实 - 章节内容与已有事实矛盾(如角色不可能同时出现在两地). "
                "对每类变更生成建议: set-fact录入新事实或更新事实, 并标注正确的importance."
            ),
        }

    def _help_output(self, args: Dict[str, Any] = None) -> Dict[str, Any]:
        """生成帮助信息"""
        detail_name = (args or {}).get("name", "")
        if detail_name:
            resolved = self.ALIAS_MAP.get(detail_name, detail_name)
            if resolved in self.COMMAND_MAP:
                info = self.COMMAND_MAP[resolved]
                return {"command": resolved, "action": info.get("action", ""),
                        "module": info.get("module", "")}
            return {"error": f"未找到指令: {detail_name}"}

        categories = {
            "系统": ["help", "status", "clear-chapter"],
            "规划": ["init", "import-settings", "preview-settings", "add-node", "add-edge", "create-character", "create-phase", "create-arc-am"],
            "创作": ["store-chapter", "store-scene", "store-summary", "extract-entities", "set-fact", "plant-hook", "for-creation", "chapter-complete", "detect-fact-changes"],
            "查询": ["get-fact", "get-facts", "search", "relevant-facts", "list-chars", "list-hooks", "list-arcs", "list-nodes"],
            "检查": ["check-continuity", "check-ooc", "audit", "overdue-hooks", "hook-stats", "detect-contradictions", "context-hierarchy", "budget-report"],
            "修改": ["analyze-revision", "set-fact", "resolve-hook", "abandon-hook", "abandon-chapter-hooks", "archive-facts", "supersede-chapter-facts", "complete-arc", "update-settings", "delete-settings", "delete-edge"],
            "分支": ["add-plot", "create-branch", "check-branches", "plot-timeline"],
            "风格": ["analyze-style", "compare-style", "char-prompt"],
            "管理": ["arc-progress", "suggest-next", "mem-stats", "kg-stats", "find-node", "find-path", "get-neighbors", "fact-history", "delete-chapter-scenes"],
        }
        return {"type": "help", "categories": categories, "total_commands": len(self.COMMAND_MAP)}
