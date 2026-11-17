# Code Analysis Reference

Static code analysis, regex debugging, AST visualization, and dependency graphs. **Load this reference when the user wants to understand code structure, find complexity hotspots, debug regexes, or visualize ASTs.**

## Static Code Analysis

### Find complexity hotspots
```python
import sys
SCRIPTS = '/home/z/my-project/skills/ipython-analyst/scripts'
if SCRIPTS not in sys.path: sys.path.insert(0, SCRIPTS)
from code_analyzer import CodeAnalyzer, FunctionMetrics, ClassMetrics, analyze_script
from dependency_analyzer import DependencyAnalyzer, analyze_dependencies
from function_isolator import FunctionIsolator
from parse_tree import ParseTreeVisualizer, visualize_ast
from regex_debugger import RegexDebugger, debug_regex

result = analyze_script('/home/z/my-project/upload/mystery.py')
print(result["summary"])
# {'loc': 245, 'classes': 3, 'functions': 18, 'regex_patterns': 2,
#  'avg_complexity': 4.2, 'issues': 5, 'top_complex': [('process_data', 14), ...]}

for issue in result["issues"]:
    if issue["severity"] == "warning":
        print(f"  {issue['location']}: {issue['message']}")
```

The v7 complexity counter correctly handles:
- `if/elif/else` chains (each `elif` adds a branch — v6 undercounted these)
- `try/except` (each `except` clause is a branch)
- `with` and `for`/`while` (each adds a branch)
- Comprehensions and generator expressions
- Ternary expressions (`x if cond else y`)
- Boolean operators (`a and b` adds a branch for short-circuit)
- `match/case` (each case is a branch — Python 3.10+)

### Extract dependency graph
```python

result = analyze_dependencies('/home/z/my-project/upload/script.py')
print("Imports:", result["imports"])
print("Classes:", result["classes"])
print("Entry points:", result["entry_points"])  # functions defined but never called
print("Orphans:", result["orphans"])  # functions called but not defined (externals)
print("Call graph:", result["call_graph"])

# Export as Graphviz DOT
from dependency_analyzer import DependencyAnalyzer
d = DependencyAnalyzer(open('/home/z/my-project/upload/script.py').read())
d.export_dot('/home/z/my-project/download/call_graph.dot')
# Render with: dot -Tsvg call_graph.dot -o call_graph.svg
```

### Visualize AST
```python

source = "def foo(x, y):\n    if x > y:\n        return x\n    return y\n"
visualize_ast(source, '/home/z/my-project/download/ast.svg', format='svg')
# Falls back to DOT if graphviz not installed
```

Color coding: functions blue, classes green, variables orange, literals cyan, control-flow red.

## Regex Debugging

### Diagnose a hanging regex
Catastrophic backtracking happens when the regex engine has to explore exponential paths. Classic triggers: `(a+)+`, `(a|a)*`, `(.*)*`. The engine appears to "hang" — it's actually running, just very slowly.

```python

db = RegexDebugger(r'^(a+)+$')
risks = db.detect_risks()
# [{'type': 'nested_quantifier', 'severity': 'high',
#   'message': 'Nested quantifiers like (a+)+ cause exponential backtracking'}]

result = db.stress_test(timeout=0.5)
# {'passed': 4, 'timeouts': 5, 'errors': 0, 'details': [...]}
```

### Common fixes for backtracking
- **Nested quantifiers** `(a+)+` → use possessive quantifier `(a++)` or atomic group `(?>a+)`
- **Greedy `.*`** → use lazy `.*?` or specific char class `[^"]*`
- **Quantified alternation** `(a|b)*` → factor out: `a*|b*` if order doesn't matter
- **Unbounded quantifier on group** `(group)*` → bound it: `(group){0,10}` if you can

### Static regex risk check (no execution)
```python
result = debug_regex(r'(a+)+')
# {'pattern': '(a+)+', 'valid': True, 'error': None,
#  'risks': [{'type': 'nested_quantifier', 'severity': 'high', ...}]}
```

### Find all `re.compile` calls in a script
```python
from code_analyzer import CodeAnalyzer
a = CodeAnalyzer(open('script.py').read())
print(a.regex_patterns)
# [{'pattern': r'\d{3}-\d{4}', 'lineno': 42}, ...]
```

## Function Isolation (Mocking)

When debugging a function whose dependencies are unavailable, mock them.

```python

iso = FunctionIsolator()
iso.mock_module("requests.get", return_value=MagicMock(status_code=200, json=lambda: {"ok": True}))
iso.mock_file("/etc/config.json", '{"timeout": 30}')
iso.mock_env({"DEBUG": "1", "API_KEY": "test"})

result = iso.run(my_function, arg1, arg2)
print(result["result"])  # what the function returned
print(result["error"])   # exception object if it raised
```

## Common Code Smells and Their Fixes

### High cyclomatic complexity (>10)
A function with too many branches is hard to test and reason about. **Fix**: extract branch groups into helper functions, or replace if/elif chains with a dispatch dict.

```python
# Before: complexity 8
def process(x):
    if x == 'a': return 1
    elif x == 'b': return 2
    elif x == 'c': return 3
    elif x == 'd': return 4
    elif x == 'e': return 5
    elif x == 'f': return 6
    elif x == 'g': return 7
    else: return 0

# After: complexity 1
PROCESSORS = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7}
def process(x):
    return PROCESSORS.get(x, 0)
```

### Deep nesting (>4)
Nested loops/ifs are hard to read and modify. **Fix**: guard clauses — return early on the negative case.

```python
# Before: nesting 4
def process(user):
    if user:
        if user.is_active:
            if user.has_permission:
                if user.data:
                    return process_data(user.data)
    return None

# After: nesting 1
def process(user):
    if not user: return None
    if not user.is_active: return None
    if not user.has_permission: return None
    if not user.data: return None
    return process_data(user.data)
```

### Too many parameters (>5)
A function with many params is hard to call correctly. **Fix**: group related params into a dataclass.

```python
@dataclass
class QueryConfig:
    table: str
    columns: list[str]
    filters: dict
    order_by: str | None = None
    limit: int | None = None

def query(config: QueryConfig) -> list:
    ...
```

## Workflow: Code Review Pass

1. Run `analyze_script(path)` for a summary.
2. For each `warning`-severity issue, look at the function.
3. If complexity > 15, it's a refactoring candidate.
4. If nesting > 5, it's a bug-prone function — recommend guard clauses.
5. If params > 7, recommend grouping into a dataclass.
6. Cross-check with `analyze_dependencies(path)` to find orphaned functions (dead code).
7. If the script uses regexes, run `debug_regex` on each pattern from `regex_patterns`.
