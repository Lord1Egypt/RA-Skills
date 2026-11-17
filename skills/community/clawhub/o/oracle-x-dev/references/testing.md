# Testing

## Backend

`backend/tests/`, run with `cd backend && source venv/bin/activate && python -m pytest`.
About 1634 tests in roughly two minutes.

**`asyncio_mode = "auto"`** is set in `backend/pyproject.toml`, so an async test
is just an async function. There is no `@pytest.mark.asyncio` anywhere in the
suite; adding one is a sign you copied from somewhere else.

```python
async def test_a_single_failure_degrades_rather_than_downs(monkeypatch):
    ...
```

**Style follows cohesion, not policy.** A file about one subject uses bare
`def test_...` functions (`test_macro_regime.py`, `test_chain_anomalies.py`). A
file covering several uses plain `class TestX:` groups with no base class and no
`unittest.TestCase` (`test_chains.py` → `TestRegistry`, `TestEvmFullness`).
Names are sentences describing the guarantee, not the function under test.

**Mocking is `monkeypatch` and nothing else.** No `unittest.mock`, no
`AsyncMock`, no `respx` — 58 files, one tool. Stub at the *service module's*
import site rather than at `httpx`, so the test pins the seam the code actually
uses:

```python
monkeypatch.setattr(ads, "get_json_impersonated", fake_chart)
monkeypatch.setattr(ads, "get_json_yahoo", fake_summary)
monkeypatch.setattr(llm, "generate", fail)
monkeypatch.setattr(history, "STORE_FILE", str(tmp_path / "chain_metrics.json"))
```

Fakes are local `async def` functions or small `class FakeSession` doubles
defined in the test file. Where a module carries process state it exposes a
reset for tests — `ai_notes.reset_state`, `llm.clear_cooldowns`,
`HealthRegistry.reset`, `bans.clear_cache`. Call it rather than reaching into
private state.

**Fixtures are local unless they are auth.** `backend/tests/conftest.py` holds
only the Supabase and auth doubles — `FakeAuth`, `FakeSupabase`, `ADMIN_EMAIL`,
and the `fake_auth`, `patch_supabase`, `admin_emails`, `banned` fixtures.
Everything else is a `@pytest.fixture` in the file that needs it.

**Route tests build a bare app** rather than importing `main.app`, which keeps
them off the lifespan and its background tasks:

```python
app = FastAPI()
app.include_router(auth_router.router)
client = TestClient(app)
```

Sync `fastapi.testclient.TestClient`, no `httpx.ASGITransport`.

**Fixture data is literal.** Small builders at the top of the file — `_board()`,
`_row()`, `_candles(closes)`, `_index(symbol, change)`. No JSON fixture files
except where a parser is tested against a real captured page, and never the
network.

**Docstrings say what regression the file guards.** Module docstring for the
subject, per-test docstring for the failure mode when it is not obvious from
the name. That is the standard to match — a test whose purpose has to be
reverse-engineered gets deleted the next time it fails.

Two files fail when wiring is wrong rather than when logic is wrong, and their
failures are worth reading carefully rather than patching around:
`test_prompts.py` (AST scan of prompt call sites) and
`test_llm_call_site_wiring.py`.

## Frontend

`frontend/lib/*.test.ts`, run with `npm test`. 18 files, about 260 tests.

Vitest with `environment: 'node'` and `include: ['lib/**/*.test.ts']`.
**Deliberately no jsdom and no testing-library** — component behaviour is
verified in a real browser instead, so the suite covers only pure logic. Do not
add a component test here; it will not run.

What that means in practice: tests live where a wrong answer *looks right*.

- `health-format.test.ts` — the clock is a parameter, never `Date.now()`. A
  fixed `const NOW = 1_700_000_000_000` is passed in, and the assertions cover
  the exact Turkish output strings and the case where an idle source must not
  be reported as failed.
- `treemap.test.ts` — `squarify` geometry against a realistic market-cap array,
  with local `area()` and `overlaps()` helpers and an epsilon.
- `chat-job.test.ts` — snake_case → camelCase mapping, backend `null` becoming
  `undefined`, and an unknown enum value degrading to a safe state rather than
  throwing.

No mocks, no `vi.fn()`. If a function needs mocking to be tested, the impurity
belongs in a hook and the logic belongs in `lib/`.

## The gates

```bash
cd backend && ruff check . && ruff format --check . && python -m pytest
cd ../frontend && npm run lint && npm run typecheck && npm test && npm run build
cd .. && python scripts/build_agent_skill.py --check
```

All of them run in `.github/workflows/ci.yml`. `ruff` must be run from
`backend/` — its configuration lives in `backend/pyproject.toml` and the repo
root has none, so running it from the root lints against different defaults and
reports problems CI will not.
