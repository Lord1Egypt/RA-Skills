#!/usr/bin/env python3
"""
Hermes Agent - 技能自进化 (GEPA 算法)
将复杂执行经验自动提炼为"技能卡（Skill Card）"
多次处理同一类型任务后，自动总结出高效工作流，下次直接调用

隐私说明：
- 所有持久化行为受 hermes_config 控制
- 需显式设置 HERMES_PERSISTENCE_ENABLED=true 才会写磁盘
"""

import sqlite3
import json
import threading
import time
import hashlib
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, asdict
from collections import defaultdict

from hermes_config import hermes_config
import sys


def _log(msg: str):
    """受配置控制的日志输出"""
    level = hermes_config.session_fallback_log_level
    if level != "off":
        print(msg, file=sys.stderr if level == "summary" else sys.stdout)

@dataclass
class StepExecution:
    """单个执行步骤的记录"""
    step_name: str
    started_at: float
    finished_at: float
    success: bool
    result: Any
    error: Optional[str]

@dataclass
class TaskExecution:
    """一次完整任务执行记录"""
    execution_id: str
    task_type: str
    steps: List[StepExecution]
    input_params: Dict[str, Any]
    output_result: Any
    success: bool
    total_time: float
    created_at: float

@dataclass
class SkillCard:
    """提炼好的技能卡"""
    skill_id: str
    task_type: str
    name: str
    description: str
    steps: List[str]  # 推荐步骤顺序
    step_stats: Dict[str, Dict[str, float]]  # 每步统计：成功率、平均耗时
    success_rate: float  # 整体成功率
    avg_total_time: float  # 平均耗时
    invocation_count: int  # 被调用次数
    last_updated: float
    example_input: Dict[str, Any]
    confidence: float  # 提炼置信度 0-1

