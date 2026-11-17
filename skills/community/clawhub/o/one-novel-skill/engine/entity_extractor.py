#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
entity_extractor.py — 章节实体提取 + 伏笔关系图

融合源: entities-master (实体提取) + code-review-graph (可视化审查)
功能: 
  1. 从正文提取角色/地点/事件实体
  2. 自动生成角色关系有向图
  3. 伏笔→回收关系图
"""

import re
from pathlib import Path
from typing import List, Dict, Set, Tuple


class EntityExtractor:
    """从章节文本提取实体"""

    @staticmethod
    def extract_characters(text: str, known_names: Set[str] = None) -> List[str]:
        """提取文本中出现的角色名
        
        策略: 对话标签前的人名 + 已知角色名匹配
        """
        chars = set(known_names or [])
        
        # 从对话标签提取: "XXX道/说/问/喊"
        for m in re.finditer(r'([\u4e00-\u9fff\u3400-\u4dbf]{1,6})(?:道|说|问|喊|叫|骂|答|笑道|喊道|问道|说道|哭道|叹道)', text):
            name = m.group(1)
            if name and len(name) >= 2 and name not in {"不知道", "可以说", "比如说", "可以说"}:
                chars.add(name)
        
        # 从"XX的"结构提取潜在名字
        for m in re.finditer(r'([\u4e00-\u9fff]{2,4})(?:的)(?:脸|手|眼|嘴|笑容|身|背影|声音)', text):
            name = m.group(1)
            if name and len(name) <= 4:
                chars.add(name)
        
        return sorted(chars)

    @staticmethod
    def extract_locations(text: str) -> List[str]:
        """提取地点实体"""
        locs = set()
        # "在XX" + 长度2-4的中文
        for m in re.finditer(r'(?:在|到|去|来|从|回到|前往)([\u4e00-\u9fff\u3400-\u4dbf]{2,6})(?:[，。！？\s]|$)', text):
            loc = m.group(1)
            if loc and loc not in {"这个时候", "这个时", "什么", "怎么样", "怎么办", "哪里"}:
                locs.add(loc)
        return sorted(locs)

    @staticmethod
    def extract_events(text: str) -> List[str]:
        """提取事件（发现/冲突/转折）"""
        events = []
        signals = [
            (r'[^。！？]{5,50}(?:发现|看到|听见|闻到|意识到)[^。！？]{5,50}[。！？]', "发现"),
            (r'[^。！？]{5,50}(?:突然|猛然|猝不及防)[^。！？]{5,50}[。！？]', "突发"),
            (r'[^。！？]{5,50}(?:但|然而|可是|却|没想到)[^。！？]{5,50}[。！？]', "转折"),
            (r'[^。！？]{5,50}(?:打|杀|战|斗|撞|碎|破)[^。！？]{10,60}[。！？]', "冲突"),
        ]
        for pat, evtype in signals:
            for m in re.finditer(pat, text):
                event = m.group(0).strip()
                if len(event) >= 10:
                    events.append((event, evtype))
        return events[:10]  # 最多10条

    @staticmethod
    def extract_relations(text: str, chars: List[str]) -> List[Tuple[str, str, str]]:
        """提取角色间关系
        
        Returns: [(角色A, 角色B, 关系类型), ...]
        """
        relations = []
        # 检测"XX和XX"、"XX与XX"共同出现的句子
        for i, a in enumerate(chars):
            for b in chars[i+1:]:
                # 检查是否在同一句中出现
                pattern = re.compile(f'{re.escape(a)}.{0,30}{re.escape(b)}')
                if pattern.search(text):
                    # 判断关系类型
                    if any(w in text[text.index(a):text.index(a)+50] for w in ["宿敌", "仇", "恨", "杀", "死"]):
                        relations.append((a, b, "对立"))
                    elif any(w in text[text.index(a):text.index(a)+50] for w in ["救", "帮", "友", "盟", "师"]):
                        relations.append((a, b, "盟友"))
                    else:
                        relations.append((a, b, "关联"))
        return relations


class DiagramEnhancer:
    """图解增强器 — 扩展 diagram_generator 的功能"""
    
    @staticmethod
    def foreshadow_graph(foreshadows: List[Dict]) -> str:
        """从伏笔数据生成有向图
        
        Args:
            foreshadows: [{"id":"FS-001","desc":"...","plant_chapter":1,"reveal_chapter":10,"status":"planted"}, ...]
        Returns:
            Mermaid 格式字符串
        """
        lines = ["```mermaid", "graph LR"]
        
        # 按状态分颜色
        status_colors = {
            "planted": "#f9f",    # 粉色-已埋
            "triggered": "#ffa",  # 黄色-已触发
            "revealed": "#afa",   # 绿色-已回收
            "closed": "#aaf",     # 蓝色-已闭环
            "abandoned": "#ddd",  # 灰色-已废弃
        }
        
        for i, fs in enumerate(foreshadows[:20]):  # 最多20条
            nid = f"F{i}"
            label = f"{fs.get('id','?')}: {fs.get('desc','')[:30]}"
            status = fs.get("status", "planted")
            color = status_colors.get(status, "#fff")
            
            lines.append(f"    {nid}[\"{label}\"]")
            lines.append(f"    style {nid} fill:{color},stroke:#333,stroke-width:1px")
        
        # 连接伏笔链（plant_chapter → reveal_chapter 的顺序关系）
        sorted_fs = sorted(foreshadows, key=lambda f: f.get("plant_chapter", 0))
        for i in range(min(len(sorted_fs) - 1, 15)):
            a_id = f"F{i}"
            b_id = f"F{i+1}"
            a_p = sorted_fs[i].get("plant_chapter", 0)
            b_p = sorted_fs[i+1].get("plant_chapter", 0)
            if a_p < b_p:
                lines.append(f"    {a_id} -.->|ch{a_p}→ch{b_p}| {b_id}")
        
        lines.append("```")
        return "\n".join(lines)
    
    @staticmethod
    def chapter_entity_graph(chapter_text: str, known_chars: Set[str] = None) -> str:
        """从单章文本生成实体关系图"""
        chars = EntityExtractor.extract_characters(chapter_text, known_chars)
        if not chars:
            return "```mermaid\ngraph TD\n    N0[无角色]\n```"
        
        from .diagram_generator import DiagramGenerator
        relations = EntityExtractor.extract_relations(chapter_text, chars)
        char_list = [{"name": c} for c in chars]
        
        if relations:
            rel_dicts = [{"from": r[0], "to": r[1], "label": r[2]} for r in relations]
        else:
            rel_dicts = None
        
        return DiagramGenerator.character_relations(char_list, rel_dicts)
