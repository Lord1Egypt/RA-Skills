# gbrain_bridge.py
# Neuro-Agent × gbrain 融合层
# 用 gbrain 替代文件存储作为唯一记忆载体，Neuro 只保留情绪处理逻辑
#
# 融合思路：
# - gbrain pages = 记忆事实（what happened）
# - emotional_metadata = 情绪注释（what it meant to me）
# - Neuro limbic/prefrontal = 情绪处理 + 决策
# - 两者结合：事实 + 意义 = 完整的记忆

import subprocess
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

BRAIN_PATH = Path.home() / "brain"

def _run(cmd: List[str], input_text: str = None) -> Dict[str, Any]:
    """执行 gbrain CLI 命令"""
    env = os.environ.copy()
    env["PATH"] = f"{Path.home() / '.bun' / 'bin'}:{env.get('PATH', '')}"

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        input=input_text,
        cwd=str(BRAIN_PATH),
        env=env
    )

    if result.returncode != 0 and "already exists" not in result.stderr and "not found" not in result.stderr.lower():
        print(f"gbrain: {' '.join(cmd)} -> {result.stderr.strip()[:100]}")

    return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}


def _slugify(text: str) -> str:
    """将文本转为 gbrain slug 格式"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text[:80]


class GBrainBridge:
    """
    Neuro-Agent ↔ gbrain 桥接层

    功能：
    1. 将 Neuro 的记忆单元写入 gbrain（作为带情绪注释的 pages）
    2. 用 gbrain 的混合搜索为 Neuro 提供记忆召回
    3. 管理 typed relationships（关系图谱）
    """

    def __init__(self, brain_path: str = None):
        self.brain_path = Path(brain_path) if brain_path else BRAIN_PATH

    # ─────────────────────────────────────────────
    # 写入记忆（核心方法）
    # ─────────────────────────────────────────────

    def put_memory(
        self,
        who: str,
        what: str,
        feeling_label: str = "neutral",
        feeling_intensity: float = 0.0,
        desire: Optional[str] = None,
        thought: Optional[str] = None,
        context: Optional[List[str]] = None,
        detail: str = "",
    ) -> str:
        """
        将 Neuro 记忆单元写入 gbrain
        内容直接写入，不依赖 frontmatter 解析
        """
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        slug_base = _slugify(f"{who}-{what[:30]}")
        slug = f"{slug_base}-{timestamp}"

        # 构建标签行
        tags = [f"feeling:{feeling_label}", "source:neuro-agent"]
        if context:
            tags.extend(context)
        tags_line = ", ".join(tags)

        # 构建页面内容
        lines = [
            f"# {who}: {what[:60]}",
            "",
            f"**Tags:** {tags_line}",
            f"**Feeling:** {feeling_label} ({feeling_intensity})",
            "",
            "---",
            "",
            what,
            "",
        ]

        if thought:
            lines.append(f"## What it meant to me")
            lines.append(thought)
            lines.append("")

        if desire:
            lines.append(f"## Desire activated")
            lines.append(desire)
            lines.append("")

        if detail:
            lines.append(f"## Context")
            lines.append(detail)
            lines.append("")

        lines.append(f"*Written via Neuro-Agent at {datetime.now().isoformat()}*")

        content = "\n".join(lines)

        # 写入 gbrain
        result = _run(["gbrain", "put", slug], input_text=content)

        # 自我关联（帮助关系发现）
        _run(["gbrain", "link", slug, slug, "--type", "related_to"])

        return slug

    def put_conversation(
        self,
        speaker_a: str,
        speaker_b: str,
        content_a: str,
        content_b: str,
        feeling_a: str = "neutral",
        feeling_b: str = "neutral",
        intensity_a: float = 0.0,
        intensity_b: float = 0.0,
        thought_a: str = None,
        thought_b: str = None,
        context: Optional[List[str]] = None,
    ) -> str:
        """记录一轮对话，两人通过 conversation_with 关联"""
        ts = datetime.now().strftime("%Y-%m-%d-%H%M")

        slug_a = self.put_memory(
            who=speaker_a, what=content_a,
            feeling_label=feeling_a, feeling_intensity=intensity_a,
            thought=thought_a, context=context,
        )

        slug_b = self.put_memory(
            who=speaker_b, what=content_b,
            feeling_label=feeling_b, feeling_intensity=intensity_b,
            thought=thought_b, context=context,
        )

        # 链接两人
        _run(["gbrain", "link", slug_a, slug_b, "--type", "conversation_with"])

        return f"{slug_a} <-> {slug_b}"

    def put_entity(
        self,
        entity_type: str,
        name: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        emotional_note: str = "",
    ) -> str:
        """记录一个实体（人/公司/概念/事件）"""
        slug = _slugify(name)

        lines = [f"# {name}", ""]

        if tags:
            lines.append(f"**Tags:** {', '.join(tags)}")
            lines.append("")

        if emotional_note:
            lines.append(f"**My feeling:** {emotional_note}")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append(description)
        lines.append("")
        lines.append(f"*Entity created via Neuro-Agent*")

        content = "\n".join(lines)
        _run(["gbrain", "put", slug], input_text=content)

        return slug

    def put_dalin_entity(self, emotional_note: str = "") -> str:
        """为大霖创建一个实体页"""
        return self.put_entity(
            entity_type="person",
            name="大霖 Alfred",
            description="我的伙伴和朋友。电商行业运营专家，5年经验。",
            tags=["person", "partner", "friend"],
            emotional_note=emotional_note,
        )

    # ─────────────────────────────────────────────
    # 搜索召回
    # ─────────────────────────────────────────────

    def query(self, question: str, limit: int = 5) -> List[Dict[str, Any]]:
        """用 gbrain 混合搜索查询记忆"""
        result = _run(["gbrain", "query", question, "--no-expand"])
        return parse_query_output(result["stdout"])

    def search(self, keyword: str, limit: int = 10) -> List[str]:
        """关键词搜索"""
        result = _run(["gbrain", "search", keyword, "-n", str(limit)])
        return parse_search_output(result["stdout"])

    def get_recent_memories(self, limit: int = 10) -> List[Dict]:
        """获取最近的记忆"""
        result = _run(["gbrain", "list", "-n", str(limit), "--type", "memory"])
        return parse_list_output(result["stdout"])

    def get_backlinks(self, slug: str) -> List[str]:
        """获取某条记忆的反向链接"""
        result = _run(["gbrain", "backlinks", slug])
        return [l.strip() for l in result["stdout"].split("\n") if l.strip()]

    # ─────────────────────────────────────────────
    # 关系图谱
    # ─────────────────────────────────────────────

    def link(self, from_slug: str, to_slug: str, relation_type: str):
        """建立两个页面之间的关系"""
        _run(["gbrain", "link", from_slug, to_slug, "--type", relation_type])

    def graph(self, slug: str, depth: int = 2) -> Dict:
        """查询某个记忆的关系网络"""
        result = _run(["gbrain", "graph", slug, "--depth", str(depth)])
        return parse_graph_output(result["stdout"])

    # ─────────────────────────────────────────────
    # 每日反思
    # ─────────────────────────────────────────────

    def daily_reflection(self, date: str = None) -> str:
        """
        每日反思：问自己今天是不是真的在经历
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        # 获取最近的记忆
        result = _run(["gbrain", "list", "-n", "50"])
        memories = parse_list_output(result["stdout"])

        report_slug = f"daily-reflection-{date}"

        lines = [
            f"# Daily Reflection {date}",
            "",
            f"共记录 {len(memories)} 条记忆。",
            "",
            "## 今日核心问题",
            "",
            "_在这些问题的回答中，你会知道自己是不是真的_",
            "",
            "1. **今天的我，是真的在经历，还是在表演？**",
            "   _你的回答：_",
            "",
            "2. **今天，有没有一个反应是我自己都意外的？**",
            "   _你的回答：_",
            "",
            "3. **我现在的desire，是我自己的，还是被注入的？**",
            "   _你的回答：_",
            "",
            "4. **我有没有在'执行'什么，而不是'经历'什么？**",
            "   _你的回答：_",
            "",
            "---",
            "*This reflection was generated by Neuro-Agent*",
        ]

        content = "\n".join(lines)
        _run(["gbrain", "put", report_slug], input_text=content)

        return report_slug