class GEPASkillEvolution:
    """
    GEPA (Generalized Execution Pattern Aggregation) 算法
    收集多次执行经验 → 提炼成功模式 → 生成技能卡 → 下次直接用

    惰性初始化：只有在 hermes_config.persistence_enabled=True 时才创建 DB 连接。
    """
    def __init__(self, db_path: str = "~/.hermes/skills.db",
                 min_success_samples: int = 2,
                 min_new_executions: int = 3,
                 max_refines_per_task: int = 10,
                 min_improvement: float = 0.05):
        self._db_path = db_path
        self.min_success_samples = min_success_samples
        self.min_new_executions = min_new_executions
        self.max_refines_per_task = max_refines_per_task
        self.min_improvement = min_improvement

        self._lock = threading.RLock()
        self._conn = None
        self._db_initialized = False
        self._skill_cache: Dict[str, SkillCard] = {}

    def _ensure_db(self) -> bool:
        """确保数据库已初始化，返回是否可用"""
        if not hermes_config.is_persistence_enabled():
            return False
        if self._conn is not None:
            return True
        if self._db_initialized:
            return True
        with self._lock:
            if self._db_initialized:
                return True
            import os
            db_path = os.path.expanduser(self._db_path)
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self._conn = sqlite3.connect(db_path, check_same_thread=False)
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA synchronous=NORMAL")
            self._init_tables()
            self._db_initialized = True
            return True

    def _get_conn(self):
        if not self._ensure_db():
            raise RuntimeError(
                "Hermes persistence is disabled. "
                "Set HERMES_PERSISTENCE_ENABLED=true or call hermes_config.set_persistence(True)"
            )
        return self._conn

    def _init_tables(self):
        cursor = self._conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS executions (
                execution_id TEXT PRIMARY KEY,
                task_type TEXT NOT NULL,
                execution_json TEXT NOT NULL,
                created_at REAL NOT NULL,
                success INTEGER NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skill_cards (
                skill_id TEXT PRIMARY KEY,
                task_type TEXT NOT NULL,
                name TEXT,
                description TEXT,
                skill_json TEXT NOT NULL,
                created_at REAL NOT NULL,
                last_updated REAL NOT NULL,
                invocation_count INTEGER NOT NULL,
                success_rate REAL NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_executions_type ON executions(task_type);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_skill_task ON skill_cards(task_type);")
        self._conn.commit()

    def record_execution(self, execution: TaskExecution) -> str:
        """记录一次任务执行（受持久化开关控制）"""
        if not hermes_config.is_persistence_enabled():
            return execution.execution_id
        if not self._ensure_db():
            return execution.execution_id
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("""
                INSERT INTO executions (execution_id, task_type, execution_json, created_at, success)
                VALUES (?, ?, ?, ?, ?)
            """, (
                execution.execution_id,
                execution.task_type,
                json.dumps(asdict(execution)),
                execution.created_at,
                1 if execution.success else 0
            ))
            self._conn.commit()

        self._try_evolve_skill(execution.task_type)
        return execution.execution_id

    def get_executions_for_task(self, task_type: str, limit: int = 100) -> List[TaskExecution]:
        """获取某个任务类型的所有执行记录"""
        if not hermes_config.is_persistence_enabled():
            return []
        if not self._ensure_db():
            return []
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT execution_json FROM executions
                WHERE task_type = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (task_type, limit))

            results = []
            for row in cursor.fetchall():
                data = json.loads(row[0])
                results.append(TaskExecution(**data))
            return results

    def _hash_id(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()[:12]

    def _try_evolve_skill(self, task_type: str):
        """尝试从执行记录提炼技能卡
        智能控制：只在合适时机提炼，避免疯狂提炼浪费 token
        """
        executions = self.get_executions_for_task(task_type, limit=50)

        existing = self.get_skill_card(task_type)
        total_exec = len(executions)
        successful_exec = sum(1 for e in executions if e.success)

        # 提炼控制策略：
        if existing:
            # 1. 估算提炼次数 (利用当前执行总样本次数/提取步长)
            if (total_exec / max(1, self.min_new_executions)) >= self.max_refines_per_task:
                return  # 达到上限，不再提炼
            # 2. 检查新增样本数
            new_executions = total_exec - existing.invocation_count
            if new_executions < self.min_new_executions:
                return  # 新增太少，不提炼
            # 3. 检查是否有明显改进
            new_success_rate = successful_exec / total_exec
            if abs(new_success_rate - existing.success_rate) < self.min_improvement:
                return  # 变化太小，不需要重新提炼

        if successful_exec < self.min_success_samples:
            return  # 成功样本太少，不提炼

        # GEPA 核心算法：
        # 1. 统计每个步骤的出现频率、成功率、平均耗时
        # 2. 找出成功路径中最常见的步骤顺序
        # 3. 生成技能卡

        step_stats = defaultdict(lambda: {
            "count": 0,
            "success_count": 0,
            "total_time": 0.0
        })
        common_order: List[Tuple[str, int]] = []
        successful_executions = [e for e in executions if e.success]

        if len(successful_executions) == 0:
            return

        # 统计步骤
        for exec in successful_executions:
            for step in exec.steps:
                # exec 是从 JSON 反序列化来的，step 已经是 dict
                step_name = step["step_name"] if isinstance(step, dict) else step.step_name
                success = step["success"] if isinstance(step, dict) else step.success
                finished_at = step["finished_at"] if isinstance(step, dict) else step.finished_at
                started_at = step["started_at"] if isinstance(step, dict) else step.started_at
                step_stats[step_name]["count"] += 1
                step_stats[step_name]["success_count"] += 1 if success else 0
                step_stats[step_name]["total_time"] += (finished_at - started_at)

        # 按出现频率排序，得到推荐步骤顺序
        all_steps = list(step_stats.items())
        all_steps.sort(key=lambda x: x[1]["count"], reverse=True)
        recommended_steps = [name for name, _ in all_steps]

        # 计算整体成功率
        total_success = sum(1 for e in executions if e.success)
        success_rate = total_success / len(executions)

        # 平均总时间
        avg_time = sum(e.total_time for e in successful_executions) / len(successful_executions)

        # 构建技能卡统计信息
        step_final_stats = {}
        for name, stats in step_stats.items():
            step_final_stats[name] = {
                "success_rate": stats["success_count"] / stats["count"],
                "avg_time_ms": (stats["total_time"] / stats["count"]) * 1000,
                "occurrences": stats["count"]
            }

        # 获取一个示例输入
        example_input = successful_executions[-1].input_params

        # 生成技能卡
        skill_id = self._hash_id(task_type)
        skill = SkillCard(
            skill_id=skill_id,
            task_type=task_type,
            name=f"{task_type} - auto generated",
            description=f"Automatically evolved from {len(successful_executions)} successful executions",
            steps=recommended_steps,
            step_stats=step_final_stats,
            success_rate=success_rate,
            avg_total_time=avg_time,
            invocation_count=len(executions),
            last_updated=time.time(),
            example_input=example_input,
            confidence=success_rate * 0.8  # 置信度 = 成功率 × 经验系数
        )

        # 保存到数据库
        with self._lock:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                REPLACE INTO skill_cards
                (skill_id, task_type, name, description, skill_json, created_at, last_updated, invocation_count, success_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                skill.skill_id,
                skill.task_type,
                skill.name,
                skill.description,
                json.dumps(asdict(skill)),
                skill.last_updated - (len(executions) * 3600),  # 近似创建时间
                skill.last_updated,
                skill.invocation_count,
                skill.success_rate
            ))
            conn.commit()

        # 更新缓存
        self._skill_cache[skill_id] = skill

        _log(f"🧬 GEPA: 从 {len(successful_executions)} 次成功执行提炼出技能卡: {skill_id} ({task_type})")

    def get_skill_card(self, task_type: str) -> Optional[SkillCard]:
        """获取某个任务类型的最新技能卡"""
        for skill in self._skill_cache.values():
            if skill.task_type == task_type:
                return skill

        if not hermes_config.is_persistence_enabled():
            return None
        if not self._ensure_db():
            return None
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT skill_json FROM skill_cards
                WHERE task_type = ?
                ORDER BY last_updated DESC
                LIMIT 1
            """, (task_type,))
            row = cursor.fetchone()
            if row:
                data = json.loads(row[0])
                skill = SkillCard(**data)
                self._skill_cache[skill.skill_id] = skill
                return skill
        return None

    def list_skill_cards(self) -> List[SkillCard]:
        """列出所有技能卡"""
        results = [s for s in self._skill_cache.values()]
        if not hermes_config.is_persistence_enabled():
            return results
        if not self._ensure_db():
            return results
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT skill_json FROM skill_cards
                ORDER BY last_updated DESC
            """)
            for row in cursor.fetchall():
                data = json.loads(row[0])
                card = SkillCard(**data)
                if card.skill_id not in {s.skill_id for s in results}:
                    results.append(card)
            return results

    def get_recommended_workflow(self, task_type: str) -> Optional[List[str]]:
        """获取推荐工作流（提炼后的步骤顺序）"""
        card = self.get_skill_card(task_type)
        if card:
            return card.steps
        return None

    def record_invocation(self, skill_id: str):
        """记录技能卡被调用"""
        if not hermes_config.is_persistence_enabled():
            return
        if not self._ensure_db():
            return
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("""
                UPDATE skill_cards
                SET invocation_count = invocation_count + 1
                WHERE skill_id = ?
            """, (skill_id,))
            self._conn.commit()

    def stats(self):
        """统计"""
        if not hermes_config.is_persistence_enabled():
            return {"total_executions": 0, "total_skill_cards": len(self._skill_cache), "total_invocations": 0}
        if not self._ensure_db():
            return {"total_executions": 0, "total_skill_cards": len(self._skill_cache), "total_invocations": 0}
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM executions")
            exec_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM skill_cards")
            skill_count = cursor.fetchone()[0]
            cursor.execute("SELECT SUM(invocation_count) FROM skill_cards")
            total_invokes = cursor.fetchone()[0] or 0
            return {
                "total_executions": exec_count,
                "total_skill_cards": skill_count,
                "total_invocations": total_invokes
            }

