#!/usr/bin/env python3
"""
批量像素素材生成+处理脚本
读取JSON配置文件，调用Seedream生图后自动处理为Godot可用格式
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# 默认Seedream生图脚本路径
DEFAULT_GENERATOR = r"D:\the things of mine\openclaw\workspace\lumi-work\脚本\生图\seedream_generate.py"
# 默认处理脚本路径（本skill目录下）
SCRIPT_DIR = Path(__file__).parent
DEFAULT_PROCESSOR = SCRIPT_DIR / "process_sprite_sheet.py"


def run_generator(prompt: str, output_path: str, negative: str, backend: str, generator_path: str) -> bool:
    """调用生图后端生成图片"""
    print(f"\n🎨 生成素材: {output_path}")
    print(f"   Prompt: {prompt[:80]}...")

    if backend == "seedream":
        if not os.path.exists(generator_path):
            print(f"错误：生图脚本不存在: {generator_path}")
            return False
        cmd = [sys.executable, generator_path, prompt, output_path, negative]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                print(f"   生图失败: {result.stderr[:200]}")
                return False
            if not os.path.exists(output_path):
                print(f"   生图失败：输出文件未生成")
                return False
            print(f"   ✅ 生成成功")
            return True
        except subprocess.TimeoutExpired:
            print(f"   生图超时（120s）")
            return False
        except Exception as e:
            print(f"   生图异常: {e}")
            return False
    else:
        print(f"警告：后端 '{backend}' 暂不支持自动生图，请手动生成后放到raw目录")
        return False


def run_processor(input_path: str, output_dir: str, target_size: int,
                  cols: int | None, bg_color: str, processor_path: str) -> bool:
    """调用处理脚本"""
    if not os.path.exists(processor_path):
        print(f"错误：处理脚本不存在: {processor_path}")
        return False

    cmd = [
        sys.executable, str(processor_path), input_path,
        "--output-dir", output_dir,
        "--target-size", str(target_size),
        "--bg-color", bg_color,
    ]
    if cols:
        cmd.extend(["--cols", str(cols)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        print(result.stdout)
        if result.returncode != 0:
            print(f"处理失败: {result.stderr[:200]}")
            return False
        return True
    except Exception as e:
        print(f"处理异常: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="批量生成并处理像素游戏素材",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
配置文件格式（JSON）:
{
  "output_base": "./game_assets",
  "backend": "seedream",
  "default_size": 48,
  "assets": [
    {"name": "slime", "category": "enemies", "prompt": "...", "cols": 4, "target_size": 48}
  ]
}
        """)
    parser.add_argument("config", help="JSON配置文件路径")
    parser.add_argument("--dry-run", action="store_true",
                        help="只显示将要执行的操作，不实际生成")
    parser.add_argument("--skip-generate", action="store_true",
                        help="跳过生图步骤，只处理已有的raw图片")
    parser.add_argument("--only", type=str, default=None,
                        help="只处理指定名称的素材（可多次使用）")
    parser.add_argument("--generator", default=DEFAULT_GENERATOR,
                        help=f"生图脚本路径（默认: {DEFAULT_GENERATOR}）")
    parser.add_argument("--processor", default=str(DEFAULT_PROCESSOR),
                        help=f"处理脚本路径（默认: {DEFAULT_PROCESSOR}）")

    args = parser.parse_args()

    # 加载配置
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"错误：配置文件不存在: {args.config}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    output_base = Path(config.get("output_base", "./game_assets"))
    backend = config.get("backend", "seedream")
    default_size = config.get("default_size", 48)
    default_bg = config.get("default_bg_color", "auto")
    assets = config.get("assets", [])

    if not assets:
        print("错误：配置文件中没有assets")
        sys.exit(1)

    print(f"📋 加载配置: {config_path}")
    print(f"   后端: {backend} | 输出目录: {output_base} | 默认帧尺寸: {default_size}")
    print(f"   素材数量: {len(assets)}")

    # 过滤
    if args.only:
        filter_names = set(args.only.split(","))
        assets = [a for a in assets if a["name"] in filter_names]
        print(f"   过滤后: {len(assets)}个素材")

    raw_dir = output_base / "_raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    fail_count = 0

    for i, asset in enumerate(assets, 1):
        name = asset["name"]
        category = asset.get("category", "uncategorized")
        prompt = asset["prompt"]
        negative = asset.get("negative_prompt", "")
        cols = asset.get("cols", None)
        target_size = asset.get("target_size", default_size)
        bg_color = asset.get("bg_color", default_bg)

        print(f"\n{'='*60}")
        print(f"[{i}/{len(assets)}] {name} ({category})")
        print(f"{'='*60}")

        if args.dry_run:
            print(f"  生图: {prompt[:60]}...")
            print(f"  处理: → {output_base}/{category}/{name}/")
            success_count += 1
            continue

        # 生图
        raw_path = raw_dir / f"{name}_raw.png"
        if not args.skip_generate and not raw_path.exists():
            if not run_generator(prompt, str(raw_path), negative, backend, args.generator):
                fail_count += 1
                continue
        elif raw_path.exists():
            print(f"  📁 已有原始图，跳过生图: {raw_path}")
        elif args.skip_generate:
            # 检查是否已有raw
            if not raw_path.exists():
                print(f"  ⚠️ 原始图不存在且跳过生图: {raw_path}")
                fail_count += 1
                continue

        # 处理
        out_dir = output_base / category / name
        if run_processor(str(raw_path), str(out_dir), target_size, cols, bg_color, args.processor):
            success_count += 1
        else:
            fail_count += 1

    # 汇总
    print(f"\n{'='*60}")
    print(f"✅ 完成！成功: {success_count} / 失败: {fail_count} / 总计: {len(assets)}")
    print(f"📁 输出目录: {output_base.resolve()}")
    if fail_count > 0:
        print(f"📁 原始图目录: {raw_dir.resolve()}（可检查失败的素材）")


if __name__ == "__main__":
    main()
