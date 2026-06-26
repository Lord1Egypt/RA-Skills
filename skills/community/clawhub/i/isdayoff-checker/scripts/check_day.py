#!/usr/bin/env python3
import argparse
import datetime
import sys
import urllib.request
import urllib.parse
import json

# Using the simple path-style endpoint: https://isdayoff.ru/YYYYMMDD
DEFAULT_ENDPOINT = "https://isdayoff.ru/"


def query_isdayoff(date_str, endpoint=DEFAULT_ENDPOINT):
    # endpoint should be base URL ending with '/'
    url = endpoint.rstrip('/') + '/' + date_str
    with urllib.request.urlopen(url, timeout=10) as r:
        text = r.read().decode('utf-8')
    # Response is typically a single digit: 0=workday, 1=dayoff, etc.
    return text.strip()


def interpret(response_text):
    # Try to parse common formats
    # Example response: "20260413;1" or just "1\n"
    parts = response_text.replace('\r','').split('\n')
    first = parts[0].strip()
    if ';' in first:
        try:
            code = int(first.split(';')[-1])
        except:
            code = None
    else:
        try:
            code = int(first)
        except:
            code = None
    if code is None:
        return (None, response_text)
    if code == 0:
        return ('workday', response_text)
    if code == 1:
        return ('dayoff', response_text)
    if code == 2:
        return ('weekend', response_text)
    return (str(code), response_text)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--date', help='Дата в формате YYYY-MM-DD (по умолчанию сегодня)')
    p.add_argument('--endpoint', help='Альтернативный endpoint API', default=DEFAULT_ENDPOINT)
    args = p.parse_args()
    if args.date:
        try:
            d = datetime.datetime.strptime(args.date, '%Y-%m-%d').date()
        except Exception as e:
            print('Invalid date format, use YYYY-MM-DD', file=sys.stderr)
            sys.exit(2)
    else:
        d = datetime.date.today()
    date_str = d.strftime('%Y%m%d')
    try:
        resp = query_isdayoff(date_str, endpoint=args.endpoint)
    except Exception as e:
        print('ERROR: failed to query API:', e, file=sys.stderr)
        sys.exit(3)
    kind, raw = interpret(resp)
    if kind is None:
        print('UNKNOWN API RESPONSE:', raw)
        sys.exit(4)
    print(f'Date: {d.isoformat()} -> {kind}')
    # exit code: 0 for workday, 1 for dayoff/weekend, else 2
    if kind == 'workday':
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
