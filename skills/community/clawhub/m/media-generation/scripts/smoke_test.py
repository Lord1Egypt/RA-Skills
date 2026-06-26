#!/usr/bin/env python3
import argparse
import base64
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path.cwd()
SCRIPTS = Path(__file__).resolve().parent
OUT = ROOT / "tmp" / "images" / "skill-smoke-tests"


def run(cmd):
    result = subprocess.run(cmd, text=True, capture_output=True)
    return {"cmd": cmd, "returncode": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}


def ensure(cond, message):
    if not cond:
        raise AssertionError(message)


def main():
    p = argparse.ArgumentParser(description="Run lightweight smoke tests for the media-generation skill scripts.")
    p.add_argument("--live", action="store_true", help="Also run live image/video generation calls")
    args = p.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    summary = {"tests": []}

    tmp_img = OUT / "smoke_source.png"
    Image.new("RGB", (64, 64), (240, 80, 80)).save(tmp_img)

    payload = json.dumps({"data": [{"b64_json": base64.b64encode(tmp_img.read_bytes()).decode()}]})
    res = run([sys.executable, str(SCRIPTS / "fetch_generated_media.py"), "--response-text", payload, "--out-dir", str(OUT), "--prefix", "b64"])
    ensure(res["returncode"] == 0, f"b64 fetch failed: {res}")
    ensure(Path(res["stdout"].splitlines()[-1]).exists(), "b64 fetch output missing")
    summary["tests"].append({"name": "fetch_b64_json", "ok": True, "output": res["stdout"]})

    data_url = "data:image/png;base64," + base64.b64encode(tmp_img.read_bytes()).decode()
    res = run([sys.executable, str(SCRIPTS / "fetch_generated_media.py"), "--response-text", data_url, "--out-dir", str(OUT), "--prefix", "dataurl"])
    ensure(res["returncode"] == 0, f"data url fetch failed: {res}")
    ensure(Path(res["stdout"].splitlines()[-1]).exists(), "data url output missing")
    summary["tests"].append({"name": "fetch_data_url", "ok": True, "output": res["stdout"]})

    res = run([sys.executable, str(SCRIPTS / "mask_inpaint.py"), "--image", str(tmp_img), "--prompt", "replace the masked area with a blue circle", "--region", "rect:4:4:20:20", "--region", "ellipse-pct:50:50:30:30", "--expand", "2", "--feather", "4", "--mask-only", "--out-dir", str(OUT), "--prefix", "mask-smoke"])
    ensure(res["returncode"] == 0, f"mask generation failed: {res}")
    mask_path = Path(res["stdout"].splitlines()[-1])
    ensure(mask_path.exists(), "mask file was not created")
    summary["tests"].append({"name": "mask_multi_region_local", "ok": True, "output": str(mask_path)})

    alpha_img = OUT / "alpha_source.png"
    alpha_canvas = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    ImageDraw.Draw(alpha_canvas).ellipse((12, 12, 52, 52), fill=(255, 0, 0, 255))
    alpha_canvas.save(alpha_img)
    res = run([sys.executable, str(SCRIPTS / "prepare_object_mask.py"), "--image", str(alpha_img), "--mode", "alpha", "--threshold", "10", "--out", str(OUT / "alpha_object_mask.png")])
    ensure(res["returncode"] == 0, f"alpha object mask failed: {res}")
    ensure(Path(res["stdout"].splitlines()[-1]).exists(), "alpha object mask missing")
    summary["tests"].append({"name": "prepare_object_mask_alpha", "ok": True})

    bg_img = OUT / "corner_bg_source.png"
    canvas = Image.new("RGB", (64, 64), (250, 250, 250))
    ImageDraw.Draw(canvas).rectangle((18, 18, 46, 46), fill=(20, 120, 240))
    canvas.save(bg_img)
    res = run([sys.executable, str(SCRIPTS / "prepare_object_mask.py"), "--image", str(bg_img), "--mode", "corner-bg", "--threshold", "30", "--out", str(OUT / "corner_bg_mask.png")])
    ensure(res["returncode"] == 0, f"corner-bg object mask failed: {res}")
    ensure(Path(res["stdout"].splitlines()[-1]).exists(), "corner-bg object mask missing")
    summary["tests"].append({"name": "prepare_object_mask_corner_bg", "ok": True})

    res = run([sys.executable, str(SCRIPTS / "object_select_edit.py"), "--image", str(bg_img), "--prompt", "replace the selected object with a matte black cube", "--selection-mode", "corner-bg", "--edit-target", "object", "--prepare-only", "--prefix", "object-select-smoke", "--mask-dir", str(ROOT / "tmp" / "images" / "masks"), "--print-json"])
    ensure(res["returncode"] == 0, f"object_select_edit prepare-only failed: {res}")
    prepared = json.loads(res["stdout"])
    ensure(Path(prepared["mask"]).exists(), "object_select_edit mask missing")
    summary["tests"].append({"name": "object_select_edit_prepare_only", "ok": True})

    reference_manifest = OUT / "reference_batch_manifest.jsonl"
    reference_manifest.write_text(
        json.dumps({"mode": "image", "prompt": "reference still {subject}", "reference_image": str(bg_img), "nsfw": "false", "download": False}, ensure_ascii=False) + "\n" +
        json.dumps({"mode": "video", "prompt": "reference video {subject}", "reference_image": str(bg_img), "preset": "normal", "seconds": 6, "download": False}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    reference_batch_summary = OUT / "reference_batch_summary.json"
    res = run([sys.executable, str(SCRIPTS / "generate_batch_media.py"), "--manifest", str(reference_manifest), "--vars-json", json.dumps({"subject": "mug"}, ensure_ascii=False), "--summary-out", str(reference_batch_summary), "--dry-run", "--print-json"])
    ensure(res["returncode"] == 0, f"reference batch dry-run failed: {res}")
    ensure(reference_batch_summary.exists(), "reference batch summary was not written")
    reference_batch_data = json.loads(reference_batch_summary.read_text(encoding="utf-8"))
    ensure("reference_media.py" in " ".join(reference_batch_data["results"][0]["cmd"]), "reference batch image did not route to reference_media.py")
    ensure("--nsfw" in reference_batch_data["results"][0]["cmd"], "reference batch image did not forward nsfw")
    ensure("--preset" in reference_batch_data["results"][1]["cmd"], "reference batch video did not forward preset")
    summary["tests"].append({"name": "generate_batch_media_reference_routing", "ok": True})

    if args.live:
        res = run([sys.executable, str(SCRIPTS / "generate_image.py"), "--prompt", "studio product shot of a green pear, clean background, softbox lighting, centered composition, commercial photography, sharp detail", "--size", "1024x1024", "--out-dir", str(ROOT / "tmp" / "images"), "--prefix", "smoke-live-image", "--print-json"])
        ensure(res["returncode"] == 0, f"live image generation failed: {res}")
        summary["tests"].append({"name": "live_generate_image", "ok": True})

        res = run([sys.executable, str(SCRIPTS / "generate_image.py"), "--prompt", "studio product shot of a blue mug, clean background, centered composition", "--size", "1024x1024", "--nsfw", "false", "--out-dir", str(ROOT / "tmp" / "images"), "--prefix", "smoke-live-image-nsfw", "--print-json"])
        ensure(res["returncode"] == 0, f"live image generation with nsfw failed: {res}")
        image_nsfw = json.loads(res["stdout"])
        ensure(image_nsfw["request"].get("nsfw") is False, "live image generation did not send nsfw=false")
        summary["tests"].append({"name": "live_generate_image_nsfw", "ok": True})

        res = run([sys.executable, str(SCRIPTS / "generate_video.py"), "--prompt", "cinematic product video of a green pear, slow turntable rotation, soft studio lighting, stable motion, short polished clip", "--size", "720x1280", "--seconds", "6", "--out-dir", str(ROOT / "tmp" / "videos"), "--prefix", "smoke-live-video", "--print-json"])
        ensure(res["returncode"] == 0, f"live video generation failed: {res}")
        summary["tests"].append({"name": "live_generate_video", "ok": True})

        res = run([sys.executable, str(SCRIPTS / "generate_video.py"), "--prompt", "short product motion clip, gentle stable motion", "--size", "720x1280", "--seconds", "6", "--preset", "normal", "--out-dir", str(ROOT / "tmp" / "videos"), "--prefix", "smoke-live-video-preset", "--print-json"])
        ensure(res["returncode"] == 0, f"live video generation with preset failed: {res}")
        video_preset = json.loads(res["stdout"])
        ensure(video_preset["request"].get("preset") == "normal", "live video generation did not send preset=normal")
        summary["tests"].append({"name": "live_generate_video_preset", "ok": True})

        res = run([sys.executable, str(SCRIPTS / "reference_media.py"), "--mode", "image", "--reference-image", str(bg_img), "--prompt", "same subject identity still portrait", "--size", "1024x1024", "--nsfw", "false", "--out-dir", str(ROOT / "tmp" / "images"), "--prefix", "smoke-reference-image", "--print-json"])
        ensure(res["returncode"] == 0, f"live reference image failed: {res}")
        reference_image = json.loads(res["stdout"])
        ensure(reference_image["result"]["request"].get("nsfw") is False, "reference image flow did not forward nsfw=false")
        summary["tests"].append({"name": "live_reference_media_image", "ok": True})

        res = run([sys.executable, str(SCRIPTS / "reference_media.py"), "--mode", "video", "--reference-image", str(bg_img), "--prompt", "gentle natural motion, stable framing", "--size", "1280x720", "--seconds", "6", "--preset", "normal", "--out-dir", str(ROOT / "tmp" / "videos"), "--prefix", "smoke-reference-video", "--print-json"])
        ensure(res["returncode"] == 0, f"live reference video failed: {res}")
        reference_video = json.loads(res["stdout"])
        ensure(reference_video["result"]["request"].get("preset") == "normal", "reference video flow did not forward preset=normal")
        summary["tests"].append({"name": "live_reference_media_video", "ok": True})

        res = run([sys.executable, str(SCRIPTS / "generate_consistent_media.py"), "--mode", "image", "--reference-image", str(bg_img), "--prompt", "wrapper compatibility portrait", "--size", "1024x1024", "--nsfw", "false", "--out-dir", str(ROOT / "tmp" / "images"), "--prefix", "smoke-wrapper-compat", "--print-json"])
        ensure(res["returncode"] == 0, f"wrapper compatibility live call failed: {res}")
        wrapper_image = json.loads(res["stdout"])
        ensure(wrapper_image["result"]["request"].get("nsfw") is False, "wrapper compatibility flow did not forward nsfw=false")
        summary["tests"].append({"name": "live_wrapper_compat_reference_image", "ok": True})

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
