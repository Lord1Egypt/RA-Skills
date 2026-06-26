---
name: pattern-code-node-discipline
description: Pure-function-plus-glue convention for n8n Code nodes — extract logic to n8n-functions/, inject via {{@js|py:...}}, pair with a test. Validator hard-fails otherwise.
user-invocable: false
---

# Pattern: Code-node discipline

n8n Code-node logic must be extracted to a pure function under `n8n-functions/{js,py}/<name>.{js,py}` and paired with a test under `n8n-functions-tests/`. The Code-node body keeps only the placeholder + thin n8n glue (`$input` / `items` / `return [{json:...}]`).

`validate.py` enforces this for any `n8n-nodes-base.code` node in a template. Inlined Code-node logic is rejected. The deprecated `n8n-nodes-base.function` node type is forbidden entirely.

## Why

- **Testable**: the pure function takes plain values and returns plain values, so `node --test` (JS) or `pytest` (Py) can exercise it without an n8n runtime.
- **Re-usable**: the same function file can be referenced from multiple workflows.
- **Reviewable**: diffs show real logic changes, not whitespace inside JSON-escaped strings.
- **Round-trippable**: `js_resolver` / `py_resolver` wrap the injected content in round-trip markers (`#:js:` for JS, `MATCH:py:` for Python; legacy `DEHYDRATE:` markers also accepted on read); `resync.py` collapses those markers back to placeholders so live edits in n8n's UI never leak duplicated function bodies into templates.

## Layout

```
<workspace>/
├── n8n-functions/
│   ├── js/<camelCaseName>.js
│   └── py/<snake_case_name>.py
├── n8n-functions-tests/
│   ├── conftest.py            (scaffolded by init.py — adds n8n-functions/py to sys.path)
│   ├── <camelCaseName>.test.js
│   └── test_<snake_case_name>.py
└── n8n-workflows-template/<key>.template.json
```

Naming:
- **JS**: `camelCase` for the function name, file matches: `calculateStatsByCategory.js` ↔ `calculateStatsByCategory.test.js`.
- **Python**: `snake_case` for the function name, file matches: `calculate_stats_by_category.py` ↔ `test_calculate_stats_by_category.py`.

Test files are required and the validator errors if missing. The directory names `n8n-functions/` and `n8n-functions-tests/` are convention, not configurable.

### Path resolution

`{{@js:...}}`, `{{@py:...}}`, `{{@txt:...}}`, `{{@json:...}}`, `{{@html:...}}` placeholder paths are **relative to the workspace root** (the directory containing `n8n-config/`, `n8n-functions/`, `cloud-functions/`, …). They are NOT relative to a default `n8n-functions/js/` prefix.

So `{{@js:n8n-functions/js/aggregate.js}}` resolves to `<workspace>/n8n-functions/js/aggregate.js`. Writing `{{@js:aggregate.js}}` would look for `<workspace>/aggregate.js` — usually a mistake. The validator's `referenced file not found` error reports the full resolved path, so always include the `n8n-functions/js/` (or `n8n-functions/py/`, `n8n-prompts/`, etc.) prefix.

---

## JavaScript example

### Pure function — `n8n-functions/js/calculateStatsByCategory.js`

```js
function calculateStatsByCategory(articles) {
  const stats = {};
  for (const article of articles) {
    const cat = article.category || "uncategorized";
    stats[cat] = (stats[cat] || 0) + 1;
  }
  return stats;
}
if (typeof module !== "undefined") module.exports = { calculateStatsByCategory };
```

The `if (typeof module !== "undefined")` trailer:
- **No-op in n8n's vm sandbox** — `module` is undefined, the condition is false, the line is skipped.
- **Active under `node --test`** — `module` is defined, the function is exported, the test can `require` it.

The trailer is **mandatory**. The validator errors if it's missing.

### Code-node body (before hydrate)

`parameters.jsCode`:

