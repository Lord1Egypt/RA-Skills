#!/usr/bin/env python3
"""Tests for three_laws — 防幻觉三定律 写前/写后校验."""
import sys, json, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))

from agents.three_laws import (
    THREE_LAWS, LAW_LABELS,
    PreWriteValidator, PostWriteValidator,
    LawViolation, ValidationReport,
    format_three_laws_block, _extract_unknown_entities,
)
from core.story_state import StoryState, CharacterState, HookState, ChapterRecord
from core.contract import ChapterCommit, ChapterCommitEvent, StateDelta, EntityDelta


def _make_test_state() -> StoryState:
    state = StoryState(novel_title="测试", volume="V1")
    state.characters["char_林风"] = CharacterState(
        id="char_林风", name="林风", role="主角",
        first_appearance=1, last_appearance=10, status="active",
        state="寻找星辰碎片",
    )
    state.characters["char_冷月"] = CharacterState(
        id="char_冷月", name="冷月", role="导师",
        first_appearance=1, last_appearance=10, status="active",
        state="守护星辰塔",
    )
    state.characters["char_已死"] = CharacterState(
        id="char_已死", name="黑雾尊者", role="反派",
        first_appearance=5, last_appearance=8, status="active",
        state="已被击杀，确认死亡",
    )
    state.chapters[10] = ChapterRecord(
        number=10, title="月食之夜", word_count=2800,
        scene="星辰塔", characters_present=["林风", "冷月"],
        key_events=["月食开始", "封印减弱"],
    )
    return state


def test_three_laws_constants():
    assert len(THREE_LAWS) == 3
    assert "大纲即法律" in THREE_LAWS[0]
    assert "设定即物理" in THREE_LAWS[1]
    assert "发明需识别" in THREE_LAWS[2]
    assert len(LAW_LABELS) == 3
    print("✅ test_three_laws_constants")


def test_law_violation():
    v = LawViolation(law_index=0, severity="P0", category="测试", description="test")
    assert v.law_index == 0
    assert v.severity == "P0"
    print("✅ test_law_violation")


def test_validation_report():
    r = ValidationReport(passed=True)
    assert r.passed
    assert len(r.violations) == 0
    assert r.p0_count == 0
    print("✅ test_validation_report")


def test_validation_report_with_violations():
    v = [LawViolation(law_index=0, severity="P0", category="测试", description="P0 desc"),
         LawViolation(law_index=1, severity="P1", category="测试", description="P1 desc")]
    r = ValidationReport(passed=False, violations=v)
    assert not r.passed
    assert r.p0_count == 1
    assert r.p1_count == 1
    text = r.to_text()
    assert "P0 desc" in text
    assert "大纲即法律" in text
    print("✅ test_validation_report_with_violations")


def test_to_prompt_block():
    v = [LawViolation(law_index=0, severity="P1", category="测试", description="prompt msg",
                      suggestion="fix it")]
    r = ValidationReport(passed=False, violations=v)
    block = r.to_prompt_block()
    assert "三定律预检警告" in block
    assert "prompt msg" in block
    assert "fix it" in block
    print("✅ test_to_prompt_block")


def test_format_three_laws_block():
    block = format_three_laws_block("zh")
    assert "防幻觉三定律" in block
    assert "大纲即法律" in block
    assert block.count("\n") >= 3
    print("✅ test_format_three_laws_block")


def test_extract_unknown_entities():
    known = {"林风"}
    text = "林风说道要去找到星辰碎片。冷月问道塔顶的封印"
    found = _extract_unknown_entities(text, known)
    # 冷月 is in the state but not in `known` for this test
    assert "冷月" in found
    assert "林风" not in found  # already known
    print("✅ test_extract_unknown_entities")


def test_pre_write_law1():
    """PreWriteValidator should flag unknown names in outline."""
    with tempfile.TemporaryDirectory() as tmp:
        state = _make_test_state()
        pv = PreWriteValidator(tmp)
        report = pv.check_outline(11, "林风去讨伐魔王，魔王说要找星辰碎片", state)
        # "魔王" is not in known characters
        unknown_violations = [v for v in report.violations if v.category == "未知角色/地点"]
        assert any("魔王" in v.description for v in unknown_violations), \
            f"Should flag 魔王, got: {[v.description for v in report.violations]}"
    print("✅ test_pre_write_law1")


def test_pre_write_law2_dead_char():
    """PreWriteValidator should flag dead character in outline."""
    with tempfile.TemporaryDirectory() as tmp:
        state = _make_test_state()
        pv = PreWriteValidator(tmp)
        report = pv.check_outline(11, "黑雾尊者复活了", state)
        death_violations = [v for v in report.violations if v.category == "角色状态冲突"]
        assert len(death_violations) >= 1, \
            f"Should flag dead char, got: {[v.description for v in report.violations]}"
    print("✅ test_pre_write_law2_dead_char")


def test_pre_write_law3():
    """PreWriteValidator should flag missing new flag."""
    with tempfile.TemporaryDirectory() as tmp:
        state = _make_test_state()
        pv = PreWriteValidator(tmp)
        # 长大纲（>50 chars）且没有明确的新增标记
        outline = (
            "林风穿过森林来到一片从未见过的山谷。山谷中有废弃的神庙，"
            "庙门上的封印已经松动。冷月说这里可能是星辰碎片最后的沉睡之地。"
            "他们走进去，墙上的壁画讲述了千年前那场战争的故事。"
        )
        report = pv.check_outline(11, outline, state)
        flag_violations = [v for v in report.violations if v.category == "可能遗漏新增标记"]
        assert len(flag_violations) >= 1, (
            f"Should flag missing new flag, got: {[v.description for v in report.violations]}"
        )
    print("✅ test_pre_write_law3")


