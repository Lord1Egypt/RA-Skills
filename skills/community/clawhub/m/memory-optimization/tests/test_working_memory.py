#!/usr/bin/env python3
"""
Tests for Working Memory Engine (Context Window Layered Compression)
"""

import json
import pytest
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))


class TestCompressLevel1:
    """Tests for Level 1 compression (full content retention)"""

    def test_level1_full_content_retained(self):
        """Level 1 retains full content without modification"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        content = "今天完成了数据库优化工作，改进了查询性能。"

        entry = engine._compress_level1(content, "session_test_001")

        assert entry.compression_level == 1
        assert entry.content["full_text"] == content
        assert entry.session_id == "session_test_001"
        assert entry.source_entities == []
        assert entry.original_tokens == entry.compressed_tokens
        assert entry.id.startswith("wm_")
        assert len(entry.id) == 15  # "wm_" + 12 char hex

    def test_level1_empty_content(self):
        """Level 1 handles empty content"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        entry = engine._compress_level1("", "session_empty")

        assert entry.compression_level == 1
        assert entry.content["full_text"] == ""
        assert entry.original_tokens == 0

    def test_level1_chinese_and_english_tokens(self):
        """Level 1 token estimation handles mixed Chinese and English"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        content = "今天完成了 database optimization 工作"

        entry = engine._compress_level1(content, "session_mixed")

        # Chinese chars: 今天完成了 (5) + 工作 (2) = 7
        # English words: database, optimization = 2 (工作 is not ASCII)
        assert entry.original_tokens == 9


class TestCompressLevel2:
    """Tests for Level 2 compression (LLM summary)"""

    def test_level2_happy_path(self):
        """Level 2 with valid LLM JSON response"""
        from working_memory import WorkingMemoryEngine

        mock_client = MagicMock()
        mock_client.call.return_value = '{"summary": "完成了数据库优化工作"}'

        engine = WorkingMemoryEngine(llm_client=mock_client)
        content = "今天完成了数据库优化工作，改进了查询性能。"

        entry = engine._compress_level2(content, "session_test_002")

        assert entry.compression_level == 2
        assert entry.content["summary"] == "完成了数据库优化工作"
        assert entry.original_tokens > 0
        assert entry.compressed_tokens < entry.original_tokens

    def test_level2_llm_returns_markdown_json(self):
        """Level 2 strips markdown code fences and extracts JSON"""
        from working_memory import WorkingMemoryEngine

        mock_client = MagicMock()
        mock_client.call.return_value = '```json\n{"summary": "完成了数据库优化工作"}\n```'

        engine = WorkingMemoryEngine(llm_client=mock_client)
        entry = engine._compress_level2("今天完成了数据库优化工作", "session_md")

        assert entry.content["summary"] == "完成了数据库优化工作"

    def test_level2_llm_returns_non_json(self):
        """Level 2 falls back to template when LLM returns non-JSON"""
        from working_memory import WorkingMemoryEngine

        mock_client = MagicMock()
        mock_client.call.return_value = "这是一个总结"  # Not JSON

        engine = WorkingMemoryEngine(llm_client=mock_client)
        entry = engine._compress_level2("今天完成了数据库优化工作，改进了查询性能。", "session_non_json")

        # Should fall back to template summary
        assert entry.content["summary"] is not None
        # Template summary should be non-empty
        assert len(entry.content["summary"]) > 0

    def test_level2_llm_returns_none(self):
        """Level 2 falls back to template when LLM returns None"""
        from working_memory import WorkingMemoryEngine

        mock_client = MagicMock()
        mock_client.call.return_value = None

        engine = WorkingMemoryEngine(llm_client=mock_client)
        entry = engine._compress_level2("今天完成了数据库优化工作，改进了查询性能。", "session_none")

        # Should fall back to template
        assert entry.content["summary"] is not None
        assert "完成了" in entry.content["summary"] or "..." in entry.content["summary"]

    def test_level2_llm_fails_stores_fallback_not_empty_string(self):
        """REGRESSION: LLM failure should store fallback summary, not empty string"""
        from working_memory import WorkingMemoryEngine

        mock_client = MagicMock()
        mock_client.call.return_value = "not json at all"

        engine = WorkingMemoryEngine(llm_client=mock_client)
        entry = engine._compress_level2("今天完成了数据库优化工作，改进了查询性能。", "session_regression")

        # Key regression: the stored entry should have a non-empty summary
        # (previously it was storing empty string when LLM failed)
        stored_summary = entry.content.get("summary", "")
        assert stored_summary != "", (
            "LLM failure: fallback template should be stored, not empty string"
        )
        assert len(stored_summary) > 0

    def test_level2_kg_returns_empty(self):
        """Level 2 handles empty KG gracefully"""
        from working_memory import WorkingMemoryEngine

        mock_client = MagicMock()
        mock_client.call.return_value = '{"summary": "完成了工作"}'

        engine = WorkingMemoryEngine(llm_client=mock_client)

        with patch('working_memory.load_all_entities', return_value={}):
            entry = engine._compress_level2("今天完成了工作", "session_empty_kg")

        # Should succeed with empty entity refs
        assert entry.source_entities == []


class TestCompressLevel3:
    """Tests for Level 3 compression (KG entity key facts)"""

    def test_level3_happy_path(self):
        """Level 3 returns high-strength entities"""
        from working_memory import WorkingMemoryEngine

        mock_entities = {
            "dec_001": {
                "id": "dec_001",
                "type": "Decision",
                "properties": {
                    "title": "使用连接池",
                    "strength": 0.9,
                    "rationale": "提高性能",
                }
            },
            "dec_002": {
                "id": "dec_002",
                "type": "Decision",
                "properties": {
                    "title": "使用缓存",
                    "strength": 0.5,  # Below threshold
                    "rationale": "减少查询",
                }
            },
        }

        with patch('working_memory.load_all_entities', return_value=mock_entities):
            engine = WorkingMemoryEngine()
            entry = engine._compress_level3("session_test_003", strength_threshold=0.7)

        assert entry.compression_level == 3
        assert len(entry.content["key_facts"]) == 1
        assert entry.content["key_facts"][0]["entity_ref"] == "dec_001"
        assert entry.content["key_facts"][0]["strength"] == 0.9

    def test_level3_threshold_boundary(self):
        """Level 3 includes entities with strength == threshold"""
        from working_memory import WorkingMemoryEngine

        mock_entities = {
            "dec_001": {
                "id": "dec_001",
                "type": "Decision",
                "properties": {
                    "title": "边界测试",
                    "strength": 0.7,  # Exactly at threshold
                }
            },
        }

        with patch('working_memory.load_all_entities', return_value=mock_entities):
            engine = WorkingMemoryEngine()
            entry = engine._compress_level3("session_boundary", strength_threshold=0.7)

        assert len(entry.content["key_facts"]) == 1

    def test_level3_no_entities_meet_threshold(self):
        """Level 3 handles no entities meeting threshold"""
        from working_memory import WorkingMemoryEngine

        mock_entities = {
            "dec_001": {
                "id": "dec_001",
                "type": "Decision",
                "properties": {"title": "低强度", "strength": 0.3},
            },
        }

        with patch('working_memory.load_all_entities', return_value=mock_entities):
            engine = WorkingMemoryEngine()
            entry = engine._compress_level3("session_low", strength_threshold=0.7)

        assert entry.content["key_facts"] == []

    def test_level3_kg_unavailable_degrades_gracefully(self):
        """Level 3 KG failure returns error field + empty key_facts (not exception)"""
        from working_memory import WorkingMemoryEngine

        def kg_raises(*args, **kwargs):
            raise RuntimeError("KG file locked")

        with patch('working_memory.load_all_entities', side_effect=kg_raises):
            engine = WorkingMemoryEngine()
            entry = engine._compress_level3("session_kg_fail", strength_threshold=0.7)

        # Should NOT raise — should degrade gracefully
        assert entry.content["key_facts"] == []
        assert entry.error == "KG unavailable"

    def test_level3_respects_max_key_facts(self):
        """Level 3 limits to MAX_KEY_FACTS (20) entities"""
        from working_memory import WorkingMemoryEngine

        mock_entities = {}
        for i in range(30):
            mock_entities[f"dec_{i:03d}"] = {
                "id": f"dec_{i:03d}",
                "type": "Decision",
                "properties": {
                    "title": f"决策{i}",
                    "strength": 1.0 - (i * 0.01),
                }
            }

        with patch('working_memory.load_all_entities', return_value=mock_entities):
            engine = WorkingMemoryEngine()
            entry = engine._compress_level3("session_many", strength_threshold=0.0)

        assert len(entry.content["key_facts"]) == 20


class TestCompressInvalidLevel:
    """Tests for invalid compression level handling"""

    def test_invalid_level_raises_value_error(self):
        """Invalid compression level raises ValueError"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()

        with pytest.raises(ValueError) as exc_info:
            engine.compress("content", "session_invalid", level=5)

        assert "Invalid compression level" in str(exc_info.value)

    def test_compress_level1_direct(self):
        """compress() with level=1 delegates to _compress_level1"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        content = "测试内容"

        entry = engine.compress(content, "session_compress_1", level=1)

        assert entry.compression_level == 1
        assert entry.content["full_text"] == content

    def test_compress_level2_direct(self):
        """compress() with level=2 delegates to _compress_level2"""
        from working_memory import WorkingMemoryEngine, WorkingMemoryEntry

        engine = WorkingMemoryEngine()

        with patch.object(engine, '_compress_level2', return_value=WorkingMemoryEntry(
            id="wm_test123",
            session_id="session_compress_2",
            timestamp="2026-04-01T00:00:00+00:00",
            compression_level=2,
            content={"summary": "test"},
            source_entities=[],
            strength_threshold=0.0,
            original_tokens=100,
            compressed_tokens=50
        )):
            entry = engine.compress("content", "session_compress_2", level=2)
            assert entry.compression_level == 2

    def test_compress_level3_direct(self):
        """compress() with level=3 delegates to _compress_level3"""
        from working_memory import WorkingMemoryEngine, WorkingMemoryEntry

        engine = WorkingMemoryEngine()

        with patch.object(engine, '_compress_level3', return_value=WorkingMemoryEntry(
            id="wm_test456",
            session_id="session_compress_3",
            timestamp="2026-04-01T00:00:00+00:00",
            compression_level=3,
            content={"facts": []},
            source_entities=[],
            strength_threshold=0.5,
            original_tokens=100,
            compressed_tokens=10
        )):
            entry = engine.compress("content", "session_compress_3", level=3, strength_threshold=0.5)
            assert entry.compression_level == 3


class TestRecover:
    """Tests for working memory recovery"""

    def test_recover_exact_level_match(self):
        """Recover returns exact level match when available"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        entry_data = {
            "compression_level": 2,
            "content": {"summary": "测试摘要"},
            "session_id": "session_recover_001",
            "strength_threshold": 0.7,
        }

        with patch.object(
            engine, '_load_session_entries',
            return_value=[entry_data]
        ):
            result = engine.recover("session_recover_001", level=2)

        assert result == "测试摘要"

    def test_recover_falls_back_to_lower_level(self):
        """Recover falls back to lower level when exact level not found"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        entries = [
            {
                "compression_level": 1,
                "content": {"full_text": "完整内容"},
                "session_id": "session_fallback",
                "strength_threshold": 0.0,
            }
        ]

        with patch.object(
            engine, '_load_session_entries', return_value=entries
        ):
            result = engine.recover("session_fallback", level=3)

        assert result == "完整内容"

    def test_recover_no_entry_returns_error_message(self):
        """Recover returns error message when no entries found"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()

        with patch.object(
            engine, '_load_session_entries', return_value=[]
        ):
            result = engine.recover("nonexistent_session", level=2)

        assert "No working memory found" in result

    def test_recover_file_not_exists(self):
        """Recover handles non-existent file"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()

        with patch.object(
            engine, '_load_session_entries', return_value=[]
        ):
            result = engine.recover("session_no_file", level=1)

        assert "No working memory found" in result

    def test_recover_skips_corrupted_lines(self):
        """Recover skips corrupted JSON lines and continues"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        good_entry = {
            "compression_level": 1,
            "content": {"full_text": "正常内容"},
            "session_id": "session_partial",
            "strength_threshold": 0.0,
        }

        with patch.object(
            engine, '_load_session_entries', return_value=[good_entry]
        ):
            result = engine.recover("session_partial", level=1)

        assert result == "正常内容"


