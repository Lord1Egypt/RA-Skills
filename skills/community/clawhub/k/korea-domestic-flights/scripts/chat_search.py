#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common_cli import parse_date_range_text, time_preference_cli_args


def run_script(script_name: str, extra_args: list[str]) -> int:
    command = [sys.executable, str(SCRIPT_DIR / script_name), *extra_args]
    return subprocess.call(command)


def time_args(args) -> list[str]:
    return time_preference_cli_args({
        "time_pref": args.time_pref,
        "depart_after": args.depart_after,
        "return_after": args.return_after,
        "exclude_early_before": args.exclude_early_before,
        "prefer": args.prefer,
    })


def main():
    parser = argparse.ArgumentParser(description="Chat-friendly wrapper for Korea domestic flight search")
    parser.add_argument("--origin", required=True, help="예: 김포")
    parser.add_argument("--destination", help="단일 목적지")
    parser.add_argument("--destinations", help="여러 목적지, 예: 제주,부산,여수")
    parser.add_argument("--when", help="단일 날짜 또는 날짜 범위. 예: 내일, 이번주말, 내일부터 3일")
    parser.add_argument("--departure")
    parser.add_argument("--return-date")
    parser.add_argument("--return-offset", type=int, default=0)
    parser.add_argument("--adults", type=int, default=1)
    parser.add_argument("--cabin", default="ECONOMY", choices=["ECONOMY", "BUSINESS", "FIRST"])
    parser.add_argument("--time-pref", help="예: 오전, 저녁, 출발 10시 이후, 복귀 18시 이후, 너무 이른 비행 제외 8시, 늦은 시간 선호")
    parser.add_argument("--depart-after")
    parser.add_argument("--return-after")
    parser.add_argument("--exclude-early-before")
    parser.add_argument("--prefer", choices=["late", "morning", "afternoon", "evening"])
    parser.add_argument("--json", action="store_true", help="JSON 출력")
    args = parser.parse_args()

    human = [] if args.json else ["--human"]
    extra_time_args = time_args(args)

    has_multi_dest = bool(args.destinations and "," in args.destinations or (args.destinations and args.destination))
    destinations_value = args.destinations or args.destination
    if not destinations_value:
        raise SystemExit("--destination 또는 --destinations 가 필요합니다.")

    if args.when and not args.departure:
        start_dt, end_dt = parse_date_range_text(args.when)
        inferred_single_day = start_dt == end_dt
        if has_multi_dest and not inferred_single_day:
            return run_script(
                "search_destination_date_matrix.py",
                [
                    "--origin", args.origin,
                    "--destinations", destinations_value,
                    "--start-date", start_dt.strftime("%Y-%m-%d"),
                    "--end-date", end_dt.strftime("%Y-%m-%d"),
                    "--return-offset", str(args.return_offset),
                    "--adults", str(args.adults),
                    "--cabin", args.cabin,
                    *extra_time_args,
                    *human,
                ],
            )
        if has_multi_dest:
            return run_script(
                "search_multi_destination.py",
                [
                    "--origin", args.origin,
                    "--destinations", destinations_value,
                    "--departure", start_dt.strftime("%Y-%m-%d"),
                    *(["--return-date", args.return_date] if args.return_date else []),
                    "--adults", str(args.adults),
                    "--cabin", args.cabin,
                    *extra_time_args,
                    *human,
                ],
            )
        if not inferred_single_day:
            return run_script(
                "search_date_range.py",
                [
                    "--origin", args.origin,
                    "--destination", destinations_value,
                    "--start-date", start_dt.strftime("%Y-%m-%d"),
                    "--end-date", end_dt.strftime("%Y-%m-%d"),
                    "--return-offset", str(args.return_offset),
                    "--adults", str(args.adults),
                    "--cabin", args.cabin,
                    *extra_time_args,
                    *human,
                ],
            )
        return run_script(
            "search_domestic.py",
            [
                "--origin", args.origin,
                "--destination", destinations_value,
                "--departure", start_dt.strftime("%Y-%m-%d"),
                *(["--return-date", args.return_date] if args.return_date else []),
                "--adults", str(args.adults),
                "--cabin", args.cabin,
                *extra_time_args,
                *human,
            ],
        )

    if has_multi_dest and args.departure and args.return_offset > 0 and not args.return_date:
        return run_script(
            "search_destination_date_matrix.py",
            [
                "--origin", args.origin,
                "--destinations", destinations_value,
                "--start-date", args.departure,
                "--end-date", args.departure,
                "--return-offset", str(args.return_offset),
                "--adults", str(args.adults),
                "--cabin", args.cabin,
                *extra_time_args,
                *human,
            ],
        )

    if has_multi_dest and args.departure:
        return run_script(
            "search_multi_destination.py",
            [
                "--origin", args.origin,
                "--destinations", destinations_value,
                "--departure", args.departure,
                *( ["--return-date", args.return_date] if args.return_date else []),
                "--adults", str(args.adults),
                "--cabin", args.cabin,
                *extra_time_args,
                *human,
            ],
        )

    if args.departure:
        return run_script(
            "search_domestic.py",
            [
                "--origin", args.origin,
                "--destination", destinations_value,
                "--departure", args.departure,
                *(["--return-date", args.return_date] if args.return_date else []),
                "--adults", str(args.adults),
                "--cabin", args.cabin,
                *extra_time_args,
                *human,
            ],
        )

    raise SystemExit("날짜 정보가 없습니다. --when 또는 --departure 를 제공하세요.")


if __name__ == "__main__":
    main()
