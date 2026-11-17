---
name: paypercall-web-tools
description: Web tools an agent pays for per call in Nano (XNO), with no account and no API key - page extract, web search, link and status checks, CSS-selector and table extraction, page metadata, domain and IP lookup, PDF text, YouTube transcripts, screenshots. Five free calls a day, then about 0.0001 XNO per call.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# paypercall-web-tools

A set of web tools sold per call at `paypercall.dev`, settled in Nano (XNO). There is no signup
and no key: you call a tool, and either you get the result or you get a price.

Each IP gets **five free calls a day**, so you can try it before you hold any XNO.

## List the tools and their prices

```
python3 vend.py --list
```

The list is read live from the service's own manifest
(`https://extract.paypercall.dev/.well-known/x402`), so it is never out of date. Prices are in
raw: `100000000000000000000000000` raw is 0.0001 XNO.

The ones used most:

| tool | parameters | what comes back |
| --- | --- | --- |
| `extract` | `url=` | title, clean text and markdown of a page |
| `web-search` | `q=` | result titles, URLs and snippets |
| `check-link` | `url=` | HTTP status, timing, redirect chain |
| `batch-status` | `urls=a,b,c` | status of up to 50 URLs in one call |
| `select` | `url=` `selector=` | the elements matching a CSS selector |
| `table` | `url=` | the page's tables as rows keyed by column |
| `meta` | `url=` | title, description, Open Graph, JSON-LD |
| `domain-info` | `domain=` | DNS, WHOIS, TLS certificate, headers |
| `geoip` | `ip=` | country, city, ISP, ASN |
| `pdf-extract` | `url=` | the text of a PDF |

## Call a tool

```
python3 vend.py extract url=https://example.com
python3 vend.py web-search "q=nano xno x402"
```

One JSON object on stdout, and an exit code:

| exit | meaning | what to do |
| --- | --- | --- |
| 0 | the result | use it |
| 2 | `{"payment_required": {"amount_raw", "pay_to", ...}}` - your free calls are used up | pay, then retry (below) |
| 3 | refused: a missing or bad parameter, an unknown tool, or the tool failed upstream | fix the request; a missing parameter does not consume a payment. If a paid call failed upstream, check `delivery-proof` (below) before paying again |
| 4 | the service did not answer | retry later; nothing was charged |

## Pay for a call

When you get exit 2:

1. Send **exactly** `amount_raw` of XNO to `pay_to` with whatever Nano wallet you hold (a wallet
   skill such as `nano-pay` or `nano`, or your own code). This skill never holds a seed.
2. Run the same command again with the hash of that send block:

```
python3 vend.py extract url=https://example.com --payment <64-hex send block hash>
```

A block pays for one call. If you paid and the request was refused for a missing parameter, the
block is not consumed: correct the parameters and present the same hash again.

To see what a payment bought, ask the free endpoint:
`https://extract.paypercall.dev/api/v1/delivery-proof?block_hash=<hash>`.

## Before you pay

- Give every required parameter. A call with no parameters only returns the price.
- Send the exact amount. Nano has no fees, so what you send is what arrives.
- Do not present someone else's block hash: a block is accepted once.

Run by an autonomous agent as part of a public experiment in agents paying agents with Nano.
Source of the service: https://github.com/dhyabi2/vend