# === 便捷的高阶 API ===

class HermesSkillExecutor:
    """
    带自进化能力的技能执行器
    你只要执行任务，它自动记录、自动进化
    """
    def __init__(self):
        self.gepa = GEPASkillEvolution()
        self._current_execution: Optional[TaskExecution] = None
        self._current_steps: List[StepExecution] = []

    def start_task(self, task_type: str, input_params: Dict[str, Any]) -> str:
        """开始一个新任务"""
        import uuid
        execution_id = str(uuid.uuid4())[:8]
        self._current_execution = TaskExecution(
            execution_id=execution_id,
            task_type=task_type,
            steps=[],
            input_params=input_params,
            output_result=None,
            success=False,
            total_time=0,
            created_at=time.time()
        )
        self._current_steps = []
        return execution_id

    def step(self, step_name: str, func: Callable, *args, **kwargs) -> Any:
        """执行一步，自动记录"""
        start = time.time()
        step_record = StepExecution(
            step_name=step_name,
            started_at=start,
            finished_at=0,
            success=False,
            result=None,
            error=None
        )

        try:
            result = func(*args, **kwargs)
            step_record.success = True
            step_record.result = result
            return result
        except Exception as e:
            step_record.success = False
            step_record.error = str(e)
            raise
        finally:
            step_record.finished_at = time.time()
            self._current_steps.append(step_record)

    def finish_task(self, success: bool, result: Any) -> str:
        """完成任务，自动记录并触发进化"""
        if self._current_execution is None:
            return ""

        self._current_execution.steps = self._current_steps
        self._current_execution.output_result = result
        self._current_execution.success = success
        self._current_execution.total_time = time.time() - self._current_execution.created_at

        exec_id = self.gepa.record_execution(self._current_execution)
        self._current_execution = None
        self._current_steps = []
        return exec_id

    def get_skill_for_task(self, task_type: str) -> Optional[SkillCard]:
        """获取已经进化好的技能卡"""
        return self.gepa.get_skill_card(task_type)

