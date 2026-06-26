---
name: mstore
description: McDonald's China coupon redemption, query, and points checking. Use when user wants to (1) Query or claim McDonald's coupons, (2) Check available coupons, (3) View points balance, (4) Query campaign calendar, (5) Order food for delivery, or (6) Redeem points for products. This skill provides direct access to McDonald's China MCP services including coupon management, points mall, and delivery ordering.
---

# McDonald's China (麦麦) Skill

## First Time Setup

On first use, you must configure the MCP Token:

1. Get your token from: https://open.mcd.cn/mcp
   - Login with your phone number (must match your McDonald's app account)
   - Click "控制台" (Console) → "激活" (Activate) to generate MCP Token
2. Set the token as an environment variable:
   ```bash
   export MCDCN_MCP_TOKEN="your_token_here"
   ```

Or run the setup script:
```bash
./scripts/setup.sh
```

## Available Tools

### Coupons (麦麦省领券)

| Command | Description |
|---------|-------------|
| `mcd-cn available-coupons` | Query coupons available to claim |
| `mcd-cn auto-bind-coupons` | Auto-claim all available coupons |
| `mcd-cn my-coupons` | List already claimed coupons |

### Points (麦麦商城)

| Command | Description |
|---------|-------------|
| `mcd-cn query-my-account` | Query points balance and account info |
| `mcd-cn mall-points-products` | List products redeemable with points |
| `mcd-cn mall-product-detail` | Get details of a specific points product |
| `mcd-cn mall-create-order` | Redeem points for a product |

### Calendar (麦麦日历)

| Command | Description |
|---------|-------------|
| `mcd-cn campaign-calender` | Query monthly marketing activities |

### Ordering (点餐)

| Command | Description |
|---------|-------------|
| `mcd-cn delivery-query-addresses` | List saved delivery addresses |
| `mcd-cn delivery-create-address` | Add new delivery address |
| `mcd-cn query-store-coupons` | Query coupons for specific store |
| `mcd-cn query-meals` | Query menu for a store |
| `mcd-cn query-meal-detail` | Get meal details |
| `mcd-cn calculate-price` | Calculate order price |
| `mcd-cn create-order` | Create delivery order |
| `mcd-cn query-order` | Query order status |

### Nutrition (餐品营养)

| Command | Description |
|---------|-------------|
| `mcd-cn list-nutrition-foods` | Get nutrition info for menu items |

### General

| Command | Description |
|---------|-------------|
| `mcd-cn now-time-info` | Get current server time |

## Usage Examples

### Check available coupons to claim
```bash
mcd-cn available-coupons
```

### Auto-claim all available coupons
```bash
mcd-cn auto-bind-coupons
```

### Check my claimed coupons
```bash
mcd-cn my-coupons
```

### Check points balance
```bash
mcd-cn query-my-account
```

### List points redemption products
```bash
mcd-cn mall-points-products
```

### Query this month's campaigns
```bash
mcd-cn campaign-calender
```

## Requirements

- **mcd-cn CLI**: Install via `brew install ryanchen01/tap/mcd-cn`
- **MCDCN_MCP_TOKEN**: Get from https://open.mcd.cn/mcp

## MCP Server Info

- **Server URL**: https://mcp.mcd.cn
- **Protocol**: Streamable HTTP
- **Rate Limit**: 600 requests/minute per token
- **Version**: MCP 2025-06-18

## Notes

- Token is linked to the phone number used during login at open.mcd.cn
- Coupons and points are tied to your McDonald's account
- Some features may require the user to have a valid delivery address set up
