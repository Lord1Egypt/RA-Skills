#!/usr/bin/env python3
"""
CLI wrapper around MinerU hosted API parsing and local open-source MinerU parsing.
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import tempfile
import uuid
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent))

from lib import TEMP_ROOT, parse_document


def _default_output_path() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    short_id = uuid.uuid4().hex[:8]
    return (
        Path(tempfile.gettempdir())
        / "mineru"
        / "doc-parsing"
        / "results"
        / f"result_{timestamp}_{short_id}.json"
    )


def _resolve_output_path(output_arg: str | None) -> Path:
    if output_arg:
        return Path(output_arg).expanduser().resolve()
    return _default_output_path().resolve()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run MinerU in hosted API mode or local open-source CLI mode.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  python scripts/mineru_caller.py --mode api --file-url "https://example.com/paper.pdf" --pretty
  python scripts/mineru_caller.py --mode api --file-path "C:/docs/paper.pdf" --pretty
  python scripts/mineru_caller.py --mode local --file-path "C:/docs/paper.pdf" --local-cmd "C:/MinerU/Scripts/mineru.exe" --pretty
  python scripts/mineru_caller.py --mode auto --file-path "C:/docs/paper.pdf" --stdout

API environment:
  MINERU_API_TOKEN                 Required for --mode api
  MINERU_API_BASE_URL             Optional, default: https://mineru.net
  MINERU_API_TIMEOUT              Optional, default: 60
  MINERU_API_POLL_TIMEOUT         Optional, default: 900
  MINERU_API_POLL_INTERVAL        Optional, default: 5

Local environment:
  MINERU_LOCAL_CMD                Optional path to mineru executable
  MINERU_LOCAL_PYTHON             Optional python path for `python -m mineru.cli.client`
  MINERU_LOCAL_BACKEND            Optional, default: pipeline
  MINERU_LOCAL_METHOD             Optional, default: auto
  MINERU_LOCAL_LANG               Optional, default: ch
  MINERU_LOCAL_MODEL_SOURCE       Optional, example: modelscope
  MINERU_LOCAL_DEVICE_MODE        Optional, example: cpu or cuda:0
  MINERU_LOCAL_TIMEOUT            Optional, in seconds

Default temp root:
  {TEMP_ROOT}
""",
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--file-url", help="Remote document URL")
    input_group.add_argument("--file-path", help="Local document path")

    parser.add_argument(
        "--mode",
        choices=("api", "local", "auto"),
        default="api",
        help="MinerU execution mode (default: api)",
    )
    parser.add_argument(
        "--language",
        default="auto",
        help="Language hint for MinerU API or local CLI (default: auto)",
    )
    parser.add_argument(
        "--ocr",
        action="store_true",
        help="Force OCR mode",
    )
    parser.add_argument(
        "--disable-formula",
        action="store_true",
        help="Disable formula extraction",
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Return after task submission without polling; API mode only",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Skip downloading full_zip_url after API completion; API mode only",
    )
    parser.add_argument(
        "--download-dir",
        help="Custom directory for API downloads or local MinerU output files",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    parser.add_argument("--local-cmd", help="Path to mineru executable for local mode")
    parser.add_argument("--local-python", help="Python path for `-m mineru.cli.client`")
    parser.add_argument("--local-backend", help="Local MinerU backend, for example pipeline")
    parser.add_argument("--local-method", choices=("auto", "txt", "ocr"), help="Local MinerU parse method")
    parser.add_argument(
        "--local-model-source",
        choices=("huggingface", "modelscope", "local"),
        help="Local MinerU model source",
    )
    parser.add_argument("--local-device", help="Local MinerU device mode, for example cpu or cuda:0")
    parser.add_argument("--local-timeout", type=float, help="Local MinerU timeout in seconds")

    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("--output", "-o", help="Write JSON envelope to a file")
    output_group.add_argument(
        "--stdout",
        action="store_true",
        help="Print JSON envelope to stdout instead of saving it",
    )

    args = parser.parse_args()

    result = parse_document(
        file_url=args.file_url,
        file_path=args.file_path,
        mode=args.mode,
        language=args.language,
        enable_formula=not args.disable_formula,
        ocr=args.ocr,
        wait=not args.no_wait,
        download=not args.no_download,
        download_dir=args.download_dir,
        local_cmd=args.local_cmd,
        local_python=args.local_python,
        local_backend=args.local_backend,
        local_method=args.local_method,
        local_model_source=args.local_model_source,
        local_device=args.local_device,
        local_timeout=args.local_timeout,
    )

    json_output = json.dumps(
        result,
        indent=2 if args.pretty else None,
        ensure_ascii=False,
    )

    if args.stdout:
        print(json_output)
    else:
        output_path = _resolve_output_path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json_output, encoding="utf-8")
        print(f"Result saved to: {output_path}", file=sys.stderr)

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
