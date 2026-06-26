---
name: store-management
description: Manage a Mobazha store using MCP tools — products, orders, messages, and settings. Requires an active MCP connection (see store-mcp-connect).
requires_credentials: true
credential_types:
  - MCP session token (established via store-mcp-connect)
---

# Store Management via AI

This skill teaches AI agents how to manage a Mobazha store using MCP tools. It requires a working MCP connection — see `store-mcp-connect` skill first.

## Product Management

### List All Products

```
Tool: listings_list_mine
Parameters: (none)
```

Returns all listings owned by the authenticated seller, including title, price, stock, status.

### Get Product Details

```
Tool: listings_get
Parameters:
  slug_or_cid: "my-product-slug"   (required)
```

### Create a Product

First, get the listing template to see all available fields:

```
Tool: listings_get_template
Parameters: (none)
```

Then create the listing:

```
Tool: listings_create
Parameters:
  listing_json: '{"title":"...", "description":"...", "price":29.99, ...}'   (required)
```

The `listing_json` should include at minimum: `title`, `description`, `price`, `priceCurrency`, `quantity`, `condition`, `listingType`.

### Update a Product

```
Tool: listings_update
Parameters:
  listing_json: '{"slug":"existing-slug", "title":"Updated Title", ...}'   (required)
```

Include the `slug` to identify which listing to update.

### Delete a Product

```
Tool: listings_delete
Parameters:
  slug: "my-product-slug"   (required)
```

### Typical "Add Product" Workflow

When a seller says "add a product," follow this sequence:

1. Ask for: product name, description, price, currency, stock quantity
2. Ask for product images (or accept URLs to download)
3. Call `listings_get_template` to get the full schema
4. Fill in the template with provided values
5. Call `listings_create` with the JSON
6. Confirm success and share the listing URL

## Order Management

### View Sales (Seller Perspective)

```
Tool: orders_get_sales
Parameters:
  limit: "20"    (optional, default varies)
  offset: "0"    (optional)
```

### View Purchases (Buyer Perspective)

```
Tool: orders_get_purchases
Parameters:
  limit: "20"    (optional)
  offset: "0"    (optional)
```

### Get Order Details

```
Tool: orders_get_detail
Parameters:
  order_id: "QmXyz..."   (required)
```

### Order Lifecycle Actions

| Action | Tool | When to Use |
|--------|------|-------------|
| Confirm | `orders_confirm` | Accept an incoming order |
| Decline | `orders_decline` | Reject an order |
| Fulfill | `orders_fulfill` | Mark as shipped, add tracking |
| Complete | `orders_complete` | Release escrow funds |
| Refund | `orders_refund` | Issue a refund |
| Cancel | `orders_cancel` | Cancel as buyer |

**Fulfill with tracking info:**

```
Tool: orders_fulfill
Parameters:
  order_id: "QmXyz..."            (required)
  shipper: "FedEx"                (optional)
  tracking_number: "123456789"    (optional)
  note: "Shipped via express"     (optional)
```

### Typical "Process New Orders" Workflow

When a seller says "check my orders":

1. Call `orders_get_sales` to list recent orders
2. Summarize: how many new/pending, total revenue
3. For each pending order, ask if the seller wants to confirm or decline
4. After confirming, ask if they have tracking info to fulfill

## Buyer Communication

### List Conversations

```
Tool: chat_get_conversations
Parameters: (none)
```

### Read Messages

```
Tool: chat_get_messages
Parameters:
  room_id: "!abc:matrix.org"    (use room_id or peer_id)
  peer_id: "QmPeerID..."        (alternative to room_id)
  limit: "20"                   (optional)
```

### Send a Message

```
Tool: chat_send_message
Parameters:
  message: "Thanks for your order!"    (required)
  room_id: "!abc:matrix.org"           (use room_id or peer_id)
  peer_id: "QmPeerID..."              (alternative)
  order_id: "QmOrderID..."            (optional, links message to order)
```

### Typical "Reply to Buyers" Workflow

1. Call `chat_get_conversations` to see active chats
2. For conversations with unread messages, call `chat_get_messages`
3. Summarize buyer questions for the seller
4. Draft replies based on seller's instructions
5. Send via `chat_send_message` after seller approval

## Discounts and Promotions

### List Discounts

```
Tool: discounts_list
Parameters: (none)
```

### Create a Discount

```
Tool: discounts_create
Parameters:
  discount_json: '{"title":"Summer Sale", "discountType":"PERCENTAGE", "value":20, ...}'   (required)
```

### Update / Delete

```
Tool: discounts_update
Parameters:
  discount_id: "abc123"         (required)
  discount_json: '{"value":25}'  (required)

Tool: discounts_delete
Parameters:
  discount_id: "abc123"   (required)
```

## Collections

### List Collections

```
Tool: collections_list
Parameters: (none)
```

### Create a Collection

```
Tool: collections_create
Parameters:
  collection_json: '{"name":"Best Sellers", "description":"Our top products"}'   (required)
```

### Add Products to Collection

```
Tool: collections_add_products
Parameters:
  collection_id: "abc123"                              (required)
  products_json: '["product-slug-1","product-slug-2"]'  (required)
```

## Store Profile

### View Profile

```
Tool: profile_get
Parameters: (none)
```

### Update Profile

```
Tool: profile_update
Parameters:
  profile_json: '{"name":"Updated Store Name", "shortDescription":"New tagline"}'   (required)
```

## Settings

### View Storefront Settings

```
Tool: settings_get_storefront
Parameters: (none)
```

Returns storefront configuration including accepted currencies, shipping options, return policy, terms of service, and store appearance settings.

## Notifications

### Check Notifications

```
Tool: notifications_list
Parameters:
  limit: "10"    (optional)
  offset: "0"    (optional)
```

### Unread Count

```
Tool: notifications_unread_count
Parameters: (none)
```

### Mark as Read

```
Tool: notifications_mark_read
Parameters:
  notification_id: "abc123"   (required)
```

## Finance and Rates

### Exchange Rates

```
Tool: exchange_rates_get
Parameters:
  currency: "USD"   (optional, returns all if omitted)
```

### Receiving Addresses (Crypto Wallets)

```
Tool: wallet_get_receiving_accounts
Parameters: (none)
```

Returns the external wallet addresses configured for receiving payments.

### Fiat Payment Providers

```
Tool: fiat_get_providers
Parameters: (none)

Tool: fiat_get_provider_config
Parameters:
  provider_id: "stripe"   (required)
```

## Marketplace Search

These tools search the **public marketplace**, not just your store. Useful for market research.

### Search Listings

```
Tool: search_listings
Parameters:
  query: "vintage watches"    (optional)
  page: "1"                   (optional)
  pageSize: "20"              (optional)
  sortBy: "relevance"         (optional)
```

### Search Seller Profiles

```
Tool: search_profiles
Parameters:
  query: "electronics"   (optional)
  page: "1"              (optional)
  pageSize: "20"         (optional)
```

Note: Search tools are only available when the MCP server was started with `--search-url` configured.

## Best Practices for AI Agents

1. **Always confirm before destructive actions** — deleting products, declining orders, issuing refunds
2. **Ask for explicit user consent** before initiating any MCP connection or executing store operations
3. **Summarize before acting** — show the seller what you found before making changes
4. **Batch intelligently** — process multiple orders or products in sequence, reporting progress
5. **Use templates** — call `listings_get_template` before creating products to ensure valid JSON
6. **Respect rate limits** — space out rapid consecutive calls
7. **Never log or display tokens** — MCP credentials must not appear in agent output or logs
