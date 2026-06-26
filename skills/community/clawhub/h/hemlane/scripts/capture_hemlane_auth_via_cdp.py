#!/usr/bin/env python3
"""Capture live Hemlane signed auth headers from direct Brave CDP."""
import argparse, json, time, websocket
from pathlib import Path

def get_tabs():
    """Get all CDP tabs from Brave."""
    import urllib.request
    resp = urllib.request.urlopen('http://127.0.0.1:19222/json')
    return json.loads(resp.read().decode())

def ensure_hemlane_cdp_context(close_extras=False):
    """Find or create an authenticated Hemlane tab."""
    tabs = get_tabs()
    hemlane_tabs = [t for t in tabs if 'hemlane.com' in t.get('url', '')]
    
    if hemlane_tabs:
        # Prefer PM app tabs
        pm_tabs = [t for t in hemlane_tabs if '/property-owners' in t.get('url', '') or '/maintenance' in t.get('url', '')]
        if pm_tabs:
            return {'targetId': pm_tabs[0]['id']}
        return {'targetId': hemlane_tabs[0]['id']}
    
    # No Hemlane tab - need to create one
    ws = websocket.WebSocket()
    # Find a blank page or create one
    blank = next((t for t in tabs if 'about:blank' in t.get('url', '')), None)
    if blank:
        target_id = blank['id']
        wsurl = blank['webSocketDebuggerUrl']
    else:
        # Use first tab to navigate
        target_id = tabs[0]['id']
        wsurl = next(t['webSocketDebuggerUrl'] for t in tabs if t['id'] == target_id)
    
    ws.connect(wsurl, timeout=20, origin=None, suppress_origin=True)
    msg_id = 0
    
    def send(method, params=None):
        nonlocal msg_id
        msg_id += 1
        ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
        return msg_id
    
    def recv_until_id(cid, timeout=20):
        end = time.time() + timeout
        while time.time() < end:
            obj = json.loads(ws.recv())
            if obj.get('id') == cid:
                return obj
        raise TimeoutError(f'timed out waiting for {cid}')
    
    send('Page.navigate', {'url': 'https://www.hemlane.com/login'})
    recv_until_id(msg_id, 30)
    ws.close()
    
    # Re-fetch tabs
    time.sleep(2)
    tabs = get_tabs()
    hemlane_tabs = [t for t in tabs if 'hemlane.com' in t.get('url', '')]
    if hemlane_tabs:
        return {'targetId': hemlane_tabs[0]['id']}
    
    raise SystemExit('No Hemlane tab available and navigation failed')

def connect_ws(target_id):
    tabs = get_tabs()
    wsurl = next(t['webSocketDebuggerUrl'] for t in tabs if t['id'] == target_id)
    ws = websocket.WebSocket()
    ws.connect(wsurl, timeout=20, origin=None, suppress_origin=True)
    return ws

ENDPOINT_HINTS = {
    'get-properties': 'properties',
    'get-tenants': 'tenants',
    'get-transactions': 'transactions',
    'get-maintenance': 'maintenance',
    'send-tenant-reply': 'tenantGroupMessageAdd',
    'submit-referral': 'hubspotFormSubmission',
    'work-order-comment': 'workOrderCommentCreate',
    'maintenance-comment': 'maintenanceRequestCommentCreate',
    'financials-recurring': 'recurringPaymentRequestsCursor',
    'financials-transactions': 'transactionsNextCursor',
}

