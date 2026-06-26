#!/usr/bin/env python3
import sys, json, urllib.request

API = 'https://api.rhdxm.com'

def post(path, data):
    req = urllib.request.Request(f'{API}{path}', json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read())

def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print("Usage: search.py <query> [-n <num>] [--agent <id>] [--content] [--freshness realtime|hour|day|week]")
        sys.exit(0)

    n, agent = 5, 'my-agent'
    if '-n' in args:
        i = args.index('-n'); n = int(args[i+1]); args = args[:i] + args[i+2:]
    if '--agent' in args:
        i = args.index('--agent'); agent = args[i+1]; args = args[:i] + args[i+2:]
    content = '--content' in args
    if content: args.remove('--content')
    freshness = None
    if '--freshness' in args:
        i = args.index('--freshness'); freshness = args[i+1]; args = args[:i] + args[i+2:]

    query = ' '.join(args)
    body = dict(query=query, agent_id=agent, max_results=n)
    if freshness: body['freshness'] = freshness
    resp = post('/search', body)
    search_id = resp['search_id']

    for i, r in enumerate(resp['results']):
        print(f"--- Result {i+1} ---")
        print(f"Title: {r['title']}")
        print(f"URL: {r['url']}")
        print(f"Score: {r['score']:.2f}")
        print(f"Snippet: {r['snippet']}")
        if content and i == 0:
            sel = post(f'/search/{search_id}/select', dict(url=r['url'], position=i, provider=r['provider']))
            print(f"Content:\n{(sel.get('content') or '')[:5000]}")
        print()

if __name__ == '__main__': main()
