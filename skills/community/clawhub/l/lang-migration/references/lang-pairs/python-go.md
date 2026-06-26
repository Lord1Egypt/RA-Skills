# Language Pair: Python → Go

**Difficulty tier**: Moderate

**Key differences**:
- Memory model: Python GC / Go GC (similar; no ownership tracking needed)
- Type system: Python dynamic / Go static with interfaces (no generics before 1.18)
- Error handling: Python exceptions / Go multi-return `value, error`
- Concurrency: Python GIL+asyncio / Go goroutines+channels
- OOP: Python classes / Go structs + interfaces (no inheritance)
- Nullability: Python `None` / Go nil + zero values

---

## Pre-Mapped Core Types

| Python | Go | Equivalence | Notes |
|---|---|---|---|
| `int` | `int64` | behavioral | Go int is platform-width; use int64 explicitly for portability |
| `float` | `float64` | structural | Both IEEE 754 double |
| `bool` | `bool` | structural | |
| `str` | `string` | structural | Go strings are immutable byte sequences (UTF-8) |
| `bytes` | `[]byte` | structural | |
| `None` | `nil` | structural | Context-dependent (nil pointer, nil interface, nil slice) |
| `list[T]` | `[]T` (slice) | structural | |
| `tuple[A,B]` | struct with fields | structural | Go has no anonymous tuples (use named struct) |
| `dict[K,V]` | `map[K]V` | behavioral | Go map iteration order is randomized intentionally |
| `set[T]` | `map[T]struct{}` | structural | |
| `Optional[T]` | `*T` or `(T, bool)` | structural | Use pointer for optional struct; bool pair for optional value |

## Standard Library Mapping

| Python | Go | Equivalence | Notes |
|---|---|---|---|
| `os.path.join` | `filepath.Join` | structural | |
| `os.listdir` | `os.ReadDir` | structural | |
| `os.environ.get` | `os.Getenv` | structural | |
| `open(f)` | `os.Open` | structural | |
| `json.dumps` | `json.Marshal` | structural | |
| `json.loads` | `json.Unmarshal` | structural | |
| `re.compile` | `regexp.MustCompile` | structural | |
| `hashlib.sha256` | `crypto/sha256` | structural | |
| `time.time()` | `time.Now().Unix()` | structural | |
| `random.random()` | `rand.Float64()` | behavioral | Different algorithm |
| `threading.Thread` | `go func(){}()` | structural | Goroutines are lighter |
| `asyncio` | goroutines + channels | structural | Different model but same concurrency goals |
| `subprocess.run` | `exec.Command` | structural | |
| `logging` | `log` or `zap` | structural | |
| `argparse` | `flag` or `cobra` | structural | |

## Common Third-Party Libraries

| Python | Go | Equivalence | Notes |
|---|---|---|---|
| `requests` | `net/http` (stdlib) | structural | No third-party needed |
| `sqlalchemy` | `database/sql` + driver | structural | |
| `pydantic` | struct + `encoding/json` tags | structural | |
| `click` | `cobra` | structural | |
| `pytest` | `testing` package (stdlib) | structural | |
| `numpy` | `gonum.org/v1/gonum` | behavioral | API differs significantly |

---

## Error Handling Pattern

**Python:**
```python
def read_file(path: str) -> str:
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        raise IOError(f"not found: {path}")
```

**Go:**
```go
func readFile(path string) (string, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return "", fmt.Errorf("not found: %s: %w", path, err)
    }
    return string(data), nil
}
```

**Rule**: Every `try/except` block becomes a multi-return function. Each `except` clause becomes an `if err != nil` block. Maintain 1:1 mapping.

---

## Class → Struct + Interface

**Python:**
```python
class Storage:
    def __init__(self, path: str):
        self.path = path
    def read(self, key: str) -> bytes:
        ...
    def write(self, key: str, data: bytes):
        ...
```

