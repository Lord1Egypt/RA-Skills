#!/usr/bin/env python3
"""
Unified Grok Swarm CLI entrypoint.
Dispatches to refactor/analyze/code/reason modes using grok_bridge.py logic.

Supports file writing when Grok generates code:
    --output-dir <path>  Directory to write files to
    --apply              Actually write files (dry-run by default)
    --execute <cmd>      Run a command after generation
    --use-morph          Use Morph LLM MCP for file edits if available
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

# Support both source and installed package layouts
current = Path(__file__).parent
if str(current) not in sys.path:
    sys.path.insert(0, str(current))

from grok_bridge import call_grok, read_files, MODE_PROMPTS


def check_morph_available():
    """Check if Morph LLM MCP is installed."""
    try:
        result = subprocess.run(
            ["claude", "mcp", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "morph" in result.stdout.lower()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def apply_with_morph(blocks, base_dir):
    """
    Apply code blocks using Morph LLM MCP edit_file tool.
    Returns summary dict.
    """
    import uuid

    applied = 0
    errors = []
    base_resolved = Path(base_dir).resolve()

    for block in blocks:
        # For Morph, we prefer partial edits. Use path_hint as target.
        path_hint = block.get("path_hint", "")
        if not path_hint:
            # Try to infer from code
            inferred_path = block.get("inferred_path", "")
            if not inferred_path:
                # No valid path - skip this block
                errors.append("No path_hint or inferred_path provided - skipping partial edit")
                continue
            path_hint = inferred_path

        # Sanitize and validate path_hint to prevent path traversal
        # Check if path_hint is absolute
        path_obj = Path(path_hint)
        if path_obj.is_absolute():
            errors.append(f"{path_hint}: absolute paths not allowed")
            continue

        # Resolve the full path and ensure it's within base_dir
        try:
            target_path = (base_resolved / path_hint).resolve()
            # Validate containment
            target_path.relative_to(base_resolved)
            validated_path = str(target_path)
        except ValueError:
            errors.append(f"{path_hint}: path traversal detected - outside base_dir")
            continue

        # Execute via claude mcp
        try:
            result = subprocess.run(
                ["claude", "mcp", "call", "morphllm", "edit_file",
                 "--file", validated_path,
                 "--code", block["code"],
                 "--language", block.get("language", "")],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                applied += 1
            else:
                errors.append(f"{path_hint}: {result.stderr}")
        except (OSError, subprocess.SubprocessError) as e:
            errors.append(f"{path_hint}: {e}")

    return {
        "applied": applied,
        "total": len(blocks),
        "errors": errors
    }


def parse_and_write(result_text, output_dir, dry_run=True):
    """
    Parse code blocks from Grok response and write to files.
    Returns summary string.
    """
    from apply import parse_code_blocks, apply_blocks, format_summary

    blocks = parse_code_blocks(result_text)

    if not blocks:
        return "No code blocks found in response."

    if dry_run:
        # Just show what would happen
        base = Path(output_dir)
        summaries = []
        for block in blocks:
            from apply import infer_filename
            filename = infer_filename(block, output_dir)
            summaries.append(f"  • {filename} ({block.get('language', 'text')}, {len(block['code']):,} chars)")
        return f"\nFound {len(blocks)} code block(s) — dry-run:\n" + "\n".join(summaries)

    # Actually write
    result = apply_blocks(blocks, output_dir, dry_run=False)
    return format_summary(result, output_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Grok Swarm — Multi-agent CLI powered by Grok 4.20",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "mode",
        nargs="?",
        choices=list(MODE_PROMPTS.keys()),
        default="reason",
        help="Task mode (default: reason)",
    )
    parser.add_argument("--prompt", "-p", required=True, help="Task instruction or question")
    parser.add_argument("--files", "-f", nargs="*", default=[], help="Files to include as context")
    parser.add_argument("--system", "-s", help="Override system prompt")
    parser.add_argument("--tools", "-t", help="Path to OpenAI-format tools JSON")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout in seconds")
    parser.add_argument("--output", help="Write raw output to file")
    parser.add_argument("--output-dir", "--od", "-d",
                        help="Directory to write generated files (used with --apply)")
    parser.add_argument("--apply", "-a", action="store_true",
                        help="Actually write files from code blocks (dry-run by default)")
    parser.add_argument("--execute", "-e", metavar="CMD",
                        help="Execute command after generation (shell string)")
    parser.add_argument("--use-morph", action="store_true",
                        help="Use Morph LLM MCP for file edits if available")

    args = parser.parse_args()

    if args.mode == "orchestrate" and not args.system:
        print("ERROR: orchestrate mode requires --system", file=sys.stderr)
        sys.exit(1)

    # Check Morph availability if --use-morph is set
    use_morph = False
    if args.use_morph:
        if check_morph_available():
            use_morph = True
            print("Morph LLM MCP detected — will use for file edits", file=sys.stderr)
        else:
            print("WARNING: --use-morph set but Morph LLM MCP not found", file=sys.stderr)
            print("  Install with: claude mcp add morphllm", file=sys.stderr)

    context = read_files(args.files) if args.files else ""

    if args.files:
        print(f"Read {len(args.files)} file(s) — {len(context):,} chars", file=sys.stderr)

    # Parse tools if provided
    tools = None
    if args.tools:
        with open(args.tools, 'r', encoding='utf-8') as f:
            tools = json.load(f)

    print(f"Calling Grok 4.20 (mode={args.mode}, 4 agents)...", file=sys.stderr)

    start = time.time()
    result = call_grok(
        prompt=args.prompt,
        mode=args.mode,
        context=context,
        system_override=args.system,
        tools=tools,
        timeout=args.timeout,
    )
    elapsed = time.time() - start

    # Preserve raw result for output
    raw_result = result

    # Handle JSON tool call responses
    response_data = None
    normalized_result = result
    if result.startswith("{") and '"tool_calls"' in result:
        try:
            response_data = json.loads(result)
            normalized_result = response_data.get("content", result)
        except json.JSONDecodeError:
            pass

    # File writing logic
    if args.apply or args.output_dir:
        output_dir = args.output_dir or "./grok-output"

        if use_morph and args.apply:
            # Use Morph LLM for edits
            from apply import parse_code_blocks
            blocks = parse_code_blocks(normalized_result)

            if not blocks:
                print("\nNo code blocks found to apply via Morph.", file=sys.stderr)
            else:
                morph_result = apply_with_morph(blocks, output_dir)
                print(f"\nApplied {morph_result['applied']}/{morph_result['total']} edits via Morph LLM",
                      file=sys.stderr)
                if morph_result['errors']:
                    for err in morph_result['errors']:
                        print(f"  Error: {err}", file=sys.stderr)
        else:
            # Use direct file writing
            summary = parse_and_write(normalized_result, output_dir, dry_run=not args.apply)
            print(summary, file=sys.stderr)

    # Write raw output if requested
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(raw_result, encoding='utf-8')
        print(f"Output written to {args.output}", file=sys.stderr)

    # Execute command if requested
    if args.execute:
        print(f"\nExecuting: {args.execute}", file=sys.stderr)
        exec_result = subprocess.run(
            args.execute,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        if exec_result.stdout:
            print(exec_result.stdout)
        if exec_result.stderr:
            print(exec_result.stderr, file=sys.stderr)
        if exec_result.returncode != 0:
            print(f"Command exited with code {exec_result.returncode}", file=sys.stderr)
            sys.exit(exec_result.returncode)

    # Output the normalized response to stdout (unless we wrote files and nothing else)
    if not args.output and not args.execute:
        print(normalized_result)

    print(f"\nCompleted in {elapsed:.1f}s", file=sys.stderr)


if __name__ == "__main__":
    main()