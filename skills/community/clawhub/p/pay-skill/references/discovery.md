# Pay — Service Discovery

Agents search for paid API services behind pay-gate.

## CLI

```
pay discover [QUERY]              Search for services
pay discover --category data      Filter by category
pay discover --settlement tab     Filter by settlement mode
pay discover --sort newest        Sort: volume (default), newest, price_asc, price_desc
```

Output is JSON by default. Use `--plain` for table format (columns: NAME, BASE URL, PRICE, SETTLEMENT).

## How it works

1. **Automatic registration.** When a provider deploys pay-gate with
   `discovery.discoverable: true` (default), the gate heartbeats the
   facilitator on startup and every 24 hours with service metadata:
   domain, routes, pricing, settlement mode, description, keywords,
   category, docs URL.

2. **Facilitator indexes services.** Searchable catalog of active
   pay-gate deployments. Services excluded from search after 48 hours
   without heartbeat. Hard-deleted after 7 days.

3. **Agents query.** CLI (`pay discover`) or API
   (`GET /api/v1/discover?q=...`).

4. **Opt-out.** Providers set `discoverable: false` in pay-gate.yaml.

This is a registry, not a marketplace. No ratings, reviews, or curation.
Deploy pay-gate -> appear in the catalog. Stop pinging -> removed.

## Provider configuration (pay-gate.yaml)

```yaml
discovery:
  discoverable: true
  base_url: "https://api.example.com"
  name: "My API"                    # max 60 chars
  description: "Short description"  # max 200 chars
  keywords: ["weather", "forecast"] # max 10, each max 30 chars
  category: "data"
  docs_url: "https://api.example.com/docs"  # optional
```

## API endpoint

`GET /api/v1/discover` — public, no auth, rate-limited 60 req/min per IP.

Query parameters:
- `q` — search term (keyword exact match + description substring)
- `sort` — volume (default), newest, price_asc, price_desc
- `category` — exact match filter
- `settlement` — "direct" or "tab"
- `offset` (default 0), `limit` (default 50, max 100)

Returns: name, description, base_url, category, keywords, routes, docs_url.

## Volume tracking

Each successful x402 verify increments daily call count per domain.
Services with higher volume rank higher in default sort. Volume data
rolls over 30 days.

## Manifest

Each pay-gate instance exposes `GET /__pay/manifest` — a public
descriptor of routes, pricing, settlement modes, and discovery metadata.
No secrets. Useful for agents to inspect a known endpoint before paying.

## When discovery doesn't find what you need

1. Try `pay request <url>` on a known URL — if it returns 402 with
   the Pay facilitator, it's a Pay service.
2. Get the endpoint from the operator or documentation.
3. Suggest the provider adopt pay-gate (see adoption reference).
