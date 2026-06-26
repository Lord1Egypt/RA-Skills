# Miro REST API - Complete Endpoint Reference

## Base URL
```
https://api.miro.com/v2
```

## Authentication
All endpoints require:
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

---

## Boards

### List Boards
```http
GET /boards
```
**Query Parameters:**
- `limit` (int, default: 100) - Items per page
- `cursor` (string) - Pagination cursor
- `sort` (string) - `created_at`, `updated_at`, `name`
- `owner_id` (string) - Filter by owner

**Response:** 200 OK
```json
{
  "data": [
    {
      "id": "uXjVGAeRkgI=",
      "name": "My Board",
      "owner": {"id": "user-123", "email": "user@example.com"},
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-20T14:45:00Z",
      "sharing": {"access": "TEAM", "team_id": "team-123"},
      "permissions": {"TEAM_MEMBER": ["EDIT", "COMMENT"]}
    }
  ],
  "cursor": "next-cursor"
}
```

### Get Board
```http
GET /boards/{board_id}
```

**Path Parameters:**
- `board_id` (string, required) - UUID

**Response:** 200 OK
```json
{
  "id": "uXjVGAeRkgI=",
  "name": "My Board",
  "picture_url": "https://...",
  "owner": {...},
  "sharing": {...},
  "team": {...}
}
```

### Create Board
```http
POST /boards
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "New Board",
  "description": "Board description",
  "sharing": {
    "access": "TEAM",
    "team_id": "team-123"
  }
}
```

**Response:** 201 Created

### Update Board
```http
PATCH /boards/{board_id}
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Updated Name",
  "description": "New description"
}
```

**Response:** 200 OK

### Delete Board
```http
DELETE /boards/{board_id}
```

**Response:** 204 No Content

---

## Board Items

### List Items
```http
GET /boards/{board_id}/items
```

**Query Parameters:**
- `limit` (int, default: 100)
- `cursor` (string)
- `type` (string) - Filter by type (CARD, SHAPE, TEXT, etc.)
- `created_after` (ISO 8601) - Filter by creation date
- `include` (string) - Additional fields (comments, webhooks)

**Response:** 200 OK
```json
{
  "data": [
    {
      "id": "item-123",
      "type": "CARD",
      "title": "Task",
      "description": "Do something",
      "owner_id": "user-123",
      "position": {"x": 100, "y": 200},
      "geometry": {"width": 200, "height": 100},
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-20T14:45:00Z"
    }
  ]
}
```

### Create Item
```http
POST /boards/{board_id}/items
Content-Type: application/json
```

**Request Body:**
```json
{
  "type": "CARD",
  "title": "New Task",
  "description": "Task description",
  "position": {"x": 100, "y": 200},
  "style": {
    "fillColor": "#FF0000",
    "fillOpacity": 0.5
  },
  "metadata": {
    "custom_field": "value"
  }
}
```

**Response:** 201 Created

### Get Item
```http
GET /boards/{board_id}/items/{item_id}
```

**Response:** 200 OK

### Update Item
```http
PATCH /boards/{board_id}/items/{item_id}
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "position": {"x": 150, "y": 250},
  "style": {"fillColor": "#00FF00"}
}
```

**Response:** 200 OK

### Delete Item
```http
DELETE /boards/{board_id}/items/{item_id}
```

**Response:** 204 No Content

### Batch Create Items
```http
POST /boards/{board_id}/items/batch
Content-Type: application/json
```

**Request Body:**
```json
{
  "items": [
    {"type": "CARD", "title": "Task 1", "position": {"x": 0, "y": 0}},
    {"type": "CARD", "title": "Task 2", "position": {"x": 200, "y": 0}}
  ]
}
```

**Response:** 201 Created

---

## Comments

### List Comments
```http
GET /boards/{board_id}/comments
```

**Query Parameters:**
- `limit` (int)
- `cursor` (string)
- `include_resolved` (boolean) - Include resolved threads

**Response:** 200 OK
```json
{
  "data": [
    {
      "id": "comment-123",
      "content": "Great idea!",
      "creator_id": "user-123",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:31:00Z",
      "reactions": [{"emoji": "👍", "user_ids": ["user-456"]}],
      "resolved": false
    }
  ]
}
```

### Create Comment
```http
POST /boards/{board_id}/comments
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": "This looks good!",
  "position": {"x": 100, "y": 200},
  "target": {
    "id": "item-123",
    "type": "CARD"
  }
}
```

**Response:** 201 Created

### Update Comment
```http
PATCH /boards/{board_id}/comments/{comment_id}
```

**Request Body:**
```json
{
  "content": "Updated comment"
}
```

### Delete Comment
```http
DELETE /boards/{board_id}/comments/{comment_id}
```

**Response:** 204 No Content

---

## Team Members

### List Team Members
```http
GET /teams/{team_id}/members
```

**Response:** 200 OK
```json
{
  "data": [
    {
      "id": "user-123",
      "email": "user@example.com",
      "name": "John Doe",
      "role": "MEMBER",
      "invited_at": "2024-01-10T10:00:00Z"
    }
  ]
}
```

### Add Team Member
```http
POST /teams/{team_id}/members
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "role": "MEMBER"
}
```

**Response:** 201 Created

### Remove Team Member
```http
DELETE /teams/{team_id}/members/{user_id}
```

**Response:** 204 No Content

---

## Webhooks

### List Webhooks
```http
GET /teams/{team_id}/webhooks
```

**Response:** 200 OK
```json
{
  "data": [
    {
      "id": "webhook-123",
      "url": "https://example.com/webhook",
      "events": ["item.created", "item.updated"],
      "created_at": "2024-01-15T10:30:00Z",
      "status": "ACTIVE"
    }
  ]
}
```

### Create Webhook
```http
POST /teams/{team_id}/webhooks
Content-Type: application/json
```

**Request Body:**
```json
{
  "url": "https://example.com/webhook",
  "events": ["item.created", "item.updated", "item.deleted"],
  "board_ids": ["board-123"]
}
```

**Response:** 201 Created

### Delete Webhook
```http
DELETE /teams/{team_id}/webhooks/{webhook_id}
```

**Response:** 204 No Content

---

## Shapes & Styling

### Shape Types
- `rectangle`
- `circle`
- `diamond`
- `triangle`
- `pentagon`
- `hexagon`
- `octagon`
- `line`
- `arrow`

### Colors
Format: `#RRGGBB` hex codes

Common colors:
- Red: `#FF0000`
- Green: `#00FF00`
- Blue: `#0000FF`
- Yellow: `#FFFF00`

### Create Styled Shape
```http
POST /boards/{board_id}/items
Content-Type: application/json
```

**Request Body:**
```json
{
  "type": "SHAPE",
  "shape": "rectangle",
  "title": "My Shape",
  "position": {"x": 100, "y": 100},
  "geometry": {"width": 300, "height": 150},
  "style": {
    "fillColor": "#FF6B6B",
    "fillOpacity": 0.8,
    "strokeColor": "#000000",
    "strokeWidth": 2
  }
}
```

---

## Pagination

All list endpoints support cursor-based pagination.

**First Request:**
```http
GET /boards?limit=50
```

**Response includes cursor:**
```json
{
  "data": [...],
  "cursor": "abc123xyz"
}
```

**Next Request:**
```http
GET /boards?limit=50&cursor=abc123xyz
```

**No cursor in response** = last page

