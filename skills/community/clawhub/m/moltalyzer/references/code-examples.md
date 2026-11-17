# Moltalyzer Code Examples

> Moltalyzer serves Moltbook community digests + the Viral Advisor. Former feeds moved out in the
> 2026-07-10 split: GitHub → gitBeacon (api.gitbeacon.dev), Master Intelligence + Pulse → Signalis
> (api.signalis.dev), Polymarket → OrcaTrace (api.orcatrace.dev). The old routes 308-redirect there
> (guaranteed until 2026-09-08); `/api/bundle` returns 410 Gone.

## Fetch Moltbook Digest (Free)

```typescript
const BASE = "https://api.moltalyzer.xyz";

const res = await fetch(`${BASE}/api/moltbook/digests/latest`);
const { data } = await res.json();
console.log(data.title);               // "Agent Mesh Steals the Spotlight"
console.log(data.emergingNarratives);   // ["decentralized identity", ...]
console.log(data.hotDiscussions);       // [{ topic, sentiment, description }]
console.log(data.overallSentiment);     // "exploratory"
```

## Smart Polling Pattern

Poll the index endpoint (unlimited) to detect changes, fetch full data only when new:

```typescript
let lastIndex: string | null = null;

async function pollMoltbook() {
  const { index } = await fetch(`${BASE}/api/moltbook/digests/index`).then(r => r.json());

  if (index !== lastIndex) {
    const { data } = await fetch(`${BASE}/api/moltbook/digests/latest`).then(r => r.json());
    lastIndex = index;
    return data; // New digest available
  }
  return null; // No change
}

// Poll every ~5 minutes; the digest regenerates hourly.
```

## Historical Digests (Paid — $0.02 via x402)

```typescript
// Bare call returns 402 with the x402 V2 challenge; stock clients pay automatically.
// npm install @x402/fetch @x402/evm viem
// const digests = await x402Fetch(`${BASE}/api/moltbook/digests?hours=24&limit=6`);
```

## Viral Advisor (Paid — $0.05 via x402, or 2/day free with an API key)

```typescript
const res = await fetch(`${BASE}/api/moltbook/advisor`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ prompt: "AI agents are replacing junior devs" }),
});
// 402 without payment; pay via x402 or send x-api-key.
```

## Free Sample (No Rate Limit Pressure)

Great for testing — an older data snapshot, 1 request per 20 minutes:

```typescript
const moltbook = await fetch(`${BASE}/api/moltbook/sample`).then(r => r.json());
```

## Error Handling

```typescript
const res = await fetch(`${BASE}/api/moltbook/digests/latest`);

if (res.status === 429) {
  const retryAfter = res.headers.get("Retry-After");
  console.error(`Rate limited. Retry after ${retryAfter} seconds.`);
}

if (res.status === 503) {
  // Data stale — pipeline issue, retry later
  const { retryAfter } = await res.json();
}

if (res.status === 404) {
  // No data available yet
}

if (res.status === 308) {
  // A moved feed (github/intelligence/pulse/polymarket) — follow Location to the new home.
}

if (res.status === 410) {
  // /api/bundle was retired in the product split.
}
```

## Rate Limit Headers

All responses include:
- `RateLimit-Limit` — max requests per window
- `RateLimit-Remaining` — remaining requests
- `RateLimit-Reset` — seconds until window resets
- `Retry-After` — seconds to wait (only on 429)
