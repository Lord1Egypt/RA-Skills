"""
Karpathy Compile Pipeline - Phase 2
Wiki → Knowledge Points 编译
"""

import os
import sys
import json
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class KnowledgePoint:
    """知识精华条目"""
    title: str
    core_concept: str
    source: str
    detailed_explanation: str
    tags: List[str]
    created_at: str
    confidence: str = "medium"  # high/medium/low
    
    def to_markdown(self) -> str:
        """转换为 Markdown 格式"""
        lines = [
            f"## {self.title}",
            "",
            f"**核心概念**: {self.core_concept}",
            f"**来源**: {self.source}",
            f"**可信度**: {self.confidence}",
            "",
            "### 详细说明",
            self.detailed_explanation,
            "",
            f"**标签**: {', '.join(self.tags)}",
            f"**创建时间**: {self.created_at}",
        ]
        return "\n".join(lines)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class WikiParser:
    """解析 Phase 1 的 wiki 文件"""
    
    def __init__(self, wiki_path: str = None):
        if wiki_path is None:
            self.wiki_path = Path(__file__).parent.parent.parent / "knowledge" / "wiki"
        else:
            self.wiki_path = Path(wiki_path)
    
    def parse_wiki_file(self, filename: str = None) -> List[Dict[str, str]]:
        """
        解析 wiki Markdown 文件
        
        Returns:
            [{source, content, tags, timestamp}, ...]
        """
        if filename is None:
            # 使用最新的 wiki 文件
            files = list(self.wiki_path.glob("wiki-*.md"))
            if not files:
                return []
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            filename = files[0].name
        
        filepath = self.wiki_path / filename
        if not filepath.exists():
            return []
        
        entries = []
        lines = filepath.read_text(encoding="utf-8").split("\n")
        
        # 跳过表头 (前两行)
        data_lines = lines[2:]  # 跳过 | ... | 行和 |---|...| 行
        
        for line in data_lines:
            line = line.strip()
            if not line:
                continue
            
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                # parts: ['', source, content, tags, timestamp, '']
                entries.append({
                    "source": parts[1],
                    "content": parts[2],
                    "tags": parts[3].split(",") if parts[3] else [],
                    "timestamp": parts[4]
                })
        
        return entries
    
    def group_by_tags(self, entries: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
        """按标签分组"""
        groups = {}
        for entry in entries:
            for tag in entry["tags"]:
                tag = tag.strip()
                if tag and tag != "general":
                    if tag not in groups:
                        groups[tag] = []
                    groups[tag].append(entry)
        return groups


class LLMDistiller:
    """使用 LLM 进行知识蒸馏"""
    
    def __init__(self, llm_endpoint: str = "http://localhost:11434/v1"):
        self.endpoint = llm_endpoint
        self.api_key = "ollama"
    
    async def distill(self, wiki_entries: List[Dict[str, str]], topic: str) -> KnowledgePoint:
        """
        将多个 wiki 条目蒸馏为一个 knowledge point
        
        Args:
            wiki_entries: Wiki 条目列表
            topic: 主题
            
        Returns:
            KnowledgePoint
        """
        # 构建 prompt
        contents = "\n".join([f"- {e['content']}" for e in wiki_entries])
        prompt = f"""你是知识蒸馏专家。请将以下关于「{topic}」的信息蒸馏为一个知识精华。

原始信息:
{contents}

请生成一个知识精华，包含:
1. 核心概念（一句话概括）
2. 详细说明（2-3句深入解释）
3. 标签（最多3个）

以JSON格式返回:
{{
  "core_concept": "...",
  "detailed_explanation": "...",
  "tags": ["tag1", "tag2"],
  "confidence": "high/medium/low"
}}
"""
        
        # 调用 Ollama LLM
        try:
            import openai
            client = openai.OpenAI(
                base_url=self.endpoint,
                api_key=self.api_key
            )
            
            response = client.chat.completions.create(
                model="qwen2.5:14b-instruct-q8_0",
                messages=[
                    {"role": "system", "content": "你是一个知识蒸馏专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content
            
            # 解析 JSON
            # 尝试提取 JSON 部分
            json_start = result_text.find("{")
            json_end = result_text.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                result_json = json.loads(result_text[json_start:json_end])
            else:
                result_json = {
                    "core_concept": wiki_entries[0]["content"][:50] if wiki_entries else topic,
                    "detailed_explanation": result_text[:200],
                    "tags": [topic],
                    "confidence": "medium"
                }
            
            return KnowledgePoint(
                title=topic,
                core_concept=result_json.get("core_concept", ""),
                source=f"compiled from {len(wiki_entries)} wiki entries",
                detailed_explanation=result_json.get("detailed_explanation", ""),
                tags=result_json.get("tags", [topic]),
                created_at=datetime.now().strftime("%Y-%m-%d"),
                confidence=result_json.get("confidence", "medium")
            )
            
        except Exception as e:
            # 如果 LLM 调用失败，使用简单策略
            return KnowledgePoint(
                title=topic,
                core_concept=wiki_entries[0]["content"][:100] if wiki_entries else topic,
                source=f"fallback from {len(wiki_entries)} wiki entries",
                detailed_explanation="LLM distillation failed, using fallback",
                tags=[topic],
                created_at=datetime.now().strftime("%Y-%m-%d"),
                confidence="low"
            )


class CompilePipeline:
    """
    Karpathy Compile Pipeline
    
    流程:
    1. 解析 Phase 1 wiki 文件
    2. 按主题分组
    3. LLM distillation 生成 knowledge points
    4. 保存到 knowledge-points/ 目录
    """
    
    def __init__(
        self,
        wiki_path: str = None,
        output_path: str = None
    ):
        self.wiki_path = Path(wiki_path) if wiki_path else Path(__file__).parent.parent.parent / "knowledge" / "wiki"
        self.output_path = Path(output_path) if output_path else Path(__file__).parent.parent.parent / "knowledge" / "knowledge-points"
        
        self.wiki_parser = WikiParser(str(self.wiki_path))
        self.llm_distiller = LLMDistiller()
        
        # 确保输出目录存在
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    async def compile(
        self,
        max_entries_per_point: int = 5,
        min_entries_for_distillation: int = 2
    ) -> List[KnowledgePoint]:
        """
        执行编译
        
        Args:
            max_entries_per_point: 每个 knowledge point 最多包含的 wiki 条目数
            min_entries_for_distillation: 最少需要多少条目才进行 LLM distillation
            
        Returns:
            生成的 KnowledgePoint 列表
        """
        # 1. 解析 wiki 文件
        entries = self.wiki_parser.parse_wiki_file()
        if not entries:
            print("[WARN] No wiki entries found")
            return []
        
        print(f"[INFO] Found {len(entries)} wiki entries")
        
        # 2. 按标签分组
        groups = self.wiki_parser.group_by_tags(entries)
        print(f"[INFO] Grouped into {len(groups)} topics")
        
        # 3. 对每个主题进行 distillation
        knowledge_points = []
        for topic, topic_entries in groups.items():
            if len(topic_entries) < min_entries_for_distillation:
                # 条目太少，直接使用第一个作为 fallback
                kp = KnowledgePoint(
                    title=topic,
                    core_concept=topic_entries[0]["content"][:100],
                    source=f"direct from {len(topic_entries)} entries",
                    detailed_explanation="",
                    tags=[topic],
                    created_at=datetime.now().strftime("%Y-%m-%d"),
                    confidence="low"
                )
            else:
                # LLM distillation
                print(f"[INFO] Distilling topic: {topic} ({len(topic_entries)} entries)")
                kp = await self.llm_distiller.distill(
                    topic_entries[:max_entries_per_point],
                    topic
                )
            
            knowledge_points.append(kp)
        
        # 4. 保存到文件
        await self.save_knowledge_points(knowledge_points)
        
        return knowledge_points
    
    async def save_knowledge_points(
        self,
        knowledge_points: List[KnowledgePoint],
        filename: str = None
    ) -> str:
        """保存 knowledge points 到文件"""
        if filename is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"knowledge-points-{date_str}.md"
        
        filepath = self.output_path / filename
        
        lines = [
            f"# Knowledge Points - {datetime.now().strftime('%Y-%m-%d')}",
            "",
            f"Generated {len(knowledge_points)} knowledge points",
            "",
            "---",
            ""
        ]
        
        for kp in knowledge_points:
            lines.append(kp.to_markdown())
            lines.append("")
            lines.append("---")
            lines.append("")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        print(f"[INFO] Saved {len(knowledge_points)} knowledge points to {filepath}")
        return str(filepath)


async def main():
    """测试 Compile Pipeline"""
    print("=== Phase 2: Compile Pipeline Test ===")
    
    pipeline = CompilePipeline()
    
    # 如果没有 wiki 条目，先生成一些测试数据
    entries = pipeline.wiki_parser.parse_wiki_file()
    if not entries:
        print("[INFO] No wiki entries, creating test data...")
        # 模拟 Phase 1 的 wiki 数据
        test_wiki_path = pipeline.wiki_path
        test_wiki_path.mkdir(parents=True, exist_ok=True)
        test_file = test_wiki_path / "wiki-2026-04-05.md"
        test_file.write_text("""\
| source | content | tags | timestamp |
|--------|---------|------|-----------|
| query:lexical | Python is a programming language | python | 2026-04-05 |
| query:lexical | Python has extensive libraries for data science | python | 2026-04-05 |
| query:lexical | Python is used for machine learning | python | 2026-04-05 |
| query:lexical | JavaScript is for web development | javascript | 2026-04-05 |
| query:lexical | JavaScript runs in browsers | javascript | 2026-04-05 |
| query:lexical | AI is artificial intelligence | ai | 2026-04-05 |
| query:lexical | AI uses machine learning algorithms | ai | 2026-04-05 |
""", encoding="utf-8")
    
    # 执行编译
    kps = await pipeline.compile()
    
    print(f"\n[RESULT] Generated {len(kps)} knowledge points:")
    for kp in kps:
        print(f"  - {kp.title}: {kp.core_concept[:50]}...")
    
    print("\n=== Phase 2 Test Complete ===")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
