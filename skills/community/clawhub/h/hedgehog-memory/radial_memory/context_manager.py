"""
radial_memory/context_manager.py
─────────────────────────────────────────────────────────
ContextWindowManager：上下文窗口生命周期管理器

负责协调「清空上下文 → 仅注入原点 → 导航寻节点 → 100% 还原工作状态」
这个完整循环，是 RadialMemory 对 agent 暴露的最高层 API。

典型 agent 使用流程::

    cw = ContextWindowManager(memory)

    # 1. 切换任务 / 重启 agent 时：清空后获取最小化原点上下文
    minimal = cw.reset()          # 只注入原点，~200 token
    inject_to_agent(minimal)

    # 2. agent 收到用户问题，判断要恢复哪个任务
    result = cw.load("JWT 登录接口")
    if result.status == "found":
        inject_to_agent(result.context)   # 注入 L1 brief，让 agent 验证
        if agent_confirms_match():
            inject_to_agent(result.full_state)  # 注入 L4 完整状态
        else:
            result2 = result.drill_deeper_or_next()
            ...

    # 3. 任务完成，agent 主动触发保存
    cw.commit(
        line_id="auth",
        task_label="实现 JWT 登录",
        full_context=agent.get_full_context(),
        conversation_summary="...",
        modified_files=[...],
    )
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .memory import NavigationSession, RadialMemory
from .models import Node


# ─────────────────────────────────────────────
# 载入结果
# ─────────────────────────────────────────────

@dataclass
class LoadResult:
    """
    一次上下文载入的结果，包含当前层级的上下文内容和操作接口。

    status:
      "found"     — 找到匹配节点，context 已就绪
      "not_found" — 未找到匹配，建议创建新线或使用 step_navigator
    """
    status: str                          # "found" | "not_found"
    context: str = ""                    # 当前层级（L1~L4）的可注入上下文字符串
    full_state: str = ""                 # L4 完整状态（可直接还原工作现场）
    line_id: str = ""
    node: Optional[Node] = None
    match_confidence: float = 0.0
    current_level: int = 1
    can_drill_deeper: bool = False
    _session: Optional[NavigationSession] = field(default=None, repr=False)

    def drill_deeper(self) -> "LoadResult":
        """
        向更具体层级钻取，返回新的 LoadResult。
        若已是最详细层级则返回自身。
        """
        if not self._session or not self._session.needs_more_detail:
            return self
        new_session = self._session.drill_deeper()
        return _session_to_result(new_session)

    def load_full_state(self) -> str:
        """
        直接返回 L4 完整状态字符串（可直接注入 agent context window）。
        这是 100% 恢复工作现场的入口。
        """
        if self._session:
            return self._session.load_full_state()
        return self.full_state


# ─────────────────────────────────────────────
# 主类
# ─────────────────────────────────────────────

class ContextWindowManager:
    """
    上下文窗口生命周期管理器。

    管理两个核心状态：
      current_context_type:
        "origin"  — 当前上下文中只有原点（最小化状态）
        "node"    — 当前上下文已载入某个节点的状态
        "empty"   — 初始状态，尚未注入任何内容

      active_line_id / active_node_position:
        当前已载入的节点位置（仅 current_context_type == "node" 时有效）
    """

    def __init__(self, memory: RadialMemory):
        self.memory = memory
        self.current_context_type: str = "empty"
        self.active_line_id: Optional[str] = None
        self.active_node_position: Optional[int] = None

    # ─────────────────────────────────────────────
    # 核心操作 1：重置（清空 → 仅保留原点）
    # ─────────────────────────────────────────────

    def reset(self) -> str:
        """
        模拟「清空上下文窗口，仅注入原点」。

        返回应注入 agent context window 的原点字符串。
        token 消耗约 100~300，取决于任务线数量。

        agent 调用时机：
          • 切换到与当前任务无关的新任务时
          • 重启 / 新对话时
          • 显式要求「回到原点」时
        """
        self.current_context_type = "origin"
        self.active_line_id = None
        self.active_node_position = None
        return self._build_reset_context()

    # ─────────────────────────────────────────────
    # 核心操作 2：载入（导航 → 找节点 → 返回可注入内容）
    # ─────────────────────────────────────────────

    def load(
        self,
        query: str,
        line_id: Optional[str] = None,
        initial_level: int = 1,
        confidence_threshold: float = 0.25,
    ) -> LoadResult:
        """
        从原点出发，按 query 导航找到最匹配的节点，
        返回 LoadResult（含可直接注入 agent 的上下文字符串）。

        流程：
          1. 在记忆文件中查找匹配节点（不消耗上下文 token）
          2. 找到后返回 L1 brief 层级的 LoadResult
          3. agent 验证是否匹配后，可调用 result.drill_deeper() 获取更多细节
          4. result.load_full_state() 获取 L4 完整状态（100% 恢复现场）

        Args:
            query:               自然语言描述，如「JWT 登录接口」
            line_id:             指定线（None = 搜全部线）
            initial_level:       初始层级，默认 L1（最省 token）
            confidence_threshold: 匹配置信度阈值

        Returns:
            LoadResult，status="found" 或 "not_found"
        """
        session = self.memory.navigate(
            query=query,
            line_id=line_id,
            initial_level=initial_level,
            confidence_threshold=confidence_threshold,
        )

        if session is None:
            return LoadResult(
                status="not_found",
                context=(
                    f"【未找到匹配节点】查询: {query}\n"
                    f"建议：调用 create_line() 创建新任务线，"
                    f"或使用 navigate_step_by_step() 手动浏览所有节点。\n\n"
                    f"{self.memory.get_origin_context()}"
                ),
            )

        result = _session_to_result(session)
        self.current_context_type = "node"
        self.active_line_id = result.line_id
        self.active_node_position = result.node.position if result.node else None
        return result

    # ─────────────────────────────────────────────
    # 核心操作 3：直接按位置载入节点
    # ─────────────────────────────────────────────

    def load_node(
        self,
        line_id: str,
        position: int = 1,
        level: int = 2,
    ) -> LoadResult:
        """
        直接按 line_id + position 精确载入节点，无需导航匹配。
        适合 agent 已经知道要加载哪个节点的情况（如从原点索引里看到的）。

        Args:
            line_id:  任务线 ID
            position: 节点位置（1=最新，越大越旧）
            level:    初始载入层级（默认 L2）
        """
        node = self.memory.get_node(line_id, position)
        if node is None:
            return LoadResult(
                status="not_found",
                context=f"【节点不存在】line={line_id}, position={position}",
            )

        session = NavigationSession(
            memory=self.memory,
            node=node,
            line_id=line_id,
            current_level=level,
            match_confidence=1.0,
        )
        result = _session_to_result(session)
        self.current_context_type = "node"
        self.active_line_id = line_id
        self.active_node_position = position
        return result

    # ─────────────────────────────────────────────
    # 核心操作 4：提交任务完成（写入记忆节点）
    # ─────────────────────────────────────────────

    def commit(
        self,
        line_id: str,
        task_label: str,
        full_context: str,
        conversation_summary: str,
        modified_files: Optional[List[dict]] = None,
        env_info: Optional[dict] = None,
        todos: Optional[List[str]] = None,
        precomputed_summaries: Optional[dict] = None,
        is_extension: bool = False,
    ) -> Node:
        """
        agent 判断当前任务阶段性完成后调用，触发节点生成和持久化。

        这是整个循环的「写入」端点：
          完整状态 → 生成多级摘要 → 写入 JSON 文件 → 旧节点推远

        Args:
            line_id:               目标任务线 ID（若不存在会抛出 ValueError）
            task_label:            本次任务简称，用于导航匹配
            full_context:          完整可还原的上下文字符串（L4，不限长度）
            conversation_summary:  本次对话的自然语言摘要
            modified_files:        变更文件列表
            env_info:              环境信息
            todos:                 未完成事项
            precomputed_summaries: 若 agent 自行生成了各级摘要可直接传入
            is_extension:          True=在原有任务上继续扩展，语义上的区别，实现相同

        Returns:
            新创建的 Node 对象
        """
        node = self.memory.complete_task(
            line_id=line_id,
            task_label=task_label,
            full_context=full_context,
            conversation_summary=conversation_summary,
            modified_files=modified_files,
            env_info=env_info,
            todos=todos,
            precomputed_summaries=precomputed_summaries,
        )

        # 更新当前活跃节点状态
        self.current_context_type = "node"
        self.active_line_id = line_id
        self.active_node_position = 1  # 新节点始终在 position=1

        return node

    # ─────────────────────────────────────────────
    # 辅助：当前状态报告
    # ─────────────────────────────────────────────

    def status_report(self) -> str:
        """
        返回当前上下文窗口状态的简短报告。
        可用于 agent 的 system prompt 或调试输出。
        """
        lines = [
            f"【上下文管理器状态】",
            f"  上下文类型:  {self.current_context_type}",
        ]
        if self.current_context_type == "node":
            lines.append(f"  活跃线:     {self.active_line_id}")
            lines.append(f"  活跃节点:   position={self.active_node_position}")
            if self.active_line_id and self.active_node_position:
                node = self.memory.get_node(self.active_line_id, self.active_node_position)
                if node:
                    lines.append(f"  任务标签:   {node.task_label}")
        lines.append(f"\n{self.memory.get_origin_context()}")
        return "\n".join(lines)

    def _build_reset_context(self) -> str:
        """清空后仅注入原点的上下文字符串。"""
        return (
            "【上下文已重置：仅保留原点结构】\n"
            "当前上下文中没有任何任务节点的具体细节。\n"
            "调用 load(query) 按需载入目标任务状态。\n\n"
            + self.memory.get_origin_context()
        )


# ─────────────────────────────────────────────
# 内部辅助
# ─────────────────────────────────────────────

def _session_to_result(session: NavigationSession) -> LoadResult:
    full_state = ""
    if session.node and session.node.state:
        full_state = session.node.state.full_context
    return LoadResult(
        status="found",
        context=session.context,
        full_state=full_state,
        line_id=session.line_id,
        node=session.node,
        match_confidence=session.match_confidence,
        current_level=session.current_level,
        can_drill_deeper=session.needs_more_detail,
        _session=session,
    )
