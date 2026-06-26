#!/usr/bin/env python3
"""
Learning Notes Explorer
Explore, search, and synthesize personal learning notes.
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path


@dataclass
class Note:
    """Learning note structure"""
    id: str
    title: str
    content: str
    source: str = ""
    source_type: str = "general"  # book, article, course, video, podcast
    tags: List[str] = field(default_factory=list)
    created_at: str = ""
    modified_at: str = ""
    related_notes: List[str] = field(default_factory=list)


@dataclass
class SearchResult:
    """Search result structure"""
    note: Note
    relevance_score: float
    matched_sections: List[str]


class NotesIndex:
    """In-memory index for notes"""
    
    def __init__(self):
        self.notes: Dict[str, Note] = {}
        self.tag_index: Dict[str, List[str]] = {}
        self.word_index: Dict[str, List[str]] = {}
    
    def add_note(self, note: Note):
        """Add a note to the index"""
        self.notes[note.id] = note
        
        # Index tags
        for tag in note.tags:
            tag_lower = tag.lower()
            if tag_lower not in self.tag_index:
                self.tag_index[tag_lower] = []
            self.tag_index[tag_lower].append(note.id)
        
        # Index words
        words = self._extract_words(note.title + " " + note.content)
        for word in words:
            if word not in self.word_index:
                self.word_index[word] = []
            if note.id not in self.word_index[word]:
                self.word_index[word].append(note.id)
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract searchable words from text"""
        # Support both English and Chinese
        words = []
        # English words
        words.extend(re.findall(r'[a-zA-Z]+', text.lower()))
        # Chinese characters (as individual searchable tokens)
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        words.extend(chinese_chars)
        return words
    
    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Search notes by query"""
        query_lower = query.lower()
        query_words = self._extract_words(query)
        
        scores: Dict[str, float] = {}
        matched_sections: Dict[str, List[str]] = {}
        
        # Check for exact matches in title
        for note_id, note in self.notes.items():
            if query_lower in note.title.lower():
                scores[note_id] = scores.get(note_id, 0) + 10
                if note_id not in matched_sections:
                    matched_sections[note_id] = []
                matched_sections[note_id].append(f"Title: {note.title}")
        
        # Check for word matches
        for word in query_words:
            if word in self.word_index:
                for note_id in self.word_index[word]:
                    scores[note_id] = scores.get(note_id, 0) + 1
        
        # Check for tag matches
        if query_lower in self.tag_index:
            for note_id in self.tag_index[query_lower]:
                scores[note_id] = scores.get(note_id, 0) + 5
        
        # Check content for phrase matches
        for note_id, note in self.notes.items():
            if query_lower in note.content.lower():
                scores[note_id] = scores.get(note_id, 0) + 3
                # Find context
                idx = note.content.lower().find(query_lower)
                if idx >= 0:
                    start = max(0, idx - 50)
                    end = min(len(note.content), idx + len(query) + 50)
                    context = note.content[start:end]
                    if note_id not in matched_sections:
                        matched_sections[note_id] = []
                    matched_sections[note_id].append(f"...{context}...")
        
        # Sort by score and create results
        sorted_notes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for note_id, score in sorted_notes[:limit]:
            results.append(SearchResult(
                note=self.notes[note_id],
                relevance_score=score,
                matched_sections=matched_sections.get(note_id, [])
            ))
        
        return results
    
    def get_by_tag(self, tag: str) -> List[Note]:
        """Get all notes with a specific tag"""
        tag_lower = tag.lower()
        note_ids = self.tag_index.get(tag_lower, [])
        return [self.notes[nid] for nid in note_ids if nid in self.notes]
    
    def get_by_source_type(self, source_type: str) -> List[Note]:
        """Get notes by source type"""
        return [n for n in self.notes.values() if n.source_type == source_type]
    
    def get_recent(self, days: int = 30) -> List[Note]:
        """Get recently created/modified notes"""
        # Simplified - return all notes sorted by created_at
        notes_list = list(self.notes.values())
        notes_list.sort(key=lambda x: x.created_at or "", reverse=True)
        return notes_list
    
    def find_connections(self, note_id: str) -> List[Dict[str, Any]]:
        """Find connections between notes"""
        if note_id not in self.notes:
            return []
        
        note = self.notes[note_id]
        connections = []
        
        # Direct connections
        for related_id in note.related_notes:
            if related_id in self.notes:
                connections.append({
                    "type": "direct",
                    "note": self.notes[related_id],
                    "reason": "Explicitly linked"
                })
        
        # Tag-based connections
        for tag in note.tags:
            for other_id in self.tag_index.get(tag.lower(), []):
                if other_id != note_id and other_id not in note.related_notes:
                    connections.append({
                        "type": "tag",
                        "note": self.notes[other_id],
                        "reason": f"Shared tag: {tag}"
                    })
        
        # Content similarity (simple word overlap)
        note_words = set(self._extract_words(note.content))
        for other_id, other in self.notes.items():
            if other_id != note_id:
                other_words = set(self._extract_words(other.content))
                overlap = note_words & other_words
                if len(overlap) >= 5:  # At least 5 common words
                    connections.append({
                        "type": "similarity",
                        "note": other,
                        "reason": f"{len(overlap)} common concepts"
                    })
        
        return connections


class NotesExplorer:
    """Main explorer class"""
    
    def __init__(self, notes_dir: Optional[str] = None):
        self.index = NotesIndex()
        self.notes_dir = notes_dir or os.path.expanduser("~/.openclaw/notes")
        self._load_notes()
    
    def _load_notes(self):
        """Load notes from storage"""
        # Load from JSON file if exists
        notes_file = os.path.join(self.notes_dir, "notes.json")
        if os.path.exists(notes_file):
            try:
                with open(notes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data.get('notes', []):
                        note = Note(**item)
                        self.index.add_note(note)
            except Exception:
                pass
        
        # If no notes loaded, add some demo notes
        if not self.index.notes:
            self._add_demo_notes()
    
    def _add_demo_notes(self):
        """Add demo notes for testing"""
        demo_notes = [
            Note(
                id="note_001",
                title="Atomic Habits - Key Concepts",
                content="""微习惯：小到不可能失败的行动。每天进步1%，一年后进步37倍。
