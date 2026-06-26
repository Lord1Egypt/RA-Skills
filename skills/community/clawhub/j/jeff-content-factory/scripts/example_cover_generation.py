#!/usr/bin/env python3
"""
Example usage of GLM-Image cover photo generator
Demonstrates different use cases and prompt styles
"""

import os
import subprocess
import sys
from pathlib import Path

# Example configurations for different article types
EXAMPLES = [
    {
        "name": "AI Enterprise Article",
        "title": "Claude Cowork企业部署完全指南",
        "theme": "AI企业自动化与协作",
        "style": "professional corporate",
        "color_scheme": "deep blue gradient",
        "output": "example-ai-enterprise-cover.png",
    },
    {
        "name": "Tech Trend Article",
        "title": "2026年AI代理发展趋势预测",
        "theme": "AI技术趋势与市场分析",
        "style": "futuristic tech",
        "color_scheme": "blue and cyan gradient",
        "output": "example-tech-trend-cover.png",
    },
    {
        "name": "Tutorial Article",
        "title": "零基础学会使用AI工具提升效率",
        "theme": "AI工具入门教程",
        "style": "friendly approachable",
        "color_scheme": "light blue and white",
        "output": "example-tutorial-cover.png",
    },
    {
        "name": "Case Study Article",
        "title": "某企业如何用AI节省70%人力成本",
        "theme": "AI企业案例研究",
        "style": "professional data-driven",
        "color_scheme": "blue with data visualization elements",
        "output": "example-case-study-cover.png",
    },
]


def run_example(example: dict, api_key: str, output_dir: str = "output/examples"):
    """Run a single example cover generation"""
    print("\n" + "=" * 70)
    print(f"📸 Example: {example['name']}")
    print("=" * 70)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, example["output"])

    # Build command
    cmd = [
        "python",
        "scripts/generate_cover_photo.py",
        "--title",
        example["title"],
        "--theme",
        example["theme"],
        "--style",
        example["style"],
        "--color-scheme",
        example["color_scheme"],
        "--output",
        output_path,
        "--api-key",
        api_key,
    ]

    # Run command
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        print(e.stderr)
        return False


def main():
    # Check for API key
    api_key = os.environ.get("GLM_API_KEY")
    if not api_key:
        print("❌ Error: GLM_API_KEY environment variable not set")
        print("\nPlease set your API key:")
        print("  export GLM_API_KEY='your-api-key-here'")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("🎨 GLM-Image Cover Photo Generator - Examples")
    print("=" * 70)
    print(f"\nGenerating {len(EXAMPLES)} example cover photos...")

    # Run all examples
    results = []
    for example in EXAMPLES:
        success = run_example(example, api_key)
        results.append((example["name"], success))

    # Summary
    print("\n" + "=" * 70)
    print("📊 Summary")
    print("=" * 70)
    successful = sum(1 for _, success in results if success)
    print(f"\n✅ Successful: {successful}/{len(EXAMPLES)}")

    if successful < len(EXAMPLES):
        print(f"❌ Failed: {len(EXAMPLES) - successful}/{len(EXAMPLES)}")
        print("\nFailed examples:")
        for name, success in results:
            if not success:
                print(f"  - {name}")

    print("\n" + "=" * 70)
    print("✅ Examples completed!")
    print("   Check output/examples/ directory for generated covers")
    print("=" * 70)


if __name__ == "__main__":
    main()
