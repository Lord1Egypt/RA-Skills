from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _shared import DATA_DIR, load_vendor_configs, read_csv_rows, unique_vendor_keys  # noqa: E402
from build_upload_csv import run_build  # noqa: E402
from collect_pages import prepare_extracted_templates, run_collect  # noqa: E402
from sync_feishu_sheet import run_sync  # noqa: E402


def resolve_vendor_keys(value: str) -> set[str] | None:
    configs = load_vendor_configs()
    if value == "default":
        return set(unique_vendor_keys(configs))
    if value == "all":
        return set(unique_vendor_keys(configs))
    keys = {part.strip() for part in value.split(",") if part.strip()}
    return keys or None


def collect_mode(args: argparse.Namespace) -> dict[str, object]:
    return run_collect(resolve_vendor_keys(args.vendors), timeout_seconds=args.timeout, headed=args.headed)


def build_mode(args: argparse.Namespace) -> dict[str, object]:
    return run_build(args.run_dir, data_dir=Path(args.data_dir), identity=args.identity)


def prepare_mode(args: argparse.Namespace) -> dict[str, object]:
    return prepare_extracted_templates(args.run_dir)


def push_mode(args: argparse.Namespace) -> dict[str, object]:
    data_dir = Path(args.data_dir)
    sync_runs = read_csv_rows(data_dir / "sync_runs.csv")
    if not sync_runs:
        raise RuntimeError(f"缺少 {data_dir / 'sync_runs.csv'} 或没有 build 记录，请先运行 --mode build。")
    last_run = sync_runs[-1]
    sheet_state = run_sync(data_dir, args.identity, folder_token=args.folder_token)
    return {
        **last_run,
        "run_dir": last_run.get("artifact_run_dir", ""),
        "data_dir": str(data_dir),
        "spreadsheet_token": sheet_state.get("spreadsheet_token", ""),
        "spreadsheet_url": sheet_state.get("url", ""),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect model pricing pages, prepare JSON extraction files, build CSV mirrors, and sync to Feishu Sheets.")
    parser.add_argument("--mode", default="collect", help="collect | prepare | build | push")
    parser.add_argument("--vendors", default="default", help="default | all | comma-separated vendor keys")
    parser.add_argument("--run-dir", default="", help="artifact run directory; prepare/build default to artifacts/latest_run.json")
    parser.add_argument("--identity", default="user")
    parser.add_argument("--data-dir", default=str(DATA_DIR))
    parser.add_argument("--folder-token", default="")
    parser.add_argument("--timeout", type=int, default=120, help="Page load timeout in seconds for collect mode")
    parser.add_argument("--headed", action="store_true", help="Use a visible browser window for collect mode")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        if args.mode == "collect":
            result = collect_mode(args)
        elif args.mode == "prepare":
            result = prepare_mode(args)
        elif args.mode == "build":
            result = build_mode(args)
        elif args.mode == "push":
            result = push_mode(args)
        else:
            raise ValueError(f"Unsupported mode: {args.mode}")
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
