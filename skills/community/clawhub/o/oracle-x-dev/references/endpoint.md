# Adding a backend endpoint

## The router

`backend/routers/<domain>.py`. A module-level `router = APIRouter()` with no
`prefix` and no `tags` — full paths are written inline on the decorator, which
is why grepping for `/api/macro/board` finds the handler in one hop.

```python
router = APIRouter()

@router.get("/api/macro/board")
async def get_macro_board():
    """The macro board: indices, metals, commodities, ratios."""
    try:
        return await fetch_macro_board()
    except UpstreamUnavailable as error:
        raise _unavailable(error) from error
```

Handlers are plain `async def` at module scope. `response_model=` is used on
the older news and market surfaces, which have pydantic models in
`backend/models/schemas.py`; the newer ones — chains, macro, live, system —
return plain dicts and skip the model. Follow whichever the neighbouring
routes do rather than converting one style to the other.

A POST that starts a background job returns `status_code=status.HTTP_202_ACCEPTED`.

Authenticated routes take the caller as a dependency, never as a parameter:

```python
from dependencies.auth import AuthUser, get_current_user

@router.get("/api/home/watchlist")
async def get_watchlists(user: AuthUser = Depends(get_current_user)):
    return await watchlist_service.list_for(user.id)
```

`get_optional_user` exists for routes that behave differently when signed in
but do not require it.

## Registration

`backend/main.py`, inside `create_app()`, two edits that must both happen:

```python
from routers import (
    ...,
    macro,          # 1. the import block near the top of the file
)

app.include_router(macro.router)  # /api/macro/board, /api/macro/regime
```

The trailing comment listing the paths is the house convention — it is the
only place the route map is readable at a glance. A module may export more than
one router (`ownership.router` and `ownership.admin_router`); register each.

## The service

`backend/services/` holds all behaviour. Services are **modules of functions**,
not classes:

```python
# services/macro_board_service.py
async def fetch_macro_board() -> dict[str, Any]: ...
```

Classes appear only for objects with a lifetime — `liquidation_service`,
`HealthRegistry`, `ServiceCache`. A service must not import `HTTPException`; a
service that does cannot be called from a scheduled job or a test.

## Caching

`backend/services/cache.py` exposes `ServiceCache(maxsize)` and the shared
singletons `home_cache`, `market_cache`, `news_cache`, `ownership_cache`. A
domain with its own eviction needs makes its own
(`chains_cache = ServiceCache(maxsize=16)`).

```python
CACHE_KEY = "macro_board"

cached = market_cache.get(CACHE_KEY)
if cached is not None:
    return cached

board = await _build_board()
market_cache.set(CACHE_KEY, board, TTL_BOARD)
return board
```

Two things to get right:

**Only cache a result that carried data.** Caching an all-errors payload pins
the failure for the whole TTL. The chains service caches its board only when at
least one row came back without an error.

**`get_with_fallback(key, max_age=...)` is the stale path.** When the upstream
is down, serving a known-old value with its age is usually better than serving
nothing — `get_fallback_age(key)` gives the number to show.

## Errors

`HTTPException` is raised in the router. Services raise a domain exception;
the canonical one is `UpstreamUnavailable` from `services/home_service.py`.
Each router keeps a local translator:

```python
def _unavailable(error: UpstreamUnavailable) -> HTTPException:
    return HTTPException(status_code=503, detail=str(error))
```

Which status, and when:

| Situation | Answer |
|---|---|
| Symbol or entity cannot be resolved | `404`, with a detail naming it. Never a placeholder payload. |
| Upstream is dead and `[]` would be a lie | `503` |
| The payload is decoration and the page renders without it | No error — return a `status: "unavailable"` field, or degrade to a stale value with per-row `error` fields |

`create_app()` installs a global exception handler that logs the traceback and
returns `{"detail": "Internal server error"}`, so an unhandled error is never
leaked to a caller — but it is also never explained to one. Handle the failures
you know about.

## After the route works

- Bind it in `frontend/hooks/` — `queries.ts` for the market surface, or the
  per-domain hook.
- If it belongs in the agent skill, add it to `ENDPOINT_GROUPS` in
  `scripts/build_agent_skill.py` and run the script. CI runs `--check`.
- Write the test (see `testing.md`).
