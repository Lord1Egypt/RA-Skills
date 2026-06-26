# Upstream Sources

This skill is an orchestrator. It does not natively crawl property portals. It calls upstream skills, plugins, or clients through source adapters, then normalizes their output into the Property Advisor listing contract.

## Implemented Adapters

### `ok`

Delegates fetching and non-UK publishing to `ok-core-skill`.

Discovery order:

1. `OK_CORE_SKILL_ROOT`
2. `PROPERTY_OK_SKILL_ROOT`
3. `/Users/a58/Desktop/skills/ok-core-skill`
4. `/Users/a58/Desktop/ok-core-skill/skills/ok-core-skill`

Runtime order:

1. `uv run python scripts/cli.py`
2. `ok-core-skill/.venv/bin/python scripts/cli.py`

Do not call `python3 scripts/cli.py` directly for OK. Always preflight before search or publish.

### `gt`

Delegates UK/Gumtree fetching and publishing to `gt-core-skill`.

Discovery order:

1. `GT_CORE_SKILL_ROOT`
2. `PROPERTY_GT_SKILL_ROOT`
3. Workspace `.agents/skills` and `skills`
4. `$CODEX_HOME/skills` / `~/.codex/skills`
5. Local desktop `gt-core-skill` development paths

Runtime rules:

- Prefer Bridge mode with search and detail support.
- Bridge mode uses `uv run python scripts/cli.py`, then `.venv/bin/python scripts/cli.py` fallback.
- Use API mode only when Bridge mode is unavailable.
- `logged_in=false` is a warning, not a search preflight failure.
- If API mode cannot hydrate details, surface `detail_degraded_reason` in `缺失/未知`.

## Optional External Providers

External providers are optional capabilities, not default dependencies.

Use them only when all of these are true:

1. The user needs a platform beyond implemented OK/GT adapters, or explicitly asks for that platform.
2. The provider/plugin/skill is installed and available in the current environment.
3. Required credentials such as API keys are configured.
4. The user confirms use when installation, credentials, or paid API usage may be involved.
5. Returned records are normalized to the Property Advisor listing contract before analysis.

### HasData

HasData may be used for Zillow, Redfin, Airbnb, or generic URL/page extraction when installed and configured.

Required setup:

```bash
openclaw plugins install clawhub:@hasdata/hasdata-openclaw-plugin
```

Required credential:

```bash
HASDATA_API_KEY
```

If the user asks for Zillow/Redfin/Airbnb/global URL extraction and HasData is not installed or configured, explain that the optional provider is missing and show the setup command. Do not claim the platform was searched.

### Other External Skills

Other ClawHub skills may be used only through a source adapter or normalization layer. Do not pass third-party raw output directly into the final table.

## Normalization Contract

Every upstream source must produce listing records compatible with the existing data contract:

- `title`
- `price`
- `location`
- `url`
- `image_url` / `images`
- `description`
- `address`
- `lat` / `lng`
- `attributes`

If detail hydration is unsupported or fails, keep the list result and set an explicit degradation reason.
