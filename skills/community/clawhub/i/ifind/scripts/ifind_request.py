#!/usr/bin/env python3
import argparse
import json
from ifind_api import IFindAPI, IFindHistoryData, IFindRealtimeData
from ifind_token_store import load_refresh_token


def build_client(kind: str):
    token = load_refresh_token()
    if kind == 'history':
        return IFindHistoryData(token)
    if kind == 'realtime':
        return IFindRealtimeData(token)
    return IFindAPI(token)


def run_endpoint(args) -> dict:
    api = build_client('base')
    payload = json.loads(args.payload)
    return api._call_api(args.endpoint, payload)


def run_preset(args) -> dict:
    if args.preset == 'realtime':
        api = build_client('realtime')
        return api.get_realtime(args.codes, args.indicators)
    if args.preset == 'ohlcv':
        api = build_client('history')
        return api.get_ohlc(
            codes=args.codes,
            startdate=args.startdate,
            enddate=args.enddate,
            adjust=args.adjust,
            period=args.period,
        )
    if args.preset == 'edb':
        api = build_client('base')
        return api.get_edb_data(
            indicators=args.indicators,
            startdate=args.startdate,
            enddate=args.enddate,
        )
    if args.preset == 'thscode':
        api = build_client('base')
        if args.seccode:
            return api.get_thscode(seccode=args.seccode, mode='seccode', isexact=args.isexact)
        return api.get_thscode(secname=args.secname, mode='secname', isexact=args.isexact)
    raise SystemExit(f'unsupported preset: {args.preset}')


def main() -> int:
    parser = argparse.ArgumentParser(description='Call iFinD QuantAPI via local wrapper')
    sub = parser.add_subparsers(dest='command', required=True)

    endpoint = sub.add_parser('endpoint')
    endpoint.add_argument('endpoint')
    endpoint.add_argument('--payload', required=True, help='JSON payload string')

    preset = sub.add_parser('preset')
    preset.add_argument('preset', choices=['realtime', 'ohlcv', 'edb', 'thscode'])
    preset.add_argument('--codes')
    preset.add_argument('--indicators')
    preset.add_argument('--startdate')
    preset.add_argument('--enddate')
    preset.add_argument('--adjust', default='1')
    preset.add_argument('--period', default='D')
    preset.add_argument('--seccode')
    preset.add_argument('--secname')
    preset.add_argument('--isexact', default='0')

    args = parser.parse_args()
    if args.command == 'endpoint':
        result = run_endpoint(args)
    else:
        result = run_preset(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
