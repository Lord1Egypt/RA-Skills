"""生成角色三联卡（Seedream 4.0）."""
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
from config import STYLE_PRESETS, PRICING
from cost_guard import CostGuard


VIEWS = [
    ("full",  "角色全身立绘，站姿，居中构图，纯色背景", "1024x1792"),
    ("close", "角色半身特写，肩部以上，正面，柔光", "1024x1024"),
    ("chibi", "Q 版头像，简化版，圆润可爱风格", "1024x1024"),
]


def build_prompt(style: str, char: dict, view_desc: str) -> str:
    preset = STYLE_PRESETS.get(style, {})
    prefix = preset.get("prefix", "")
    palette = preset.get("palette", "")
    return (
        f"{prefix}，{view_desc}。"
        f"{char.get('visual', '')}，"
        f"{char.get('personality', '')}气质。"
        f"{palette}。高质量，精细线条。"
    )


def download(url: str, path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, stream=True)
    with open(path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--script", required=True)
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    script = json.loads(pathlib.Path(args.script).read_text())
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    style = script.get("style", "三渲二国风")
    characters = script.get("characters", [])

    project_dir = out_dir.parent
    guard = CostGuard.load(project_dir)

    client = ArkClient()
    manifest: dict = {}

    for char in characters:
        cid = char["id"]
        imgs = []
        for view_name, view_desc, size in VIEWS:
            out = out_dir / f"{cid}_{view_name}.png"
            if out.exists():
                print(f"  ⏭️  {out.name} 已存在")
                imgs.append(str(out))
                continue
            prompt = build_prompt(style, char, view_desc)
            print(f"  🎨 {cid}/{view_name}: {prompt[:60]}...")
            url = client.generate_image(prompt=prompt, size=size)
            download(url, out)
            imgs.append(str(out))
            guard.charge("characters", f"{cid}_{view_name}", PRICING["image_per_pic"])
        manifest[cid] = {"name": char.get("name", cid), "images": imgs}

    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2)
    )
    print(f"✅ 角色卡: {len(characters)} 人 × 3 张 = {len(characters)*3} 张")
    return 0


if __name__ == "__main__":
    sys.exit(main())
