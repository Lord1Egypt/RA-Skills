# Magento 2 Diagnostics Reference

Domain knowledge for interpreting diagnostic results and troubleshooting Magento stores.

## Order Status Flow

```
pending → processing → complete
                    ↘ shipped → complete
pending → canceled
pending → payment_review → processing → ...
                         ↘ canceled
processing → complete
processing → closed (after credit memo)
```

### Common reasons orders get stuck

| Status | Common Causes |
|--------|--------------|
| **Pending (>24h)** | Payment gateway didn't callback; offline payment method awaiting confirmation; fraud review hold |
| **Payment Review** | PayPal/Stripe fraud filter triggered; manual review required in payment dashboard |
| **Processing (>48h)** | Warehouse sync issue; dropship supplier delay; fulfillment workflow bottleneck |

### Resolution paths

- **Stuck pending**: Check payment method → if payment received, update status to processing → ship
- **Payment review**: Check payment provider dashboard → approve or cancel → update order accordingly
- **Stuck processing**: Check warehouse/fulfillment system → create shipment → order moves to complete

## MSI (Multi-Source Inventory) Troubleshooting

### Salable qty vs source qty discrepancy

Salable quantity can differ from the sum of source quantities because:

1. **Reservations**: Unshipped orders create reservations that reduce salable qty
2. **Stock configuration**: Different stocks may aggregate different sources
3. **Source status**: Disabled sources don't contribute to salable qty

### Diagnostic path

```
inventory.py salable-qty <sku> <stock_id>     → Check salable qty
inventory.py source-items --sku <sku>          → Check per-source qty
diagnose.py inventory-risk                     → Overall risk assessment
```

If salable qty is lower than expected:
1. Check open orders for that SKU (reservations)
2. Verify all sources are enabled
3. Check stock-sales channel assignments

## Cache Types Reference

Magento caches different types of data. After updates, flush the relevant caches:

| Cache Type | What it caches | When to flush |
|-----------|---------------|---------------|
| `config` | Store configuration, module settings | After config changes, price updates |
| `layout` | Page layout XML | Rarely needed |
| `block_html` | HTML blocks, category pages, CMS | After product/price/category changes |
| `full_page` | Full page HTML output | After product content changes |
| `collections` | Database query results | Rarely needed |
| `reflection` | Class reflection data | After module install |
| `db_ddl` | Database schema | After module install/upgrade |
| `compiled_config` | Compiled configuration | After config changes |
| `eav` | Entity attribute values | After attribute changes |
| `customer_notification` | Customer notification data | Rarely needed |
| `config_integration` | Integration config | After integration setup |
| `config_integration_api` | Integration API config | After integration setup |
| `webhook` | Webhook config | Rarely needed |
| `weee` | Fixed product tax | After FPT changes |
| `translate` | Translation strings | After language changes |
| `vertex` | Vertex tax calculations | After tax config |

### Quick flush guide

```
Updated product prices → system.py cache-flush --types config,block_html
Updated product content → system.py cache-flush --types full_page,block_html
Disabled a promotion → system.py cache-flush --types config,block_html
Changed store config → system.py cache-flush --types config
Not sure what changed → system.py cache-flush (flush all)
```

## Common API Error Codes

| HTTP Status | Magento Context | Typical Cause |
|-------------|----------------|---------------|
| 400 | Validation error | Missing required fields, invalid data format |
| 401 | Auth failure | OAuth credentials expired or incorrect |
| 404 | Entity not found | SKU/order ID doesn't exist or wrong store scope |
| 405 | Method not allowed | Wrong HTTP method for endpoint |
| 409 | Conflict | Concurrent modification (rare in REST) |
| 500 | Server error | Magento bug, module conflict, or data integrity issue |
| 503 | Service unavailable | Magento in maintenance mode or cache lock |

### Error resolution patterns

- **404 on known SKU**: Check product is in the correct store scope (website/store view). Multi-site setups may restrict visibility.
- **400 on order operations**: Order may be in wrong status for the operation (e.g., can't ship a pending order).
- **500 on bulk operations**: May indicate a plugin/observer throwing an exception. Check Magento exception logs.
- **Rate limiting (429)**: Reduce batch size or increase `OPENCLAW_DELAY_MS`.

## Promotion coupon_type Reference

| Value | Meaning | Code location |
|-------|---------|---------------|
| 1 | No coupon required | N/A |
| 2 | Specific coupon | `code` field on the rule itself |
| 3 | Auto-generated coupons | `coupon` table (multiple codes possible) |

When auditing promotions:
- `coupon_type=2` with empty `code` → rule won't apply, needs a code set
- `coupon_type=3` with no coupons in coupon table → rule was configured but coupons never generated
- Exhausted coupons (`times_used >= usage_limit`) → rule still shows as active but coupons can't be used
