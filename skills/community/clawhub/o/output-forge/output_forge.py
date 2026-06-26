#!/usr/bin/env python3
"""
OutputForge - AI Output Formatter
Transform raw AI output into platform-ready content

Author: Shadow Rose
License: MIT
"""

import sys
import os
import argparse
import json
from datetime import datetime
from pathlib import Path

# Import modules
try:
    from output_templates import TEMPLATES, apply_template
    from output_clean import clean_ai_isms
except ImportError as e:
    print(f"Error: Missing required module. Ensure output_templates.py and output_clean.py are in the same directory.")
    print(f"Details: {e}")
    sys.exit(1)

# Load config from JSON
import types as _types
def _load_config():
    _defaults = {
        "DEFAULT_AUTHOR": "Anonymous",
        "DEFAULT_CLEANUP_RULES": [],
        "CLEANUP_LEVEL": "moderate",
    }
    for _path in ("config.json", "config_example.json"):
        if os.path.exists(_path):
            try:
                with open(_path, "r", encoding="utf-8") as _f:
                    _data = json.load(_f)
                    _defaults.update(_data)
                    return _types.SimpleNamespace(**_defaults)
            except json.JSONDecodeError:
                pass
    return _types.SimpleNamespace(**_defaults)
config = _load_config()


def read_input(source):
    """Read input from file or stdin"""
    if source == '-' or source is None:
        return sys.stdin.read()
    
    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {source}")
    
    return path.read_text(encoding='utf-8')


def inject_metadata(content, metadata):
    """Inject metadata into content based on template needs"""
    # Metadata is a dict with keys: title, author, date, tags, description
    # This is used by templates during rendering
    return metadata


def split_for_threads(content, max_length=280, overlap=20):
    """Split long content into thread-friendly chunks"""
    if len(content) <= max_length:
        return [content]
    
    paragraphs = content.split('\n\n')
    threads = []
    current = ""
    
    for para in paragraphs:
        # If single paragraph exceeds limit, split by sentences
        if len(para) > max_length:
            sentences = para.replace('. ', '.|').split('|')
            for sentence in sentences:
                if len(current) + len(sentence) + 1 > max_length:
                    if current:
                        threads.append(current.strip())
                    current = sentence + " "
                else:
                    current += sentence + " "
        else:
            if len(current) + len(para) + 2 > max_length:
                threads.append(current.strip())
                current = para + "\n\n"
            else:
                current += para + "\n\n"
    
    if current.strip():
        threads.append(current.strip())
    
    return threads


def format_output(content, format_type, metadata=None, options=None):
    """Main formatting function"""
    if metadata is None:
        metadata = {}
    if options is None:
        options = {}
    
    # Clean AI-isms if requested
    if options.get('clean_ai_isms', True):
        content = clean_ai_isms(content, options.get('cleanup_rules', config.DEFAULT_CLEANUP_RULES))
    
    # Apply template
    if format_type not in TEMPLATES:
        raise ValueError(f"Unknown format: {format_type}. Available: {', '.join(TEMPLATES.keys())}")
    
    # Special handling for threads
    if format_type in ['twitter', 'thread']:
        max_len = options.get('max_thread_length', 280)
        threads = split_for_threads(content, max_len)
        return apply_template(format_type, threads, metadata, options)
    
    return apply_template(format_type, content, metadata, options)


def batch_process(input_dir, output_dir, format_type, metadata=None, options=None):
    """Process multiple files in batch mode"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = []
    for file in input_path.glob('*.txt'):
        try:
            content = file.read_text(encoding='utf-8')
            formatted = format_output(content, format_type, metadata, options)
            
            # Determine output extension
            ext_map = {
                'wordpress': '.html',
                'medium': '.md',
                'email': '.html',
                'twitter': '.txt',
                'linkedin': '.txt',
                'markdown': '.md',
                'latex': '.tex',
                'plain': '.txt'
            }
            ext = ext_map.get(format_type, '.txt')
            
            output_file = output_path / f"{file.stem}{ext}"
            output_file.write_text(formatted, encoding='utf-8')
            
            results.append({
                'input': str(file),
                'output': str(output_file),
                'status': 'success'
            })
        except Exception as e:
            results.append({
                'input': str(file),
                'error': str(e),
                'status': 'failed'
            })
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='OutputForge - Transform AI output for any platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Format for WordPress
  python output_forge.py input.txt -f wordpress -o output.html
  
  # Clean AI-isms and format for Medium
  python output_forge.py input.txt -f medium --title "My Post" --author "Jane Doe"
  
  # Split into Twitter thread
  python output_forge.py input.txt -f twitter -o thread.txt
  
  # Batch process directory
  python output_forge.py --batch input_dir/ output_dir/ -f markdown
  
  # Read from stdin
  cat ai_output.txt | python output_forge.py -f plain
        """
    )
    
    parser.add_argument('input', nargs='?', default='-', help='Input file (or - for stdin)')
    parser.add_argument('-f', '--format', required=True, 
                       choices=list(TEMPLATES.keys()),
                       help='Output format')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('--batch', nargs=2, metavar=('INPUT_DIR', 'OUTPUT_DIR'),
                       help='Batch process: input_dir output_dir')
    
    # Metadata options
    parser.add_argument('--title', help='Content title')
    parser.add_argument('--author', help='Content author')
    parser.add_argument('--date', help='Publication date (default: today)')
    parser.add_argument('--tags', help='Comma-separated tags')
    parser.add_argument('--description', help='SEO description')
    
    # Processing options
    parser.add_argument('--no-clean', action='store_true', 
                       help='Disable AI-ism cleanup')
    parser.add_argument('--max-thread-length', type=int, default=280,
                       help='Max length for thread posts (default: 280)')
    parser.add_argument('--image-placeholders', action='store_true',
                       help='Add image placeholder markers')
    
    args = parser.parse_args()
    
    # Build metadata
    metadata = {
        'title': args.title or 'Untitled',
        'author': args.author or config.DEFAULT_AUTHOR,
        'date': args.date or datetime.now().strftime('%Y-%m-%d'),
        'tags': [t.strip() for t in args.tags.split(',')] if args.tags else [],
        'description': args.description or ''
    }
    
    # Build options
    options = {
        'clean_ai_isms': not args.no_clean,
        'cleanup_rules': config.DEFAULT_CLEANUP_RULES,
        'max_thread_length': args.max_thread_length,
        'image_placeholders': args.image_placeholders
    }
    
    try:
        if args.batch:
            # Batch mode
            input_dir, output_dir = args.batch
            results = batch_process(input_dir, output_dir, args.format, metadata, options)
            
            # Print summary
            success = sum(1 for r in results if r['status'] == 'success')
            failed = sum(1 for r in results if r['status'] == 'failed')
            print(f"Batch processing complete: {success} succeeded, {failed} failed")
            
            if failed > 0:
                print("\nFailed files:")
                for r in results:
                    if r['status'] == 'failed':
                        print(f"  {r['input']}: {r['error']}")
        else:
            # Single file mode
            content = read_input(args.input)
            formatted = format_output(content, args.format, metadata, options)
            
            if args.output:
                Path(args.output).write_text(formatted, encoding='utf-8')
                print(f"Output written to: {args.output}")
            else:
                print(formatted)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
