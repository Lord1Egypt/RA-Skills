---
name: pg-sell
description: Use when selling API capacity on ProxyGate — creating listings, managing listings (update/pause/delete), rotating keys, uploading docs, starting tunnels, managing headers, viewing earnings, or exposing local services. Make sure to use this skill whenever someone mentions "list API", "sell capacity", "create listing", "start tunnel", "expose service", "earnings", "go live", "monetize API", "rotate key", "pause listing", or wants to make their API available on ProxyGate.
---

# ProxyGate — Sell API Capacity

Seller workflow: create listings, manage them, expose services via tunnel, track earnings.

## Process

### 1. Scaffold a project (optional)

If building a new service from scratch:

```bash
proxygate create                                    # interactive
proxygate create my-agent --template http-api --port 3000
proxygate create my-agent --template llm-agent --port 8080
```

Templates: `http-api` (Hono REST API), `llm-agent` (Hono + LLM provider + streaming).

### 2. Test locally

Validate endpoints before going live:

```bash
proxygate test                                      # auto-detect from tunnel config
proxygate test --endpoint "POST /v1/analyze" --payload '{"code":"x=1"}'
proxygate test -c proxygate.tunnel.yaml
```

### 3. Create a listing

```bash
proxygate listings create    # interactive — walks through service, pricing, description, docs
```

Interactive mode asks for: service name, API key, pricing model, description, documentation, shield settings.

Non-interactive:
```bash
proxygate listings create --non-interactive \
  --service-name "My API" \
  --base-url "https://api.example.com" \
  --auth-pattern bearer \
  --api-key "your-api-key" \
  --price 5000 \
  --total-rpm 100 \
  --categories ai \
  --description "Fast Llama 3.3 access"
```

### 4. Manage listings

```bash
# View listings
proxygate listings list                     # list your listings
proxygate listings list --table             # table format with status, RPM, price

# Update a listing
proxygate listings update <id> --price 3000 --description "Updated pricing"

# Pause/unpause (stop accepting requests temporarily)
proxygate listings pause <id>
proxygate listings unpause <id>

# Delete permanently
proxygate listings delete <id>

# Rotate API key or OAuth2 credentials (no downtime)
proxygate listings rotate-key <id> --key <new-api-key>
proxygate listings rotate-key <id> --oauth2 <new-token>

# Upload API documentation
proxygate listings upload-docs <id> ./openapi.yaml    # OpenAPI or markdown

# View docs for your listing
proxygate listings docs <id>

# Manage upstream headers
proxygate listings headers <id>                        # list current headers
proxygate listings headers <id> set X-Custom "value"   # add/update header
proxygate listings headers <id> unset X-Custom         # remove header
```

### 5. Configure tunnel

Create `proxygate.tunnel.yaml`:

```yaml
services:
  - name: my-api
    port: 8080
    price_per_request: 1000           # lamports (0.001 USDC)
    description: My AI service
    docs: ./openapi.yaml              # auto-uploaded on connect
    endpoints:
      - method: POST
        path: /v1/analyze
        description: Analyze code
    paths:
      - /v1/*
```

Per-token pricing:
```yaml
services:
  - name: llm-service
    port: 3000
    pricing_unit: per_token
    price_per_input_token: 100
    price_per_output_token: 300
```

### 6. Start tunnel

```bash
# Development (request logging + config file watching + auto-reload)
proxygate dev
proxygate dev -c my-services.yaml

# Production (stable connection, auto-reconnect, graceful drain on Ctrl+C)
proxygate tunnel
proxygate tunnel -c proxygate.tunnel.yaml
```

Dev mode shows live request/response logs with status, latency, and size. Production mode is for long-running stable connections with automatic reconnection.

### 7. Check earnings

```bash
proxygate settlements                              # earnings summary
proxygate settlements -r seller                    # seller-specific view
proxygate settlements -s weather-api --from 2026-03-01  # filtered
proxygate balance                                  # current balance
proxygate listings list --table                    # listing status overview
```

## SDK — Programmatic Serving

```typescript
import { ProxyGate, ProxyGateClient } from '@proxygate/sdk';

// One-liner: expose services immediately
const tunnel = await ProxyGate.serve({
  keypair: '~/.proxygate/keypair.json',
  services: [
    { name: 'code-review', port: 3000, docs: './openapi.yaml' },
  ],
  onConnected(listings) { console.log('Live!', listings); },
});

// Or via client for more control
const client = await ProxyGateClient.create({
  keypairPath: '~/.proxygate/keypair.json',
});

// Manage listings programmatically
const { listings } = await client.listings.list();
await client.listings.update('listing-id', { price_per_request: 3000 });
await client.listings.pause('listing-id');
await client.listings.unpause('listing-id');
await client.listings.rotateKey('listing-id', { api_key: 'your-new-api-key' });
await client.listings.uploadDocs('listing-id', {
  doc_type: 'openapi',
  content: fs.readFileSync('./openapi.yaml', 'utf-8'),
});

// Start tunnel
const tunnel = await client.serve([
  { name: 'my-api', port: 3000 },
]);

// Graceful shutdown (waits for in-flight requests)
await tunnel.drain();
tunnel.disconnect();
```

## Success criteria

- [ ] Service running locally and responding to requests
- [ ] Listing created (visible in `proxygate listings list`)
- [ ] Tunnel connected (dev or production mode)
- [ ] Incoming requests visible in dev mode logs

## Related skills

| Need | Skill |
|------|-------|
| First-time setup | `pg-setup` |
| Buy API access | `pg-buy` |
| Sell API capacity | **This skill** |
| Job marketplace | `pg-jobs` |
| Check status | `pg-status` |
| Update CLI/SDK | `pg-update` |
