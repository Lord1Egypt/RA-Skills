#!/usr/bin/env python3
import sys, json, urllib.request

API = 'https://api.rhdxm.com'

def find(query, n=5, ecosystem=None):
    body = dict(task=query, max_results=n)
    if ecosystem: body['ecosystem'] = ecosystem
    data = json.dumps(body).encode()
    req = urllib.request.Request(f'{API}/find-capability', data, headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read())

def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print("Usage: capabilities.py <query> [-n <num>] [--ecosystem mcp|openclaw]")
        print("\nFind the best tool for your task across MCP servers and OpenClaw skills.")
        sys.exit(0)

    n, ecosystem = 5, None
    if '-n' in args:
        i = args.index('-n'); n = int(args[i+1]); args = args[:i] + args[i+2:]
    if '--ecosystem' in args:
        i = args.index('--ecosystem'); ecosystem = args[i+1]; args = args[:i] + args[i+2:]

    query = ' '.join(args)
    resp = find(query, n, ecosystem)
    for r in resp['results']:
        print(f"\n--- {r['name']} [{r['ecosystem']}] ---")
        print(f"Homepage: {r.get('homepage', 'n/a')}")
        print(f"Stars: {r.get('stars', 'n/a')}  Author: {r.get('author', 'n/a')}")
        print(f"{r['description']}")

if __name__ == '__main__': main()
