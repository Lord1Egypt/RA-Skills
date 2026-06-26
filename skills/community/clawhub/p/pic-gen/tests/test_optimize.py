#!/usr/bin/env python3
"""
pic-gen 测试套件
"""

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))

from optimize import (
    optimize_for_qwen,
    optimize_for_midjourney,
    optimize_for_stable_diffusion,
    optimize_for_flux,
    optimize_for_dalle,
)


def test_qwen():
    prompts = ["一只猫", "梵高风格的向日葵", "赛博朋克城市夜景"]
    for p in prompts:
        result = optimize_for_qwen(p)
        assert len(result) > len(p), f"qwen优化后不应变短: {result}"
        print(f"[qwen] ✓ {p!r} → {result!r}")


def test_midjourney():
    prompts = ["a cat on the moon", "sunflower field"]
    for p in prompts:
        result = optimize_for_midjourney(p)
        assert "--ar" in result, f"MJ 应包含 --ar: {result}"
        assert "--v" in result, f"MJ 应包含 --v: {result}"
        print(f"[midjourney] ✓ {p!r} → {result!r}")


def test_stable_diffusion():
    prompts = ["a cat", "beautiful landscape"]
    for p in prompts:
        pos, neg = optimize_for_stable_diffusion(p)
        assert len(pos) > len(p), f"SD正向不应变短"
        assert len(neg) > 0, f"SD应有negative prompt"
        print(f"[stable_diffusion] ✓ {p!r} → pos={pos[:60]!r}... neg={neg[:40]!r}...")


def test_flux():
    prompts = ["a cat", "cyberpunk city"]
    for p in prompts:
        result = optimize_for_flux(p)
        assert len(result) >= len(p), f"flux优化后不应变短"
        print(f"[flux] ✓ {p!r} → {result!r}")


def test_dalle():
    prompts = ["一只猫", "van gogh sunflower"]
    for p in prompts:
        result = optimize_for_dalle(p)
        assert len(result) >= len(p), f"dalle优化后不应变短"
        print(f"[dalle] ✓ {p!r} → {result!r}")


def main():
    print("=" * 60)
    print("Running pic-gen tests...")
    print("=" * 60)
    tests = [
        ("Qwen", test_qwen),
        ("Midjourney", test_midjourney),
        ("Stable Diffusion", test_stable_diffusion),
        ("Flux", test_flux),
        ("DALL-E", test_dalle),
    ]
    failed = 0
    for name, fn in tests:
        try:
            print(f"\n--- {name} ---")
            fn()
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            failed += 1

    print("\n" + "=" * 60)
    if failed:
        print(f"FAILED: {failed}/{len(tests)}")
        sys.exit(1)
    else:
        print(f"PASSED: all {len(tests)} tests")
        sys.exit(0)


if __name__ == "__main__":
    main()
