#!/usr/bin/env python3
"""HTTP request inspection: headers, status, redirects, timing."""

import argparse, json, ssl, sys, time, urllib.request, urllib.error

def inspect_url(url, headers_only=False, follow=False, full=False, timeout=10):
    req = urllib.request.Request(url, method='HEAD' if headers_only else 'GET')
    req.add_header('User-Agent', 'NetworkToolbox/1.0')

    start = time.time()
    try:
        if follow:
            resp = urllib.request.urlopen(req, timeout=timeout)
        else:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
    except urllib.error.HTTPError as e:
        resp = e
    except urllib.error.URLError as e:
        return {"error": str(e.reason), "url": url}
    except Exception as e:
        return {"error": str(e), "url": url}

    elapsed = (time.time() - start) * 1000
    result = {
        'url': url,
        'status': resp.status,
        'reason': resp.reason,
        'time_ms': round(elapsed, 1),
    }

    # Headers
    headers = dict(resp.headers)
    result['headers'] = headers

    # Body
    if not headers_only and full:
        try:
            body = resp.read().decode('utf-8', errors='replace')
            result['body_length'] = len(body)
            result['body_preview'] = body[:2000]
        except:
            pass
    elif not headers_only:
        try:
            body = resp.read(512)
            result['body_preview'] = body.decode('utf-8', errors='replace')[:200]
        except:
            pass

    resp.close()
    return result

def main():
    p = argparse.ArgumentParser(description='HTTP request inspection')
    p.add_argument('url', help='URL to inspect')
    p.add_argument('--headers-only', action='store_true', help='Send HEAD request')
    p.add_argument('--follow', action='store_true', help='Follow redirects')
    p.add_argument('--full', action='store_true', help='Fetch full response body')
    p.add_argument('--timeout', type=int, default=10)
    p.add_argument('--json', action='store_true', help='JSON output')
    args = p.parse_args()

    result = inspect_url(args.url, args.headers_only, args.follow, args.full, args.timeout)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    if 'error' in result:
        print(f"ERROR: {result['error']}")
        return

    print(f"URL:    {result['url']}")
    print(f"Status: {result['status']} {result['reason']}")
    print(f"Time:   {result['time_ms']:.0f}ms")
    print(f"\nHeaders ({len(result['headers'])}):")
    for k, v in sorted(result['headers'].items()):
        print(f"  {k}: {v}")

    if 'body_preview' in result:
        print(f"\nBody preview ({len(result.get('body_preview', ''))} chars):")
        print(result['body_preview'])

if __name__ == '__main__':
    main()
