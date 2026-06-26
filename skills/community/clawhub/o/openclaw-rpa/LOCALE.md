# Locale (zh-CN / en-US)

- **`config.example.json`** — committed template; default **`locale`** is **`en-US`**.
- **`config.json`** — local file (create with `python3 scripts/bootstrap_config.py` or copy from the example). Not committed to git so each machine can differ.
- **`SKILL.md`** — short router; tells the agent to read `SKILL.zh-CN.md` or `SKILL.en-US.md`.
- **`SKILL.zh-CN.md`** — full Simplified Chinese instructions.
- **`SKILL.en-US.md`** — English instructions (same behaviour).

## Switch conversation language

```bash
python3 scripts/set_locale.py en-US
python3 scripts/set_locale.py zh-CN
```

If `config.json` does not exist yet, `set_locale.py` copies from `config.example.json` first.

After changing locale, start a **new agent session** or ensure the agent **re-reads** the locale file.
