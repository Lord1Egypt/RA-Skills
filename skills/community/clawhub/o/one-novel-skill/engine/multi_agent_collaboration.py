#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
multi_agent_collaboration.py — 多智能体协作模式引擎

SKILL.md 声明功能：
- 串行：单个智能体顺序写作（中短篇）——已有 scheduler.py 支持
- 并行：多个子智能体并行写作（中长篇，速度优先）——新增
- 团队：协调者→架构师→写手→编辑（百万字史诗）——新增
- 团队模式角色：协调者(分配任务/追踪进度/解决冲突)、架构师(维护契约和一致性)、
  写手(按契约生成草稿)、编辑(执行质量审查)
"""

import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field

_log = logging.getLogger("multi_agent")


# ====== 角色定义 ======

@dataclass
class TeamRole:
    """团队角色"""
    role_id: str
    name: str
    responsibility: str
    required_skills: List[str]
    can_delegate_to: List[str] = field(default_factory=list)


TEAM_ROLES = {
    "coordinator": TeamRole(
        role_id="coordinator",
        name="协调者",
        responsibility="分配任务、追踪进度、解决角色间冲突、确保全局一致性",
        required_skills=["全局视野", "冲突解决", "进度管理"],
        can_delegate_to=["architect", "writer", "editor"],
    ),
    "architect": TeamRole(
        role_id="architect",
        name="架构师",
        responsibility="维护章节契约、世界观一致性、伏笔闭环、角色弧光连贯",
        required_skills=["世界观设计", "叙事结构", "角色发展"],
        can_delegate_to=["writer"],
    ),
    "writer": TeamRole(
        role_id="writer",
        name="写手",
        responsibility="按契约和架构师规范生成章节草稿",
        required_skills=["文字功底", "风格把控", "场景描写"],
        can_delegate_to=[],
    ),
    "editor": TeamRole(
        role_id="editor",
        name="编辑",
        responsibility="执行质量审查、AI检测、P0/P1检查、格式校验",
        required_skills=["文本分析", "质量把控", "规则执行"],
        can_delegate_to=["writer"],
    ),
}


# ====== 任务定义 ======

@dataclass
class AgentTask:
    """智能体任务"""
    task_id: str
    chapter: int
    assigned_role: str
    status: str = "pending"  # pending → assigned → running → completed | failed
    result: Any = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)  # 依赖的任务ID
    metadata: Dict = field(default_factory=dict)


@dataclass
class ChapterContract:
    """架构师维护的章节契约"""
    chapter: int
    required_beats: List[str] = field(default_factory=list)
    forbidden_moves: List[str] = field(default_factory=list)
    continuity_notes: List[str] = field(default_factory=list)
    character_states: Dict[str, str] = field(default_factory=dict)
    confirmed: bool = False


# ====== 协作模式 ======

class CollaborationMode:
    SERIAL = "serial"       # 串行：单智能体顺序
    PARALLEL = "parallel"   # 并行：多写手同时写作
    TEAM = "team"           # 团队：协调者→架构师→写手→编辑


class MultiAgentCollaborationEngine:
    """多智能体协作引擎 — 支持串行/并行/团队三种模式"""

    def __init__(self, book_dir: str = ""):
        self.book_dir = Path(book_dir) if book_dir else Path.cwd()
        self._mode = CollaborationMode.SERIAL
        self._roles = dict(TEAM_ROLES)
        self._tasks: Dict[str, AgentTask] = {}
        self._contracts: Dict[int, ChapterContract] = {}
        self._task_counter = 0
        self._progress_log: List[Dict] = []

    # ====== 模式设置 ======

    def set_mode(self, mode: str) -> bool:
        """设置协作模式"""
        if mode in (CollaborationMode.SERIAL, CollaborationMode.PARALLEL, CollaborationMode.TEAM):
            self._mode = mode
            _log.info(f"协作模式切换: {mode}")
            return True
        _log.warning(f"未知模式: {mode}，可用: serial/parallel/team")
        return False

    @property
    def mode(self) -> str:
        return self._mode

    def get_mode_description(self) -> str:
        descriptions = {
            CollaborationMode.SERIAL: "串行模式 — 单智能体顺序写作（适合中短篇）",
            CollaborationMode.PARALLEL: "并行模式 — 多写手同时写作（适合中长篇，速度优先）",
            CollaborationMode.TEAM: "团队模式 — 协调者→架构师→写手→编辑（适合百万字史诗）",
        }
        return descriptions.get(self._mode, "未知模式")

    # ====== 任务管理 ======

    def create_task(self, chapter: int, role: str = "writer",
                    dependencies: List[str] = None) -> AgentTask:
        """创建新任务"""
        self._task_counter += 1
        task_id = f"task_{self._task_counter:04d}"

        task = AgentTask(
            task_id=task_id,
            chapter=chapter,
            assigned_role=role,
            dependencies=dependencies or [],
        )
        self._tasks[task_id] = task
        return task

    def assign_task(self, task_id: str, role: str) -> bool:
        """将任务分配给指定角色"""
        task = self._tasks.get(task_id)
        if task is None:
            return False

        role_info = self._roles.get(role)
        if role_info is None:
            _log.warning(f"未知角色: {role}")
            return False

        task.assigned_role = role
        task.status = "assigned"
        _log.info(f"任务 {task_id} (第{task.chapter}章) 分配给 {role_info.name}")
        return True

    def start_task(self, task_id: str) -> bool:
        """标记任务开始执行"""
        task = self._tasks.get(task_id)
        if task is None or task.status not in ("assigned", "pending"):
            return False
        task.status = "running"
        task.started_at = datetime.now().isoformat()
        return True

    def complete_task(self, task_id: str, result: Any = None) -> bool:
        """标记任务完成"""
        task = self._tasks.get(task_id)
        if task is None:
            return False
        task.status = "completed"
        task.result = result
        task.completed_at = datetime.now().isoformat()
        _log.info(f"任务 {task_id} (第{task.chapter}章) 完成")
        return True

    def fail_task(self, task_id: str, error: str) -> bool:
        """标记任务失败"""
        task = self._tasks.get(task_id)
        if task is None:
            return False
        task.status = "failed"
        task.error = error
        task.completed_at = datetime.now().isoformat()
        _log.error(f"任务 {task_id} (第{task.chapter}章) 失败: {error}")
        return True

    def get_pending_tasks(self) -> List[AgentTask]:
        """获取待执行的任务（依赖已满足）"""
        completed_ids = {
            tid for tid, t in self._tasks.items()
            if t.status == "completed"
        }
        pending = []
        for task in self._tasks.values():
            if task.status not in ("pending", "assigned"):
                continue
            # 检查依赖是否全部满足
            if all(dep in completed_ids for dep in task.dependencies):
                pending.append(task)
        return pending

    def get_task_status_summary(self) -> Dict[str, int]:
        """获取任务状态摘要"""
        summary = {"pending": 0, "assigned": 0, "running": 0, "completed": 0, "failed": 0}
        for task in self._tasks.values():
            summary[task.status] = summary.get(task.status, 0) + 1
        return summary

    # ====== 契约管理（架构师职责） ======

    def create_contract(self, chapter: int, required_beats: List[str] = None,
                        forbidden_moves: List[str] = None,
                        continuity_notes: List[str] = None,
                        character_states: Dict[str, str] = None) -> ChapterContract:
        """架构师创建章节契约"""
        contract = ChapterContract(
            chapter=chapter,
            required_beats=required_beats or [],
            forbidden_moves=forbidden_moves or [],
            continuity_notes=continuity_notes or [],
            character_states=character_states or {},
        )
        self._contracts[chapter] = contract
        _log.info(f"架构师: 第{chapter}章契约已创建")
        return contract

    def confirm_contract(self, chapter: int) -> bool:
        """协调者确认契约"""
        contract = self._contracts.get(chapter)
        if contract is None:
            return False
        contract.confirmed = True
        _log.info(f"协调者: 第{chapter}章契约已确认")
        return True

    def get_contract(self, chapter: int) -> Optional[ChapterContract]:
        """获取章节契约"""
        return self._contracts.get(chapter)

    # ====== 进度追踪（协调者职责） ======

    def log_progress(self, role: str, action: str, chapter: int, detail: str = ""):
        """协调者记录进度"""
        self._progress_log.append({
            "role": role,
            "action": action,
            "chapter": chapter,
            "detail": detail,
            "time": datetime.now().isoformat(),
        })

    def get_progress_report(self) -> str:
        """协调者生成进度报告"""
        lines = [
            f"【{self.get_mode_description()} 进度报告】",
            f"",
            f"任务统计: {self.get_task_status_summary()}",
            f"",
            f"最近活动:",
        ]
        for entry in self._progress_log[-10:]:
            role_name = self._roles.get(entry["role"], TeamRole(entry["role"], entry["role"], "", [])).name
            lines.append(f"  [{role_name}] {entry['action']} (第{entry['chapter']}章) {entry['detail']}")
        return "\n".join(lines)

    # ====== 并行执行 ======

    def execute_parallel(self, chapters: List[int], writer_fn: Callable,
                         max_workers: int = 3) -> Dict[str, Any]:
        """并行模式：多写手同时写作多个章节

        Args:
            chapters: 要写的章节列表
            writer_fn: 写作函数，签名为 fn(chapter: int, contract: ChapterContract) -> str
            max_workers: 最大并行写手数
        """
        results = {"success": [], "failed": [], "tasks": {}}
        task_map = {}  # chapter → task_id

        # 1. 架构师创建所有契约
        for ch in chapters:
            self.create_contract(ch, required_beats=[f"完成第{ch}章核心情节"])

        # 2. 协调者确认契约并创建任务
        for ch in chapters:
            self.confirm_contract(ch)
            task = self.create_task(ch, role="writer")
            task_map[ch] = task.task_id

        # 3. 并行执行
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_chapter = {}
            for ch in chapters:
                contract = self.get_contract(ch)
                task_id = task_map[ch]
                self.start_task(task_id)
                future = executor.submit(self._safe_writer, writer_fn, ch, contract, task_id)
                future_to_chapter[future] = ch

            for future in as_completed(future_to_chapter):
                ch = future_to_chapter[future]
                try:
                    text = future.result()
                    if text and len(text) > 50:
                        self.complete_task(task_map[ch], {"text": text, "word_count": len(text)})
                        results["success"].append(ch)
                        self.log_progress("writer", "完成章节", ch, f"{len(text)}字")
                    else:
                        self.fail_task(task_map[ch], "生成的文本为空或太短")
                        results["failed"].append(ch)
                except Exception as e:
                    self.fail_task(task_map[ch], str(e))
                    results["failed"].append(ch)

        results["tasks"] = {
            tid: {"chapter": t.chapter, "status": t.status, "error": t.error}
            for tid, t in self._tasks.items() if t.chapter in chapters
        }

        return results

    def _safe_writer(self, writer_fn, chapter, contract, task_id):
        """安全的写手执行包装"""
        try:
            return writer_fn(chapter, contract)
        except Exception as e:
            _log.error(f"写手执行失败 (第{chapter}章): {e}")
            raise

    # ====== 团队模式 ======

    def execute_team(self, chapters: List[int],
                     architect_fn: Callable = None,
                     writer_fn: Callable = None,
                     editor_fn: Callable = None) -> Dict[str, Any]:
        """团队模式：协调者→架构师→写手→编辑

        Args:
            chapters: 要写的章节列表
            architect_fn: 架构师函数，签名为 fn(chapter: int) -> ChapterContract
            writer_fn: 写手函数，签名为 fn(chapter: int, contract: ChapterContract) -> str
            editor_fn: 编辑函数，签名为 fn(chapter: int, text: str) -> Dict(审查结果)
        """
        results = {"success": [], "failed": [], "editor_reports": {}}
        task_map = {}

        for ch in chapters:
            self.log_progress("coordinator", "开始处理章节", ch)

            # 1. 架构师：创建契约
            if architect_fn:
                try:
                    contract = architect_fn(ch)
                    if isinstance(contract, ChapterContract):
                        self._contracts[ch] = contract
                    else:
                        self.create_contract(ch)
                except Exception as e:
                    self.log_progress("architect", "契约创建失败", ch, str(e))
                    self.create_contract(ch)
            else:
                self.create_contract(ch)

            # 2. 协调者：确认契约
            self.confirm_contract(ch)
            contract = self.get_contract(ch)

            # 3. 写手：生成草稿
            task = self.create_task(ch, role="writer")
            task_map[ch] = task.task_id
            self.start_task(task.task_id)

            text = ""
            if writer_fn:
                try:
                    text = writer_fn(ch, contract)
                except Exception as e:
                    self.log_progress("writer", "写作失败", ch, str(e))

            if not text or len(text) < 50:
                self.fail_task(task.task_id, "写手生成失败")
                results["failed"].append(ch)
                self.log_progress("coordinator", "章节失败", ch, "写手输出为空")
                continue

            # 4. 编辑：审查
            editor_report = {"passed": True, "issues": []}
            if editor_fn:
                try:
                    editor_report = editor_fn(ch, text)
                except Exception as e:
                    self.log_progress("editor", "审查异常", ch, str(e))
                    editor_report = {"passed": False, "issues": [str(e)]}

            results["editor_reports"][ch] = editor_report

            # 5. 协调者：根据编辑结果决定
            if editor_report.get("passed", True):
                self.complete_task(task.task_id, {"text": text, "word_count": len(text)})
                results["success"].append(ch)
                self.log_progress("coordinator", "章节通过", ch,
                                 f"{len(text)}字, 编辑通过")
            else:
                # 编辑不通过：重新分配给写手修改（当前版本标记为失败）
                self.fail_task(task.task_id,
                              f"编辑不通过: {editor_report.get('issues', [])[:3]}")
                results["failed"].append(ch)
                self.log_progress("coordinator", "章节需修改", ch,
                                 f"问题数: {len(editor_report.get('issues', []))}")

        results["tasks"] = {
            tid: {"chapter": t.chapter, "status": t.status, "error": t.error}
            for tid, t in self._tasks.items() if t.chapter in chapters
        }

        return results

    # ====== 角色能力查询 ======

    def get_roles(self) -> Dict[str, Dict]:
        """获取所有角色定义"""
        return {
            rid: {
                "name": role.name,
                "responsibility": role.responsibility,
                "skills": role.required_skills,
                "can_delegate_to": [self._roles[r].name for r in role.can_delegate_to if r in self._roles],
            }
            for rid, role in self._roles.items()
        }

    def get_role_for_chapter_stage(self, stage: str) -> Optional[str]:
        """根据章节处理阶段获取对应角色"""
        stage_role_map = {
            "plan": "architect",
            "contract": "architect",
            "write": "writer",
            "review": "editor",
            "approve": "coordinator",
        }
        return stage_role_map.get(stage)

    # === 兼容 Engine 接口 ===

    def analyze(self, text: str = "", chapter: int = 1, **kwargs) -> Dict[str, Any]:
        """统一 analyze 接口（兼容 registry 规范）"""
        return {
            "verdict": "完成",
            "mode": self._mode,
            "mode_description": self.get_mode_description(),
            "task_summary": self.get_task_status_summary(),
            "contracts_count": len(self._contracts),
            "roles": list(self._roles.keys()),
        }
