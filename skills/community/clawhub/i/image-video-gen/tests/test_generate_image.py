"""Regression tests for scripts/generate_image.py.

Mocks out the HTTP layer (requests.post / requests.get) and exercises the
per-model validation chain: duration/size/ratio/resolution coercion, prompt
whitelisting, target* restrictions, klingV3Omni special serialization, etc.

Run:   pytest tests -q
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest
import requests


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "generate_image.py"


@pytest.fixture(autouse=True)
def _require_token():
    os.environ.setdefault("AI_ARTIST_TOKEN", "sk-test-dummy")


@pytest.fixture()
def gi(monkeypatch):
    """Import a fresh copy of the module with network + estimator stubbed."""
    # Force a fresh import so each test has an isolated cache
    spec = importlib.util.spec_from_file_location("generate_image_under_test", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]

    # Seed the model-list cache so check_model_available passes for every test
    mod._MODEL_LIST_CACHE["rows"] = [
        {"sourceType": "IMAGE_MODEL", "sourceValue": cfg["methodType"],
         "hiddenState": "0", "sourceName": cfg["source_name"]}
        for k, cfg in mod.MODEL_CONFIGS.items() if cfg["media_type"] == "image"
    ] + [
        {"sourceType": "VIDEO_MODEL", "sourceValue": cfg["methodType"],
         "hiddenState": "0", "sourceName": cfg["source_name"]}
        for k, cfg in mod.MODEL_CONFIGS.items() if cfg["media_type"] == "video"
    ]
    mod._MODEL_LIST_CACHE["expires_at"] = float("inf")

    captured = {"payloads": []}

    class Resp:
        status_code = 200
        def json(self):
            return {"msg": "ok", "code": 200, "data": ["task-xxx"]}
        def raise_for_status(self):
            pass

    def fake_post(url, **kw):
        if "consumeSource/list" in url:
            r = Resp()
            r.json = lambda: {"code": 200, "msg": "ok", "rows": mod._MODEL_LIST_CACHE["rows"]}  # type: ignore
            return r
        if "estimate" in url.lower() or "cost" in url.lower():
            r = Resp()
            r.json = lambda: {"msg": "ok", "code": 200,
                              "data": {"estimatedCost": 1.0, "sufficientBalance": True}}  # type: ignore
            return r
        body = json.loads(kw["data"]) if "data" in kw else kw.get("json", {})
        captured["payloads"].append(body)
        return Resp()

    monkeypatch.setattr(requests, "post", fake_post)
    monkeypatch.setattr(mod, "estimate_generation_cost", lambda _: True)
    return mod, captured


def _last_parameter(captured):
    return json.loads(captured["payloads"][-1]["parameter"])


# ---------------------------------------------------------------------------
# Prompt validation
# ---------------------------------------------------------------------------
class TestPromptRequired:
    @pytest.mark.parametrize("model", ["S5.0L", "N2", "W2.7"])
    def test_image_empty_prompt_rejected(self, gi, model):
        mod, _ = gi
        assert mod.create_generation_task("", model=model) is None
        assert mod.create_generation_task("   ", model=model) is None
        assert mod.create_generation_task(None, model=model) is None

    @pytest.mark.parametrize("model", ["S1.5Pro", "V3.1FB", "W2.6t", "klingV3Omni"])
    def test_video_empty_prompt_rejected(self, gi, model):
        mod, _ = gi
        assert mod.create_video_task("", model=model) is None

    def test_w26i_allows_empty_prompt(self, gi):
        mod, captured = gi
        assert mod.create_video_task("", model="W2.6i", first_image_url="x") == "task-xxx"

    def test_kling_customize_allows_empty_prompt(self, gi):
        mod, _ = gi
        result = mod.create_video_task(
            "", model="klingV3Omni", shot_type="customize",
            multi_prompt=[{"index": 1, "prompt": "a", "duration": 5}],
        )
        assert result == "task-xxx"


# ---------------------------------------------------------------------------
# Duration enforcement
# ---------------------------------------------------------------------------
class TestDurationRules:
    @pytest.mark.parametrize("model", ["V3.1FB", "V3.1PB"])
    def test_v31fb_pb_fixed_eight(self, gi, model):
        mod, captured = gi
        mod.create_video_task("hi", model=model, duration=4)
        assert _last_parameter(captured)["duration"] == 8

    def test_v31fast_snaps_to_valid(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="V3.1Fast", duration=5)
        assert _last_parameter(captured)["duration"] == 8
        mod.create_video_task("hi", model="V3.1Fast", duration=4)
        assert _last_parameter(captured)["duration"] == 4

    def test_kling_3_to_15(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="klingV3Omni", duration=20)
        assert _last_parameter(captured)["duration"] == 10

    def test_w26r_capped_at_10(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="W2.6r", duration=15)
        assert _last_parameter(captured)["duration"] == 10

    def test_w27r_with_video_capped_at_10(self, gi):
        mod, captured = gi
        mod.create_video_task(
            "hi", model="W2.7r", duration=15,
            video_url_list=["https://x.mp4"],
        )
        assert _last_parameter(captured)["duration"] == 10

    def test_w27r_without_video_allows_15(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="W2.7r", duration=15)
        assert _last_parameter(captured)["duration"] == 15


# ---------------------------------------------------------------------------
# Size serialization
# ---------------------------------------------------------------------------
class TestSizeSerialization:
    def test_w26t_uses_star_pixel_size(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="W2.6t")
        assert "*" in _last_parameter(captured)["size"]

    def test_w26r_uses_star_pixel_size(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="W2.6r")
        assert "*" in _last_parameter(captured)["size"]

    def test_w27_series_uses_ratio_string(self, gi):
        mod, captured = gi
        for model in ["W2.7t", "W2.7i", "W2.7r"]:
            kw = {"first_image_url": "x"} if model == "W2.7i" else {}
            mod.create_video_task("hi", model=model, **kw)
            size = _last_parameter(captured)["size"]
            assert "*" not in size, f"{model} should NOT use pixel format"

    def test_image_w27_uses_star_default(self, gi):
        mod, captured = gi
        mod.create_generation_task("hi", model="W2.7")
        assert "*" in _last_parameter(captured)["size"]


# ---------------------------------------------------------------------------
# Whitelist filtering
# ---------------------------------------------------------------------------
class TestFieldWhitelist:
    def test_s15pro_strips_v3_fields(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="S1.5Pro")
        p = _last_parameter(captured)
        for k in ("n", "personGeneration", "resizeMode", "enhancePrompt",
                 "shotType", "promptExtend"):
            assert k not in p, f"S1.5Pro should not carry {k}"

    def test_w26t_strips_veo_fields(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="W2.6t")
        p = _last_parameter(captured)
        for k in ("n", "personGeneration", "resizeMode", "enhancePrompt",
                 "generateAudio"):
            assert k not in p

    def test_kling_has_exclusives(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="klingV3Omni")
        p = _last_parameter(captured)
        for k in ("mode", "multiShot", "keepOriginalSound", "shotType"):
            assert k in p
        assert "resolution" not in p

    def test_w26i_omits_ratio_and_last_image(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="W2.6i", first_image_url="x",
                              last_image_url="y")
        p = _last_parameter(captured)
        assert "ratio" not in p
        assert "lastImageUrl" not in p

    def test_image_websearch_only_where_supported(self, gi):
        mod, captured = gi
        mod.create_generation_task("hi", model="S5.0L", web_search=True)
        assert _last_parameter(captured)["webSearch"] is True
        mod.create_generation_task("hi", model="W2.7")
        assert "webSearch" not in _last_parameter(captured)


# ---------------------------------------------------------------------------
# Target* restrictions
# ---------------------------------------------------------------------------
class TestRestrictions:
    @pytest.mark.parametrize("model,exp", [
        ("S1.5Pro",  {"targetMaxSize": 30, "targetMinLength": 300, "targetMaxLength": 6000}),
        ("V3.1FB",   {"targetMaxSize": 10, "targetMinLength": 300, "targetMaxLength": 6000}),
        ("W2.6t",    {"targetMaxSize": 10, "targetMinLength": 360, "targetMaxLength": 2000}),
        ("W2.6r",    {"targetMaxSize": 10, "targetMinLength": 240, "targetMaxLength": 5000}),
        ("W2.7i",    {"targetMaxSize": 20, "targetMinLength": 240, "targetMaxLength": 8000}),
        ("W2.7r",    {"targetMaxSize": 10, "targetMinLength": 240, "targetMaxLength": 5000}),
    ])
    def test_video_target_values(self, gi, model, exp):
        mod, captured = gi
        kw = {"first_image_url": "x"} if model == "W2.7i" else {}
        mod.create_video_task("hi", model=model, **kw)
        p = _last_parameter(captured)
        for key, val in exp.items():
            assert p.get(key) == val, f"{model} {key}"

    def test_kling_has_no_maxlength(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="klingV3Omni")
        p = _last_parameter(captured)
        assert p["targetMaxSize"] == 10
        assert p["targetMinLength"] == 300
        assert "targetMaxLength" not in p

    @pytest.mark.parametrize("model,length,limit", [
        ("S5.0L", 500, 300),
        ("W2.7", 3000, 2500),
    ])
    def test_image_prompt_truncated(self, gi, model, length, limit):
        mod, captured = gi
        mod.create_generation_task("a" * length, model=model)
        assert len(_last_parameter(captured)["prompt"]) == limit

    def test_video_negative_prompt_truncated(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="V3.1Fast", negative_prompt="n" * 500)
        assert len(_last_parameter(captured)["negativePrompt"]) == 250


# ---------------------------------------------------------------------------
# Value whitelisting (coerce_value)
# ---------------------------------------------------------------------------
class TestValueCoercion:
    def test_bad_ratio_falls_back(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="klingV3Omni", ratio="3:4")  # not allowed
        assert _last_parameter(captured)["ratio"] == "16:9"

    def test_bad_resolution_falls_back(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="S1.5Pro", resolution="4K")
        assert _last_parameter(captured)["resolution"] == "720p"

    def test_bad_generation_type_falls_back(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="W2.6t", generation_type="FIRST&LAST")
        assert _last_parameter(captured)["generationType"] == "TEXT"

    def test_bad_image_quality_falls_back(self, gi):
        mod, captured = gi
        mod.create_generation_task("hi", model="S5.0L", quality="4K")
        assert _last_parameter(captured)["quality"] == "2K"


# ---------------------------------------------------------------------------
# klingV3Omni-specific serialization
# ---------------------------------------------------------------------------
class TestKlingSerialization:
    def test_shot_type_multi_becomes_intelligence(self, gi):
        mod, captured = gi
        mod.create_video_task("hi", model="klingV3Omni", shot_type="multi")
        assert _last_parameter(captured)["shotType"] == "intelligence"

    def test_edit_packs_videolist(self, gi):
        mod, captured = gi
        mod.create_video_task(
            "hi", model="klingV3Omni",
            generation_type="EDIT",
            first_clip_url="https://x.mp4",
            keep_original_sound="yes",
        )
        p = _last_parameter(captured)
        assert "firstClipUrl" not in p
        assert p["videoList"] == [{
            "video_url": "https://x.mp4",
            "refer_type": "base",
            "keep_original_sound": "yes",
        }]
        assert p["generateAudio"] is False

    def test_feature_videolist_uses_feature_refer_type(self, gi):
        mod, captured = gi
        mod.create_video_task(
            "hi", model="klingV3Omni",
            generation_type="FEATURE",
            first_clip_url="https://x.mp4",
        )
        p = _last_parameter(captured)
        assert p["videoList"][0]["refer_type"] == "feature"


# ---------------------------------------------------------------------------
# Media type inference
# ---------------------------------------------------------------------------
class TestInferMediaType:
    @pytest.mark.parametrize("prompt", [
        "生成一段海边日落的视频",
        "让这张照片动起来",
        "一个 8 秒的动画短片",
        "a smooth motion clip of a cat jumping",
        "镜头推进展示产品",
    ])
    def test_video_prompts(self, gi, prompt):
        mod, _ = gi
        assert mod._infer_media_type(prompt) == "video"

    @pytest.mark.parametrize("prompt", [
        "画一只可爱的柴犬",
        "赛博朋克风格的海报",
        "一只戴墨镜的猫",          # neutral
        "",
        None,
        "生成头像插画",
    ])
    def test_image_prompts(self, gi, prompt):
        mod, _ = gi
        assert mod._infer_media_type(prompt) == "image"

    def test_mixed_prompt_prefers_image(self, gi):
        """When both video and image cues coexist, fall back to image (safer default)."""
        mod, _ = gi
        assert mod._infer_media_type("一张海报，画面略微动起来") == "image"


# ---------------------------------------------------------------------------
# Model availability guard
# ---------------------------------------------------------------------------
class TestModelAvailability:
    def test_rejects_hidden_model(self, gi):
        mod, _ = gi
        # Mark S4.5 as hidden in the cache
        for row in mod._MODEL_LIST_CACHE["rows"]:
            if row["sourceValue"] == "0" and row["sourceType"] == "IMAGE_MODEL":
                row["hiddenState"] = "1"
        assert mod.create_generation_task("hi", model="S4.5") is None
