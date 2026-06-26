# IC Trade Navigator — MCP Connector

**Taiwan-neutral IC component quoting connector for Claude Desktop and MCP-compatible clients.**

Connect your local ERP inventory to real-time market intelligence — without sending your pricing data to any server.

---

## What This Is

This connector is the **client-side** component of the IC Trade Navigator system. It:

- Reads your local `inventory.xlsx` (part numbers + stock quantities only)
- Calls the IC Trade Navigator API (`GET /v1/quote`) to fetch market pricing, risk scores, and trade advisory
- Merges both sources into a unified view — locally, on your machine
- Exposes three MCP tools to Claude Desktop for conversational IC trading workflows

**Your floor prices, purchase costs, and ERP financial data never leave your machine.**

---

## Architecture

```
Your Machine                          IC Trade Navigator Server
─────────────────────────────         ──────────────────────────
inventory.xlsx  ←─ read               (Black-box API)
    │                                  • Market scraping
    │  part_number + qty only          • Risk scoring
    └──────────────────────────────►   • Multilingual advisory
                                       • Taiwan-neutral filtering
    ◄──────────────────────────────
    quoted_price, risk_level,
    advisory (en/de/ja/zh-TW/fr/ko)
         │
    merged_view  ─► Claude Desktop
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install httpx openpyxl
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env:
#   QUOTE_ENGINE_URL     = https://api.ic-navigator.com   (or your self-hosted URL)
#   QUOTE_ENGINE_API_KEY = JAY-IC-xxxxxxxxxxxxxxxxxxxx
#   ERP_EXCEL_PATH       = /path/to/your/inventory.xlsx
```

### 3. Single quote (CLI)

```bash
python -m mcp_connector.client quote STM32L412CBU6 --qty 500 --lang zh-TW
```

### 4. Batch quote from inventory

```bash
python -m mcp_connector.client batch data/inventory.xlsx
```

### 5. JSON output (for ERP integration)

```bash
python -m mcp_connector.client quote GD32F103C8T6 --qty 1000 --lang en --json
```

---

## MCP Tools (Claude Desktop)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ic-trade-navigator": {
      "command": "python",
      "args": ["-m", "mcp_connector.server"],
      "env": {
        "QUOTE_ENGINE_URL": "https://api.ic-navigator.com",
        "QUOTE_ENGINE_API_KEY": "JAY-IC-your-key-here",
        "ERP_EXCEL_PATH": "/absolute/path/to/inventory.xlsx"
      }
    }
  }
}
```

Available tools in Claude:

| Tool | Description |
|---|---|
| `quote_part` | Get market quote + risk score for one part number |
| `read_erp_inventory` | Look up your local stock for a part |
| `get_combined_view` | Full merged view: market + local ERP |

---

## Inventory File Format

Your `inventory.xlsx` should have these columns (column names are configurable):

| Part Number | Stock Qty | Status | Package | Date Code |
|---|---|---|---|---|
| STM32L412CBU6 | 12000 | In Stock | UFQFPN32 | 2347 |
| GD32F103C8T6 | 8000 | In Stock | LQFP48 | 2344 |

A sample file is included at `data/inventory.xlsx`.

**Pricing columns are automatically blocked** — even if present in your file, the connector will never read or transmit them.

---

## Response Fields

```json
{
  "part_number": "STM32L412CBU6",
  "quoted_price": 2.8500,
  "quote_action": "auto_quote",
  "risk_level": "low",
  "risk_index": 0.12,
  "tw_neutral_confidence": 0.88,
  "advisory": "Part is in normal active supply...",
  "advisory_lang": "en",
  "local_stock_qty": 12000,
  "recommendation": "✅ Auto-quote ready. Local stock: 12,000 units."
}
```

### Risk Levels

| Level | Score | Meaning |
|---|---|---|
| 🟢 `low` | < 0.30 | Standard procurement confidence |
| 🟡 `medium` | 0.30–0.65 | Request Certificate of Conformance |
| 🔴 `high` | ≥ 0.65 | Escalate to procurement quality team |

### Advisory Languages

`en` · `de` · `ja` · `zh-TW` · `fr` · `ko`

---

## Custom Column Mapping

If your Excel uses different column headers:

```bash
python -m mcp_connector.client batch inventory.xlsx \
  --col-pn "MPN" \
  --col-qty "Available" \
  --col-status "Lifecycle"
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `QUOTE_ENGINE_URL` | ✅ | — | API server base URL |
| `QUOTE_ENGINE_API_KEY` | ✅ | — | Your `JAY-IC-` API key |
| `ERP_EXCEL_PATH` | — | `data/inventory.xlsx` | Path to local inventory file |
| `CONNECTOR_TIMEOUT` | — | `15` | HTTP timeout in seconds |

---

## Privacy Guarantee

This connector enforces a strict data boundary:

- **Sent to server:** `part_number`, `qty`, `lang` — nothing else
- **Blocked fields:** Any column header containing `price`, `cost`, `floor`, `margin`, `sale`, `purchase`, `底价`, `售价`, `进价`, `含税`
- **Client-side only:** All ERP merging and display runs locally

---

## License

MIT License — see [LICENSE](LICENSE)

---

## Get an API Key

This connector requires access to the IC Trade Navigator API.
Contact: jay.ictw@gmail.com
