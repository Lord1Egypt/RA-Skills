"""
Command-line interface for scripts.

This module provides a comprehensive command-line interface for the scripts library,
allowing users to count tokens and estimate costs for various LLM models directly
from the terminal.

The CLI supports:
    - Token counting for text input or files
    - Cost estimation with detailed breakdowns
    - Listing all supported models by provider
    - Verbose output with detailed information
    - Support for both input and output token pricing

Examples:
    Basic token counting:
    
    .. code-block:: bash
    
        scripts "Hello, world!" gpt-4
        scripts --file input.txt claude-3-opus-20240229
    
    Cost estimation:
    
    .. code-block:: bash
    
        scripts --cost "Your text here" gpt-4
        scripts --cost --output-tokens "Response text" gpt-4
    
    List supported models:
    
    .. code-block:: bash
    
        scripts --list-models
    
    Verbose output:
    
    .. code-block:: bash
    
        scripts --verbose --cost --file large_document.txt gpt-4

Functions:
    main: Main CLI entry point that handles argument parsing and execution
    list_models: Display all supported models organized by provider

The CLI provides comprehensive error handling and user-friendly output formatting
for both simple token counting and detailed cost analysis workflows.
"""

import argparse
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import List, Optional, Tuple

from .core import TokenCounter, get_supported_models, estimate_cost
from .exceptions import UnsupportedModelError, TokenizationError


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file_handle:
        return file_handle.read()


def _read_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must start with http:// or https://")
    with urllib.request.urlopen(url, timeout=10) as response:
        return response.read().decode("utf-8", errors="replace")


def _collect_inputs(argv: List[str]) -> List[Tuple[str, str, Optional[str]]]:
    """Collect inputs. Returns list of (source, value, label) where label is path for display."""
    items: List[Tuple[str, str, Optional[str]]] = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in {"--file", "-f"}:
            if i + 1 >= len(argv):
                raise ValueError("--file requires a path")
            path = argv[i + 1]
            items.append(("file", path, path))
            i += 2
            continue
        if arg in {"--url", "-u"}:
            if i + 1 >= len(argv):
                raise ValueError("--url requires a URL")
            items.append(("url", argv[i + 1], argv[i + 1]))
            i += 2
            continue
        if arg in {"--model", "-m", "--currency"}:
            i += 2
            continue
        if arg in {"--cost", "-c", "--output-tokens", "--verbose", "-v", "--list-models", "-l"}:
            i += 1
            continue
        if arg.startswith("-"):
            i += 1
            continue
        # Positional: treat as file path if it exists, else inline text
        p = Path(arg)
        if p.is_file():
            items.append(("file", arg, arg))
        else:
            items.append(("text", arg, None))
        i += 1
    return items


def _format_cost(cost: float, currency: str) -> str:
    if cost <= 0:
        return "NA"
    symbol = "₹" if currency.upper() == "INR" else "$"
    precision = 2 if currency.upper() == "INR" else 6
    return f"{symbol}{cost:.{precision}f}"


