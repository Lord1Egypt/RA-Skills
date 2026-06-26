"""run_monitor.py — Run the LLM behavioral test suite and write a report.

Usage:
    python run_monitor.py

Writes results to monitor_report.json.
Exits with code 0 if all tests pass, 1 if any fail.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
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


def run_assertions(output: str, assertions: list[dict]) -> list[dict]:
    """Run behavioral assertions against output. Returns a list of result dicts."""
    from llm_behave.core.assertions import AssertBehavior

    results = []
    ab = AssertBehavior(output)

    for assertion in assertions:
        atype = assertion.get("type")
        threshold = assertion.get("threshold")

        try:
            if atype == "mentions":
                kwargs = {"threshold": threshold} if threshold is not None else {}
                ab.mentions(assertion["concept"], **kwargs)
            elif atype == "not_mentions":
                kwargs = {"threshold": threshold} if threshold is not None else {}
                ab.not_mentions(assertion["concept"], **kwargs)
            elif atype == "tone":
                kwargs = {"threshold": threshold} if threshold is not None else {}
                ab.tone(assertion["expected"], **kwargs)
            elif atype == "intent":
                kwargs = {"threshold": threshold} if threshold is not None else {}
                ab.intent(assertion["expected"], **kwargs)
            else:
                results.append({
                    "type": atype,
                    "passed": False,
                    "score": None,
                    "message": f"Unknown assertion type: {atype!r}",
                })
                continue

            # Passed — grab the last result for its score
            last = ab.results[-1]
            results.append({
                "type": atype,
                "passed": True,
                "score": round(last.similarity_score, 4) if last.similarity_score is not None else None,
                "message": "",
            })

        except AssertionError:
            last = ab.results[-1]
            results.append({
                "type": atype,
                "passed": False,
                "score": round(last.similarity_score, 4) if last.similarity_score is not None else None,
                "message": last.message,
            })

    return results


def run_test(test: dict, baseline_dir: Path) -> dict:
    """Run a single test. Returns a result dict."""
    name = test["name"]
    provider_name = test["provider"]
    model = test["model"]
    prompt = test["prompt"]
    assertions_cfg = test.get("assertions", [])
    drift_cfg = test.get("drift", {})

    result = {
        "name": name,
        "provider": provider_name,
        "model": model,
        "passed": True,
        "status": "pass",
        "output": None,
        "output_preview": None,
        "assertion_results": [],
        "drift": None,
        "error": None,
    }

    # Call the LLM
    try:
        provider = get_provider(provider_name, model)
        output = provider.chat([{"role": "user", "content": prompt}])
        result["output"] = output
        result["output_preview"] = output[:200]
    except EnvironmentError as e:
        result["passed"] = False
        result["status"] = "error"
        result["error"] = str(e)
        return result
    except Exception as e:
        result["passed"] = False
        result["status"] = "error"
        result["error"] = f"LLM call failed: {e}"
        return result

    # Run behavioral assertions
    if assertions_cfg:
        assertion_results = run_assertions(output, assertions_cfg)
        result["assertion_results"] = assertion_results
        if any(not r["passed"] for r in assertion_results):
            result["passed"] = False

    # Run drift detection
    if drift_cfg.get("enabled", False):
        from llm_behave.core.drift import DriftTest

        threshold = drift_cfg.get("threshold", 0.80)
        baseline_file = baseline_dir / f"{name}.json"

        if not baseline_file.exists():
            result["drift"] = {
                "enabled": True,
                "passed": False,
                "score": None,
                "threshold": threshold,
                "message": f"No baseline found. Run capture_baseline.py first.",
            }
            result["passed"] = False
        else:
            try:
                drift_result = DriftTest.compare(
                    baseline_name=name,
                    current_output=output,
                    threshold=threshold,
                    baseline_dir=baseline_dir,
                )
                result["drift"] = {
                    "enabled": True,
                    "passed": drift_result.passed,
                    "score": round(drift_result.drift_score, 4),
                    "threshold": threshold,
                    "message": "" if drift_result.passed else drift_result.details,
                }
                if not drift_result.passed:
                    result["passed"] = False
            except Exception as e:
                result["drift"] = {
                    "enabled": True,
                    "passed": False,
                    "score": None,
                    "threshold": threshold,
                    "message": f"Drift check failed: {e}",
                }
                result["passed"] = False

    if not result["passed"] and result["status"] != "error":
        result["status"] = "fail"

    return result


def print_summary(results: list[dict]) -> None:
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed

    print(f"\nResults: {total} run | {passed} passed | {failed} failed\n")

    for r in results:
        icon = "PASS" if r["passed"] else ("ERROR" if r["status"] == "error" else "FAIL")
        print(f"  [{icon}] {r['name']} ({r['provider']} / {r['model']})")

        if r["error"]:
            print(f"         Error: {r['error']}")

        for a in r.get("assertion_results", []):
            if not a["passed"]:
                score_str = f" [score: {a['score']}]" if a["score"] is not None else ""
                print(f"         assertion({a['type']}) FAILED{score_str}: {a['message']}")

        drift = r.get("drift")
        if drift and drift["enabled"] and not drift["passed"]:
            score_str = f" [score: {drift['score']}]" if drift["score"] is not None else ""
            print(f"         drift FAILED{score_str}: {drift['message']}")

    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run LLM behavioral tests and write monitor_report.json.")
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
        help="Directory where baselines are stored (default: .llm_behave_baselines)",
    )
    parser.add_argument(
        "--output",
        default="monitor_report.json",
        metavar="PATH",
        help="Output path for the report (default: monitor_report.json)",
    )
    args = parser.parse_args()

    check_dependencies()

    suite_path = Path(args.suite)
    baseline_dir = Path(args.baseline_dir)
    output_path = Path(args.output)

    tests = load_test_suite(suite_path)
    print(f"Running {len(tests)} test(s) from {suite_path}")

    results = []
    for test in tests:
        name = test.get("name", "<unnamed>")
        print(f"  running: {name} ...", end=" ", flush=True)
        result = run_test(test, baseline_dir)
        results.append(result)
        print("PASS" if result["passed"] else ("ERROR" if result["status"] == "error" else "FAIL"))

    # Write report
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": str(suite_path),
        "total": len(results),
        "passed": sum(1 for r in results if r["passed"]),
        "failed": sum(1 for r in results if not r["passed"]),
        "results": results,
    }

    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    print_summary(results)
    print(f"Report written to {output_path}")

    if report["failed"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
