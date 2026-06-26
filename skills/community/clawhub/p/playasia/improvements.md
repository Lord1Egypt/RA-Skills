# L402 Agentic Platform — Improvements

## Done

- Three purchase methods: Wallet (instant), Lightning (instant/anonymous), Bitcoin on-chain (anonymous)
- Smart routing: `POST /buy` — token present = wallet, absent = anonymous BTC/LN
- `GET /order` with `sid` for anonymous order tracking
- `POST /account/topup` with optional `method` (bitcoin/lightning/browser)
- Auth docs: skill file, info JSON, HTML page all document three methods
- Error handling table in skill + README
- Code examples in README
- Stored XSS fix (strip_tags on all user inputs)
- Rate limiting on all endpoints + address burn protection (3 unpaid/IP)
- Token update restricted via API (can only rename + lower limits)
- Real-time mempool polling on `/order` for unpaid BTC orders
- `mark_displayed` on API delivery (prevents code recycling)
- Skill URL in info JSON + linked from HTML page
- `.well-known/ai-plugin.json` and `.well-known/mcp.json` updated
- Stock check on anonymous buy (uses lookup table `on_sale` flag)
- English product names in catalog search
- Admin monitoring page (`agentic.php`) with 5 tabs
- Frontend access token page with usage stats + activity log
- `deploy.sh` for ClawHub publishing

## TODO

### Cloudflare
- Grok reported Cloudflare challenge blocking `curl` access to `/l402/v1/skill`
- May need a WAF page rule or exception for `/l402/v1/*` API paths
- Critical for agent discovery — if they can't fetch the skill file, they can't use the API

### Webhook for order confirmation
```
POST /l402/v1/webhooks
{ "event": "order.paid", "url": "https://your-agent.com/callback" }
```
Eliminates polling for anonymous BTC orders. Significant effort.

### Batch purchasing
```
POST /l402/v1/batch
{ "items": [{"pax":"A", "qty":1}, {"pax":"B", "qty":2}] }
```
Nice for power users. Low priority.

### Invoice QR code
Return base64 PNG QR in the `/buy` response for easy mobile Lightning payments.

### HTML page rework
- The `/l402` developer page could show purchase flow diagrams
- Consider rendering the skill markdown as HTML for browser visitors

### Doc sync
Keep in sync on changes: `SKILL.md`, inline skill in `l402.php`, `README.md`, `.well-known/*.json`, HTML page.