def main() -> None:
    """
    Main CLI entry point.
    
    Parses command-line arguments and executes the appropriate scripts functionality.
    Supports token counting, cost estimation, model listing, and file input processing.
    
    The function handles:
        - Argument parsing and validation
        - Text input from command line or file
        - Token counting for specified models
        - Cost estimation with input/output token differentiation
        - Model listing with provider organization
        - Comprehensive error handling and user feedback
        - Verbose output formatting
    
    Command-line Arguments:
        text (str, optional): Text to count tokens for
        model (str, optional): Model name (required unless using --list-models)
        --file, -f (str): Read text from file instead of command line
        --list-models, -l: List all supported models by provider
        --cost, -c: Show cost estimation along with token count
        --output-tokens: Calculate cost for output tokens instead of input
        --verbose, -v: Show detailed output with additional information
    
    Exit Codes:
        0: Success
        1: Error (unsupported model, file not found, tokenization failure, etc.)
    
    Raises:
        SystemExit: On error conditions or user interruption
    
    Examples:
        Basic usage:
        
        .. code-block:: bash
        
            scripts "Hello, world!" gpt-4
            scripts --file document.txt claude-3-opus-20240229
        
        With cost estimation:
        
        .. code-block:: bash
        
            scripts --cost --verbose "Long text content" gpt-4
            scripts --cost --output-tokens "Response text" gpt-4
        
        List models:
        
        .. code-block:: bash
        
            scripts --list-models
    """
    parser = argparse.ArgumentParser(
        description="Count tokens for various LLM models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  scripts file1.txt file2.txt --model gpt-4
  scripts --file input.txt --model claude-3-opus-20240229
  scripts --cost --model gpt-4 AGENTS.md SOUL.md MEMORY.md
  scripts --list-models
        """
    )

    parser.add_argument(
        "paths",
        nargs="*",
        metavar="FILE",
        help="Local file path(s) to count tokens (default input mode). Multiple paths supported for batch."
    )

    parser.add_argument(
        "--model", "-m",
        help="Model name (e.g., gpt-4, claude-3-opus-20240229)"
    )

    parser.add_argument(
        "--file", "-f",
        action="append",
        help="Read text from file (can be used multiple times)"
    )

    parser.add_argument(
        "--url", "-u",
        action="append",
        help="Read text from URL (http/https, can be used multiple times)"
    )

    parser.add_argument(
        "--list-models", "-l",
        action="store_true",
        help="List all supported models"
    )

    parser.add_argument(
        "--cost", "-c",
        action="store_true",
        help="Show cost estimation along with token count"
    )

    parser.add_argument(
        "--currency",
        default="USD",
        help="Currency for cost output (USD or INR)"
    )

    parser.add_argument(
        "--output-tokens",
        action="store_true",
        help="Calculate cost for output tokens instead of input tokens"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show verbose output"
    )

    args = None

    try:
        args = parser.parse_args()
        if args.list_models:
            list_models()
            return
        
        if not args.model:
            parser.error("Model name is required unless using --list-models")

        inputs = _collect_inputs(sys.argv[1:])
        # Also add positional paths from argparse (in case -m was before paths)
        for p in (args.paths or []):
            if Path(p).is_file():
                if not any(src == "file" and val == p for src, val, _ in inputs):
                    inputs.append(("file", p, p))
            else:
                if not any(src == "text" and val == p for src, val, _ in inputs):
                    inputs.append(("text", p, None))

        if not inputs:
            parser.error("Provide local file path(s), --file, or --url inputs")

        items: List[Tuple[str, str, Optional[str]]] = []
        for source, value, label in inputs:
            if source == "text":
                items.append((source, value, label))
                continue
            try:
                if source == "file":
                    content = _read_file(value)
                    items.append((source, content, value))
                elif source == "url":
                    content = _read_url(value)
                    items.append((source, content, value))
                else:
                    continue
            except FileNotFoundError:
                print(f"Error: File '{value}' not found", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error reading {source} '{value}': {e}", file=sys.stderr)
                sys.exit(1)

        try:
            counter = TokenCounter(args.model)
            for index, (source, content, label) in enumerate(items, start=1):
                token_count = counter.count(content)
                prefix = f"{label}: " if label else f"{index}) "
                if args.cost:
                    cost = estimate_cost(
                        token_count,
                        args.model,
                        input_tokens=not args.output_tokens,
                        currency=args.currency,
                    )
                    cost_display = _format_cost(cost, args.currency)
                    print(f"{prefix}tokens={token_count} cost={cost_display}")
                else:
                    print(f"{prefix}tokens={token_count}")

        except UnsupportedModelError as e:
            print(f"Error: {e}", file=sys.stderr)
            if args.verbose:
                print("\nUse --list-models to see supported models", file=sys.stderr)
            sys.exit(1)

        except TokenizationError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(1)
    
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args is not None and args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def list_models() -> None:
    """
    List all supported models organized by provider.
    
    Displays a comprehensive list of all supported models grouped by their
    respective providers (OpenAI, Anthropic, Google, Meta, etc.). The output
    includes model counts per provider and a total count across all providers.
    
    The function:
        - Retrieves all supported models using get_supported_models()
        - Groups models by provider with clear section headers
        - Sorts models alphabetically within each provider
        - Shows model counts for each provider and overall total
        - Formats output for easy readability
    
    Output Format:
        .. code-block:: text
        
            Supported models:
            ==================================================
            
            OPENAI (25 models):
            ------------------------------
              gpt-3.5-turbo
              gpt-4
              gpt-4o
              ...
            
            ANTHROPIC (12 models):
            ------------------------------
              claude-3-haiku-20240307
              claude-3-opus-20240229
              ...
            
            Total: 200+ models
    
    Note:
        This function is typically called when the --list-models CLI flag is used.
        It provides users with a complete overview of available models for token
        counting and cost estimation.
    """
    models = get_supported_models()
    
    print("Supported models:")
    print("=" * 50)
    
    for provider, model_list in models.items():
        print(f"\n{provider.upper()} ({len(model_list)} models):")
        print("-" * 30)
        
        for model in sorted(model_list):
            print(f"  {model}")
    
    print(f"\nTotal: {sum(len(models) for models in models.values())} models")


if __name__ == "__main__":
    main()
