# HomeBox API Reference — v1 (hay-kot) vs v2 (sysadminsmedia)

Base URL: `{HOMEBOX_BASE_URL}/api/v1`

Auth: All endpoints (except login) require `Authorization: Bearer {HOMEBOX_TOKEN}` header.

---

## Auto-Detection

The script probes `GET /api/v1/entities`:
- **200** → v2 (sysadminsmedia)
- **404** → v1 (hay-kot, archived at v0.10.3)

Override with `HOMEBOX_API_VERSION=v1` or `HOMEBOX_API_VERSION=v2`.

---

## Authentication

### Login (both versions)
```
POST /v1/users/login
Content-Type: application/x-www-form-urlencoded
Body: username=<email>&password=<password>&stayLoggedIn=true
```
Response: `{ "token": "...", "attachmentToken": "...", "expiresAt": "..." }`

### Token Refresh (both)
```
GET /v1/users/refresh
```

### Logout (both)
```
POST /v1/users/logout
```

---

## Items vs Entities

| Operation | v1 (hay-kot) | v2 (sysadminsmedia) |
|-----------|-------------|---------------------|
| **List/Search** | `GET /v1/items?q=&tags=&parents=&page=&pageSize=` | `GET /v1/entities?q=&tags=&parents=&page=&pageSize=` |
| **Create** | `POST /v1/items` | `POST /v1/entities` |
| **Get** | `GET /v1/items/{id}` | `GET /v1/entities/{id}` |
| **Update** | `PUT /v1/items/{id}` | `PUT /v1/entities/{id}` |
| **Patch** | `PATCH /v1/items/{id}` (limited — only `id`, `quantity`) | `PATCH /v1/entities/{id}` (full partial update) |
| **Delete** | `DELETE /v1/items/{id}` | `DELETE /v1/entities/{id}` |
| **Duplicate** | `POST /v1/items/{id}/duplicate` | `POST /v1/entities/{id}/duplicate` |
| **Path** | `GET /v1/items/{id}/path` | `GET /v1/entities/{id}/path` |

### Search Parameters (both)
- `q` — text search (name, description, model, serial, notes)
- `tags` — comma-separated tag IDs (v1: label IDs)
- `parents` — comma-separated parent/location IDs
- `page`, `pageSize` — pagination

### Create Body

v1:
```json
{
  "name": "string (required)",
  "description": "string",
  "labelIds": ["label-id"],
  "locationId": "uuid",
  "parentId": "uuid (nullable)",
  "quantity": 0
}
```

v2:
```json
{
  "name": "string (required)",
  "description": "string",
  "entityTypeId": "string",
  "parentId": "uuid (nullable, also used for location)",
  "quantity": 1,
  "tagIds": ["tag-id"]
}
```

### Update Body (PUT)

v1: full item object including `id`, `name`, `description`, `locationId`, `parentId`, `quantity`, `labelIds`, `archived`, `insured`, `lifetimeWarranty`, `manufacturer`, `modelNumber`, `serialNumber`, `notes`, `purchaseTime`, `purchaseFrom`, `purchasePrice`, `warrantyDetails`, `warrantyExpires`, `soldTime`, `soldPrice`, `soldTo`, `soldNotes`, `syncChildItemsLocations`.

v2: same fields but `entityTypeId` instead of `locationId`, `tagIds` instead of `labelIds`, `purchaseDate`/`soldDate` instead of `purchaseTime`/`soldTime`, `syncChildEntityLocations` instead of `syncChildItemsLocations`.

### Response Differences

v1 item:
```json
{
  "id": "...",
  "name": "...",
  "location": { "id": "...", "name": "Room" },
  "labels": [{ "id": "...", "name": "Electronics" }]
}
```

v2 entity:
```json
{
  "id": "...",
  "name": "...",
  "parentId": "location-or-container-id",
  "entityType": { "id": "...", "name": "Device", "isLocation": false },
  "tags": [{ "id": "...", "name": "Electronics" }]
}
```

---

## Locations

| Operation | v1 | v2 |
|-----------|----|----|
| **List** | `GET /v1/locations` | Via entities: `GET /v1/entities?parentId=root&entityTypeId=<location-type>` |
| **Create** | `POST /v1/locations` | Same as creating an entity, but with an entity type where `isLocation: true` |
| **Get** | `GET /v1/locations/{id}` | `GET /v1/entities/{id}` |
| **Update** | `PUT /v1/locations/{id}` | `PUT /v1/entities/{id}` |
| **Delete** | `DELETE /v1/locations/{id}` | `DELETE /v1/entities/{id}` |
| **Tree** | `GET /v1/locations/tree` | `GET /v1/entities/tree` |

---

## Labels vs Tags

