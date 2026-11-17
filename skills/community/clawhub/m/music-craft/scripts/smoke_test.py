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
    assert "-n" in command and "-y" not in command, "must not overwrite by default"
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
        "[Verse]\nNeon rain on the avenue\n[Chorus]\nStay with me tonight",
        "unrelated transcript with no matching keywords",
        min_overlap=0.45,
    )

    assert result["status"] == "failed"
    assert result["word_overlap"] < 0.45
    assert any("low lyric overlap" in warning for warning in result["warnings"])


def test_wait_for_acestep_duration_guard_and_loopback() -> None:
    import wait_for_acestep as w

    original = w.probe_duration_seconds
    try:
        w.probe_duration_seconds = lambda path: 294.885 if "short" in path.name else 371.0
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp)
            (cache / "short_take.mp3").write_bytes(b"x")
            assert w.check_duration(cache / "short_take.mp3", 371.0, 2.0)["verdict"] == "rejected"
            assert w.scan_cache(cache, 371.0, 2.0)["state"] == "not_found"
            (cache / "full_take.mp3").write_bytes(b"x")
            found = w.scan_cache(cache, 371.0, 2.0)
            assert found["state"] == "found" and found["selected"]["file"].endswith("full_take.mp3")
        w.probe_duration_seconds = lambda path: None
        assert w.check_duration(Path("x.mp3"), 30.0, 2.0)["verdict"] == "unverified"
    finally:
        w.probe_duration_seconds = original
    assert w.is_loopback_url("http://127.0.0.1:8001")
    assert w.is_loopback_url("http://localhost:8001")
    assert not w.is_loopback_url("http://example.com:8001")


def test_helpers_refuse_redirects_and_proxies() -> None:
    import urllib.error
    import urllib.request

    import acestep_request
    import wait_for_acestep

    for module in (acestep_request, wait_for_acestep):
        opener = module.loopback_opener()
        handlers = {type(handler).__name__ for handler in opener.handlers}
        assert "_RejectRedirects" in handlers, handlers
        proxies = [h.proxies for h in opener.handlers if isinstance(h, urllib.request.ProxyHandler) and h.proxies]
        assert not proxies, f"proxies must be disabled, found {proxies}"
        # Offline check: no network call is made; the handler is invoked directly.
        request = urllib.request.Request("http://127.0.0.1:8001/health")
        try:
            module._RejectRedirects().redirect_request(request, None, 302, "Found", {}, "http://example.com/")
        except urllib.error.HTTPError as exc:
            assert "redirect refused" in str(exc.msg)
        else:
            raise AssertionError("redirect was not refused")


def test_extract_stems_checks_the_chosen_models_checkpoints() -> None:
    import inspect

    import extract_stems

    assert "allow_model_download" in inspect.signature(extract_stems.separate_stems).parameters
    with tempfile.TemporaryDirectory() as tmp:
        remote = Path(tmp) / "remote"
        remote.mkdir()
        (remote / "htdemucs_ft.yaml").write_text("models: ['f7e0c4bc', 'd12395a8']\n", encoding="utf-8")
        (remote / "files.txt").write_text("root: x/\nf7e0c4bc-ba3fe64a.th\nd12395a8-e57c48e6.th\n955717e8-8726e21a.th\n", encoding="utf-8")
        required = extract_stems.required_checkpoint_files(remote, "htdemucs_ft")
        assert required == ["f7e0c4bc-ba3fe64a.th", "d12395a8-e57c48e6.th"], required
        cache = Path(tmp) / "checkpoints"
        cache.mkdir()
        (cache / "955717e8-8726e21a.th").write_bytes(b"x")  # unrelated model
        (cache / "f7e0c4bc-ba3fe64a.th").write_bytes(b"x")  # partially cached
        assert extract_stems.missing_checkpoints(cache, required) == ["d12395a8-e57c48e6.th"]
        try:
            extract_stems.required_checkpoint_files(remote, "unknown_model")
        except OSError:
            pass
        else:
            raise AssertionError("unknown model must fail closed")


def main() -> int:
    tests = [
        ("extract_stems planned paths", test_extract_stems_writes_normalized_output_paths),
        ("remix_stems ffmpeg command", test_remix_stems_builds_ffmpeg_amix_command),
        ("wait_for_acestep status classification", test_wait_for_acestep_classifies_empty_query_as_pending),
        ("wait_for_acestep cache files", test_wait_for_acestep_detects_new_audio_files),
        ("wait_for_acestep duration guard and loopback", test_wait_for_acestep_duration_guard_and_loopback),
        ("helpers refuse redirects and proxies", test_helpers_refuse_redirects_and_proxies),
        ("extract_stems checks chosen model checkpoints", test_extract_stems_checks_the_chosen_models_checkpoints),
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
