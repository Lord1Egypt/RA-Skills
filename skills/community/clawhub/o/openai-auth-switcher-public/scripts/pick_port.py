#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import socket
from contextlib import closing

DEFAULT_CANDIDATES = [9527, 12138]


def is_port_free(port: int, host: str = '127.0.0.1') -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
            return True
        except OSError:
            return False


def pick_port(candidates: list[int] | None = None, host: str = '127.0.0.1') -> dict:
    tried = []
    for port in (candidates or DEFAULT_CANDIDATES):
        tried.append(port)
        if is_port_free(port, host=host):
            return {'ok': True, 'port': port, 'source': 'preferred', 'tried': tried}

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind((host, 0))
        port = sock.getsockname()[1]
        return {'ok': True, 'port': port, 'source': 'fallback-random', 'tried': tried}


def main() -> int:
    parser = argparse.ArgumentParser(description='Pick a preferred web port for openai-auth-switcher-public')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    result = pick_port(host=args.host)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result['port'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
