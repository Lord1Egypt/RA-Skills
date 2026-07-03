# Localization (mandatory)

## Rules

1. **Default language**: **English** for skill docs and agent reasoning.  
2. **User messages**: Translate hints, errors, setup text to the user’s **agent UI locale** (`resolve_user_locale()` in **`scripts/i18n_messages.py`**).  
3. **Never translate**: vessel names, port names, cargo names, email subjects from brokers, API values, IMO, laycan dates in data tables.

## Locale sources (first match)

`HIFLEET_USER_LOCALE` → `OPENCLAW_USER_LOCALE` → `OPENCLAW_LOCALE` → `CURSOR_AGENT_LOCALE` → `LANG` → **`en`**.

## Usage

```python
from i18n_messages import resolve_user_locale, t
user_msg = t("llm.json_parse_failed", resolve_user_locale())
```

## Agent

At session start (or before first user-facing error), **`read_file` this file**. Reply in the resolved locale; keep business rows verbatim.

## Related skills

**`hifleet-schedule`** uses the same i18n pattern for schedule queries.
