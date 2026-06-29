#!/usr/bin/env python3
"""Smoke tests for music-craft-minimax v1.5.0+. Standard library only.

v1.5.0 removes URL downloads, image pipeline, and LRCLib. Tests for those
features moved to publish/music-source-fetch/scripts/smoke_test.py.

Run: python3 smoke_test.py
"""

from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def _print_pass(name: str) -> None:
    print(f"PASS {name}")


def _print_fail(name: str, error: BaseException) -> None:
    print(f"FAIL {name}: {error}")


def _run_lint_music_request(*args: str) -> dict:
    script_path = SCRIPT_DIR / "lint_music_request.py"
    cmd = [sys.executable, str(script_path), *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"command failed: {result.stderr}"
    assert result.stdout.strip(), "expected JSON output"
    return json.loads(result.stdout)


def test_check_environment_no_longer_lists_yt_dlp_or_image_imports() -> None:
    """v1.5.0: yt-dlp moved to music-source-fetch. Image imports (cv2, PIL) removed."""
    import check_environment

    assert "yt-dlp" not in check_environment.PATH_EXECUTABLES, (
        "yt-dlp should not be a recommended binary anymore "
        "(it moved to music-source-fetch)"
    )
    assert "cv2" not in check_environment.OPTIONAL_IMPORTS, (
        "cv2 (image analysis) was removed with the analyze_image.py deletion"
    )
    assert "PIL" not in check_environment.OPTIONAL_IMPORTS, (
        "PIL (image analysis) was removed with the analyze_image.py deletion"
    )


# ---- Task 7: v1.5.0 orchestrator flag strip ----


def test_orchestrator_parse_song_stem() -> None:
    """Parse 'Artist - Title [noise]' into (artist, title) with noise stripped."""
    import re as _re

    # Replicate the exact logic from the orchestrator's _parse_song_stem
    YT_NOISE = [
        r"\(official\s+(?:music\s+)?video\)",
        r"\(official\s+lyric\s+video\)",
        r"\[lyrics?\]",
        r"\(remastered(?:\s+\d{4})?\)",
        r"\(lyric\s+video\)",
    ]
    YT_RE = _re.compile("|".join(YT_NOISE), _re.IGNORECASE)

    def strip_noise(text):
        return YT_RE.sub("", text).strip(" \t-.")

    def parse(stem):
        if " - " not in stem:
            return ("", "")
        artist, title = stem.split(" - ", 1)
        artist = artist.strip()
        title = strip_noise(title).strip()
        if not artist or not title:
            return ("", "")
        return (artist, title)

    assert parse("Coldplay - Yellow") == ("Coldplay", "Yellow")
    assert parse("Coldplay - Yellow (Official Music Video)") == ("Coldplay", "Yellow")
    assert parse("Coldplay - Yellow [Lyrics]") == ("Coldplay", "Yellow")
    assert parse("Coldplay - Yellow (Lyric Video)") == ("Coldplay", "Yellow")
    assert parse("AC-DC - Back In Black") == ("AC-DC", "Back In Black")
    assert parse("no-separator-here") == ("", "")
    assert parse("") == ("", "")
    assert parse("Artist - ") == ("", "")
    assert parse(" - Title") == ("", "")


def test_cached_or_compute_roundtrip() -> None:
    from _analysis_cache import cached_or_compute

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        audio_path = tmpdir_path / "input audio.wav"
        audio_path.write_bytes(b"dummy audio bytes")

        cache_dir = tmpdir_path / "nested" / "cache" / "dir"
        calls = {"count": 0}
        payload = {
            "title": "café",
            "artist": "東京",
            "notes": {"line": "mañana", "tags": ["über", "façade"]},
        }

        def compute():
            calls["count"] += 1
            return json.loads(json.dumps(payload, ensure_ascii=False))

        first = cached_or_compute(str(audio_path), "unicode_analysis", compute, cache_dir=str(cache_dir))
        assert first["_cache"] == "miss"
        assert calls["count"] == 1
        assert first["title"] == "café"
        assert first["notes"]["line"] == "mañana"

        cache_files = list(cache_dir.glob(".unicode_analysis_*.json"))
        assert len(cache_files) == 1, f"expected one cache file in {cache_dir}, found {len(cache_files)}"
        saved_text = cache_files[0].read_text(encoding="utf-8")
        assert "café" in saved_text and "東京" in saved_text and "mañana" in saved_text
        assert "\\u" not in saved_text, "unicode should be preserved in the cache file"

        second = cached_or_compute(str(audio_path), "unicode_analysis", compute, cache_dir=str(cache_dir))
        assert second["_cache"] == "hit"
        assert calls["count"] == 1, "cache hit should not recompute"
        assert second["title"] == "café"
        assert second["notes"]["tags"] == ["über", "façade"]


def test_build_final_prompt_priorities() -> None:
    from emotion_to_prompt import build_final_prompt

    emotion_data = {
        "emotion_profile": {"intensity_curve": {"pattern": "wave"}},
        "music_generation_hints": [],
        "emotion_sections": [],
    }
    style_data = {
        "estimated_key": "C major",
        "beat_tracking": {
            "bpm_estimated": 142,
            "bpm_confidence": 0.96,
            "time_signature_estimate": 4,
        },
        "melody_analysis": {
            "key_estimate_from_midi": "F# minor",
            "interval_pattern": "rising_fifths",
            "scale_modes": ["dorian", "aeolian"],
        },
        "brightness": "warm bass-heavy",
        "energy_description": "moderate",
    }

    prompt = build_final_prompt(
        emotion_data=emotion_data,
        style_data=style_data,
        style_category="pop",
        target_bpm=120,
        duration_seconds=180,
        language="english",
    )

    assert "beat grid: 4/4 at 142 BPM (confidence 0.96)" in prompt
    assert "melodic key from MIDI: F# minor" in prompt
    assert "tempo 142 BPM in F# minor" in prompt
    assert "tonal character: dark warm tone, rolled-off highs" in prompt
    assert "tempo 120 BPM in C major" not in prompt


def test_lint_music_request_standard_spanish_song() -> None:
    payload = _run_lint_music_request(
        "--text",
        "Write a Spanish pop song about a rainy night.",
    )

    assert payload["route"] == "base_prompt"
    assert payload["request_type"] == "standard_song"
    assert payload["fields"]["language"]["value"] == "Spanish"
    assert payload["fields"]["genre"]["value"] == "pop"
    assert payload["fields"]["theme"]["value"] == "rainy night"
    assert payload["fields"]["lyrics_source"]["value"] == "missing"
    assert "lyrics_source" in payload["missing_fields"]
    assert payload["prompt_warnings"] == []
    assert payload["blockers"] == []
    assert payload["retry_guidance"] == []


def test_lint_music_request_routes_cover_to_minimax_cover() -> None:
    payload = _run_lint_music_request(
        "--text",
        "Make a reggaeton cover from /tmp/song.mp3 with new Spanish lyrics",
    )

    assert payload["route"] == "minimax_cover"
    assert payload["request_type"] == "cover"
    assert payload["blockers"] == []


def test_lint_music_request_routes_style_transfer_to_minimax_style_transfer() -> None:
    payload = _run_lint_music_request(
        "--text",
        "Do a style transfer of /tmp/original.wav into reggaeton with original melody-free production.",
    )

    assert payload["route"] == "minimax_style_transfer"
    assert payload["request_type"] == "style_transfer"
    assert "missing target style" not in payload["blockers"]


def test_lint_music_request_instrumental_jingle_skips_vocal_question() -> None:
    payload = _run_lint_music_request(
        "--text",
        "Create a 30-second instrumental jingle for a cooking channel, no vocals.",
    )

    assert payload["route"] == "base_prompt"
    assert payload["request_type"] == "instrumental"
    assert payload["fields"]["vocal_mode"]["value"] == "instrumental"
    assert payload["fields"]["vocal_mode"]["confidence"] == "clear"
    assert payload["fields"]["duration"]["value"] == "30 seconds"
    assert "vocal_mode" not in payload["missing_fields"]


def test_lint_music_request_plain_style_reference_needs_clarification() -> None:
    payload = _run_lint_music_request(
        "--text",
        "Make a song like Daft Punk.",
    )

    assert payload["route"] == "needs_clarification"
    assert payload["request_type"] == "text_reference"
    assert payload["fields"]["references"]["value"] == "style reference"
    assert "missing target style or mood for the new song" in payload["blockers"]


def test_lint_music_request_text_style_reference_with_clear_target() -> None:
    payload = _run_lint_music_request(
        "--text",
        "Make a synthwave song in the style of Daft Punk.",
    )

    assert payload["route"] == "base_prompt"
    assert payload["request_type"] == "text_reference"
    assert payload["fields"]["genre"]["value"] == "synthwave"


def test_lint_music_request_url_returns_url_not_accepted_warning() -> None:
    """v1.5.0: a YouTube URL must trigger a soft ``url_not_accepted`` warning, not a cover route.

    The published minimax skill refuses URLs outright and asks the user for a
    local file path. The linter reflects that contract: detecting a URL in a
    cover request emits a ``url_not_accepted`` warning (a list of dicts under
    ``payload['warnings']``) and the route is forced to
    ``needs_clarification`` so the agent can ask the user for a local file.
    """
    payload = _run_lint_music_request(
        "--text",
        "Make a reggaeton cover from https://youtube.com/watch?v=abc123",
    )

    warnings = payload.get("warnings", [])
    assert any(
        isinstance(w, dict) and w.get("code") == "url_not_accepted"
        for w in warnings
    ), f"expected url_not_accepted warning, got warnings: {warnings!r}"
    message = " ".join(
        str(w.get("message", "")) for w in warnings if isinstance(w, dict)
    )
    assert "URL" in message or "local file" in message, (
        f"warning message should mention URL or local file, got: {message!r}"
    )
    assert payload["route"] == "needs_clarification", (
        f"URLs must route to needs_clarification so the agent asks for a "
        f"local file; got route={payload['route']!r}"
    )
    assert payload["route"] != "minimax_cover", (
        f"URLs must not auto-route to cover anymore; got route={payload['route']!r}"
    )


def test_lint_music_request_jiosaavn_url_returns_url_not_accepted_warning() -> None:
    """v1.5.0: a JioSaavn URL gets the same soft warning and needs_clarification route.

    Mirrors the YouTube case: even though the v1.4.0 linter treated JioSaavn
    URLs as usable audio sources, the v1.5.0 linter refuses all URLs and asks
    for a local file. This regression-guards the new contract for the most
    likely production source after YouTube.
    """
    payload = _run_lint_music_request(
        "--text",
        "Make a reggaeton cover from https://www.jiosaavn.com/song/x/AbC123",
    )

    warnings = payload.get("warnings", [])
    assert any(
        isinstance(w, dict) and w.get("code") == "url_not_accepted"
        for w in warnings
    ), f"expected url_not_accepted warning, got warnings: {warnings!r}"
    assert payload["route"] == "needs_clarification", (
        f"JioSaavn URL must route to needs_clarification; got route={payload['route']!r}"
    )
    assert payload["route"] != "minimax_cover", (
        f"JioSaavn URL must not auto-route to cover; got route={payload['route']!r}"
    )


def test_lint_music_request_local_file_still_routes_to_cover() -> None:
    """Sanity: a local audio file in a cover request still routes to ``minimax_cover``.

    The v1.5.0 contract strips URL handling but must keep local-file routing
    intact. This test guards the happy path so the URL-strip refactor does
    not regress the most common use case (user supplies ``/tmp/song.mp3``).
    """
    payload = _run_lint_music_request(
        "--text",
        "Make a reggaeton cover from /tmp/song.mp3 with new Spanish lyrics",
    )

    warnings = payload.get("warnings", [])
    assert not any(
        isinstance(w, dict) and w.get("code") == "url_not_accepted"
        for w in warnings
    ), f"local file must not produce a url_not_accepted warning; got: {warnings!r}"
    assert payload["route"] == "minimax_cover", (
        f"local audio should still route to cover; got {payload['route']!r}"
    )
    assert payload["request_type"] == "cover"


def test_lint_music_request_mashup_routes_to_minimax_mashup_when_complete() -> None:
    payload = _run_lint_music_request(
        "--text",
        "Mash up Song A at /tmp/song_a.mp3 and Song B at /tmp/song_b.mp3 into a pop track.",
    )

    assert payload["route"] == "minimax_mashup"
    assert payload["request_type"] == "mashup"
    assert payload["blockers"] == []


def test_lint_music_request_emotion_prompt_routes_to_minimax_emotion_prompt() -> None:
    payload = _run_lint_music_request(
        "--text",
        "Run emotion analysis on /tmp/song.wav and turn it into a sad pop prompt.",
    )

    assert payload["route"] == "minimax_emotion_prompt"
    assert payload["request_type"] == "emotion_prompt"


def test_lint_music_request_mashup_blocker_for_missing_song_b() -> None:
    payload = _run_lint_music_request(
        "--text",
        "Make a mashup with only Song A in pop style.",
    )

    assert payload["route"] == "needs_clarification"
    assert payload["request_type"] == "mashup"
    assert "unclear Song A vs Song B assignment" in payload["blockers"]


def test_lint_music_request_blocker_for_missing_lyrics_decision() -> None:
    payload = _run_lint_music_request(
        "--text",
        "Cover a track into reggaeton.",
    )

    assert payload["route"] == "needs_clarification"
    assert payload["request_type"] == "cover"
    assert "missing lyrics decision" in payload["blockers"]


def test_lint_music_request_blocker_for_conflicting_cover_style_transfer() -> None:
    payload = _run_lint_music_request(
        "--text",
        "Make a cover and style transfer of this YouTube song into pop.",
    )

    assert payload["route"] == "needs_clarification"
    assert payload["request_type"] == "cover"
    assert any("conflicting cover/style-transfer" in blocker for blocker in payload["blockers"])


def test_lint_music_request_cinematic_with_instruments_is_not_placeholder() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        prompt_file = Path(tmpdir) / "prompt.txt"
        prompt_file.write_text(
            "Cinematic instrumental, strings, piano, drums, soft verse building to loud chorus. "
            "ALL instruments always playing throughout, never go a cappella.",
            encoding="utf-8",
        )

        payload = _run_lint_music_request("--prompt-file", str(prompt_file))

    assert not any("vague placeholder" in warning for warning in payload["prompt_warnings"])


def test_lint_music_request_prompt_warnings_and_flag_conflicts() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        prompt_file = tmpdir_path / "prompt.txt"
        prompt_file.write_text(
            "Make it good and emotional. 80 BPM in C major. Use strings. Verse-chorus-bridge-chorus. Avoid sparse arrangements.",
            encoding="utf-8",
        )
        flags_file = tmpdir_path / "flags.json"
        flags_file.write_text(
            json.dumps(
                {
                    "bpm": 120,
                    "key": "D minor",
                    "structure": "verse-chorus-verse",
                    "avoid": "sparse, a cappella, minimal arrangement",
                }
            ),
            encoding="utf-8",
        )

        payload = _run_lint_music_request("--prompt-file", str(prompt_file), "--mmx-flags", str(flags_file))

    warnings = payload["prompt_warnings"]
    conflicts = payload["flag_conflicts"]
    guidance = payload["retry_guidance"]

    assert any("explicit instruments" in warning for warning in warnings)
    assert any("anti-sparse" in warning for warning in warnings)
    assert any("vague placeholder" in warning for warning in warnings)
    assert any("bpm" in conflict.lower() for conflict in conflicts)
    assert any("key" in conflict.lower() for conflict in conflicts)
    assert any("structure" in conflict.lower() for conflict in conflicts)
    assert any("avoid" in conflict.lower() for conflict in conflicts)
    assert len(guidance) == len(conflicts)
    assert any("bpm" in line.lower() for line in guidance)


def test_lint_music_request_key_conflict() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        prompt_file = tmpdir_path / "prompt.txt"
        prompt_file.write_text("Pop track at 120 BPM in E minor.", encoding="utf-8")
        flags_file = tmpdir_path / "flags.json"
        flags_file.write_text(json.dumps({"bpm": 120, "key": "C major"}), encoding="utf-8")

        payload = _run_lint_music_request("--prompt-file", str(prompt_file), "--mmx-flags", str(flags_file))

    assert any("key conflict" in conflict for conflict in payload["flag_conflicts"])
    assert any("key" in line.lower() for line in payload["retry_guidance"])


def test_lint_music_request_duration_conflict() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        prompt_file = tmpdir_path / "prompt.txt"
        prompt_file.write_text("Make a 30 second pop track at 120 BPM.", encoding="utf-8")
        flags_file = tmpdir_path / "flags.json"
        flags_file.write_text(json.dumps({"bpm": 120, "duration": "90 seconds"}), encoding="utf-8")

        payload = _run_lint_music_request("--prompt-file", str(prompt_file), "--mmx-flags", str(flags_file))

    assert any("duration conflict" in conflict for conflict in payload["flag_conflicts"])
    assert any("duration" in line.lower() for line in payload["retry_guidance"])


def test_lint_music_request_vocal_mode_conflict() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        prompt_file = tmpdir_path / "prompt.txt"
        prompt_file.write_text("Make an instrumental pop track at 120 BPM.", encoding="utf-8")
        flags_file = tmpdir_path / "flags.json"
        flags_file.write_text(json.dumps({"bpm": 120, "vocals": "female vocal"}), encoding="utf-8")

        payload = _run_lint_music_request("--prompt-file", str(prompt_file), "--mmx-flags", str(flags_file))

    assert any("vocal mode conflict" in conflict for conflict in payload["flag_conflicts"])
    assert any("vocal" in line.lower() for line in payload["retry_guidance"])


def test_lint_music_request_language_conflict() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        prompt_file = tmpdir_path / "prompt.txt"
        prompt_file.write_text("Write a Spanish pop song at 120 BPM.", encoding="utf-8")
        flags_file = tmpdir_path / "flags.json"
        flags_file.write_text(json.dumps({"bpm": 120, "language": "French"}), encoding="utf-8")

        payload = _run_lint_music_request("--prompt-file", str(prompt_file), "--mmx-flags", str(flags_file))

    assert any("language conflict" in conflict for conflict in payload["flag_conflicts"])
    assert any("language" in line.lower() for line in payload["retry_guidance"])


def test_lint_music_request_warns_and_blocks_on_prompt_byte_length() -> None:
    """MiniMax rejects long prompts late; lint must catch byte length first."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        warning_prompt = tmpdir_path / "warning_prompt.txt"
        warning_prompt.write_text("a" * 1850, encoding="utf-8")
        warning_payload = _run_lint_music_request("--prompt-file", str(warning_prompt))

        error_prompt = tmpdir_path / "error_prompt.txt"
        error_prompt.write_text("é" * 1001, encoding="utf-8")  # 2002 UTF-8 bytes
        error_payload = _run_lint_music_request("--prompt-file", str(error_prompt))

    assert any("prompt length" in warning.lower() for warning in warning_payload["prompt_warnings"])
    assert warning_payload["route"] != "needs_clarification"
    assert any("prompt length" in blocker.lower() for blocker in error_payload["blockers"])
    assert error_payload["route"] == "needs_clarification"


def test_lint_music_request_warns_on_long_lyric_heavy_generation() -> None:
    """MiniMax lyric-heavy generations often return 120-150s instead of the requested 180s+.

    When the prompt implies dense lyrics AND requests >150 seconds, the linter must
    emit a warning advising that exact full-length is better handled by music-craft
    with ACE-Step.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        prompt_file = Path(tmpdir) / "prompt.txt"
        prompt_file.write_text(
            "English vocal song, 180 seconds, with full lyrics and dense verses. "
            "Male lead vocal throughout.",
            encoding="utf-8",
        )

        payload = _run_lint_music_request("--prompt-file", str(prompt_file))

    assert any(
        "shorter than requested" in warning or "120-150" in warning
        for warning in payload["prompt_warnings"]
    ), f"expected lyric-truncation warning in {payload['prompt_warnings']!r}"


def test_lint_music_request_blocks_invalid_lyrics_tags_and_estimates_duration() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        prompt_file = tmpdir_path / "prompt.txt"
        lyrics_file = tmpdir_path / "lyrics.txt"
        flags_file = tmpdir_path / "flags.json"
        prompt_file.write_text(
            "Spanish vocal pop song, 90 BPM, 180 seconds, piano and drums, never go a cappella.",
            encoding="utf-8",
        )
        lyrics_file.write_text(
            "[Verse]\n"
            "Cada noche vuelvo a caminar por las avenidas de tu voz\n"
            "y cada esquina guarda lo que nunca dije yo\n\n"
            "[Guitar Solo - distorted]\n"
            "la la la\n",
            encoding="utf-8",
        )
        flags_file.write_text(json.dumps({"bpm": 90}), encoding="utf-8")

        payload = _run_lint_music_request(
            "--prompt-file", str(prompt_file),
            "--lyrics-file", str(lyrics_file),
            "--mmx-flags", str(flags_file),
        )

    assert payload["route"] == "needs_clarification"
    assert payload["fields"]["lyrics_source"]["value"] == "lyrics_file"
    assert any("invalid lyrics tags" in blocker for blocker in payload["blockers"])
    assert payload["lyrics_warnings"], "expected invalid tag warning"
    assert payload["duration_estimate"]["bpm"] == 90
    assert payload["duration_estimate"]["estimated_lyrics_seconds"] > 0


def test_lint_music_request_plain_lyrics_word_stays_standard_song() -> None:
    payload = _run_lint_music_request(
        "--text",
        "Make a 3 minute Spanish pop song with emotional lyrics about moving on.",
    )

    assert payload["route"] == "base_prompt"
    assert payload["request_type"] == "standard_song"
    assert payload["fields"]["lyrics_source"]["value"] == "missing"
    assert "lyrics_source" in payload["missing_fields"]


def test_lint_lyrics_rejects_non_whitelisted_tags_and_reports_duration() -> None:
    from lint_lyrics import lint_lyrics_text

    result = lint_lyrics_text(
        "[Verse]\nCamino por la ciudad\n\n[Section 1]\nEsto no debe cantarse\n",
        bpm=95,
        target_seconds=180,
    )

    assert result["status"] == "blocked"
    assert "[Section 1]" in result["invalid_tags"]
    assert result["duration_estimate"]["estimated_lyrics_seconds"] > 0


def test_verify_lyrics_alignment_flags_semantic_mismatch() -> None:
    from verify_lyrics_alignment import compare_lyrics

    result = compare_lyrics(
        "[Verse]\nI walk home under neon rain\n[Chorus]\nStay with me tonight",
        "verse chorus generated tags in a different language ohne klare uebereinstimmung",
        min_overlap=0.45,
    )

    assert result["status"] == "failed"
    assert result["word_overlap"] < 0.45
    assert any("low lyric overlap" in warning for warning in result["warnings"])


def test_finalize_track_refuses_overwrite_without_flag() -> None:
    script_path = SCRIPT_DIR / "finalize_track.sh"
    text = script_path.read_text(encoding="utf-8")

    assert "--overwrite" in text
    assert "Refusing to overwrite" in text


def test_extract_lyrics_whisper_default_model_and_section_normalization() -> None:
    import extract_lyrics_whisper

    segments = [{"text": f"unique lyric phrase number {idx}"} for idx in range(12)]
    tags = extract_lyrics_whisper.detect_repeated_sections(segments)

    assert extract_lyrics_whisper.DEFAULT_WHISPER_MODEL == "medium"
    assert len(tags) == len(segments)
    assert not any(tag.startswith("Section ") for tag in tags)
    assert tags.count("Verse 3") <= 1


def test_extract_lyrics_whisper_sanity_flags_language_and_looping() -> None:
    from extract_lyrics_whisper import lyrics_sanity_warnings

    warnings = lyrics_sanity_warnings(
        transcript="Ich habe mich interessiert wegen des Traummeters. " * 4,
        detected_language="de",
        expected_language="en",
        segments=[
            {"text": "Ich habe mich interessiert wegen des Traummeters"},
            {"text": "Ich habe mich interessiert wegen des Traummeters"},
            {"text": "Ich habe mich interessiert wegen des Traummeters"},
        ],
    )

    assert any("language mismatch" in warning.lower() for warning in warnings)
    assert any("loop" in warning.lower() for warning in warnings)


def test_generate_with_retry_moves_saved_file_to_requested_output_path() -> None:
    """When --output-path is provided, the wrapper moves the generated file there after success.

    The wrapper runs mmx in an isolated temp directory, captures the saved-filename
    from stdout JSON (e.g. {"saved": "music_2026-06-11-14-35-32.mp3"}), and moves the
    generated file to the requested output path so caller-specified names are respected.
    """
    import generate_with_retry as _gwr
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        output_path = tmpdir_path / "M1_song.mp3"

        # The run_with_retry function creates its own internal temp dir (run_dir).
        # We intercept subprocess.run and create the file in the same cwd that
        # run_with_retry passes to the subprocess, so the move can find it.
        def fake_run(cmd, *args, cwd=None, **kwargs):
            # Create the generated file inside the run_dir (cwd) that run_with_retry set up
            if cwd:
                generated_file = Path(cwd) / "music_2026-06-11-14-35-32.mp3"
                generated_file.write_bytes(b"fake audio content")
            result = _mock.Mock()
            result.returncode = 0
            result.stdout = '{"saved": "music_2026-06-11-14-35-32.mp3"}'
            result.stderr = ""
            return result

        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("generate_with_retry._is_probeable_audio", return_value=True):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=1,
                retry_delay=0.1,
                output_path=str(output_path),
            )

        assert ret == 0, f"expected success, got {ret}"
        assert output_path.exists(), f"output file not found at {output_path}"
        assert output_path.read_bytes() == b"fake audio content"


