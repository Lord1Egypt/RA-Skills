#!/usr/bin/env python3
"""Tests for novel_rag — RAG semantic retrieval for writing context."""
import sys
import tempfile
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))

from rag.novel_rag import (
    NovelRAGIndex, RAGDocument, SearchResult,
    format_rag_prompt, build_and_search, DEFAULT_TOP_K,
)
from core.story_state import StoryState, CharacterState, HookState, ChapterRecord


def _make_test_state() -> StoryState:
    state = StoryState(novel_title="测试小说", volume="V1")
    state.characters["char_主角"] = CharacterState(
        id="char_主角", name="林风", role="主角",
        first_appearance=1, last_appearance=10, status="active",
        state="寻找丢失的星辰碎片",
        key_items=["星辰剑", "地图"],
    )
    state.characters["char_导师"] = CharacterState(
        id="char_导师", name="冷月", role="导师",
        first_appearance=1, last_appearance=8, status="active",
        state="守护星辰塔，指导林风修炼",
    )
    state.hooks["hook_星辰碎片"] = HookState(
        id="hook_星辰碎片", description="星辰碎片散落在大陆各处，集齐可打开星界之门",
        type="悬念", chapter_created=1, status="活跃",
    )
    state.hooks["hook_星界之门"] = HookState(
        id="hook_星界之门", description="星界之门在月食之夜会减弱封印",
        type="设定", chapter_created=3, status="活跃",
    )
    state.chapters[5] = ChapterRecord(
        number=5, title="星辰塔的秘密", word_count=3000,
        scene="星辰塔顶", characters_present=["林风", "冷月"],
        key_events=["冷月揭示星辰碎片的历史", "林风第一次感应到碎片", "星辰塔结界被触动"],
        strand_weights={"quest": 0.5, "fire": 0.3, "constellation": 0.2},
    )
    state.chapters[10] = ChapterRecord(
        number=10, title="月食之夜", word_count=2800,
        scene="废弃神庙", characters_present=["林风"],
        key_events=["月食开始", "星界之门封印减弱", "神秘声音从门后传来"],
        strand_weights={"quest": 0.6, "fire": 0.1, "constellation": 0.3},
    )
    return state


def test_basic_index_build():
    """Build index from test state."""
    with tempfile.TemporaryDirectory() as tmp:
        idx = NovelRAGIndex(tmp)
        count = idx.build(_make_test_state())
        assert count >= 6, f"Expected >=6 docs, got {count}"
    print("✅ test_basic_index_build")


def test_search_returns_results():
    """Search should return top-K results."""
    with tempfile.TemporaryDirectory() as tmp:
        idx = NovelRAGIndex(tmp)
        idx.build(_make_test_state())
        results = idx.search("星辰碎片", top_k=3)
        assert len(results) <= 3
        assert len(results) >= 1, f"Expected at least 1 result, got {len(results)}"
        assert all(r.score > 0 for r in results)
    print("✅ test_search_returns_results")


def test_search_category_filter():
    """Category filter should restrict results."""
    with tempfile.TemporaryDirectory() as tmp:
        idx = NovelRAGIndex(tmp)
        idx.build(_make_test_state())
        results = idx.search("星辰", top_k=10, categories=["hook"])
        assert all(r.category == "hook" for r in results)
    print("✅ test_search_category_filter")


def test_search_min_score():
    """Min score filter should exclude low-similarity results."""
    with tempfile.TemporaryDirectory() as tmp:
        idx = NovelRAGIndex(tmp)
        idx.build(_make_test_state())
        results_default = idx.search("完全不相关的内容！！！", top_k=10)
        results_filtered = idx.search("完全不相关的内容！！！", top_k=10, min_score=0.01)
        assert len(results_filtered) <= len(results_default)
    print("✅ test_search_min_score")


def test_save_load_persistence():
    """Save then load should preserve index."""
    with tempfile.TemporaryDirectory() as tmp:
        idx = NovelRAGIndex(tmp)
        idx.build(_make_test_state())
        idx.save()

        idx2 = NovelRAGIndex.load(tmp)
        assert idx2 is not None
        assert len(idx2._docs) == len(idx._docs)
    print("✅ test_save_load_persistence")


def test_load_missing_cache():
    """Loading from directory without cache should return None."""
    with tempfile.TemporaryDirectory() as tmp:
        idx = NovelRAGIndex.load(tmp)
        assert idx is None
    print("✅ test_load_missing_cache")


def test_format_rag_prompt_empty():
    """Empty results should produce fallback text."""
    text = format_rag_prompt([], top_k=5)
    assert "无相关结果" in text
    print("✅ test_format_rag_prompt_empty")


def test_format_rag_prompt_has_results():
    """Results should produce categorized output."""
    results = [
        SearchResult(doc_id="c1", content="林风", category="character", score=0.9),
        SearchResult(doc_id="h1", content="星辰碎片", category="hook", score=0.8),
    ]
    text = format_rag_prompt(results, top_k=5)
    assert "RAG" in text
    assert "角色" in text and "伏笔" in text
    print("✅ test_format_rag_prompt_has_results")


def test_build_and_search_convenience():
    """Convenience function should build and search in one call."""
    with tempfile.TemporaryDirectory() as tmp:
        # Create a minimal story-state.json so it auto-loads
        state = _make_test_state()
        state.save(tmp)
        results = build_and_search(tmp, "星辰碎片", top_k=3, force_rebuild=True)
        assert len(results) >= 1
    print("✅ test_build_and_search_convenience")


def test_empty_state():
    """Empty state should build index with 0 docs."""
    with tempfile.TemporaryDirectory() as tmp:
        idx = NovelRAGIndex(tmp)
        count = idx.build(StoryState())
        assert count == 0
        results = idx.search("test")
        assert len(results) == 0
    print("✅ test_empty_state")


def test_recent_boost():
    """Recent chapters should get boost."""
    with tempfile.TemporaryDirectory() as tmp:
        idx = NovelRAGIndex(tmp)
        idx.build(_make_test_state())
        results = idx.search("月食", top_k=5, boost_recent=True)
        if results:
            # Ch10 is very recent (max chapter), should be boosted
            ch10_results = [r for r in results if r.chapter == 10]
            if ch10_results:
                assert any(r.chapter == 10 for r in results[:2])
    print("✅ test_recent_boost")


def test_bible_indexing():
    """Index should pick up bible.json characters."""
    with tempfile.TemporaryDirectory() as tmp:
        # Create bible.json
        bible = {
            "title": "测试小说",
            "characters": {
                "林风": {
                    "role": "protagonist",
                    "traits": ["勇敢", "执着"],
                    "background": "星辰镇出身的少年",
                    "motivation": "找回失落的星辰碎片",
                }
            },
            "world_info": "星辰大陆，一共七块星辰碎片"
        }
        (Path(tmp) / "bible.json").write_text(json.dumps(bible, ensure_ascii=False), encoding="utf-8")
        idx = NovelRAGIndex(tmp)
        count = idx.build(_make_test_state())
        assert count >= 8  # +1 from bible character + world info + title
    print("✅ test_bible_indexing")


if __name__ == "__main__":
    test_basic_index_build()
    test_search_returns_results()
    test_search_category_filter()
    test_search_min_score()
    test_save_load_persistence()
    test_load_missing_cache()
    test_format_rag_prompt_empty()
    test_format_rag_prompt_has_results()
    test_build_and_search_convenience()
    test_empty_state()
    test_recent_boost()
    test_bible_indexing()
    print("\n🎉 All RAG tests passed!")
