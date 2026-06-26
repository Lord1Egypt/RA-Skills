"""capture_baseline.py — Save LLM output baselines for drift detection.

Run once before monitoring begins:
    python capture_baseline.py

Re-capture a single test after intentional prompt/model changes:
    python capture_baseline.py --update-baseline <test-name>

Force re-capture of all tests:
    python capture_baseline.py --force
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def check_dependencies() -> None:
    try:
        import llm_behave  # noqa: F401
    except ImportError:
        print("ERROR: llm-behave is not installed.")
        print("Install with: pip install llm-behave[semantic]")
        sys.exit(1)

    try:
        from llm_behave.engines.semantic import get_semantic_engine
        get_semantic_engine()
    except Exception as e:
        print(f"ERROR: Could not load semantic engine: {e}")
        print("Install with: pip install llm-behave[semantic]")
        sys.exit(1)


def load_test_suite(path: Path) -> list[dict]:
    try:
        import yaml
    except ImportError:
        print("ERROR: pyyaml is not installed. Install with: pip install pyyaml")
        sys.exit(1)

    if not path.exists():
        print(f"ERROR: test_suite.yaml not found at {path}")
        print("Create it in your project root. See references/test-suite-format.md for the format.")
        sys.exit(1)

    try:
        with open(path) as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR: Could not parse {path}: {e}")
        sys.exit(1)

    if not isinstance(data, dict) or "tests" not in data:
        print(f"ERROR: {path} must have a top-level 'tests' key.")
        sys.exit(1)

    return data["tests"]


def get_provider(provider_name: str, model: str):
    if provider_name == "openai":
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise EnvironmentError("OPENAI_API_KEY is not set.")
        from llm_behave.providers.openai_adapter import OpenAIProvider
        return OpenAIProvider(model=model)

    elif provider_name == "anthropic":
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise EnvironmentError("ANTHROPIC_API_KEY is not set.")
        from llm_behave.providers.anthropic_adapter import AnthropicProvider
        return AnthropicProvider(model=model)

    elif provider_name == "ollama":
        host = os.environ.get("OLLAMA_BASE_URL")
        from llm_behave.providers.ollama_adapter import OllamaProvider
        return OllamaProvider(model=model, host=host)

    elif provider_name == "custom":
        base_url = os.environ.get("CUSTOM_LLM_BASE_URL")
        if not base_url:
            raise EnvironmentError("CUSTOM_LLM_BASE_URL is not set.")
        api_key = os.environ.get("CUSTOM_LLM_API_KEY", "none")
        from llm_behave.providers.openai_adapter import OpenAIProvider
        return OpenAIProvider(model=model, base_url=base_url, api_key=api_key)

    else:
        raise ValueError(f"Unknown provider '{provider_name}'. Supported: openai, anthropic, ollama, custom")


def capture_baseline(test: dict, baseline_dir: Path) -> None:
    name = test["name"]
    prompt = test["prompt"]
    provider_name = test["provider"]
    model = test["model"]

    provider = get_provider(provider_name, model)
    output = provider.chat([{"role": "user", "content": prompt}])

    from llm_behave.core.drift import DriftTest
    DriftTest._save_baseline(name, output, baseline_dir)

    preview = output[:80].replace("\n", " ")
    print(f"  [saved] {name} ({provider_name} / {model})")
    print(f"          {preview!r}{'...' if len(output) > 80 else ''}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture LLM baselines for drift detection.")
    parser.add_argument(
        "--update-baseline",
        metavar="TEST_NAME",
        help="Delete and re-capture the baseline for a single named test.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-capture all tests, overwriting existing baselines.",
    )
    parser.add_argument(
        "--suite",
        default="test_suite.yaml",
        metavar="PATH",
        help="Path to test_suite.yaml (default: test_suite.yaml)",
    )
    parser.add_argument(
        "--baseline-dir",
        default=".llm_behave_baselines",
        metavar="DIR",
        help="Directory to store baselines (default: .llm_behave_baselines)",
    )
    args = parser.parse_args()

    check_dependencies()

    suite_path = Path(args.suite)
    baseline_dir = Path(args.baseline_dir)
    tests = load_test_suite(suite_path)

    # Determine which tests to capture
    if args.update_baseline:
        target_names = {args.update_baseline}
        matching = [t for t in tests if t["name"] == args.update_baseline]
        if not matching:
            print(f"ERROR: No test named '{args.update_baseline}' found in {suite_path}")
            sys.exit(1)
        tests_to_run = matching
        # Delete existing baseline so _save_baseline starts fresh
        baseline_file = baseline_dir / f"{args.update_baseline}.json"
        if baseline_file.exists():
            baseline_file.unlink()
            print(f"Deleted existing baseline: {baseline_file}")
    elif args.force:
        tests_to_run = tests
        # Delete all existing baselines for these tests
        for t in tests:
            baseline_file = baseline_dir / f"{t['name']}.json"
            if baseline_file.exists():
                baseline_file.unlink()
        print(f"Deleted all existing baselines in {baseline_dir}/")
    else:
        # Default: skip tests that already have a baseline
        tests_to_run = []
        for t in tests:
            baseline_file = baseline_dir / f"{t['name']}.json"
            if baseline_file.exists():
                print(f"  [skip]  {t['name']} — baseline already exists (use --force to re-capture)")
            else:
                tests_to_run.append(t)

    if not tests_to_run:
        print("\nNothing to capture. All baselines are already saved.")
        print("Use --force to re-capture all, or --update-baseline <name> to reset one.")
        sys.exit(0)

    print(f"\nCapturing {len(tests_to_run)} baseline(s) into {baseline_dir}/\n")
    captured = 0
    failed = 0

    for test in tests_to_run:
        name = test.get("name", "<unnamed>")
        try:
            capture_baseline(test, baseline_dir)
            captured += 1
        except EnvironmentError as e:
            print(f"  [error] {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  [error] {name}: {e}")
            failed += 1

    print(f"\nDone. Captured: {captured}  Failed: {failed}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
