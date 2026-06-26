from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys
import time

# Author: https://github.com/sawyer-shi


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.mind_map_generator import generate_mind_map


def _read_input(raw_input: str) -> tuple[str, Path | None]:
    candidate = Path(raw_input)
    if candidate.exists() and candidate.is_file():
        return candidate.read_text(encoding="utf-8"), candidate
    return raw_input, None


def _save_input_markdown(markdown_content: str, source_path: Path | None, output_dir: Path, filename: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    if source_path is not None:
        target_name = source_path.name
    elif filename:
        target_name = f"{filename}_input.md"
    else:
        target_name = f"mind_map_input_{int(time.time())}.md"

    if not target_name.lower().endswith(".md"):
        target_name += ".md"

    safe_name = "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "_" for ch in target_name)
    md_path = output_dir / safe_name

    if md_path.exists():
        stem = md_path.stem
        suffix = md_path.suffix
        md_path = output_dir / f"{stem}_{int(time.time())}{suffix}"

    md_path.write_text(markdown_content, encoding="utf-8")
    return md_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run mind map generation from file or inline markdown")
    parser.add_argument("--layout", choices=["free", "center", "horizontal"], default="free")
    parser.add_argument("--input", required=True, help="Markdown file path or inline markdown text")
    parser.add_argument("--filename", default="")
    parser.add_argument("--output-dir", default="mind_map_output")
    parser.add_argument("--flat-output", action="store_true", help="Write files directly to output-dir without YYYY-MM-DD subfolder")
    parser.add_argument("--download-md", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    if not args.flat_output:
        output_dir = output_dir / datetime.now().strftime("%Y-%m-%d")

    markdown_content, source_path = _read_input(args.input)
    input_md_path = _save_input_markdown(markdown_content, source_path, output_dir, args.filename)

    result = generate_mind_map(
        markdown_content=markdown_content,
        layout_type=args.layout,
        filename=args.filename or None,
        download_md=args.download_md,
        output_dir=str(output_dir),
    )
    result["input_markdown_path"] = str(input_md_path)
    print(result)


if __name__ == "__main__":
    main()
