# LobsterSearch MCP — Usage Examples

## Discovery

### Search for businesses

> "Find me a good ramen place in Bugis"

```json
{
  "tool": "search",
  "arguments": {
    "query": "best ramen in Bugis",
    "limit": 5
  }
}
```

### Search with filters

> "Any hair salons in Singapore?"

```json
{
  "tool": "search",
  "arguments": {
    "query": "hair salon",
    "business_type": "salon",
    "city": "Singapore"
  }
}
```

### Get business details

> "Tell me more about Tanjong Rhu Dental"

```json
{
  "tool": "details",
  "arguments": {
    "slug": "tanjong-rhu-dental"
  }
}
```

### Compare businesses

> "Compare these three dental clinics"

```json
{
  "tool": "compare",
  "arguments": {
    "business_ids": ["uuid-1", "uuid-2", "uuid-3"]
  }
}
```

---

## Catalog

### Browse a business catalog

> "What does this restaurant sell?"

```json
{
  "tool": "browse_catalog",
  "arguments": {
    "business_id": "abc-123",
    "sort_by": "price_low"
  }
}
```

### Get product details with variants

> "Tell me about this product — what sizes and colors are available?"

```json
{
  "tool": "get_product_details",
  "arguments": {
    "offering_id": "product-uuid"
  }
}
```

### Check variant availability

> "Is the large black version in stock?"

```json
{
  "tool": "check_availability",
  "arguments": {
    "offering_id": "product-uuid",
    "options": {
      "Size": "Large",
      "Color": "Black"
    }
  }
}
```

---

## Commerce

### Create a draft order

> "I'd like to order 2 of these"

```json
{
  "tool": "create_order",
  "arguments": {
    "business_id": "abc-123",
    "items": [
      {
        "offering_id": "product-uuid",
        "variant_id": "variant-uuid",
        "quantity": 2
      }
    ],
    "customer_email": "user@example.com",
    "customer_name": "John Doe"
  }
}
```

### Confirm and get payment link

> "Yes, let's go ahead with this order"

```json
{
  "tool": "confirm_order",
  "arguments": {
    "order_id": "order-uuid"
  }
}
```

Response includes a Stripe Checkout URL for payment.

### Check order status

> "What's the status of my order?"

```json
{
  "tool": "get_order_status",
  "arguments": {
    "order_id": "order-uuid"
  }
}
```

### Cancel an order

> "Actually, cancel that order"

```json
{
  "tool": "cancel_order",
  "arguments": {
    "order_id": "order-uuid",
    "reason": "Changed my mind"
  }
}
```

---

## Full Agent Shopping Flow

A typical agent-driven shopping experience:

```
1. search("sushi near Marina Bay")          → find businesses
2. details(id: "...")                        → get full profile
3. browse_catalog(business_id: "...")        → see what they sell
4. get_product_details(offering_id: "...")   → check variants and prices
5. check_availability(offering_id, options)  → verify stock
6. create_order(business_id, items)          → draft with stock reservation
7. confirm_order(order_id)                   → get payment link
8. get_order_status(order_id)               → track through fulfillment
```

Each step returns `next_actions` telling the agent what to do next.