def test_generate_with_retry_warns_when_output_is_shorter_than_expected() -> None:
    """When --expected-duration-seconds is provided, the wrapper warns if output is materially shorter.

    The check is best-effort: ffprobe is used only if available on the system.
    If ffprobe is absent or fails, the warning is skipped silently (no hard dependency).
    This test asserts that the warning is actually emitted to stderr.
    """
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        output_path = tmpdir_path / "song.mp3"

        call_log: list = []

        def fake_run(cmd, *args, cwd=None, **kwargs):
            call_log.append(cmd[0] if cmd else "")
            if cwd:
                generated_file = Path(cwd) / "song.mp3"
                generated_file.write_bytes(b"fake audio content")
            result = _mock.Mock()
            result.returncode = 0
            result.stdout = '{"saved": "song.mp3"}'
            result.stderr = ""
            return result

        def fake_ffprobe(cmd, *args, **kwargs):
            call_log.append(cmd[0] if cmd else "")
            result = _mock.Mock()
            result.returncode = 0
            # Simulate ffprobe reporting 90s duration (materially shorter than 180s expected)
            result.stdout = "90.0\n"
            result.stderr = ""
            return result

        def tracking_run(cmd, *args, **kwargs):
            if cmd and "ffprobe" in str(cmd[0]):
                return fake_ffprobe(cmd, *args, **kwargs)
            return fake_run(cmd, *args, **kwargs)

        stderr_buffer = io.StringIO()
        with _mock.patch("subprocess.run", side_effect=tracking_run), \
             _mock.patch("generate_with_retry.shutil.which", return_value="/usr/bin/ffprobe"), \
             _mock.patch("sys.stderr", stderr_buffer):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=1,
                retry_delay=0.1,
                output_path=str(output_path),
                expected_duration_seconds=180,
            )

        assert ret == 0, f"expected success, got {ret}"
        assert output_path.exists(), "output file should exist after move"
        # ffprobe must have been called (shutil.which returned a path)
        assert any("ffprobe" in c for c in call_log), f"ffprobe should have been called, got {call_log}"
        # The warning must actually be emitted to stderr
        stderr_content = stderr_buffer.getvalue()
        assert "materially shorter" in stderr_content or "WARNING" in stderr_content, (
            f"expected duration-warning in stderr, got: {stderr_content!r}"
        )