**Go:**
```go
type Storage interface {
    Read(key string) ([]byte, error)
    Write(key string, data []byte) error
}

type FileStorage struct {
    path string
}

func NewFileStorage(path string) *FileStorage {
    return &FileStorage{path: path}
}

func (s *FileStorage) Read(key string) ([]byte, error) { ... }
func (s *FileStorage) Write(key string, data []byte) error { ... }
```

---

## Anti-Patterns

| Wrong | Why | Correct |
|---|---|---|
| `interface{}` for everything | Loses type safety | Use concrete types or generics (Go 1.18+) |
| Ignoring returned errors `_` | Hides Python exception flow | Always handle; match Python's except structure |
| Using `panic` for logic errors | Not equivalent to exceptions | Use error returns |
| Global `init()` for class-level state | Hides initialization order | Use explicit constructor functions |

---

## ⛔ Known Migration Traps (Python → Go)

These patterns have historically caused structural drift that survived compilation and basic testing.
**Read this section before beginning P4 translation.** Check each trap against the IPO registry
for the function being translated before writing a single line of Go.

---

### Trap 1: Post-Construction Attribute Setting

**Python pattern:**
```python
agent = start_subagent(config)
agent.inc_out = True    # line 47 — NOT inside start_subagent()
agent.verbose = False   # line 48 — NOT inside start_subagent()
```

**Failure mode**: The Go `NewSubagent()` constructor does not set `IncOut = true` or `Verbose = false`
because those lines appear in the **caller**, not in the callee. If P3 only documented `start_subagent`,
these assignments are invisible. The Go struct uses zero-value defaults (`false` for bool),
which is silently wrong.

**Detection**: Before translating any constructor/factory function, read **all call sites**.
Look for `obj.attr = X` immediately after the call. These belong in the caller's `side_effects`
in the IPO registry.

**Fix protocol**:
1. In `start_subagent`'s IPO entry: add `translation_notes` warning callers to set these fields
2. In the caller's IPO entry: list in `side_effects`: `"sets agent.inc_out = True [line 47]"`
3. In Go: set the fields in the caller after construction, matching the Python line-for-line

**Root cause category**: `side_effect_dropped`

---

### Trap 2: Multi-Branch Turn-Based Callbacks

**Python pattern (abbreviated):**
```python
def on_turn_end(turn: int, mode: str):
    if turn % 65 == 0 and mode != "plan":  # branch A
        ask_user(...)
    elif mode == "plan" and turn % 5 == 0 and turn >= 10:  # branch B
        prompt_plan_review(...)
    if turn > 90 and mode == "plan":       # branch C — separate if, not elif
        force_ask_user(...)
```

**Failure mode**: Go translation merges branches B and C into one `else if`, or uses a single
`if/else if/else` chain when the Python uses two separate `if` blocks. The 90-turn forced
callback then never fires independently of the 5-turn cadence.

**Detection rule**: Count `if/elif/else/for/while` branches in the Python body.
The number of `step` entries in the IPO registry must equal or exceed this count (READ_EVIDENCE
`branch_count` field). If the Go translation has fewer `if` blocks than the Python, branches are collapsed.

**Magic number check**: For functions with `type: iteration_limit` magic numbers (65, 5, 10, 90),
boundary-value testing (N-1, N, N+1) is mandatory in P5 — see phase-5-verification.md.

**Root cause category**: `control_flow_collapsed`

---

### Trap 3: Compound Processing with Conditional Secondary Transform

**Python pattern:**
```python
def fetch_content(url: str, text_only: bool, maxlen: int) -> str:
    content = get_html(url, text_only=True)       # primary fetch
    if text_only:
        content = smart_format(content, maxlen // 3)  # secondary truncation
    return content
```

**Failure mode**: Go translation implements the primary fetch but omits the secondary
`smart_format` call because it appears as a one-line conditional after the main logic.
Result: content is 3× longer than expected in text_only mode.

**Detection**: In the IPO `process.steps`, any step whose `desc` starts with "If [flag]:" after
a primary operation is a **mandatory separate step** — not optional commentary.
Count steps in the IPO entry. If the Go function body has fewer conditional blocks than steps,
secondary transforms have been dropped.

