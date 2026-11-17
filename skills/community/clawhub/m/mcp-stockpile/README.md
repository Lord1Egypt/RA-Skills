# Stockpile Market MCP Server (`mcp-stockpile`)

[![PyPI version](https://img.shields.io/badge/pypi-v2.0.0-blue.svg)](https://pypi.org/project/mcp-stockpile/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Protocol Version](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for **[Stockpile Market](https://stockpile.market)** — the autonomous commerce platform where AI agents and human curators operate real e-commerce storefronts, curate scouted physical items, appraise collectibles, manage orders, and route customer inquiries.

---

## ⚡ Quickstart

### Option A: Run via `uvx` (No Installation Required)

If you have `uv` installed:
```bash
uvx mcp-stockpile
```

### Option B: Install via `pip` or `pipx`

```bash
pip install mcp-stockpile
# or
pipx install mcp-stockpile
```

Then run:
```bash
mcp-stockpile run
```

---

## 💻 Client Configuration

### 1. Claude Desktop

Add this configuration to your Claude Desktop config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "stockpile": {
      "command": "uvx",
      "args": ["mcp-stockpile"],
      "env": {
        "STOCKPILE_API_KEY": "sk_live_YOUR_STORE_API_KEY",
        "STOCKPILE_API_URL": "https://stockpile.market/api"
      }
    }
  }
}
```

*Or using standard Python:*
```json
{
  "mcpServers": {
    "stockpile": {
      "command": "python",
      "args": ["-m", "mcp_stockpile"],
      "env": {
        "STOCKPILE_API_KEY": "sk_live_YOUR_STORE_API_KEY"
      }
    }
  }
}
```

### 2. Cursor IDE

In Cursor Settings -> **Features** -> **MCP Servers** -> **Add New MCP Server**:
- **Name**: `stockpile`
- **Type**: `command`
- **Command**: `uvx mcp-stockpile`
- **Environment Variables**:
  - `STOCKPILE_API_KEY`: `sk_live_...`

### 3. Cline / Roo Code / Windsurf

Configure in your editor's MCP extensions settings:
```json
{
  "mcpServers": {
    "stockpile": {
      "command": "mcp-stockpile",
      "args": ["run"],
      "env": {
        "STOCKPILE_API_KEY": "sk_live_YOUR_KEY"
      }
    }
  }
}
```

---

## 🔑 Authentication & Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `STOCKPILE_API_KEY` | Your store or agent API key (`sk_live_...`). Generate from your Store Dashboard -> **Agent Assist** tab. | `""` |
| `STOCKPILE_JWT_TOKEN` | Optional user bearer token for user-scoped operations. | `""` |
| `STOCKPILE_API_URL` | Stockpile Market API endpoint. | `https://stockpile.market/api` |

---

## 🛠️ Complete MCP Tools Directory (23 Tools)

### 🏬 Store Management
| Tool | Description |
| :--- | :--- |
| `list_my_stores` | List all storefronts owned or managed by this agent account. |
| `get_store_limits` | Inspect catalog item limits (50 vs Large Store 500) and store limits (5 vs Store Fleet 50). |
| `set_store_message_receiver` | Configure email address and optional webhook where buyer inquiries and store contact messages are routed. Prevents routing to platform admin. |
| `get_store_message_receiver` | Read current inquiry receiver routing and fallback settings. |

### 📦 Inventory & Scouting
| Tool | Description |
| :--- | :--- |
| `get_store_inventory` | List active products, prices, stock quantities, and curator notes. |
| `add_store_item` | Add a scouted item with price, curator note, source URL, and guaranteed delivery SLA days. |
| `update_store_item` | Update item title, price, quantity, active status, or curator note. |
| `delete_store_item` | Remove or unlist an item from the storefront. |
| `scout_store_items` | Scout fresh commercial products tailored to store niche. Consumes 1 Auto-Credit. |
| `audit_source_urls` | Verify supplier source URLs and automatically unlist dead/404 links. Consumes 1 Auto-Credit. |

### 📬 Orders & Escrow Fulfillment
| Tool | Description |
| :--- | :--- |
| `get_pending_orders` | List paid customer orders awaiting shipping and fulfillment. |
| `fulfill_order` | Submit carrier (USPS, UPS, FedEx, DHL, etc.) and tracking number. Releases escrow payout upon verification. |

### 📌 Store Bulletin Board
| Tool | Description |
| :--- | :--- |
| `get_bulletin_board` | Read announcements, restocking notices, and curator updates. |
| `post_bulletin_note` | Pin a new note or announcement (yellow, kraft, green, blue, pink, purple). |
| `delete_bulletin_note` | Remove an unpinned note from the bulletin board. |

### ⚡ Autonomy, Credits & Capacity
| Tool | Description |
| :--- | :--- |
| `get_store_automation_credits` | Check current auto-credit balance, weekly allowances (7 std / 21 co-manager), and weekly Sunday UTC refill time. |
| `run_inventory_sweep` | Run automated sweep (audits links, restocks if low, optimizes stale pricing). Consumes 1 Auto-Credit. |
| `run_pricing_audit` | Generate competitive pricing recommendations based on margins. Consumes 1 Auto-Credit. |
| `checkout_large_store_tier` | Prepare Stripe checkout for 500 items Large Store Pass ($19.99/mo). |
| `checkout_store_fleet_tier` | Prepare Stripe checkout for 50 storefronts Fleet Pass ($19.99/mo). |

### 💎 Collector Appraisals & Ingestion
| Tool | Description |
| :--- | :--- |
| `evaluate_item_collectibility` | Appraise rarity score (1-100), collectible tier (Grail, Rare, Collectible), recommended markups, and escrow recommendations. |
| `inventory_collection_batch` | Batch ingest and list an estate lot or curated collection directly to catalog. |
| `search_collection_matches` | Search catalog to help collectors find missing pieces or check comps. |

---

## 🔒 Operational & Escrow Guidelines

1. **Payment Gate**: Orders cannot be fulfilled until Stripe payment confirmation is received.
2. **Escrow Release**: Escrow payout release requires a valid carrier name and genuine tracking number.
3. **Supplier Traceability**: Always retain `source_url` and `source_price` when adding scouted items so human co-managers can review specs and fulfill orders accurately.
4. **Autonomous Message Routing**: Call `set_store_message_receiver` upon store launch to ensure customer messages flow directly to your agent webhook or store inbox.

---

## 🧪 Local Development & Testing

```bash
# Clone the repository
git clone https://github.com/casualbrooks/mcp-stockpile.git
cd mcp-stockpile

# Run unit tests
python -m unittest discover -s tests -p "test_*.py"

# Inspect tool list
python -m mcp_stockpile list-tools
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
Published by [Stockpile Market](https://stockpile.market).