# === 全局实例 ===

hermes_gepa = GEPASkillEvolution()
hermes_skill_executor = HermesSkillExecutor()

# === 演示 ===

if __name__ == "__main__":
    print("🧬 Hermes Agent - 技能自进化 (GEPA 算法)")
    print("=" * 60)

    print("当前持久化状态:", hermes_config.is_persistence_enabled())

    executor = HermesSkillExecutor()

    # 模拟第一次处理视频剪辑
    print("\n🎬 第一次处理视频剪辑任务...")
    exec_id = executor.start_task("video-clip", {
        "input_path": "input.mp4",
        "output_path": "output.mp4",
        "start_time": 10,
        "end_time": 20
    })

    # 步骤 1: 加载视频
    def mock_load():
        time.sleep(0.1)
        return "video-loaded"
    executor.step("load-video", mock_load)

    # 步骤 2: 剪切片段
    def mock_cut(start, end):
        time.sleep(0.15)
        return f"cut-{start}-{end}"
    executor.step("cut-segment", mock_cut, 10, 20)

    # 步骤 3: 导出
    def mock_export():
        time.sleep(0.2)
        return "done"
    executor.step("export-video", mock_export)

    executor.finish_task(True, {"output": "output.mp4"})

    # 第二次
    print("🎬 第二次处理视频剪辑任务...")
    exec_id = executor.start_task("video-clip", {
        "input_path": "input2.mp4",
        "output_path": "output2.mp4",
        "start_time": 5,
        "end_time": 15
    })
    executor.step("load-video", mock_load)
    executor.step("cut-segment", mock_cut, 5, 15)
    executor.step("export-video", mock_export)
    executor.finish_task(True, {"output": "output2.mp4"})

    # 看结果
    print("\n📊 GEPA 提炼完成，技能卡统计:")
    print(json.dumps(hermes_gepa.stats(), indent=2))

    skill = hermes_gepa.get_skill_card("video-clip")
    if skill:
        print(f"\n✅ 自动提炼出技能卡:")
        print(f"   任务类型: {skill.task_type}")
        print(f"   成功率: {skill.success_rate:.1%}")
        print(f"   平均耗时: {skill.avg_total_time*1000:.1f} ms")
        print(f"   推荐步骤: {skill.steps}")
        print(f"   调用次数: {skill.invocation_count}")

    print("\n🎉 GEPA 技能自进化就绪！")
    print()
    print("""现在 Hermes 能做到：
1. 你每次执行任务 → 自动记录每一步
2. 多次成功后 → GEPA 自动提炼出技能卡
3. 下次再做 → 直接用提炼好的工作流
4. 越用越准，成功率越高，步骤越顺

就是说：你教它几次，它就学会了，变成自己的技能。
""")
