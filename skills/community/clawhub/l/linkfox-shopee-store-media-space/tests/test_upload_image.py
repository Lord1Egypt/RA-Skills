from __future__ import annotations

import base64
import importlib
import sys
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
common = importlib.import_module("_shopee_media_space_common")
runner = importlib.import_module("_media_space_api_runner")


def test_upload_media_space_image_reads_file_and_calls_dedicated_endpoint(tmp_path, monkeypatch):
    image = tmp_path / "product.jpg"
    image.write_bytes(b"\xff\xd8\xfftest-image")
    captured = {}

    def fake_call_api(endpoint, payload):
        captured["endpoint"] = endpoint
        captured["payload"] = payload
        return {"success": True, "imageId": "img-1"}

    monkeypatch.setattr(common, "call_api", fake_call_api)

    result = common.upload_media_space_image({"shopId": " 123 ", "filePath": str(image)})

    assert result["imageId"] == "img-1"
    assert captured["endpoint"].endswith("/shopee/uploadMediaSpaceImage")
    assert captured["payload"] == {
        "shopId": "123",
        "fileBase64": base64.b64encode(image.read_bytes()).decode("ascii"),
        "fileName": "product.jpg",
        "contentType": "image/jpeg",
    }


def test_upload_media_space_image_rejects_unsupported_type(tmp_path):
    image = tmp_path / "product.gif"
    image.write_bytes(b"GIF89a")

    try:
        common.upload_media_space_image({"shopId": "123", "filePath": str(image)})
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("expected unsupported image type to fail")


def test_runner_routes_upload_image_to_dedicated_endpoint(monkeypatch):
    monkeypatch.setattr(runner, "ensure_auth_skill_available", lambda caller: None)
    monkeypatch.setattr(
        runner,
        "upload_media_space_image",
        lambda params: {"success": True, "imageId": "img-2"},
    )

    def fail_if_proxy_called(*args, **kwargs):
        raise AssertionError("upload_image must not use developerProxy")

    monkeypatch.setattr(runner, "developer_proxy_call", fail_if_proxy_called)

    result = runner.run_media_space_api(
        "upload_image",
        {"shopId": "123", "filePath": "/tmp/product.jpg"},
    )

    assert result == {
        "api": "upload_image",
        "uploadMediaSpaceImage": {"success": True, "imageId": "img-2"},
    }


def test_upload_media_space_image_rejects_missing_file(tmp_path):
    missing = tmp_path / "missing.jpg"

    try:
        common.upload_media_space_image({"shopId": "123", "filePath": str(missing)})
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("expected missing image file to fail")


def test_upload_media_space_image_rejects_empty_file(tmp_path):
    image = tmp_path / "empty.png"
    image.write_bytes(b"")

    try:
        common.upload_media_space_image({"shopId": "123", "filePath": str(image)})
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("expected empty image file to fail")


def test_upload_media_space_image_rejects_missing_shop_id(tmp_path):
    image = tmp_path / "product.jpg"
    image.write_bytes(b"\xff\xd8\xfftest-image")

    try:
        common.upload_media_space_image({"filePath": str(image)})
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("expected missing shopId to fail")


def test_upload_media_space_image_rejects_file_over_10mb(tmp_path):
    image = tmp_path / "large.jpg"
    with image.open("wb") as stream:
        stream.seek(10 * 1024 * 1024)
        stream.write(b"x")

    try:
        common.upload_media_space_image({"shopId": "123", "filePath": str(image)})
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("expected oversized image file to fail")


def test_upload_media_space_image_accepts_explicit_content_type(tmp_path, monkeypatch):
    image = tmp_path / "product.bin"
    image.write_bytes(b"\x89PNG\r\n\x1a\ntest-image")
    captured = {}

    def fake_call_api(endpoint, payload):
        captured.update(payload)
        return {"success": True, "imageId": "img-3"}

    monkeypatch.setattr(common, "call_api", fake_call_api)

    common.upload_media_space_image(
        {"shopId": "123", "filePath": str(image), "contentType": "image/png"}
    )

    assert captured["contentType"] == "image/png"
