#!/usr/bin/env python3
"""Batch parse all documents in a folder with LlamaParse using async concurrency.

Usage:
    python batch_parse.py <input_dir> [options]

Options:
    --tier TIER              Parsing tier (default: agentic)
    --version VERSION        Tier version (default: latest)
    --output VIEWS           Comma-separated expand views (default: markdown,text)
    --max-concurrent N       Max concurrent parse operations (default: 5)
    --out-dir DIR            Output directory for results (default: <input_dir>_parsed)
    --extensions EXTS        Comma-separated file extensions to process (default: pdf,png,jpg,jpeg,docx,pptx,xlsx)

Requires:
    pip install llama-cloud>=1.0
    export LLAMA_CLOUD_API_KEY=llx-...
"""

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path


DEFAULT_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "docx", "pptx", "xlsx", "tiff", "bmp", "webp", "html", "csv"}


async def parse_single_file(client, file_path: Path, tier: str, version: str, expand: list, out_dir: Path, semaphore):
    async with semaphore:
        try:
            print(f"  ⏳ Starting: {file_path.name}")
            start = time.time()

            file_obj = await client.files.create(
                file=str(file_path),
                purpose="parse",
                external_file_id=str(file_path),
            )

            result = await client.parsing.parse(
                file_id=file_obj.id,
                tier=tier,
                version=version,
                expand=expand,
            )

            stem = file_path.stem
            elapsed = time.time() - start

            # Save markdown
            if "markdown" in expand and result.markdown:
                md_content = "\n\n---\n\n".join(
                    page.markdown for page in result.markdown.pages if page.markdown
                )
                (out_dir / f"{stem}.md").write_text(md_content)

            # Save text
            if "text" in expand and result.text:
                txt_content = "\n\n".join(
                    page.text for page in result.text.pages if page.text
                )
                (out_dir / f"{stem}.txt").write_text(txt_content)

            # Save items
            if "items" in expand and result.items:
                pages_data = []
                for page in result.items.pages:
                    page_items = []
                    for item in page.items:
                        item_dict = {"type": getattr(item, "type", "unknown")}
                        if hasattr(item, "md"):
                            item_dict["md"] = item.md
                        if hasattr(item, "rows"):
                            item_dict["rows"] = item.rows
                        page_items.append(item_dict)
                    pages_data.append({"page": page.page_number, "items": page_items})
                (out_dir / f"{stem}_items.json").write_text(json.dumps(pages_data, indent=2, default=str))

            page_count = 0
            if result.markdown and result.markdown.pages:
                page_count = len(result.markdown.pages)
            elif result.items and result.items.pages:
                page_count = len(result.items.pages)

            print(f"  ✅ Done: {file_path.name} ({page_count} pages, {elapsed:.1f}s)")
            return {"file": file_path.name, "status": "success", "pages": page_count, "time": elapsed}

        except Exception as e:
            print(f"  ❌ Error: {file_path.name} — {e}")
            return {"file": file_path.name, "status": "error", "error": str(e)}


async def batch_parse(
    input_dir: str,
    tier: str = "agentic",
    version: str = "latest",
    expand: list = None,
    max_concurrent: int = 5,
    out_dir: str = None,
    extensions: set = None,
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
    if extensions is None:
        extensions = DEFAULT_EXTENSIONS

    input_path = Path(input_dir)
    if not input_path.is_dir():
        print(f"Error: {input_dir} is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Collect files
    files = sorted([
        f for f in input_path.iterdir()
        if f.is_file() and f.suffix.lstrip(".").lower() in extensions
    ])

    if not files:
        print(f"No matching files found in {input_dir}")
        return

    # Setup output directory
    out_path = Path(out_dir) if out_dir else Path(f"{input_dir}_parsed")
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"📁 Found {len(files)} files to parse")
    print(f"⚙️  Tier: {tier}, Version: {version}, Expand: {expand}")
    print(f"📂 Output: {out_path}")
    print(f"🔄 Max concurrent: {max_concurrent}\n")

    client = AsyncLlamaCloud(api_key=api_key)
    semaphore = asyncio.Semaphore(max_concurrent)

    start_time = time.time()
    tasks = [
        parse_single_file(client, f, tier, version, expand, out_path, semaphore)
        for f in files
    ]
    results = await asyncio.gather(*tasks)

    total_time = time.time() - start_time
    successful = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "error")

    print(f"\n{'='*50}")
    print(f"📊 BATCH PARSE SUMMARY")
    print(f"{'='*50}")
    print(f"  Total files:  {len(files)}")
    print(f"  Successful:   {successful}")
    print(f"  Failed:       {failed}")
    print(f"  Total time:   {total_time:.1f}s")
    if successful > 0:
        print(f"  Avg per file: {total_time/successful:.1f}s")
    print(f"  Output dir:   {out_path}")

    if failed > 0:
        print(f"\n❌ Failed files:")
        for r in results:
            if r["status"] == "error":
                print(f"  - {r['file']}: {r['error']}")


def main():
    parser = argparse.ArgumentParser(description="Batch parse documents with LlamaParse")
    parser.add_argument("input_dir", help="Directory containing documents to parse")
    parser.add_argument("--tier", default="agentic", choices=["agentic_plus", "agentic", "cost_effective", "fast"])
    parser.add_argument("--version", default="latest")
    parser.add_argument("--output", default="markdown,text", help="Comma-separated expand views")
    parser.add_argument("--max-concurrent", type=int, default=5)
    parser.add_argument("--out-dir", help="Output directory (default: <input_dir>_parsed)")
    parser.add_argument("--extensions", default=None, help="Comma-separated file extensions")

    args = parser.parse_args()
    expand = [v.strip() for v in args.output.split(",")]
    extensions = {e.strip().lower() for e in args.extensions.split(",")} if args.extensions else None

    asyncio.run(batch_parse(
        input_dir=args.input_dir,
        tier=args.tier,
        version=args.version,
        expand=expand,
        max_concurrent=args.max_concurrent,
        out_dir=args.out_dir,
        extensions=extensions,
    ))


if __name__ == "__main__":
    main()