def test_generate_with_retry_warns_on_long_cloud_prompt() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    long_prompt = "wide cinematic indie rock " * 30
    stderr_buffer = io.StringIO()
    with _mock.patch("sys.stderr", stderr_buffer):
        _gwr._warn_prompt_budget(["music", "generate", "--prompt", long_prompt])

    assert "prompt is" in stderr_buffer.getvalue()
    assert "500 characters" in stderr_buffer.getvalue()


def test_generate_with_retry_requires_out_when_output_path_is_requested() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "song.mp3"
        stderr_buffer = io.StringIO()
        with _mock.patch("subprocess.run") as run_mock, _mock.patch("sys.stderr", stderr_buffer):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello"],
                attempts=1,
                retry_delay=0.1,
                output_path=str(output_path),
            )

    assert ret != 0
    assert not run_mock.called
    assert "--out" in stderr_buffer.getvalue()
    assert "--output-path" in stderr_buffer.getvalue()


def test_generate_with_retry_resolves_equals_form_relative_paths() -> None:
    import generate_with_retry as _gwr

    base = Path("/tmp/music-wrapper-cwd")
    args = _gwr._resolve_relative_paths(
        [
            "music",
            "generate",
            "--out=track.mp3",
            "--audio-file=source.wav",
            "--lyrics-file=lyrics.txt",
            "--prompt=hello",
        ],
        base,
    )

    assert f"--out={base / 'track.mp3'}" in args
    assert f"--audio-file={base / 'source.wav'}" in args
    assert f"--lyrics-file={base / 'lyrics.txt'}" in args
    assert "--prompt=hello" in args


