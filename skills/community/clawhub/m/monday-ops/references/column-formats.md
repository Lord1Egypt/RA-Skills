
When calling `change_item_column_values` or `create_item` with column values, each column type requires a specific JSON format. The values are passed as a JSON object where keys are **column IDs** (not display names).

## How to Find Column IDs

Call `get_board_schema` with the board ID. The response lists each column with:
- `id` — the internal ID to use in API calls (e.g., `status`, `date4`, `text0`, `numbers9`)
- `title` — the human-readable name (e.g., "Status", "Due Date", "Description")
- `type` — the column type that determines the value format
- `settings_str` — JSON string with the column's configuration (allowed statuses, labels, etc.)

## Column Types and Value Formats

### Status Column (`type: "status"`)

Use the display label. The available labels are defined in `settings_str`.

```json
{"label": "Working on it"}
```

Common default labels: `"Working on it"`, `"Done"`, `"Stuck"`, `""` (empty/default).

To find available labels, parse `settings_str` → look for the `labels` object which maps index numbers to label text.

### Date Column (`type: "date"`)

```json
{"date": "2026-05-15"}
```

With time:
```json
{"date": "2026-05-15", "time": "14:30:00"}
```

### People Column (`type: "people"`)

Requires user IDs. Get these from `list_users_and_teams`.

Single person:
```json
{"personsAndTeams": [{"id": 12345678, "kind": "person"}]}
```

Multiple people:
```json
{"personsAndTeams": [
  {"id": 12345678, "kind": "person"},
  {"id": 87654321, "kind": "person"}
]}
```

Team:
```json
{"personsAndTeams": [{"id": 98765, "kind": "team"}]}
```

### Text Column (`type: "text"`)

```json
"Plain text value here"
```

Or as object:
```json
{"text": "Plain text value here"}
```

### Number Column (`type: "numbers"`)

```json
42
```

Or as string:
```json
"42"
```

### Dropdown Column (`type: "dropdown"`)

Use label IDs from `settings_str` → `labels` array.

```json
{"ids": [1, 3]}
```

To find label IDs, parse `settings_str` for the dropdown. Each label has an `id` and `name`.

### Checkbox Column (`type: "checkbox"`)

```json
{"checked": true}
```

### Email Column (`type: "email"`)

```json
{"email": "user@example.com", "text": "User Name"}
```

### Phone Column (`type: "phone"`)

```json
{"phone": "+1234567890", "countryShortName": "US"}
```

### Link Column (`type: "link"`)

```json
{"url": "https://example.com", "text": "Example Site"}
```

### Long Text Column (`type: "long_text"`)

```json
{"text": "This is a longer description with\nmultiple lines of content."}
```

### Timeline Column (`type: "timeline"`)

```json
{"from": "2026-05-01", "to": "2026-05-31"}
```

### Rating Column (`type: "rating"`)

```json
{"rating": 4}
```

Values typically range from 1-5.

### Tags Column (`type: "tags"`)

Uses tag IDs. Tags are workspace-level entities.

```json
{"tag_ids": [100, 200, 300]}
```

### Country Column (`type: "country"`)

```json
{"countryCode": "US", "countryName": "United States"}
```

### Week Column (`type: "week"`)

```json
{"week": {"startDate": "2026-05-04", "endDate": "2026-05-10"}}
```

### Hour Column (`type: "hour"`)

```json
{"hour": 14, "minute": 30}
```

### Color Picker Column (`type: "color_picker"`)

```json
{"color": {"hex": "#FF5733"}}
```

### Formula Column (`type: "formula"`)

Formula columns are read-only — you cannot set their values. They compute automatically based on other column values.

### Mirror Column (`type: "mirror"`)

Mirror columns are read-only — they reflect values from connected boards.

### Auto-number Column (`type: "auto_number"`)

Auto-number columns are read-only — they auto-increment.

## Clearing a Column Value

To clear/reset any column value, pass an empty object or null:

```json
{}
```

Or for some types:
```json
""
```

## Example: Setting Multiple Columns at Once

When creating or updating an item, you can set multiple columns in a single call:

```json
{
  "status": {"label": "Working on it"},
  "date4": {"date": "2026-05-15"},
  "person": {"personsAndTeams": [{"id": 12345, "kind": "person"}]},
  "numbers9": 42,
  "text0": "Sprint 5 deliverable"
}
```

The keys (`status`, `date4`, `person`, etc.) are the column IDs from `get_board_schema`, NOT the display names.

## Common Pitfalls

1. **Using display names as keys** — Always use the internal column `id`, not the `title`.
2. **Wrong status label** — The label must exactly match one of the options in the column's settings. Case-sensitive.
3. **Missing `kind` in people values** — Always include `"kind": "person"` or `"kind": "team"`.
4. **Sending numbers as strings for number columns** — While sometimes accepted, prefer sending actual numbers.
5. **Setting read-only columns** — Formula, mirror, and auto-number columns cannot be set.
