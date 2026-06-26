#!/usr/bin/env python3
"""
text_diff.py - Compare two text files or strings with multiple diff formats.

Usage:
    python3 text_diff.py <file1> <file2> [options]
    python3 text_diff.py --text "string1" --text2 "string2" [options]
"""

import argparse
import difflib
import json
import sys
from pathlib import Path


# ANSI colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"


def colorize(text, color, use_color=True):
    if not use_color:
        return text
    return f"{color}{text}{RESET}"


def load_text(path_or_text):
    """Load text from a file path."""
    p = Path(path_or_text)
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    print(f"[ERROR] File not found: {path_or_text}", file=sys.stderr)
    sys.exit(2)


def unified_diff(lines1, lines2, label1, label2, context=3, use_color=True):
    """Standard unified diff output."""
    diff = list(difflib.unified_diff(
        lines1, lines2,
        fromfile=label1, tofile=label2,
        n=context
    ))
    if not diff:
        return None, []
    output = []
    for line in diff:
        if line.startswith("+++") or line.startswith("---"):
            output.append(colorize(line.rstrip(), BOLD, use_color))
        elif line.startswith("@@"):
            output.append(colorize(line.rstrip(), CYAN, use_color))
        elif line.startswith("+"):
            output.append(colorize(line.rstrip(), GREEN, use_color))
        elif line.startswith("-"):
            output.append(colorize(line.rstrip(), RED, use_color))
        else:
            output.append(line.rstrip())
    return diff, output


def context_diff(lines1, lines2, label1, label2, context=3, use_color=True):
    """Context diff output (like diff -c)."""
    diff = list(difflib.context_diff(
        lines1, lines2,
        fromfile=label1, tofile=label2,
        n=context
    ))
    if not diff:
        return None, []
    output = []
    for line in diff:
        if line.startswith("***") or line.startswith("---"):
            output.append(colorize(line.rstrip(), BOLD, use_color))
        elif line.startswith("! "):
            output.append(colorize(line.rstrip(), YELLOW, use_color))
        elif line.startswith("+ "):
            output.append(colorize(line.rstrip(), GREEN, use_color))
        elif line.startswith("- "):
            output.append(colorize(line.rstrip(), RED, use_color))
        else:
            output.append(line.rstrip())
    return diff, output


def side_by_side_diff(lines1, lines2, use_color=True, width=40):
    """Side-by-side comparison."""
    matcher = difflib.SequenceMatcher(None, lines1, lines2)
    output = []
    header = f"{'LEFT':<{width}} | {'RIGHT':<{width}}"
    output.append(colorize(header, BOLD, use_color))
    output.append("-" * (width * 2 + 3))

    has_diff = False
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for l, r in zip(lines1[i1:i2], lines2[j1:j2]):
                l_str = l.rstrip()[:width]
                r_str = r.rstrip()[:width]
                output.append(f"{l_str:<{width}} | {r_str:<{width}}")
        elif tag == "replace":
            has_diff = True
            left = lines1[i1:i2]
            right = lines2[j1:j2]
            for l, r in zip(left, right):
                l_str = colorize(l.rstrip()[:width], RED, use_color)
                r_str = colorize(r.rstrip()[:width], GREEN, use_color)
                pad_l = width if not use_color else width + len(RED) + len(RESET)
                output.append(f"{l_str:<{pad_l}} | {r_str}")
            # Handle unequal lengths
            for l in left[len(right):]:
                l_str = colorize(l.rstrip()[:width], RED, use_color)
                pad_l = width if not use_color else width + len(RED) + len(RESET)
                output.append(f"{l_str:<{pad_l}} | {'':>{width}}")
            for r in right[len(left):]:
                r_str = colorize(r.rstrip()[:width], GREEN, use_color)
                output.append(f"{'':<{width}} | {r_str}")
        elif tag == "insert":
            has_diff = True
            for r in lines2[j1:j2]:
                r_str = colorize(r.rstrip()[:width], GREEN, use_color)
                output.append(f"{'':<{width}} | {r_str}")
        elif tag == "delete":
            has_diff = True
            for l in lines1[i1:i2]:
                l_str = colorize(l.rstrip()[:width], RED, use_color)
                pad_l = width if not use_color else width + len(RED) + len(RESET)
                output.append(f"{l_str:<{pad_l}} | {'':<{width}}")

    return has_diff, output