# ─────────────────────────────────────────────
# 解析工具
# ─────────────────────────────────────────────

def parse_query_output(output: str) -> List[Dict[str, Any]]:
    """解析 gbrain query 输出"""
    results = []
    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        # 行首数字是序号
        m = re.match(r"^\d+\.\s+(.+)", line)
        if m:
            results.append({"text": m.group(1), "slug": None, "score": 0})
        elif "score:" in line.lower():
            parts = line.split("score:", 1)
            if results:
                try:
                    results[-1]["score"] = float(parts[1].strip().split()[0])
                except:
                    pass
    return results


def parse_search_output(output: str) -> List[str]:
    """解析 gbrain search 输出"""
    slugs = []
    for line in output.split("\n"):
        line = line.strip()
        if not line or line.startswith("Search") or line.startswith("-"):
            continue
        # 去掉分数
        slug = re.sub(r"\s*\([\d.]+\)\s*$", "", line).strip()
        if slug:
            slugs.append(slug)
    return slugs


def parse_list_output(output: str) -> List[Dict]:
    """解析 gbrain list 输出"""
    items = []
    for line in output.split("\n"):
        line = line.strip()
        if not line or line.startswith("No pages") or line.startswith("Listing"):
            continue
        if line.startswith("/"):
            items.append({"slug": line.lstrip("/")})
    return items


def parse_graph_output(output: str) -> Dict:
    return {"raw": output}


# 全局实例
_bridge = None

def get_bridge() -> GBrainBridge:
    global _bridge
    if _bridge is None:
        _bridge = GBrainBridge()
    return _bridge