| Operation | v1 (labels) | v2 (tags) |
|-----------|-------------|-----------|
| **List** | `GET /v1/labels` | `GET /v1/tags` |
| **Create** | `POST /v1/labels` `{name, description, color}` | `POST /v1/tags` `{name, description, color}` |
| **Get** | `GET /v1/labels/{id}` | `GET /v1/tags/{id}` |
| **Update** | `PUT /v1/labels/{id}` | `PUT /v1/tags/{id}` |
| **Delete** | `DELETE /v1/labels/{id}` | `DELETE /v1/tags/{id}` |

---

## Entity Types (v2 only)

| Operation | Endpoint |
|-----------|----------|
| **List** | `GET /v1/entity-types` |
| **Create** | `POST /v1/entity-types` `{name, description, isLocation, icon}` |
| **Update** | `PUT /v1/entity-types/{id}` |
| **Delete** | `DELETE /v1/entity-types/{id}` |

---

## Templates (v2 only)

| Operation | Endpoint |
|-----------|----------|
| **List** | `GET /v1/templates` |
| **Create** | `POST /v1/templates` |
| **Create item from template** | `POST /v1/templates/{id}/create-item` |

---

## Attachments (both)

```
POST   /v1/{entities|items}/{id}/attachments          (multipart/form-data)
POST   /v1/{entities|items}/{id}/attachments/external  ({name, url, mimeType})
GET    /v1/{entities|items}/{id}/attachments/{aid}
PUT    /v1/{entities|items}/{id}/attachments/{aid}
DELETE /v1/{entities|items}/{id}/attachments/{aid}
```

---

## Maintenance (both)

```
GET  /v1/{entities|items}/{id}/maintenance
POST /v1/{entities|items}/{id}/maintenance  ({action, scheduledDate, completedDate, cost, notes, vendor})
```

---

## Statistics

| Metric | v1 | v2 |
|--------|----|----|
| **Overview** | `GET /v1/groups/statistics` | Same |
| **By Labels/Tags** | `GET /v1/groups/statistics/labels` | `GET /v1/groups/statistics/tags` |
| **By Locations** | `GET /v1/groups/statistics/locations` | Same |
| **Purchase Price** | `GET /v1/groups/statistics/purchase-price` | Same |

---

## Group Management (v2 only)

| Operation | Endpoint |
|-----------|----------|
| **Get/Update** | `GET/PUT /v1/groups` |
| **Create/Delete** | `POST/DELETE /v1/groups` |
| **List all** | `GET /v1/groups/all` |
| **Invitations** | `GET/POST/DELETE /v1/groups/invitations/{id?}` |
| **Members** | `GET/DELETE /v1/groups/members/{user_id?}` |

---

## Exports (v2 only)

| Operation | Endpoint |
|-----------|----------|
| **List** | `GET /v1/group/exports` |
| **Start** | `POST /v1/group/exports` |
| **Get** | `GET /v1/group/exports/{id}` |
| **Delete** | `DELETE /v1/group/exports/{id}` |
| **Download** | `GET /v1/group/exports/{id}/download` |

---

## Other Endpoints

| Function | v1 | v2 |
|----------|----|----|
| **Import** | `POST /v1/items/import` | `POST /v1/entities/import` |
| **Fields** | `GET /v1/items/fields` | `GET /v1/entities/fields` |
| **Field values** | `GET /v1/items/fields/values` | `GET /v1/entities/fields/values` |
| **Asset lookup** | `GET /v1/assets/{assetId}` | Same |
| **Barcode** | `GET /v1/products/search-from-barcode?barcode=` | Same |
| **QR code** | `GET /v1/qrcode?content=` | Same |
| **BOM report** | `GET /v1/reporting/bill-of-materials` | Same |
| **Notifiers** | `GET/POST/PUT/DELETE /v1/notifiers/{id?}` | Same |
| **Currency** | `GET /v1/currency` | Same |
| **Status** | `GET /v1/status` | Same |

---

## Admin Actions (v2 only)

```
POST /v1/actions/create-missing-thumbnails
POST /v1/actions/ensure-asset-ids
POST /v1/actions/ensure-import-refs
POST /v1/actions/set-primary-photos
POST /v1/actions/wipe-inventory
POST /v1/actions/zero-item-time-fields
```

## Label Generation (v1 only)

```
GET /v1/labelmaker/asset/{assetId}
GET /v1/labelmaker/item/{itemId}
GET /v1/labelmaker/location/{locationId}
```

## User Management (both v1 and v2)

```
GET    /v1/users/self
POST   /v1/users/change-password
POST   /v1/users/register               (v1 only?)
```

## API Keys (v2 only)

```
GET  /v1/api-keys
POST /v1/api-keys
```