```
{{@js:n8n-functions/js/calculateStatsByCategory.js}}

const body = $input.body || {};
const articles = Array.isArray(body.articles) ? body.articles : [];
const stats = calculateStatsByCategory(articles);

try {
  return { json: { stats } };
} catch(e) {
  return { error: e.message };
}
```

### Code-node body (after hydrate)

```
/* #:js:n8n-functions/js/calculateStatsByCategory.js */
function calculateStatsByCategory(articles) {
  const stats = {};
  for (const article of articles) {
    const cat = article.category || "uncategorized";
    stats[cat] = (stats[cat] || 0) + 1;
  }
  return stats;
}
if (typeof module !== "undefined") module.exports = { calculateStatsByCategory };
/* /#:js:n8n-functions/js/calculateStatsByCategory.js */

const body = $input.body || {};
const articles = Array.isArray(body.articles) ? body.articles : [];
const stats = calculateStatsByCategory(articles);

try {
  return { json: { stats } };
} catch(e) {
  return { error: e.message };
}
```

### Test — `n8n-functions-tests/calculateStatsByCategory.test.js`

```js
const { test } = require("node:test");
const assert = require("node:assert/strict");
const { calculateStatsByCategory } = require("../n8n-functions/js/calculateStatsByCategory.js");

test("groups articles by category", () => {
  const result = calculateStatsByCategory([
    { category: "sports" }, { category: "sports" }, { category: "tech" }
  ]);
  assert.deepEqual(result, { sports: 2, tech: 1 });
});
```

Pure CommonJS (`require` throughout). Don't add `package.json` `"type": "module"` — `node --test` runs these as CJS scripts.

---

## Python example

### Pure function — `n8n-functions/py/calculate_stats_by_category.py`

```python
def calculate_stats_by_category(articles):
    stats = {}
    for article in articles:
        cat = article.get("category", "uncategorized")
        stats[cat] = stats.get(cat, 0) + 1
    return stats
```

No guards, no exports — Python files are always importable as modules.

### Code-node body (before hydrate)

`parameters.pythonCode` (with `parameters.language == "python"`):

```
{{@py:n8n-functions/py/calculate_stats_by_category.py}}

body = items[0]["json"]
articles = body.get("articles", [])
stats = calculate_stats_by_category(articles)
return [{"json": {"stats": stats}}]
```

### Code-node body (after hydrate)

```
# MATCH:py:n8n-functions/py/calculate_stats_by_category.py
def calculate_stats_by_category(articles):
    stats = {}
    for article in articles:
        cat = article.get("category", "uncategorized")
        stats[cat] = stats.get(cat, 0) + 1
    return stats
# /MATCH:py:n8n-functions/py/calculate_stats_by_category.py

body = items[0]["json"]
articles = body.get("articles", [])
stats = calculate_stats_by_category(articles)
return [{"json": {"stats": stats}}]
```

### Test — `n8n-functions-tests/test_calculate_stats_by_category.py`

```python
from calculate_stats_by_category import calculate_stats_by_category

def test_groups_by_category():
    result = calculate_stats_by_category([
        {"category": "sports"}, {"category": "sports"}, {"category": "tech"}
    ])
    assert result == {"sports": 2, "tech": 1}
```

No `sys.path` manipulation here — `init.py` scaffolds `n8n-functions-tests/conftest.py` once with:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "n8n-functions" / "py"))
```

The hyphenated dir name `n8n-functions` cannot be imported as a Python package (hyphens are forbidden in module names), so pytest's `conftest.py` is where the `sys.path` insert lives.

The Python source file must **not** contain any of the substrings `# MATCH:py:`, `# /MATCH:py:`, `# DEHYDRATE:py:`, or `# /DEHYDRATE:py:` — those would corrupt the round-trip. `py_resolver.resolve()` raises `ValueError` on encounter.

---

## Structure rules

Function files must contain only function declarations + (JS only) the conditional export trailer. Top-level code is rejected at validate time.

