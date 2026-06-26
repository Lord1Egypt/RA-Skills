"""Command line entry point for opendart-cli."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .client import OpenDartClient, OpenDartError, report_codes


def _print_json(obj) -> None:
    json.dump(obj, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="opendart",
        description="DART OpenAPI 비공식 CLI (opendart-cli v%s)" % __version__,
    )
    p.add_argument("--version", action="version", version=f"opendart-cli {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    # corp-code
    c = sub.add_parser("corp-code", help="고유번호 목록 다운로드 및 캐시")
    c.add_argument("--refresh", action="store_true", help="원격에서 강제로 재다운로드")
    c.add_argument("--count", action="store_true", help="행 개수만 출력")

    # find-corp
    f = sub.add_parser("find-corp", help="회사명/종목코드로 corp_code 검색")
    f.add_argument("query", help="회사명 일부, 6자리 종목코드, 또는 8자리 corp_code")
    f.add_argument("--limit", type=int, default=20)

    # list
    l = sub.add_parser("list", help="공시 검색")
    l.add_argument("--corp-code")
    l.add_argument("--bgn", dest="bgn_de", help="YYYYMMDD")
    l.add_argument("--end", dest="end_de", help="YYYYMMDD")
    l.add_argument(
        "--pblntf-ty",
        choices=list("ABCDEFGHIJ"),
        help="A=정기 B=주요 C=발행 D=지분 E=기타 F=외감 G=펀드 H=자산유동화 I=거래소 J=공정위",
    )
    l.add_argument("--corp-cls", choices=["Y", "K", "N", "E"], help="Y=유가 K=코스닥 N=코넥스 E=기타")
    l.add_argument("--last-reprt", choices=["Y", "N"], help="최종보고서만")
    l.add_argument("--page", type=int, default=1)
    l.add_argument("--page-count", type=int, default=10)

    # company
    co = sub.add_parser("company", help="기업 개황")
    co.add_argument("--corp-code", required=True)

    # finance
    fin = sub.add_parser("finance", help="단일회사 재무제표 조회")
    fin.add_argument("--corp-code", required=True)
    fin.add_argument("--bsns-year", required=True, help="YYYY")
    fin.add_argument(
        "--reprt-code",
        required=True,
        choices=sorted(report_codes().keys()),
        help="11011=사업 11012=반기 11013=1Q 11014=3Q",
    )
    fin.add_argument("--fs-div", choices=["OFS", "CFS"], help="OFS=개별 CFS=연결 (--all 시에만 사용)")
    fin.add_argument("--all", dest="full", action="store_true", help="전체 재무제표 (fnlttSinglAcntAll)")

    # majorstock
    ms = sub.add_parser("majorstock", help="대량보유자 현황")
    ms.add_argument("--corp-code", required=True)

    # elestock
    es = sub.add_parser("elestock", help="임원 지분 현황")
    es.add_argument("--corp-code", required=True)

    # document
    d = sub.add_parser("document", help="공시서류 원본 ZIP 다운로드")
    d.add_argument("--rcept-no", required=True, help="접수번호(14자리)")
    d.add_argument("--out", required=True, help="저장 경로")

    # report-codes
    rc = sub.add_parser("report-codes", help="보고서 코드 참조표")
    rc.set_defaults(_static=True)

    return p


def _run(args: argparse.Namespace) -> int:
    if args.command == "report-codes":
        _print_json(report_codes())
        return 0

    client = OpenDartClient()

    if args.command == "corp-code":
        rows = client.load_corp_codes(refresh=args.refresh)
        if args.count:
            _print_json({"count": len(rows), "cache_path": str(client.corp_code_cache_path())})
        else:
            _print_json({"count": len(rows), "cache_path": str(client.corp_code_cache_path()), "sample": rows[:5]})
        return 0

    if args.command == "find-corp":
        _print_json(client.find_corp(args.query, limit=args.limit))
        return 0

    if args.command == "list":
        _print_json(
            client.list_disclosures(
                corp_code=args.corp_code,
                bgn_de=args.bgn_de,
                end_de=args.end_de,
                last_reprt_at=args.last_reprt,
                pblntf_ty=args.pblntf_ty,
                corp_cls=args.corp_cls,
                page_no=args.page,
                page_count=args.page_count,
            )
        )
        return 0

    if args.command == "company":
        _print_json(client.company(args.corp_code))
        return 0

    if args.command == "finance":
        _print_json(
            client.finance(
                corp_code=args.corp_code,
                bsns_year=args.bsns_year,
                reprt_code=args.reprt_code,
                fs_div=args.fs_div,
                full=args.full,
            )
        )
        return 0

    if args.command == "majorstock":
        _print_json(client.major_stock(args.corp_code))
        return 0

    if args.command == "elestock":
        _print_json(client.exec_stock(args.corp_code))
        return 0

    if args.command == "document":
        data = client.download_document(args.rcept_no)
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        _print_json({"saved": str(out), "bytes": len(data)})
        return 0

    raise SystemExit(f"Unknown command: {args.command}")


def main(argv: Optional[list] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        return _run(args)
    except OpenDartError as exc:
        sys.stderr.write(f"[DART 오류] {exc}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
