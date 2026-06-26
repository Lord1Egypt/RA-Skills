# Fallback Queries (When MCP is Unavailable)

Use the methods in this file only when `mcp.ping()` returns `false`. Under normal circumstances, prioritize the MCP service.

---

## Fallback Query 1: polymarket-cli

Applicable when: MCP service is unavailable and polymarket-cli is installed locally.

> Note: When executing external commands, you must use `execFileSync` (with argument array), do not use template string concatenation to prevent command injection.

```js
const { execFileSync } = require("child_process");

try {
  const raw = execFileSync(
    "polymarket",
    ["portfolio", "trades", address, "--json"],
    { encoding: "utf-8" },
  );
  return JSON.parse(raw);
} catch (_) {}
```

### polymarket-cli Common Commands Reference

```bash
# Query user positions
polymarket portfolio positions <address>

# Query user trade history
polymarket portfolio trades <address>

# Query market info
polymarket markets get <conditionId>

# Search markets
polymarket markets search "<keyword>"

# Output JSON format (for program parsing)
polymarket ... --json
```

Installation: `brew install Polymarket/polymarket-cli/polymarket` or refer to https://github.com/Polymarket/polymarket-cli

---

## Fallback Query 2: Polymarket REST API

Applicable when: Both MCP service and polymarket-cli are unavailable - final fallback.

```js
const url = new URL("https://data-api.polymarket.com/activity");
url.searchParams.set("user", address);
url.searchParams.set("limit", "500");
const res = await fetch(url.toString());
return await res.json();
```

---

## Complete Fallback Chain Example

```js
const { execFileSync } = require("child_process");
const mcp = require("../../polymarket-data-layer/scripts/mcp-client");

async function getActivity(address, days = 30) {
  if (await mcp.ping()) {
    return await mcp.queryWithRetry(`
      SELECT wallet_address AS address, condition_id,
             toUnixTimestamp(traded_at) AS timestamp,
             amount, side, outcome_side
      FROM default.trades
      WHERE wallet_address = '${address.toLowerCase()}'
        AND traded_at >= now() - INTERVAL ${days} DAY
      ORDER BY traded_at DESC
    `);
  }

  // Fallback 1: polymarket-cli
  try {
    const raw = execFileSync(
      "polymarket",
      ["portfolio", "trades", address, "--json"],
      { encoding: "utf-8" },
    );
    return JSON.parse(raw);
  } catch (_) {}

  // Fallback 2: REST API
  const url = new URL("https://data-api.polymarket.com/activity");
  url.searchParams.set("user", address);
  url.searchParams.set("limit", "500");
  const res = await fetch(url.toString());
  return await res.json();
}
```
