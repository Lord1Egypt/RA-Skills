"""
Smoke Test for PaddleOCR Document Parsing Skill — AMD Radeon Cloud Edition

Verifies configuration and API connectivity.

Usage:
    uv run scripts/smoke_test.py
    uv run scripts/smoke_test.py --skip-api-test
    uv run scripts/smoke_test.py --test-url "https://example.com/test.pdf"
"""

# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "httpx==0.28.1",
# ]
# ///

import argparse
import base64
import sys
from pathlib import Path

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))


def print_config_guide() -> None:
    """Print configuration guide."""
    from lib import DEFAULT_TIMEOUT

    print(
        f"""
============================================================
AMD RADEON CLOUD — DOCUMENT PARSING CONFIGURATION
============================================================

Set the PADDLEOCR_DOC_PARSING_API_URL environment variable
to your AMD Radeon Cloud endpoint.

Example:
  export PADDLEOCR_DOC_PARSING_API_URL=http://host:port/layout-parsing

No API key or token is required.

Optional:
  PADDLEOCR_DOC_PARSING_TIMEOUT  - Request timeout in seconds (default: {DEFAULT_TIMEOUT})

============================================================
"""
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="PaddleOCR Document Parsing (AMD Radeon Cloud) smoke test"
    )
    parser.add_argument("--test-url", help="Optional: Custom document URL for testing")
    parser.add_argument(
        "--skip-api-test",
        action="store_true",
        help="Skip API connectivity test, only check configuration",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("PaddleOCR Document Parsing (AMD Radeon Cloud) - Smoke Test")
    print("=" * 60)

    print("\n[1/3] Checking dependencies...")

    try:
        import httpx

        print(f"  + httpx: {httpx.__version__}")
    except ImportError:
        print("  X httpx not installed")
        print("\nRun this script with uv to auto-resolve dependencies:")
        print("  uv run scripts/smoke_test.py")
        print("\nOr install manually:")
        print("  pip install httpx")
        return 1

    print("\n[2/3] Checking configuration...")

    from lib import get_config

    try:
        api_url = get_config()
        print(f"  + API endpoint: {api_url}")
    except ValueError as e:
        print(f"  X {e}")
        print_config_guide()
        return 1

    if args.skip_api_test:
        print("\n[3/3] Skipping API connectivity test (--skip-api-test)")
        print("\n" + "=" * 60)
        print("Configuration Check Complete!")
        print("=" * 60)
        return 0

    print("\n[3/3] Testing API connectivity...")

    test_url = (
        args.test_url
        or "https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/pp_structure_v3_demo.png"
    )
    print(f"  Test document: {test_url}")

    from lib import parse_document, _http_timeout_from_env, DEFAULT_TIMEOUT
    import httpx as _httpx

    # Download and encode the test file
    try:
        timeout = _http_timeout_from_env("PADDLEOCR_DOC_PARSING_TIMEOUT", float(DEFAULT_TIMEOUT))
        with _httpx.Client(timeout=timeout) as client:
            resp = client.get(test_url)
            resp.raise_for_status()
        file_data = base64.b64encode(resp.content).decode("utf-8")
    except Exception as e:
        print(f"\n  X Failed to download test file: {e}")
        return 1

    result = parse_document(file_data=file_data, file_source=test_url)

    if not result.get("ok"):
        error = result.get("error", {})
        print(f"\n  X API call failed: {error.get('message')}")
        return 1

    print("  + API call successful!")

    text = result.get("text", "")
    if text:
        preview = text[:200].replace("\n", " ")
        if len(text) > 200:
            preview += "..."
        print(f"\n  Preview: {preview}")

    print("\n" + "=" * 60)
    print("Smoke Test PASSED")
    print("=" * 60)
    print("\nNext steps:")
    print('  uv run scripts/layout_caller.py --file-url "URL" --pretty')
    print('  uv run scripts/layout_caller.py --file-path "doc.pdf" --pretty')

    return 0


if __name__ == "__main__":
    sys.exit(main())
