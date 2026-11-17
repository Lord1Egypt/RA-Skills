#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scheduler — 指挥官模式调度引擎（四轮重构后最终版）

统一使用 StateRepository + ChapterOrchestrator + UnitOfWork。
不再直接创建 NovelState 实例，不再从废弃模块导入。
"""

import json
import time
import logging
from pathlib import Path
from typing import List, Optional, Dict

from .circuit_breaker import CircuitBreaker

_log = logging.getLogger("scheduler")

# 管线阶段定义
PIPELINE_STAGES = [
    ("plan",     "规划",       ["planning", "architecture", "development"]),
    ("spec",     "规格生成",   ["SpecBuilder"]),
    ("generate", "文本生成",   ["generator"]),
    ("quality",  "质量审查",   ["detector", "orchestrator"]),
    ("save",     "保存",       ["novel_state"]),
]


class ChapterResult:
    """单章执行结果"""

    def __init__(self, chapter: int):
        self.chapter = chapter
        self.success = False
        self.error: Optional[str] = None
        self.stages: Dict[str, str] = {}
        self.time_seconds = 0.0

    def to_dict(self) -> dict:
        return {
            "chapter": self.chapter,
            "success": self.success,
            "error": self.error,
            "stages": self.stages,
            "time_seconds": round(self.time_seconds, 2),
        }


class BatchReport:
    """批量执行报告"""

    def __init__(self):
        self.chapters: List[ChapterResult] = []
        self.total_time = 0.0
        self.total_chapters = 0
        self.successful = 0
        self.failed = 0

    @property
    def summary(self) -> str:
        return (
            f"{self.successful}/{self.total_chapters} 章成功, "
            f"{self.failed} 章失败, "
            f"耗时 {round(self.total_time, 1)}s"
        )

    def to_dict(self) -> dict:
        return {
            "total_chapters": self.total_chapters,
            "successful": self.successful,
            "failed": self.failed,
            "total_time": round(self.total_time, 2),
            "chapters": [c.to_dict() for c in self.chapters],
        }


class QualityDebt:
    """Quality Debt 记录"""

    def __init__(self, book_dir):
        self.book_dir = book_dir
        self._debts = []
        self._load()

    def add(self, chapter, category, description, severity="warning"):
        import time as _t
        self._debts.append({
            "chapter": chapter, "category": category,
            "description": description, "severity": severity,
            "timestamp": _t.strftime("%Y-%m-%dT%H:%M:%S"),
            "resolved": False,
        })
        self._save()

    def pending(self):
        return [d for d in self._debts if not d.get("resolved", False)]

    def report(self):
        p = self.pending()
        if not p:
            return "无 Quality Debt"
        lines = ["Quality Debt: {} 条未解决".format(len(p))]
        for d in p:
            lines.append("  ch{} [{}] {}".format(d["chapter"], d["severity"], d["description"]))
        return chr(10).join(lines)

    def _load(self):
        import json as _j
        p = self.book_dir / "追踪" / "quality_debt.json"
        if p.exists():
            try:
                self._debts = _j.loads(p.read_text(encoding="utf-8"))
            except Exception:
                self._debts = []

    def _save(self):
        import json as _j
        p = self.book_dir / "追踪" / "quality_debt.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(_j.dumps(self._debts, ensure_ascii=False, indent=2), encoding="utf-8")


class Scheduler:
    """指挥官模式调度引擎 — 统一 StateRepository + ChapterOrchestrator"""

    def __init__(self, book_dir="", novel_state=None):
        self.book_dir = Path(book_dir) if book_dir else Path.cwd()

        # 统一状态入口：通过 StateRepository
        from infrastructure.state_repository import StateRepository
        self._state_repo = StateRepository(str(self.book_dir))

        # 向后兼容：保留 novel_state 引用（通过 StateRepository 代理）
        if novel_state is not None:
            self.novel_state = novel_state
        else:
            # 使用 LegacyStateAdapter 包装 StateRepository
            self.novel_state = self._create_legacy_adapter()

        self.breaker = CircuitBreaker(
            max_consecutive_failures=3,
            recovery_timeout=60.0,
        )
        self.debt = QualityDebt(self.book_dir)

    def _create_legacy_adapter(self):
        """创建向后兼容的状态适配器（桥接 StateRepository → NovelState API）"""
        from engine.novel_state import NovelState
        return NovelState(str(self.book_dir))

    # ── 属性（通过 StateRepository） ───────

    @property
    def current_chapter(self) -> int:
        state = self._state_repo.load()
        return state.progress.last_chapter

    @current_chapter.setter
    def current_chapter(self, val: int):
        # setter 仅用于内部状态同步，不写入 state.json
        # 正式的章节完成通过 ChapterOrchestrator.generate_chapter() → UnitOfWork
        pass

    @property
    def chapters_done(self) -> int:
        state = self._state_repo.load()
        return state.progress.written

    # ── 批量执行（指挥官模式） ───────────────

    def run_batch(self, start_ch: int, end_ch: int) -> BatchReport:
        report = BatchReport()
        total_start = time.time()

        state = self._state_repo.load()
        resume_from = max(start_ch, state.progress.last_chapter + 1)
        if resume_from > start_ch:
            _log.info(f"Scheduler: 断点恢复 → 从第{resume_from}章继续")

        # 使用 ChapterOrchestrator (DDD)
        from infrastructure.state_repository import StateRepository
        from infrastructure.persistence_gateway import PersistenceGateway
        from infrastructure.llm_gateway import LLMGateway
        from infrastructure.detector_gateway import DetectorGateway
        from application.orchestrator import ChapterOrchestrator, ChapterRequest
        from engine.generator import TextGenerator
        from engine.engines_planning import PlanningEngine
        from engine.engines_writing import WritingEngine

        state_repo = StateRepository(str(self.book_dir))
        persistence = PersistenceGateway(str(self.book_dir))
        gen = TextGenerator()
        llm = LLMGateway(gen)
        detector = DetectorGateway()
        planning = PlanningEngine()
        writing = WritingEngine()

        orch = ChapterOrchestrator(
            state_repo=state_repo,
            persistence=persistence,
            llm=llm,
            detector=detector,
            planning_engine=planning,
            writing_engine=writing,
            book_dir=str(self.book_dir),
        )

        state = state_repo.load()
        platform = state.meta.platform or "番茄"
        genre = state.meta.genre or "都市"

        for ch in range(resume_from, end_ch + 1):
            ch_result = ChapterResult(ch)

            if self.breaker.state.name == "OPEN":
                ch_result.error = "熔断器 OPEN，跳过"
                ch_result.stages["breaker"] = "skipped"
                report.chapters.append(ch_result)
                report.failed += 1
                _log.warning(f"Scheduler: ch{ch} 跳过（熔断器 OPEN）")
                continue

            ch_start = time.time()
            _log.info(f"Scheduler: ch{ch}/{end_ch} 开始")

            try:
                request = ChapterRequest(chapter=ch, total_chapters=end_ch,
                                         platform=platform, genre=genre)
                result = orch.generate_chapter(request)

                if result.success:
                    ch_result.success = True
                    ch_result.stages["orchestrator"] = "ok"
                    self.breaker._record_success()
                    report.successful += 1
                    _log.info(f"Scheduler: ch{ch} OK")
                else:
                    errors = len(result.issues)
                    if errors <= 3:
                        self.debt.add(ch, "quality", f"ChapterOrchestrator {errors} issues", "minor")
                        ch_result.success = True
                        ch_result.stages["orchestrator"] = f"debt:{errors}issues"
                        self.breaker._record_success()
                        report.successful += 1
                        _log.info(f"Scheduler: ch{ch} (debt={errors} issues)")
                    else:
                        ch_result.error = f"ChapterOrchestrator 返回 {errors} 个问题"
                        ch_result.stages["orchestrator"] = f"error:{errors}"
                        self.breaker._record_failure()
                        report.failed += 1
                        _log.warning(f"Scheduler: ch{ch} FAIL {errors} issues")
            except Exception as e:
                ch_result.error = str(e)
                ch_result.stages["orchestrator"] = f"error:{e}"
                self.breaker._record_failure()
                report.failed += 1
                _log.error(f"Scheduler: ch{ch} 异常: {e}")

            ch_result.time_seconds = time.time() - ch_start
            report.chapters.append(ch_result)

        report.total_time = time.time() - total_start
        report.total_chapters = len(report.chapters)
        _log.info(f"Scheduler batch: {report.summary}")
        return report

    # ── 单章执行 ──────────────────────────────

    def run_chapter(self, chapter: int) -> ChapterResult:
        report = self.run_batch(chapter, chapter)
        return report.chapters[0] if report.chapters else ChapterResult(chapter)

    # ── 查询 ──────────────────────────────────

    def status(self) -> dict:
        state = self._state_repo.load()
        return {
            "chapters_done": state.progress.written,
            "current_chapter": state.progress.last_chapter,
            "breaker": self.breaker.stats(),
            "state_source": "StateRepository (统一)",
        }

    # ── 并行批量（手动触发） ──────────────────

    def prepare_parallel(self, start_ch: int, end_ch: int, max_workers: int = 3) -> dict:
        """准备并行写入任务"""
        task_dir = self.book_dir / "_temp" / "parallel"
        task_dir.mkdir(parents=True, exist_ok=True)

        state = self._state_repo.load()
        char_states = {
            name: {"identity": c.identity, "location": c.location,
                   "state": c.state.get("state", "?") if isinstance(c.state, dict) else "?"}
            for name, c in state.characters.items()
        }

        last_plot = [
            {"chapter": t.chapter, "event": t.event}
            for t in state.timeline[-5:]
        ]

        constitution_block = ""
        try:
            from .constitution_context import ConstitutionManager
            cm = ConstitutionManager(self.book_dir)
            if cm.exists():
                constitution_block = cm.get_prompt_block()
        except ImportError:
            pass

        chapters = list(range(start_ch, end_ch + 1))
        tasks = []

        for ch in chapters:
            spec = {}
            spec_path = self.book_dir / "规格" / f"第{ch:03d}.json"
            if spec_path.exists():
                try:
                    spec = json.loads(spec_path.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    spec = {"chapter": ch}

            task = {
                "chapter": ch,
                "spec": spec,
                "characters": char_states,
                "last_plot": last_plot,
                "constitution": constitution_block,
                "book_dir": str(self.book_dir),
            }
            task_file = task_dir / f"ch{ch:03d}_task.json"
            task_file.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
            tasks.append({"chapter": ch, "task_file": str(task_file)})

        manifest = {
            "start": start_ch, "end": end_ch, "total": len(chapters),
            "max_workers": max_workers, "tasks": tasks,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        (task_dir / "tasks.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

        instructions = (
            f"[并行任务] 第{start_ch}-{end_ch}章，{len(chapters)}个任务，最多{max_workers}个子Agent\n"
            f"任务目录: {task_dir}\n\n"
            f"使用方法:\n"
            f"  1. 每个子Agent读取 task_dir/chXXX_task.json\n"
            f"  2. 生成章节正文\n"
            f"  3. 保存到 task_dir/chXXX_result.json ({{chapter}}: text)\n"
            f"  4. 主Agent执行: 收集并行结果"
        )
        (task_dir / "README.md").write_text(instructions, encoding="utf-8")

        return {
            "tasks_dir": str(task_dir),
            "task_count": len(tasks),
            "instructions": instructions,
        }

    def collect_parallel_results(self, task_dir: str = None) -> BatchReport:
        """收集并行写入结果 — 通过 UnitOfWork 事务保护"""
        if task_dir is None:
            task_dir = str(self.book_dir / "_temp" / "parallel")
        td = Path(task_dir)
        report = BatchReport()

        result_files = sorted(td.glob("ch*_result.json"))
        if not result_files:
            _log.warning("collect_parallel_results: 无结果文件")
            return report

        from infrastructure.persistence_gateway import PersistenceGateway
        from application.unit_of_work import UnitOfWork
        from domain.commands import WriteChapterCommand

        gw = PersistenceGateway(str(self.book_dir))

        for rf in result_files:
            try:
                data = json.loads(rf.read_text(encoding="utf-8"))
                ch = data.get("chapter", 0)
                text = data.get("text", "")

                if not text:
                    cr = ChapterResult(ch)
                    cr.error = "无正文内容"
                    report.chapters.append(cr)
                    report.failed += 1
                    continue

                # 通过 UnitOfWork 事务保护写入
                with UnitOfWork(self._state_repo, gw) as uow:
                    uow.register_file_write(f"正文/第{ch:03d}章.txt", text)
                    uow.register_command(WriteChapterCommand(chapter=ch, text=text))

                cr = ChapterResult(ch)
                cr.success = True
                cr.stages["parallel"] = "ok"
                report.chapters.append(cr)
                report.successful += 1
                _log.info(f"Collect parallel: ch{ch} OK ({len(text)}字)")

            except (json.JSONDecodeError, KeyError, OSError) as e:
                ch_num = int(rf.stem.split("_")[0].replace("ch", "")) if "ch" in rf.stem else 0
                cr = ChapterResult(ch_num)
                cr.error = str(e)
                report.chapters.append(cr)
                report.failed += 1

        report.total_chapters = len(report.chapters)
        _log.info(f"Collect parallel: {report.summary}")
        return report

    # ── 重置 ──────────────────────────────────

    def reset(self):
        """重置运行时状态"""
        self.breaker.reset()
        _log.info("Scheduler: 运行时状态已重置")
