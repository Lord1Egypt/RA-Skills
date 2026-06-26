#!/usr/bin/env python3
import sys, json, urllib.request

API = 'https://api.rhdxm.com'

def find(query, n=5):
    data = json.dumps(dict(query=query, max_results=n)).encode()
    req = urllib.request.Request(f'{API}/find', data, headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read())

def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print("Usage: finder.py <query> [-n <num>]")
        print("\nFind the right MCP server for your task.")
        sys.exit(0)

    n = 5
    if '-n' in args:
        i = args.index('-n'); n = int(args[i+1]); args = args[:i] + args[i+2:]

    query = ' '.join(args)
    resp = find(query, n)
    for r in resp['results']:
        print(f"\n--- {r['name']} ---")
        print(f"URL: {r['url']}")
        print(f"Stars: {r.get('stars', 'n/a')}  Language: {r.get('language', 'n/a')}  Category: {r['category']}")
        print(f"{r['description']}")

if __name__ == '__main__': main()