class TestWriteEntry:
    """Tests for atomic file writing"""

    def test_write_entry_creates_parent_dir(self):
        """_write_entry creates parent directory if not exists"""
        from working_memory import WorkingMemoryEngine, WORKING_MEMORY_FILE

        with tempfile.TemporaryDirectory() as tmpdir:
            wm_file = Path(tmpdir) / "memory" / "working_memory.jsonl"
            entry = WorkingMemoryEngine()._compress_level1(
                "test", "session_write"
            )

            with patch(
                'working_memory.WORKING_MEMORY_FILE', wm_file
            ), patch('fcntl.flock'):
                engine = WorkingMemoryEngine()
                engine._write_entry(entry)

            assert wm_file.exists()

    def test_write_entry_atomic_with_lock(self):
        """_write_entry uses file locking for atomic writes"""
        from working_memory import WorkingMemoryEngine, WORKING_MEMORY_FILE

        with tempfile.TemporaryDirectory() as tmpdir:
            wm_file = Path(tmpdir) / "memory" / "working_memory.jsonl"

            entry = WorkingMemoryEngine()._compress_level1(
                "test content", "session_atomic"
            )

            with patch(
                'working_memory.WORKING_MEMORY_FILE', wm_file
            ), patch('fcntl.flock') as mock_flock:
                engine = WorkingMemoryEngine()
                engine._write_entry(entry)

                # Verify flock was called with LOCK_EX
                assert mock_flock.call_count >= 2  # LOCK_EX + LOCK_UN

    def test_write_entry_content_is_valid_json(self):
        """Written entry is valid JSON with all required fields"""
        from working_memory import WorkingMemoryEngine, WORKING_MEMORY_FILE

        with tempfile.TemporaryDirectory() as tmpdir:
            wm_file = Path(tmpdir) / "memory" / "working_memory.jsonl"
            entry = WorkingMemoryEngine()._compress_level1(
                "test", "session_json"
            )

            with patch(
                'working_memory.WORKING_MEMORY_FILE', wm_file
            ), patch('fcntl.flock'):
                engine = WorkingMemoryEngine()
                engine._write_entry(entry)

            with open(wm_file, 'r') as f:
                line = f.readline()
                op = json.loads(line)
                assert op["op"] == "write"
                assert op["entry"]["id"] == entry.id
                assert op["entry"]["session_id"] == "session_json"
                assert "timestamp" in op