def test_generate_with_retry_probe_falls_back_to_mp3_header_without_ffprobe() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        mp3_path = Path(tmpdir) / "song.mp3"
        tiny_mp3_path = Path(tmpdir) / "tiny.mp3"
        bad_path = Path(tmpdir) / "bad.mp3"
        mp3_path.write_bytes(b"ID3\x04" + (b"0" * _gwr.MP3_FALLBACK_MIN_BYTES))
        tiny_mp3_path.write_bytes(b"ID3\x04fake mp3 payload")
        bad_path.write_bytes(b"not mp3")

        stderr_buffer = io.StringIO()
        with _mock.patch("generate_with_retry.shutil.which", return_value=None), \
             _mock.patch("sys.stderr", stderr_buffer):
            assert _gwr._is_probeable_audio(mp3_path) is True
            assert _gwr._is_probeable_audio(tiny_mp3_path) is False
            assert _gwr._is_probeable_audio(bad_path) is False

        assert "MP3 header" in stderr_buffer.getvalue()
        assert "minimum" in stderr_buffer.getvalue()


def test_generate_with_retry_probe_reads_header_only() -> None:
    source = (SCRIPT_DIR / "generate_with_retry.py").read_text(encoding="utf-8")
    probe_source = source.split("def _is_probeable_audio", 1)[1].split("\ndef ", 1)[0]

    assert ".read_bytes()" not in probe_source
    assert "handle.read(MP3_MIN_HEADER_BYTES)" in probe_source


def test_generate_with_retry_accepts_saved_file_after_signal_exit() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "M3_song.mp3"

        def fake_run(cmd, *args, cwd=None, **kwargs):
            output_path.write_bytes(b"fake cloud mp3 content")
            result = _mock.Mock()
            result.returncode = 143
            result.stdout = ""
            result.stderr = "Terminated: 15\n"
            return result

        stderr_buffer = io.StringIO()
        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("generate_with_retry._is_probeable_audio", return_value=True), \
             _mock.patch("sys.stderr", stderr_buffer):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=1,
                retry_delay=0.1,
            )

        assert ret == 0, f"expected saved file after signal to be accepted, got {ret}"
        assert output_path.exists()
        assert "accepting saved file" in stderr_buffer.getvalue()


def test_generate_with_retry_moves_signal_out_file_to_output_path() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        mmx_out = tmpdir_path / "mmx_out.mp3"
        output_path = tmpdir_path / "requested_name.mp3"

        def fake_run(cmd, *args, cwd=None, **kwargs):
            mmx_out.write_bytes(b"fresh cloud mp3 content")
            result = _mock.Mock()
            result.returncode = 143
            result.stdout = ""
            result.stderr = "Terminated: 15\n"
            return result

        stderr_buffer = io.StringIO()
        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("generate_with_retry._is_probeable_audio", return_value=True), \
             _mock.patch("sys.stderr", stderr_buffer):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(mmx_out)],
                attempts=1,
                retry_delay=0.1,
                output_path=str(output_path),
            )

        assert ret == 0, f"expected --out file to be moved to output_path, got {ret}"
        assert output_path.read_bytes() == b"fresh cloud mp3 content"
        assert not mmx_out.exists(), "--out file should have been moved to output_path"


def test_generate_with_retry_rejects_stale_file_after_signal_exit() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "M3_song.mp3"
        output_path.write_bytes(b"old mp3 content")

        def fake_run(cmd, *args, cwd=None, **kwargs):
            result = _mock.Mock()
            result.returncode = 143
            result.stdout = ""
            result.stderr = "Terminated: 15\n"
            return result

        stderr_buffer = io.StringIO()
        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("generate_with_retry._is_probeable_audio", return_value=True), \
             _mock.patch("sys.stderr", stderr_buffer):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=1,
                retry_delay=0.1,
            )

        assert ret == 143, f"expected stale file not to be accepted, got {ret}"
        assert "accepting saved file" not in stderr_buffer.getvalue()


def test_generate_with_retry_rejects_overwritten_file_without_overwrite_flag() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "M3_song.mp3"
        output_path.write_bytes(b"old mp3 content")

        def fake_run(cmd, *args, cwd=None, **kwargs):
            output_path.write_bytes(b"new mp3 content")
            result = _mock.Mock()
            result.returncode = 143
            result.stdout = ""
            result.stderr = "Terminated: 15\n"
            return result

        stderr_buffer = io.StringIO()
        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("generate_with_retry._is_probeable_audio", return_value=True), \
             _mock.patch("sys.stderr", stderr_buffer):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=1,
                retry_delay=0.1,
            )

        assert ret == 143, f"expected overwritten file not to be accepted, got {ret}"
        assert "without --overwrite" in stderr_buffer.getvalue()


def test_generate_with_retry_recovers_internal_file_after_signal_exit() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "M3_song.mp3"

        def fake_run(cmd, *args, cwd=None, **kwargs):
            if cwd:
                (Path(cwd) / "music_internal_saved.mp3").write_bytes(b"fresh internal mp3")
            result = _mock.Mock()
            result.returncode = 143
            result.stdout = ""
            result.stderr = "Terminated: 15\n"
            return result

        stderr_buffer = io.StringIO()
        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("generate_with_retry._is_probeable_audio", return_value=True), \
             _mock.patch("sys.stderr", stderr_buffer):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=1,
                retry_delay=0.1,
                output_path=str(output_path),
            )

        assert ret == 0, f"expected internal saved file to be recovered, got {ret}"
        assert output_path.read_bytes() == b"fresh internal mp3"
        assert "recovered from the run directory" in stderr_buffer.getvalue()


