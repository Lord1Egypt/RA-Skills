# Kaiten API Reference

Full interactive docs: https://developers.kaiten.ru

## Authentication

All requests require `Authorization: Bearer <token>` header.

API base: `https://<company>.kaiten.ru/api/latest/`

## Entities

### Space
Top-level container for boards.
```json
{
  "id": 180884,
  "title": "My Space",
  "created": "2022-03-21T09:12:24.509Z"
}
```

### Board
A Kanban board within a space. Contains columns and lanes.
```json
{
  "id": 442783,
  "title": "My Board",
  "space_id": 180884
}
```

### Column
Vertical divisions on a board (e.g., "To Do", "In Progress", "Done").
Has `sort_order` for ordering. May have subcolumns via `/columns/{id}/subcolumns`.

### Lane (Swimlane)
Horizontal divisions on a board for categorization.

### Card (Task)
The primary work item.

Key fields:
- `id` — unique ID
- `title` — card title
- `description` — markdown description
- `board_id`, `column_id`, `lane_id` — location on board
- `owner_id` — creator/owner user ID
- `state` — 1=active, 2=archived
- `condition` — 1=normal, 2=blocked, 3=in-progress
- `asap` — boolean priority flag
- `due_date` — deadline (ISO 8601)
- `planned_start`, `planned_end` — planned dates
- `size`, `size_text` — story points / estimate
- `tag_ids` — array of tag IDs
- `sort_order` — position in column
- `type_id` — card type
- `sprint_id` — sprint association
- `created`, `updated` — timestamps

### Tag
Labels for categorization.
```json
{"id": 912182, "name": "🔥 ASAP"}
```

### User
```json
{
  "id": 179308,
  "full_name": "Nikita TRATOROV",
  "email": "support@nixprosoft.ru",
  "role": 1
}
```
Roles: 1=admin, 2=member

### Comment
```json
{
  "id": 123,
  "text": "Comment text (supports markdown)",
  "author_id": 179308,
  "created": "2024-01-01T00:00:00Z"
}
```

### Checklist & Checklist Item
```json
{
  "id": 1,
  "name": "Checklist name",
  "items": [
    {"id": 1, "text": "Item text", "checked": false, "sort_order": 1}
  ]
}
```

### Time Log
```json
{
  "time_spent": 60,
  "comment": "Worked on feature",
  "user_id": 179308,
  "created": "2024-01-01T00:00:00Z"
}
```
`time_spent` is in minutes.

## Filtering Cards

GET `/cards` supports query params:
- `limit` — max results (default 20)
- `offset` — pagination offset
- `board_id` — filter by board
- `column_id` — filter by column
- `lane_id` — filter by lane
- `owner_id` — filter by owner
- `tag_id` — filter by tag
- `condition` — filter by condition (1/2/3)
- `state` — filter by state (1=active, 2=archived)

## Search

GET `/search?query=<text>` — full-text search across cards.

## Webhooks

POST `/webhooks` — create webhook for real-time notifications.

GET `/webhooks` — list active webhooks.

## Error Handling

- `401` — invalid or expired token
- `403` — insufficient permissions
- `404` — entity not found
- `422` — validation error (check response body for details)
- `429` — rate limited (respect Retry-After header)
