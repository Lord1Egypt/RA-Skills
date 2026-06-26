import argparse
import os
from dotenv import load_dotenv

from parser_unit import PosterGenParserUnit
from renderer_unit import PosterGenRendererUnit
from mm_output.integrate import add_mm_output_args, generate_mm_outputs
from paper2slides import generate_poster_image, generate_slides_images, generate_xhs_slides

load_dotenv()


def run_paper2slides(output_type, parser_results, args):
    """Run Paper2Slides pipeline for image/slides generation."""
    generators = {
        "poster_image": generate_poster_image,
        "slides_image": generate_slides_images,
        "xhs_slides": generate_xhs_slides,
    }
    
    gen = generators[output_type]
    
    # Build kwargs based on output type
    kwargs = {
        "parser_results": parser_results,
        "output_dir": args.output_dir,
        "style": args.style,
        "text_model": args.text_model,
        "language": args.language,
    }
    
    if output_type == "poster_image":
        kwargs["density"] = args.density
    else:
        kwargs["slides_length"] = args.slides_length
    
    result = gen(**kwargs)
    
    print(f"\n[Paper2Slides] {output_type} generation complete.")
    print(f"  Status: {result['status']}")
    print(f"  Output dir: {result['output_dir']}")
    print(f"  Images: {result['num_images']}")
    if result.get("html_path"):
        print(f"  XHS HTML: {result['html_path']}")
    if result.get("pdf_path"):
        print(f"  Slides PDF: {result['pdf_path']}")
    for img_path in result.get("images", []):
        print(f"  - {img_path}")


def main():
    parser = argparse.ArgumentParser(description="Parse a PDF or Markdown to extract text/assets, then render a preview.")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pdf_path", type=str, help="Path to the PDF file.")
    group.add_argument("--md_path", type=str, help="Path to the Markdown (.md) file.")
    
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the output.")
    parser.add_argument("--render_mode", type=str, default="llm", choices=["llm", "simple"], help="Render mode: 'llm' (default) or 'simple'.")
    parser.add_argument("--text_model", type=str, default=None, help="Text model name, e.g. gpt-4.1-2025-04-14. If unset, will use env TEXT_MODEL or default.")
    parser.add_argument("--temperature", type=float, default=None, help="LLM temperature (default 0.7).")
    parser.add_argument("--max_tokens", type=int, default=16384, help="Max tokens for LLM output (default 8192).")
    parser.add_argument("--max_attempts", type=int, default=None, help="Max retry attempts for LLM generation (default 3).")
    parser.add_argument("--template", type=str, default=None, help="Specific template path or name to use. Overrides POSTER_TEMPLATE env var.")
    parser.add_argument("--output_type", type=str, default="html",
                        choices=["html", "poster_image", "slides_image", "xhs_slides"],
                        help="Output type: 'html' (default), 'poster_image', 'slides_image' (landscape 16:9), 'xhs_slides' (vertical 9:16 + XHS HTML with copywriting).")
    parser.add_argument("--style", type=str, default="academic",
                        choices=["academic", "doraemon", "minimal"],
                        help="Visual style for poster_image/slides_image (default: academic).")
    parser.add_argument("--density", type=str, default="medium",
                        choices=["sparse", "medium", "dense"],
                        help="Content density for poster_image (default: medium).")
    parser.add_argument("--slides_length", type=str, default="medium",
                        choices=["short", "medium", "long"],
                        help="Slide count for slides_image: short=5-8, medium=8-12, long=12-15.")
    parser.add_argument("--language", type=str, default="auto",
                        choices=["auto", "zh", "en"],
                        help="Language for output: 'auto' (default, match input content), 'zh' (Chinese), 'en' (English).")
    
    add_mm_output_args(parser)
    args = parser.parse_args()

    # Validate input files
    if args.pdf_path and not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found at {args.pdf_path}")
        exit(1)
    if args.md_path and not os.path.exists(args.md_path):
        print(f"Error: Markdown file not found at {args.md_path}")
        exit(1)

    # Step 1: Parse input
    unit = PosterGenParserUnit()
    results = unit.parse(args.pdf_path, args.output_dir) if args.pdf_path else unit.parse_markdown(args.md_path, args.output_dir)
    
    print("\nParsing complete.")
    print(f"Results saved in {os.path.abspath(args.output_dir)}")
    print(f"  - Markdown text: {results['raw_text_path']}")
    print(f"  - Figures JSON: {results['figures_path']} ({results['figure_count']} figures)")
    print(f"  - Tables JSON: {results['tables_path']} ({results['table_count']} tables)")

    # Branch: Paper2Slides pipeline
    if args.output_type in ("poster_image", "slides_image", "xhs_slides"):
        run_paper2slides(args.output_type, results, args)
        return

    # Step 2: Render to HTML
    renderer = PosterGenRendererUnit()
    
    template = args.template or os.getenv("POSTER_TEMPLATE")
    print(f"Template selection: '{template}'" if template else "Template selection: None (will render all available templates)")

    html = renderer.render(
        results,
        args.output_dir,
        mode=args.render_mode,
        model_id=args.text_model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        max_attempts=args.max_attempts,
        template_name=template
    )

    if html:
        print("\nRendering complete.")
        paths = html if isinstance(html, list) else [html]
        for p in paths:
            print(f"  - HTML Output: {p}")

        # Step 4: Multi-modal output
        for p in paths:
            generate_mm_outputs(p, args.output_dir, args)


if __name__ == "__main__":
    main()
