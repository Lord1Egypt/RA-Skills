# config.json example (hifleet-opentonnages)

```json
{
  "hifleet_api_key": "from HiFleet website",
  "hifleet_charter_api_base": "https://api.hifleet.com/openclaw/vessel/charter",
  "hifleet_liner_api_base": "https://api.hifleet.com/openclaw/vessel/charter/liner",
  "charter_enrich_url": "https://api.hifleet.com/openclaw/vessel/charter/enrich-row"
}
```

`hifleet_liner_api_base` — contact fetch **`POST …/unlock`** (see **`CONTACT_API.md`**).

Optional: `HIFLEET_USER_LOCALE` for localized error/setup text.

**No** IMAP / mailbox fields in this skill.
