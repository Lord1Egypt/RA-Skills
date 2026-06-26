#!/usr/bin/env python3
import sys, json, urllib.request

API = 'https://api.rhdxm.com'

def post(path, data):
    req = urllib.request.Request(f'{API}{path}', json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read())

def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print("Usage: researcher.py <topic> [-n <num>] [-q <num_queries>] [--agent <id>] [--freshness realtime|hour|day|week]")
        sys.exit(0)

    n, nq, agent = 5, 3, 'my-agent'
    if '-n' in args:
        i = args.index('-n'); n = int(args[i+1]); args = args[:i] + args[i+2:]
    if '-q' in args:
        i = args.index('-q'); nq = int(args[i+1]); args = args[:i] + args[i+2:]
    if '--agent' in args:
        i = args.index('--agent'); agent = args[i+1]; args = args[:i] + args[i+2:]
    freshness = None
    if '--freshness' in args:
        i = args.index('--freshness'); freshness = args[i+1]; args = args[:i] + args[i+2:]

    topic = ' '.join(args)
    queries = [f"{topic} part {i+1}" for i in range(nq)]
    print(f"Researching: {topic}")
    print(f"Queries: {nq}, Results per query: {n}\n")

    for qi, query in enumerate(queries):
        print(f"=== Query {qi+1}/{nq}: {query} ===")
        body = dict(query=query, agent_id=agent, max_results=n)
        if freshness: body['freshness'] = freshness
        resp = post('/search', body)
        search_id = resp['search_id']

        for i, r in enumerate(resp['results']):
            print(f"  [{i+1}] {r['title']}")
            print(f"      {r['url']}")
            if i == 0:
                sel = post(f'/search/{search_id}/select', dict(url=r['url'], position=i, provider=r['provider']))
                content = (sel.get('content') or '')[:500]
                if content: print(f"      Preview: {content[:200]}...")
        print()

if __name__ == '__main__': main()