def test_generate_with_retry_recovers_internal_signal_output_without_explicit_destination() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    old_cwd = Path.cwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        def fake_run(cmd, *args, cwd=None, **kwargs):
            if cwd:
                (Path(cwd) / "music_internal_saved.mp3").write_bytes(b"fresh internal mp3")
            result = _mock.Mock()
            result.returncode = 143
            result.stdout = ""
            result.stderr = "Terminated: 15\n"
            return result

        stderr_buffer = io.StringIO()
        try:
            os.chdir(tmpdir_path)
            with _mock.patch("subprocess.run", side_effect=fake_run), \
                 _mock.patch("generate_with_retry._is_probeable_audio", return_value=True), \
                 _mock.patch("sys.stderr", stderr_buffer):
                ret = _gwr.run_with_retry(
                    "fake_mmx",
                    ["music", "generate", "--prompt", "hello"],
                    attempts=1,
                    retry_delay=0.1,
                )
        finally:
            os.chdir(old_cwd)

        recovered_path = tmpdir_path / "music_internal_saved.mp3"
        assert ret == 0, f"expected internal signal output to be recovered, got {ret}"
        assert recovered_path.read_bytes() == b"fresh internal mp3"
        assert "recovered from the run directory" in stderr_buffer.getvalue()


def test_generate_with_retry_moves_success_output_without_explicit_destination() -> None:
    import generate_with_retry as _gwr
    import unittest.mock as _mock

    old_cwd = Path.cwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        def fake_run(cmd, *args, cwd=None, **kwargs):
            if cwd:
                (Path(cwd) / "music_saved.mp3").write_bytes(b"fresh success mp3")
            result = _mock.Mock()
            result.returncode = 0
            result.stdout = '{"saved": "music_saved.mp3"}'
            result.stderr = ""
            return result

        try:
            os.chdir(tmpdir_path)
            with _mock.patch("subprocess.run", side_effect=fake_run), \
                 _mock.patch("generate_with_retry._is_probeable_audio", return_value=True):
                ret = _gwr.run_with_retry(
                    "fake_mmx",
                    ["music", "generate", "--prompt", "hello"],
                    attempts=1,
                    retry_delay=0.1,
                )
        finally:
            os.chdir(old_cwd)

        moved_path = tmpdir_path / "music_saved.mp3"
        assert ret == 0, f"expected success output to be moved out of tempdir, got {ret}"
        assert moved_path.read_bytes() == b"fresh success mp3"


def test_generate_with_retry_warns_on_unprobeable_fresh_success_output() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "final.mp3"

        def fake_run(cmd, *args, cwd=None, **kwargs):
            if cwd:
                (Path(cwd) / "music_saved.mp3").write_bytes(b"truncated success mp3")
            result = _mock.Mock()
            result.returncode = 0
            result.stdout = '{"saved": "music_saved.mp3"}'
            result.stderr = ""
            return result

        stderr_buffer = io.StringIO()
        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("generate_with_retry._is_probeable_audio", return_value=False), \
             _mock.patch("sys.stderr", stderr_buffer):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=1,
                retry_delay=0.1,
                output_path=str(output_path),
            )

        assert ret == 0, f"expected clean mmx success to be preserved with warning, got {ret}"
        assert output_path.read_bytes() == b"truncated success mp3"
        assert "could not be validated" in stderr_buffer.getvalue()


def test_generate_with_retry_rejects_success_output_from_previous_attempt() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    old_cwd = Path.cwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        output_path = tmpdir_path / "final.mp3"
        call_count = {"value": 0}

        def fake_run(cmd, *args, cwd=None, **kwargs):
            call_count["value"] += 1
            if cwd and call_count["value"] == 1:
                (Path(cwd) / "music_saved.mp3").write_bytes(b"first attempt mp3")
            result = _mock.Mock()
            if call_count["value"] == 1:
                result.returncode = 6
                result.stdout = ""
                result.stderr = "code 6, Network request failed\n"
            else:
                result.returncode = 0
                result.stdout = '{"saved": "music_saved.mp3"}'
                result.stderr = ""
            return result

        stderr_buffer = io.StringIO()
        try:
            os.chdir(tmpdir_path)
            with _mock.patch("subprocess.run", side_effect=fake_run), \
                 _mock.patch("generate_with_retry._is_probeable_audio", return_value=True), \
                 _mock.patch("time.sleep", lambda _seconds: None), \
                 _mock.patch("sys.stderr", stderr_buffer):
                ret = _gwr.run_with_retry(
                    "fake_mmx",
                    ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                    attempts=2,
                    retry_delay=0.1,
                    output_path=str(output_path),
                )
        finally:
            os.chdir(old_cwd)

        assert ret == 1, f"expected stale saved file from previous attempt to fail, got {ret}"
        assert not output_path.exists()
        assert "no generated output file" in stderr_buffer.getvalue()


def test_generate_with_retry_rejects_unprobeable_success_output_from_previous_attempt() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    old_cwd = Path.cwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        output_path = tmpdir_path / "final.mp3"
        call_count = {"value": 0}

        def fake_run(cmd, *args, cwd=None, **kwargs):
            call_count["value"] += 1
            if cwd and call_count["value"] == 1:
                (Path(cwd) / "music_saved.mp3").write_bytes(b"truncated mp3")
            result = _mock.Mock()
            if call_count["value"] == 1:
                result.returncode = 6
                result.stdout = ""
                result.stderr = "code 6, Network request failed\n"
            else:
                result.returncode = 0
                result.stdout = '{"saved": "music_saved.mp3"}'
                result.stderr = ""
            return result

        stderr_buffer = io.StringIO()
        try:
            os.chdir(tmpdir_path)
            with _mock.patch("subprocess.run", side_effect=fake_run), \
                 _mock.patch("generate_with_retry._is_probeable_audio", return_value=False), \
                 _mock.patch("time.sleep", lambda _seconds: None), \
                 _mock.patch("sys.stderr", stderr_buffer):
                ret = _gwr.run_with_retry(
                    "fake_mmx",
                    ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                    attempts=2,
                    retry_delay=0.1,
                    output_path=str(output_path),
                )
        finally:
            os.chdir(old_cwd)

        assert ret == 1, f"expected unprobeable stale success output to fail, got {ret}"
        assert not output_path.exists()
        assert "no generated output file" in stderr_buffer.getvalue()


def test_generate_with_retry_prefers_fresh_out_over_stale_saved_name() -> None:
    import generate_with_retry as _gwr
    import unittest.mock as _mock

    old_cwd = Path.cwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        mmx_out = tmpdir_path / "mmx_out.mp3"
        output_path = tmpdir_path / "final.mp3"
        call_count = {"value": 0}

        def fake_run(cmd, *args, cwd=None, **kwargs):
            call_count["value"] += 1
            if cwd and call_count["value"] == 1:
                (Path(cwd) / "music_saved.mp3").write_bytes(b"stale first attempt mp3")
            if call_count["value"] == 2:
                mmx_out.write_bytes(b"fresh second attempt mp3")
            result = _mock.Mock()
            if call_count["value"] == 1:
                result.returncode = 6
                result.stdout = ""
                result.stderr = "code 6, Network request failed\n"
            else:
                result.returncode = 0
                result.stdout = '{"saved": "music_saved.mp3"}'
                result.stderr = ""
            return result

        try:
            os.chdir(tmpdir_path)
            with _mock.patch("subprocess.run", side_effect=fake_run), \
                 _mock.patch("generate_with_retry._is_probeable_audio", return_value=True), \
                 _mock.patch("time.sleep", lambda _seconds: None):
                ret = _gwr.run_with_retry(
                    "fake_mmx",
                    ["music", "generate", "--prompt", "hello", "--out", str(mmx_out)],
                    attempts=2,
                    retry_delay=0.1,
                    output_path=str(output_path),
                )
        finally:
            os.chdir(old_cwd)

        assert ret == 0, f"expected fresh --out artifact to be preserved, got {ret}"
        assert output_path.read_bytes() == b"fresh second attempt mp3"
        assert not mmx_out.exists()


def test_generate_with_retry_moves_success_out_file_to_output_path() -> None:
    import generate_with_retry as _gwr
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        mmx_out = tmpdir_path / "mmx_out.mp3"
        output_path = tmpdir_path / "requested_name.mp3"

        def fake_run(cmd, *args, cwd=None, **kwargs):
            mmx_out.write_bytes(b"fresh external mp3")
            result = _mock.Mock()
            result.returncode = 0
            result.stdout = ""
            result.stderr = ""
            return result

        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("generate_with_retry._is_probeable_audio", return_value=True):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(mmx_out)],
                attempts=1,
                retry_delay=0.1,
                output_path=str(output_path),
            )

        assert ret == 0, f"expected --out artifact to move to output_path, got {ret}"
        assert output_path.read_bytes() == b"fresh external mp3"
        assert not mmx_out.exists(), "--out artifact should have been moved"


def test_generate_with_retry_accepts_successful_in_place_out_overwrite() -> None:
    import generate_with_retry as _gwr
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "stable.mp3"
        output_path.write_bytes(b"old mp3")

        def fake_run(cmd, *args, cwd=None, **kwargs):
            output_path.write_bytes(b"new mp3")
            result = _mock.Mock()
            result.returncode = 0
            result.stdout = ""
            result.stderr = ""
            return result

        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("generate_with_retry._is_probeable_audio", return_value=True):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=1,
                retry_delay=0.1,
            )

        assert ret == 0, f"expected successful in-place --out overwrite to stay success, got {ret}"
        assert output_path.read_bytes() == b"new mp3"