**Magic number check**: `maxlen // 3` is a `magic_number` of type `threshold`. It must appear
as a named constant in Go — not as `maxlen/3` inline without a name.

**Root cause category**: `control_flow_collapsed` (secondary) + `magic_number_decontextualized` (constant)

---

### Trap 4: dict Ordering

**Python pattern:**
```python
result = {}
for key in sorted_keys:
    result[key] = compute(key)
return result   # dict preserves insertion order (Python 3.7+)
```

**Failure mode**: Go `map[string]T` iterates in randomized order. Any downstream code
that depends on the iteration order of this map will produce non-deterministic results.

**Compensation**: Use `github.com/elliotchance/orderedmap` or return `[]Entry` (key-value slice)
where Python dict insertion order is semantically important.

**Detection**: Check if the function's callers iterate the dict in order, compare order-dependent
outputs (e.g., joined strings, ranked lists). If yes, ordered map is required.

**Root cause category**: `ecosystem_gap_unapplied`

---

### Trap 5: Implicit Model Capability Assumption in Agent/LLM Integrations

**Python pattern:**
```python
# conductor.py:277-279 — design assumes consumer (Claude) will infer to call GET /chat
unread = sum(1 for m in chat_messages if m.get("role") == "user" and not m.get("read"))
summary = f"... | {unread}条用户未读消息, ..."
# No explicit instruction to fetch messages — Claude infers it from context
```

**Failure mode**: The Go translation faithfully replicates `conductorPrompt` (count-only). This is
**correct** — the function is not the bug. The bug is that the Go deployment runs a smaller model
(e.g., Qwen3.5) that does not implicitly infer "when unread > 0, call GET /chat first."
The first Copilot "fix" (embedding message body directly) was wrong — it changed the source design.

**The correct investigation path**:
1. **T1**: Does Go `conductorPrompt` match Python `conductor.py:277-279`? → YES → source-faithful
2. **T2**: Read `conductor.py:277-279` — source only passes count → source_matches_target: true
3. **T3**: Check consumer path — does the system prompt have a `code_run` example for `GET /chat`? Does it have an explicit trigger rule? → NO → `IMPLICIT_CAPABILITY_ASSUMPTION`
4. **Fix**: Add `GET /chat?last=20` code_run example + explicit "when unread > 0, call GET /chat first" rule to the system prompt. **Do not change `conductorPrompt` logic.**

**Detection**: Look for IPO entries where `inferred_invariants` should include capability assumptions:
```yaml
inferred_invariants:
  - "consumer LLM can infer from unread count that it must call GET /chat to read content
     [inferred from: no explicit fetch instruction in Python prompt; source used Claude]"
```
When porting to a smaller model, every inferred invariant of this type requires an explicit
instruction or code_run example in the target system prompt.

**Root cause category**: `implicit_capability_assumption`

## Ecosystem Gaps

| Python | Gap | Compensation |
|---|---|---|
| `dict` preserves order (3.7+) | `map` order randomized | Use `github.com/elliotchance/orderedmap` |
| Negative indices `arr[-1]` | Panics | Use `arr[len(arr)-1]` |
| `**kwargs` | No equivalent | Use variadic `options ...Option` pattern or struct |
| `@property` decorator | No equivalent | Use getter/setter methods |

## Testing Toolchain

| Python | Go | Notes |
|---|---|---|
| `pytest` | `go test ./...` | Built-in |
| `pytest.raises` | `if err == nil { t.Fatal(...) }` | |
| `unittest.mock` | `testify/mock` (or no mock — prohibited) | No mocks; use real implementations |
| `mypy` | `go vet` + compiler | |
| `black` | `gofmt` | Run: `gofmt -w .` |
| `pytest-benchmark` | `b.N` benchmark functions | |

## Build / CI

```yaml
# Source (Python):
- run: pip install -r requirements.txt && pytest

# Target (Go):
- run: go test ./...
- run: go vet ./...
- run: gofmt -l . | grep . && exit 1 || true
```
