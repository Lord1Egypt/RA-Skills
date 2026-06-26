"""
radial_memory/models.py
─────────────────────────────────────────────────────────
数据模型：原点 / 线 / 节点 / 状态快照

空间语义：
  Origin（原点）
    ├─ Line "auth"   nodes: [pos=1(最新/最详细), pos=2, pos=3(最旧/最笼统)]
    ├─ Line "rec"    nodes: [pos=1, ...]
    └─ ...

  节点 position 越小（靠近原点）= 越新 = 默认加载的层级细节越高
  节点 position 越大（远离原点）= 越旧 = 默认只展示笼统摘要

抽象层级（每个节点内部，从笼统→详细）：
  L0  origin_entry  ≤80字    始终存在于原点上下文
  L1  brief         ≤200字   导航时首次加载用于匹配验证
  L2  summary       ≤600字   钻取第一层
  L3  detailed      ≤1800字  钻取第二层
  L4  full          无限制   完整快照（存在 state.full_context）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ─────────────────────────────────────────────
# 抽象层级配置
# ─────────────────────────────────────────────

LEVELS: Dict[int, Dict] = {
    0: {"name": "origin_entry", "max_chars": 80},
    1: {"name": "brief",        "max_chars": 200},
    2: {"name": "summary",      "max_chars": 600},
    3: {"name": "detailed",     "max_chars": 1800},
    4: {"name": "full",         "max_chars": None},   # 无限制，存于 state.full_context
}


# ─────────────────────────────────────────────
# 状态快照：节点携带的完整可恢复状态
# ─────────────────────────────────────────────

@dataclass
class FileChange:
    """一次任务中发生变更的文件记录"""
    path: str
    change_type: str        # "modified" | "created" | "deleted"
    diff_summary: str       # 变更内容的自然语言摘要


@dataclass
class StateSnapshot:
    """
    完整状态快照：可用于瞬间恢复 agent 的工作上下文。
    存储于每个节点，对应 L4（最完整层级）。
    """
    conversation_summary: str           # 本次任务对话的自然语言摘要
    modified_files: List[FileChange] = field(default_factory=list)
    env_info: Dict = field(default_factory=dict)    # 环境信息（包版本、变量等）
    todos: List[str] = field(default_factory=list)  # 未完成事项
    full_context: str = ""              # 完整上下文字符串，可直接注入 context window


# ─────────────────────────────────────────────
# 节点：线上的一个时间戳状态点
# ─────────────────────────────────────────────

@dataclass
class Node:
    """
    线上的一个任务完成节点。

    position：
        1 = 最新（最靠近原点），detail 最高
        N = 越旧越远离原点，detail 越低

    summaries：
        多级摘要字典，key 为层级 0-3（L4 存在 state.full_context）
        {0: "80字", 1: "200字", 2: "600字", 3: "1800字"}

    accumulated_history_summary：
        本节点之前所有历史节点的累积摘要，
        让后续节点不必逐一加载历史即可感知全局演进。
    """
    id: str
    line_id: str
    position: int                           # 1=最近原点
    created_at: str                         # ISO 8601
    task_label: str                         # 用户可读的任务名称
    summaries: Dict[int, str] = field(default_factory=dict)
    state: Optional[StateSnapshot] = None
    accumulated_history_summary: str = ""   # 前序历史的累积摘要

    def get_summary(self, level: int) -> str:
        """
        获取指定层级的摘要。
        若该层级不存在，向上/向下寻找最近可用层级。
        """
        if level in self.summaries:
            return self.summaries[level]
        # 向下找最接近的层级
        for lvl in range(level - 1, -1, -1):
            if lvl in self.summaries:
                return self.summaries[lvl]
        return self.task_label


# ─────────────────────────────────────────────
# 线：某个任务域/模块的全部历史节点序列
# ─────────────────────────────────────────────

@dataclass
class Line:
    """
    一条线代表一个持续演进的任务域（如某模块、某功能领域）。
    nodes 按 position 排序：index 0 始终是最新节点（position=1）。
    """
    id: str
    name: str
    description: str
    created_at: str
    nodes: List[Node] = field(default_factory=list)

    @property
    def latest_node(self) -> Optional[Node]:
        return self.nodes[0] if self.nodes else None

    def get_origin_entry(self) -> str:
        """
        返回此线在原点上下文中的 L0 单行描述。
        始终占用极少 token，确保原点紧凑。
        """
        if not self.nodes:
            return f"[{self.name}] {self.description} — 暂无任务"
        latest = self.nodes[0]
        l0 = latest.summaries.get(0, latest.task_label)
        return f"[{self.name}] {l0}  (共{len(self.nodes)}个节点, 最新:{latest.created_at[:10]})"


# ─────────────────────────────────────────────
# 原点：始终在上下文中的项目级枢纽
# ─────────────────────────────────────────────

@dataclass
class Origin:
    """
    原点：整个记忆体的中心，始终以紧凑形式存在于 agent 上下文。
    包含所有线的 L0 摘要，token 消耗控制在 ~300 以内。
    """
    project_name: str
    created_at: str
    lines: Dict[str, Line] = field(default_factory=dict)

    def get_context(self) -> str:
        """
        生成始终注入上下文的原点概况字符串。
        格式紧凑，agent 看到后能立刻感知全局结构。
        """
        if not self.lines:
            return (
                f"【原点】项目: {self.project_name}\n"
                f"当前无任何任务线，可调用 create_line() 创建。"
            )

        lines_text = "\n".join(
            f"  {lid}: {line.get_origin_entry()}"
            for lid, line in self.lines.items()
        )
        return (
            f"【原点】项目: {self.project_name}\n"
            f"任务线总览 ({len(self.lines)} 条):\n"
            f"{lines_text}"
        )