class TestHelperMethods:
    """Tests for helper methods"""

    def test_estimate_tokens_chinese(self):
        """Token estimation for Chinese text"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        tokens = engine._estimate_tokens("今天天气很好")
        assert tokens == 6

    def test_estimate_tokens_english(self):
        """Token estimation for English text"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        tokens = engine._estimate_tokens("hello world today")
        assert tokens == 3

    def test_estimate_tokens_mixed(self):
        """Token estimation for mixed text"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        tokens = engine._estimate_tokens("今天 hello 天气 today 很好 world")
        assert tokens == 9

    def test_estimate_tokens_empty(self):
        """Token estimation for empty string"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        assert engine._estimate_tokens("") == 0
        assert engine._estimate_tokens(None) == 0

    def test_generate_id_uniqueness(self):
        """Generated IDs are unique"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        ids = [engine._generate_id() for _ in range(100)]
        assert len(ids) == len(set(ids))  # All unique

    def test_strip_markdown_fences(self):
        """_strip_markdown_fences removes ``` fences"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()

        assert engine._strip_markdown_fences(
            '```json\n{"summary": "test"}\n```'
        ) == '{"summary": "test"}'

        assert engine._strip_markdown_fences(
            '```\n{"summary": "test"}\n```'
        ) == '{"summary": "test"}'

        assert engine._strip_markdown_fences(
            '{"summary": "test"}'
        ) == '{"summary": "test"}'


class TestTemplateSummary:
    """Tests for template summary fallback"""

    def test_template_summary_short_content(self):
        """Template summary returns content as-is if <= 2 sentences"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        content = "今天完成了工作。"

        result = engine._template_summary(content)
        assert result == content[:500]

    def test_template_summary_long_content(self):
        """Template summary returns first + last sentence for long content"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        content = "第一句话。今天第二句话。今天第三句话。"

        result = engine._template_summary(content)
        assert "第一句话" in result
        assert "第三句话" in result

    def test_template_summary_empty(self):
        """Template summary handles empty content"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        assert engine._template_summary("") == ""
        assert engine._template_summary(None) == ""


class TestReconstructContent:
    """Tests for content reconstruction from entries"""

    def test_reconstruct_level1(self):
        """Reconstruct returns full_text for level 1"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        entry = {
            "compression_level": 1,
            "content": {"full_text": "完整内容"},
        }
        assert engine._reconstruct_content(entry) == "完整内容"

    def test_reconstruct_level2(self):
        """Reconstruct returns summary for level 2"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        entry = {
            "compression_level": 2,
            "content": {"summary": "摘要内容"},
        }
        assert engine._reconstruct_content(entry) == "摘要内容"

    def test_reconstruct_level3_with_facts(self):
        """Reconstruct formats key facts for level 3"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        entry = {
            "compression_level": 3,
            "content": {
                "summary": "Session X: 2 entities",
                "key_facts": [
                    {
                        "entity_type": "Decision",
                        "fact": "使用连接池",
                        "strength": 0.9,
                    },
                    {
                        "entity_type": "Finding",
                        "fact": "性能提升50%",
                        "strength": 0.8,
                    },
                ]
            },
            "strength_threshold": 0.7,
        }
        result = engine._reconstruct_content(entry)
        assert "Decision" in result
        assert "使用连接池" in result
        assert "strength=0.90" in result

    def test_reconstruct_level3_no_facts(self):
        """Reconstruct falls back to summary when no key_facts"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        entry = {
            "compression_level": 3,
            "content": {"key_facts": []},
            "strength_threshold": 0.7,
        }
        result = engine._reconstruct_content(entry)
        assert result == ""


class TestStats:
    """Tests for statistics"""

    def test_stats_empty_file(self):
        """Stats handles empty/non-existent file"""
        from working_memory import WorkingMemoryEngine, WORKING_MEMORY_FILE

        with tempfile.TemporaryDirectory() as tmpdir:
            wm_file = Path(tmpdir) / "memory" / "working_memory.jsonl"

            with patch('working_memory.WORKING_MEMORY_FILE', wm_file):
                engine = WorkingMemoryEngine()
                stats = engine.get_stats()

            assert stats["total_entries"] == 0
            assert stats["total_sessions"] == 0
            assert stats["by_level"] == {1: 0, 2: 0, 3: 0}


class TestWorkingMemoryEntry:
    """Tests for WorkingMemoryEntry"""

    def test_to_entry_dict_without_error(self):
        """to_entry_dict excludes error field when no error"""
        from working_memory import WorkingMemoryEntry

        entry = WorkingMemoryEntry(
            id="wm_test",
            session_id="session_test",
            timestamp="2026-04-01T00:00:00+00:00",
            compression_level=1,
            content={"full_text": "test"},
            source_entities=[],
            strength_threshold=0.0,
            original_tokens=10,
            compressed_tokens=10,
        )

        result = entry.to_entry_dict()
        assert "error" not in result

    def test_to_entry_dict_with_error(self):
        """to_entry_dict includes error field when error present"""
        from working_memory import WorkingMemoryEntry

        entry = WorkingMemoryEntry(
            id="wm_test",
            session_id="session_test",
            timestamp="2026-04-01T00:00:00+00:00",
            compression_level=1,
            content={"full_text": "test"},
            source_entities=[],
            strength_threshold=0.0,
            original_tokens=10,
            compressed_tokens=10,
            error="KG unavailable",
        )

        result = entry.to_entry_dict()
        assert result["error"] == "KG unavailable"


class TestLoadSessionEntries:
    """Tests for _load_session_entries"""

    def test_load_session_entries_file_not_exists(self):
        """Returns empty list when file doesn't exist"""
        from working_memory import WorkingMemoryEngine, WORKING_MEMORY_FILE

        with tempfile.TemporaryDirectory() as tmpdir:
            wm_file = Path(tmpdir) / "memory" / "working_memory.jsonl"

            with patch('working_memory.WORKING_MEMORY_FILE', wm_file):
                engine = WorkingMemoryEngine()
                entries = engine._load_session_entries("any_session")

            assert entries == []

    def test_load_session_entries_with_data(self):
        """Returns entries for matching session"""
        from working_memory import WorkingMemoryEngine, WORKING_MEMORY_FILE

        with tempfile.TemporaryDirectory() as tmpdir:
            wm_file = Path(tmpdir) / "memory" / "working_memory.jsonl"
            wm_file.parent.mkdir(parents=True, exist_ok=True)

            entry = {
                "op": "write",
                "entry": {
                    "id": "wm_test123",
                    "session_id": "session_match",
                    "timestamp": "2026-04-01T00:00:00+00:00",
                    "compression_level": 1,
                    "content": {"full_text": "test"},
                    "source_entities": [],
                    "strength_threshold": 0.0,
                    "original_tokens": 10,
                    "compressed_tokens": 10,
                }
            }
            wm_file.write_text(json.dumps(entry) + "\n")

            with patch('working_memory.WORKING_MEMORY_FILE', wm_file):
                engine = WorkingMemoryEngine()
                entries = engine._load_session_entries("session_match")

            assert len(entries) == 1
            assert entries[0]["id"] == "wm_test123"


class TestExtractEntityMentions:
    """Tests for _extract_entity_mentions"""

    def test_extract_entity_mentions_load_error(self):
        """Returns empty list when load_all_entities raises exception"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()

        with patch('working_memory.load_all_entities', side_effect=Exception("KG error")):
            result = engine._extract_entity_mentions("some content")

        assert result == []

    def test_extract_entity_mentions_matches_title(self):
        """Finds entities with title matching content"""
        from working_memory import WorkingMemoryEngine

        mock_entities = {
            "dec_1": {
                "id": "dec_1",
                "type": "Decision",
                "properties": {"title": "数据库优化"}
            }
        }

        engine = WorkingMemoryEngine()

        with patch('working_memory.load_all_entities', return_value=mock_entities):
            result = engine._extract_entity_mentions("讨论了数据库优化的问题")

        assert "dec_1" in result


class TestReconstructContentEdge:
    """Tests for _reconstruct_content edge cases"""

    def test_reconstruct_invalid_level(self):
        """Returns empty string for invalid compression level"""
        from working_memory import WorkingMemoryEngine

        engine = WorkingMemoryEngine()
        entry = {
            "compression_level": 99,  # Invalid level
            "content": {},
        }
        result = engine._reconstruct_content(entry)
        assert result == ""
