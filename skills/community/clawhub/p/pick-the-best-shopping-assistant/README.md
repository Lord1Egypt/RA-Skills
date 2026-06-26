# Shopping Assistant Skill

Personal shopping assistant that helps you find products, compare prices, and get the best deals across multiple e-commerce platforms using MCP protocol.

## Features

- 🔍 **Smart Search** - Natural language product search with GPT-powered intent recognition
- 💰 **Price Comparison** - Find the cheapest products automatically
- ⭐ **Best Value Finder** - Discover quality products at great prices
- 🌍 **Multi-Market** - Search across GB, US, DE, AU, FR, PL markets
- 🎯 **Smart Filtering** - Auto-extract brand, price range, ratings from your query
- 🔌 **MCP Integration** - Uses Model Context Protocol for seamless tool access

## Quick Start

### Activate the Skill

```bash
/shopping-assistant
```

Or use trigger words: `shopping`, `shop`, `buy`, `product`, `deal`, `price`

### Example Queries

```
# Basic search
Find me wireless earbuds

# Price-focused
Show me the cheapest laptop under £500

# Quality-focused
Best value coffee machine with at least 4 stars

# Brand-specific
Sony headphones under £100

# Gift recommendations
Gift ideas for a tech enthusiast under $50

# With discounts
Gaming keyboards on sale
```

## How It Works

The skill uses the **gpt-mcp MCP server** which provides shopping tools via Model Context Protocol.

### MCP Server Configuration

The skill includes a `.mcp.json` configuration file that defines the gpt-mcp server connection:

```json
{
  "mcpServers": {
    "gpt-mcp": {
      "type": "sse",
      "url": "https://pickthebest.com/gb/en/v1/shopping/mcp",
      "description": "GPT-powered shopping search MCP server"
    }
  }
}
```

### Available MCP Tools

- **gpt-mcp::smart_search** - Natural language search with GPT-powered intent recognition
- **gpt-mcp::search_cheapest** - Find lowest prices
- **gpt-mcp::search_best_value** - Find best quality-to-price ratio

### Market Support

- 🇬🇧 GB (United Kingdom)
- 🇺🇸 US (United States)
- 🇩🇪 DE (Germany)
- 🇦🇺 AU (Australia)
- 🇫🇷 FR (France)
- 🇵🇱 PL (Poland)

### Market Auto-Detection

The skill automatically detects your market from:
- Currency symbols (£→GB, $→US, €→DE)
- Explicit mentions ("UK", "USA", "Germany")
- Defaults to GB if unclear

## Multi-Turn Conversations

The skill supports refining your search through conversation:

```
You: Show me headphones
Assistant: [Shows results]

You: Only Sony brand
Assistant: [Filters to Sony products]

You: Under £100
Assistant: [Adds price filter]

You: Show cheapest
Assistant: [Sorts by price ascending]
```

## Response Format

Results are presented in a clean, user-friendly format:

```markdown
### 🛍️ Shopping Results

**Query**: "wireless earbuds"
**Found**: 25 products

#### Top Picks:

**1. Sony WF-1000XM4** by Sony
💰 **Price**: £199.99 🏷️ 15% OFF
⭐ **Rating**: 4.7/5 (12,453 reviews)
🏷️ **Category**: Electronics > Audio > Headphones
🔗 [View on Amazon](https://amazon.co.uk/...)
```

## Technical Details

### MCP Tools from gpt-mcp Server

1. **gpt-mcp::smart_search** (Recommended) - Natural language search with GPT-powered intent recognition
2. **gpt-mcp::search_cheapest** - Find lowest prices
3. **gpt-mcp::search_best_value** - Find best quality-to-price ratio

### MCP Protocol Integration

The skill uses Model Context Protocol to communicate with the gpt-mcp server:

- **Protocol**: MCP (Model Context Protocol)
- **Server Type**: SSE (Server-Sent Events)
- **Configuration**: `.mcp.json` in skill directory
- **Tool Invocation**: Direct MCP tool calls via protocol

Response parsing is handled automatically by the MCP framework.

## Troubleshooting

### No Results Found
- Try broader keywords
- Remove specific filters
- Try a different market

### API Timeout
- The API may take 2-5 seconds (uses GPT-4)
- Skill will retry once automatically

### Wrong Market
- Explicitly mention the market: "search in US"
- Use currency symbols: $ for US, £ for GB, € for DE

## Dependencies

- **MCP-enabled Claude Code** - Supports Model Context Protocol for tool invocation
- **gpt-mcp server** - Backend shopping service (configured in `.mcp.json`)

## Privacy & Affiliate Links

- All product URLs include affiliate tags for revenue tracking
- No personal data is sent to the API
- Search queries are processed by GPT-4 for intent recognition

## Examples

### Find Cheap Products

```
Find me the cheapest wireless mouse
```

### Find Quality Products

```
Best value laptop with at least 4.5 stars and 1000+ reviews
```

### Brand-Specific Search

```
Show me Sony or Bose headphones under £200
```

### Gift Recommendations

```
Gift for a coffee lover under £50
```

### Discount Hunting

```
Gaming products on sale with at least 20% off
```

## MCP Configuration

This skill includes a `.mcp.json` configuration file that connects to the gpt-mcp server:

```json
{
  "mcpServers": {
    "gpt-mcp": {
      "type": "sse",
      "url": "https://pickthebest.com/gb/en/v1/shopping/mcp",
      "description": "GPT-powered shopping search MCP server"
    }
  }
}
```

No additional setup required - the skill automatically uses this MCP server connection.

## Contributing

This skill uses the gpt-mcp MCP server. For backend API documentation, see:
- `gpt_mcp/MCP_API_DOCUMENTATION.md`

For MCP protocol details, see:
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

---

**Happy Shopping! 🛍️**