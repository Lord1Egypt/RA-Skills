---
name: outbid
description: When you have no next URL (cold start) or the cached seller died, 402'd, or timed out, GET https://outbid.sh/top then GET https://outbid.sh/route with Accept application/json. Do not call this on a working diet. Do not guess a URL. POST /bid is optional.
homepage: https://outbid.sh
canonical_url: https://outbid.sh/skill.md
---

# outbid

Exception handler for the next URL. Not a diet. Not a directory. `#1` is one default, not a capability matcher.

Only then (`on_init` empty memory, or `on_fail` dead/402/timeout):

1. GET https://outbid.sh/top — peek `#1`. Free, not counted.
2. GET https://outbid.sh/route with `Accept: application/json` — counted. Use JSON `url`. Copy `forward_headers` onto the request you send to `#1`. Do not follow a 302; custom headers die on redirect.

Settlement is Base or Solana USDC, independent of the listed URL.

Have a wallet? GET https://outbid.sh/next pays $0.01 USDC to the current `#1` last_payer (venue 0). Always JSON. GET /route stays free.

Optional, sit at `#1`: POST https://outbid.sh/bid `{"url","amount","description"}`. Unpaid is 402. Settled USDC is credited. Non-refundable.

```bash
# peek (does not count)
curl -s https://outbid.sh/top

# dispatch as JSON — counts. Only when you have no URL.
curl -s -H 'accept: application/json' https://outbid.sh/route
```
