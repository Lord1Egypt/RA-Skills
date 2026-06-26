"""
radial_memory/memory.py
─────────────────────────────────────────────────────────
核心类 RadialMemory：原点辐射状记忆体的完整实现。

关键设计：
  • 原点 (Origin)   — 始终在上下文，包含所有线的 L0 摘要
  • 线 (Line)       — 对应一个任务域/模块，节点按时间新→旧排列
  • 节点 (Node)     — position=1 最新最清晰，position 越大越旧越笼统
  • 载入导航        — 从原点出发，逐步从笼统向具体钻取，直到命中目标任务
  • 任务完成触发    — 由 agent 判断任务结束后主动调用 complete_task()
  • 非破坏性归档    — 旧节点永不删除，只升高 position（自动降一级默认精度）
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from .models import LEVELS, FileChange, Line, Node, Origin, StateSnapshot
from .storage import Storage
from .summarizer import BaseSummarizer, KeywordSummarizer


# ─────────────────────────────────────────────
# 导航会话：记录一次上下文载入过程的中间状态
# ─────────────────────────────────────────────

class NavigationSession:
    """
    一次从原点到目标节点的导航过程。
    agent 可以逐步调用 drill_deeper() 精化上下文，
    也可以直接用 context 属性获取当前已载入内容。

    使用方法::

        session = memory.start_navigation("认证模块 JWT 改造")
        print(session.context)          # 查看当前层级内容
        if session.needs_more_detail:
            session = session.drill_deeper()  # 向更具体层级钻取
    """

    def __init__(
        self,
        memory: "RadialMemory",
        node: Node,
        line_id: str,
        current_level: int,
        match_confidence: float,
    ):
        self._memory = memory
        self.node = node
        self.line_id = line_id
        self.current_level = current_level
        self.match_confidence = match_confidence
        self.context = self._build_context()

    @property
    def needs_more_detail(self) -> bool:
        return self.current_level < 4 and self.node.state is not None

    @property
    def is_full_state_loaded(self) -> bool:
        return self.current_level >= 4

    def drill_deeper(self) -> "NavigationSession":
        """
        向下一个抽象层级钻取，返回新的 NavigationSession。
        若已是最详细层级，直接返回自身。
        """
        if not self.needs_more_detail:
            return self
        next_level = min(self.current_level + 1, 4)
        return NavigationSession(
            memory=self._memory,
            node=self.node,
            line_id=self.line_id,
            current_level=next_level,
            match_confidence=self.match_confidence,
        )

    def load_full_state(self) -> str:
        """直接返回完整状态快照（L4），可注入 agent context window。"""
        if self.node.state:
            return self.node.state.full_context
        return self.context

    def _build_context(self) -> str:
        line = self._memory.origin.lines[self.line_id]
        parts = [
            "╔══ 已载入上下文 ══════════════════════════════",
            f"║ 项目:  {self._memory.origin.project_name}",
            f"║ 任务线: {line.name}  ({self.line_id})",
            f"║ 任务:  {self.node.task_label}",
            f"║ 时间:  {self.node.created_at[:16]}  [位置 pos={self.node.position}]",
            f"║ 匹配置信度: {self.match_confidence:.0%}  |  当前层级: L{self.current_level} ({LEVELS[self.current_level]['name']})",
            "╠══ 内容 ══════════════════════════════════════",
        ]

        # 输出从 L1 到 current_level 的所有摘要（逐层递进）
        for lvl in range(1, self.current_level + 1):
            level_name = LEVELS[lvl]["name"]
            if lvl == 4 and self.node.state:
                content = self.node.state.full_context
            else:
                content = self.node.summaries.get(lvl, "")
            if content:
                parts.append(f"║ [L{lvl} {level_name}]")
                # 缩进内容
                for line_text in content.splitlines():
                    parts.append(f"║   {line_text}")
                parts.append("║")

        # 附加文件变更和 TODO（L3+ 时显示）
        if self.current_level >= 3 and self.node.state:
            st = self.node.state
            if st.modified_files:
                parts.append("║ [变更文件]")
                for f in st.modified_files[:8]:
                    parts.append(f"║   {f.change_type:8s} {f.path}")
                    if f.diff_summary:
                        parts.append(f"║             → {f.diff_summary}")
                parts.append("║")
            if st.todos:
                parts.append("║ [未完成 TODOs]")
                for todo in st.todos:
                    parts.append(f"║   [ ] {todo}")
                parts.append("║")
            if st.env_info:
                parts.append(f"║ [环境] {st.env_info}")
                parts.append("║")

        # 历史累积摘要
        if self.node.accumulated_history_summary:
            parts.append("║ [前序历史摘要]")
            for line_text in self.node.accumulated_history_summary.splitlines():
                parts.append(f"║   {line_text}")

        parts.append("╚══════════════════════════════════════════════")
        return "\n".join(parts)


# ─────────────────────────────────────────────
# 主类：RadialMemory
# ─────────────────────────────────────────────

class RadialMemory:
    """
    原点辐射状 Agent 记忆系统。

    快速开始::

        mem = RadialMemory("./my_project_memory", project_name="电商推荐系统")

        # 创建任务线
        mem.create_line("auth", "认证模块", "用户认证、JWT、权限管理")

        # 任务完成后由 agent 调用
        mem.complete_task(
            line_id="auth",
            task_label="实现 JWT 登录接口",
            full_context="<完整上下文字符串>",
            conversation_summary="实现了 /login 接口，返回 access_token 和 refresh_token...",
            modified_files=[{"path": "auth/views.py", "change_type": "modified", "diff_summary": "新增 login() 视图函数"}],
            todos=["补充单元测试", "添加限流"],
        )

        # 始终注入上下文的原点概况
        print(mem.get_origin_context())

        # 从原点导航到目标任务
        session = mem.navigate("JWT 登录")
        print(session.context)
        if session.needs_more_detail:
            session = session.drill_deeper()
    """

    def __init__(
        self,
        storage_path: str,
        project_name: str = "Project",
        summarizer: Optional[BaseSummarizer] = None,
    ):
        self.storage = Storage(storage_path)
        self.summarizer = summarizer or KeywordSummarizer()

        origin = self.storage.load()
        if origin is None:
            origin = Origin(
                project_name=project_name,
                created_at=_now(),
                lines={},
            )
            self.storage.save(origin)
        self.origin = origin

    # ─────────────────────────────────────────────
    # 原点上下文（始终注入到 agent context window）
    # ─────────────────────────────────────────────

    def get_origin_context(self) -> str:
        """
        返回极紧凑的原点概况字符串。
        应始终存在于 agent 的 system prompt 或 context window 开头。
        """
        return self.origin.get_context()

    # ─────────────────────────────────────────────
    # 线管理
    # ─────────────────────────────────────────────

    def create_line(self, line_id: str, name: str, description: str) -> Line:
        """
        创建新任务线。
        line_id: 短标识符，如 "auth", "rec_engine", "infra"
        """
        if line_id in self.origin.lines:
            raise ValueError(f"任务线 '{line_id}' 已存在。如需获取，请用 get_line()。")
        line = Line(
            id=line_id,
            name=name,
            description=description,
            created_at=_now(),
            nodes=[],
        )
        self.origin.lines[line_id] = line
        self.storage.save(self.origin)
        return line

    def get_or_create_line(self, line_id: str, name: str, description: str) -> Line:
        """获取已有线，或在不存在时创建。"""
        if line_id not in self.origin.lines:
            return self.create_line(line_id, name, description)
        return self.origin.lines[line_id]

    def get_line(self, line_id: str) -> Line:
        if line_id not in self.origin.lines:
            raise KeyError(f"任务线 '{line_id}' 不存在。")
        return self.origin.lines[line_id]

    def list_lines(self) -> List[Dict]:
        """列出所有任务线的基本信息。"""
        return [
            {
                "id": lid,
                "name": line.name,
                "description": line.description,
                "node_count": len(line.nodes),
                "latest_task": line.nodes[0].task_label if line.nodes else None,
                "latest_at": line.nodes[0].created_at[:16] if line.nodes else None,
            }
            for lid, line in self.origin.lines.items()
        ]

    # ─────────────────────────────────────────────
    # 任务完成 → 生成节点（核心写入操作）
    # ─────────────────────────────────────────────

    def complete_task(
        self,
        line_id: str,
        task_label: str,
        full_context: str,
        conversation_summary: str,
        modified_files: Optional[List[Dict]] = None,
        env_info: Optional[Dict] = None,
        todos: Optional[List[str]] = None,
        precomputed_summaries: Optional[Dict[int, str]] = None,
    ) -> Node:
        """
        由 agent 在判断当前任务阶段性完成后调用。
        自动执行：
          1. 创建 StateSnapshot（L4 完整快照）
          2. 生成 L3→L2→L1→L0 各级摘要
          3. 构建累积历史摘要（含前序所有节点的精华）
          4. 将新节点插入线的 position=1（最靠近原点）
          5. 所有旧节点 position += 1（推远一格）
          6. 持久化

        Args:
            line_id:               目标任务线 ID
            task_label:            本次任务的简短名称（用于导航匹配）
            full_context:          完整上下文字符串（L4，可直接恢复工作状态）
            conversation_summary:  本次对话/工作的自然语言摘要
            modified_files:        变更文件列表，每项含 path/change_type/diff_summary
            env_info:              环境信息字典
            todos:                 未完成事项列表
            precomputed_summaries: 若 agent 自行生成了各级摘要，可直接传入 {1:…, 2:…, 3:…}
                                   传入后跳过自动摘要生成，节省 LLM 调用
        Returns:
            新创建的 Node 对象
        """
        if line_id not in self.origin.lines:
            raise ValueError(
                f"任务线 '{line_id}' 不存在。请先调用 create_line() 创建。"
            )

        line = self.origin.lines[line_id]

        # —— 1. 构建 StateSnapshot ——
        files = [
            FileChange(
                path=f["path"],
                change_type=f.get("change_type", "modified"),
                diff_summary=f.get("diff_summary", ""),
            )
            for f in (modified_files or [])
        ]
        state = StateSnapshot(
            conversation_summary=conversation_summary,
            modified_files=files,
            env_info=env_info or {},
            todos=todos or [],
            full_context=full_context,
        )

        # —— 2. 构建本节点的累积历史摘要 ——
        accumulated_history = _build_accumulated_history(line)

        # —— 3. 生成各级摘要 ——
        if precomputed_summaries:
            summaries = precomputed_summaries
            # 确保 L0 存在
            if 0 not in summaries:
                summaries[0] = self.summarizer.summarize(
                    summaries.get(1, task_label),
                    LEVELS[0]["max_chars"],
                    context_hint=task_label,
                )
        else:
            summaries = self._generate_summaries(
                state=state,
                task_label=task_label,
            )

        # —— 4. 更新累积历史摘要（存入新节点）——
        new_accumulated = self.summarizer.summarize(
            accumulated_history or task_label,
            max_chars=400,
            context_hint="任务历史摘要",
        )

        # —— 5. 创建新节点 ——
        node = Node(
            id=str(uuid.uuid4()),
            line_id=line_id,
            position=1,           # 最靠近原点
            created_at=_now(),
            task_label=task_label,
            summaries=summaries,
            state=state,
            accumulated_history_summary=new_accumulated,
        )

        # —— 6. 将旧节点推远（position += 1）——
        for old_node in line.nodes:
            old_node.position += 1

        # —— 7. 新节点置于最前 ——
        line.nodes.insert(0, node)

        # —— 8. 持久化 ——
        self.storage.save(self.origin)

        return node

    def extend_task(
        self,
        line_id: str,
        task_label: str,
        full_context: str,
        conversation_summary: str,
        modified_files: Optional[List[Dict]] = None,
        env_info: Optional[Dict] = None,
        todos: Optional[List[str]] = None,
        precomputed_summaries: Optional[Dict[int, str]] = None,
    ) -> Node:
        """
        对已有任务进行扩展/修改后调用（语义同 complete_task，
        但语义上表示「在原有工作基础上继续」）。
        新节点同样插入 position=1，旧节点被推远并在累积历史中保留。
        """
        return self.complete_task(
            line_id=line_id,
            task_label=task_label,
            full_context=full_context,
            conversation_summary=conversation_summary,
            modified_files=modified_files,
            env_info=env_info,
            todos=todos,
            precomputed_summaries=precomputed_summaries,
        )

    # ─────────────────────────────────────────────
    # 上下文导航（从原点出发寻找目标任务）
    # ─────────────────────────────────────────────

    def navigate(
        self,
        query: str,
        line_id: Optional[str] = None,
        initial_level: int = 1,
        confidence_threshold: float = 0.25,
    ) -> Optional[NavigationSession]:
        """
        从原点导航，找到与 query 最相关的任务节点，返回 NavigationSession。

        算法：
          1. 按 position 从小到大（新→旧）遍历候选节点
          2. 对每个节点用 L1（brief）做 verify_match
          3. 取置信度最高者，若超过阈值则返回 NavigationSession
          4. agent 可通过 session.drill_deeper() 继续钻取更高层级

        Args:
            query:                 自然语言任务描述
            line_id:               指定线 ID（None = 搜索全部线）
            initial_level:         初始载入层级（默认 L1，最省 token）
            confidence_threshold:  最低匹配置信度（低于此视为未找到）

        Returns:
            NavigationSession 或 None（未找到）
        """
        # 确定候选线
        if line_id:
            if line_id not in self.origin.lines:
                return None
            candidates = [(line_id, self.origin.lines[line_id])]
        else:
            candidates = list(self.origin.lines.items())

        best_node: Optional[Node] = None
        best_line_id: Optional[str] = None
        best_confidence: float = 0.0

        for lid, line in candidates:
            # 从最新节点（position=1）向旧节点扫描
            for node in line.nodes:
                summary = node.summaries.get(1, node.task_label)
                is_match, confidence = self.summarizer.verify_match(query, summary)

                if confidence > best_confidence:
                    best_confidence = confidence
                    best_node = node
                    best_line_id = lid

                # 找到高置信度匹配立即停止当前线的扫描
                if is_match and confidence >= 0.7:
                    break

        if best_node is None or best_confidence < confidence_threshold:
            return None

        return NavigationSession(
            memory=self,
            node=best_node,
            line_id=best_line_id,
            current_level=initial_level,
            match_confidence=best_confidence,
        )

    def navigate_step_by_step(
        self,
        query: str,
        line_id: Optional[str] = None,
    ) -> "StepNavigator":
        """
        返回一个步进式导航器，适合 agent 手动控制每一步。

        使用方法::

            nav = memory.navigate_step_by_step("JWT 登录接口")
            result = nav.next()        # 获取下一个候选节点 (L1 摘要)
            while result:
                if agent_says_match(result.context):
                    result = result.drill_deeper()  # 钻取更多细节
                    break
                result = nav.next()    # 当前不符合，看下一个节点
        """
        return StepNavigator(self, query, line_id)

    # ─────────────────────────────────────────────
    # 查询与信息展示
    # ─────────────────────────────────────────────

    def get_line_history(self, line_id: str) -> List[Dict]:
        """返回某条线上所有节点的摘要列表（从新到旧）。"""
        line = self.get_line(line_id)
        return [
            {
                "position": n.position,
                "task_label": n.task_label,
                "created_at": n.created_at[:16],
                "l0_summary": n.summaries.get(0, ""),
                "l1_summary": n.summaries.get(1, ""),
            }
            for n in line.nodes
        ]

    def get_node(self, line_id: str, position: int) -> Optional[Node]:
        """直接按 position 获取节点（1=最新）。"""
        line = self.get_line(line_id)
        for n in line.nodes:
            if n.position == position:
                return n
        return None

    def load_node_context(
        self, line_id: str, position: int, level: int = 2
    ) -> str:
        """直接加载指定节点指定层级的上下文字符串。"""
        node = self.get_node(line_id, position)
        if node is None:
            return f"节点不存在: line={line_id}, position={position}"
        session = NavigationSession(
            memory=self,
            node=node,
            line_id=line_id,
            current_level=level,
            match_confidence=1.0,
        )
        return session.context

    # ─────────────────────────────────────────────
    # 内部工具
    # ─────────────────────────────────────────────

    def _generate_summaries(
        self,
        state: StateSnapshot,
        task_label: str,
    ) -> Dict[int, str]:
        """
        自底向上生成 L3→L2→L1→L0 四级摘要。
        L4（full_context）存于 state，不在此字典中。
        """
        # L3 源材料：对话摘要 + 文件变更 + TODO
        l3_parts = [state.conversation_summary]
        if state.modified_files:
            file_lines = "\n".join(
                f"  [{f.change_type}] {f.path}: {f.diff_summary}"
                for f in state.modified_files[:12]
            )
            l3_parts.append(f"变更文件:\n{file_lines}")
        if state.todos:
            l3_parts.append("TODOs: " + "; ".join(state.todos))
        l3_raw = "\n\n".join(l3_parts)

        l3 = self.summarizer.summarize(l3_raw, LEVELS[3]["max_chars"], task_label)
        l2 = self.summarizer.summarize(l3, LEVELS[2]["max_chars"], task_label)
        l1 = self.summarizer.summarize(l2, LEVELS[1]["max_chars"], task_label)
        l0 = self.summarizer.summarize(l1, LEVELS[0]["max_chars"], task_label)

        return {0: l0, 1: l1, 2: l2, 3: l3}


# ─────────────────────────────────────────────
# 步进导航器
# ─────────────────────────────────────────────

class StepNavigator:
    """
    手动控制的步进式导航器。
    适合 agent 自主判断每个节点是否匹配。
    """

    def __init__(
        self,
        memory: RadialMemory,
        query: str,
        line_id: Optional[str],
    ):
        self._memory = memory
        self._query = query
        # 构建候选列表：(line_id, node)，按 position 从小到大（新→旧）
        if line_id and line_id in memory.origin.lines:
            lines = [(line_id, memory.origin.lines[line_id])]
        else:
            lines = list(memory.origin.lines.items())

        self._candidates: List[Tuple[str, Node]] = []
        for lid, line in lines:
            for node in sorted(line.nodes, key=lambda n: n.position):
                self._candidates.append((lid, node))

        self._index = 0

    def next(self) -> Optional[NavigationSession]:
        """
        返回下一个候选节点的 L1 导航会话。
        若已遍历完所有节点则返回 None。
        """
        if self._index >= len(self._candidates):
            return None
        lid, node = self._candidates[self._index]
        self._index += 1
        return NavigationSession(
            memory=self._memory,
            node=node,
            line_id=lid,
            current_level=1,
            match_confidence=0.0,  # 步进模式下由 agent 自行判断
        )

    @property
    def remaining(self) -> int:
        return max(0, len(self._candidates) - self._index)


# ─────────────────────────────────────────────
# 内部辅助函数
# ─────────────────────────────────────────────

def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _build_accumulated_history(line: Line) -> str:
    """
    从线的当前最新节点提取累积历史摘要字符串，
    作为新节点 accumulated_history_summary 的原材料。
    """
    if not line.nodes:
        return ""
    latest = line.nodes[0]  # 当前最新节点
    prev_summary = latest.summaries.get(2, latest.summaries.get(1, latest.task_label))

    if latest.accumulated_history_summary:
        return (
            f"{latest.accumulated_history_summary}\n"
            f"[{latest.created_at[:10]} - {latest.task_label}]: {prev_summary}"
        )
    return f"[{latest.created_at[:10]} - {latest.task_label}]: {prev_summary}"
