#!/usr/bin/env python3
"""Build a GPT review prompt from the standardized template.

Usage:
    python3 scripts/build_prompt.py \
      --article /path/to/article.md \
      --output /tmp/gpt_prompt.txt \
      --context 播客

    python3 scripts/build_prompt.py \
      --article /path/to/article.md \
      --output /tmp/gpt_prompt.txt \
      --context "B站视频" \
      --dimensions all
"""

import argparse
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(SCRIPT_DIR, "..", "references", "prompt-template.md")


def get_context_suffix(context):
    """Return platform-specific extra instructions."""
    extras = {
        "播客": """
### 平台特性：播客
- 听众无法回看/回听，听不懂就过去了
- 术语必须翻译成口语
- 过渡比结构更重要：段落之间的桥接决定听众能不能跟上
""",
        "B站视频": """
### 平台特性：B站视频
- 观众可以暂停/回看，技术事实必须经得起验证
- 观众会验证截图内容和数据
- B站技术用户非常较真，编造或模糊细节会翻车
- 前15秒决定完播率
- 参赛作品需要体现"真实搭建"而非"纯讲故事"
""",
    }
    return extras.get(context, "")


def main():
    parser = argparse.ArgumentParser(description="Build GPT review prompt from template")
    parser.add_argument("--article", required=True, help="Path to article file")
    parser.add_argument("--output", required=True, help="Output prompt file")
    parser.add_argument("--context", default="文章",
                        help="Content type: 播客/B站视频/文章 (default: 文章)")
    parser.add_argument("--template", default=DEFAULT_TEMPLATE,
                        help=f"Template file (default: {DEFAULT_TEMPLATE})")
    parser.add_argument("--dimensions", default="all",
                        help="Dimensions to include: all/fact/reader/takeaway/viral/antislop")
    args = parser.parse_args()

    # Read article
    with open(args.article, "r") as f:
        article_text = f.read()

    # Read template
    template_path = args.template
    if not os.path.exists(template_path):
        print(f"Error: Template not found at {template_path}")
        import sys
        sys.exit(1)

    with open(template_path, "r") as f:
        template = f.read()

    # Build prompt
    prompt = template.replace("{{ARTICLE}}", article_text)
    prompt = prompt.replace("{{CONTEXT}}", args.context)

    # Add platform-specific suffix
    suffix = get_context_suffix(args.context)
    if suffix:
        prompt += suffix

    # Write output
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        f.write(prompt)

    print(f"Prompt written to {args.output} ({len(prompt)} chars)")


if __name__ == "__main__":
    main()
