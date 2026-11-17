# Test isolation for module-level mutable state (Python)

When auth/cache/rate-limit state lives at module level (dicts, counters, timestamps),
tests that mutate it in one case bleed into the next. Standard isolation techniques:

## 1. `importlib.reload()` before each test

This is the robust technique for environments preserving module identity across tests
unreliably, or when the module re-reads env/class state on each load.

```python
import importlib
import auth                     # module with mutable state (locked_until, failed_attempts, etc.)

def reload_auth():
    importlib.reload(auth)
    return auth.login

def test_lockout():
    login = reload_auth()
    # ... manipulate state ...
```

## 2. Read state via module reference, not captured ref

WRONG — captured ref still points to old dict after reload:
```python
login, _failed_attempts = reload_auth()  # BAD: stale ref
_failed_attempts.get("admin", 0)         # always 0—dict was replaced
```

RIGHT — read fresh from module after each mutation:
```python
login = reload_auth()
auth._failed_attempts.get("admin", 0)    # OK: reads current module state
```

## 3. `us._users.clear()` fixture

For simple in-memory services with a well-known module-level dict, an autouse fixture
is cheaper and less error-prone than reload:

```python
import user_service as us
from user_service import create_user, get_user, delete_user

@pytest.fixture(autouse=True)
def _reset_users():
    us._users.clear()
    yield
```

**When to prefer each:**
- Prefer `clear()` when the state is a plain module-level dict and the test target
  imports the module normally.
- Prefer `reload()` when the module also reads env/config at import time, or when
  import side effects must be fresh.

## 4. **Known vs unknown users for failure counters**

Auth code intentionally does NOT increment `_failed_attempts` for unknown users
(user-enumeration protection). Tests for counter logic must use a **known user**:

```python
login("admin", "wrongpass")              # known user → counter increments
auth._failed_attempts.get("admin")       # → 1
```

Using an unknown user for counter tests always returns 0 — that's correct behaviour,
not a test bug.

## 5. **Env var isolation**

Config from `os.environ` is read at import time. Set env vars BEFORE reload:

```python
os.environ["AUTH_MAX_ATTEMPTS"] = "3"
importlib.reload(auth)                  # picks up new env
```

## When to use

- Rate-limit sliding windows (`_rate_history`)
- Lockout timers (`_locked_until`)
- Failure counters (`_failed_attempts`)
- Cache dicts
- Any mutable global that `login()` / `process()` / `handle()` mutates
