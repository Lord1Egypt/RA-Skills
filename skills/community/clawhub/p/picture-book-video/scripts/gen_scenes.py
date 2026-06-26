#!/usr/bin/env python3
"""
批量生成场景图片 - 从 scene_prompts.json 调用 ComfyUI

用法:
  python3 gen_scenes.py --prompts scene_prompts.json --output-dir ./scenes/
"""
import argparse
import json
import os
import subprocess
import sys

GENERATE_SCRIPT = os.path.expanduser(
    "~/.openclaw/workspace/skills/comfyui-image-video/scripts/generate.py"
)


def main():
    p = argparse.ArgumentParser(description="批量生成场景图片")
    p.add_argument("--prompts", required=True, help="scene_prompts.json 路径")
    p.add_argument("--output-dir", required=True, help="输出目录")
    p.add_argument("--skip-existing", action="store_true", help="跳过已存在的场景")
    args = p.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.prompts) as f:
        prompts = json.load(f)

    for item in prompts:
        scene = item["scene"]
        prompt = item["prompt"]
        output = os.path.join(args.output_dir, f"scene_{scene:02d}.png")

        if args.skip_existing and os.path.exists(output):
            print(f"⏭️  Scene {scene:02d} 已存在，跳过")
            continue

        print(f"\n🎬 Generating scene {scene:02d}...")
        print(f"   Prompt: {prompt[:80]}...")

        result = subprocess.run(
            [
                sys.executable,
                GENERATE_SCRIPT,
                "image",
                "--prompt",
                prompt,
                "--width",
                "1920",
                "--height",
                "1080",
                "--steps",
                "4",
                "--output",
                output,
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode == 0:
            print(f"   ✅ Scene {scene:02d} done")
        else:
            print(f"   ❌ Failed: {result.stderr[:200]}")
            sys.exit(1)

    print("\n✅ All scenes generated!")


if __name__ == "__main__":
    main()
