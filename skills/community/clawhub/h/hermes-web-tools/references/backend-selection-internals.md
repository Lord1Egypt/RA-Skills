# Web Backend Selection Internals (hermes-agent)

Session detail from the 2026-08-21 web_extract investigation. Code paths are
in `~/.hermes/hermes-agent/tools/web_tools.py` (~1600 lines).

## Resolution chain

```
_get_capability_backend(capability)      # line ~345
  ├─ web.{capability}_backend  → returned unconditionally if set (STRICT)
  └─ _get_backend()                      # line ~223
       ├─ web.backend → returned as-is ("nous" maps to "firecrawl" gateway)
       ├─ selection_exists("web") → "firecrawl"
       └─ never configured → credential ladder:
            tavily > exa > parallel > keenable > firecrawl(key/gateway)
            > searxng > brave-free > ddgs
          then plugin-registered providers, then keyless ring
          (Exa/Parallel/Tavily/Firecrawl/Keenable round-robin)
```

## Key facts

- `_LEGACY_WEB_BACKENDS` = {parallel, firecrawl, tavily, exa, searxng,
  brave-free, ddgs, xai, keenable}. Any other name is looked up in
  `agent/web_search_registry`; unregistered + stored selection → typed error.
- Strict-selection commit: `d7119ea2a` "honor the stored web backend
  selection; no silent backend swaps". Related: `96c2fd3c0` keyless fresh
  installs, `d1eefe6ac` one-shot keyless rescue, `4ea69d9d2` 5-vendor ring.
- web_extract dispatch (line ~1120): resolves provider via registry;
  search-only providers (ddgs/searxng/brave-free/xai) get a typed
  "search-only" error for extract; disabled-plugin case gets a
  `hermes plugins enable <key>` hint.

## Incident transcript (2026-08-21)

- Symptom: `web_extract` on any URL → `"web is configured to use
  'trafilatura' (set via hermes tools), but no registered web extract
  provider has that name."`
- Config had `web.backend: trafilatura` AND `web.extract_backend:
  trafilatura`. `trafilatura` appears nowhere in repo git history — never a
  valid backend; likely a manual config edit or convention imported from
  another tool.
- `.env` had TAVILY_API_KEY and EXA_API_KEY set but ignored — strict
  selection means keys don't reroute traffic once a selection exists.
- Search still worked (`search_backend: ddgs`) — per-capability resolution
  is independent.
- Fix options presented (not applied — user rule): set
  `web.extract_backend tavily`, or clear selections to re-enable
  auto-detect. Requires `/reset` to take effect.

## Useful probes

```bash
grep -n -A5 '^web:' ~/.hermes/config.yaml
grep -oE '^(TAVILY|EXA|FIRECRAWL|PARALLEL|KEENABLE|BRAVE_SEARCH)_API_KEY' ~/.hermes/.env
hermes plugins list | grep 'web-'        # informational only
cd ~/.hermes/hermes-agent && git log --oneline -10 -- tools/web_tools.py plugins/web/
```
