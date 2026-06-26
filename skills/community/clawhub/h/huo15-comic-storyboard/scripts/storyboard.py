"""分镜关键帧生成（Seedream 4.0 图生图 + 多图参考）."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import requests

HERE = pathlib.Path(__file__).resolve()
# _shared/ 定位：优先 bundled（scripts/_shared/），fallback monorepo 根
for _cand in (HERE.parent / "_shared", HERE.parents[2] / "_shared"):
    if (_cand / "config.py").exists():
        sys.path.insert(0, str(_cand))
        break

from ark_api import ArkClient
from config import STYLE_PRESETS, PRICING, DEFAULTS
from cost_guard import CostGuard
from checkpoint import Checkpoint


MAX_REF = 4  # Seedream 4.0 最多 4 张参考图


def build_prompt(style: str, scene: dict) -> str:
    preset = STYLE_PRESETS.get(style, {})
    prefix = preset.get("prefix", "")
    lighting = preset.get("lighting", "")
    return (
        f"{prefix}，{scene.get('location', '')}，{scene.get('time', '')}。"
        f"{scene.get('action', '')}。"
        f"{scene.get('camera', '')}。"
        f"{scene.get('mood', '')}氛围。{lighting}。"
        f"竖屏构图，9:16。"
    )


def pick_refs(char_ids: list[str], char_manifest: dict) -> list[str]:
    refs = []
    for cid in char_ids[:MAX_REF]:
        info = char_manifest.get(cid, {})
        for img in info.get("images", []):
            if "_full." in img:
                refs.append(img)
                break
    return refs


def download(url: str, path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, stream=True)
    with open(path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--script", required=True)
    p.add_argument("--char-dir", required=True)
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    script = json.loads(pathlib.Path(args.script).read_text())
    char_manifest = json.loads(
        (pathlib.Path(args.char_dir) / "manifest.json").read_text()
    )
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    project_dir = out_dir.parent
    guard = CostGuard.load(project_dir)
    cp = Checkpoint(project_dir)

    client = ArkClient()
    style = script.get("style", DEFAULTS["style"])
    manifest: dict = {}

    for scene in script.get("scenes", []):
        sid = scene["id"]
        out = out_dir / f"{sid}.png"
        if out.exists() or cp.sub_done("storyboard", sid):
            print(f"  ⏭️  {sid} 已完成")
            manifest[sid] = {"path": str(out)}
            continue

        prompt = build_prompt(style, scene)
        refs = pick_refs(scene.get("characters", []), char_manifest)
        print(f"  🎞️  {sid}: {prompt[:50]}... (refs={len(refs)})")

        for attempt in range(DEFAULTS["scene_retry"] + 1):
            try:
                url = client.generate_image(
                    prompt=prompt,
                    reference_images=refs,
                    size="768x1344",
                )
                download(url, out)
                break
            except Exception as e:
                if attempt == DEFAULTS["scene_retry"]:
                    print(f"  ❌ {sid} 多次失败: {e}")
                    raise
                print(f"  ↻ {sid} 重试 {attempt+1}")

        guard.charge("storyboard", sid, PRICING["image_per_pic"])
        cp.sub_mark("storyboard", sid)
        manifest[sid] = {"path": str(out), "prompt": prompt}

    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2)
    )
    print(f"✅ 分镜: {len(manifest)} 张")
    return 0


if __name__ == "__main__":
    sys.exit(main())
