# Look — Default Configuration

Full default config.json for ocas-look. Copied to `data/ocas-look/config.json` on initialization.

```json
{
  "skill_id": "ocas-look",
  "skill_version": "2.3.0",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "domains": {
    "events": true,
    "food": true,
    "places": true,
    "products": true,
    "civic": true,
    "receipts": true,
    "documents": true
  },
  "user_profile": {
    "diet": "vegetarian"
  },
  "commerce": {
    "auto_purchase": false
  },
  "retention": {
    "days": 30,
    "max_records": 10000
  }
}
```

## Customization

- `user_profile.diet`: adjust per user preference (vegan, omnivore, etc.)
- `commerce.auto_purchase`: never enable without explicit user consent
- `retention.days` and `retention.max_records`: adjust based on storage constraints
