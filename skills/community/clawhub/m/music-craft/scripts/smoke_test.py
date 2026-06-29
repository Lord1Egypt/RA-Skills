#!/usr/bin/env python3
"""Smoke tests for pure helper behavior in the local music-craft skill."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def _print_pass(name: str) -> None:
    print(f"PASS {name}")


def _print_fail(name: str, error: BaseException) -> None:
    print(f"FAIL {name}: {error}")


def test_extract_stems_writes_normalized_output_paths() -> None:
    from extract_stems import planned_stem_paths

    with tempfile.TemporaryDirectory() as tmpdir:
        paths = planned_stem_paths(Path(tmpdir), ["vocals", "drums", "bass", "other"])

    assert set(paths.keys()) == {"vocals", "drums", "bass", "other"}
    assert all(path.name.endswith(".wav") for path in paths.values())


def test_remix_stems_builds_ffmpeg_amix_command() -> None:
    from remix_stems import build_ffmpeg_command

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        stems = {}
        for name in ("vocals", "drums", "bass", "other"):
            path = tmpdir_path / f"{name}.wav"
            path.write_bytes(b"fake")
            stems[name] = path
        output = tmpdir_path / "mix.mp3"
        command = build_ffmpeg_command(stems, output)

    assert command[0] == "ffmpeg"
    assert any("amix=inputs=4:duration=longest:normalize=0" in part for part in command)
    assert str(output) == command[-1]


def test_wait_for_acestep_classifies_empty_query_as_pending() -> None:
    from wait_for_acestep import classify_query_result

    assert classify_query_result({"data": []})["state"] == "pending"
    assert classify_query_result({"data": [{"status": 2}]})["state"] == "succeeded"
    assert classify_query_result({"data": [{"status": 1}]})["state"] == "processing"
    assert classify_query_result({"data": [{"status": 0}]})["state"] == "pending"


def test_wait_for_acestep_detects_new_audio_files() -> None:
    from wait_for_acestep import newest_audio_files

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        (tmpdir_path / "a.mp3").write_bytes(b"a")
        (tmpdir_path / "b.wav").write_bytes(b"b")
        files = newest_audio_files(tmpdir_path, limit=2)

    assert len(files) == 2
    assert all(path.suffix in {".mp3", ".wav"} for path in files)


def test_remix_stems_reads_stems_json() -> None:
    from remix_stems import load_stems_json

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        stems = {}
        for name in ("vocals", "drums", "bass", "other"):
            path = tmpdir_path / f"{name}.wav"
            path.write_bytes(b"fake")
            stems[name] = str(path)
        stems_json = tmpdir_path / "stems.json"
        stems_json.write_text(json.dumps({"stems": stems}), encoding="utf-8")
        loaded = load_stems_json(stems_json)

    assert set(loaded.keys()) == {"vocals", "drums", "bass", "other"}


def test_lint_lyrics_rejects_non_whitelisted_tags_and_reports_duration() -> None:
    from lint_lyrics import lint_lyrics_text

    result = lint_lyrics_text(
        "[Verse]\nCamino por la ciudad\n\n[Lyrics]\nEsto no debe cantarse\n",
        bpm=95,
        target_seconds=180,
    )

    assert result["status"] == "blocked"
    assert "[Lyrics]" in result["invalid_tags"]
    assert result["duration_estimate"]["estimated_lyrics_seconds"] > 0


def test_verify_lyrics_alignment_flags_semantic_mismatch() -> None:
    from verify_lyrics_alignment import compare_lyrics

    result = compare_lyrics(
        "[Verse]\nI walk home under neon rain\n[Chorus]\nStay with me tonight",
        "unrelated transcript with no matching keywords",
        min_overlap=0.45,
    )

    assert result["status"] == "failed"
    assert result["word_overlap"] < 0.45
    assert any("low lyric overlap" in warning for warning in result["warnings"])


def main() -> int:
    tests = [
        ("extract_stems planned paths", test_extract_stems_writes_normalized_output_paths),
        ("remix_stems ffmpeg command", test_remix_stems_builds_ffmpeg_amix_command),
        ("wait_for_acestep status classification", test_wait_for_acestep_classifies_empty_query_as_pending),
        ("wait_for_acestep cache files", test_wait_for_acestep_detects_new_audio_files),
        ("remix_stems reads stems.json", test_remix_stems_reads_stems_json),
        ("lint_lyrics whitelist and duration", test_lint_lyrics_rejects_non_whitelisted_tags_and_reports_duration),
        ("verify_lyrics_alignment mismatch", test_verify_lyrics_alignment_flags_semantic_mismatch),
    ]
    failures = 0
    for name, func in tests:
        try:
            func()
        except Exception as exc:  # noqa: BLE001
            failures += 1
            _print_fail(name, exc)
        else:
            _print_pass(name)
    if failures:
        print(f"{failures} test(s) failed")
        return 1
    print("All smoke tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
