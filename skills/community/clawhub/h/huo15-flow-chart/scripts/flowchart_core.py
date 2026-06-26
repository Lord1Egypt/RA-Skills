"""火一五流程图 — 数据模型 + YAML/JSON 解析 + Mermaid/PlantUML/DOT 代码生成。

支持的图表类型
==============

| 类型                 | 输出 DSL           | 典型用途 |
|--------------------|-------------------|----------|
| flowchart          | Mermaid flowchart  | 普通流程图（含分组 subgraph）|
| swimlane           | PlantUML activity  | 真·泳道图（按角色分栏）|
| swimlane_mermaid   | Mermaid subgraph   | 泳道风格（不需要 Java 时用）|
| sequence           | Mermaid sequence   | 时序图 |
| state              | Mermaid state v2   | 状态图 |
| gantt              | Mermaid gantt      | 甘特图 |
| er                 | Mermaid erDiagram  | ER 图 |
| class              | Mermaid classDiagram | UML 类图 |
| journey            | Mermaid journey    | 用户旅程 |
| pie                | Mermaid pie        | 饼图 |
| architecture       | Mermaid flowchart  | 系统架构（分层 + 分组） |
| c4_context         | Mermaid C4Context  | C4 上下文图 |
| c4_container       | Mermaid C4Container | C4 容器图 |
| mindmap            | Mermaid mindmap    | 简单思维导图（正经的用 huo15-mind-map）|

用 YAML 描述；具体字段按 type 不同而不同，见 SKILL.md 示例。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml  # type: ignore
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ----- 通用数据结构 -----


@dataclass
class Node:
    id: str
    label: str = ""
    shape: str = "rect"     # rect/round/stadium/diamond/hexagon/circle/cylinder/cloud/component
    lane: Optional[str] = None
    style_class: Optional[str] = None
    group: Optional[str] = None   # 分组名，用于 subgraph
    tier: Optional[str] = None    # architecture tier 分层名
    category: Optional[str] = None  # 1..5 或 c1..c5，用于分色（可视层级）


@dataclass
class Edge:
    src: str
    dst: str
    label: Optional[str] = None
    # solid / dashed / thick / dotted / bidir
    # v1.3.2 语义类型：success / warning / error / info（带配色）
    kind: str = "solid"
    style_class: Optional[str] = None
    semantic: Optional[str] = None  # success / warning / error / info / neutral


@dataclass
class Tier:
    id: str
    label: str = ""
    direction: str = ""     # 可选 override
    children: List[str] = field(default_factory=list)


@dataclass
class Group:
    id: str
    label: str = ""
    direction: str = ""     # 可选 override
    children: List[str] = field(default_factory=list)


@dataclass
class FlowChart:
    diagram_type: str = "flowchart"
    title: str = ""
    direction: str = "TB"
    nodes: List[Node] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)
    groups: List[Group] = field(default_factory=list)
    tiers: List[Tier] = field(default_factory=list)  # architecture 多层分层
    lanes: List[str] = field(default_factory=list)
    raw: Optional[str] = None   # 原样 Mermaid/DOT 代码时用
    extras: Dict[str, Any] = field(default_factory=dict)


# ----- 解析 -----


def parse(text_or_path: str, hint: str = "auto") -> FlowChart:
    """顶层解析。按 hint / 扩展名 / 内容特征分发。"""
    import os
    text = text_or_path
    if os.path.exists(text_or_path):
        with open(text_or_path, encoding="utf-8") as f:
            text = f.read()
        if hint == "auto":
            ext = os.path.splitext(text_or_path)[1].lower()
            hint = {".yaml": "yaml", ".yml": "yaml", ".json": "json",
                    ".mmd": "mermaid", ".mermaid": "mermaid",
                    ".puml": "plantuml", ".plantuml": "plantuml",
                    ".dot": "dot", ".gv": "dot"}.get(ext, "auto")
    if hint == "auto":
        stripped = text.lstrip()
        if stripped.startswith("{"):
            hint = "json"
        elif re.match(r"^(flowchart|graph|sequenceDiagram|stateDiagram|gantt|classDiagram|erDiagram|journey|pie|C4Context|C4Container|mindmap|%%\{init)", stripped):
            hint = "mermaid"
        elif stripped.startswith("@startuml") or stripped.startswith("@startsalt"):
            hint = "plantuml"
        elif stripped.startswith("digraph") or stripped.startswith("graph "):
            hint = "dot"
        else:
            hint = "yaml"

    if hint == "json":
        return parse_spec(json.loads(text))
    if hint == "yaml":
        if not HAS_YAML:
            raise RuntimeError("需要 PyYAML（pip install pyyaml）才能解析 YAML 规格文件")
        return parse_spec(yaml.safe_load(text))
    if hint == "mermaid":
        return FlowChart(diagram_type="mermaid_raw", raw=text)
    if hint == "plantuml":
        return FlowChart(diagram_type="plantuml_raw", raw=text)
    if hint == "dot":
        return FlowChart(diagram_type="dot_raw", raw=text)
    raise ValueError(f"未知输入类型：{hint}")


def parse_spec(spec: Dict[str, Any]) -> FlowChart:
    """从 dict（已解析的 YAML/JSON）构造 FlowChart。"""
    fc = FlowChart()
    fc.diagram_type = str(spec.get("type") or spec.get("diagram") or "flowchart").lower()
    fc.title = spec.get("title", "") or ""
    fc.direction = spec.get("direction", "TB")
    fc.extras = {k: v for k, v in spec.items() if k not in {
        "type", "diagram", "title", "direction", "nodes", "edges",
        "groups", "lanes", "relations"
    }}

    # 节点
    for n in spec.get("nodes", []) or []:
        if isinstance(n, str):
            fc.nodes.append(Node(id=n, label=n))
            continue
        fc.nodes.append(Node(
            id=n["id"],
            label=n.get("label", n["id"]),
            shape=n.get("shape", "rect"),
            lane=n.get("lane"),
            style_class=n.get("class"),
            group=n.get("group"),
            tier=n.get("tier"),
            category=n.get("category") or n.get("cat"),
        ))

    # 边（兼容 relations 别名）
    _SEMANTIC_KINDS = {"success", "warning", "error", "info", "neutral"}
    for e in (spec.get("edges") or spec.get("relations") or []):
        if isinstance(e, list):
            if len(e) == 2:
                fc.edges.append(Edge(src=e[0], dst=e[1]))
            elif len(e) >= 3:
                fc.edges.append(Edge(src=e[0], dst=e[1], label=e[2]))
            continue
        raw_kind = e.get("kind", "solid")
        semantic = e.get("semantic") or e.get("sem")
        # 允许把语义直接写在 kind 上：kind: success
        if not semantic and raw_kind in _SEMANTIC_KINDS:
            semantic = raw_kind
            raw_kind = "solid"
        fc.edges.append(Edge(
            src=e.get("from") or e.get("src") or e["source"],
            dst=e.get("to") or e.get("dst") or e["target"],
            label=e.get("label"),
            kind=raw_kind,
            style_class=e.get("class"),
            semantic=semantic,
        ))

    # 分层 / tiers
    for t in spec.get("tiers", []) or []:
        if isinstance(t, str):
            fc.tiers.append(Tier(id=t, label=t))
        else:
            fc.tiers.append(Tier(
                id=t["id"],
                label=t.get("label", t["id"]),
                direction=t.get("direction", ""),
                children=t.get("children", []) or t.get("nodes", []),
            ))

    # 分组 / 子图
    for g in spec.get("groups", []) or []:
        if isinstance(g, str):
            fc.groups.append(Group(id=g, label=g))
            continue
        fc.groups.append(Group(
            id=g["id"],
            label=g.get("label", g["id"]),
            direction=g.get("direction", ""),
            children=g.get("children", []) or g.get("nodes", []),
        ))

    # 泳道
    if "lanes" in spec:
        lanes = spec["lanes"]
        if lanes and isinstance(lanes[0], dict):
            for lane in lanes:
                fc.lanes.append(lane.get("name") or lane.get("id") or "")
                for step in lane.get("steps") or lane.get("nodes") or []:
                    if isinstance(step, str):
                        fc.nodes.append(Node(id=step, label=step, lane=lane.get("name")))
                    else:
                        fc.nodes.append(Node(
                            id=step["id"],
                            label=step.get("label", step["id"]),
                            shape=step.get("shape", "rect"),
                            lane=lane.get("name"),
                        ))
        else:
            fc.lanes = [str(l) for l in lanes]

    return fc


# ----- Mermaid 生成 -----


_MM_SHAPE = {
    "rect": ("[", "]"),
    "round": ("(", ")"),
    "stadium": ("([", "])"),
    "subroutine": ("[[", "]]"),
    "cylinder": ("[(", ")]"),
    "circle": ("((", "))"),
    "asymmetric": (">", "]"),
    "diamond": ("{", "}"),
    "hexagon": ("{{", "}}"),
    "parallelogram": ("[/", "/]"),
    "trapezoid": ("[/", "\\]"),
}

_MM_EDGE = {
    "solid":  "-->",
    "dashed": "-.->",
    "dotted": "-.->",
    "thick":  "==>",
    "bidir":  "<-->",
    "none":   "---",
}


# ----- Icon 字典（label 里 :name: 语法替换为 emoji） -----
# 覆盖流程图常见语义，贴近 Material / Lucide 图标集
_ICON_ALIASES: Dict[str, str] = {
    "user": "👤", "users": "👥", "person": "👤", "admin": "🛡️",
    "login": "🔑", "key": "🔑", "lock": "🔒", "unlock": "🔓",
    "security": "🛡️", "shield": "🛡️",
    "start": "🟢", "play": "▶️", "stop": "⏹️", "pause": "⏸️",
    "check": "✅", "cross": "❌", "success": "✅", "fail": "❌", "error": "❌",
    "warning": "⚠️", "info": "ℹ️", "question": "❓",
    "db": "💾", "database": "💾", "cache": "⚡", "storage": "🗄️",
    "cloud": "☁️", "api": "🔌", "server": "🖥️", "mobile": "📱",
    "web": "🌐", "browser": "🌐", "globe": "🌐",
    "mail": "✉️", "email": "✉️", "bell": "🔔",
    "search": "🔍", "edit": "✏️", "delete": "🗑️", "trash": "🗑️",
    "cart": "🛒", "pay": "💳", "card": "💳", "money": "💰", "coin": "🪙",
    "order": "📦", "box": "📦", "package": "📦", "ship": "🚚", "truck": "🚚",
    "deliver": "📬", "inbox": "📥", "outbox": "📤",
    "ai": "🤖", "bot": "🤖", "brain": "🧠",
    "chart": "📊", "graph": "📈", "analytics": "📊",
    "doc": "📄", "file": "📄", "folder": "📁",
    "clock": "⏰", "time": "⏱️", "calendar": "📅",
    "star": "⭐", "heart": "❤️", "like": "👍", "dislike": "👎",
    "fire": "🔥", "rocket": "🚀", "bulb": "💡", "tools": "🛠️", "gear": "⚙️",
    "settings": "⚙️", "config": "⚙️",
    "git": "🔀", "branch": "🔀", "merge": "🔀",
    "build": "🏗️", "deploy": "📦", "launch": "🚀",
    "test": "🧪", "bug": "🐛", "check_circle": "✅",
    "phone": "📞", "link": "🔗", "queue": "📮", "mq": "📮",
    "log": "📜", "doc_text": "📝",
    "china": "🇨🇳", "world": "🌍",
    "alarm": "🚨", "siren": "🚨",
}

_ICON_RE = re.compile(r":([a-z0-9_\-]+):")


def _expand_icons(text: str) -> str:
    """把 :icon_name: 替换为 emoji；未知 name 原样保留。

    支持多次出现；也允许与普通文字混排。
    """
    if not text or ":" not in text:
        return text
    def _repl(m):
        key = m.group(1).lower()
        return _ICON_ALIASES.get(key, m.group(0))
    return _ICON_RE.sub(_repl, text)


def _mm_label(label: str) -> str:
    if not label:
        return ""
    # 展开 :icon_name: → emoji（v1.3.2）
    label = _expand_icons(label)
    # Mermaid 特殊字符需要用引号包起来
    if any(c in label for c in "()[]{}|<>/\\\"\n"):
        safe = label.replace('"', '\\"').replace("\n", "<br/>")
        return f'"{safe}"'
    # 检测 emoji：常见 pictograph / 变体选择符 / symbol-like 范围
    # 避开 CJK 主区 (0x4E00-0x9FFF)
    for c in label:
        cp = ord(c)
        if (0x2600 <= cp <= 0x27BF  # miscellaneous symbols & dingbats
            or 0xFE00 <= cp <= 0xFE0F  # variation selectors
            or 0x1F300 <= cp <= 0x1FAFF  # emoji
            or 0x1F000 <= cp <= 0x1F02F  # mahjong/playing card
            or 0x1F0A0 <= cp <= 0x1F0FF):
            return f'"{label}"'
    return label


def _mm_node(n: Node) -> str:
    open_br, close_br = _MM_SHAPE.get(n.shape, _MM_SHAPE["rect"])
    return f"{n.id}{open_br}{_mm_label(n.label or n.id)}{close_br}"


def _mm_edge(e: Edge) -> str:
    arrow = _MM_EDGE.get(e.kind, _MM_EDGE["solid"])
    if e.label:
        label_part = f"|{_mm_label(e.label).strip('"')}|"
        return f"{e.src} {arrow}{label_part} {e.dst}"
    return f"{e.src} {arrow} {e.dst}"


def to_mermaid(fc: FlowChart, style_directive: str = "", style: Optional[Any] = None) -> str:
    """把 FlowChart 转成 Mermaid 代码。

    style_directive - `%%{init:...}%%` 那一行
    style           - Style 对象（可选，用于注入 decision / database 的 classDef）
    """
    if fc.diagram_type == "mermaid_raw":
        # 原样 Mermaid 代码，只在开头插入 style_directive
        raw = fc.raw or ""
        if style_directive and "%%{init" not in raw:
            return style_directive + "\n" + raw
        return raw

    t = fc.diagram_type
    body: List[str]

    if t in ("flowchart", "architecture", "swimlane_mermaid"):
        body = _mm_flowchart(fc)
    elif t == "sequence":
        body = _mm_sequence(fc)
    elif t == "state":
        body = _mm_state(fc)
    elif t == "gantt":
        body = _mm_gantt(fc)
    elif t == "er":
        body = _mm_er(fc)
    elif t == "class":
        body = _mm_class(fc)
    elif t == "journey":
        body = _mm_journey(fc)
    elif t == "pie":
        body = _mm_pie(fc)
    elif t in ("c4_context", "c4context"):
        body = _mm_c4(fc, "Context")
    elif t in ("c4_container", "c4container"):
        body = _mm_c4(fc, "Container")
    elif t == "mindmap":
        body = _mm_mindmap(fc)
    else:
        body = _mm_flowchart(fc)

    # 基于 style 注入的 decision / database / terminal / category classDef（仅 flowchart 家族）
    if style is not None and t in ("flowchart", "architecture", "swimlane_mermaid"):
        try:
            from styles import (
                decision_classdef, database_classdef,
                terminal_classdef, category_classdefs,
                semantic_colors,
            )
            auto = fc.extras.get("_auto_classdefs", {})
            decision_ids: List[str] = auto.get("decision_ids", []) or []
            database_ids: List[str] = auto.get("database_ids", []) or []
            terminal_ids: List[str] = auto.get("terminal_ids", []) or []
            cat_map: Dict[str, List[str]] = auto.get("category_map", {}) or {}
            sem_map: Dict[str, List[int]] = auto.get("semantic_edges", {}) or {}
            if decision_ids:
                body.append("    " + decision_classdef(style))
                for nid in decision_ids:
                    body.append(f"    class {nid} decision")
            if database_ids:
                body.append("    " + database_classdef(style))
                for nid in database_ids:
                    body.append(f"    class {nid} database")
            if terminal_ids:
                body.append("    " + terminal_classdef(style))
                for nid in terminal_ids:
                    body.append(f"    class {nid} terminal")
            if cat_map:
                for cls in category_classdefs(style):
                    body.append("    " + cls)
                for cid, ids in cat_map.items():
                    for nid in ids:
                        body.append(f"    class {nid} {cid}")
            # 语义边：linkStyle N stroke:#...,color:#...,stroke-width:2px
            if sem_map:
                colors = semantic_colors(style)
                for sem, idxs in sem_map.items():
                    col = colors.get(sem, style.line_color)
                    idx_list = ",".join(str(i) for i in idxs)
                    body.append(
                        f"    linkStyle {idx_list} "
                        f"stroke:{col},color:{col},stroke-width:2px"
                    )
        except Exception:
            pass

    # Mermaid 要求 frontmatter（---title---）必须位于文件最前；init 指令跟在其后。
    if body and body[0].startswith("---"):
        first_block = body[0]  # 例如 "---\ntitle: xxx\n---"
        rest = body[1:]
        if style_directive:
            return "\n".join([first_block, style_directive] + rest)
        return "\n".join([first_block] + rest)

    if style_directive:
        return "\n".join([style_directive] + body)
    return "\n".join(body)


def _mm_flowchart(fc: FlowChart) -> List[str]:
    lines = [f"flowchart {fc.direction}"]
    if fc.title:
        lines.insert(0, f"---\ntitle: {fc.title}\n---")

    # 收集需要特殊 classDef 的节点
    decision_ids = [n.id for n in fc.nodes if n.shape == "diamond"]
    database_ids = [n.id for n in fc.nodes if n.shape in ("cylinder",)]
    terminal_ids = [n.id for n in fc.nodes if n.shape == "stadium"]
    # category 分组：c1..c5
    category_map: Dict[str, List[str]] = {}
    for n in fc.nodes:
        if not n.category:
            continue
        key = str(n.category).strip().lower().lstrip("c")
        if key in ("1", "2", "3", "4", "5"):
            category_map.setdefault(f"c{key}", []).append(n.id)

    # tiers 优先（architecture 类型）；否则用 groups
    use_tiers = bool(fc.tiers) and fc.diagram_type == "architecture"
    if use_tiers:
        groups_by_id: Dict[str, Group] = {t.id: Group(id=t.id, label=t.label, direction=t.direction, children=t.children) for t in fc.tiers}
    else:
        groups_by_id = {g.id: g for g in fc.groups}

    grouped_nodes: Dict[str, List[Node]] = {g.id: [] for g in groups_by_id.values()}
    ungrouped: List[Node] = []

    for n in fc.nodes:
        key: Optional[str] = None
        if use_tiers:
            # architecture tiers：从 node.tier 取
            key = getattr(n, 'tier', None) or n.group
        elif fc.diagram_type == "swimlane_mermaid":
            key = n.lane
            if key and key not in groups_by_id:
                groups_by_id[key] = Group(id=key, label=key)
                grouped_nodes.setdefault(key, [])
        else:
            key = n.group
        if key and key in groups_by_id:
            grouped_nodes[key].append(n)
        else:
            ungrouped.append(n)

    # 先输出顶层节点
    for n in ungrouped:
        lines.append("    " + _mm_node(n))

    # 输出 subgraph
    for gid, g in groups_by_id.items():
        direction = g.direction or fc.direction
        title = g.label or gid
        lines.append(f"    subgraph {gid}[\"{title}\"]")
        if direction:
            lines.append(f"        direction {direction}")
        # children 列表里的 + grouped_nodes 里的
        children_ids = set(g.children)
        seen = set()
        for n in grouped_nodes.get(gid, []):
            lines.append("        " + _mm_node(n))
            seen.add(n.id)
        for cid in g.children:
            if cid in seen:
                continue
            # 这个 id 可能是先前声明过的顶层节点
            lines.append(f"        {cid}")
        lines.append("    end")

    # 边
    for e in fc.edges:
        lines.append("    " + _mm_edge(e))

    # classDef / class
    classes = {n.style_class for n in fc.nodes if n.style_class}
    for cls in sorted(c for c in classes if c):
        lines.append(f"    classDef {cls} fill:#f9f9f9,stroke:#999,stroke-width:1px")
    for n in fc.nodes:
        if n.style_class:
            lines.append(f"    class {n.id} {n.style_class}")

    # 语义边索引（edge 在 body 里是按 fc.edges 顺序输出的）
    semantic_edges: Dict[str, List[int]] = {}
    for idx, e in enumerate(fc.edges):
        if e.semantic:
            semantic_edges.setdefault(e.semantic, []).append(idx)

    # 自动 decision / database / terminal / category classDef（渲染阶段注入）
    fc.extras["_auto_classdefs"] = {
        "semantic_edges": semantic_edges,
        "decision_ids": decision_ids,
        "database_ids": database_ids,
        "terminal_ids": terminal_ids,
        "category_map": category_map,
    }

    return lines


def _mm_sequence(fc: FlowChart) -> List[str]:
    lines = ["sequenceDiagram"]
    if fc.title:
        lines.append(f"    title {fc.title}")
    # 节点看作 actor / participant
    for n in fc.nodes:
        role = "actor" if n.shape == "actor" else "participant"
        lines.append(f"    {role} {n.id} as {n.label or n.id}")
    for e in fc.edges:
        arrow = "->>" if e.kind != "dashed" else "-->>"
        lbl = (e.label or "").replace("\n", " ")
        lines.append(f"    {e.src}{arrow}{e.dst}: {lbl}")
    # extras 支持 notes/auto_number
    if fc.extras.get("auto_number"):
        lines.insert(1, "    autonumber")
    for note in fc.extras.get("notes", []) or []:
        pos = note.get("position", "over")
        over = note.get("over") or note.get("participant", "")
        txt = (note.get("text", "") or "").replace("\n", "<br/>")
        lines.append(f"    Note {pos} {over}: {txt}")
    return lines


def _mm_state(fc: FlowChart) -> List[str]:
    lines = ["stateDiagram-v2"]
    if fc.title:
        lines.insert(0, f"---\ntitle: {fc.title}\n---")
    if fc.direction:
        lines.append(f"    direction {fc.direction}")
    for n in fc.nodes:
        if n.label and n.label != n.id:
            lines.append(f"    {n.id} : {n.label}")
    for e in fc.edges:
        lbl = f" : {e.label}" if e.label else ""
        lines.append(f"    {e.src} --> {e.dst}{lbl}")
    return lines


def _mm_gantt(fc: FlowChart) -> List[str]:
    lines = ["gantt"]
    if fc.title:
        lines.append(f"    title {fc.title}")
    lines.append(f"    dateFormat {fc.extras.get('dateFormat', 'YYYY-MM-DD')}")
    if "axisFormat" in fc.extras:
        lines.append(f"    axisFormat {fc.extras['axisFormat']}")
    # sections / tasks
    sections = fc.extras.get("sections") or []
    if sections:
        for sec in sections:
            lines.append(f"    section {sec.get('name', '')}")
            for task in sec.get("tasks", []):
                _gantt_task(lines, task)
    else:
        for task in fc.extras.get("tasks", []) or []:
            _gantt_task(lines, task)
    return lines


def _gantt_task(lines: List[str], task: Dict[str, Any]) -> None:
    def _s(v: Any) -> str:
        if v is None:
            return ""
        if hasattr(v, "strftime"):  # datetime.date / datetime
            return v.strftime("%Y-%m-%d")
        return str(v)
    name = _s(task.get("name", ""))
    tid = _s(task.get("id", ""))
    status = _s(task.get("status", ""))
    start = _s(task.get("start", ""))
    dur = _s(task.get("duration", task.get("end", "")))
    parts = [p for p in [status, tid, start, dur] if p]
    lines.append(f"    {name} :{', '.join(parts)}")


def _mm_er(fc: FlowChart) -> List[str]:
    lines = ["erDiagram"]
    if fc.title:
        lines.insert(0, f"---\ntitle: {fc.title}\n---")
    # 节点 = 实体；label 可附带字段
    for n in fc.nodes:
        fields = n.label.split("\n") if "\n" in n.label else []
        if len(fields) > 1:
            lines.append(f"    {n.id} {{")
            for f in fields[1:]:
                lines.append(f"        {f}")
            lines.append("    }")
    for e in fc.edges:
        relation = e.kind if e.kind != "solid" else "||--o{"
        lbl = e.label or "relates to"
        lines.append(f"    {e.src} {relation} {e.dst} : \"{lbl}\"")
    return lines


def _mm_class(fc: FlowChart) -> List[str]:
    lines = ["classDiagram"]
    if fc.title:
        lines.insert(0, f"---\ntitle: {fc.title}\n---")
    if fc.direction:
        lines.append(f"    direction {fc.direction}")
    for n in fc.nodes:
        if "\n" in n.label:
            parts = n.label.split("\n")
            lines.append(f"    class {n.id} {{")
            for p in parts[1:]:
                lines.append(f"        {p}")
            lines.append("    }")
        else:
            lines.append(f"    class {n.id}")
    for e in fc.edges:
        rel = {
            "extends": "<|--",
            "implements": "<|..",
            "composition": "*--",
            "aggregation": "o--",
            "dependency": "..>",
            "association": "-->",
        }.get(e.kind, "-->")
        lbl = f" : {e.label}" if e.label else ""
        lines.append(f"    {e.src} {rel} {e.dst}{lbl}")
    return lines


def _mm_journey(fc: FlowChart) -> List[str]:
    lines = ["journey"]
    if fc.title:
        lines.append(f"    title {fc.title}")
    for section in fc.extras.get("sections", []) or []:
        lines.append(f"    section {section.get('name', '')}")
        for task in section.get("tasks", []) or []:
            lines.append(f"      {task['name']}: {task.get('score', 3)}: {', '.join(task.get('actors', []))}")
    return lines


def _mm_pie(fc: FlowChart) -> List[str]:
    lines = ["pie" + (" showData" if fc.extras.get("show_data") else "")]
    if fc.title:
        lines.append(f"    title {fc.title}")
    for item in fc.extras.get("items", []) or []:
        lines.append(f"    \"{item['name']}\" : {item['value']}")
    return lines


def _mm_c4(fc: FlowChart, level: str) -> List[str]:
    lines = [f"C4{level}"]
    if fc.title:
        lines.append(f"    title {fc.title}")
    # 节点：shape 用 Person / System / System_Ext / Container / Db / ContainerDb
    shape_to_kind = {
        "person": "Person",
        "person_ext": "Person_Ext",
        "system": "System",
        "system_ext": "System_Ext",
        "container": "Container",
        "container_db": "ContainerDb",
        "component": "Component",
        "db": "ContainerDb",
    }
    for n in fc.nodes:
        kind = shape_to_kind.get(n.shape.lower(), "System")
        desc = ""
        if "\n" in n.label:
            parts = n.label.split("\n", 1)
            lbl, desc = parts[0], parts[1]
        else:
            lbl = n.label or n.id
        desc_part = f', "{desc}"' if desc else ""
        lines.append(f'    {kind}({n.id}, "{lbl}"{desc_part})')
    for e in fc.edges:
        lbl = e.label or ""
        lines.append(f'    Rel({e.src}, {e.dst}, "{lbl}")')
    return lines


def _mm_mindmap(fc: FlowChart) -> List[str]:
    lines = ["mindmap"]
    # 简化：假定第一个 node 是根，其他都是根的 child（不处理多级）
    if not fc.nodes:
        return lines
    root = fc.nodes[0]
    lines.append(f"  root(({root.label or root.id}))")
    # 按 edges 建父子关系
    children: Dict[str, List[str]] = {}
    for e in fc.edges:
        children.setdefault(e.src, []).append(e.dst)
    node_by_id = {n.id: n for n in fc.nodes}

    def _render(nid: str, depth: int) -> None:
        for cid in children.get(nid, []):
            node = node_by_id.get(cid)
            label = node.label if node else cid
            lines.append("  " * (depth + 1) + label)
            _render(cid, depth + 1)

    _render(root.id, 1)
    return lines


# ----- PlantUML 生成（真·泳道图） -----


def to_plantuml(fc: FlowChart, style_skinparam: str = "") -> str:
    if fc.diagram_type == "plantuml_raw":
        return fc.raw or ""

    if fc.diagram_type == "swimlane":
        return _puml_swimlane(fc, style_skinparam)
    if fc.diagram_type == "sequence":
        return _puml_sequence(fc, style_skinparam)
    if fc.diagram_type in ("c4_context", "c4context", "c4_container", "c4container"):
        return _puml_c4(fc, style_skinparam)
    # fallback：让 Mermaid 干
    raise ValueError(f"PlantUML 当前只支持 swimlane/sequence/c4；请用 type: swimlane_mermaid 等走 Mermaid。")


def _puml_swimlane(fc: FlowChart, skin: str) -> str:
    out = ["@startuml"]
    if skin:
        out.append(skin)
    if fc.title:
        out.append(f"title {fc.title}")

    # 按 lane 分组
    lane_order = fc.lanes or []
    if not lane_order:
        lane_order = list(dict.fromkeys([n.lane for n in fc.nodes if n.lane]))

    lane_nodes: Dict[str, List[Node]] = {l: [] for l in lane_order}
    for n in fc.nodes:
        if n.lane in lane_nodes:
            lane_nodes[n.lane].append(n)

    # 构建 id → node 映射与 children 图
    node_by_id = {n.id: n for n in fc.nodes}
    successors: Dict[str, List[Tuple[str, Optional[str]]]] = {}
    for e in fc.edges:
        successors.setdefault(e.src, []).append((e.dst, e.label))

    out.append("start")
    visited = set()

    def _activity_body(n: Node) -> str:
        if n.shape == "diamond":
            return f"if ({n.label or n.id}?) then"
        return f":{n.label or n.id};"

    # 按 lane 顺序，深度优先走边
    first = fc.nodes[0] if fc.nodes else None
    cursor = first
    cur_lane: Optional[str] = None
    while cursor and cursor.id not in visited:
        visited.add(cursor.id)
        if cursor.lane and cursor.lane != cur_lane:
            out.append(f"|{cursor.lane}|")
            cur_lane = cursor.lane
        out.append(_activity_body(cursor))
        nexts = successors.get(cursor.id, [])
        if not nexts:
            break
        # 只线性前进（复杂分支建议用原生 PlantUML 写）
        nxt_id, lbl = nexts[0]
        if lbl:
            out.append(f"note right: {lbl}")
        cursor = node_by_id.get(nxt_id)

    out.append("stop")
    out.append("@enduml")
    return "\n".join(out)


def _puml_sequence(fc: FlowChart, skin: str) -> str:
    out = ["@startuml"]
    if skin:
        out.append(skin)
    if fc.title:
        out.append(f"title {fc.title}")
    for n in fc.nodes:
        role = "actor" if n.shape == "actor" else "participant"
        out.append(f'{role} "{n.label or n.id}" as {n.id}')
    for e in fc.edges:
        arrow = "-->" if e.kind == "dashed" else "->"
        lbl = f" : {e.label}" if e.label else ""
        out.append(f"{e.src} {arrow} {e.dst}{lbl}")
    out.append("@enduml")
    return "\n".join(out)


def _puml_c4(fc: FlowChart, skin: str) -> str:
    """C4-PlantUML 生成器（Person/System/Container/Rel）。"""
    level = "Context" if fc.diagram_type in ("c4_context", "c4context") else "Container"
    out = ["@startuml"]
    if skin:
        out.append(skin)
    if fc.title:
        out.append(f"title {fc.title}")

    shape_to_c4 = {
        "person": "Person",
        "person_ext": "Person_Ext",
        "system": "System",
        "system_ext": "System_Ext",
        "container": "Container",
        "container_db": "ContainerDb",
        "db": "ContainerDb",
        "component": "Component",
    }

    for n in fc.nodes:
        kind = shape_to_c4.get(n.shape.lower(), "System")
        if "\n" in n.label:
            parts = n.label.split("\n", 1)
            lbl, desc = parts[0], parts[1]
        else:
            lbl = n.label or n.id
            desc = ""

        if desc:
            out.append(f'{kind}({n.id}, "{lbl}", "{desc}")')
        else:
            # Try to detect technology from group or extras
            tech = fc.extras.get("technologies", {}).get(n.id, "")
            if tech:
                out.append(f'{kind}({n.id}, "{lbl}", "{tech}")')
            else:
                out.append(f'{kind}({n.id}, "{lbl}")')

    for e in fc.edges:
        lbl = e.label or ""
        # C4-PlantUML Rel 支持方向：Left/Right/Up/Down
        out.append(f'Rel({e.src}, {e.dst}, "{lbl}")')

    out.append("@enduml")
    return "\n".join(out)


# ----- Graphviz DOT 生成（复杂网络拓扑、系统架构备选） -----


def to_dot(fc: FlowChart, style: Optional[Any] = None) -> str:
    """把 FlowChart 转成 Graphviz DOT 代码。用于网络拓扑 / 架构备选。"""
    from styles import Style  # 避免循环

    if fc.diagram_type == "dot_raw":
        return fc.raw or ""

    lines = ["digraph G {"]
    lines.append(f'  rankdir={fc.direction if fc.direction in ("TB","BT","LR","RL") else "TB"};')
    lines.append('  node [shape=box, style="rounded,filled", fontname="PingFang SC"];')
    if style:
        lines.append(f'  bgcolor="{style.background}";')
        lines.append(f'  node [fillcolor="{style.primary_color}", fontcolor="{style.primary_text_color}", color="{style.primary_border_color}"];')
        lines.append(f'  edge [color="{style.line_color}", fontname="PingFang SC"];')
    if fc.title:
        lines.append(f'  label="{fc.title}"; labelloc=t; fontsize=18;')

    # 分组
    for g in fc.groups:
        lines.append(f'  subgraph cluster_{g.id} {{')
        lines.append(f'    label="{g.label}";')
        lines.append('    style="rounded,filled"; fillcolor="#F5F5F5";')
        for cid in g.children:
            lines.append(f"    {cid};")
        lines.append("  }")

    for n in fc.nodes:
        attrs = [f'label="{n.label or n.id}"']
        if n.shape in ("cylinder", "cylinder"):
            attrs.append('shape=cylinder')
        elif n.shape == "diamond":
            attrs.append('shape=diamond')
        elif n.shape == "circle":
            attrs.append('shape=circle')
        lines.append(f"  {n.id} [{', '.join(attrs)}];")
    for e in fc.edges:
        attrs = []
        if e.label:
            attrs.append(f'label="{e.label}"')
        if e.kind == "dashed":
            attrs.append('style=dashed')
        attr_str = f" [{', '.join(attrs)}]" if attrs else ""
        lines.append(f"  {e.src} -> {e.dst}{attr_str};")
    lines.append("}")
    return "\n".join(lines)


# ----- draw.io XML 生成（支持导出 .drawio 源文件） -----

_DRAWIO_SHAPE = {
    "rect": "rectangle",
    "round": "rectangle",      # 用 rounded=1 参数表达圆角
    "stadium": "rectangle",    # 半圆端 via arcSize=50
    "subroutine": "process",
    "cylinder": "cylinder",
    "circle": "ellipse",
    "asymmetric": "rectangle",
    "diamond": "rhombus",
    "hexagon": "hexagon",
    "parallelogram": "parallelogram",
    "trapezoid": "trapezoid",
    "person": "umlActor",
    "person_ext": "umlActor",
    "system": "rectangle",
    "system_ext": "rectangle",
    "container": "rectangle",
    "container_db": "cylinder",
    "db": "cylinder",
    "component": "component",
}


def _dx_escape(s: str) -> str:
    """转义 XML 特殊字符。"""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&apos;"))


def _dx_style(shape: str, params: Dict[str, str]) -> str:
    """把形状 + 样式参数序列化成 draw.io style 字符串。"""
    shape_type = _DRAWIO_SHAPE.get(shape, "rectangle")
    base: Dict[str, str] = {
        "shape": shape_type,
        "whiteSpace": "wrap",
        "html": "1",
        "align": "center",
        "verticalAlign": "middle",
        "spacing": "4",
    }
    # 圆角策略
    if shape in ("round", "stadium"):
        base["rounded"] = "1"
        base["arcSize"] = "45" if shape == "stadium" else "20"
    elif shape in ("rect", "system", "system_ext", "container", "subroutine"):
        base["rounded"] = "1"
        base["arcSize"] = "12"
    base.update(params)
    return ";".join(f"{k}={v}" for k, v in base.items() if v != "")


def to_drawio(fc: FlowChart, style: Optional[Any] = None,
               theme: str = "modern",
               font_family: Optional[str] = None,
               shadow: bool = True) -> str:
    """把 FlowChart 转成 draw.io .drawio XML（现代风格：渐变 + 圆角 + 阴影 + 弧形正交连线）。"""
    # 字体与配色
    ff = font_family or (
        style.font_family.split(",")[0].strip('"') if style else "PingFang SC"
    )
    if style:
        fill = style.primary_color
        stroke = style.primary_border_color
        font_color = style.primary_text_color
        bg = style.background
        line = style.line_color
        accent = style.accent_color
        grad_start = getattr(style, "gradient_start", "") or ""
        grad_end = getattr(style, "gradient_end", "") or ""
        corner = getattr(style, "corner_radius", 12)
        sw = getattr(style, "stroke_width", 1.6)
        sec = style.secondary_color
        tert = style.tertiary_color
    else:
        fill, stroke, font_color = "#1E293B", "#0F172A", "#FFFFFF"
        bg, line, accent = "#FAFAFA", "#64748B", "#6366F1"
        grad_start, grad_end = "", ""
        corner, sw = 12, 1.6
        sec, tert = "#F1F5F9", "#E2E8F0"

    # 形状专用的 fill 选择：判断节点用 accent，数据库/容器用 secondary
    def node_colors(shape: str) -> Dict[str, str]:
        if shape == "diamond":
            return {"fill": accent, "text": "#FFFFFF", "stroke": accent}
        if shape in ("cylinder", "container_db", "db"):
            return {"fill": sec, "text": stroke, "stroke": tert}
        if shape in ("system_ext", "person_ext"):
            return {"fill": tert, "text": stroke, "stroke": line}
        return {"fill": fill, "text": font_color, "stroke": stroke}

    # 布局：tiers 优先，否则 groups，否则单列网格
    tier_list = [t.id for t in fc.tiers] if fc.tiers else []
    group_list = [g.id for g in fc.groups] if fc.groups else []
    uses_tiers = bool(tier_list)
    container_list = tier_list if uses_tiers else group_list

    # 把节点按 container 分桶（tier/group/ungrouped）
    bucket: Dict[str, List[Node]] = {cid: [] for cid in container_list}
    ungrouped: List[Node] = []
    for n in fc.nodes:
        k = getattr(n, "tier", None) if uses_tiers else n.group
        if k and k in bucket:
            bucket[k].append(n)
        else:
            ungrouped.append(n)

    # 计算容器 & 节点坐标
    NODE_W, NODE_H = 200, 72
    H_GAP, V_GAP = 48, 56
    C_PAD = 28                      # 容器内边距
    C_HEAD = 40                     # 容器 header 高度
    START_X, START_Y = 48, 64

    pos: Dict[str, Tuple[int, int]] = {}
    container_rect: Dict[str, Tuple[int, int, int, int]] = {}  # id -> (x,y,w,h)

    cur_y = START_Y
    if container_list:
        # 所有容器里节点数量最多的 → 决定容器宽度
        max_cols = max((len(bucket.get(cid, [])) for cid in container_list), default=1)
        max_cols = max(max_cols, 1)
        content_w = max_cols * NODE_W + (max_cols - 1) * H_GAP
        container_w = content_w + C_PAD * 2
        for cid in container_list:
            rows = bucket.get(cid, [])
            # 分行：每行至多 max_cols 个
            n_rows = max(1, (len(rows) + max_cols - 1) // max_cols) if rows else 1
            container_h = C_HEAD + n_rows * NODE_H + (n_rows - 1) * V_GAP + C_PAD * 2 - C_PAD
            container_rect[cid] = (START_X, cur_y, container_w, container_h)
            # 节点位置相对画布
            for i, n in enumerate(rows):
                row = i // max_cols
                col = i % max_cols
                x = START_X + C_PAD + col * (NODE_W + H_GAP)
                y = cur_y + C_HEAD + row * (NODE_H + V_GAP)
                pos[n.id] = (x, y)
            cur_y += container_h + V_GAP

    # ungrouped 节点一行排
    if ungrouped:
        ug_cols = max(1, min(len(ungrouped), 4))
        for i, n in enumerate(ungrouped):
            row = i // ug_cols
            col = i % ug_cols
            x = START_X + col * (NODE_W + H_GAP)
            y = cur_y + row * (NODE_H + V_GAP)
            pos[n.id] = (x, y)

    # 若仍没有任何节点位置（诡异情况）给个默认
    for n in fc.nodes:
        if n.id not in pos:
            idx = fc.nodes.index(n)
            pos[n.id] = (START_X + (idx % 4) * (NODE_W + H_GAP),
                         START_Y + (idx // 4) * (NODE_H + V_GAP))

    # 分配 cell id
    CELL_ROOT = 1
    next_id = [2]

    def alloc() -> int:
        nid = next_id[0]
        next_id[0] += 1
        return nid

    container_cell: Dict[str, int] = {}
    node_cell: Dict[str, int] = {}

    # ---- 输出 XML ----
    shadow_flag = "1" if shadow else "0"
    diag_name = _dx_escape(fc.title) if fc.title else "FlowChart"
    lines: List[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<mxfile host="huo15-flow-chart" modified="2026-04-24" agent="huo15-flow-chart/1.3.3" version="24.0.0">',
        f'  <diagram name="{diag_name}" id="huo15-fc">',
        f'    <mxGraphModel dx="1600" dy="1100" grid="1" gridSize="10" guides="1" '
        f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" math="0" shadow="{shadow_flag}">',
        '      <root>',
        '        <mxCell id="0" />',
        f'        <mxCell id="{CELL_ROOT}" parent="0" />',
    ]

    # 容器（tier/group）cell
    for cid in container_list:
        rect = container_rect.get(cid)
        if not rect:
            continue
        x, y, w, h = rect
        label_text = ""
        if uses_tiers:
            tobj = next((t for t in fc.tiers if t.id == cid), None)
            label_text = (tobj.label if tobj else cid) or cid
        else:
            gobj = next((g for g in fc.groups if g.id == cid), None)
            label_text = (gobj.label if gobj else cid) or cid
        cell_no = alloc()
        container_cell[cid] = cell_no
        container_style = ";".join([
            "rounded=1",
            f"arcSize={corner + 4}",
            f"fillColor={sec}",
            f"strokeColor={tert}",
            f"strokeWidth={max(sw - 0.4, 1.0)}",
            f"fontColor={stroke}",
            "fontSize=14",
            "fontStyle=1",
            "verticalAlign=top",
            "align=left",
            "spacingTop=8",
            "spacingLeft=14",
            "dashed=0",
            f"shadow={shadow_flag}",
            "container=1",
            "collapsible=0",
            f"fontFamily={ff}",
        ])
        lines.append(
            f'        <mxCell id="{cell_no}" value="{_dx_escape(label_text)}" '
            f'style="{container_style}" vertex="1" parent="{CELL_ROOT}">'
        )
        lines.append(
            f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />'
        )
        lines.append('        </mxCell>')

    # 节点 cell
    for n in fc.nodes:
        x, y = pos[n.id]
        container_id = (getattr(n, "tier", None) if uses_tiers else n.group)
        parent_cell = container_cell.get(container_id or "", CELL_ROOT)
        # 子单元坐标相对父容器
        if parent_cell != CELL_ROOT and container_id in container_rect:
            cx, cy, _, _ = container_rect[container_id]
            nx, ny = x - cx, y - cy
        else:
            nx, ny = x, y

        colors = node_colors(n.shape)
        node_style_map: Dict[str, str] = {
            "fillColor": colors["fill"],
            "strokeColor": colors["stroke"],
            "fontColor": colors["text"],
            "fontFamily": ff,
            "fontSize": "13",
            "fontStyle": "1",
            "strokeWidth": str(sw),
            "shadow": shadow_flag,
        }
        # 渐变（仅当 style 提供了渐变起止色，且形状是"实心"节点时）
        if grad_start and grad_end and n.shape not in ("cylinder", "container_db", "db",
                                                        "system_ext", "person_ext"):
            node_style_map["fillColor"] = grad_start
            node_style_map["gradientColor"] = grad_end
            node_style_map["gradientDirection"] = "north"

        style_str = _dx_style(n.shape, node_style_map)
        cell_no = alloc()
        node_cell[n.id] = cell_no
        label = _dx_escape(n.label or n.id)
        lines.append(
            f'        <mxCell id="{cell_no}" value="{label}" '
            f'style="{style_str}" vertex="1" parent="{parent_cell}">'
        )
        lines.append(
            f'          <mxGeometry x="{nx}" y="{ny}" width="{NODE_W}" height="{NODE_H}" as="geometry" />'
        )
        lines.append('        </mxCell>')

    # 边 cell —— 现代：正交弧线 + 配色
    for e in fc.edges:
        src = node_cell.get(e.src)
        dst = node_cell.get(e.dst)
        if src is None or dst is None:
            continue
        edge_map: Dict[str, str] = {
            "edgeStyle": "orthogonalEdgeStyle",
            "rounded": "1",
            "curved": "0",
            "arcSize": "12",
            "strokeColor": line,
            "strokeWidth": str(sw),
            "fontColor": stroke,
            "fontSize": "12",
            "fontFamily": ff,
            "labelBackgroundColor": bg,
            "html": "1",
            "endArrow": "classic",
            "endFill": "1",
            "jettySize": "auto",
            "orthogonalLoop": "1",
        }
        if e.kind == "dashed" or e.kind == "dotted":
            edge_map["dashed"] = "1"
        elif e.kind == "thick":
            edge_map["strokeWidth"] = str(sw + 1.5)
        elif e.kind == "bidir":
            edge_map["startArrow"] = "classic"
            edge_map["startFill"] = "1"
        edge_style = ";".join(f"{k}={v}" for k, v in edge_map.items())
        cell_no = alloc()
        label = _dx_escape(e.label or "")
        lines.append(
            f'        <mxCell id="{cell_no}" value="{label}" style="{edge_style}" '
            f'edge="1" parent="{CELL_ROOT}" source="{src}" target="{dst}">'
        )
        lines.append(
            '          <mxGeometry relative="1" as="geometry" />'
        )
        lines.append('        </mxCell>')

    lines.extend([
        '      </root>',
        '    </mxGraphModel>',
        '  </diagram>',
        '</mxfile>',
    ])
    return "\n".join(lines)