def test_generate_with_retry_success_without_preserved_output_fails() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "missing.mp3"

        def fake_run(cmd, *args, cwd=None, **kwargs):
            result = _mock.Mock()
            result.returncode = 0
            result.stdout = '{"saved": "missing.mp3"}'
            result.stderr = ""
            return result

        stderr_buffer = io.StringIO()
        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("sys.stderr", stderr_buffer):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=1,
                retry_delay=0.1,
                output_path=str(output_path),
            )

        assert ret == 1, f"expected missing success artifact to fail, got {ret}"
        assert not output_path.exists()
        assert "no generated output file" in stderr_buffer.getvalue()


def test_generate_with_retry_rejects_unprobeable_signal_output() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "M3_song.mp3"

        def fake_run(cmd, *args, cwd=None, **kwargs):
            output_path.write_bytes(b"not actually an mp3")
            result = _mock.Mock()
            result.returncode = 143
            result.stdout = ""
            result.stderr = "Terminated: 15\n"
            return result

        stderr_buffer = io.StringIO()
        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("generate_with_retry._is_probeable_audio", return_value=False), \
             _mock.patch("sys.stderr", stderr_buffer):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=1,
                retry_delay=0.1,
            )

        assert ret == 143, f"expected unprobeable output not to be accepted, got {ret}"
        assert "not probeable" in stderr_buffer.getvalue()


def test_generate_with_retry_does_not_accept_saved_name_on_non_signal_failure() -> None:
    import generate_with_retry as _gwr
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "M3_song.mp3"

        def fake_run(cmd, *args, cwd=None, **kwargs):
            if cwd:
                (Path(cwd) / "music_saved.mp3").write_bytes(b"fresh internal mp3")
            result = _mock.Mock()
            result.returncode = 2
            result.stdout = '{"saved": "music_saved.mp3"}'
            result.stderr = "real non-signal failure\n"
            return result

        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("generate_with_retry._is_probeable_audio", return_value=True):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=1,
                retry_delay=0.1,
                output_path=str(output_path),
            )

        assert ret == 2, f"expected non-signal failure to stay failed, got {ret}"
        assert not output_path.exists()


def test_batch_cover_dry_run_builds_sequential_retry_commands() -> None:
    import contextlib
    import io

    from batch_cover import build_cover_commands, run_batch

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        source = tmpdir_path / "source.mp3"
        source.write_bytes(b"fake source audio")
        prompts = tmpdir_path / "prompts.json"
        prompts.write_text(
            json.dumps(
                [
                    {"name": "warm_folk", "prompt": "warm indie folk"},
                    {"name": "dry_soul", "prompt": "dry vintage soul"},
                ]
            ),
            encoding="utf-8",
        )
        out_dir = tmpdir_path / "covers"

        commands = build_cover_commands(
            audio_file=source,
            prompts_file=prompts,
            out_dir=out_dir,
            expected_duration_seconds=180,
            overwrite=False,
        )

    assert len(commands) == 2
    for item in commands:
        assert item["name"] in {"warm_folk", "dry_soul"}
        command = item["command"]
        assert command[:2] == [sys.executable, str(SCRIPT_DIR / "generate_with_retry.py")]
        assert command.count("--output-path") == 1
        assert "--expected-duration-seconds" in command
        assert command[-1].endswith(".mp3")
        assert "music" in command and "cover" in command
        assert command.count("--audio-file") == 1
        assert command.count("--out") == 1

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        ret = run_batch(commands, dry_run=True)
    payload = json.loads(buffer.getvalue())
    assert ret == 0
    assert len(payload["results"]) == 2
    assert all(item["status"] == "dry_run" for item in payload["results"])
    assert all(item["command"] for item in payload["results"])


def test_per_stem_analysis_reads_stems_json_and_classifies_mix_issues() -> None:
    from per_stem_analysis import build_stem_report

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        stems_dir = tmpdir_path / "stems"
        stems_dir.mkdir()
        stems = {}
        for name, size in {"vocals": 100, "drums": 600, "bass": 250, "other": 50}.items():
            path = stems_dir / f"{name}.wav"
            path.write_bytes(b"0" * size)
            stems[name] = str(path)
        stems_json = stems_dir / "stems.json"
        stems_json.write_text(json.dumps({"stems": stems}), encoding="utf-8")

        report = build_stem_report(stems_json)

    assert report["status"] == "ok"
    assert set(report["stems"].keys()) == {"vocals", "drums", "bass", "other"}
    assert any("dominant" in note.lower() for note in report["mix_notes"])
    assert report["recommendations"], "expected non-musician recommendations"


def test_hybrid_remix_requires_validated_transformed_stem_unless_smoke_test_mode() -> None:
    from hybrid_remix import build_plan

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        stems_dir = tmpdir_path / "stems"
        stems_dir.mkdir()
        stems = {}
        for name in ("vocals", "drums", "bass", "other"):
            path = stems_dir / f"{name}.wav"
            path.write_bytes(b"fake wav")
            stems[name] = str(path)
        stems_json = stems_dir / "stems.json"
        stems_json.write_text(json.dumps({"stems": stems}), encoding="utf-8")
        output = tmpdir_path / "preview.mp3"

        try:
            build_plan(
                stems_json=stems_json,
                target_stem="drums",
                prompt="tight acoustic drums",
                output=output,
                transformed_stem=None,
                allow_stem_cover=False,
            )
        except ValueError as exc:
            assert "stem-only MiniMax cover" in str(exc)
        else:
            raise AssertionError("expected hybrid remix to reject unvalidated stem-to-cover path")

        plan = build_plan(
            stems_json=stems_json,
            target_stem="drums",
            prompt="tight acoustic drums",
            output=output,
            transformed_stem=Path(stems["drums"]),
            allow_stem_cover=False,
        )

    assert plan["target_stem"] == "drums"
    assert "ffmpeg" in plan["mix_command"][0]
    assert plan["cover_command"] is None


def test_hybrid_remix_validates_source_stems_before_stem_cover_plan() -> None:
    from hybrid_remix import build_plan

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        stems_dir = tmpdir_path / "stems"
        stems_dir.mkdir()
        stems = {}
        for name in ("vocals", "bass", "other"):
            path = stems_dir / f"{name}.wav"
            path.write_bytes(b"fake wav")
            stems[name] = str(path)
        stems["drums"] = str(stems_dir / "missing_drums.wav")
        stems_json = stems_dir / "stems.json"
        stems_json.write_text(json.dumps({"stems": stems}), encoding="utf-8")

        try:
            build_plan(
                stems_json=stems_json,
                target_stem="drums",
                prompt="tight acoustic drums",
                output=tmpdir_path / "preview.mp3",
                transformed_stem=None,
                allow_stem_cover=True,
            )
        except FileNotFoundError as exc:
            assert "source stem not found" in str(exc)
        else:
            raise AssertionError("expected missing source stem to fail during plan construction")


def test_generate_with_retry_saved_name_signal_respects_existing_output_path() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "M3_song.mp3"
        output_path.write_bytes(b"old output")

        def fake_run(cmd, *args, cwd=None, **kwargs):
            if cwd:
                (Path(cwd) / "music_saved.mp3").write_bytes(b"fresh internal mp3")
            result = _mock.Mock()
            result.returncode = 143
            result.stdout = '{"saved": "music_saved.mp3"}'
            result.stderr = "Terminated: 15\n"
            return result

        stderr_buffer = io.StringIO()
        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("generate_with_retry._is_probeable_audio", return_value=True), \
             _mock.patch("sys.stderr", stderr_buffer):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=1,
                retry_delay=0.1,
                output_path=str(output_path),
            )

        assert ret == 143, f"expected existing output path to be rejected, got {ret}"
        assert output_path.read_bytes() == b"old output"
        assert "not accepting signal-saved output" in stderr_buffer.getvalue()


def test_generate_with_retry_rejects_stale_saved_name_from_previous_attempt() -> None:
    import generate_with_retry as _gwr
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "M3_song.mp3"
        call_count = {"value": 0}

        def fake_run(cmd, *args, cwd=None, **kwargs):
            call_count["value"] += 1
            if cwd and call_count["value"] == 1:
                (Path(cwd) / "music_saved.mp3").write_bytes(b"old internal mp3")
            result = _mock.Mock()
            if call_count["value"] == 1:
                result.returncode = 6
                result.stdout = ""
                result.stderr = "code 6, Network request failed\n"
            else:
                result.returncode = 143
                result.stdout = '{"saved": "music_saved.mp3"}'
                result.stderr = "Terminated: 15\n"
            return result

        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("generate_with_retry._is_probeable_audio", return_value=True), \
             _mock.patch("time.sleep", lambda _seconds: None):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=2,
                retry_delay=0.1,
                output_path=str(output_path),
            )

        assert ret == 143, f"expected stale saved_name file not to be recovered, got {ret}"
        assert not output_path.exists()


