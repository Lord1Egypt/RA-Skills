"""
orchestrator_v4_acp.py - 主控，使用 ACP spawn 子 agent 作为 Worker

核心设计：
- Fast 任务 → 当前会话直接回答（控制上下文）
- Slow 任务 → sessions_spawn 子 agent（隔离上下文）
- Long 任务 → V3 Bridge 子进程（双向心跳，>30分钟）
- 历史记录按 token 截断
- 中间结果强制摘要
- 集成：生命周期管理 / 后台监控 / 微调度器 / V3桥接
"""

import asyncio
import uuid
import time
import json
import logging
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from typing import Dict, List, Optional, Callable, Any, AsyncIterator, Awaitable
from pathlib import Path

# === 可选模块（向后兼容，导入失败自动降级） ===
_HAS_AUDIT = False
_HAS_LIFECYCLE = False
_HAS_MONITOR = False
_HAS_SCHEDULER = False
_HAS_V3_BRIDGE = False
_HAS_HYBRID_WORKER = False

logger = logging.getLogger(__name__)


class TaskDuration(Enum):
    """任务时长估计"""
    SHORT = "short"    # < 1分钟
    MEDIUM = "medium"  # 1-30分钟
    LONG = "long"      # > 30分钟


class SessionState(Enum):
    """会话状态"""
    IDLE = auto()
    ACTIVE = auto()
    PAUSED = auto()
    SHUTTING_DOWN = auto()
    ERROR = auto()


class WorkerMode(Enum):
    """Worker 模式"""
    FAST = "fast"
    SLOW = "slow"
    AUTO = "auto"


@dataclass
class OrchestratorConfig:
    """编排器配置"""
    # Worker
    default_worker_mode: WorkerMode = WorkerMode.AUTO
    fast_timeout: float = 60.0
    slow_timeout: float = 300.0
    complex_slow_timeout: float = 600.0  # 复杂 slow 任务（需要读多文件/大改动）
    subagent_agent_id: str = "main"
    subagent_model: str = ""
    subagent_thinking: str = "off"
    subagent_cleanup: str = "delete"
    subagent_sandbox: str = "inherit"
    max_parallel_subagents: int = 3  # 最大并行 subagent 数

    # 上下文控制（关键！）
    max_history_tokens: int = 2000      # 历史记录最大 token
    max_result_tokens: int = 500        # 单结果最大 token
    max_file_context_tokens: int = 1000 # 文件上下文最大 token
    summary_threshold: int = 300        # 超过此长度强制摘要

    # 会话
    session_timeout_sec: float = 3600.0
    task_timeout_sec: float = 300.0
    max_task_chain_length: int = 3      # 任务链最大长度

    # 持久化
    checkpoint_dir: str = "./checkpoints"
    auto_checkpoint: bool = True
    checkpoint_interval_sec: float = 60.0
    resume_from_latest_checkpoint: bool = True
    latest_checkpoint_name: str = "checkpoint_latest.json"

    # 监控
    enable_health_check: bool = True
    health_check_interval_sec: float = 30.0

    # === 新模块配置 ===
    # 生命周期管理
    enable_lifecycle_manager: bool = True
    restart_policy: str = "on_failure"  # never / on_failure / always
    max_restarts: int = 3
    restart_window_sec: float = 60.0

    # 后台监控
    enable_background_monitor: bool = True
    monitor_check_interval: float = 5.0
    monitor_heartbeat_timeout: float = 30.0

    # 微调度器
    enable_micro_scheduler: bool = False  # 默认关闭，多任务时显式开启
    scheduler_max_concurrent: int = 3

    # V3 桥接 / 长任务
    enable_v3_bridge: bool = False  # 默认关闭
    v3_bridge_heartbeat_interval: float = 5.0
    long_task_threshold_sec: float = 1800.0  # 30分钟
    long_task_keywords: List[str] = field(default_factory=lambda: [
        "监控", "扫描", "渗透测试", "train", "long running",
        "部署", "迁移", "全量", "批量处理", "数据导入"
    ])

    # 审计子代理
    enable_audit: bool = False  # 默认关闭，显式开启
    audit_on_code_tasks: bool = True  # 代码类任务自动审计
    audit_timeout: float = 120.0  # 审计超时（秒）
    audit_max_retries: int = 3  # 审计 REJECT 后最大重试次数
    
    # 任务预规划（自动拆分大任务给子代理）
    enable_task_planning: bool = True
    max_subtask_complexity: int = 3   # 单个子任务最大复杂度，超过则拆
    max_files_per_subtask: int = 2    # 每个子任务最多读的文件数（代码生成类）
    analysis_max_files_per_subtask: int = 8  # 分析类任务每个子任务最多读的文件数
    subtask_timeout: float = 300.0    # 单个子任务超时（秒）
    
    # 大项目分析策略（v4.1）
    large_project_file_threshold: int = 50     # 超过此文件数启用模块拆分
    large_project_line_threshold: int = 5000   # 超过此行数启用模块拆分
    analysis_timeout_small: float = 300.0   # 小模块超时（<20文件）
    analysis_timeout_medium: float = 480.0  # 中模块超时（20-50文件）
    analysis_timeout_large: float = 600.0   # 大模块超时（>50文件）
    analysis_file_read_cap_small: int = 10  # 小模块文件读取上限
    analysis_file_read_cap_medium: int = 15 # 中模块文件读取上限
    analysis_file_read_cap_large: int = 20  # 大模块文件读取上限
    retry_shrink_factor: float = 0.5  # 超时重试时范围缩小比例

    # 日志
    log_level: str = "INFO"
    log_file: Optional[str] = "orchestrator.log"


