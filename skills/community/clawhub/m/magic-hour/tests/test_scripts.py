"""Offline tests: the magic_hour SDK is replaced by a fake module."""

import json
import os
import sys
import types
from types import SimpleNamespace

import pytest

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)

import generate_image  # noqa: E402
import image_to_video  # noqa: E402
import status  # noqa: E402
import text_to_video  # noqa: E402


class FakeResource:
    def __init__(self, log, response):
        self.log, self.response = log, response

    def generate(self, **kwargs):
        self.log.append(kwargs)
        return self.response

    def check_result(self, **kwargs):
        self.log.append(kwargs)
        return self.response


@pytest.fixture
def fake_sdk(monkeypatch):
    calls = []
    response = SimpleNamespace(
        id="proj_123", status="complete", credits_charged=120, width=854, height=480, fps=30,
        downloads=[SimpleNamespace(url="https://cdn/out.mp4", expires_at="x")], error=None,
    )
    mod = types.ModuleType("magic_hour")

    class Client:
        def __init__(self, token, **kw):
            calls.append({"token": token})
            r = FakeResource(calls, response)
            self.v1 = SimpleNamespace(
                text_to_video=r, image_to_video=r, ai_image_generator=r,
                video_projects=r, image_projects=r,
            )

    mod.Client = Client
    monkeypatch.setitem(sys.modules, "magic_hour", mod)
    monkeypatch.setenv("MAGIC_HOUR_API_KEY", "mhk_test")
    return calls


def run(capsys, fn, argv):
    fn(argv)
    return json.loads(capsys.readouterr().out.strip().splitlines()[-1])


def test_text_to_video(fake_sdk, capsys):
    out = run(capsys, text_to_video.main, ["a corgi", "--model", "wan-2.2", "--duration", "5", "--aspect-ratio", "9:16"])
    assert out == {
        "project_id": "proj_123", "status": "complete", "model": "wan-2.2",
        "url": "https://cdn/out.mp4", "urls": ["https://cdn/out.mp4"], "credits_charged": 120,
        "width": 854, "height": 480, "fps": 30, "estimated_credits": 120,
    }
    assert fake_sdk[0]["token"] == "mhk_test"
    call = fake_sdk[1]
    assert call["style"] == {"prompt": "a corgi"} and call["end_seconds"] == 5.0
    assert call["aspect_ratio"] == "9:16" and call["resolution"] == "480p"
    assert call["wait_for_completion"] is True and call["download_outputs"] is False


def test_text_to_video_warns_on_bad_duration(fake_sdk, capsys):
    text_to_video.main(["x", "--model", "kling-2.6", "--duration", "7"])
    assert "duration 7s not in allowed" in capsys.readouterr().err


def test_image_to_video_url_and_local(fake_sdk, capsys, tmp_path):
    out = run(capsys, image_to_video.main, ["https://example.com/a.png", "zoom in", "--model", "kling-3.0"])
    assert out["status"] == "complete" and out["estimated_credits"] == 240
    assert fake_sdk[-1]["assets"] == {"image_file_path": "https://example.com/a.png"}

    img = tmp_path / "pic.png"
    img.write_bytes(b"\x89PNG")
    run(capsys, image_to_video.main, [str(img), "pan", "--download-dir", str(tmp_path / "o")])
    assert fake_sdk[-1]["assets"]["image_file_path"] == str(img)
    assert fake_sdk[-1]["download_directory"] == str(tmp_path / "o")


def test_image_to_video_missing_file(fake_sdk, capsys):
    with pytest.raises(SystemExit):
        image_to_video.main(["/nope/missing.png", "pan"])
    assert json.loads(capsys.readouterr().out)["status"] == "error"


def test_generate_image(fake_sdk, capsys):
    out = run(capsys, generate_image.main, ["a cat", "--model", "nano-banana-pro", "--count", "2", "--aspect-ratio", "1:1"])
    assert out["project_id"] == "proj_123" and out["url"] == "https://cdn/out.mp4"
    assert "fps" not in out
    call = fake_sdk[-1]
    assert call["image_count"] == 2 and call["model"] == "nano-banana-pro" and call["aspect_ratio"] == "1:1"


def test_status_no_wait(fake_sdk, capsys):
    out = run(capsys, status.main, ["proj_123", "--kind", "image"])
    assert out["status"] == "complete"
    assert fake_sdk[-1] == {"id": "proj_123", "wait_for_completion": False, "download_outputs": False}


def test_missing_api_key(monkeypatch, capsys):
    monkeypatch.delenv("MAGIC_HOUR_API_KEY", raising=False)
    with pytest.raises(SystemExit):
        text_to_video.main(["x"])
    assert "MAGIC_HOUR_API_KEY" in json.loads(capsys.readouterr().out)["error"]["message"]


def test_sdk_error_is_json(fake_sdk, capsys, monkeypatch):
    class Boom(Exception):
        status_code = 402

    def raise_boom(**kw):
        raise Boom("insufficient credits")

    import magic_hour
    orig = magic_hour.Client

    class C(orig):
        def __init__(self, token, **kw):
            super().__init__(token, **kw)
            self.v1.text_to_video.generate = raise_boom

    monkeypatch.setattr(magic_hour, "Client", C)
    with pytest.raises(SystemExit):
        text_to_video.main(["x"])
    out = json.loads(capsys.readouterr().out)
    assert out["error"] == {"message": "insufficient credits", "status_code": 402}