def word_diff(lines1, lines2, use_color=True):
    """Word-level diff highlighting changes within lines."""
    text1 = "".join(lines1)
    text2 = "".join(lines2)
    words1 = text1.split()
    words2 = text2.split()

    matcher = difflib.SequenceMatcher(None, words1, words2)
    output_parts = []
    has_diff = False

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            output_parts.append(" ".join(words1[i1:i2]))
        elif tag == "replace":
            has_diff = True
            output_parts.append(colorize(" ".join(words1[i1:i2]), RED, use_color))
            output_parts.append(colorize(" ".join(words2[j1:j2]), GREEN, use_color))
        elif tag == "insert":
            has_diff = True
            output_parts.append(colorize(" ".join(words2[j1:j2]), GREEN, use_color))
        elif tag == "delete":
            has_diff = True
            output_parts.append(colorize(" ".join(words1[i1:i2]), RED, use_color))

    return has_diff, [" ".join(output_parts)]


def json_diff(text1_lines, text2_lines, use_color=True):
    """Structural JSON diff."""
    try:
        obj1 = json.loads("".join(text1_lines))
        obj2 = json.loads("".join(text2_lines))
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parse error: {e}", file=sys.stderr)
        sys.exit(2)

    def flatten(obj, prefix=""):
        items = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                key = f"{prefix}.{k}" if prefix else k
                if isinstance(v, (dict, list)):
                    items.update(flatten(v, key))
                else:
                    items[key] = v
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                key = f"{prefix}[{i}]"
                if isinstance(v, (dict, list)):
                    items.update(flatten(v, key))
                else:
                    items[key] = v
        else:
            items[prefix] = obj
        return items

    flat1 = flatten(obj1)
    flat2 = flatten(obj2)
    all_keys = sorted(set(flat1.keys()) | set(flat2.keys()))

    output = []
    has_diff = False
    output.append(colorize("JSON Structural Diff:", BOLD, use_color))
    output.append("")

    for key in all_keys:
        v1 = flat1.get(key, "<missing>")
        v2 = flat2.get(key, "<missing>")
        if v1 == v2:
            continue
        has_diff = True
        output.append(colorize(f"  {key}:", CYAN, use_color))
        output.append(colorize(f"    - {v1}", RED, use_color))
        output.append(colorize(f"    + {v2}", GREEN, use_color))

    if not has_diff:
        output.append("  (no structural differences)")

    return has_diff, output


def yaml_diff(text1_lines, text2_lines, use_color=True):
    """Structural YAML diff (requires PyYAML)."""
    try:
        import yaml
    except ImportError:
        print("[ERROR] PyYAML is required for YAML diff. Install with: pip install pyyaml", file=sys.stderr)
        sys.exit(2)

    try:
        obj1 = yaml.safe_load("".join(text1_lines)) or {}
        obj2 = yaml.safe_load("".join(text2_lines)) or {}
    except yaml.YAMLError as e:
        print(f"[ERROR] YAML parse error: {e}", file=sys.stderr)
        sys.exit(2)

    # Convert to JSON representation for structural comparison
    j1 = json.dumps(obj1, sort_keys=True, default=str).splitlines(keepends=True)
    j2 = json.dumps(obj2, sort_keys=True, default=str).splitlines(keepends=True)
    return unified_diff(j1, j2, "file1 (yaml)", "file2 (yaml)", use_color=use_color)


def compute_stats(lines1, lines2):
    """Compute diff statistics."""
    matcher = difflib.SequenceMatcher(None, lines1, lines2)
    added = 0
    removed = 0
    changed = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "insert":
            added += j2 - j1
        elif tag == "delete":
            removed += i2 - i1
        elif tag == "replace":
            changed += max(i2 - i1, j2 - j1)
    similarity = round(matcher.ratio() * 100, 1)
    return {"added": added, "removed": removed, "changed": changed, "similarity_pct": similarity}