**JavaScript** — at brace-depth 0, the only allowed line shapes are:
- Blank lines.
- Line comments (`//`) and block comments (`/* */`, including JSDoc above a function).
- `function <name>(...)` and `async function <name>(...)` declarations (with the body indented inside `{ ... }`).
- The conditional export trailer: `if (typeof module !== "undefined") module.exports = { ... };`.
- Bare `module.exports = { ... };` / `exports.<name> = ...;` lines (allowed but not required if the trailer wraps them).

Anything else at depth 0 — `const`/`let`/`var`, top-level `return`, top-level `for`/`if`/`while`, function calls, bare expressions — is a violation.

**Python** — at column 0, the only allowed line shapes are:
- Blank lines.
- Comment lines (`#`).
- A module-level docstring (a triple-quoted string as the first non-blank, non-comment line). Python convention; allowed.
- `import ...` and `from ... import ...`.
- `def <name>(...)` and `async def <name>(...)` (with the body indented).

Anything else at column 0 — assignments, `for`/`if`/`while` blocks, top-level function calls, bare strings *anywhere else* in the file — is a violation.

The error message includes the offending line number and an excerpt:

```
node 'Code': n8n-functions/js/aggregate.js contains top-level code outside function declarations
(line 1: 'const articles = items[0].json.body || [];'). Pure-function files must declare functions
only — n8n-glue belongs in the Code-node body, not the file.
```

The structural check makes "pure functions only" enforceable, not aspirational. An agent who tries to satisfy the trailer + test rules by pasting the n8n-glue into the function file will fail this check on the first non-`function` line.

---

## Validator checks (template only)

`validate.py` runs these against every `n8n-nodes-base.code` node in a template. All checks are **errors**, no warnings. Built JSON skips these checks (placeholders are already replaced post-hydrate).

| Rule | Error |
|---|---|
| Node type is `n8n-nodes-base.function` | Deprecated; switch to `n8n-nodes-base.code`. |
| `jsCode` (or `pythonCode` when `language == "python"`) is empty | Cannot validate without code. |
| No `{{@js:...}}` (or `{{@py:...}}`) placeholder in the code field | Inlined logic is rejected — extract to `n8n-functions/{js,py}/`. |
| Placeholder points to a file that doesn't exist | Bad path — fix or remove. |
| JS file is missing `if (typeof module !== "undefined")` trailer | Tests cannot `require` the function. |
| Function file contains top-level code outside function declarations | The file must be a pure-function library; n8n-glue belongs in the Code-node body. See **Structure rules** above. |
| No paired test file at `n8n-functions-tests/<stem>.test.js` (JS) or `test_<stem>.py` (Py) | Pure function ships untested. |

There is **no opt-out** for trivial Code nodes.

## Running the tests

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/test_functions.py --target n8n
```

Runs both `node --test` (over `*.test.js`) and `pytest` (over `test_*.py`) under `n8n-functions-tests/`.

`pytest` must be available — `pip install pytest` if it isn't. The runner reports the failure cleanly via subprocess exit code.

---

## Primitive exemption

Harness-maintained primitive Code nodes (lock acquisition, lock release, rate-limit check, error-handler cleanup) begin their body with `// @n8n-evol-I:primitive`. This marker suppresses the placeholder and purity checks in `validate.py` — the validator's `_validate_code_node` short-circuits with no errors as soon as it sees the marker as the first non-whitespace characters of the code field.

Only primitives under `primitives/workflows/` should use this marker. User Code nodes must follow the discipline rule without exception; using the marker in a user workflow will silently bypass validation, defeating the whole point of the rule.

The marker exists because the primitive bodies legitimately use `this.helpers.redis` and have top-level statements (SETNX with TTL, INCR + EXPIRE, owner-pointer writes) — they're not pure functions and can't be written as such without losing atomicity. The marker is the explicit, narrow opt-out for this case.
