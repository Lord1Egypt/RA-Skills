---
name: google-index-checker
version: 1.1.0
description: Check Google indexed page count for any domain using the "site:" search operator in Chrome Remote Debugging Protocol (CDP on localhost:9222). Use when the user wants to check how many pages Google has indexed for a website, compare indexing across multiple domains, or monitor SEO indexing status. Supports single or multiple domains with comparison table output.
---

# Google Index Checker

Check the number of indexed pages for any domain(s) using Google's `site:` search operator via Chrome Remote Debugging Protocol (CDP) on `localhost:9222`.

## Prerequisites

- Chrome running with `--remote-debugging-port=9222`
- Node.js with `ws` npm package available at `/tmp/wsclient/node_modules/ws`
  - Install once: `npm install ws --prefix /tmp/wsclient`
  - If not found, install before starting

## Connection Info

- **CDP HTTP endpoint**: `http://localhost:9222/json`
- **Important**: Use `localhost:9222`, NOT `127.0.0.1:9222` — Chrome listens on IPv6 `::1`, not IPv4 `127.0.0.1`
- All browser tabs share the same cookie/login session (same Chrome profile)
- After each task, close all tabs and clean up `/tmp/wsclient`

## Instructions

### Step 1: Parse user input

Extract the domain(s) to check. Accept:
- Single: `example.com`, `www.example.com`, `https://example.com`
- Multiple: comma-separated, space-separated, or line-by-line
- Normalize: strip protocol and trailing slashes

### Step 2: Prepare browser connection

1. Install `ws` if needed: `npm install ws --prefix /tmp/wsclient`
2. Create **one** CDP tab: `PUT http://localhost:9222/json/new`
3. Save the `webSocketDebuggerUrl` from the response

### Step 3: Query each domain (reuse same tab)

For each domain, use `Page.navigate` in the **same tab** (do NOT create new tabs):

1. `Page.navigate` → `https://www.google.com/search?q=site:{domain}`
2. Wait for `Page.loadEventFired` + 3 seconds
3. `Runtime.evaluate` → `document.getElementById('result-stats')?.textContent`
4. Parse count from text like `"找到约 12,700 条结果"` using regex `/找到约 ([\d,]+) 条结果/`
5. Strip commas → integer

### Step 4: Present results

#### Single domain
```
**{domain}** has approximately **{count}** pages indexed by Google.
```

#### Multiple domains
```markdown
## Google Index Coverage Report ({date})

| Domain | Indexed Pages | Notes |
|--------|--------------|-------|
| example.com | 13,200 | — |
| example.org | 8,500 | — |
| example.net | 1,200 | — |

Data source: Google `site:` search operator (approximate values)
```

### Step 5: Clean up

1. Close the tab: `DELETE http://localhost:9222/json/close/{targetId}`
2. Verify: `GET http://localhost:9222/json` should return `[]`
3. Remove temp package: `rm -rf /tmp/wsclient`

## CDN Script Template (copy-paste ready)

```javascript
const WebSocket = require('/tmp/wsclient/node_modules/ws');
const http = require('http');

function cdpSend(ws, id, method, params) {
  return new Promise(resolve => {
    const handler = data => {
      const msg = JSON.parse(data);
      if (msg.id === id) resolve(msg);
    };
    ws.on('message', handler);
    ws.send(JSON.stringify({id, method, params}));
  });
}

function extractCount(text) {
  if (!text) return 'NOT_FOUND';
  const m = text.match(/找到约 ([\d,]+) 条结果/);
  return m ? m[1].replace(/,/g, '') : 'PARSE_ERROR:' + text;
}

async function main() {
  // 1. Create one tab
  const target = await new Promise((resolve, reject) => {
    const req = http.request({hostname: 'localhost', port: 9222, path: '/json/new', method: 'PUT'}, res => {
      let d = ''; res.on('data', c => d += c); res.on('end', () => resolve(JSON.parse(d)));
    });
    req.on('error', reject); req.end();
  });

  // 2. Connect WebSocket
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise(r => ws.on('open', r));
  await cdpSend(ws, 1, 'Page.enable', {});
  await cdpSend(ws, 2, 'Runtime.enable', {});

  // 3. Loop through domains
  const domains = [['Name', 'example.com']]; // Replace with actual domains
  for (const [name, domain] of domains) {
    await cdpSend(ws, 10, 'Page.navigate', {url: 'https://www.google.com/search?q=site:' + domain});
    await new Promise(resolve => {
      ws.on('message', data => {
        const msg = JSON.parse(data);
        if (msg.method === 'Page.loadEventFired') resolve();
      });
    });
    await new Promise(r => setTimeout(r, 3000));
    const r = await cdpSend(ws, 11, 'Runtime.evaluate', {expression: "document.getElementById('result-stats')?.textContent || 'NOT_FOUND'"});
    console.log(name + '|' + domain + '|' + extractCount(r.result.result.value));
  }

  // 4. Cleanup
  ws.close();
  http.request({hostname: 'localhost', port: 9222, path: '/json/close/' + target.id, method: 'DELETE'}, () => {}).end();
  await new Promise(r => setTimeout(r, 1000));
  
  // 5. Verify tabs closed
  const remaining = await new Promise((resolve, reject) => {
    const req = http.request({hostname: 'localhost', port: 9222, path: '/json', method: 'GET'}, res => {
      let d = ''; res.on('data', c => d += c); res.on('end', () => resolve(JSON.parse(d)));
    });
    req.on('error', reject); req.end();
  });
  console.log('Tabs remaining:', remaining.length);
  process.exit(0);
}

main().catch(e => { console.error(e); process.exit(1); });
```

## Edge Cases

| Problem | Solution |
|---------|----------|
| `#result-stats` not found | Try `div[id^=result]` or `document.body.innerText` |
| Google CAPTCHA | Take screenshot, stop, report to user |
| 0 results | Check if site is new or blocked by robots.txt |
| `localhost:9222` returns 404 | Chrome not started with `--remote-debugging-port=9222` |
| Tabs accumulate | Always close tab after use, verify with `GET /json` |

## Important Notes

- The `site:` operator returns **approximate** values, not exact counts
- Results vary between Google data centers
- For precise data, use Google Search Console
- One tab, sequential navigation — do NOT create new tabs per domain
