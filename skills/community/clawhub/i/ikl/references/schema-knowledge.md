# knowledge.json Schema

## Structure

```json
{
  "entries": [
    {
      "id": "k001",
      "category": "personal_facts",
      "level": 2,
      "key": "birthday",
      "value": "1990-01-15",
      "added_at": "2026-01-01T00:00:00Z"
    }
  ]
}
```

## Fields

- **id**: Unique entry identifier (k001, k002, etc.)
- **category**: Must match a category in permissions.json
- **level**: Sensitivity level (must match a defined level for that category)
- **key**: Short descriptor (birthday, city, job_title, etc.)
- **value**: The actual information
- **added_at**: When this entry was created/updated

## Rules

- Every entry MUST have a category and level — this is what the permission gate checks
- The agent should only retrieve entries where `level <= allowed_level` for the requester
- When the user shares new information, classify it and add it here
- Periodically review with the user to ensure accuracy