身份认同是改变的核心。不要想着'我要戒烟'，要想'我不是烟民'。
习惯的四步法：提示、渴望、反应、奖励。
两分钟规则：任何习惯都可以在2分钟内开始。""",
                source="《原子习惯》by James Clear",
                source_type="book",
                tags=["habits", "self-improvement", "productivity", "习惯"],
                created_at="2024-01-15"
            ),
            Note(
                id="note_002",
                title="Deep Work - Focus Strategy",
                content="""深度工作：在无干扰状态下专注进行职业活动的能力。
四种深度工作哲学：
1. 禁欲主义哲学 - 长期隔离
2. 双峰哲学 - 分阶段深度/浅度
3. 节奏哲学 - 固定时间深度工作
4. 记者哲学 - 随时进入深度状态
度量指标：深度工作时间 / 总工作时间""",
                source="《深度工作》by Cal Newport",
                source_type="book",
                tags=["focus", "productivity", "work", "专注"],
                created_at="2024-01-20",
                related_notes=["note_001"]
            ),
            Note(
                id="note_003",
                title="刻意练习 Principles",
                content="""刻意练习的四个要素：
1. 明确目标：设定具体可衡量的子目标
2. 专注投入：全神贯注于任务
3. 即时反馈：立即知道对错
4. 走出舒适区：不断挑战更高难度
与天真的练习不同，刻意练习是有目的、有指导的练习。""",
                source="《刻意练习》by Anders Ericsson",
                source_type="book",
                tags=["learning", "practice", "skill", "学习"],
                created_at="2024-02-01"
            ),
            Note(
                id="note_004",
                title="Learning How to Learn - Coursera",
                content="""组块化：将信息打包成大脑易于处理的单元。