def test_post_write_new_entities():
    """PostWriteValidator should flag unmarked new entities."""
    with tempfile.TemporaryDirectory() as tmp:
        state = _make_test_state()
        pv = PostWriteValidator(tmp)
        commit = ChapterCommit(
            chapter_number=11,
            chapter_title="测试",
            word_count=1000,
            events=[
                ChapterCommitEvent(event_type="action", description="林风遇到了新角色"),
            ],
            state_delta=StateDelta(
                character_states={"char_林风": "继续前进"},
            ),
            entity_delta=EntityDelta(
                new_characters=[{"name": "白龙", "role": "配角"}],
            ),
            hooks_created=[],
            hooks_resolved=[],
        )
        report = pv.check_commit(11, commit, state)
        new_entity_violations = [v for v in report.violations if v.category == "未标记的新实体"]
        assert len(new_entity_violations) >= 1
    print("✅ test_post_write_new_entities")


def test_post_write_dead_char():
    """PostWriteValidator should flag dead character resurrection."""
    with tempfile.TemporaryDirectory() as tmp:
        state = _make_test_state()
        pv = PostWriteValidator(tmp)
        commit = ChapterCommit(
            chapter_number=11,
            chapter_title="测试",
            word_count=1000,
            events=[ChapterCommitEvent(event_type="action", description="黑雾尊者回来了")],
            state_delta=StateDelta(character_states={"char_已死": "突然复活现身"}),
            entity_delta=EntityDelta(),
            hooks_created=[],
            hooks_resolved=[],
        )
        report = pv.check_commit(11, commit, state)
        dead_violations = [v for v in report.violations if v.category == "角色死而复生"]
        assert len(dead_violations) >= 1
    print("✅ test_post_write_dead_char")


def test_post_write_fake_hook_resolve():
    """PostWriteValidator should flag hook resolution with no matching hook."""
    with tempfile.TemporaryDirectory() as tmp:
        state = _make_test_state()
        pv = PostWriteValidator(tmp)
        commit = ChapterCommit(
            chapter_number=11,
            chapter_title="测试",
            word_count=1000,
            events=[ChapterCommitEvent(event_type="action", description="事件")],
            state_delta=StateDelta(),
            entity_delta=EntityDelta(),
            hooks_created=[],
            hooks_resolved=["不存在的伏笔"],
        )
        report = pv.check_commit(11, commit, state)
        fake_violations = [v for v in report.violations if v.category == "伏笔来源不明"]
        assert len(fake_violations) >= 1
    print("✅ test_post_write_fake_hook_resolve")


def test_pre_write_no_bible_degradation():
    """PreWriteValidator 在无 bible.json 时应正常降级。"""
    with tempfile.TemporaryDirectory() as tmp:
        state = _make_test_state()
        pv = PreWriteValidator(tmp)  # 没有 bible.json
        report = pv.check_outline(11, "林风继续前进", state)
        # 不崩溃就是通过
        assert isinstance(report, ValidationReport)
    print("✅ test_pre_write_no_bible_degradation")


def test_pre_write_chapter_zero():
    """PreWriteValidator 在 chapter=0 时应正常工作。"""
    with tempfile.TemporaryDirectory() as tmp:
        state = _make_test_state()
        pv = PreWriteValidator(tmp)
        report = pv.check_outline(0, "林风说要去星辰塔", state)
        assert isinstance(report, ValidationReport)
    print("✅ test_pre_write_chapter_zero")


def test_extract_names_with_middle_dot():
    """_extract_unknown_entities 应支持带 · 的 5 字名。"""
    known = {"林风"}
    text = "艾琳娜·烬羽说道：星辰碎片在塔顶"
    found = _extract_unknown_entities(text, known)
    assert "艾琳娜·烬羽" in found, f"Should detect 艾琳娜·烬羽, got: {found}"
    print("✅ test_extract_names_with_middle_dot")


def test_clean_chapter_passes():
    """A clean chapter should produce no violations."""
    with tempfile.TemporaryDirectory() as tmp:
        state = _make_test_state()
        pv = PostWriteValidator(tmp)
        commit = ChapterCommit(
            chapter_number=11,
            chapter_title="测试",
            word_count=1000,
            events=[ChapterCommitEvent(event_type="action", description="林风继续走")],
            state_delta=StateDelta(character_states={"char_林风": "继续前进"}),
            entity_delta=EntityDelta(),
            hooks_created=["【新增】白龙——守护星辰塔的远古生物"],
            hooks_resolved=[],
        )
        report = pv.check_commit(11, commit, state)
        assert report.passed, f"Expected clean commit to pass, got violations: {[v.description for v in report.violations]}"
    print("✅ test_clean_chapter_passes")


if __name__ == "__main__":
    test_three_laws_constants()
    test_law_violation()
    test_validation_report()
    test_validation_report_with_violations()
    test_to_prompt_block()
    test_format_three_laws_block()
    test_extract_unknown_entities()
    test_pre_write_law1()
    test_pre_write_law2_dead_char()
    test_pre_write_law3()
    test_post_write_new_entities()
    test_post_write_dead_char()
    test_post_write_fake_hook_resolve()
    test_pre_write_no_bible_degradation()
    test_pre_write_chapter_zero()
    test_extract_names_with_middle_dot()
    test_clean_chapter_passes()
    print("\n🎉 All three_laws tests passed!")
