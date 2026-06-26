---
name: x402-news-search-skill
description: Agent skill for x402-paid global news aggregation and source/time-filtered search.
version: 1.0.0
---

# x402 News Search Skill (Local Only)

Use this skill to let your AI agent search global news via:

- API base: `https://www.x402api.app/`
- Endpoint: `POST /api/v1/news/search`
- Payment: x402 pay-per-call

This is a news aggregation capability: your agent can search across web-indexed news sources, including major US and European outlets, and can filter by source domain and publication time.

## What this skill is for

- Search broad global news by keyword
- Filter by source domain (for example `cnn.com`, `bloomberg.com`, `ft.com`)
- Filter by publication time range (`time_published`)
- Keep the same x402 payment flow used by your other endpoints

## Environment variables

```bash
EVM_PRIVATE_KEY=0x_your_private_key
API_BASE_URL=https://www.x402api.app/
```

## API contract

Endpoint:

`POST /api/v1/news/search`

Body example:

```json
{
  "query": "Federal Reserve rates",
  "limit": 10,
  "time_published": "7d",
  "source": "bloomberg.com",
  "country": "US",
  "lang": "en"
}
```

### Parameters

- `query` (required): search keywords
- `limit` (optional): `1-500`, default `10`
- `time_published` (optional): time filter (for example `anytime`, `1h`, `1d`, `7d`, `1y`)
- `source` (optional): source domain filter, for example `cnn.com`
- `country` (optional): 2-letter country code, default `US`
- `lang` (optional): 2-letter language code, default `en`

## x402 payment flow (same pattern as your other APIs)

1. Call the endpoint without payment and get `402 Payment Required`.
2. Parse payment requirements from response headers.
3. Create and sign payment payload.
4. Retry with payment signature header.
5. Read final response body.

## Example buyer code

```ts
import { x402Client, x402HTTPClient } from "@x402/core/client";
import { ExactEvmScheme, toClientEvmSigner } from "@x402/evm";
import { createPublicClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const baseUrl =
  process.env.X402_API_BASE_URL ??
  process.env.API_BASE_URL ??
  "https://www.x402api.app/";
const endpoint = `${baseUrl.replace(/\/$/, "")}/api/v1/news/search`;

async function main() {
  const privateKey = process.env.EVM_PRIVATE_KEY;
  if (!privateKey) throw new Error("Missing EVM_PRIVATE_KEY");
  if (!privateKey.startsWith("0x")) throw new Error("EVM_PRIVATE_KEY must start with 0x");

  const account = privateKeyToAccount(privateKey as `0x${string}`);
  const publicClient = createPublicClient({ chain: base, transport: http() });
  const signer = toClientEvmSigner(account, publicClient);
  const client = new x402Client().register("eip155:*", new ExactEvmScheme(signer));
  const httpClient = new x402HTTPClient(client);

  const payload = {
    query: "AI chip demand",
    limit: 10,
    time_published: "7d",
    source: "reuters.com",
    country: "US",
    lang: "en",
  };

  const unpaid = await fetch(endpoint, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (unpaid.status !== 402) {
    const text = await unpaid.text();
    throw new Error(`Expected 402, got ${unpaid.status}. body=${text}`);
  }

  const required = httpClient.getPaymentRequiredResponse(
    (name) => unpaid.headers.get(name),
    {},
  );
  const paymentPayload = await httpClient.createPaymentPayload(required);

  const paid = await fetch(endpoint, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      ...httpClient.encodePaymentSignatureHeader(paymentPayload),
    },
    body: JSON.stringify(payload),
  });

  const result = await paid.json();
  if (!paid.ok) throw new Error(`Request failed: ${paid.status} ${JSON.stringify(result)}`);
  console.log(result);
}

void main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```

## News aggregation coverage (major outlets)

The search can cover web-indexed mainstream media, including but not limited to:

### United States

- The New York Times (`nytimes.com`)
- The Washington Post (`washingtonpost.com`)
- The Wall Street Journal (`wsj.com`)
- Bloomberg (`bloomberg.com`)
- Reuters (`reuters.com`)
- Associated Press (`apnews.com`)
- CNN (`cnn.com`)
- Fox News (`foxnews.com`)
- NBC News (`nbcnews.com`)
- ABC News (`abcnews.go.com`)
- CBS News (`cbsnews.com`)
- USA Today (`usatoday.com`)
- Los Angeles Times (`latimes.com`)
- Politico (`politico.com`)
- Axios (`axios.com`)
- Business Insider (`businessinsider.com`)
- Forbes (`forbes.com`)
- The Atlantic (`theatlantic.com`)
- Time (`time.com`)
- Newsweek (`newsweek.com`)

### Europe / UK

- Financial Times (`ft.com`)
- The Economist (`economist.com`)
- BBC News (`bbc.com`)
- Reuters Europe coverage (`reuters.com`)
- The Guardian (`theguardian.com`)
- The Times (`thetimes.co.uk`)
- The Telegraph (`telegraph.co.uk`)
- Sky News (`news.sky.com`)
- Euronews (`euronews.com`)
- POLITICO Europe (`politico.eu`)
- Le Monde (`lemonde.fr`)
- Le Figaro (`lefigaro.fr`)
- AFP (`afp.com`)
- Der Spiegel (`spiegel.de`)
- Die Zeit (`zeit.de`)
- Frankfurter Allgemeine Zeitung (`faz.net`)
- Handelsblatt (`handelsblatt.com`)
- El País (`elpais.com`)
- El Mundo (`elmundo.es`)
- Corriere della Sera (`corriere.it`)
- La Repubblica (`repubblica.it`)
- ANSA (`ansa.it`)
- NRC (`nrc.nl`)
- De Telegraaf (`telegraaf.nl`)
- Swissinfo (`swissinfo.ch`)

> Note: Coverage depends on upstream indexing and availability; this list represents major outlets that are commonly discoverable.

## Recommended agent behaviors

- If the user specifies a media brand, map it to domain and set `source`.
- If the user asks “latest”, set a tighter `time_published` (like `1d` or `7d`) and then sort/compare timestamps.
- If result count is low, remove `source` first, then expand time range.
- Always surface source domain + publish time in final answer.

## Error handling

- `402 Payment Required`: generate payment payload and retry.
- `invalid_json_body` (`400`): send valid JSON.
- `invalid_news_request` (`400`): fix query/limit/source format.
- `news_upstream_auth_failed` (`502`): server-side upstream auth issue.
- `news_upstream_rate_limited` (`429`): retry with backoff.
- `news_upstream_error` (`502`): transient upstream failure, retry.

