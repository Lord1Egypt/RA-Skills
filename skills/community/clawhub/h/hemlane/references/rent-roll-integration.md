# Hemlane Rent Roll Integration

## Purpose
Sync Hemlane tenant/lease data with Lofty property records for complete occupancy tracking.

## Data Flow

```
Hemlane (Property Management) → Rent Roll JSON → Lofty Property Updates
```

## GraphQL Operations

From `tenant-reply_hemlane.com.har`:
- `ODTenantsAndLeasesBucketCounts` - Get tenant counts by status
- `TGTenantGroup` - Get detailed tenant group info
- `ODTenantsIndexNewPermissions` - Tenant permissions
- `OwnerTenantsAndLeasesTenantGroups` - List tenant groups

## Auth Requirements

- `x-csrf-token` - Required (see `requests_hemlane.com.har`)
- Session cookies - From authenticated Hemlane browser session
- Use `capture_hemlane_auth_via_cdp.py` (similar to Lofty pattern)

## Output Schema

```json
{
  "propertyId": "hemlane-property-id",
  "address": "123 Main St",
  "tenants": [
    {
      "id": "tenant-id",
      "name": "John Doe",
      "email": "john@example.com",
      "leaseStart": "2025-01-01",
      "leaseEnd": "2025-12-31",
      "rentAmount": 1850.00,
      "paymentStatus": "current"
    }
  ],
  "occupancyStatus": "occupied",
  "totalRent": 1850.00
}
```

## Integration Points

1. **Lofty Sync** - Match Hemlane property IDs to Lofty property IDs
2. **DETAILS.md Update** - Write occupancy status to `Public/DETAILS.md`
3. **Rent Roll Reconciliation** - Compare Hemlane rent vs Lofty rent

## Next Steps

- [ ] Capture fresh Hemlane HAR with tenant/lease data
- [ ] Extract exact GraphQL query structure
- [ ] Build auth capture script for Hemlane CDP
- [ ] Create merge script for Lofty + Hemlane data