def main():
    parser = argparse.ArgumentParser(
        description="Compare two text files or strings and show what changed.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 text_diff.py old.txt new.txt
  python3 text_diff.py --text "hello world" --text2 "hello there"
  python3 text_diff.py config1.json config2.json --format json
  python3 text_diff.py file1.txt file2.txt --format side-by-side
  python3 text_diff.py file1.txt file2.txt --word-diff
  python3 text_diff.py file1.txt file2.txt --output-json
        """
    )
    parser.add_argument("file1", nargs="?", help="First file to compare")
    parser.add_argument("file2", nargs="?", help="Second file to compare")
    parser.add_argument("--text", help="First inline string to compare")
    parser.add_argument("--text2", help="Second inline string to compare")
    parser.add_argument(
        "--format", "-f",
        choices=["unified", "context", "side-by-side", "json", "yaml"],
        default="unified",
        help="Diff format (default: unified)"
    )
    parser.add_argument("--word-diff", action="store_true", help="Word-level diff")
    parser.add_argument("--ignore-whitespace", "-w", action="store_true",
                        help="Ignore leading/trailing whitespace")
    parser.add_argument("--ignore-case", "-i", action="store_true",
                        help="Case-insensitive comparison")
    parser.add_argument("--context", "-C", type=int, default=3,
                        help="Lines of context (default: 3)")
    parser.add_argument("--output-json", action="store_true",
                        help="Output diff statistics as JSON")
    parser.add_argument("--no-color", action="store_true",
                        help="Disable ANSI color output")

    args = parser.parse_args()
    use_color = not args.no_color and sys.stdout.isatty() or (not args.no_color and not args.output_json)

    # Load inputs
    if args.text and args.text2:
        lines1 = [(args.text + "\n")]
        lines2 = [(args.text2 + "\n")]
        label1, label2 = "text1", "text2"
    elif args.file1 and args.file2:
        lines1 = load_text(args.file1)
        lines2 = load_text(args.file2)
        label1, label2 = args.file1, args.file2
    else:
        parser.print_help()
        sys.exit(2)

    # Apply transformations
    if args.ignore_whitespace:
        lines1 = [l.strip() + "\n" for l in lines1]
        lines2 = [l.strip() + "\n" for l in lines2]
    if args.ignore_case:
        lines1 = [l.lower() for l in lines1]
        lines2 = [l.lower() for l in lines2]

    # Compute stats
    stats = compute_stats(lines1, lines2)

    if args.output_json:
        has_diff = lines1 != lines2
        print(json.dumps({
            "identical": not has_diff,
            "stats": stats,
            "label1": label1,
            "label2": label2
        }, indent=2))
        sys.exit(0 if not has_diff else 1)

    # Run the appropriate diff
    has_diff = False
    output_lines = []

    if args.word_diff:
        has_diff, output_lines = word_diff(lines1, lines2, use_color=use_color)
    elif args.format == "unified":
        diff, output_lines = unified_diff(lines1, lines2, label1, label2,
                                          context=args.context, use_color=use_color)
        has_diff = bool(diff)
    elif args.format == "context":
        diff, output_lines = context_diff(lines1, lines2, label1, label2,
                                          context=args.context, use_color=use_color)
        has_diff = bool(diff)
    elif args.format == "side-by-side":
        has_diff, output_lines = side_by_side_diff(lines1, lines2, use_color=use_color)
    elif args.format == "json":
        has_diff, output_lines = json_diff(lines1, lines2, use_color=use_color)
    elif args.format == "yaml":
        diff, output_lines = yaml_diff(lines1, lines2, use_color=use_color)
        has_diff = bool(diff)

    if not has_diff:
        print(colorize("Files are identical.", GREEN, use_color))
        sys.exit(0)

    for line in output_lines:
        print(line)

    # Print stats summary
    print()
    summary = (
        f"Stats: +{stats['added']} added, -{stats['removed']} removed, "
        f"~{stats['changed']} changed | {stats['similarity_pct']}% similar"
    )
    print(colorize(summary, CYAN, use_color))

    sys.exit(1)


if __name__ == "__main__":
    main()