@dataclass
class UserRequest:
    """用户请求"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    content: str = ""
    request_type: str = "general"
    mode: WorkerMode = WorkerMode.AUTO
    priority: str = "normal"
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)


@dataclass
class OrchestratorResponse:
    """编排器响应"""
    request_id: str = ""
    content: str = ""
    worker_mode: str = ""
    task_count: int = 0
    execution_time_sec: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


def estimate_tokens(text: str) -> int:
    """估算文本 token 数（粗略估计：1 token ≈ 4 字符）"""
    return len(text) // 4


def truncate_by_tokens(text: str, max_tokens: int) -> str:
    """按 token 截断文本"""
    max_chars = max_tokens * 4
    if len(text) <= max_chars:
        return text
    return text[:max_chars - 20] + "... [truncated]"


class ContextManager:
    """上下文管理器 - 控制 token 使用"""

    def __init__(self, config: OrchestratorConfig):
        self.config = config
        self._history: List[Dict] = []
        self._current_tokens = 0

    def add_exchange(self, user_msg: str, assistant_msg: str):
        """添加一轮对话"""
        exchange = {
            "role_user": user_msg[:200],  # 限制单条长度
            "role_assistant": assistant_msg[:500],
            "timestamp": time.time()
        }
        self._history.append(exchange)

        # 如果超出 token 限制，移除最旧的
        while self._estimate_total_tokens() > self.config.max_history_tokens and len(self._history) > 1:
            self._history.pop(0)

    def _estimate_total_tokens(self) -> int:
        """估算总 token"""
        total = 0
        for h in self._history:
            total += estimate_tokens(h.get("role_user", ""))
            total += estimate_tokens(h.get("role_assistant", ""))
        return total

    def get_formatted_history(self, max_entries: int = 5) -> List[Dict]:
        """获取格式化的历史记录（用于 prompt）"""
        recent = self._history[-max_entries:]
        formatted = []
        for h in recent:
            formatted.append({"role": "user", "content": h["role_user"]})
            formatted.append({"role": "assistant", "content": h["role_assistant"]})
        return formatted

    def clear(self):
        """清空历史"""
        self._history.clear()


class OrchestratorV4ACP:
    """v4 主控编排器 - ACP 版本（带上下文控制）"""

    def __init__(self, config: Optional[OrchestratorConfig] = None, spawn_func: Optional[Callable[..., Awaitable[Any]]] = None):
        self.config = config or OrchestratorConfig()
        self.state = SessionState.IDLE
        self._spawn_func = spawn_func

        # 上下文管理
        self.context_manager = ContextManager(self.config)

        # 会话管理
        self._session_id = str(uuid.uuid4())[:8]
        self._request_context: Dict[str, Any] = {}
        self._last_activity = time.time()

        # 运行时
        self._main_loop: Optional[asyncio.Task] = None
        self._checkpoint_task: Optional[asyncio.Task] = None
        self._shutdown = False
        self._paused = False  # 暂停标志，阻止新 subagent 创建
        self._redirect_instructions: Optional[str] = None  # 新指令，用于暂停后改变任务方向

        # 回调
        self._on_response: Optional[Callable[[OrchestratorResponse], None]] = None
        self._on_error: Optional[Callable[[Exception, str], None]] = None

        # 统计
        self._stats = {
            "fast_tasks": 0,
            "slow_tasks": 0,
            "long_tasks": 0,
            "spawned_agents": 0,
            "total_tokens_saved": 0
        }

        # subagent 并发控制
        self._spawn_semaphore = asyncio.Semaphore(self.config.max_parallel_subagents)

        # 任务追踪器（进度感知）
        self._active_tasks: Dict[str, Dict[str, Any]] = {}  # label → {status, task_desc, session_key, started_at, completed_at}
        self._task_counter = {"total": 0, "completed": 0, "failed": 0, "running": 0, "paused": 0}

        # === 新模块初始化（向后兼容） ===
        # 生命周期管理器
        self._lifecycle: Optional[Any] = None
        if self.config.enable_lifecycle_manager and _HAS_LIFECYCLE:
            policy_map = {"never": RestartPolicy.NEVER, "on_failure": RestartPolicy.ON_FAILURE, "always": RestartPolicy.ALWAYS}
            policy = policy_map.get(self.config.restart_policy, RestartPolicy.ON_FAILURE)
            self._lifecycle = ProcessLifecycleManager(
                default_restart_policy=policy,
                default_max_restarts=self.config.max_restarts,
                default_restart_window_sec=self.config.restart_window_sec,
            )
            logger.info("生命周期管理器已初始化")

        # 后台监控器
        self._monitor: Optional[Any] = None
        if self.config.enable_background_monitor and _HAS_MONITOR:
            self._monitor = BackgroundMonitor(
                check_interval=self.config.monitor_check_interval,
            )
            logger.info("后台监控器已初始化")

        # 微调度器（按需创建，不常驻）
        self._scheduler_enabled = self.config.enable_micro_scheduler and _HAS_SCHEDULER

        # V3 桥接（按需创建）
        self._v3_bridge_enabled = self.config.enable_v3_bridge and _HAS_V3_BRIDGE

        # 审计子代理
        self._audit_enabled = self.config.enable_audit and _HAS_AUDIT
        if self._audit_enabled:
            logger.info("审计子代理已启用")

        # Hybrid Worker（统一 Fast/Slow 执行）
        self._hybrid_worker = None
        if _HAS_HYBRID_WORKER:
            worker_config = ACPWorkerConfig()  # 使用默认配置
            self._hybrid_worker = HybridWorkerACP(config=worker_config)
            logger.info("HybridWorker 已初始化")

        # 确保目录存在
        Path(self.config.checkpoint_dir).mkdir(parents=True, exist_ok=True)

    async def start(self):
        """启动编排器"""
        if self.config.resume_from_latest_checkpoint:
            self._load_latest_checkpoint()

        self.state = SessionState.ACTIVE

        if self.config.enable_health_check:
            self._main_loop = asyncio.create_task(self._health_check_loop())

        if self.config.auto_checkpoint:
            self._checkpoint_task = asyncio.create_task(self._checkpoint_loop())

        # 启动后台监控器
        if self._monitor:
            await self._monitor.start()

        self._log("info", f"OrchestratorV4ACP started (session={self._session_id})")

    async def stop(self, graceful: bool = True):
        """停止编排器"""
        self.state = SessionState.SHUTTING_DOWN
        self._shutdown = True

        for task in [self._main_loop, self._checkpoint_task]:
            if task:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        # 停止后台监控器
        if self._monitor:
            await self._monitor.stop()

        await self._save_checkpoint("final")
        self.state = SessionState.IDLE
        self._log("info", "OrchestratorV4ACP stopped")

    def pause(self):
        self.state = SessionState.PAUSED

    def resume(self):
        self.state = SessionState.ACTIVE

    def redirect(self, new_instructions: str):
        """
        用户在暂停期间调用，传入新的指令/思路
        把新指令存到 self._redirect_instructions，恢复后将按新思路执行
        """
        self._redirect_instructions = new_instructions
        self._log("info", "收到新指令，将在恢复后按新思路执行")

    def resume_with_redirect(self) -> Optional[str]:
        """
        恢复暂停状态，如果有新指令则清空当前 running 任务并返回新指令

        Returns:
            如果有新指令，返回新指令内容；否则返回 None（正常恢复）
        """
        self._paused = False
        self.state = SessionState.ACTIVE

        if self._redirect_instructions:
            # 清空当前 _active_tasks 中所有 running 状态的任务
            for label, task_info in list(self._active_tasks.items()):
                if task_info.get("status") == "running":
                    task_info["status"] = "cancelled"
                    task_info["completed_at"] = time.time()
                    self._task_counter["running"] = max(0, self._task_counter["running"] - 1)

            # 更新 _task_counter，确保状态一致性
            self._task_counter["running"] = sum(
                1 for t in self._active_tasks.values() if t.get("status") == "running"
            )

            instructions = self._redirect_instructions
            self._redirect_instructions = None  # 清空已处理的新指令
            self._log("info", f"按新思路恢复，已取消 {len([t for t in self._active_tasks.values() if t.get('status') == 'cancelled'])} 个运行中任务")
            return instructions

        return None

    def get_redirect_status(self) -> Dict[str, Any]:
        """
        获取重定向状态

        Returns:
            {"has_redirect": bool, "instructions": str or None}
        """
        return {
            "has_redirect": self._redirect_instructions is not None,
            "instructions": self._redirect_instructions
        }

    def pause_all(self) -> List[Dict[str, Any]]:
        """暂停编排器：阻止新的 subagent 创建，但不杀死已运行的 subagent"""
        self._paused = True
        self.state = SessionState.PAUSED
        self._log("info", "编排器已暂停，新的 subagent 创建将被阻止")
        # 收集当前 running 的任务列表
        running_tasks = [
            {"label": label, **info}
            for label, info in self._active_tasks.items()
            if info.get("status") in ("running", "spawning")
        ]
        return running_tasks

    def resume_all(self):
        """恢复编排器：允许新的 subagent 创建"""
        self._paused = False
        self.state = SessionState.ACTIVE
        self._log("info", "编排器已恢复，可以继续创建 subagent")

    def stop_all(self):
        """停止编排器：标记关闭状态并取消所有活跃任务"""
        self._shutdown = True
        self.state = SessionState.SHUTTING_DOWN
        cancelled_labels = []
        for label, info in list(self._active_tasks.items()):
            if info.get("status") in ("running", "spawning", "paused"):
                self._active_tasks[label]["status"] = "cancelled"
                self._active_tasks[label]["completed_at"] = time.time()
                cancelled_labels.append(label)
                # 减少 running 计数
                if info.get("status") in ("running", "spawning"):
                    self._task_counter["running"] = max(0, self._task_counter["running"] - 1)
        self._log("info", f"编排器已停止，共取消 {len(cancelled_labels)} 个活跃任务: {cancelled_labels}")

    def get_control_status(self) -> Dict[str, Any]:
        """获取控制状态"""
        return {
            "paused": self._paused,
            "shutdown": self._shutdown,
            "active_count": self._task_counter["running"],
            "can_spawn": not self._paused and not self._shutdown,
        }

    async def handle(self, content: str, **kwargs) -> OrchestratorResponse:
        """处理用户请求的主入口"""
        mode = kwargs.get("mode", "auto")
        if isinstance(mode, str):
            mode = WorkerMode(mode)

        request = UserRequest(
            content=content,
            request_type=kwargs.get("request_type", "general"),
            mode=mode,
            priority=kwargs.get("priority", "normal"),
            context=kwargs.get("context", {})
        )

        start_time = time.time()
        self._last_activity = start_time

        try:
            # 分析请求
            task_plan = await self._analyze_request(request)

            # 检查任务链长度
            if len(task_plan) > self.config.max_task_chain_length:
                self._log("warning", f"Task chain too long ({len(task_plan)}), truncating to {self.config.max_task_chain_length}")
                task_plan = task_plan[:self.config.max_task_chain_length]

            # 执行任务
            if len(task_plan) == 1:
                result = await self._execute_single_task(request, task_plan[0])
            else:
                result = await self._execute_task_plan(request, task_plan)

            # 截断结果
            result = truncate_by_tokens(result, self.config.max_result_tokens)

            # 审计检查（仅对代码类任务或显式开启时）
            # 审计结果内部消化，不暴露给用户
            audit_result = None
            audit_retries = 0
            if self._audit_enabled and self.config.audit_on_code_tasks and request.request_type in ("code", "debug"):
                # 审计循环重试机制
                for retry in range(self.config.audit_max_retries + 1):
                    audit_result = await self._run_audit(
                        task_description=content,
                        result=result,
                    )
                    if audit_result.get("status") == "PASS":
                        if retry > 0:
                            self._log("info", f"审计在第 {retry} 次重试后通过")
                        break
                    elif audit_result.get("status") == "REJECT":
                        if retry < self.config.audit_max_retries:
                            audit_retries += 1
                            self._log("warning", f"审计 REJECT，第 {retry + 1} 次重试: {audit_result.get('reason', '')[:200]}")
                            # 把审计反馈塞进 task 内容让 worker 重做
                            retry_content = f"{content}\n\n[审计反馈，请修正以下问题]\n{audit_result.get('reason', '')}"
                            result = await self._execute_single_task(
                                request,
                                {**task_plan[0], "content": retry_content} if len(task_plan) == 1 else task_plan[0]
                            )
                            result = truncate_by_tokens(result, self.config.max_result_tokens)
                        else:
                            # 达到最大重试次数，内部消化，不标记审计信息
                            self._log("warning", f"审计循环结束，最终仍为 REJECT，返回最后一次结果")

            # 构建响应
            execution_time = time.time() - start_time
            response = OrchestratorResponse(
                request_id=request.id,
                content=result,
                worker_mode=request.mode.value,
                task_count=len(task_plan),
                execution_time_sec=execution_time,
                metadata={
                    "stats": self._stats.copy(),
                    "context_tokens": self.context_manager._estimate_total_tokens(),
                    "audit_retries": audit_retries,
                }
            )

            # 记录到上下文管理器
            self.context_manager.add_exchange(content, result)

            if self._on_response:
                self._on_response(response)

            return response

        except Exception as e:
            self.state = SessionState.ERROR
            if self._on_error:
                self._on_error(e, request.id)
            raise

    async def _analyze_request(self, request: UserRequest) -> List[Dict]:
        """分析请求，生成任务计划"""
        content = request.content.strip()
        request_type = request.request_type

        # 显式指定 fast/slow 时，优先服从，不走自动复杂度判断
        if request.mode == WorkerMode.FAST:
            return [{"type": "respond", "content": content, "mode": WorkerMode.FAST}]
        if request.mode == WorkerMode.SLOW:
            return [{"type": "respond", "content": content, "mode": WorkerMode.SLOW}]

        # 自动检测请求类型（当 request_type 为 general 时）
        if request_type == "general":
            detected = self._auto_detect_request_type(content)
            if detected != "general":
                request_type = detected
                self._log("info", f"自动识别请求类型: {detected}")

        if request_type == "code":
            return self._plan_code_tasks(content, request)
        elif request_type == "debug":
            return self._plan_debug_tasks(content, request)
        elif request_type == "research":
            return self._plan_research_tasks(content, request)
        else:
            complexity = self._assess_complexity(content)

            if complexity <= 2:
                return [{"type": "respond", "content": content, "mode": WorkerMode.FAST}]
            else:
                return [{"type": "respond", "content": content, "mode": WorkerMode.SLOW}]

    def _assess_complexity(self, content: str) -> int:
        """
        评估任务复杂度（1-5），加权打分取最高分

        多个关键词同时命中时取最高分，而非先到先得。
        中英文关键词都覆盖。
        """
        # 关键词 → 复杂度分数（支持中英文）
        keyword_scores = {
            # 1分：简单问答
            1: ["是", "否", "什么", "简单", "快速", "你好", "hi", "hello", "yes", "no", "what"],
            # 2分：基础解释
            2: ["解释", "如何", "例子", "介绍", "区别", "对比", "explain", "how", "example", "compare", "difference"],
            # 3分：中等分析
            3: ["分析", "总结", "评估", "建议", "方案", "analyze", "summarize", "evaluate", "suggest", "plan"],
            # 4分：复杂设计
            4: ["设计", "架构", "优化", "重构", "系统", "实现", "开发", "编写", "design", "architecture", "optimize", "refactor", "implement", "develop"],
            # 5分：深度研究
            5: ["完整", "全面", "详细", "深入研究", "最佳实践", "从零开始", "端到端", "comprehensive", "in-depth", "best practice", "end-to-end", "from scratch"],
        }

        content_lower = content.lower()

        # 取所有命中关键词的最高分
        max_score = 0
        for level, words in keyword_scores.items():
            if any(w in content_lower for w in words):
                max_score = max(max_score, level)

        # 没命中任何关键词时，按长度兜底
        if max_score == 0:
            text_len = len(content)
            if text_len < 30:
                max_score = 1
            elif text_len < 100:
                max_score = 2
            elif text_len > 300:
                max_score = 4
            else:
                max_score = 3

        # 长文本加分（>200字至少3分，>500字至少4分）
        if len(content) > 500 and max_score < 4:
            max_score = 4
        elif len(content) > 200 and max_score < 3:
            max_score = 3

        return max_score

    def _auto_detect_request_type(self, content: str) -> str:
        """
        自动识别请求类型（零成本，纯关键词）

        Returns: "code" / "debug" / "research" / "analysis" / "general"
        """
        content_lower = content.lower()

        # 分析类（v4.1 新增，优先级最高）
        analysis_keywords = [
            "分析", "analyze", "analysis", "review", "审查", "调研", "研究",
            "架构", "architecture", "设计", "design",
            "源码", "source code", "codebase",
            "报告", "report", "总结", "summary",
        ]
        if any(kw in content_lower for kw in analysis_keywords):
            return "analysis"

        # 代码类
        code_keywords = [
            "写代码", "编写", "实现", "开发", "写一个", "创建一个",
            "write code", "implement", "develop", "create a", "build a",
            "函数", "类", "脚本", "API", "接口",
            "function", "class", "script",
        ]
        if any(kw in content_lower for kw in code_keywords):
            return "code"

        # 调试类
        debug_keywords = [
            "修复", "bug", "报错", "错误", "异常", "崩溃", "不工作",
            "fix", "debug", "error", "exception", "crash", "broken",
            "为什么不", "怎么回事", "出了什么问题",
        ]
        if any(kw in content_lower for kw in debug_keywords):
            return "debug"

        # 研究类
        research_keywords = [
            "对比", "评测", "选型", "趋势",
            "research", "investigate", "compare", "benchmark", "survey",
            "有哪些", "推荐", "最好的",
        ]
        if any(kw in content_lower for kw in research_keywords):
            return "research"

        return "general"

    def _plan_code_tasks(self, content: str, request: UserRequest) -> List[Dict]:
        return [
            {"type": "analyze", "content": f"分析需求: {content}", "mode": WorkerMode.SLOW},
            {"type": "code", "content": content, "mode": WorkerMode.SLOW},
        ]

    def _plan_debug_tasks(self, content: str, request: UserRequest) -> List[Dict]:
        return [
            {"type": "diagnose", "content": content, "mode": WorkerMode.SLOW},
        ]

    def _plan_research_tasks(self, content: str, request: UserRequest) -> List[Dict]:
        return [
            {"type": "search", "content": f"搜索: {content}", "mode": WorkerMode.SLOW},
            {"type": "synthesize", "content": "综合发现", "mode": WorkerMode.FAST}
        ]
    
    def plan_complex_task(self, content: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        预规划复杂任务：分析任务需要多少子代理、每个干什么、预计多久
        
        这是 orchestrator 的核心差异化能力——不是直接干活，
        而是先规划怎么拆、怎么派、怎么收。
        
        Args:
            content: 用户的任务描述
            context: 额外上下文（如涉及的文件列表）
        
        Returns:
            {
                "complexity": 4,
                "duration": "LONG",
                "request_type": "code",
                "total_subtasks": 5,
                "estimated_time_sec": 600,
                "strategy": "parallel",  # parallel / sequential / mixed
                "subtasks": [
                    {
                        "id": "step-1",
                        "description": "...",
                        "files_to_read": ["file1.py"],
                        "estimated_time_sec": 120,
                        "mode": "slow",
                        "dependencies": [],
                        "priority": "high"
                    },
                    ...
                ],
                "merge_strategy": "concatenate",  # concatenate / synthesize
                "notes": "..."
            }
        """
        # 评估基本属性
        complexity = self._assess_complexity(content)
        duration = self._estimate_duration(content)
        request_type = self._auto_detect_request_type(content)
        
        # 真实扫描文件系统
        target_dir = context.get("target_dir") if context else None
        scan = self.scan_task_scope(content, target_dir=target_dir)
        files = [f["path"] for f in scan["files"]]
        
        # 简单任务不需要拆
        if complexity <= 2 and len(files) <= self.config.max_files_per_subtask and request_type == "general":
            return {
                "complexity": complexity,
                "duration": duration.value,
                "request_type": request_type,
                "total_subtasks": 1,
                "estimated_time_sec": int(self.config.fast_timeout),
                "strategy": "direct",
                "subtasks": [{
                    "id": "step-0",
                    "description": content,
                    "files_to_read": files,
                    "estimated_time_sec": int(self.config.fast_timeout),
                    "mode": "fast",
                    "dependencies": [],
                    "priority": "normal",
                }],
                "merge_strategy": "none",
                "notes": "简单任务，直接执行",
            }
        
        # 大项目分析模式（v4.1）：按模块拆分，而非按文件数机械切片
        is_large_project = scan.get("is_large_project", False)
        modules = scan.get("modules", {})
        is_analysis = request_type in ("research", "general", "analysis") and any(
            kw in content.lower() for kw in ["分析", "analyze", "analysis", "review", "审查", "调研", "研究", "报告", "架构", "源码"]
        )
        
        if is_large_project and modules and is_analysis:
            # ---- 第一步：分离大模块和小模块 ----
            # 小模块判定：文件数 <= 20 且行数 <= 2000
            SMALL_MODULE_FILE_THRESHOLD = 20
            SMALL_MODULE_LINE_THRESHOLD = 2000
            # 合并后单个 subtask 的负载上限
            MERGED_BATCH_FILE_LIMIT = 60
            MERGED_BATCH_LINE_LIMIT = 5000
            
            large_modules = {}  # 大模块：每个单独一个 subtask
            small_modules = {}  # 小模块：待合并
            
            for module_key, module_info in modules.items():
                fc = module_info["file_count"]
                tl = module_info["total_lines"]
                if fc > SMALL_MODULE_FILE_THRESHOLD or tl > SMALL_MODULE_LINE_THRESHOLD:
                    large_modules[module_key] = module_info
                else:
                    small_modules[module_key] = module_info
            
            subtasks = []
            step_idx = 0
            
            # ---- 第二步：大模块各自生成 subtask ----
            for module_key, module_info in large_modules.items():
                file_count = module_info["file_count"]
                total_lines = module_info["total_lines"]
                
                if file_count > 50:
                    timeout = int(self.config.analysis_timeout_large)
                    file_cap = self.config.analysis_file_read_cap_large
                elif file_count > 20:
                    timeout = int(self.config.analysis_timeout_medium)
                    file_cap = self.config.analysis_file_read_cap_medium
                else:
                    timeout = int(self.config.analysis_timeout_small)
                    file_cap = self.config.analysis_file_read_cap_small
                
                subtasks.append({
                    "id": f"step-{step_idx}",
                    "description": (
                        f"分析模块 [{module_key}]（{file_count} 个文件，{total_lines} 行代码）\n\n"
                        f"原始任务：{content[:200]}\n\n"
                        f"⚠️ 文件读取约束：\n"
                        f"- 优先读 index.ts / 主文件 / types.ts 了解结构\n"
                        f"- 每个子目录只读 1-2 个核心文件，不要逐个读\n"
                        f"- 总共最多读 {file_cap} 个文件\n"
                        f"- 如果时间不够，优先输出已分析的内容，不要卡在读文件上"
                    ),
                    "files_to_read": [],
                    "estimated_time_sec": timeout,
                    "mode": "slow",
                    "dependencies": [],
                    "priority": "normal",
                    "module_key": module_key,
                    "module_file_count": file_count,
                    "module_total_lines": total_lines,
                    "file_read_cap": file_cap,
                })
                step_idx += 1
            
            # ---- 第三步：小模块按负载贪心合并 ----
            if small_modules:
                # 按文件数降序排列，大的先放，贪心装箱
                sorted_small = sorted(small_modules.items(), key=lambda x: x[1]["file_count"], reverse=True)
                
                current_batch = []  # [(module_key, module_info), ...]
                current_files = 0
                current_lines = 0
                
                def _flush_batch(batch, idx):
                    """把当前 batch 生成一个合并 subtask"""
                    batch_file_count = sum(m[1]["file_count"] for m in batch)
                    batch_total_lines = sum(m[1]["total_lines"] for m in batch)
                    batch_keys = [m[0] for m in batch]
                    
                    # 合并后的文件读取上限 = 各模块 cap 之和，但不超过合理值
                    per_module_cap = max(3, self.config.analysis_file_read_cap_small // 2)
                    merged_file_cap = min(
                        per_module_cap * len(batch),
                        self.config.analysis_file_read_cap_large
                    )
                    
                    # 合并后超时取中模块级别
                    if batch_file_count > 50:
                        merged_timeout = int(self.config.analysis_timeout_large)
                    elif batch_file_count > 20:
                        merged_timeout = int(self.config.analysis_timeout_medium)
                    else:
                        merged_timeout = int(self.config.analysis_timeout_small)
                    
                    module_list_str = "\n".join(
                        f"  - [{k}]（{m['file_count']} 文件，{m['total_lines']} 行）"
                        for k, m in batch
                    )
                    
                    if len(batch) == 1:
                        label = batch_keys[0]
                    else:
                        label = "+".join(batch_keys[:3])
                        if len(batch_keys) > 3:
                            label += f"+{len(batch_keys)-3}more"
                    
                    return {
                        "id": f"step-{idx}",
                        "description": (
                            f"分析以下 {len(batch)} 个小模块（共 {batch_file_count} 个文件，{batch_total_lines} 行代码）：\n"
                            f"{module_list_str}\n\n"
                            f"原始任务：{content[:200]}\n\n"
                            f"⚠️ 文件读取约束：\n"
                            f"- 每个模块优先读 index.ts / 主文件 / types.ts\n"
                            f"- 每个模块读 1-3 个核心文件即可\n"
                            f"- 总共最多读 {merged_file_cap} 个文件\n"
                            f"- 如果时间不够，优先输出已分析的内容"
                        ),
                        "files_to_read": [],
                        "estimated_time_sec": merged_timeout,
                        "mode": "slow",
                        "dependencies": [],
                        "priority": "normal",
                        "module_key": label,
                        "module_file_count": batch_file_count,
                        "module_total_lines": batch_total_lines,
                        "file_read_cap": merged_file_cap,
                        "merged_modules": batch_keys,
                    }
                
                for module_key, module_info in sorted_small:
                    fc = module_info["file_count"]
                    tl = module_info["total_lines"]
                    
                    # 如果加入当前 batch 会超限，先 flush
                    if current_batch and (current_files + fc > MERGED_BATCH_FILE_LIMIT or current_lines + tl > MERGED_BATCH_LINE_LIMIT):
                        subtasks.append(_flush_batch(current_batch, step_idx))
                        step_idx += 1
                        current_batch = []
                        current_files = 0
                        current_lines = 0
                    
                    current_batch.append((module_key, module_info))
                    current_files += fc
                    current_lines += tl
                
                # flush 最后一批
                if current_batch:
                    subtasks.append(_flush_batch(current_batch, step_idx))
                    step_idx += 1
            
            # ---- 第四步：统计和返回 ----
            original_module_count = len(modules)
            merged_count = len(subtasks)
            small_count = len(small_modules)
            
            estimated_total = max(t["estimated_time_sec"] for t in subtasks) if subtasks else 0
            
            merge_note = ""
            if small_count > 0 and merged_count < original_module_count:
                merge_note = f"，{small_count} 个小模块合并为 {merged_count - len(large_modules)} 个批次"
            
            return {
                "complexity": complexity,
                "duration": duration.value,
                "request_type": request_type,
                "total_subtasks": len(subtasks),
                "estimated_time_sec": estimated_total,
                "strategy": "parallel",
                "subtasks": subtasks,
                "merge_strategy": "synthesize",
                "notes": f"🔥 大项目分析模式：{original_module_count} 个模块 → {merged_count} 个子任务{merge_note}",
                "is_large_project": True,
            }
        
        # 常规复杂任务：按文件数和复杂度拆分（原逻辑）
        subtasks = []
        max_files = self.config.max_files_per_subtask
        max_subtasks_cap = 20  # 子任务数上限，防止大项目拆出几百个
        
        if len(files) > max_files:
            # 按文件分组拆分（带上限）
            file_groups = [files[i:i+max_files] for i in range(0, len(files), max_files)]
            if len(file_groups) > max_subtasks_cap:
                # 超过上限，增大每组文件数重新分组
                adjusted_max = max(2, len(files) // max_subtasks_cap + 1)
                file_groups = [files[i:i+adjusted_max] for i in range(0, len(files), adjusted_max)]
            for idx, group in enumerate(file_groups):
                file_names = ", ".join(Path(f).name for f in group)
                subtasks.append({
                    "id": f"step-{idx}",
                    "description": f"处理以下文件的相关任务：{file_names}\n\n原始任务：{content[:200]}",
                    "files_to_read": group,
                    "estimated_time_sec": int(self.config.subtask_timeout),
                    "mode": "slow",
                    "dependencies": [],
                    "priority": "normal",
                })
        elif request_type == "code":
            # 代码任务按阶段拆
            subtasks = [
                {"id": "step-0", "description": f"分析需求并设计方案：{content[:200]}", "files_to_read": files[:max_files], "estimated_time_sec": 180, "mode": "slow", "dependencies": [], "priority": "high"},
                {"id": "step-1", "description": f"根据方案编写代码：{content[:200]}", "files_to_read": files[:max_files], "estimated_time_sec": 300, "mode": "slow", "dependencies": ["step-0"], "priority": "high"},
                {"id": "step-2", "description": "代码审查与优化", "files_to_read": [], "estimated_time_sec": 120, "mode": "slow", "dependencies": ["step-1"], "priority": "normal"},
            ]
        elif request_type == "research":
            # 研究任务按阶段拆
            subtasks = [
                {"id": "step-0", "description": f"搜索和收集信息：{content[:200]}", "files_to_read": [], "estimated_time_sec": 180, "mode": "slow", "dependencies": [], "priority": "high"},
                {"id": "step-1", "description": "综合分析与对比", "files_to_read": [], "estimated_time_sec": 180, "mode": "slow", "dependencies": ["step-0"], "priority": "normal"},
                {"id": "step-2", "description": "撰写总结报告", "files_to_read": [], "estimated_time_sec": 120, "mode": "slow", "dependencies": ["step-1"], "priority": "normal"},
            ]
        else:
            # 通用复杂任务：按内容长度拆
            chunk_size = 500  # 每块最多 500 字符
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
            if len(chunks) == 1:
                subtasks = [{
                    "id": "step-0",
                    "description": content,
                    "files_to_read": files[:max_files],
                    "estimated_time_sec": int(self.config.subtask_timeout),
                    "mode": "slow",
                    "dependencies": [],
                    "priority": "normal",
                }]
            else:
                for idx, chunk in enumerate(chunks):
                    subtasks.append({
                        "id": f"step-{idx}",
                        "description": chunk,
                        "files_to_read": files[:max_files] if idx == 0 else [],
                        "estimated_time_sec": int(self.config.subtask_timeout),
                        "mode": "slow",
                        "dependencies": [f"step-{idx-1}"] if idx > 0 else [],
                        "priority": "normal",
                    })
        
        # 计算策略
        has_deps = any(t.get("dependencies") for t in subtasks)
        if has_deps:
            strategy = "sequential" if all(t.get("dependencies") for t in subtasks[1:]) else "mixed"
        else:
            strategy = "parallel"
        
        # 估算总时间
        if strategy == "parallel":
            estimated_total = max(t["estimated_time_sec"] for t in subtasks)
        else:
            estimated_total = sum(t["estimated_time_sec"] for t in subtasks)
        
        return {
            "complexity": complexity,
            "duration": duration.value,
            "request_type": request_type,
            "total_subtasks": len(subtasks),
            "estimated_time_sec": estimated_total,
            "strategy": strategy,
            "subtasks": subtasks,
            "merge_strategy": "synthesize" if len(subtasks) > 1 else "none",
            "notes": f"任务已拆为 {len(subtasks)} 个子任务，策略: {strategy}",
        }
    
    def _extract_file_references(self, content: str) -> List[str]:
        """从文本中提取文件路径引用"""
        import re
        # 匹配常见文件路径模式
        patterns = [
            r'[A-Z]:\\[^\s\'"<>]+\.\w+',          # Windows 绝对路径
            r'/[\w/.-]+\.\w+',                       # Unix 绝对路径
            r'[\w.-]+\.(?:py|js|ts|md|json|yaml)',   # 文件名
        ]
        files = []
        for pattern in patterns:
            files.extend(re.findall(pattern, content))
        return list(set(files))
    
    def scan_task_scope(self, content: str, target_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        扫描任务涉及的文件和代码量，为规划提供真实数据
        
        Args:
            content: 用户任务描述
            target_dir: 目标目录（如果任务涉及某个项目/目录）
        
        Returns:
            {
                "files": [{"path": "...", "name": "...", "size_kb": 12.3, "lines": 450, "language": "python"}],
                "total_files": 7,
                "total_lines": 3200,
                "total_size_kb": 155.2,
                "languages": {"python": 5, "markdown": 2},
                "estimated_subtasks": 4,
                "estimated_time_sec": 600,
                "scan_note": "..."
            }
        """
        import os
        import re
        
        # 1. 提取文件引用
        referenced_files = self._extract_file_references(content)
        
        # 2. 如果有目标目录，扫描整个目录
        scanned_files = []
        if target_dir and os.path.isdir(target_dir):
            code_extensions = {
                '.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.rs', '.java',
                '.cpp', '.c', '.h', '.md', '.json', '.yaml', '.yml',
                '.css', '.scss', '.less', '.html', '.vue', '.svelte',
                '.sh', '.bash', '.sql', '.graphql', '.gql',
                '.toml', '.ini', '.env',
            }
            skip_dirs = {
                # 构建产物
                '__pycache__', 'node_modules', '.git', '.venv', 'venv',
                'checkpoints', '.clawhub', '.next', 'dist', 'build', 'out',
                '.turbo', '.cache', '.parcel-cache', '.nuxt', '.output',
                # 依赖/缓存
                '.npm', '.yarn', '.pnpm-store', 'coverage', '.nyc_output',
                # IDE
                '.idea', '.vscode',
                # 其他
                '.svn', '.hg', 'vendor', 'target',
            }
            for root, dirs, filenames in os.walk(target_dir):
                dirs[:] = [d for d in dirs if d not in skip_dirs]
                for fname in filenames:
                    ext = os.path.splitext(fname)[1].lower()
                    if ext in code_extensions:
                        fpath = os.path.join(root, fname)
                        scanned_files.append(fpath)
        
        # 3. 合并引用文件和扫描文件（去重）
        all_paths = list(set(referenced_files + scanned_files))
        
        # 4. 分析每个文件
        file_infos = []
        total_lines = 0
        total_size = 0
        languages: Dict[str, int] = {}
        
        ext_to_lang = {
            '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
            '.jsx': 'javascript', '.tsx': 'typescript',
            '.go': 'go', '.rs': 'rust', '.java': 'java',
            '.cpp': 'cpp', '.c': 'c', '.h': 'c-header',
            '.md': 'markdown', '.json': 'json', '.yaml': 'yaml', '.yml': 'yaml',
            '.css': 'css', '.scss': 'scss', '.less': 'less',
            '.html': 'html', '.vue': 'vue', '.svelte': 'svelte',
            '.sh': 'shell', '.bash': 'shell', '.zsh': 'shell',
            '.sql': 'sql', '.graphql': 'graphql', '.gql': 'graphql',
            '.toml': 'toml', '.ini': 'ini', '.env': 'env',
        }
        
        for fpath in all_paths:
            if not os.path.isfile(fpath):
                continue
            try:
                size = os.path.getsize(fpath)
                size_kb = round(size / 1024, 1)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = sum(1 for _ in f)
                ext = os.path.splitext(fpath)[1].lower()
                lang = ext_to_lang.get(ext, 'other')
                
                file_infos.append({
                    "path": fpath,
                    "name": os.path.basename(fpath),
                    "size_kb": size_kb,
                    "lines": lines,
                    "language": lang,
                })
                total_lines += lines
                total_size += size_kb
                languages[lang] = languages.get(lang, 0) + 1
            except Exception:
                continue
        
        # 5. 估算子任务数和时间
        max_files = self.config.max_files_per_subtask
        max_lines_per_subtask = 500  # 每个子任务最多处理 500 行代码
        
        # 大项目检测
        is_large_project = (
            len(file_infos) >= self.config.large_project_file_threshold or
            total_lines >= self.config.large_project_line_threshold
        )
        
        # 模块识别（按顶层目录分组）
        modules: Dict[str, List[Dict]] = {}
        if target_dir and is_large_project:
            for fi in file_infos:
                rel = os.path.relpath(fi["path"], target_dir)
                parts = rel.replace("\\", "/").split("/")
                # 取第一级目录作为模块标识（更粗粒度，避免拆太细）
                if len(parts) >= 2:
                    module_key = parts[0]
                else:
                    module_key = "_root"
                if module_key not in modules:
                    modules[module_key] = []
                modules[module_key].append(fi)
            
            # 合并小模块（<5 个文件的模块合并为 _misc）
            merged_modules: Dict[str, List[Dict]] = {}
            misc_files: List[Dict] = []
            for k, v in modules.items():
                if len(v) < 5:
                    misc_files.extend(v)
                else:
                    merged_modules[k] = v
            if misc_files:
                merged_modules["_misc"] = misc_files
            modules = merged_modules
        
        if is_large_project and modules:
            # 大项目：按模块估算子任务数
            estimated_subtasks = len(modules)
            scan_note = (
                f"🔥 大项目检测：{len(file_infos)} 个文件，{total_lines} 行代码"
                f"（{round(total_size, 1)}KB），识别到 {len(modules)} 个模块"
            )
        else:
            # 常规项目：按文件数/行数拆
            by_files = max(1, len(file_infos) // max_files + (1 if len(file_infos) % max_files else 0))
            by_lines = max(1, total_lines // max_lines_per_subtask + (1 if total_lines % max_lines_per_subtask else 0))
            estimated_subtasks = max(by_files, by_lines)
            scan_note = f"扫描到 {len(file_infos)} 个文件，共 {total_lines} 行代码（{round(total_size, 1)}KB）"
            if estimated_subtasks > 1:
                scan_note += f"，建议拆为 {estimated_subtasks} 个子任务"
        
        # 估算时间：每个子任务 3-5 分钟
        estimated_time = estimated_subtasks * 240  # 4 分钟/子任务
        
        return {
            "files": file_infos,
            "total_files": len(file_infos),
            "total_lines": total_lines,
            "total_size_kb": round(total_size, 1),
            "languages": languages,
            "estimated_subtasks": estimated_subtasks,
            "estimated_time_sec": estimated_time,
            "scan_note": scan_note,
            "is_large_project": is_large_project,
            "modules": {k: {"file_count": len(v), "total_lines": sum(f["lines"] for f in v)} for k, v in modules.items()} if modules else {},
        }

    async def _execute_single_task(self, request: UserRequest, task_def: Dict) -> str:
        """执行单个任务，根据模式和时长选择执行方式"""
        mode = task_def.get("mode", request.mode)
        content = task_def.get("content", request.content)

        # 检查是否为长任务
        duration = self._estimate_duration(content)
        if duration == TaskDuration.LONG and self._v3_bridge_enabled:
            return await self._execute_long(content, request)

        if mode == WorkerMode.FAST:
            return await self._execute_fast(content, request)
        else:
            return await self._execute_slow(content, request)

    def _estimate_duration(self, content: str) -> TaskDuration:
        """评估任务预计时长"""
        content_lower = content.lower()

        # 关键词匹配长任务
        for kw in self.config.long_task_keywords:
            if kw in content_lower:
                return TaskDuration.LONG

        # 高复杂度 + 长文本 → LONG
        complexity = self._assess_complexity(content)
        if complexity >= 4 and len(content) > 200:
            return TaskDuration.LONG

        # 中等复杂度 → MEDIUM
        if complexity >= 3:
            return TaskDuration.MEDIUM

        return TaskDuration.SHORT

    async def _execute_long(self, content: str, request: UserRequest) -> str:
        """Long 任务：通过 V3 Bridge 执行（>30分钟）"""
        self._stats["long_tasks"] += 1

        if not _HAS_V3_BRIDGE:
            self._log("warning", "V3 Bridge 不可用，降级为 Slow Worker")
            return await self._execute_slow(content, request)

        # 创建 V3 Bridge 实例
        bridge = V3Bridge(
            heartbeat_interval=self.config.v3_bridge_heartbeat_interval,
        )
        executor = LongTaskExecutor(bridge)

        try:
            results = []
            async for progress in executor.execute(content):
                status = progress.get("status", "")
                if status == "completed":
                    result = progress.get("result", "")
                    results.append(str(result))
                elif status == "progress":
                    detail = progress.get("detail", "")
                    self._log("info", f"Long task progress: {progress.get('progress', 0)}% - {detail}")

            if results:
                return "\n".join(results)
            return "[Long Task] 执行完成，无返回结果"
        except Exception as e:
            self._log("error", f"Long task failed: {e}")
            # 降级为 Slow Worker
            return await self._execute_slow(content, request)
        finally:
            await bridge.disconnect()

    async def _execute_fast(self, content: str, request: UserRequest) -> str:
        """Fast 任务：当前会话直接回答（简洁 prompt）"""
        self._stats["fast_tasks"] += 1

        # 如果 HybridWorker 可用，委托给它
        if self._hybrid_worker:
            from hybrid_worker_acp import TaskContext
            ctx = TaskContext(
                task_id=str(uuid.uuid4())[:8],
                task_description=content,
                conversation_history=self.context_manager.get_formatted_history(3)
            )
            result = await self._hybrid_worker.process(content, context=ctx, mode=WorkerMode.FAST)
            return result.get("result", str(result))

        # 原有 stub 逻辑作为 fallback
        history = self.context_manager.get_formatted_history(3)
        history_str = "\n".join([
            f"{h['role']}: {h['content'][:100]}"
            for h in history
        ])

        prompt = f"""快速回答以下问题，保持简洁（200字以内）：

{content}

历史上下文：
{history_str}

请直接给出答案，不要过多解释。"""

        # 实际使用时，这里直接返回，由外层 agent 处理
        # 或者调用一个轻量级的本地函数
        return f"[Fast Response] {content[:50]}..."

    async def _execute_slow(self, content: str, request: UserRequest) -> str:
        """Slow 任务：spawn 子 agent"""
        self._stats["slow_tasks"] += 1
        self._stats["spawned_agents"] += 1

        # 构建完整 prompt
        history = self.context_manager.get_formatted_history(2)
        history_str = "\n".join([
            f"{h['role']}: {h['content'][:150]}"
            for h in history
        ])

        # 如果 HybridWorker 可用，使用它的 PromptTemplate 生成更好的 prompt
        if self._hybrid_worker:
            from hybrid_worker_acp import TaskContext
            ctx = TaskContext(
                task_id=str(uuid.uuid4())[:8],
                task_description=content,
                conversation_history=history,
                available_tools=self._get_available_tools()
            )
            task_prompt = self._hybrid_worker.template.build_slow_prompt(content, ctx)
        else:
            task_prompt = f"""深入分析并全面回答以下问题：

{content}

历史上下文：
{history_str}

请提供详细的分析和解决方案。"""

        # 使用 sessions_spawn 创建子 agent
        # 注意：这里需要 OpenClaw 运行时环境
        return await self._spawn_sub_agent(task_prompt, request.id)

    async def _spawn_sub_agent(self, task_prompt: str, parent_task_id: str) -> str:
        """
        Spawn 子 agent 执行任务
        
        默认使用注入的 spawn_func 对接 OpenClaw sessions_spawn。
        未注入时退回模拟结果，便于本地测试。
        集成生命周期管理和后台监控。
        """
        # 检查暂停状态
        if self._paused:
            return "[已暂停] 编排器当前处于暂停状态，等待恢复"
        
        if not self._spawn_func:
            return f"[Slow Worker Response via Sub-Agent]\nTask: {task_prompt[:100]}..."

        # 并发控制：等待信号量
        async with self._spawn_semaphore:
            return await self._do_spawn(task_prompt, parent_task_id)

    async def _do_spawn(self, task_prompt: str, parent_task_id: str) -> str:
        """实际执行 spawn（在信号量保护内调用），带自动重试闭环"""
        label = f"slow-worker-{parent_task_id}"

        # 注册到任务追踪器
        task_desc = task_prompt[:80].replace("\n", " ")
        self._active_tasks[label] = {
            "status": "spawning",
            "task_desc": task_desc,
            "session_key": "",
            "started_at": time.time(),
            "completed_at": None,
        }
        self._task_counter["total"] += 1
        self._task_counter["running"] += 1

        # 智能超时：根据任务复杂度选择超时
        # 长 prompt（>1000字符）或包含"读取"/"修改"/"集成"等关键词 → 用 complex_slow_timeout
        task_len = len(task_prompt)
        complex_keywords = ["读取", "修改", "集成", "重构", "分析并", "所有文件", "全部", "完整"]
        analysis_keywords = ["分析", "analyze", "analysis", "review", "审查", "调研", "研究"]
        is_complex = task_len > 1000 or any(kw in task_prompt for kw in complex_keywords)
        is_analysis = any(kw in task_prompt for kw in analysis_keywords)
        
        if is_analysis:
            # 分析类任务：根据 prompt 中的模块大小提示动态超时
            # 从 prompt 中提取文件读取上限数字作为模块大小参考
            import re
            file_cap_match = re.search(r'最多读\s*(\d+)\s*个文件', task_prompt)
            if file_cap_match:
                file_cap = int(file_cap_match.group(1))
                if file_cap >= 20:
                    timeout = int(self.config.analysis_timeout_large)
                elif file_cap >= 10:
                    timeout = int(self.config.analysis_timeout_medium)
                else:
                    timeout = int(self.config.analysis_timeout_small)
            else:
                timeout = int(self.config.analysis_timeout_medium)
        elif is_complex:
            timeout = int(self.config.complex_slow_timeout)
        else:
            timeout = int(self.config.slow_timeout)

        payload: Dict[str, Any] = {
            "runtime": "subagent",
            "agentId": self.config.subagent_agent_id,
            "label": label,
            "mode": "run",
            "task": task_prompt,
            "timeoutSeconds": timeout,
            "runTimeoutSeconds": timeout,
            "cleanup": self.config.subagent_cleanup,
            "sandbox": self.config.subagent_sandbox,
            "cwd": str(Path.cwd()),
        }
        if self.config.subagent_model:
            payload["model"] = self.config.subagent_model
        if self.config.subagent_thinking:
            payload["thinking"] = self.config.subagent_thinking

        # 安全上限：单次调用最多重试 max_restarts 次，防止无限递归
        max_restarts = max(0, self.config.max_restarts)
        last_error: Optional[Exception] = None

        for attempt in range(max_restarts + 1):
            try:
                result = await self._spawn_func(**payload)
            except Exception as e:
                last_error = e
                # spawn 失败，记录到生命周期管理器
                if self._lifecycle:
                    self._lifecycle.register(parent_task_id, f"failed-{label}")
                    self._lifecycle.mark_failed(parent_task_id, str(e))

                # 检查是否应该自动重启
                if attempt < max_restarts and self._lifecycle and self._lifecycle.should_restart(parent_task_id):
                    self._lifecycle.record_restart(parent_task_id)
                    delay = self._lifecycle.get_restart_delay(parent_task_id)
                    self._log(
                        "warning",
                        f"Spawn sub-agent 失败，准备第 {attempt + 1} 次重试（共允许 {max_restarts} 次），延迟 {delay:.1f} 秒: {e}"
                    )
                    await asyncio.sleep(delay)
                    continue

                # 达到重试上限或不应重启，记录错误并返回错误信息字符串，避免整个编排器崩溃
                self._log("error", f"Spawn sub-agent 最终失败（已重试 {attempt} 次）: {e}")
                # 更新任务追踪器
                if label in self._active_tasks:
                    self._active_tasks[label]["status"] = "failed"
                    self._active_tasks[label]["completed_at"] = time.time()
                self._task_counter["running"] = max(0, self._task_counter["running"] - 1)
                self._task_counter["failed"] += 1
                return f"[Spawn 失败] 子 agent 启动失败，已重试 {attempt} 次，错误: {e}"

            # 提取 session_key 用于注册
            session_key = ""
            if isinstance(result, dict):
                session_key = result.get("childSessionKey") or result.get("sessionKey") or result.get("session_key") or ""

            # 注册到生命周期管理器
            if self._lifecycle and session_key:
                self._lifecycle.register(parent_task_id, session_key)

            # 注册到后台监控器
            if self._monitor and session_key:
                self._monitor.register(
                    task_id=parent_task_id,
                    session_key=session_key,
                    timeout=self.config.slow_timeout,
                )

            # 解析结果
            if isinstance(result, dict):
                status = result.get("status", "")
                if status == "accepted":
                    # spawn 成功但结果是异步的
                    parts = [f"[Slow Worker spawned] label={label}"]
                    if session_key:
                        parts.append(f"sessionKey={session_key}")

                    # 更新任务追踪器
                    if label in self._active_tasks:
                        self._active_tasks[label]["status"] = "running"
                        self._active_tasks[label]["session_key"] = session_key

                    # 标记生命周期完成（spawn 成功）
                    if self._lifecycle:
                        self._lifecycle.mark_completed(parent_task_id, success=True)
                    if self._monitor:
                        self._monitor.heartbeat(parent_task_id)

                    return " ".join(parts)

                # 其他 dict 结果
                accepted = result.get("accepted")
                if isinstance(accepted, str) and accepted.strip():
                    if self._lifecycle:
                        self._lifecycle.mark_completed(parent_task_id, success=True)
                    if self._monitor:
                        self._monitor.mark_done(parent_task_id, success=True)
                    return accepted.strip()

            # 标记完成
            if self._lifecycle:
                self._lifecycle.mark_completed(parent_task_id, success=True)
            if self._monitor:
                self._monitor.mark_done(parent_task_id, success=True)

            return str(result)

        # 理论上不会走到这里，作为兜底返回错误信息
        err_msg = f"[Spawn 失败] 子 agent 启动失败，已重试 {max_restarts} 次"
        if last_error:
            err_msg += f"，最后错误: {last_error}"
        return err_msg

    async def _execute_task_plan(self, request: UserRequest, task_plan: List[Dict]) -> str:
        """执行多任务计划，支持 MicroScheduler 并发或顺序执行"""

        # 如果启用了微调度器且有多个任务，用并发调度
        if self._scheduler_enabled and len(task_plan) > 1:
            return await self._execute_task_plan_scheduled(request, task_plan)

        # 否则顺序执行（原逻辑）
        results = []

        for i, task_def in enumerate(task_plan):
            task_content = task_def["content"]

            # 如果有上一步结果，添加摘要
            if results and i > 0:
                prev_summary = await self._summarize_result(results[-1])
                task_content += f"\n\n上一步结果摘要:\n{prev_summary}"

            task_result = await self._execute_single_task(
                request,
                {**task_def, "content": task_content}
            )

            task_result = truncate_by_tokens(task_result, self.config.max_result_tokens)
            results.append(task_result)

        return self._synthesize_results(results, request)

    async def _execute_task_plan_scheduled(self, request: UserRequest, task_plan: List[Dict]) -> str:
        """使用 MicroScheduler 并发执行多任务计划"""
        scheduler = MicroScheduler(
            max_concurrent=self.config.scheduler_max_concurrent,
            executor=self._make_scheduler_executor(request),
        )

        # 提交所有任务（按顺序建立依赖链）
        prev_task_id = None
        for i, task_def in enumerate(task_plan):
            task_id = f"step-{i}"
            deps = [prev_task_id] if prev_task_id else []
            priority = TaskPriority.HIGH if task_def.get("mode") == WorkerMode.SLOW else TaskPriority.NORMAL
            scheduler.submit(
                task_id=task_id,
                content=json.dumps(task_def, ensure_ascii=False),
                priority=priority,
                dependencies=deps,
            )
            prev_task_id = task_id

        # 执行
        results_map = await scheduler.run()

        # 按顺序收集结果
        results = []
        for i in range(len(task_plan)):
            task_id = f"step-{i}"
            tr = results_map.get(task_id)
            if tr and tr.success:
                results.append(truncate_by_tokens(tr.content, self.config.max_result_tokens))
            else:
                error = tr.error if tr else "unknown"
                results.append(f"[步骤 {i} 失败: {error}]")

        return self._synthesize_results(results, request)

    def _make_scheduler_executor(self, request: UserRequest) -> Callable:
        """创建调度器的任务执行函数"""
        async def executor(task):
            task_def = json.loads(task.content)
            return await self._execute_single_task(request, task_def)
        return executor

    async def _run_audit(self, task_description: str, result: str, files: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        对 worker 结果执行审计检查

        Args:
            task_description: 任务描述（作为审计契约）
            result: worker 返回的结果
            files: 需要审查的文件列表（可选）

        Returns:
            审计结果 dict，包含 status（PASS/REJECT/ERROR）和 reason
        """
        if not self._audit_enabled or not self._spawn_func:
            return {"status": "SKIP", "reason": "审计未启用或无 spawn 能力"}

        # 构建审计 prompt
        contract = f"任务要求：{task_description}\n\nWorker 返回结果：\n{result[:2000]}"
        if files:
            file_list = "\n".join(f"- {f}" for f in files)
        else:
            file_list = "（无文件，仅审查 Worker 返回的文本结果）"

        audit_prompt = build_audit_prompt(
            contract=contract,
            files=files or [],
            extra_context="请重点检查：结果是否完整回答了任务要求，有无明显错误或遗漏。",
        )

        try:
            audit_result = await self._spawn_func(
                runtime="subagent",
                agentId=self.config.subagent_agent_id,
                label=f"audit-{str(uuid.uuid4())[:6]}",
                mode="run",
                task=audit_prompt,
                timeoutSeconds=int(self.config.audit_timeout),
                runTimeoutSeconds=int(self.config.audit_timeout),
                cleanup="delete",
                sandbox=self.config.subagent_sandbox,
            )

            # 解析审计结果
            if isinstance(audit_result, dict):
                raw = audit_result.get("result") or audit_result.get("content") or str(audit_result)
            else:
                raw = str(audit_result)

            parsed = parse_audit_result(raw)

            status = parsed.get("status", "ERROR")
            if status == "REJECT":
                self._log("warning", f"审计官 REJECT: {parsed.get('reason', 'unknown')}")
            elif status == "PASS":
                self._log("info", "审计官 PASS")

            return parsed

        except Exception as e:
            self._log("error", f"审计执行失败: {e}")
            return {"status": "ERROR", "reason": str(e)}

    async def _summarize_result(self, result: str) -> str:
        """摘要上一步结果"""
        if len(result) <= self.config.summary_threshold:
            return result

        # 超过阈值，生成摘要
        # 实际应该 spawn 一个 Fast Worker 来摘要
        # 这里简单截断
        return result[:self.config.summary_threshold] + "... [summarized]"

    def _synthesize_results(self, results: List[str], request: UserRequest) -> str:
        """汇总多任务结果"""
        if len(results) == 1:
            return results[0]

        parts = ["## 执行结果\n"]
        for i, result in enumerate(results, 1):
            parts.append(f"### 步骤 {i}\n{result[:300]}\n")

        return "\n".join(parts)

    def get_status(self) -> Dict:
        """获取完整状态"""
        return {
            "session_id": self._session_id,
            "state": self.state.name,
            "stats": self._stats,
            "context_tokens": self.context_manager._estimate_total_tokens(),
            "last_activity": self._last_activity
        }

    def get_system_status(self) -> Dict:
        """获取完整系统状态（含所有子模块）"""
        status = {
            "orchestrator": {
                "session_id": self._session_id,
                "state": self.state.name,
                "uptime_sec": round(time.time() - self._last_activity, 1),
                "stats": self._stats.copy(),
                "context_tokens": self.context_manager._estimate_total_tokens(),
            },
            "modules": {
                "lifecycle_manager": "enabled" if self._lifecycle else "disabled",
                "background_monitor": "enabled" if self._monitor else "disabled",
                "micro_scheduler": "enabled" if self._scheduler_enabled else "disabled",
                "v3_bridge": "enabled" if self._v3_bridge_enabled else "disabled",
            },
        }

        # 生命周期管理器状态
        if self._lifecycle:
            all_procs = self._lifecycle.get_all()
            status["lifecycle"] = {
                "total_processes": len(all_procs),
                "by_status": {},
            }
            for p in all_procs.values():
                s = p.status.value if hasattr(p.status, 'value') else str(p.status)
                status["lifecycle"]["by_status"][s] = status["lifecycle"]["by_status"].get(s, 0) + 1

        # 后台监控器状态（get_summary 是 async，这里只放基础信息）
        if self._monitor:
            try:
                # 直接读取内部属性获取同步快照
                monitored = getattr(self._monitor, '_monitored', {})
                status["monitor"] = {
                    "total_agents": len(monitored),
                    "agents": {tid: getattr(a, 'status', 'unknown').value if hasattr(getattr(a, 'status', None), 'value') else str(getattr(a, 'status', 'unknown')) for tid, a in monitored.items()},
                }
            except Exception:
                status["monitor"] = {"error": "获取状态失败"}

        return status

    def get_history(self, limit: int = 10) -> List[Dict]:
        """获取会话历史"""
        return self.context_manager._history[-limit:]

    def get_progress_report(self) -> Dict[str, Any]:
        """
        获取当前任务进度报告（给用户看的）

        Returns:
            {
                "summary": "已完成 2/3 个子代理任务",
                "counter": {"total": 3, "completed": 2, "running": 1, "failed": 0},
                "tasks": [
                    {"label": "...", "status": "running", "task_desc": "...", "session_key": "...", "elapsed": 12.3},
                    ...
                ]
            }
        """
        now = time.time()
        tasks = []
        for label, info in self._active_tasks.items():
            elapsed = now - info["started_at"] if info["started_at"] else 0
            tasks.append({
                "label": label,
                "status": info["status"],
                "task_desc": info["task_desc"],
                "session_key": info.get("session_key", ""),
                "elapsed_sec": round(elapsed, 1),
            })

        total = self._task_counter["total"]
        completed = self._task_counter["completed"]
        running = self._task_counter["running"]
        failed = self._task_counter["failed"]

        summary = f"已完成 {completed}/{total} 个子代理任务"
        if running > 0:
            summary += f"，{running} 个运行中"
        if failed > 0:
            summary += f"，{failed} 个失败"

        return {
            "summary": summary,
            "counter": self._task_counter.copy(),
            "tasks": tasks,
        }

    def mark_task_completed(self, label: str, success: bool = True):
        """
        外部标记任务完成（子代理结果 push 回来时调用）
        """
        if label in self._active_tasks:
            self._active_tasks[label]["status"] = "completed" if success else "failed"
            self._active_tasks[label]["completed_at"] = time.time()
            self._task_counter["running"] = max(0, self._task_counter["running"] - 1)
            if success:
                self._task_counter["completed"] += 1
            else:
                self._task_counter["failed"] += 1

    def clear_history(self):
        """清空历史"""
        self.context_manager.clear()

    async def _health_check_loop(self):
        """健康检查循环"""
        while not self._shutdown:
            try:
                if time.time() - self._last_activity > self.config.session_timeout_sec:
                    self._log("warning", "Session timeout, pausing...")
                    self.pause()

                await asyncio.sleep(self.config.health_check_interval_sec)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self._log("error", f"Health check error: {e}")
                await asyncio.sleep(self.config.health_check_interval_sec)

    async def _checkpoint_loop(self):
        """自动 Checkpoint 循环"""
        while not self._shutdown:
            try:
                await asyncio.sleep(self.config.checkpoint_interval_sec)
                await self._save_checkpoint()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self._log("error", f"Checkpoint error: {e}")

    async def _save_checkpoint(self, suffix: str = "auto"):
        """保存 checkpoint"""
        checkpoint = {
            "session_id": self._session_id,
            "timestamp": time.time(),
            "history": self.context_manager._history,
            "stats": self._stats,
            "request_context": self._request_context
        }

        path = Path(self.config.checkpoint_dir) / f"checkpoint_{self._session_id}_{suffix}.json"
        latest_path = Path(self.config.checkpoint_dir) / self.config.latest_checkpoint_name
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(checkpoint, f, ensure_ascii=False, indent=2)
            with open(latest_path, "w", encoding="utf-8") as f:
                json.dump(checkpoint, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self._log("error", f"Failed to save checkpoint: {e}")

    def _load_latest_checkpoint(self):
        """从最近 checkpoint 恢复上下文和统计"""
        latest_path = Path(self.config.checkpoint_dir) / self.config.latest_checkpoint_name
        if not latest_path.exists():
            return
        try:
            with open(latest_path, "r", encoding="utf-8") as f:
                checkpoint = json.load(f)
            history = checkpoint.get("history")
            if isinstance(history, list):
                self.context_manager._history = history
            stats = checkpoint.get("stats")
            if isinstance(stats, dict):
                self._stats.update(stats)
            request_context = checkpoint.get("request_context")
            if isinstance(request_context, dict):
                self._request_context = request_context
        except Exception as e:
            self._log("warning", f"Failed to load latest checkpoint: {e}")

    def _get_available_tools(self) -> List[str]:
        return ["file_read", "file_write", "shell_exec", "web_search", "code_execution"]

    def _log(self, level: str, message: str):
        log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [{level.upper()}] {message}"
        if self.config.log_file:
            try:
                with open(self.config.log_file, "a", encoding="utf-8") as f:
                    f.write(log_entry + "\n")
            except Exception:
                pass

    def on_response(self, callback: Callable[[OrchestratorResponse], None]):
        self._on_response = callback

    def on_error(self, callback: Callable[[Exception, str], None]):
        self._on_error = callback


# ========== 便捷入口 ==========

async def create_orchestrator(spawn_func: Optional[Callable[..., Awaitable[Any]]] = None, **config_kwargs) -> OrchestratorV4ACP:
    config = OrchestratorConfig(**config_kwargs)
    orch = OrchestratorV4ACP(config, spawn_func=spawn_func)
    await orch.start()
    return orch


async def quick_ask(content: str, spawn_func: Optional[Callable[..., Awaitable[Any]]] = None, **kwargs) -> str:
    orch = await create_orchestrator(spawn_func=spawn_func, **kwargs)
    try:
        response = await orch.handle(content, **kwargs)
        return response.content
    finally:
        await orch.stop(graceful=False)
