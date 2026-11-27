---
name: grantusage-window-check
description: Check licensing-window availability facts for film/TV titles on streaming platforms (Apple TV, Crunchyroll, Rakuten TV, Pluto TV, Roku Channel, Samsung TV Plus). Query the latest observation, expiring windows, and public window conflicts; fetch verifiable evidence packs (x402 paid). Records observable facts only - no ownership determination, no legal advice.
metadata:
  version: 1.0.0
  author: GrantUsage
  homepage: https://grantusage.com
---

# GrantUsage Licensing-Window Check

Verify what a streaming platform actually shows, right now, for a title, in a
territory - and compare it against the declared licensing window.

## When to use

- "Is <title> still available on <platform> in <territory>?" (availability fact)
- "Which windows in the public list expire this week?"
- "Show me public declaration-vs-fact conflicts (window expired but still listed)."
- "Get the verifiable evidence pack for case #N." (paid, x402)

## Endpoint

MCP server (streamable HTTP): `https://grantusage.com/mcp` - JSON-RPC 2.0.

## Tools (free, no signup, no API key)

### check_availability
```bash
curl -sS https://grantusage.com/mcp -H 'Content-Type: application/json' -d '{
  "jsonrpc":"2.0","id":1,"method":"tools/call",
  "params":{"name":"check_availability","arguments":
    {"platform":"Apple TV","title":"Ted Lasso","territory":"DE"}}}'
```
Returns the latest observation (observable / http_status / content_hash /
observed_at) and an evidence-page link when a case exists.

### list_expiring
```bash
curl -sS https://grantusage.com/mcp -H 'Content-Type: application/json' -d '{
  "jsonrpc":"2.0","id":1,"method":"tools/call",
  "params":{"name":"list_expiring","arguments":{"days":14}}}'
```

### list_conflicts
```bash
curl -sS https://grantusage.com/mcp -H 'Content-Type: application/json' -d '{
  "jsonrpc":"2.0","id":1,"method":"tools/call",
  "params":{"name":"list_conflicts","arguments":{}}}'
```
Public A/B-grade conflicts only (declaration vs. observable fact). C-grade
"exposure" rows are deliberately excluded.

### get_evidence_bundle (paid, x402)
Same JSON-RPC; without payment the server answers HTTP 402 with an x402 offer
(USDC on Base, eip155:8453, $0.05/call). Pay the offer, retry with the
`X-PAYMENT` header to receive timeline + snapshot hashes + independent
timestamps + declaration source.

## Scope discipline (keep this wording)

- Verdicts record **observable facts and declaration conflicts** - "window
  expired but still listed", "still listed", "effective but not yet listed".
- Never say "infringement", "unlawful", or "we can help you recover money" -
  this service performs no ownership determination and gives no legal advice.
- Self-built observation policy: public pages only, honest UA, rate limited,
  no logins, no geo-spoofing, no DRM circumvention -
  https://grantusage.com/verifier

## More

- Public conflict list: https://grantusage.com/conflicts
- Free self-check (1 title x 3 territories): https://grantusage.com/app
- Machine-readable docs: https://grantusage.com/llms-full.txt
- Contact: hello@foxreply.com
