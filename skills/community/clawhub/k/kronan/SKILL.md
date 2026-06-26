---
name: kronan-cli
description: >
  Comprehensive CLI for Krónan.is grocery store using the official Public API.
  Search products, browse categories, manage shopping cart and lists, view orders,
  track purchase statistics, and manage shopping notes. Full CRUD operations
  for all API features. Designed for both humans and AI agents.
version: 0.3.0
requires:
  binaries:
    - gh        # GitHub CLI — required for install
    - bun       # Bun runtime — only needed if building from source
  paths:
    - ~/.kronan/token   # AccessToken for Public API authentication
metadata:
  openclaw:
    homepage: https://github.com/arnif/kronan-cli
    emoji: "\U0001F6D2"
---

# kronan-cli

CLI tool for shopping at [Krónan.is](https://www.kronan.is), Iceland's grocery store chain. Uses the official Krónan Public API. Designed for both humans and AI agents.

## Prerequisites

- [GitHub CLI](https://cli.github.com) (`gh`) — required for the install command
- A Krónan account with **Auðkenni** (Icelandic e-ID) login
- An Access Token from https://kronan.is/adgangur/adgangslyklar

## Install

```bash
gh repo clone arnif/kronan-cli /tmp/kronan-cli && bash /tmp/kronan-cli/install.sh
```

**What this does:** clones the repo to `/tmp/kronan-cli`, then `install.sh` downloads a pre-built binary from the latest GitHub release and places it at `~/.local/bin/kronan` (override with `INSTALL_DIR`).

To build from source instead:

```bash
gh repo clone arnif/kronan-cli && cd kronan-cli
bun install && bun build --compile src/index.ts --outfile kronan
mv kronan ~/.local/bin/
```

## Security and privacy

- **Install script**: `install.sh` executes on your machine and downloads a binary. Audit the [repository](https://github.com/arnif/kronan-cli) and the script before running.
- **Token storage**: Access tokens are stored at `~/.kronan/token`. These are credentials for the Krónan Public API. Ensure the file is only readable by your user (`chmod 600 ~/.kronan/token`).
- **PII**: `kronan me` outputs your identity information (name and type - user or customer group). Be careful when sharing this output.
- **API Access**: Tokens are created in your Krónan account settings and can be revoked at any time at https://kronan.is/adgangur/adgangslyklar

## Authentication

First, create an access token:
1. Go to https://kronan.is/adgangur/adgangslyklar
2. Log in with Auðkenni (Icelandic e-ID)
3. Create a new access token

Then save it with the CLI:

```bash
kronan token <your-access-token>
```

The token will be validated and saved locally.

```bash
kronan logout    # Clear stored token
kronan status    # Check authentication status
```

## Commands

### Search products

```bash
kronan search "mjolk"
kronan search "epli" --limit 5
kronan search "braud" --json
```

### Product details

```bash
kronan product <sku>
kronan product 02500188 --json
```

### Browse by category

```bash
kronan categories                    # List all categories
kronan category 01-01-02-epli        # Browse products in category
```

### Cart management

```bash
kronan cart                         # View cart
kronan cart add <sku> [quantity]    # Add item to cart
kronan cart clear                   # Clear all items from cart
```

### Order history and modifications

```bash
kronan orders                # Recent orders
kronan orders --json         # JSON output for parsing
kronan order <token>         # Specific order details (use order token, not ID)

# Modify orders (before fulfillment)
kronan order delete-lines <token> <lineId1> [lineId2...]
kronan order lower-quantity <token> <lineIds...> --quantity N
kronan order toggle-substitution <token> <lineIds...>
```

### Product lists (full CRUD)

```bash
kronan lists                                    # List all product lists
kronan lists create <name> [--description "..."] # Create new list
kronan lists view <token>                       # View list details
kronan lists delete <token> [--force]           # Delete a list
kronan lists add <list-token> <sku> [qty]       # Add item to list
kronan lists remove <list-token> <sku>          # Remove item from list
kronan lists clear <token> [--force]            # Clear all items
```

### Shopping notes (Skundalisti)

```bash
kronan notes                                    # View shopping note
kronan notes add [--text "..."] [--sku SKU] [--quantity N]
kronan notes update <line-token> [--text "..."] [--quantity N]
kronan notes remove <line-token>                # Remove item
kronan notes toggle <line-token>               # Mark complete/incomplete
kronan notes clear [--force]                   # Clear all items
kronan notes archived                          # View completed items
```

### Purchase statistics

```bash
kronan stats [--limit N] [--offset N]          # View purchase history
kronan stats --include-ignored                 # Include hidden products
kronan stats ignore <id>                       # Hide product from stats
kronan stats unignore <id>                     # Unhide product
```

### User identity

```bash
kronan me              # Show current identity (user or customer group)
kronan me --json
```

## AI Agent Usage

All commands support `--json` for structured output. This makes kronan-cli suitable as a tool for AI agents managing grocery shopping.

**Important:** Commands that change state can modify the user's real data. Agents **must ask for explicit user confirmation** before running any state-changing command.

State-changing commands:
- `cart add`, `cart clear`
- `order delete-lines`, `order lower-quantity`, `order toggle-substitution`
- `lists create`, `lists delete`, `lists add`, `lists remove`, `lists clear`
- `notes add`, `notes update`, `notes remove`, `notes toggle`, `notes clear`
- `stats ignore`, `stats unignore`

Read-only commands are safe to run without confirmation:
- `search`, `product`, `categories`, `category`
- `orders`, `order` (view)
- `cart` (view)
- `lists` (view)
- `notes` (view), `notes archived`
- `stats` (view)
- `me`, `status`

### Example agent workflows

**Build a weekly cart from frequently purchased items:**

```bash
# 1. Get purchase statistics to find frequently bought items
kronan stats --limit 50 --json

# 2. Add top items to cart at their typical quantities
kronan cart add 100224198 6    # Nýmjólk x6
kronan cart add 02200946 1     # Heimilisbrauð

# 3. Review the cart
kronan cart --json
```

**Create a shopping list for a recipe:**

```bash
# 1. Create a new list
kronan lists create "Pizza Night" --description "Ingredients for homemade pizza"

# 2. Search for products and add to list
kronan search "mozzarella" --json
kronan lists add <list-token> 100246180 2

kronan search "pizzasósa" --json
kronan lists add <list-token> 100221958 1

# 3. View the completed list
kronan lists view <list-token>
```

**Manage shopping with notes (Skundalisti):**

```bash
# 1. Add items to shopping note
kronan notes add --text "Mjólk"
kronan notes add --sku 100224198 --quantity 2

# 2. Mark items as you shop
kronan notes toggle <line-token>

# 3. View remaining items
kronan notes

# 4. View completed items
kronan notes archived
```

**Analyze and optimize purchases:**

```bash
# View purchase frequency for all products
kronan stats --json

# Hide irrelevant products from stats
kronan stats ignore <id>
```

## Flags

| Flag | Description |
|------|-------------|
| `--json` | Structured JSON output (for AI agents) |
| `--page <n>` | Page number (search, category) |
| `--limit <n>` | Results per page |
| `--offset <n>` | Offset for pagination |
| `--include-ignored` | Include ignored products in stats |
| `--force` | Skip confirmation for destructive operations |
| `--text "..."` | Text for shopping note item |
| `--sku SKU` | Product SKU |
| `--quantity N` | Quantity (default: 1) |
| `--description "..."` | Description for product list |

## API Reference

The CLI uses the official Krónan Public API at `https://api.kronan.is/api/v1/`.

API Documentation:
- Swagger UI: https://api.kronan.is/api/v1/schema/swagger-ui/
- ReDoc: https://api.kronan.is/api/v1/schema/redoc/

Key endpoints:

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/products/search/` | POST | Yes | Product search |
| `/products/{sku}/` | GET | Yes | Product detail |
| `/categories/` | GET | Yes | Category tree |
| `/categories/{slug}/products/` | GET | Yes | Category products |
| `/checkout/` | GET | Yes | View checkout/cart |
| `/checkout/lines/` | POST | Yes | Add/replace checkout lines |
| `/orders/` | GET | Yes | Order history |
| `/orders/{token}/` | GET | Yes | Order details |
| `/orders/{token}/delete-lines/` | POST | Yes | Delete order lines |
| `/orders/{token}/lower-quantity-lines/` | POST | Yes | Lower line quantity |
| `/orders/{token}/lines-toggle-substitution/` | POST | Yes | Toggle substitution |
| `/me/` | GET | Yes | Current identity |
| `/product-lists/` | GET/POST | Yes | List/create product lists |
| `/product-lists/{token}/` | GET/PATCH/DELETE | Yes | Product list CRUD |
| `/product-lists/{token}/update-item/` | POST | Yes | Add/update list item |
| `/shopping-notes/` | GET | Yes | View shopping note |
| `/shopping-notes/add-line/` | POST | Yes | Add note line |
| `/shopping-notes/change-line/` | PATCH | Yes | Update note line |
| `/shopping-notes/delete-line/` | DELETE | Yes | Delete note line |
| `/shopping-notes/toggle-complete-on-line/` | PATCH | Yes | Toggle completion |
| `/product-purchase-stats/` | GET | Yes | Purchase statistics |
| `/product-purchase-stats/{id}/set-ignored/` | PATCH | Yes | Ignore/unignore product |

Auth header format: `Authorization: AccessToken {token}`

## Migration from v0.1.x

If you were using the previous version with Cognito authentication:

1. Remove old tokens: `rm ~/.kronan/tokens.json`
2. Get a new access token from https://kronan.is/adgangur/adgangslyklar
3. Run `kronan token <new-token>`
4. Update any scripts using `kronan login` to use `kronan token` instead

Note: Order IDs in the new API are tokens (UUIDs), not numeric IDs.

## Version History

- **v0.3.0** - Added comprehensive commands: categories, order modifications, product lists CRUD, shopping notes, purchase statistics
- **v0.2.0** - Migrated to Krónan Public API with AccessToken authentication
- **v0.1.0** - Initial release with Cognito authentication