def test_generate_with_retry_rejects_stale_internal_file_from_previous_attempt() -> None:
    import generate_with_retry as _gwr
    import io
    import unittest.mock as _mock

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "M3_song.mp3"
        call_count = {"value": 0}

        def fake_run(cmd, *args, cwd=None, **kwargs):
            call_count["value"] += 1
            if cwd and call_count["value"] == 1:
                (Path(cwd) / "old_internal_saved.mp3").write_bytes(b"old internal mp3")
            result = _mock.Mock()
            if call_count["value"] == 1:
                result.returncode = 6
                result.stdout = ""
                result.stderr = "code 6, Network request failed\n"
            else:
                result.returncode = 143
                result.stdout = ""
                result.stderr = "Terminated: 15\n"
            return result

        stderr_buffer = io.StringIO()
        with _mock.patch("subprocess.run", side_effect=fake_run), \
             _mock.patch("time.sleep", lambda _seconds: None), \
             _mock.patch("sys.stderr", stderr_buffer):
            ret = _gwr.run_with_retry(
                "fake_mmx",
                ["music", "generate", "--prompt", "hello", "--out", str(output_path)],
                attempts=2,
                retry_delay=0.1,
                output_path=str(output_path),
            )

        assert ret == 143, f"expected stale internal file not to be recovered, got {ret}"
        assert not output_path.exists()
        assert "recovered from the run directory" not in stderr_buffer.getvalue()


def test_generate_with_retry_retries_transient_failure_and_injects_timeout() -> None:
    script_path = SCRIPT_DIR / "generate_with_retry.py"
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        fake_mmx = tmpdir_path / "fake_mmx.py"
        attempts_file = tmpdir_path / "attempts.txt"
        args_file = tmpdir_path / "args.txt"
        fake_mmx.write_text(
            """
import pathlib
import sys

attempts = pathlib.Path(sys.argv[1])
args_file = pathlib.Path(sys.argv[2])
count = int(attempts.read_text() or "0") if attempts.exists() else 0
count += 1
attempts.write_text(str(count))
args_file.write_text(" ".join(sys.argv[3:]))
if count == 1:
    print("code 6, Network request failed", file=sys.stderr)
    raise SystemExit(6)
raise SystemExit(0)
""".strip(),
            encoding="utf-8",
        )

        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--mmx-bin", sys.executable,
                "--retry-delay", "0",
                "--",
                str(fake_mmx), str(attempts_file), str(args_file),
                "music", "generate", "--prompt", "hello",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0, result.stderr
        assert attempts_file.read_text() == "2"
        assert "--timeout 600" in args_file.read_text()


def test_verify_cloud_output_rejects_zero_duration() -> None:
    script_path = SCRIPT_DIR / "verify_cloud_output.sh"
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        audio_path = tmpdir_path / "song.mp3"
        audio_path.write_bytes(b"ID3 fake")
        ffprobe_path = tmpdir_path / "ffprobe"
        ffprobe_path.write_text(
            "#!/usr/bin/env bash\n"
            "case \"$*\" in\n"
            "  *format=duration*) echo '0.000000' ;;\n"
            "  *format=format_name*) echo 'mp3' ;;\n"
            "  *) exit 1 ;;\n"
            "esac\n",
            encoding="utf-8",
        )
        ffprobe_path.chmod(0o755)
        env = {**os.environ, "PATH": f"{tmpdir}:{os.environ.get('PATH', '')}"}

        result = subprocess.run(
            [str(script_path), str(audio_path), "--min-bytes", "1"],
            capture_output=True,
            text=True,
            env=env,
            timeout=10,
        )

    assert result.returncode == 1
    assert "duration must be positive" in result.stderr


def test_finalize_track_script_documents_loudnorm_command() -> None:
    script_path = SCRIPT_DIR / "finalize_track.sh"
    text = script_path.read_text(encoding="utf-8")

    assert "loudnorm=I=-16:TP=-1:LRA=11" in text
    assert "ffmpeg" in text


def test_compute_audio_embedding_requires_remote_code_opt_in() -> None:
    source = (SCRIPT_DIR / "compute_audio_embedding.py").read_text(encoding="utf-8")

    assert "allow_remote_code" in source
    assert "trust_remote_code=allow_remote_code" in source
    assert "--allow-remote-model-code" in source


def test_orchestrator_passes_remote_code_consent_to_mert() -> None:
    source = (SCRIPT_DIR / "analysis_orchestrator.py").read_text(encoding="utf-8")

    assert "allow_remote_model_code" in source
    assert "allow_remote_code=allow_remote_model_code" in source
    assert "--allow-remote-model-code" in source
    assert "auto-installs yt-dlp" not in source


def test_lint_music_request_uses_only_stdlib() -> None:
    """Verify lint_music_request.py imports only standard-library modules."""
    lint_path = SCRIPT_DIR / "lint_music_request.py"
    source = lint_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.append(node.module)

    stdlib_modules = set(sys.stdlib_module_names)
    non_stdlib = [name for name in imported if name.split(".")[0] not in stdlib_modules]
    assert not non_stdlib, f"non-stdlib imports detected: {non_stdlib}"


def test_orchestrator_rejects_youtube_flag() -> None:
    """v1.5.0: --youtube was removed. URL downloads live in music-source-fetch."""
    import subprocess, sys, os
    cwd = os.path.dirname(os.path.abspath(__file__))
    result = subprocess.run(
        [sys.executable, "analysis_orchestrator.py", "--youtube", "https://youtube.com/x",
         "--audio", "/tmp/none.wav"],
        capture_output=True, text=True, cwd=cwd,
    )
    assert result.returncode != 0, f"--youtube should be rejected, got rc=0:\n{result.stdout}"
    assert "unrecognized arguments" in result.stderr, \
        f"expected 'unrecognized arguments', got:\n{result.stderr}"


def test_orchestrator_rejects_image_and_video_flags() -> None:
    """v1.5.0: --image, --video, --vlm, --ocr, --faces all removed (no image pipeline)."""
    import subprocess, sys, os
    cwd = os.path.dirname(os.path.abspath(__file__))
    for flag in ("--image", "--video", "--vlm", "--ocr", "--faces"):
        result = subprocess.run(
            [sys.executable, "analysis_orchestrator.py", flag, "/tmp/x",
             "--audio", "/tmp/none.wav"],
            capture_output=True, text=True, cwd=cwd,
        )
        assert result.returncode != 0, f"{flag} should be rejected, got rc=0"
        assert "unrecognized arguments" in result.stderr, \
            f"{flag} should be unrecognized; got:\n{result.stderr}"


def test_orchestrator_rejects_lyrics_source_flag() -> None:
    """v1.5.0: --lyrics-source removed. Whisper is the only lyrics source."""
    import subprocess, sys, os
    cwd = os.path.dirname(os.path.abspath(__file__))
    result = subprocess.run(
        [sys.executable, "analysis_orchestrator.py", "--lyrics-source", "auto",
         "--audio", "/tmp/none.wav"],
        capture_output=True, text=True, cwd=cwd,
    )
    assert result.returncode != 0
    assert "unrecognized arguments" in result.stderr


def test_orchestrator_accepts_local_audio_still() -> None:
    """Sanity: --audio (local file path) and friends still work after the strip."""
    import subprocess, sys, os
    cwd = os.path.dirname(os.path.abspath(__file__))
    result = subprocess.run(
        [sys.executable, "analysis_orchestrator.py", "--help"],
        capture_output=True, text=True, cwd=cwd,
    )
    assert result.returncode == 0
    assert "--audio" in result.stdout
    assert "--lyrics" in result.stdout
    assert "--use-demucs" in result.stdout
    # Negative: removed flags must NOT appear in --help
    for removed in ("--youtube", "--audio-url", "--image", "--video",
                    "--vlm", "--ocr", "--faces", "--lyrics-source"):
        assert removed not in result.stdout, \
            f"{removed} should not appear in --help after v1.5.0 strip"