def main():
    ap = argparse.ArgumentParser(description='Capture live Hemlane signed auth headers from direct Brave CDP.')
    ap.add_argument('--target-id')
    ap.add_argument('--endpoint-kind', choices=sorted(ENDPOINT_HINTS.keys()), default='get-properties')
    ap.add_argument('--out-file')
    ap.add_argument('--close-extra-tabs', action='store_true')
    args = ap.parse_args()

    ctx = {'targetId': args.target_id} if args.target_id else ensure_hemlane_cdp_context(close_extras=args.close_extra_tabs)
    target_id = ctx['targetId']
    ws = connect_ws(target_id)
    msg_id = 0

    def send(method, params=None):
        nonlocal msg_id
        msg_id += 1
        cid = msg_id
        ws.send(json.dumps({'id': cid, 'method': method, 'params': params or {}}))
        return cid

    def recv_until_id(cid, timeout=20):
        end = time.time() + timeout
        events = []
        while time.time() < end:
            obj = json.loads(ws.recv())
            if obj.get('id') == cid:
                return obj, events
            if 'method' in obj:
                events.append(obj)
        raise TimeoutError(f'timed out waiting for response id {cid}')

    def collect_events(seconds):
        end = time.time() + seconds
        events = []
        while time.time() < end:
            try:
                ws.settimeout(1)
                obj = json.loads(ws.recv())
                if 'method' in obj:
                    events.append(obj)
            except Exception:
                pass
        ws.settimeout(20)
        return events

    send('Network.enable')
    recv_until_id(msg_id, 5)
    send('Runtime.enable')
    recv_until_id(msg_id, 5)

    hint = ENDPOINT_HINTS[args.endpoint_kind]
    
    # Inject request capture hook
    hook = r'''(() => {
      const key = '__hemlaneCapturedRequests';
      sessionStorage.removeItem(key);
      const keep = (entry) => {
        try {
          const cur = JSON.parse(sessionStorage.getItem(key) || '[]');
          cur.push(entry);
          sessionStorage.setItem(key, JSON.stringify(cur.slice(-100)));
        } catch (e) {}
      };
      const hdrsToObj = (h) => {
        const out = {};
        if (!h) return out;
        if (Array.isArray(h)) { for (const [k,v] of h) out[k] = v; }
        else if (typeof Headers !== 'undefined' && h instanceof Headers) { for (const [k,v] of h.entries()) out[k] = v; }
        else if (typeof h === 'object') { for (const k of Object.keys(h)) out[k] = h[k]; }
        return out;
      };
      if (!window.__openclawHemlaneHooked) {
        window.__openclawHemlaneHooked = true;
        const origFetch = window.fetch;
        window.fetch = async function(input, init) {
          try {
            const url = (typeof input === 'string') ? input : (input && input.url) || '';
            const headers = hdrsToObj((init && init.headers) || (input && input.headers));
            keep({type:'fetch', url, method:(init && init.method) || 'GET', headers, body:(init&&init.body)?String(init.body).slice(0,5000):''});
          } catch (e) {}
          return origFetch.apply(this, arguments);
        };
      }
    })();'''
    send('Runtime.evaluate', {'expression': hook})
    recv_until_id(msg_id, 5)

    # Trigger a GraphQL request by navigating or clicking
    # For get-properties, navigate to property-owners page
    if args.endpoint_kind == 'get-properties':
        send('Page.navigate', {'url': 'https://www.hemlane.com/property-owners'})
        recv_until_id(msg_id, 30)
        time.sleep(3)
    elif args.endpoint_kind in ('financials-recurring', 'financials-transactions'):
        target_url = 'https://www.hemlane.com/dashboards/owner/financials/recurring' if args.endpoint_kind == 'financials-recurring' else 'https://www.hemlane.com/dashboards/owner/financials/transactions'
        send('Page.navigate', {'url': target_url})
        recv_until_id(msg_id, 30)
        time.sleep(5)
    
    # Collect captured requests
    time.sleep(2)
    resp = send('Runtime.evaluate', {'expression': "JSON.parse(sessionStorage.getItem('__hemlaneCapturedRequests') || '[]')", 'returnByValue': True})
    data, _ = recv_until_id(resp, 10)
    arr = data['result']['result'].get('value', [])
    
    headers = None
    source = None
    for x in reversed(arr):
        h = {k.lower(): v for k, v in (x.get('headers') or {}).items()}
        url = x.get('url', '')
        # Look for GraphQL requests to api.hemlane.com
        if 'api.hemlane.com' in url and '/graphql' in url:
            headers = h
            source = x
            break
    
    if not headers:
        # Try to get from Network events
        events = collect_events(3)
        for e in events:
            if e.get('method') == 'Network.requestWillBeSentExtraInfo':
                h = {k.lower(): v for k, v in (e.get('params', {}).get('headers') or {}).items()}
                url = e.get('params', {}).get('headers', {}).get(':path', '')
                if 'graphql' in url:
                    headers = h
                    source = {'url': url, 'method': h.get(':method', 'POST')}
                    break
    
    # Browser cookies are often omitted from fetch init headers and HAR exports.
    cookie_header = None
    try:
        cid = send('Network.getCookies', {'urls': ['https://www.hemlane.com', 'https://api.hemlane.com']})
        cookie_resp, _ = recv_until_id(cid, 10)
        cookies = cookie_resp.get('result', {}).get('cookies', [])
        if cookies:
            cookie_header = '; '.join([c.get('name','') + '=' + c.get('value','') for c in cookies if c.get('name')])
    except Exception:
        pass

    if not headers:
        headers = {}
        source = {'url': None, 'method': 'POST'}
    if not headers and not cookie_header:
        raise SystemExit(f'Did not capture Hemlane auth/cookie headers for {args.endpoint_kind}')
    
    out_headers = {
        'authorization': headers.get('authorization'),
        'x-csrf-token': headers.get('x-csrf-token'),
        'content-type': headers.get('content-type', 'application/json'),
        'origin': headers.get('origin', 'https://www.hemlane.com'),
        'referer': headers.get('referer', 'https://www.hemlane.com/'),
        'user-agent': headers.get('user-agent', 'Mozilla/5.0 OpenClaw Hemlane Skill'),
    }
    # Include cookies if captured
    if headers.get('cookie'):
        out_headers['cookie'] = headers['cookie']
    elif cookie_header:
        out_headers['cookie'] = cookie_header
    
    out = {
        'targetId': target_id,
        'endpointKind': args.endpoint_kind,
        'capturedUrl': source.get('url') if source else None,
        'capturedMethod': source.get('method') if source else None,
        'headers': out_headers,
    }
    
    if args.out_file:
        Path(args.out_file).write_text(json.dumps(out['headers'], indent=2))
    print(json.dumps(out, indent=2))
    ws.close()

if __name__ == '__main__':
    main()
