#!/usr/bin/env python3
"""
kb-digest: 知识提炼器
任意链接/PDF/文字 → 结构化知识卡片
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass


def build_llm_config(api_key: str = None, base_url: str = None, model: str = None) -> dict:
    api_key = api_key or os.getenv("OPENCLAW_LLM_API_KEY")
    if not api_key:
        raise RuntimeError("未检测到 LLM 配置，请通过 OpenClaw 运行或传入 --llm-api-key")
    base_url = (base_url or os.getenv("OPENCLAW_LLM_BASE_URL", "")).rstrip("/")
    if not base_url:
        raise RuntimeError("未检测到 LLM 地址，请通过 OpenClaw 运行或传入 --llm-base-url")
    model_raw = model or os.getenv("OPENCLAW_LLM_MODEL", "")
    model = model_raw.split("/")[-1]
    if not model:
        raise RuntimeError("未检测到 LLM 模型，请通过 OpenClaw 运行或传入 --llm-model")
    return {"api_key": api_key, "base_url": base_url, "model": model}


def fetch_url(url: str) -> str:
    import requests

    if "arxiv.org/abs/" in url:
        resp = requests.get(url, timeout=15)
        from markdownify import markdownify as md
        return md(resp.text, strip=["script", "style"])[:8000]

    headers = {"User-Agent": "Mozilla/5.0 (compatible; kb-digest/1.0)"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    try:
        from markdownify import markdownify as md
        content = md(resp.text, strip=["script", "style", "nav", "footer"])
    except ImportError:
        import re
        content = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", resp.text))
    return content[:8000]


def fetch_pdf(path: str) -> str:
    try:
        import pypdf
        reader = pypdf.PdfReader(path)
        pages = [page.extract_text() for page in reader.pages[:20]]
        return "\n".join(p for p in pages if p)[:8000]
    except ImportError:
        raise RuntimeError("请安装 pypdf: pip install pypdf")


def digest(content: str, source_name: str, output_type: str, cfg: dict) -> str:
    prompts = {
        "card": f"""将以下内容提炼为结构化知识卡片，用中文输出。

格式严格按照:
---
📚 知识卡片 | [标题]

💡 一句话
  [核心内容，20字内]

🔑 核心要点
  1. [要点1]
  2. [要点2]
  3. [要点3]
  （最多5条）

❓ Q&A
  Q: [问题1]
  A: [回答1]

  Q: [问题2]
  A: [回答2]

🧠 思维导图（Markdown 树形）
  主题
  ├── 子主题1
  │   └── 细节
  └── 子主题2

🔗 延伸阅读
  [相关概念或资源]

来源: {source_name}
生成: {datetime.now().strftime("%Y-%m-%d %H:%M")}
---

内容:
{content[:4000]}""",

        "summary": f"用中文写一份300字以内的摘要，提炼最重要的信息:\n\n{content[:4000]}",

        "qa": f"""从以下内容中提取10个最有价值的问答对，中文输出，JSON格式:
[{{"q": "问题", "a": "回答"}}, ...]

内容:
{content[:4000]}""",

        "mindmap": f"""将以下内容整理为思维导图，Markdown 树形结构，中文输出:

内容:
{content[:4000]}""",

        "podcast": f"""将以下内容改写为一段轻松的播客对话脚本，两位主持人（A/B），中文输出，300-500字:

内容:
{content[:4000]}""",
    }

    import requests as _req
    resp = _req.post(
        f"{cfg['base_url']}/chat/completions",
        headers={"Authorization": f"Bearer {cfg['api_key']}", "Content-Type": "application/json"},
        json={
            "model": cfg["model"],
            "messages": [{"role": "user", "content": prompts.get(output_type, prompts["card"])}],
            "temperature": 0.3,
            "max_tokens": 1500,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def process_batch(file_path: str, output_type: str, cfg: dict):
    urls = [u.strip() for u in Path(file_path).read_text().splitlines()
            if u.strip() and not u.startswith("#")]
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] {url}")
        try:
            result = digest(fetch_url(url), url, output_type, cfg)
            print(result)
            out_file = Path(f"digest_{i:02d}.md")
            out_file.write_text(result)
            print(f"  → 已保存: {out_file}")
        except Exception as e:
            print(f"  ❌ 失败: {e}")


def push_feishu(content: str):
    url = os.getenv("FEISHU_WEBHOOK_URL")
    if not url:
        print("⚠️  未设置 FEISHU_WEBHOOK_URL")
        return
    import requests
    requests.post(url, json={"msg_type": "text", "content": {"text": content}})
    print("✅ 已推送到飞书")


def main():
    parser = argparse.ArgumentParser(
        description="kb-digest: 任意内容 → 结构化知识卡片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python handler.py --url "https://arxiv.org/abs/1706.03762"
  python handler.py --pdf paper.pdf
  python handler.py --text "把这段话提炼一下..."
  python handler.py --url "..." --output mindmap
  python handler.py --url "..." --output podcast
  python handler.py --batch urls.txt
        """,
    )

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--url", help="网页 URL")
    source.add_argument("--pdf", help="PDF 文件路径")
    source.add_argument("--text", help="直接输入文本")
    source.add_argument("--batch", help="批量处理：包含多个 URL 的文件")

    parser.add_argument("--output", choices=["card", "summary", "qa", "mindmap", "podcast"],
                        default="card", help="输出格式（默认: card 知识卡片）")
    parser.add_argument("--push", choices=["feishu"], help="推送渠道")
    parser.add_argument("--save", help="保存到文件路径（如 output.md）")

    llm_group = parser.add_argument_group("LLM 配置（覆盖 OPENCLAW_LLM_* 环境变量）")
    llm_group.add_argument("--llm-api-key", help="LLM API Key")
    llm_group.add_argument("--llm-base-url", help="LLM API 地址")
    llm_group.add_argument("--llm-model", help="模型标识")

    args = parser.parse_args()

    try:
        cfg = build_llm_config(
            api_key=args.llm_api_key,
            base_url=args.llm_base_url,
            model=args.llm_model,
        )
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)

    if args.batch:
        process_batch(args.batch, args.output, cfg)
        return

    print("  正在获取内容...", end="", flush=True)
    try:
        if args.url:
            content, source_name = fetch_url(args.url), args.url
        elif args.pdf:
            content, source_name = fetch_pdf(args.pdf), args.pdf
        else:
            content, source_name = args.text, "用户输入"
        print(" 完成")
    except Exception as e:
        print(f" 失败\n❌ {e}")
        sys.exit(1)

    print(f"  AI 提炼中（{args.output}）...", end="", flush=True)
    try:
        result = digest(content, source_name, args.output, cfg)
        print(" 完成\n")
    except Exception as e:
        print(f" 失败\n❌ {e}")
        sys.exit(1)

    print(result)

    if args.save:
        Path(args.save).write_text(result)
        print(f"\n✅ 已保存到 {args.save}")

    if args.push == "feishu":
        push_feishu(result)


if __name__ == "__main__":
    main()
