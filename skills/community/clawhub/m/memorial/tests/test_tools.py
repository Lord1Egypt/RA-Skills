#!/usr/bin/env python3
"""
test_tools.py — 工具链自动化测试

运行：python tests/test_tools.py
"""

import json
import os
import shutil
import sys
import tempfile

# 确保能找到 tools 目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "tools"))

PASSED = 0
FAILED = 0


def test(name):
    def decorator(func):
        def wrapper():
            global PASSED, FAILED
            try:
                func()
                PASSED += 1
                print(f"  [ok] {name}")
            except Exception as e:
                FAILED += 1
                print(f"  [FAIL] {name}: {e}")
        return wrapper
    return decorator


# ── skill_writer tests ────────────────────────────────────────────────────────

@test("skill_writer: create + combine + list")
def test_skill_writer():
    from skill_writer import action_create, action_combine, action_list, memorial_dir
    slug = "__test_writer__"
    base = memorial_dir(slug)
    try:
        action_create("TestPerson", slug)
        assert os.path.exists(os.path.join(base, "SKILL.md"))
        assert os.path.exists(os.path.join(base, "remembrance.md"))
        assert os.path.exists(os.path.join(base, "persona.md"))
        assert os.path.exists(os.path.join(base, "meta.json"))

        with open(os.path.join(base, "SKILL.md"), encoding="utf-8") as f:
            content = f.read()
        assert "name: memorial___test_writer__" in content

        with open(os.path.join(base, "meta.json"), encoding="utf-8") as f:
            meta = json.load(f)
        assert meta["version"] == "v1"
        assert meta["slug"] == slug
    finally:
        if os.path.exists(base):
            shutil.rmtree(base)


# ── version_manager tests ────────────────────────────────────────────────────

@test("version_manager: backup + rollback")
def test_version_manager():
    from skill_writer import action_create, memorial_dir
    from version_manager import action_backup, action_rollback, versions_dir
    slug = "__test_version__"
    base = memorial_dir(slug)
    try:
        action_create("TestVersion", slug)
        rem_path = os.path.join(base, "remembrance.md")

        # Backup original
        action_backup(slug)
        backups = os.listdir(versions_dir(slug))
        assert len(backups) >= 1

        # Modify
        with open(rem_path, encoding="utf-8") as f:
            original = f.read()
        with open(rem_path, "w", encoding="utf-8") as f:
            f.write(original + "\n## Added Section\n")

        # Rollback
        first_backup = sorted(os.listdir(versions_dir(slug)))[0]
        action_rollback(slug, first_backup)

        with open(rem_path, encoding="utf-8") as f:
            restored = f.read()
        assert "Added Section" not in restored
    finally:
        if os.path.exists(base):
            shutil.rmtree(base)


# ── wechat_parser tests ──────────────────────────────────────────────────────

@test("wechat_parser: detect format + parse + analyze")
def test_wechat_parser():
    from wechat_parser import detect_format, parse_wechatmsg_txt, analyze_messages

    sample = "2023-12-25 08:30:00  grandpa\nhello\n2023-12-25 08:31:00  me\nhi\n"
    assert detect_format(sample) == "wechatmsg_txt"

    # parse_wechatmsg_txt expects file content string
    msgs = parse_wechatmsg_txt(sample)
    assert len(msgs) >= 2

    analysis = analyze_messages(msgs, "grandpa")
    assert analysis["total_messages"] >= 1


# ── qq_parser tests ──────────────────────────────────────────────────────────

@test("qq_parser: parse txt format")
def test_qq_parser():
    from qq_parser import parse_qq_txt, analyze_messages

    sample = "2023-12-25 08:30:45 testuser(12345)\nhello world\n\n2023-12-25 08:31:02 me(54321)\nhi\n"
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", encoding="utf-8", delete=False)
    tmp.write(sample)
    tmp.close()

    try:
        msgs = parse_qq_txt(tmp.name)
        assert len(msgs) == 2

        analysis = analyze_messages(msgs, "testuser")
        assert analysis["total_messages"] == 1
    finally:
        os.unlink(tmp.name)


# ── voice_preprocessor tests ────────────────────────────────────────────────

@test("voice_preprocessor: WAV conversion + denoising")
def test_voice_preprocessor():
    import numpy as np
    import soundfile as sf
    from voice_preprocessor import process_directory, get_audio_info

    test_dir = tempfile.mkdtemp()
    out_dir = os.path.join(test_dir, "processed")

    try:
        # Create test WAV files
        for i, dur in enumerate([3, 8], 1):
            sr = 16000
            t = np.linspace(0, dur, sr * dur, dtype=np.float32)
            signal = 0.5 * np.sin(2 * np.pi * 300 * t) + 0.1 * np.random.randn(len(t)).astype(np.float32)
            sf.write(os.path.join(test_dir, f"test_{i}.wav"), signal, sr)

        stats = process_directory(test_dir, out_dir, do_denoise=True)
        assert stats["success"] == 2
        assert stats["duration"] > 10

        # Verify processed files
        for f in os.listdir(out_dir):
            info = get_audio_info(os.path.join(out_dir, f))
            assert info["duration"] > 0
            assert info["sample_rate"] == 16000
    finally:
        shutil.rmtree(test_dir)


# ── interview_guide tests ───────────────────────────────────────────────────

@test("interview_guide: family + self modes")
def test_interview_guide():
    from interview_guide import generate_questions, generate_self_questions, format_guide, format_self_guide

    # Family mode
    qs = generate_questions("TestPerson", "child", birth_year=1940)
    assert len(qs) >= 10

    guide = format_guide("TestPerson", "child", qs)
    assert "TestPerson" in guide

    # Self mode
    modules = generate_self_questions("TestPerson", birth_year=1950)
    assert len(modules) == 5

    self_guide = format_self_guide("TestPerson", modules, "short")
    assert "分次进行" in self_guide


# ── audio_transcriber tests ─────────────────────────────────────────────────

@test("audio_transcriber: format helpers")
def test_audio_transcriber():
    from audio_transcriber import _fmt_duration, _extract_time_from_filename, format_batch_transcript

    assert _fmt_duration(0) == "0:00"
    assert _fmt_duration(65) == "1:05"
    assert _fmt_duration(3661) == "1:01:01"

    assert _extract_time_from_filename("MSG_20231225_143022.m4a") == "2023-12-25 14:30"
    assert _extract_time_from_filename("random.m4a") is None

    # Batch format
    results = [{"filename": "test.wav", "text": "hello", "duration": 2.0, "language": "zh"}]
    report = format_batch_transcript(results, "TestPerson", "chat")
    assert "hello" in report


# ── voice_synthesizer tests ─────────────────────────────────────────────────

@test("voice_synthesizer: model finder helpers")
def test_voice_synthesizer():
    from voice_synthesizer import find_ref_audio, find_ref_text, voice_dir

    # These should not crash even when no data exists
    ref = find_ref_audio("__nonexistent__")
    assert ref is None

    text = find_ref_text("", "__nonexistent__")
    assert text == ""


# ── Run all tests ────────────────────────────────────────────────────────────

def main():
    print("Memorial Skill - Tool Tests\n")

    tests = [
        test_skill_writer,
        test_version_manager,
        test_wechat_parser,
        test_qq_parser,
        test_voice_preprocessor,
        test_interview_guide,
        test_audio_transcriber,
        test_voice_synthesizer,
    ]

    for t in tests:
        t()

    print(f"\nResults: {PASSED} passed, {FAILED} failed, {PASSED + FAILED} total")
    sys.exit(1 if FAILED > 0 else 0)


if __name__ == "__main__":
    main()
