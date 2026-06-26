# contacts.json Schema

## Structure

```json
{
  "contacts": {
    "<contact_id>": {
      "name": "Display name",
      "relationship": "friend",
      "identifiers": {
        "telegram_user_id": "123456789",
        "telegram_username": "alice"
      },
      "added_at": "ISO 8601 timestamp",
      "notes": "Optional context"
    }
  },
  "relationship_types": [
    "partner", "family", "close_friend", "friend",
    "colleague", "acquaintance", "stranger"
  ],
  "defaults": {
    "unknown_sender": "stranger"
  }
}
```

## Fields

- **contact_id**: Unique key (use lowercase name or handle)
- **relationship**: One of the relationship_types
- **identifiers**: Platform-specific IDs for matching incoming messages. Include all known identifiers (telegram_user_id, telegram_username, discord_id, etc.)
- **added_at**: When this contact was registered
- **notes**: Optional context about how user knows this person

## Matching Logic

When a message arrives, match the sender against all contacts' `identifiers`. First match wins. If no match → `stranger`.
