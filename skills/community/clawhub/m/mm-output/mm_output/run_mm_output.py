#!/usr/bin/env python3
"""
Run PosterGen with Multi-modal Output Support

This is an enhanced version of run.py that includes MMOutput integration.
It provides all the functionality of the original run.py plus multi-modal output generation.
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from parser_unit import PosterGenParserUnit
from renderer_unit import PosterGenRendererUnit
from integrate import add_mm_output_args, generate_mm_outputs

import os
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Parse a PDF or Markdown to extract text/assets, render a preview, and generate multi-modal outputs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pdf_path", type=str, help="Path to the PDF file.")
    group.add_argument("--md_path", type=str, help="Path to the Markdown (.md) file.")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the output.")
    parser.add_argument("--render_mode", type=str, default="llm", choices=["llm", "simple"], help="Render mode: 'llm' (default) or 'simple'.")
    parser.add_argument("--text_model", type=str, default=None, help="Text model name, e.g. gpt-4.1-2025-04-14.")
    parser.add_argument("--temperature", type=float, default=None, help="LLM temperature (default 0.7).")
    parser.add_argument("--max_tokens", type=int, default=16384, help="Max tokens for LLM output.")
    parser.add_argument("--max_attempts", type=int, default=None, help="Max retry attempts for LLM generation.")
    parser.add_argument("--template", type=str, default=None, help="Template path or name. Overrides POSTER_TEMPLATE env var.")
    
    add_mm_output_args(parser)
    args = parser.parse_args()
    
    if args.pdf_path and not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found at {args.pdf_path}")
        sys.exit(1)
    if args.md_path and not os.path.exists(args.md_path):
        print(f"Error: Markdown file not found at {args.md_path}")
        sys.exit(1)
    
    parser_unit = PosterGenParserUnit()
    if args.pdf_path:
        parser_results = parser_unit.parse(args.pdf_path, args.output_dir)
    else:
        parser_results = parser_unit.parse_markdown(args.md_path, args.output_dir)
    
    renderer_unit = PosterGenRendererUnit()
    selected_template = args.template or os.getenv("POSTER_TEMPLATE")
    html_path = renderer_unit.render(
        parser_results,
        args.output_dir,
        mode=args.render_mode,
        model_id=args.text_model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        max_attempts=args.max_attempts,
        template_name=selected_template
    )
    
    if not html_path:
        print("Warning: HTML rendering returned None")
        return
    
    results = generate_mm_outputs(html_path, args.output_dir, args)
    if results:
        print("Done.")


if __name__ == "__main__":
    main()
