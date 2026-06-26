#!/usr/bin/env python3
"""
WorkingMemoryEngine — Context Window Layered Compression

Three-level compression for working memory:
1. Level 1 (完整): Current session full content — no compression
2. Level 2 (摘要): LLM-generated summary with key points
3. Level 3 (关键事实): Only high-strength KG entities (strength >= threshold)

Usage:
    python3 working_memory.py run --session-id xxx --level 2
    python3 working_memory.py recover --session-id xxx --level 3
    python3 working_memory.py stats
"""

import argparse
import fcntl
import json
import sys
import uuid
import warnings
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

# Path configuration
WORKSPACE_ROOT = Path.home() / ".openclaw" / "workspace" / "memory"
WORKING_MEMORY_FILE = WORKSPACE_ROOT / "working_memory.jsonl"

# Import from memory_ontology — reuse existing infrastructure
from memory_ontology import load_all_entities, GRAPH_FILE


# Import shared LLM client
from utils.llm_client import LLMClient


# ========== Compression Prompts ==========

SUMMARY_PROMPT = """请将以下会话内容压缩为简洁摘要。

会话内容：
{content}

输出格式（必须是有效 JSON，不要有其他内容）：
{{
  "summary": "压缩后的摘要，应该包含：主要话题/目标、关键决策（如果有）、重要发现（如果有）、下一步行动（如果有）。保持简洁，删除重复信息和冗余描述。summary 应在 100-300 字之间。"
}}
"""


# ========== Data Classes ==========

@dataclass
class WorkingMemoryEntry:
    """Single working memory entry."""
    id: str
    session_id: str
    timestamp: str
    compression_level: int
    content: Dict
    source_entities: List[str]
    strength_threshold: float
    original_tokens: int
    compressed_tokens: int
    error: Optional[str] = None

    def to_entry_dict(self) -> Dict:
        """Convert to entry dict for JSON serialization."""
        result = {
            "id": self.id,
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "compression_level": self.compression_level,
            "content": self.content,
            "source_entities": self.source_entities,
            "strength_threshold": self.strength_threshold,
            "original_tokens": self.original_tokens,
            "compressed_tokens": self.compressed_tokens,
            "created_by": "working_memory_engine",
        }
        if self.error:
            result["error"] = self.error
        return result


# ========== WorkingMemoryEngine ==========

