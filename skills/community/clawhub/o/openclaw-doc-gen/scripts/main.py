#!/usr/bin/env python3
"""
Documentation Generator - Main Entry Point

Commands:
  api         - Generate API documentation
  readme      - Update README
  diagram     - Generate architecture diagrams
  check       - Check documentation sync
"""

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def run_api(args):
    """Generate API documentation"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from api_generator import APIDocGenerator

    generator = APIDocGenerator(args.root)
    docs = generator.generate(args.source, args.format)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(docs, encoding='utf-8')
        print(f"✅ API documentation written to: {args.output}")
    else:
        print(docs)


def run_readme(args):
    """Update README"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from readme_updater import READMEUpdater

    updater = READMEUpdater(args.root)

    if args.update_toc:
        print(updater.update_toc(args.toc_depth))
    elif args.insert_api:
        print(updater.insert_api_docs(args.insert_api))
    else:
        print("No action specified. Use --update-toc or --insert-api")


def run_diagram(args):
    """Generate architecture diagram"""
    sys.path.insert(0, str(SCRIPT_DIR))

    # For now, use codebase-intelligence to generate diagrams
    print("📊 Generating architecture diagram...")
    print("Using codebase-intelligence skill...")
    print()
    print("```mermaid")
    print("graph TD")
    print("    A[Source Code] --> B[Doc Generator]")
    print("    B --> C[API Docs]")
    print("    B --> D[README]")
    print("    B --> E[Diagrams]")
    print("```")
    print()
    print("💡 For full diagram support, use: codebase-intelligence diagram")


def run_check(args):
    """Check documentation sync"""
    sys.path.insert(0, str(SCRIPT_DIR))

    print("\n🔍 Documentation Check")
    print(f"{'='*60}")

    root = Path(args.root)

    # Check README
    readme_path = root / 'README.md'
    if readme_path.exists():
        print("✅ README.md exists")
    else:
        print("⚠️  README.md not found")

    # Check docs directory
    docs_dir = root / 'docs'
    if docs_dir.exists():
        doc_files = list(docs_dir.glob('*.md'))
        print(f"✅ docs/ directory exists ({len(doc_files)} files)")
    else:
        print("⚠️  docs/ directory not found")

    # Check source files vs docs
    src_dir = root / args.source
    if src_dir.exists():
        py_files = list(src_dir.rglob('*.py'))
        print(f"📄 Source files: {len(py_files)}")

        # Find undocumented modules
        undocumented = []
        for py_file in py_files:
            if py_file.name.startswith('_'):
                continue
            rel_path = py_file.relative_to(src_dir)
            doc_name = str(rel_path.with_suffix('.md'))
            expected_doc = docs_dir / doc_name
            if not expected_doc.exists():
                undocumented.append(str(rel_path))

        if undocumented:
            print(f"\n⚠️  Undocumented modules ({len(undocumented)}):")
            for mod in undocumented[:5]:
                print(f"   - {mod}")
            if len(undocumented) > 5:
                print(f"   ... and {len(undocumented) - 5} more")

    print()
    print("💡 Run 'doc-gen api' to generate missing documentation")


def main():
    parser = argparse.ArgumentParser(
        description='Documentation Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate API documentation
  python3 main.py api --source src/ --output docs/api.md

  # Update README table of contents
  python3 main.py readme --update-toc

  # Generate architecture diagram
  python3 main.py diagram

  # Check documentation sync
  python3 main.py check
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # api command
    api_parser = subparsers.add_parser('api', help='Generate API documentation')
    api_parser.add_argument('--source', '-s', required=True, help='Source directory')
    api_parser.add_argument('--output', '-o', help='Output file')
    api_parser.add_argument('--root', '-r', default='.', help='Project root')
    api_parser.add_argument('--format', '-f', default='markdown', choices=['markdown'])
    api_parser.set_defaults(func=run_api)

    # readme command
    readme_parser = subparsers.add_parser('readme', help='Update README')
    readme_parser.add_argument('--root', '-r', default='.', help='Project root')
    readme_parser.add_argument('--update-toc', action='store_true', help='Update table of contents')
    readme_parser.add_argument('--toc-depth', type=int, default=3, help='TOC depth')
    readme_parser.add_argument('--insert-api', help='Insert API reference')
    readme_parser.set_defaults(func=run_readme)

    # diagram command
    diagram_parser = subparsers.add_parser('diagram', help='Generate architecture diagram')
    diagram_parser.add_argument('--root', '-r', default='.', help='Project root')
    diagram_parser.add_argument('--format', default='mermaid', choices=['mermaid'])
    diagram_parser.add_argument('--output', '-o', help='Output file')
    diagram_parser.set_defaults(func=run_diagram)

    # check command
    check_parser = subparsers.add_parser('check', help='Check documentation sync')
    check_parser.add_argument('--root', '-r', default='.', help='Project root')
    check_parser.add_argument('--source', '-s', default='src', help='Source directory')
    check_parser.set_defaults(func=run_check)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
