# Localization

## Goal

- Skill docs and agent reasoning: **English first**.  
- **User-visible** hints, errors, setup text: match the **agent/front-end locale**.  
- **Business records** (ship names, ports, cargo, API values): **never translate**.

## Detect locale

Read (first non-empty):

1. `HIFLEET_USER_LOCALE`  
2. `OPENCLAW_USER_LOCALE` / `OPENCLAW_LOCALE`  
3. `CURSOR_AGENT_LOCALE`  
4. `LANG`

Normalize: `zh-CN` / `zh` → Chinese (Simplified); `zh-TW` → Traditional; `en*` → English; default **en**.

## Implementation

```python
from i18n_messages import resolve_user_locale, t
loc = resolve_user_locale()
msg = t("config.missing_api_key", loc)
```

Add keys in **`scripts/i18n_messages.py`** (`en` table is source of truth).

## Agent rule

Before replying to the user, **`read_file` this file** once per session if handling errors or setup. Compose the answer in the resolved locale; keep data rows in original language.
