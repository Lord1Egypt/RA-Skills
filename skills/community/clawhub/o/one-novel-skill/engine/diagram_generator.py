#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diagram_generator.py — 关键情节图解生成

融合源: novel-generator-1.0.0 的 Mermaid 图解能力
功能: 自动生成人物关系图/势力分布图/等级体系图/剧情时间线图
输出: Mermaid 语法格式，可嵌入 markdown 文档
"""

import re
from typing import List, Dict, Optional
from pathlib import Path


class DiagramGenerator:
    """图解生成器"""

    @staticmethod
    def character_relations(chars: List[Dict], relations: Optional[List[Dict]] = None) -> str:
        """生成人物关系图 (Mermaid graph TD)
        
        Args:
            chars: [{"name": "主角", "title": "身份/标签"}, ...]
            relations: [{"from": "主角", "to": "反派", "label": "宿敌"}, ...]
        Returns:
            Mermaid 格式字符串
        """
        lines = ["```mermaid", "graph TD"]
        
        # 节点定义
        node_ids = {}
        for i, c in enumerate(chars):
            nid = f"N{i}"
            name = c.get("name", f"角色{i}")
            title = c.get("title", "")
            label = f"{name}" + (f"\\n{title}" if title else "")
            lines.append(f"    {nid}[{label}]")
            node_ids[name] = nid
        
        # 关系边
        if relations:
            for r in relations:
                f = r.get("from", "")
                t = r.get("to", "")
                lbl = r.get("label", "")
                f_id = node_ids.get(f, "")
                t_id = node_ids.get(t, "")
                if f_id and t_id:
                    if lbl:
                        lines.append(f"    {f_id} -->|{lbl}| {t_id}")
                    else:
                        lines.append(f"    {f_id} --- {t_id}")
        
        # 如果没有显式关系，自动连接相邻角色
        if not relations:
            for i in range(min(len(chars) - 1, 10)):
                f_id = node_ids.get(chars[i].get("name", ""))
                t_id = node_ids.get(chars[i+1].get("name", ""))
                if f_id and t_id:
                    lines.append(f"    {f_id} --- {t_id}")
        
        lines.append("```")
        return "\n".join(lines)

    @staticmethod
    def power_levels(levels: List[Dict]) -> str:
        """生成等级体系图 (Mermaid graph BT)
        
        Args:
            levels: [{"name": "炼气期", "color": "#f9f"}, ...]
                    从低到高排列
        Returns:
            Mermaid 格式字符串
        """
        lines = ["```mermaid", "graph BT"]
        node_ids = []
        
        for i, lv in enumerate(levels):
            nid = f"L{i}"
            name = lv.get("name", f"等级{i}")
            color = lv.get("color", "")
            if color:
                lines.append(f"    {nid}[{name}]")
                lines.append(f"    style {nid} fill:{color},stroke:#333")
            else:
                lines.append(f"    {nid}[{name}]")
            node_ids.append(nid)
        
        for i in range(len(node_ids) - 1):
            lines.append(f"    {node_ids[i]} --> {node_ids[i+1]}")
        
        lines.append("```")
        return "\n".join(lines)

    @staticmethod
    def force_relations(factions: List[Dict], conflicts: Optional[List[Dict]] = None) -> str:
        """生成势力关系图 (Mermaid graph LR)
        
        Args:
            factions: [{"name": "赵家", "color": ""}, ...]
            conflicts: [{"from": "赵家", "to": "林家", "type": "对立"}, ...]
        """
        lines = ["```mermaid", "graph LR"]
        node_ids = {}
        
        for i, f in enumerate(factions):
            nid = f"F{i}"
            name = f.get("name", f"势力{i}")
            color = f.get("color", "")
            if color:
                lines.append(f"    {nid}[{name}]")
                lines.append(f"    style {nid} fill:{color},stroke:#333,color:#fff")
            else:
                lines.append(f"    {nid}[{name}]")
            node_ids[name] = nid
        
        edge_styles = {"对立": "-.->|对立|", "同盟": "==>|同盟|", "从属": "-->|从属|", "中立": "---|中立|"}
        if conflicts:
            for c in conflicts:
                f = c.get("from", "")
                t = c.get("to", "")
                tpe = c.get("type", "中立")
                f_id = node_ids.get(f, "")
                t_id = node_ids.get(t, "")
                if f_id and t_id:
                    arrow = edge_styles.get(tpe, "---")
                    lines.append(f"    {f_id} {arrow} {t_id}")
        
        lines.append("```")
        return "\n".join(lines)

    @staticmethod
    def timeline_plot(events: List[Dict]) -> str:
        """生成剧情时间线图 (Mermaid timeline)
        
        Args:
            events: [{"time": "第1章", "event": "主角获得系统", "section": "开局"}, ...]
        """
        lines = ["```mermaid", "timeline"]
        
        # 按 section 分组
        sections = {}
        for ev in events:
            sec = ev.get("section", "主线")
            if sec not in sections:
                sections[sec] = []
            sections[sec].append(ev)
        
        for section, evs in sections.items():
            lines.append(f"    {section} : {evs[0].get('time', '')} : {evs[0].get('event', '')}")
            for ev in evs[1:]:
                lines.append(f"        : {ev.get('time', '')} : {ev.get('event', '')}")
        
        lines.append("```")
        return "\n".join(lines)

    @staticmethod
    def auto_from_chapter_specs(specs: List[Dict]) -> Dict[str, str]:
        """从章节spec自动生成各类图解
        
        Returns:
            {"人物关系图": "...mermaid...", "势力分布图": "...", "等级体系图": "..."}
        """
        result = {}
        
        # 从spec提取角色
        chars = set()
        relations = []
        for spec in specs:
            bs = spec.get("before_state", {})
            if isinstance(bs, dict):
                for c in bs.get("characters", []):
                    if isinstance(c, dict):
                        chars.add(c.get("name", ""))
                    elif isinstance(c, str):
                        chars.add(c)
        
        if chars:
            char_list = [{"name": c} for c in sorted(chars) if c]
            result["人物关系图"] = DiagramGenerator.character_relations(char_list)
        
        return result

    def generate_for_book(self, book_dir: Path) -> Dict[str, str]:
        """为小说项目生成所有图解"""
        # 从规格加载
        spec_dir = book_dir / "规格"
        specs = []
        if spec_dir.exists():
            import json
            for f in sorted(spec_dir.glob("*.json")):
                try:
                    specs.append(json.loads(f.read_text(encoding="utf-8")))
                except (json.JSONDecodeError, OSError):
                    pass
        
        result = self.auto_from_chapter_specs(specs)
        
        # 从设定加载势力/等级
        setting_dir = book_dir / "设定"
        if setting_dir.exists():
            # 尝试从世界观.md或势力.md提取
            for fname in ["势力.md", "世界观.md"]:
                f = setting_dir / fname
                if f.exists():
                    text = f.read_text(encoding="utf-8", errors="replace")
                    factions = self._extract_factions(text)
                    if factions:
                        result["势力分布图"] = DiagramGenerator.force_relations(factions)
        
        return result

    def _extract_factions(self, text: str) -> List[Dict]:
        """从设定文本提取势力信息"""
        factions = []
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):
                name = line[2:].split(":")[0].split("：")[0].strip()
                if name and len(name) <= 10:
                    factions.append({"name": name})
        return factions

    def save_to_book(self, book_dir: Path, diagrams: Dict[str, str]) -> bool:
        """保存图解到项目目录"""
        diag_dir = book_dir / "大纲" / "图解"
        diag_dir.mkdir(parents=True, exist_ok=True)
        try:
            for title, mermaid in diagrams.items():
                safe_name = title.replace("/", "-").replace("\\", "-")
                (diag_dir / f"{safe_name}.md").write_text(mermaid, encoding="utf-8")
            # 生成索引
            index_lines = ["# 图解索引\n"]
            for title in diagrams:
                index_lines.append(f"- [{title}]({title}.md)")
            (diag_dir / "README.md").write_text("\n".join(index_lines), encoding="utf-8")
            return True
        except OSError:
            return False
