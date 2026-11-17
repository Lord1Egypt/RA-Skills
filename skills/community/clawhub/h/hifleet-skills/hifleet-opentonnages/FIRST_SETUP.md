# First setup

## Capability

**HiFleet public open tonnage + public cargo** (marketplace data). Requires **`hifleet_api_key`** only — **no mailbox**.

| Question type | Route |
|---------------|--------|
| Public / platform **open vessels** | **V** |
| Public / platform **cargo** | **G** |

**Not this skill**: liner schedule → **hifleet-schedule**.

## Config

```json
{
  "hifleet_api_key": "from HiFleet website",
  "hifleet_charter_api_base": "https://api.hifleet.com/openclaw/vessel/charter",
  "hifleet_liner_api_base": "https://api.hifleet.com/openclaw/vessel/charter/liner",
  "charter_enrich_url": "https://api.hifleet.com/openclaw/vessel/charter/enrich-row"
}
```

Get key at [mytonnages.hifleet.com](https://mytonnages.hifleet.com).

## Product note (tell users)

- **Search** returns vessel/cargo details; **contacts are not shown by default**.
- To get phone/email/owner: user provides **record id** from the list (or asks for **all**); uses API points per row — see **`CONTACT_API.md`**.
- Say **「获取联系方式」** — do not say 「解锁」.
- Optional **enrich-row** adds ship archive, tags, port distance.

## Language

`HIFLEET_USER_LOCALE` / `OPENCLAW_USER_LOCALE` — see **`LOCALIZATION.md`**.
