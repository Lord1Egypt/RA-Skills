# Handwrytten MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that lets AI assistants like Claude send real handwritten notes through [Handwrytten](https://www.handwrytten.com) — robots with real pens writing your messages on physical cards, mailed to your recipients.

## What can it do?

Once connected, your AI assistant can:

- **Send handwritten notes** — single or bulk, with per-recipient customization
- **Browse cards and fonts** — discover available stationery templates and handwriting styles
- **Manage addresses** — save, update, and delete recipient and sender addresses
- **Create custom cards** — upload images, add logos and text, design your own cards
- **Include gift cards and inserts** — attach gift cards or marketing inserts to orders
- **Manage QR codes** — create and attach QR codes to custom cards
- **Track orders** — check order status, view history, get tracking info
- **Prospect** — calculate mailing targets by ZIP code and radius

## Quick Start

### 1. Get an API Key

Sign up at [handwrytten.com](https://www.handwrytten.com) and get your API key from the [API settings page](https://www.handwrytten.com/api/).

### 2. Install

```bash
npm install -g @handwrytten/mcp-server
```

### 3. Configure Your AI Client

#### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "handwrytten": {
      "command": "handwrytten-mcp",
      "env": {
        "HANDWRYTTEN_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Config file locations:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

#### Claude Code

```bash
claude mcp add handwrytten -- env HANDWRYTTEN_API_KEY=your_api_key_here handwrytten-mcp
```

#### Cursor

Add to your Cursor MCP settings:

```json
{
  "mcpServers": {
    "handwrytten": {
      "command": "handwrytten-mcp",
      "env": {
        "HANDWRYTTEN_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 4. Start Using It

Just ask your AI assistant naturally:

> "Send a thank-you card to Jane Doe at 123 Main St, Phoenix, AZ 85001"

> "What cards do you have available for birthdays?"

> "Send handwritten notes to everyone in this CSV file"

## Available Tools

### Orders (Core)

| Tool | Description |
|------|-------------|
| `send_order` | Send a handwritten note — the primary tool. Supports single and bulk sends. |
| `get_order` | Get order details including status and tracking |
| `list_orders` | List orders with pagination |

### Cards & Fonts

| Tool | Description |
|------|-------------|
| `list_cards` | Browse all available card/stationery templates |
| `get_card` | Get details of a specific card |
| `list_card_categories` | Get card categories (Thank You, Birthday, etc.) |
| `list_fonts` | Browse handwriting styles for orders |
| `list_customizer_fonts` | Browse printed fonts for custom card text zones |

### Address Book

| Tool | Description |
|------|-------------|
| `list_recipients` | List saved recipient addresses |
| `add_recipient` | Save a new recipient address |
| `update_recipient` | Update an existing recipient |
| `delete_recipient` | Delete recipient address(es) |
| `list_senders` | List saved sender (return) addresses |
| `add_sender` | Save a new sender address |
| `delete_sender` | Delete sender address(es) |
| `list_countries` | Get supported countries |
| `list_states` | Get states/provinces for a country |

### Gift Cards & Inserts

| Tool | Description |
|------|-------------|
| `list_gift_cards` | Browse gift card products with denominations |
| `list_inserts` | Browse card inserts (business cards, flyers) |

### Custom Cards

| Tool | Description |
|------|-------------|
| `list_custom_card_dimensions` | Get available card dimensions |
| `upload_custom_image` | Upload a cover or logo image |
| `check_custom_image` | Check image quality requirements |
| `list_custom_images` | List uploaded images |
| `delete_custom_image` | Delete an uploaded image |
| `create_custom_card` | Create a custom card design |
| `get_custom_card` | Get custom card details |
| `delete_custom_card` | Delete a custom card |

### QR Codes

| Tool | Description |
|------|-------------|
| `list_qr_codes` | List account QR codes |
| `create_qr_code` | Create a new QR code |
| `delete_qr_code` | Delete a QR code |
| `list_qr_code_frames` | Browse decorative QR code frames |

### Basket (Advanced)

| Tool | Description |
|------|-------------|
| `basket_add_order` | Add an order to the basket |
| `basket_send` | Submit the basket for processing |
| `basket_list` | List items in the basket |
| `basket_count` | Count basket items |
| `basket_remove` | Remove a basket item |
| `basket_clear` | Clear the basket |
| `list_past_baskets` | List previously submitted baskets |

### Account & Prospecting

| Tool | Description |
|------|-------------|
| `get_user` | Get account profile and credits balance |
| `list_signatures` | List saved handwriting signatures |
| `calculate_targets` | Prospect by ZIP code and radius |

## Example Conversations

**Simple send:**
> You: "Send a thank-you note to John Smith at 456 Oak Ave, Tempe AZ 85281 from our company"
> Claude: *calls list_cards → list_fonts → send_order*

**Bulk send:**
> You: "Send birthday cards to all these people: [list/CSV]"
> Claude: *calls list_cards → list_fonts → send_order with array of recipients*

**Custom card:**
> You: "Create a custom card with our company logo and send it to our top 5 clients"
> Claude: *calls upload_custom_image → create_custom_card → list_recipients → send_order*

## Development

```bash
git clone https://github.com/handwrytten/handwrytten-mcp-server
cd handwrytten-mcp-server
npm install
npm run build
```

Test locally:

```bash
HANDWRYTTEN_API_KEY=your_key node dist/index.js
```

## Built On

- [Handwrytten TypeScript SDK](https://www.npmjs.com/package/handwrytten) — the official SDK this server wraps
- [Model Context Protocol SDK](https://www.npmjs.com/package/@modelcontextprotocol/sdk) — the MCP framework

## License

MIT