def main() -> int:
    tests = [
        ('test_check_environment_no_longer_lists_yt_dlp_or_image_imports', test_check_environment_no_longer_lists_yt_dlp_or_image_imports),
        ('test_orchestrator_parse_song_stem', test_orchestrator_parse_song_stem),
        ('test_cached_or_compute_roundtrip', test_cached_or_compute_roundtrip),
        ('test_build_final_prompt_priorities', test_build_final_prompt_priorities),
        ('test_lint_music_request_standard_spanish_song', test_lint_music_request_standard_spanish_song),
        ('test_lint_music_request_routes_cover_to_minimax_cover', test_lint_music_request_routes_cover_to_minimax_cover),
        ('test_lint_music_request_routes_style_transfer_to_minimax_style_transfer', test_lint_music_request_routes_style_transfer_to_minimax_style_transfer),
        ('test_lint_music_request_instrumental_jingle_skips_vocal_question', test_lint_music_request_instrumental_jingle_skips_vocal_question),
        ('test_lint_music_request_plain_style_reference_needs_clarification', test_lint_music_request_plain_style_reference_needs_clarification),
        ('test_lint_music_request_text_style_reference_with_clear_target', test_lint_music_request_text_style_reference_with_clear_target),
        ('test_lint_music_request_url_returns_url_not_accepted_warning', test_lint_music_request_url_returns_url_not_accepted_warning),
        ('test_lint_music_request_jiosaavn_url_returns_url_not_accepted_warning', test_lint_music_request_jiosaavn_url_returns_url_not_accepted_warning),
        ('test_lint_music_request_local_file_still_routes_to_cover', test_lint_music_request_local_file_still_routes_to_cover),
        ('test_lint_music_request_mashup_routes_to_minimax_mashup_when_complete', test_lint_music_request_mashup_routes_to_minimax_mashup_when_complete),
        ('test_lint_music_request_emotion_prompt_routes_to_minimax_emotion_prompt', test_lint_music_request_emotion_prompt_routes_to_minimax_emotion_prompt),
        ('test_lint_music_request_mashup_blocker_for_missing_song_b', test_lint_music_request_mashup_blocker_for_missing_song_b),
        ('test_lint_music_request_blocker_for_missing_lyrics_decision', test_lint_music_request_blocker_for_missing_lyrics_decision),
        ('test_lint_music_request_blocker_for_conflicting_cover_style_transfer', test_lint_music_request_blocker_for_conflicting_cover_style_transfer),
        ('test_lint_music_request_cinematic_with_instruments_is_not_placeholder', test_lint_music_request_cinematic_with_instruments_is_not_placeholder),
        ('test_lint_music_request_prompt_warnings_and_flag_conflicts', test_lint_music_request_prompt_warnings_and_flag_conflicts),
        ('test_lint_music_request_key_conflict', test_lint_music_request_key_conflict),
        ('test_lint_music_request_duration_conflict', test_lint_music_request_duration_conflict),
        ('test_lint_music_request_vocal_mode_conflict', test_lint_music_request_vocal_mode_conflict),
        ('test_lint_music_request_language_conflict', test_lint_music_request_language_conflict),
        ('test_lint_music_request_warns_and_blocks_on_prompt_byte_length', test_lint_music_request_warns_and_blocks_on_prompt_byte_length),
        ('test_lint_music_request_warns_on_long_lyric_heavy_generation', test_lint_music_request_warns_on_long_lyric_heavy_generation),
        ('test_lint_music_request_blocks_invalid_lyrics_tags_and_estimates_duration', test_lint_music_request_blocks_invalid_lyrics_tags_and_estimates_duration),
        ('test_lint_music_request_plain_lyrics_word_stays_standard_song', test_lint_music_request_plain_lyrics_word_stays_standard_song),
        ('test_lint_lyrics_rejects_non_whitelisted_tags_and_reports_duration', test_lint_lyrics_rejects_non_whitelisted_tags_and_reports_duration),
        ('test_verify_lyrics_alignment_flags_semantic_mismatch', test_verify_lyrics_alignment_flags_semantic_mismatch),
        ('test_finalize_track_refuses_overwrite_without_flag', test_finalize_track_refuses_overwrite_without_flag),
        ('test_extract_lyrics_whisper_default_model_and_section_normalization', test_extract_lyrics_whisper_default_model_and_section_normalization),
        ('test_extract_lyrics_whisper_sanity_flags_language_and_looping', test_extract_lyrics_whisper_sanity_flags_language_and_looping),
        ('test_generate_with_retry_moves_saved_file_to_requested_output_path', test_generate_with_retry_moves_saved_file_to_requested_output_path),
        ('test_generate_with_retry_warns_when_output_is_shorter_than_expected', test_generate_with_retry_warns_when_output_is_shorter_than_expected),
        ('test_generate_with_retry_warns_on_long_cloud_prompt', test_generate_with_retry_warns_on_long_cloud_prompt),
        ('test_generate_with_retry_requires_out_when_output_path_is_requested', test_generate_with_retry_requires_out_when_output_path_is_requested),
        ('test_generate_with_retry_resolves_equals_form_relative_paths', test_generate_with_retry_resolves_equals_form_relative_paths),
        ('test_generate_with_retry_probe_falls_back_to_mp3_header_without_ffprobe', test_generate_with_retry_probe_falls_back_to_mp3_header_without_ffprobe),
        ('test_generate_with_retry_probe_reads_header_only', test_generate_with_retry_probe_reads_header_only),
        ('test_generate_with_retry_accepts_saved_file_after_signal_exit', test_generate_with_retry_accepts_saved_file_after_signal_exit),
        ('test_generate_with_retry_moves_signal_out_file_to_output_path', test_generate_with_retry_moves_signal_out_file_to_output_path),
        ('test_generate_with_retry_rejects_stale_file_after_signal_exit', test_generate_with_retry_rejects_stale_file_after_signal_exit),
        ('test_generate_with_retry_rejects_overwritten_file_without_overwrite_flag', test_generate_with_retry_rejects_overwritten_file_without_overwrite_flag),
        ('test_generate_with_retry_recovers_internal_file_after_signal_exit', test_generate_with_retry_recovers_internal_file_after_signal_exit),
        ('test_generate_with_retry_recovers_internal_signal_output_without_explicit_destination', test_generate_with_retry_recovers_internal_signal_output_without_explicit_destination),
        ('test_generate_with_retry_moves_success_output_without_explicit_destination', test_generate_with_retry_moves_success_output_without_explicit_destination),
        ('test_generate_with_retry_warns_on_unprobeable_fresh_success_output', test_generate_with_retry_warns_on_unprobeable_fresh_success_output),
        ('test_generate_with_retry_rejects_success_output_from_previous_attempt', test_generate_with_retry_rejects_success_output_from_previous_attempt),
        ('test_generate_with_retry_rejects_unprobeable_success_output_from_previous_attempt', test_generate_with_retry_rejects_unprobeable_success_output_from_previous_attempt),
        ('test_generate_with_retry_prefers_fresh_out_over_stale_saved_name', test_generate_with_retry_prefers_fresh_out_over_stale_saved_name),
        ('test_generate_with_retry_moves_success_out_file_to_output_path', test_generate_with_retry_moves_success_out_file_to_output_path),
        ('test_generate_with_retry_accepts_successful_in_place_out_overwrite', test_generate_with_retry_accepts_successful_in_place_out_overwrite),
        ('test_generate_with_retry_success_without_preserved_output_fails', test_generate_with_retry_success_without_preserved_output_fails),
        ('test_generate_with_retry_rejects_unprobeable_signal_output', test_generate_with_retry_rejects_unprobeable_signal_output),
        ('test_generate_with_retry_does_not_accept_saved_name_on_non_signal_failure', test_generate_with_retry_does_not_accept_saved_name_on_non_signal_failure),
        ('test_batch_cover_dry_run_builds_sequential_retry_commands', test_batch_cover_dry_run_builds_sequential_retry_commands),
        ('test_per_stem_analysis_reads_stems_json_and_classifies_mix_issues', test_per_stem_analysis_reads_stems_json_and_classifies_mix_issues),
        ('test_hybrid_remix_requires_validated_transformed_stem_unless_smoke_test_mode', test_hybrid_remix_requires_validated_transformed_stem_unless_smoke_test_mode),
        ('test_hybrid_remix_validates_source_stems_before_stem_cover_plan', test_hybrid_remix_validates_source_stems_before_stem_cover_plan),
        ('test_generate_with_retry_saved_name_signal_respects_existing_output_path', test_generate_with_retry_saved_name_signal_respects_existing_output_path),
        ('test_generate_with_retry_rejects_stale_saved_name_from_previous_attempt', test_generate_with_retry_rejects_stale_saved_name_from_previous_attempt),
        ('test_generate_with_retry_rejects_stale_internal_file_from_previous_attempt', test_generate_with_retry_rejects_stale_internal_file_from_previous_attempt),
        ('test_generate_with_retry_retries_transient_failure_and_injects_timeout', test_generate_with_retry_retries_transient_failure_and_injects_timeout),
        ('test_verify_cloud_output_rejects_zero_duration', test_verify_cloud_output_rejects_zero_duration),
        ('test_finalize_track_script_documents_loudnorm_command', test_finalize_track_script_documents_loudnorm_command),
        ('test_compute_audio_embedding_requires_remote_code_opt_in', test_compute_audio_embedding_requires_remote_code_opt_in),
        ('test_orchestrator_passes_remote_code_consent_to_mert', test_orchestrator_passes_remote_code_consent_to_mert),
        ('test_lint_music_request_uses_only_stdlib', test_lint_music_request_uses_only_stdlib),
        ('test_orchestrator_rejects_youtube_flag', test_orchestrator_rejects_youtube_flag),
        ('test_orchestrator_rejects_image_and_video_flags', test_orchestrator_rejects_image_and_video_flags),
        ('test_orchestrator_rejects_lyrics_source_flag', test_orchestrator_rejects_lyrics_source_flag),
        ('test_orchestrator_accepts_local_audio_still', test_orchestrator_accepts_local_audio_still),
    ]

    failures = 0
    for name, func in tests:
        try:
            func()
        except Exception as exc:  # noqa: BLE001 - smoke harness wants to report any failure
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