专注模式 vs 发散模式：
- 专注模式用于学习具体概念
- 发散模式用于创造性思考
番茄工作法：25分钟专注 + 5分钟休息
间隔重复：在遗忘曲线最佳点复习""",
                source="Learning How to Learn Course",
                source_type="course",
                tags=["learning", "memory", "study", "学习"],
                created_at="2024-02-10"
            ),
        ]
        for note in demo_notes:
            self.index.add_note(note)
    
    def search(self, query: str, limit: int = 10) -> str:
        """Search notes and return formatted results"""
        results = self.index.search(query, limit)
        
        if not results:
            return f"No notes found for '{query}'. Try different keywords or check your spelling."
        
        lines = [f"## Search Results: '{query}'", ""]
        lines.append(f"Found {len(results)} note(s):\n")
        
        for i, result in enumerate(results, 1):
            note = result.note
            lines.append(f"{i}. **{note.title}**")
            lines.append(f"   Source: {note.source}")
            lines.append(f"   Type: {note.source_type}")
            lines.append(f"   Tags: {', '.join(note.tags)}")
            
            # Show preview
            preview = note.content[:150].replace('\n', ' ')
            if len(note.content) > 150:
                preview += "..."
            lines.append(f"   Preview: {preview}")
            
            if result.matched_sections:
                lines.append(f"   Match: {result.matched_sections[0][:100]}...")
            
            lines.append("")
        
        return '\n'.join(lines)
    
    def synthesize_topic(self, topic: str) -> str:
        """Synthesize knowledge on a topic"""
        results = self.index.search(topic, limit=5)
        
        if not results:
            return f"No notes found for topic '{topic}'."
        
        lines = [f"## Knowledge Synthesis: {topic}", ""]
        
        # Key concepts
        lines.append("### Key Concepts Learned")
        for result in results:
            note = result.note
            lines.append(f"- **{note.title}** (from {note.source})")
            # Extract first sentence or line as summary
            summary = note.content.split('\n')[0][:100]
            lines.append(f"  - {summary}")
        lines.append("")
        
        # Sources
        lines.append("### Sources")
        sources = set(r.note.source for r in results)
        for source in sources:
            related = [r for r in results if r.note.source == source]
            if related:
                insight = related[0].note.content[:80].replace('\n', ' ')
                lines.append(f"- **{source}** - {insight}...")
        lines.append("")
        
        # Connections
        lines.append("### Connections Between Notes")
        all_tags = set()
        for r in results:
            all_tags.update(r.note.tags)
        if all_tags:
            lines.append(f"Common themes: {', '.join(list(all_tags)[:5])}")
        lines.append("")
        
        # Suggested next steps
        lines.append("### Suggested Next Steps")
        lines.append(f"- [ ] Explore related topic: advanced {topic}")
        lines.append(f"- [ ] Review and connect with other notes")
        lines.append(f"- [ ] Create practical application from these insights")
        
        return '\n'.join(lines)
    
    def review_recent(self, days: int = 30) -> str:
        """Review recent notes"""
        notes = self.index.get_recent(days)
        
        lines = [f"## Recent Learning Activity (Last {days} days)", ""]
        
        if not notes:
            lines.append("No notes found in this time period.")
            return '\n'.join(lines)
        
        # Group by source type
        by_type: Dict[str, List[Note]] = {}
        for note in notes:
            st = note.source_type
            if st not in by_type:
                by_type[st] = []
            by_type[st].append(note)
        
        lines.append(f"Total notes: {len(notes)}\n")
        
        for source_type, type_notes in by_type.items():
            lines.append(f"### {source_type.title()} ({len(type_notes)})")
            for note in type_notes[:5]:
                lines.append(f"- {note.title}")
                preview = note.content[:80].replace('\n', ' ')
                lines.append(f"  {preview}...")
            lines.append("")
        
        # Topics covered
        all_tags = set()
        for note in notes:
            all_tags.update(note.tags)
        if all_tags:
            lines.append("### Topics Covered")
            lines.append(f"Tags: {', '.join(sorted(all_tags))}")
        
        return '\n'.join(lines)
    
    def explore_connections(self, note_title: str) -> str:
        """Explore connections for a specific note"""
        # Find note by title
        target_note = None
        for note in self.index.notes.values():
            if note_title.lower() in note.title.lower():
                target_note = note
                break
        
        if not target_note:
            return f"Note '{note_title}' not found."
        
        connections = self.index.find_connections(target_note.id)
        
        lines = [f"## Connections: {target_note.title}", ""]
        lines.append(f"**Source:** {target_note.source}")
        lines.append(f"**Tags:** {', '.join(target_note.tags)}\n")
        
        if not connections:
            lines.append("No connections found for this note.")
            return '\n'.join(lines)
        
        # Group by type
        by_type: Dict[str, List[Dict]] = {}
        for conn in connections:
            t = conn['type']
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(conn)
        
        for conn_type, conns in by_type.items():
            lines.append(f"### {conn_type.title()} Connections ({len(conns)})")
            for conn in conns[:5]:
                note = conn['note']
                lines.append(f"- **{note.title}**")
                lines.append(f"  Reason: {conn['reason']}")
                preview = note.content[:60].replace('\n', ' ')
                lines.append(f"  Preview: {preview}...")
            lines.append("")
        
        return '\n'.join(lines)
    
    def learning_path(self, topic: str) -> str:
        """Generate a learning path for a topic"""
        related_notes = self.index.search(topic, limit=10)
        
        lines = [f"## Learning Path: {topic}", ""]
        
        # What we already know
        lines.append("### Prerequisites (Already Learned)")
        if related_notes:
            for result in related_notes[:5]:
                lines.append(f"✓ {result.note.title}")
        else:
            lines.append("No existing notes found. Starting from scratch.")
        lines.append("")
        
        # Recommended sequence
        lines.append("### Recommended Learning Sequence")
        steps = [
            f"1. Foundational concepts in {topic}",
            f"2. Core principles and frameworks",
            f"3. Practical applications and case studies",
            f"4. Advanced topics and edge cases",
            f"5. Integration with existing knowledge"
        ]
        for step in steps:
            lines.append(step)
        lines.append("")
        
        # Suggested resources
        lines.append("### Suggested Resources")
        # Based on existing notes, suggest similar
        sources = set()
        for r in related_notes:
            sources.add(r.note.source_type)
        
        if 'book' in sources:
            lines.append("- Recommended book on this topic")
        if 'course' in sources:
            lines.append("- Online course for structured learning")
        lines.append("- Practice exercises to apply concepts")
        lines.append("- Community discussions for deeper insights")
        
        return '\n'.join(lines)


def main():
    """Main entry point"""
    explorer = NotesExplorer()
    
    if len(sys.argv) < 2:
        # Interactive mode or show help
        print("Usage: handler.py <command> [args]")
        print("")
        print("Commands:")
        print("  search <query>        - Search notes by keyword")
        print("  topic <topic>         - Synthesize knowledge on a topic")
        print("  recent [days]         - Review recent notes (default 30 days)")
        print("  connections <title>   - Explore connections for a note")
        print("  path <topic>          - Generate learning path")
        print("")
        print("Examples:")
        print('  handler.py search "habits"')
        print('  handler.py topic "刻意练习"')
        print('  handler.py recent 7')
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == "search":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not query:
            print("Error: Search query required")
            sys.exit(1)
        result = explorer.search(query)
        print(result)
    
    elif command == "topic":
        topic = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not topic:
            print("Error: Topic required")
            sys.exit(1)
        result = explorer.synthesize_topic(topic)
        print(result)
    
    elif command == "recent":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        result = explorer.review_recent(days)
        print(result)
    
    elif command == "connections":
        title = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not title:
            print("Error: Note title required")
            sys.exit(1)
        result = explorer.explore_connections(title)
        print(result)
    
    elif command == "path":
        topic = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not topic:
            print("Error: Topic required")
            sys.exit(1)
        result = explorer.learning_path(topic)
        print(result)
    
    else:
        # Default to search
        query = " ".join(sys.argv[1:])
        result = explorer.search(query)
        print(result)


if __name__ == "__main__":
    main()
