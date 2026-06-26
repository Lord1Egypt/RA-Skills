# Profile Schema Reference

Defines the structure of `~/.openclaw/workspace/me.json`. Read this when writing or updating the profile, or when you need to understand what fields are available.

---

## File Location & Relationship to System Files

| File | Path | Managed by |
|---|---|---|
| Our profile | `~/.openclaw/workspace/me.json` | This skill (user-editable) |
| System profile | `~/.openclaw/memory/user_profile.json` | OpenClaw (auto-updated) |

The two files serve different purposes and coexist without conflict. `me.json` captures what the user told us during onboarding — explicit, human-readable, editable. The system's `user_profile.json` tracks behavioral patterns inferred automatically. When the two conflict, prefer the user's explicit input in `me.json`.

---

## Full Schema

```json
{
  "name": "Billy",
  "role": "AI Algorithm Engineer",
  "company": "Startup (building a product)",
  "timezone": "America/Los_Angeles",
  "primary_goals": ["content creation", "product development"],
  "communication_style": "concise, direct, bilingual (EN/CN)",
  "created": "2026-04-09",
  "updated": "2026-04-09",
  "history": [
    {
      "field": "timezone",
      "old_value": "America/New_York",
      "new_value": "America/Los_Angeles",
      "changed_at": "2026-04-09",
      "note": "User mentioned moving to LA"
    }
  ]
}
```

---

## Field Reference

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Preferred name or nickname |
| `role` | string | No | Job title or primary role |
| `company` | string | No | Employer, project, or "freelance" |
| `timezone` | string | No | IANA timezone ID (e.g., `America/Los_Angeles`) or city name |
| `primary_goals` | string[] | No | What the user mainly wants help with (2–5 items ideal) |
| `communication_style` | string | No | Free-text description of preferred tone and format |
| `created` | date string | Yes | ISO date when profile was first created |
| `updated` | date string | Yes | ISO date of the most recent change |
| `history` | object[] | No | Log of field changes over time (for transparency) |

---

## History Entry Fields

| Field | Type | Description |
|---|---|---|
| `field` | string | Which top-level field was changed |
| `old_value` | any | Value before the change |
| `new_value` | any | Value after the change |
| `changed_at` | date string | ISO date of the change |
| `note` | string | Optional: what prompted the change |

---

## Partial Profiles Are Fine

Not every field needs to be filled. Leave fields out rather than storing placeholders like `null` or `"unknown"` — a lean, accurate profile is more useful than a padded one.

**Minimal valid profile:**
```json
{
  "name": "Sam",
  "created": "2026-04-09",
  "updated": "2026-04-09"
}
```

---

## Adding Custom Fields

The schema is intentionally open. If the user mentions something important that doesn't fit an existing field, add it:

```json
{
  "name": "Billy",
  "preferred_language": "English with Chinese for technical terms",
  "editor": "VS Code",
  "created": "2026-04-09",
  "updated": "2026-04-09"
}
```

Use lowercase snake_case names. Only add values you'd actually use to personalize a response.

---

## Division of Labor with basic-memory

| What | Where |
|---|---|
| Identity (name, role, timezone, goals, style) | `me.json` — set once, updated rarely |
| Decisions, tasks, daily context | `~/.openclaw/workspace/MEMORY.md` |
| Running conversation highlights | `~/.openclaw/workspace/memory/YYYY-MM-DD.md` |

Don't duplicate identity-level facts in `MEMORY.md` if they're already in `me.json`. Let each file own its layer.

---

## What Not to Store

Never write these to `me.json`:

- Passwords, PINs, or passphrases
- API keys or authentication tokens
- Credit card or bank account details
- Social security or national ID numbers
- Medical or health information

If a user tries to save this kind of data, skip the field and explain: "I don't store sensitive data — I'll leave that out."