class WorkingMemoryEngine:
    """Working Memory compression engine with 3-level layered compression."""

    # Compression ratios (approximate)
    LEVEL1_RATIO = 1.0
    LEVEL2_RATIO = 0.1
    LEVEL3_RATIO = 0.02

    # Default strength threshold for Level 3
    DEFAULT_STRENGTH_THRESHOLD = 0.7

    # Maximum entities to include in Level 3
    MAX_KEY_FACTS = 20

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()

    # --- Public API ---

    def compress(
        self,
        session_content: str,
        session_id: str,
        level: int,
        strength_threshold: float = None,
    ) -> WorkingMemoryEntry:
        """Compress session content at specified level.

        Args:
            session_content: Full session text content
            session_id: Unique session identifier
            level: Compression level (1=full, 2=summary, 3=key facts)
            strength_threshold: Minimum strength for Level 3 (default 0.7)

        Returns:
            WorkingMemoryEntry with compressed content

        Raises:
            ValueError: If level is not 1, 2, or 3
        """
        if level == 1:
            return self._compress_level1(session_content, session_id)
        elif level == 2:
            return self._compress_level2(session_content, session_id)
        elif level == 3:
            threshold = strength_threshold or self.DEFAULT_STRENGTH_THRESHOLD
            return self._compress_level3(session_id, threshold)
        else:
            raise ValueError(f"Invalid compression level: {level}. Must be 1, 2, or 3.")

    def recover(self, session_id: str, level: int) -> str:
        """Recover session content at specified compression level.

        Tries exact level match first, then falls back to lower levels.

        Args:
            session_id: Session identifier
            level: Desired compression level

        Returns:
            Reconstructed content string, or error message if not found
        """
        entries = self._load_session_entries(session_id)

        # Try exact level first
        for entry in entries:
            if entry.get('compression_level') == level:
                return self._reconstruct_content(entry)

        # Fallback to lower levels
        for lvl in range(level - 1, 0, -1):
            for entry in entries:
                if entry.get('compression_level') == lvl:
                    return self._reconstruct_content(entry)

        return f"No working memory found for session {session_id}"

    def get_stats(self) -> Dict:
        """Get working memory statistics.

        Returns:
            Dict with entries count, sessions count, levels distribution
        """
        if not WORKING_MEMORY_FILE.exists():
            return {
                "total_entries": 0,
                "total_sessions": 0,
                "by_level": {1: 0, 2: 0, 3: 0},
            }

        by_level = {1: 0, 2: 0, 3: 0}
        sessions = set()
        total = 0

        with open(WORKING_MEMORY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or not line.startswith('{'):
                    continue
                try:
                    op = json.loads(line)
                    entry = op.get('entry', {})
                    lvl = entry.get('compression_level', 0)
                    if lvl in by_level:
                        by_level[lvl] += 1
                        total += 1
                    sid = entry.get('session_id')
                    if sid:
                        sessions.add(sid)
                except json.JSONDecodeError:
                    continue

        return {
            "total_entries": total,
            "total_sessions": len(sessions),
            "by_level": by_level,
        }

    # --- Compression Methods ---

    def _compress_level1(
        self, content: str, session_id: str
    ) -> WorkingMemoryEntry:
        """Level 1: Full content retention — no compression."""
        original_tokens = self._estimate_tokens(content)

        return WorkingMemoryEntry(
            id=self._generate_id(),
            session_id=session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            compression_level=1,
            content={"full_text": content},
            source_entities=[],
            strength_threshold=0.0,
            original_tokens=original_tokens,
            compressed_tokens=original_tokens,
        )

    def _compress_level2(
        self, content: str, session_id: str
    ) -> WorkingMemoryEntry:
        """Level 2: LLM-generated summary with entity reference extraction."""
        original_tokens = self._estimate_tokens(content)

        # Get summary via LLM with robust JSON extraction
        prompt = SUMMARY_PROMPT.format(content=content)
        summary = self._call_llm_summary(prompt)
        if summary is None:
            summary = self._template_summary(content)

        # Extract KG entity references from content
        entity_refs = self._extract_entity_mentions(content)
        summary_tokens = self._estimate_tokens(summary)

        return WorkingMemoryEntry(
            id=self._generate_id(),
            session_id=session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            compression_level=2,
            content={"summary": summary},
            source_entities=entity_refs,
            strength_threshold=0.0,
            original_tokens=original_tokens,
            compressed_tokens=summary_tokens,
        )

    def _compress_level3(
        self, session_id: str, strength_threshold: float
    ) -> WorkingMemoryEntry:
        """Level 3: Only high-strength KG entities."""
        try:
            all_entities = load_all_entities()
        except Exception as e:
            warnings.warn(f"KG unavailable during Level 3 compression: {e}")
            return WorkingMemoryEntry(
                id=self._generate_id(),
                session_id=session_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                compression_level=3,
                content={"key_facts": []},
                source_entities=[],
                strength_threshold=strength_threshold,
                original_tokens=0,
                compressed_tokens=0,
                error="KG unavailable",
            )

        # Filter by strength threshold
        high_strength = [
            e for e in all_entities.values()
            if e.get('properties', {}).get('strength', 0) >= strength_threshold
        ]
        # Sort by strength descending and limit
        high_strength.sort(
            key=lambda e: e.get('properties', {}).get('strength', 0),
            reverse=True
        )
        high_strength = high_strength[:self.MAX_KEY_FACTS]

        # Build key facts
        key_facts = []
        for entity in high_strength:
            props = entity.get('properties', {})
            key_facts.append({
                "entity_ref": entity.get('id', ''),
                "entity_type": entity.get('type', ''),
                "fact": (props.get('title') or props.get('rationale') or '')[:200],
                "strength": props.get('strength', 0),
            })

        summary = (
            f"Session {session_id}: {len(key_facts)} high-strength entities "
            f"(threshold={strength_threshold})"
        )

        return WorkingMemoryEntry(
            id=self._generate_id(),
            session_id=session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            compression_level=3,
            content={"summary": summary, "key_facts": key_facts},
            source_entities=[e.get('id', '') for e in high_strength],
            strength_threshold=strength_threshold,
            original_tokens=0,
            compressed_tokens=sum(
                self._estimate_tokens(kf['fact']) for kf in key_facts
            ),
        )

    # --- LLM Methods ---

    def _call_llm_summary(self, prompt: str) -> Optional[str]:
        """Call LLM for summarization with robust JSON extraction.

        Tries:
        1. json.loads() directly
        2. Strip markdown code fences and retry
        3. None (caller falls back to template)
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a professional summarization assistant. "
                    "Output ONLY valid JSON, no markdown, no explanation."
                )
            },
            {"role": "user", "content": prompt}
        ]
        response = self.llm_client.call(messages, temperature=0.3)
        if not response:
            return None

        # Try direct JSON parse
        try:
            data = json.loads(response)
            summary = data.get('summary', '')
            if summary and len(summary) < len(response):
                return summary
        except json.JSONDecodeError:
            pass

        # Try stripping markdown code fences
        stripped = self._strip_markdown_fences(response)
        try:
            data = json.loads(stripped)
            summary = data.get('summary', '')
            if summary:
                warnings.warn(
                    "LLM returned markdown-wrapped JSON — stripped fences"
                )
                return summary
        except json.JSONDecodeError:
            pass

        warnings.warn(
            f"LLM did not return valid JSON summary. "
            f"Response preview: {response[:100]!r}"
        )
        return None

    def _strip_markdown_fences(self, text: str) -> str:
        """Strip markdown JSON code fences from text."""
        text = text.strip()
        # Remove ```json ... ``` or ``` ... ```
        if text.startswith('```'):
            lines = text.split('\n')
            # Remove first line (```json or ```)
            if lines[0].startswith('```'):
                lines = lines[1:]
            # Remove last line (```)
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            text = '\n'.join(lines)
        return text

    def _template_summary(self, content: str) -> str:
        """Template-based summary fallback when LLM unavailable."""
        if not content:
            return ""

        # Simple extractive: first sentence + last sentence
        sentences = content.replace('\n', '。').split('。')
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= 2:
            return content[:500]
        return f"{sentences[0]}。... {sentences[-1]}。"

    # --- KG Integration ---

    def _extract_entity_mentions(self, content: str) -> List[str]:
        """Extract KG entity references from content.

        Matches entity titles mentioned in content against loaded KG entities.
        """
        try:
            all_entities = load_all_entities()
        except Exception:
            return []

        mentioned = []
        for entity in all_entities.values():
            title = entity.get('properties', {}).get('title', '')
            if title and title in content:
                mentioned.append(entity.get('id', ''))

        return mentioned[:10]  # Limit to 10 references

    # --- Storage Methods ---

    def _load_session_entries(self, session_id: str) -> List[Dict]:
        """Load working memory entries for a session.

        Skips malformed lines but warns about them.
        """
        if not WORKING_MEMORY_FILE.exists():
            return []

        entries = []
        skipped = 0
        with open(WORKING_MEMORY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or not line.startswith('{'):
                    continue
                try:
                    op = json.loads(line)
                    entry = op.get('entry', {})
                    if entry.get('session_id') == session_id:
                        entries.append(entry)
                except json.JSONDecodeError:
                    skipped += 1
                    continue

        if skipped > 0:
            warnings.warn(
                f"Skipped {skipped} corrupted JSON line(s) in working_memory.jsonl"
            )
        return entries

    def _write_entry(self, entry: WorkingMemoryEntry):
        """Write entry to working_memory.jsonl with file lock."""
        WORKING_MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

        operation = {
            "op": "write",
            "entry": entry.to_entry_dict(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        lock_file = WORKING_MEMORY_FILE.with_suffix('.lock')
        # Use 'a' mode to avoid TOCTOU race: truncate-before-lock
        # Open lock file first, then acquire exclusive lock
        lock_f = open(lock_file, 'a')
        try:
            fcntl.flock(lock_f.fileno(), fcntl.LOCK_EX)
            try:
                with open(WORKING_MEMORY_FILE, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(operation, ensure_ascii=False) + '\n')
            finally:
                fcntl.flock(lock_f.fileno(), fcntl.LOCK_UN)
        finally:
            lock_f.close()

    def _reconstruct_content(self, entry: Dict) -> str:
        """Reconstruct human-readable content from an entry."""
        level = entry.get('compression_level', 1)
        content = entry.get('content', {})

        if level == 1:
            return content.get('full_text', '')
        elif level == 2:
            return content.get('summary', '')
        elif level == 3:
            facts = content.get('key_facts', [])
            if not facts:
                return content.get('summary', '')
            threshold = entry.get('strength_threshold', 0)
            lines = [
                f"Key facts (threshold={threshold}, {len(facts)} entities):"
            ]
            for fact in facts:
                entity_type = fact.get('entity_type', 'unknown')
                strength = fact.get('strength', 0)
                fact_text = fact.get('fact', '')
                lines.append(
                    f"  - [{entity_type}] {fact_text} (strength={strength:.2f})"
                )
            return '\n'.join(lines)
        return ''

    # --- Helper Methods ---

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation.

        Chinese: ~1 token per character
        English: ~1 token per word
        """
        if not text:
            return 0
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        english_words = len([w for w in text.split() if w.isascii()])
        return chinese_chars + english_words

    def _generate_id(self) -> str:
        """Generate a unique working memory entry ID."""
        return f"wm_{uuid.uuid4().hex[:12]}"


# ========== CLI ==========

def main():
    parser = argparse.ArgumentParser(
        description='WorkingMemoryEngine — Context Window Layered Compression'
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # run command
    run_parser = subparsers.add_parser('run', help='Compress and save working memory')
    run_parser.add_argument(
        '--session-id', required=True, help='Session ID'
    )
    run_parser.add_argument(
        '--level', type=int, default=2,
        help='Compression level (1=full, 2=summary, 3=key facts)'
    )
    run_parser.add_argument(
        '--threshold', type=float, default=0.7,
        help='Strength threshold for Level 3 (default 0.7)'
    )
    run_parser.add_argument(
        '--content',
        help='Session content (reads from stdin if not provided)'
    )

    # recover command
    recover_parser = subparsers.add_parser(
        'recover', help='Recover working memory content'
    )
    recover_parser.add_argument(
        '--session-id', required=True, help='Session ID'
    )
    recover_parser.add_argument(
        '--level', type=int, default=3,
        help='Desired compression level'
    )

    # stats command
    subparsers.add_parser('stats', help='Show working memory statistics')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    engine = WorkingMemoryEngine()

    if args.command == 'run':
        content = args.content or sys.stdin.read()
        entry = engine.compress(
            content,
            args.session_id,
            args.level,
            args.threshold
        )
        engine._write_entry(entry)
        msg = f"Saved working memory: {entry.id} (level={entry.compression_level})"
        if entry.error:
            msg += f" [error: {entry.error}]"
        print(msg)

    elif args.command == 'recover':
        content = engine.recover(args.session_id, args.level)
        print(content)

    elif args.command == 'stats':
        stats = engine.get_stats()
        print(f"Total entries: {stats['total_entries']}")
        print(f"Total sessions: {stats['total_sessions']}")
        print(f"By level: L1={stats['by_level'][1]}, "
              f"L2={stats['by_level'][2]}, L3={stats['by_level'][3]}")


if __name__ == '__main__':
    main()
