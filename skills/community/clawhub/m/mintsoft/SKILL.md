---
name: mintsoft
description: "Mintsoft warehouse-management API wrapper — query warehouses, orders, products, stock levels, ASNs, and the Product Usage stock-flow report from a single ms-apikey credential."
homepage: https://api.mintsoft.co.uk/swagger/index.html
metadata:
  {
    "openclaw":
      {
        "emoji": "📦",
        "requires":
          {
            "bins": ["python3"],
            "env": ["MINTSOFT_API_KEY"],
          },
        "primaryEnv": "MINTSOFT_API_KEY",
      },
  }
---

# Mintsoft

Run the bundled `scripts/mintsoft_api.py` for every Mintsoft operation. It wraps the public REST API at `https://api.mintsoft.co.uk/api` and prints JSON to stdout.

```bash
python3 "{baseDir}/scripts/mintsoft_api.py" <command> [options]
```

Background: Mintsoft is a UK warehouse-management / 3PL platform. The API authenticates via an `ms-apikey` header. Tokens are tenant-scoped and **valid for 24 hours**; refresh with `auth` whenever the cached token expires.

## First run — install the one Python dependency

The script uses [`httpx`](https://www.python-httpx.org/). If `whoami` fails with `ModuleNotFoundError: No module named 'httpx'`, install it once:

```bash
python3 -c "import httpx" || python3 -m pip install httpx
```

## Auth — two paths

**Preferred: provide a long-lived key directly.**

```bash
export MINTSOFT_API_KEY="<your-api-key>"
python3 "{baseDir}/scripts/mintsoft_api.py" whoami
```

**Alternative: log in once with username/password to mint and cache a key.**

```bash
export MINTSOFT_USERNAME="you@example.com"
export MINTSOFT_PASSWORD="…"
python3 "{baseDir}/scripts/mintsoft_api.py" auth
# → caches the returned key to ~/.config/mintsoft-skill/token.json (mode 0600, 24h TTL)
python3 "{baseDir}/scripts/mintsoft_api.py" whoami
# → {"authenticated": true, "source": "cache (~/.config/mintsoft-skill/token.json)", "warehouse_count": N}
```

`whoami` is also the safest first command to run — it confirms which credential source is being used and that the API accepts it. If neither env var nor cached token is present, every command exits non-zero with a clear error.

## Workflow rules

1. **Warehouses first**, then drill. Most stock/inventory queries need a `WarehouseId` — fetch the warehouse list once per session and reuse the IDs.
2. **`--summary` by default on list commands.** Mintsoft list endpoints return verbose objects; full output saturates context fast. Only drop `--summary` after the user asks for full detail or you've narrowed by ID.
3. **Filter at the API, not in post.** Every list command exposes the same date/status/warehouse filters the Mintsoft UI uses — push those down rather than paginating everything and filtering locally.
4. **Pagination has a deadline.** The script caps long pagination at `--timeout 90` (seconds) by default and emits a `warning` to stderr if it stops early. Bump `--timeout 0` only when you genuinely need an unbounded sweep.

## Commands

### Warehouses

```bash
python3 "{baseDir}/scripts/mintsoft_api.py" warehouses --summary
python3 "{baseDir}/scripts/mintsoft_api.py" warehouses          # full object per warehouse
```

### Orders

```bash
python3 "{baseDir}/scripts/mintsoft_api.py" orders --summary
python3 "{baseDir}/scripts/mintsoft_api.py" orders --status Dispatched --summary
python3 "{baseDir}/scripts/mintsoft_api.py" orders --since 2026-01-01 --limit 200 --summary
python3 "{baseDir}/scripts/mintsoft_api.py" orders --include-items --limit 50
python3 "{baseDir}/scripts/mintsoft_api.py" order <OrderID>
```

### Stock levels (cross-warehouse aggregate)

```bash
python3 "{baseDir}/scripts/mintsoft_api.py" stock-levels --summary
python3 "{baseDir}/scripts/mintsoft_api.py" stock-levels --breakdown   # per-warehouse split
```

### Inventory (per-warehouse)

```bash
python3 "{baseDir}/scripts/mintsoft_api.py" inventory --warehouse <WarehouseID> --summary
python3 "{baseDir}/scripts/mintsoft_api.py" inventory --warehouse <WarehouseID> --since 2026-01-01
```

### Products

```bash
python3 "{baseDir}/scripts/mintsoft_api.py" products --summary --limit 100
python3 "{baseDir}/scripts/mintsoft_api.py" product <ProductID>
```

### ASN (Advanced Shipping Notices)

```bash
# Open ASNs in a date window
python3 "{baseDir}/scripts/mintsoft_api.py" asn-list --from-date 2026-06-01 --to-date 2026-06-30 --summary

# Filter by status (semicolon-separated ids — e.g. 1=Pending, 2=Confirmed)
python3 "{baseDir}/scripts/mintsoft_api.py" asn-list --from-date 2026-06-01 --status "1;2" --summary

# Single ASN detail
python3 "{baseDir}/scripts/mintsoft_api.py" asn <ASN_ID>
```

ASN list items always include `Items` (per-SKU expected/received/booked quantities) so you can compare what was promised vs what arrived without a second call.

### Product Usage Report (stock flow)

Same dataset as Mintsoft's Reports → Overview → Product Usage Report. Supports filtering by flow direction, date range, warehouse, client, product, or free-text search.

```bash
# All outbound movements in a month
python3 "{baseDir}/scripts/mintsoft_api.py" product-usage --flow OUT --from-date 2026-06-01 --to-date 2026-06-30 --summary

# Specific SKU across all flow types
python3 "{baseDir}/scripts/mintsoft_api.py" product-usage --search "WIDGET-001" --from-date 2026-06-01 --summary

# Full detail with location/batch/serial breakdown (no --summary)
python3 "{baseDir}/scripts/mintsoft_api.py" product-usage --flow OUT --from-date 2026-06-01 --include-details
```

`--flow` values: `IN`, `OUT`, `ALLOCATE`, `UNALLOCATE`.

## Output shape

Every list command emits:

```json
{ "count": N, "<resource>": [ … ] }
```

`<resource>` matches the command name (`orders`, `warehouses`, `stock_levels`, `inventory`, `products`, `asns`, `product_usage`). Single-record commands print the resource directly. Errors print `{"error": "…", "detail": "…"}` to stdout and exit non-zero.

## Useful patterns

- **Stock review across warehouses.** `warehouses --summary` → for each `ID`, `inventory --warehouse <ID> --summary` → aggregate by SKU client-side.
- **Outbound shipment audit.** `product-usage --flow OUT --from-date <start> --to-date <end> --summary` matches the data behind the "Mintsoft Outbound" report and is a drop-in for that workbook tab.
- **ASN reconciliation.** `asn-list --from-date <start>` then compare `QuantityExpected` vs `QuantityReceived` per line in the response.

## Notes

- The API has rate limits; the script retries `429` with `Retry-After` headroom.
- The Mintsoft API has a long-standing typo on ASN items (`QuantityReceieved`). The script normalises that to `QuantityReceived` in summary output but the raw passthrough preserves the upstream spelling.
- Token cache lives under `~/.config/mintsoft-skill/` (override via `MINTSOFT_CONFIG_DIR`). It contains a Mintsoft API key — treat it as a secret.
- Endpoint reference: <https://api.mintsoft.co.uk/swagger/index.html>.
