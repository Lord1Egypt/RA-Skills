---
name: oracle-x-dev
description: Extend the Oracle-X financial terminal codebase — add or change a FastAPI endpoint, wire a new upstream data source into the health badge, register a blockchain adapter, write a prompt or an LLM-backed note, and test any of it the way this repository tests things. Use whenever work touches backend/routers, backend/services, backend/prompts, backend/tests or frontend/lib in the Oracle-X repo, whenever someone asks how to add a route, a data provider, a chain, a prompt or a note here, and whenever a change is about to be committed and needs to clear the four quality gates. Consult it before writing the first line, because this codebase has conventions — one-service routers, duck-typed chain adapters, prompts as files with literal call sites, monkeypatch at the import site — that a reasonable-looking change will violate silently.
version: "1.3.0"
license: Complete terms in LICENSE.txt
metadata:
  homepage: "https://github.com/Yigtwxx/OracleX"
  openclaw:
    emoji: "🛠️"
    homepage: "https://github.com/Yigtwxx/OracleX"
    requires:
      bins:
        - python3
        - git
---

# Working in Oracle-X

A FastAPI backend and a Next.js 14 frontend for a self-hosted financial
terminal. This skill is about extending it. For what the system *is* — why
authorization lives in the application layer, why migrations are applied by
hand — read the repository's `CLAUDE.md` first; it is short and this skill does
not repeat it.

Run everything from the right directory. The backend imports as
`from services... import ...` with `pythonpath = ["."]`, so it only works from
`backend/`, and `ruff` reads `backend/pyproject.toml` (`line-length = 100`) —
running it from the repo root silently picks up different defaults.

## Before you commit

Four gates, all of them in CI, all of them cheap enough to run locally:

```bash
cd backend && source venv/bin/activate
ruff check . && ruff format --check .
python -m pytest                                  # ~1900 tests, ~2 min

cd ../frontend
npm run lint && npm run typecheck && npm test && npm run build

cd .. && python scripts/build_agent_skill.py --check
python scripts/build_repo_facts.py --check
```

The last one exists because the API skill's endpoint reference is generated
from the app's OpenAPI schema. If you touched a route that the skill documents,
regenerate it or the build fails.

## What are you doing?

| Task | Read |
|---|---|
| Adding or changing an endpoint | `references/endpoint.md` |
| Calling a new external API | `references/upstream.md` |
| Adding a blockchain | `references/chains.md` |
| Writing a prompt, or anything LLM-backed | `references/llm.md` |
| Writing tests | `references/testing.md` |

Each reference is the mechanics: exact file paths, the order of steps, the
signatures that matter. Read the one that fits before writing code — every one
of them documents at least one convention that a sensible-looking change gets
wrong.

## The rules that bite

These are the mistakes this codebase actually catches in review, ordered by how
expensive they are to find later.

**Identity comes from `AuthUser`, never from the request.** The backend holds
Supabase's service role key, which bypasses Row Level Security, so Supabase
enforces nothing here. A `user_id` arriving in a path, query or body is
attacker-controlled. Depend on `get_current_user` and read the id off what it
returns — it is also the single choke point that refuses suspended accounts, so
routing around it opens two holes rather than one.

**Unmeasured is `None`, never `0`.** A zero fee and a fee that could not be
read render identically on the board and mean opposite things. This holds
everywhere a number reaches the UI, and the chain adapters state it in every
docstring for a reason.

**The API declines rather than guessing.** 404 when a symbol cannot be
resolved, 503 when an upstream is dead and an empty list would be a lie, and no
error at all where the payload is decoration and the page renders without it.
Never a placeholder number. In a trading terminal a plausible wrong figure is
worse than an error.

**Routers hold no logic.** Validate, call one service, shape the response.
`HTTPException` is raised in the router; a service raises a domain error
(`UpstreamUnavailable`) and the router translates it. A service that imports
`HTTPException` is a service that cannot be called from a job or a test.

**Never call `httpx` directly.** `services/http_client.py` wraps every helper
in an observer that attributes the call to a health category. A direct call is
invisible to the LIVE badge, which means a dead provider reports as healthy.
The same applies to a new hostname: unmapped hosts are dropped silently.

**Never call a provider SDK directly.** `services/llm` resolves an ordered
chain so one provider's outage is not the terminal's outage, and it strips
`<think>` blocks, handles quota cooldowns and retries in one place.

**Prompt names must be string literals.** `test_prompts.py` walks the AST of
the whole backend looking for literal arguments to `load_prompt` and
`render_prompt`. A computed name passes review and fails the suite, and more
importantly it defeats the check that every placeholder is supplied and every
template is still used.

**Comments explain why.** The existing code records what broke before and what
the alternative cost. A comment restating the line below it is noise. Write
code, identifiers and comments in English.

## Where things live

```
backend/
  routers/      thin: validate, call one service, shape the response
  services/     all behaviour; modules of functions, classes only for state
    llm/        the provider chain — the only path to a model
    chains/     per-chain adapters + registry + anomaly detection
  prompts/      <domain>/<name>.md, loaded by name, never inline
  models/       pydantic response models (newer surfaces return plain dicts)
  dependencies/ auth and rate limiting
  tests/        pytest, asyncio_mode=auto, monkeypatch only
  evals/        standalone CLI scripts — not pytest, not in CI
frontend/
  hooks/        API bindings: queries.ts plus one hook per domain
  lib/          pure logic — this is where the vitest suite lives
  components/   presentational
```

The split in `frontend/` is the load-bearing part: tests cover `lib/` because
that is where a wrong answer looks right. Component behaviour is checked in a
real browser instead, which is why there is no jsdom and no testing-library.

## Adding a surface end to end

The order matters — each step depends on the one before it, and the last two
are the ones people forget.

1. **Service** in `backend/services/`, a module of functions. Cache through
   `services/cache.py` if the upstream is slow or rate-limited, and only cache
   a result that actually carried data.
2. **Upstream calls** through `services/http_client.py`, with the new host
   mapped in `health_registry._HOST_MAP` and its name added to the category's
   provider list.
3. **Router** in `backend/routers/`, registered in `create_app()` in
   `backend/main.py` — both the import block and an `include_router` line with
   the trailing comment naming its paths.
4. **Tests** in `backend/tests/`, stubbing the upstream at the service module's
   import site.
5. **Frontend binding** in `frontend/hooks/`, with any derivation logic in
   `frontend/lib/` and a vitest file beside it.
6. **The agent skill**, if the endpoint belongs in it: one line in
   `ENDPOINT_GROUPS` in `scripts/build_agent_skill.py`, then regenerate.
