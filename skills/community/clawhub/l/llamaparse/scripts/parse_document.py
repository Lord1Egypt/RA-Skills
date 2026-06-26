#!/usr/bin/env python3
"""Parse a single document with LlamaParse and output results.

Usage:
    python parse_document.py <file_path> [options]

Options:
    --tier TIER          Parsing tier: agentic_plus|agentic|cost_effective|fast (default: agentic)
    --version VERSION    Tier version (default: latest)
    --output VIEWS       Comma-separated expand views: markdown,text,items,metadata (default: markdown,text)
    --prompt PROMPT      Custom parsing instruction/prompt
    --chart-parsing      Enable specialized chart parsing
    --save-screenshots   Save page screenshots to current directory
    --out-dir DIR        Output directory for results (default: current directory)

Requires:
    pip install llama-cloud>=1.0
    export LLAMA_CLOUD_API_KEY=llx-...
"""

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path


async def parse_document(
    file_path: str,
    tier: str = "agentic",
    version: str = "latest",
    expand: list[str] = None,
    custom_prompt: str = None,
    chart_parsing: bool = False,
    save_screenshots: bool = False,
    out_dir: str = ".",
):
    try:
        from llama_cloud import AsyncLlamaCloud
    except ImportError:
        print("Error: llama-cloud not installed. Run: pip install llama-cloud>=1.0", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("LLAMA_CLOUD_API_KEY")
    if not api_key:
        print("Error: LLAMA_CLOUD_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    if expand is None:
        expand = ["markdown", "text"]

    if save_screenshots and "images_content_metadata" not in expand:
        expand.append("images_content_metadata")

    client = AsyncLlamaCloud(api_key=api_key)

    # Build processing options
    processing_options = {}
    if chart_parsing:
        processing_options["specialized_chart_parsing"] = tier if tier in ("agentic", "agentic_plus") else "agentic"
    if custom_prompt:
        processing_options["auto_mode_configuration"] = [{
            "parsing_conf": {"custom_prompt": custom_prompt}
        }]

    # Build output options
    output_options = {}
    if save_screenshots:
        output_options["images_to_save"] = ["screenshot"]

    print(f"📄 Uploading {file_path}...")
    file_obj = await client.files.create(file=file_path, purpose="parse")

    print(f"⚙️  Parsing with tier={tier}, version={version}, expand={expand}...")
    parse_kwargs = {
        "file_id": file_obj.id,
        "tier": tier,
        "version": version,
        "expand": expand,
    }
    if processing_options:
        parse_kwargs["processing_options"] = processing_options
    if output_options:
        parse_kwargs["output_options"] = output_options

    result = await client.parsing.parse(**parse_kwargs)

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    stem = Path(file_path).stem

    # Save markdown
    if "markdown" in expand and result.markdown:
        md_file = out_path / f"{stem}_parsed.md"
        md_content = "\n\n---\n\n".join(
            page.markdown for page in result.markdown.pages if page.markdown
        )
        md_file.write_text(md_content)
        print(f"✅ Markdown saved to {md_file}")

    # Save text
    if "text" in expand and result.text:
        txt_file = out_path / f"{stem}_parsed.txt"
        txt_content = "\n\n".join(
            page.text for page in result.text.pages if page.text
        )
        txt_file.write_text(txt_content)
        print(f"✅ Text saved to {txt_file}")

    # Save items as JSON
    if "items" in expand and result.items:
        items_file = out_path / f"{stem}_items.json"
        pages_data = []
        for page in result.items.pages:
            page_items = []
            for item in page.items:
                item_dict = {"type": getattr(item, "type", "unknown")}
                if hasattr(item, "md"):
                    item_dict["md"] = item.md
                if hasattr(item, "rows"):
                    item_dict["rows"] = item.rows
                if hasattr(item, "csv"):
                    item_dict["csv"] = item.csv
                page_items.append(item_dict)
            pages_data.append({"page": page.page_number, "items": page_items})
        items_file.write_text(json.dumps(pages_data, indent=2, default=str))
        print(f"✅ Items saved to {items_file}")

    # Save screenshots
    if save_screenshots and hasattr(result, "images_content_metadata") and result.images_content_metadata:
        try:
            import httpx
        except ImportError:
            print("⚠️  httpx not installed, skipping screenshots. Run: pip install httpx")
        else:
            screenshots_dir = out_path / f"{stem}_screenshots"
            screenshots_dir.mkdir(exist_ok=True)
            count = 0
            async with httpx.AsyncClient() as http:
                for img in result.images_content_metadata.images:
                    if img.presigned_url and re.match(r"^page_\d+\.jpg$", img.filename):
                        resp = await http.get(img.presigned_url)
                        (screenshots_dir / img.filename).write_bytes(resp.content)
                        count += 1
            print(f"✅ {count} screenshots saved to {screenshots_dir}/")

    page_count = 0
    if result.markdown and result.markdown.pages:
        page_count = len(result.markdown.pages)
    elif result.text and result.text.pages:
        page_count = len(result.text.pages)
    elif result.items and result.items.pages:
        page_count = len(result.items.pages)

    print(f"\n📊 Done! Parsed {page_count} pages from {file_path}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Parse a document with LlamaParse")
    parser.add_argument("file_path", help="Path to the document to parse")
    parser.add_argument("--tier", default="agentic", choices=["agentic_plus", "agentic", "cost_effective", "fast"])
    parser.add_argument("--version", default="latest")
    parser.add_argument("--output", default="markdown,text", help="Comma-separated expand views")
    parser.add_argument("--prompt", help="Custom parsing instruction")
    parser.add_argument("--chart-parsing", action="store_true", help="Enable specialized chart parsing")
    parser.add_argument("--save-screenshots", action="store_true")
    parser.add_argument("--out-dir", default=".", help="Output directory")

    args = parser.parse_args()
    expand = [v.strip() for v in args.output.split(",")]

    asyncio.run(parse_document(
        file_path=args.file_path,
        tier=args.tier,
        version=args.version,
        expand=expand,
        custom_prompt=args.prompt,
        chart_parsing=args.chart_parsing,
        save_screenshots=args.save_screenshots,
        out_dir=args.out_dir,
    ))


if __name__ == "__main__":
    main()
