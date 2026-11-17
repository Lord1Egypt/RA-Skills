---
name: ipython-analyst
description: 'Run Python interactively to analyze data, debug code, profile performance, validate schemas, process large files, and inspect ASTs. Use this whenever the user needs hands-on Python execution — debugging a script, profiling slow code, regex stress-testing, parsing CSV/Excel/JSON, building ML baselines, analyzing logs, validating schemas, diffing outputs between code versions, visualizing ASTs, detecting file formats, or running distributed/parallel jobs. Strong triggers include phrases like "debug this script", "profile my function", "this regex hangs on", "validate this JSON against a schema", "diff the output of these two versions", "what format is this file", "parse this log", "find the bottleneck", "stress test this parser", or any request to execute Python code interactively to investigate a concrete problem. Prefer this over the charts skill when the deliverable is a diagnostic answer (a fix, a profile, a validation report) rather than a polished chart; prefer docx/xlsx/pdf skills when the user wants a written document or spreadsheet as the final artifact.'
---

# IPython Analyst v7

Execute Python interactively for data analysis, code debugging, profiling, and scientific computing. Variables, imports, models, and figures persist across calls within the same session — build up state incrementally instead of re-running everything from scratch.

## File Paths

| Path | Purpose |
|------|---------|
| `/home/z/my-project/upload/` | User uploaded files (read) |
| `/home/z/my-project/download/` | Generated outputs (write — only place the user can download from) |

## Workflow

1. **Classify the task** using the decision tree below. Pick the right reference file and script.
2. **Read the matching reference** (one file, not all of them) for domain-specific patterns and pitfalls.
3. **Execute code via the ipython tool.** Variables persist — reuse them. Save long-running setup (data loads, model fits) once.
4. **For non-trivial utilities, import from `scripts/`** rather than re-typing the class. Each script is self-contained, tested, and imports cleanly. Add the scripts directory to `sys.path` once per session, then use normal imports:

   ```python
   import sys
   SCRIPTS = '/home/z/my-project/skills/ipython-analyst/scripts'
   if SCRIPTS not in sys.path: sys.path.insert(0, SCRIPTS)

   # Then import as normal modules — no exec(), no open().read()
   from safe_execution import timeout_context, OperationTimeout
   from debug_utils import summarize_exception, post_mortem
   from code_analyzer import CodeAnalyzer, analyze_script
   ```

   This is safer than `exec(open(...).read())` because Python's import machinery validates the file is a proper module, caches it, and won't re-execute on subsequent imports. The scripts directory contains only skill-owned helper code; do not add untrusted paths to `sys.path`.
5. **Save final outputs** to `/home/z/my-project/download/` with descriptive filenames. Use the user's language for any labels or text in outputs.
6. **Present results** with a brief explanation and the download path. Don't dump 500 lines of repr — summarize.

## Decision Tree — Pick Your Reference

Read **only** the reference file that matches the task. Loading all of them wastes context.

| User wants… | Read this reference | Use these scripts |
|-------------|---------------------|-------------------|
| Debug a script (pdb, post-mortem, tracebacks, exceptions) | `references/debugging.md` | `scripts/debug_utils.py`, `scripts/safe_execution.py` |
| Profile slow code (CPU, memory, line-by-line) | `references/debugging.md` § Profiling | `scripts/profiler.py` |
| Analyze CSV/Excel/JSON, build a chart, compute stats | `references/data-analysis.md` | (uses pandas/numpy/seaborn inline) |
| Build ML baseline (classify/regress/cluster) | `references/machine-learning.md` | (uses sklearn inline) |
| Analyze a graph (centrality, communities, paths) | `references/network-analysis.md` | (uses networkx inline) |
| Static code analysis (complexity, smells, AST) | `references/code-analysis.md` | `scripts/code_analyzer.py`, `scripts/dependency_analyzer.py`, `scripts/parse_tree.py` |
| Debug a regex (risks, stress test, catastrophic backtracking) | `references/code-analysis.md` § Regex | `scripts/regex_debugger.py` |
| Run a function with mocked deps (filesystem, modules, env) | `references/code-analysis.md` § Isolation | `scripts/function_isolator.py` |
| Validate JSON/CSV against a schema | `references/schema-validation.md` | `scripts/schema_validator.py` |
| Generate edge-case tests for a parser | `references/schema-validation.md` § Test Gen | `scripts/test_generator.py` |
| Validate text chunking preserves data | `references/schema-validation.md` § Chunking | `scripts/chunking_validator.py` |
| Diff two outputs (regression testing, baseline compare) | `references/schema-validation.md` § Differ | `scripts/output_differ.py` |
| Parse and summarize log files | `references/environment.md` § Logs | `scripts/log_analyzer.py` |
| Detect format of an unknown file/content | `references/environment.md` § Format | `scripts/format_detector.py` |
| Verify installed packages / extract imports from a script | `references/environment.md` § Env | `scripts/env_check.py` |
| Process large CSV without OOM (chunked, streaming) | `references/distributed.md` | `scripts/distributed.py` |
| Parallel map / Dask cluster / parallel groupby | `references/distributed.md` | `scripts/distributed.py` |
| Track session memory, compress dormant variables | `references/environment.md` § Session | `scripts/session_manager.py` |

If multiple rows match, read the most specific one first (e.g., for "profile my regex", read `code-analysis.md` § Regex first, then `debugging.md` § Profiling if you need broader profiling context).

## Available Libraries (verified in this environment)

| Category | Libraries |
|----------|-----------|
| Data | pandas, numpy, dask (optional) |
| Visualization | matplotlib, seaborn, plotly |
| Statistics | scipy.stats, statsmodels |
| Optimization | scipy.optimize, PuLP |
| Symbolic | sympy, mpmath |
| ML | scikit-learn, torch (CPU) |
| Networks | networkx |
| Images | PIL, opencv |
| Code analysis | ast, dis, inspect, tokenize |
| Profiling | cProfile, pstats, tracemalloc |
| Testing | unittest, pytest |
| Compression | zlib, gzip, pickle, joblib |
| Distributed | multiprocessing, concurrent.futures, dask |
| Progress | tqdm (optional) |

Target **Python 3.11+**. Use modern features where they help: `X | Y` type unions, `match`/`case`, `ExceptionGroup`/`TaskGroup` for concurrent fan-out, `tomllib` for TOML parsing, fine-grained error locations in tracebacks.

## Core Principles

### 1. Persist state, don't redo work
The ipython tool keeps variables across calls. Use this — load data once, then run multiple analyses on `df` without re-reading the file. Same for trained models, parsed ASTs, compiled regexes. Re-running 30 seconds of setup because you forgot to reuse `df` is a real cost.

### 2. Reach for scripts/ before rewriting
Each script in `scripts/` is the polished version of a utility — bugs fixed, edge cases handled, tested. If you need a `RegexDebugger`, `CodeAnalyzer`, `SchemaValidator`, etc., load the script. Only hand-roll when the script genuinely doesn't fit (and if it's a recurring need, add it to the script).

### 3. Timeouts on unbounded work
Any regex match, parser run, or external call that *might* hang needs a timeout. Use `safe_execution.timeout_context(seconds)` (SIGALRM-based, interrupts blocking C code). This is mandatory for regex stress tests — catastrophic backtracking will otherwise lock the session.

### 4. Memory matters for big data
For files >500MB or DataFrames >2GB: stream with `distributed.process_large_file(output_path=...)` (writes chunks to disk, never accumulates in memory), or use `DaskProcessor` as a context manager (`with DaskProcessor() as dp: ...` — closes the cluster, prevents zombie processes).

### 5. Charts → use the `charts` skill
This skill produces diagnostic figures (a quick scatter to see a distribution, a profile plot). For publication-quality charts, dashboards, mind maps, or any deliverable where the chart *is* the final artifact, use the dedicated `charts` skill instead — it has proper layout engines, color systems, and per-chart-type recipes.

### 6. Don't shadow builtins
A common v6 bug was `class TimeoutError(Exception)` which shadowed the builtin `TimeoutError` and silently broke code that caught the builtin. v7 uses a distinct name (`OperationTimeout`) — preserve this.

## Scripts Index

All scripts live at `/home/z/my-project/skills/ipython-analyst/scripts/`. Each is self-contained. To use them, add the directory to `sys.path` once, then import normally:

```python
import sys
SCRIPTS = '/home/z/my-project/skills/ipython-analyst/scripts'
if SCRIPTS not in sys.path: sys.path.insert(0, SCRIPTS)
# Now: from debug_utils import post_mortem, summarize_exception
```

| Script | What it gives you |
|--------|-------------------|
| `safe_execution.py` | `resource_limits`, `timeout_context`, `OperationTimeout`, `safe_eval` |
| `session_manager.py` | `SessionManager`, `VariableInfo`, `memory_report` |
| `debug_utils.py` | `post_mortem`, `format_exception`, `extract_traceback`, `summarize_exception`, `breakpoint_helper` |
| `code_analyzer.py` | `CodeAnalyzer`, `FunctionMetrics`, `ClassMetrics`, `analyze_script` |
| `dependency_analyzer.py` | `DependencyAnalyzer`, `analyze_dependencies` |
| `regex_debugger.py` | `RegexDebugger`, `debug_regex` |
| `function_isolator.py` | `FunctionIsolator` (mock modules, files, env) |
| `profiler.py` | `Profiler`, `profile` decorator (memory + CPU) |
| `schema_validator.py` | `SchemaValidator`, `SchemaField`, `validate_schema` |
| `test_generator.py` | `TestCaseGenerator`, `TestCase`, `generate_tests` |
| `chunking_validator.py` | `ChunkingValidator`, `validate_chunking` |
| `log_analyzer.py` | `LogAnalyzer`, `analyze_logs` |
| `output_differ.py` | `OutputDiffer`, `BaselineManager`, `compare_outputs` |
| `parse_tree.py` | `ParseTreeVisualizer`, `visualize_ast` (DOT/SVG/PNG) |
| `format_detector.py` | `FormatDetector`, `detect_format` |
| `distributed.py` | `DistributedProcessor`, `DaskProcessor`, `parallel_apply`, `process_large_csv` |
| `env_check.py` | `check_requirements`, `verify_environment`, `_extract_imports` |

## Quick Recipes

> **Setup for all recipes**: Add scripts to `sys.path` first:
> ```python
> import sys
> SCRIPTS = '/home/z/my-project/skills/ipython-analyst/scripts'
> if SCRIPTS not in sys.path: sys.path.insert(0, SCRIPTS)
> ```

### Debug a script that just crashed
```python
from debug_utils import post_mortem, summarize_exception, format_exception
# Drop into post-mortem on the last uncaught exception:
post_mortem()  # opens pdb at the failing frame
# Or summarize without entering pdb:
summary = summarize_exception(exc)  # returns dict with type, message, frames, locals
```

### Profile a slow function
```python
from profiler import Profiler
result = Profiler().profile_both(my_func, *args)  # CPU + memory in one pass
print(result['cpu']['stats'][:2000])  # top 20 by cumtime
print(f"Peak: {result['memory']['peak_mb']:.1f} MB")
```

### Stress-test a regex for catastrophic backtracking
```python
from regex_debugger import RegexDebugger
db = RegexDebugger(r'^(a+)+$')
print(db.detect_risks())      # [{'type': 'nested_quantifier', ...}]
print(db.stress_test(0.5))    # {'passed': 4, 'timeouts': 2, 'errors': 0}
```

### Validate JSON against a schema
```python
from schema_validator import SchemaField, validate_schema
schema = {
    'name': SchemaField(type=str, required=True),
    'age':  SchemaField(type=int, min_value=0, max_value=150),
    'email': SchemaField(type=str, pattern=r'^[\w.]+@[\w.]+$'),
}
result = validate_schema(data, schema)
print(result['errors'])
```

### Process a large CSV in chunks (no OOM)
```python
from distributed import process_large_csv
def agg(chunk): return chunk.groupby('product')['revenue'].sum()
result = process_large_csv(
    '/home/z/my-project/upload/sales.csv',
    process_func=agg, chunk_size=50_000,
    output_path='/home/z/my-project/download/agg_by_product.csv',
    show_progress=True,
)
```

### Detect file format (with debug)
```python
from format_detector import detect_format
with open('/home/z/my-project/upload/mystery.txt') as f: content = f.read()
fmt = detect_format(content, debug=True)
```

## Output Guidelines

- **Charts**: PNG, dpi=150–200. Prefer `constrained_layout=True` on `plt.subplots()` — do NOT combine it with `tight_layout()` or `bbox_inches='tight'` (they conflict and silently break margins). For legends, use `bbox_to_anchor` outside the plot area, not `loc='best'`.
- **Data**: CSV with `index=False`; JSON for nested structures; joblib for ML models.
- **Language**: Match the user's language for every text element (titles, labels, legends, captions). If you must deviate, explain why once.
- **Naming**: Descriptive filenames — `revenue_by_product_q4.png` not `chart1.png`.
- **Reproducibility**: Set seeds (`np.random.seed(42)`, `random_state=42`) for any ML or stochastic work.

## What NOT to Use This Skill For

- **Polished charts/dashboards** → use the `charts` skill (proper layout engines, palettes, per-type recipes).
- **Word/PDF/Excel deliverables** → use `docx`/`pdf`/`xlsx` skills.
- **Building a Next.js web app** → use `fullstack-dev` skill.
- **One-shot "write me a fib function"** → just answer; don't invoke the skill.
- **Image generation / VLM / TTS** → use those specific media skills.

## Bug Fixes Since v6

For reviewers familiar with v6, here's what changed. These were all real bugs found in v6's utilities; the v7 scripts have them fixed.

1. `verify_environment` now passes correct import names (`'PIL'` not `'pil'`, `'cv2'` stays `'cv2'`) — v6 lowercased names so the check always reported Pillow/OpenCV as missing.
2. `OperationTimeout` replaces the v6 `class TimeoutError(Exception)` that shadowed the builtin and broke `except TimeoutError:` callers.
3. `FormatDetector._score_format` now scores `weight` for the first match (was `weight * 0.5`); additional matches still add diminishing amounts, capped at `weight`.
4. `SchemaValidator._validate_field` removed the redundant ternary — `isinstance(value, field.type)` works for both single types and tuples.
5. `DistributedProcessor.process_large_file` no longer pre-reads the whole file just to count rows for the progress bar. It estimates from file size or counts chunks as they arrive.
6. `CodeAnalyzer._analyze_function` now counts `except` handlers, comprehensions, ternaries, boolean operators, and `match/case` as branches. v6 only counted `If`/`For`/`While` and missed `ast.ExceptHandler` (a 2-except-handler function was reported as complexity 1), `ast.ListComp`/`SetComp`/`DictComp`/`GeneratorExp`, `ast.IfExp` (ternary), `ast.BoolOp` (`and`/`or` short-circuits), and `ast.Match`.
7. `resource_limits` saves and restores the original soft limit (was resetting to `RLIM_INFINITY` which silently fails when the hard limit is lower, and could leave the process with the wrong limit).
8. `SessionManager._get_object_size` returns `0` on error (not `-1`) so `list_variables` totals aren't distorted by failure.
9. `DependencyAnalyzer` and `env_check._extract_imports` use `node.names` (correct) instead of `node.aliases` (doesn't exist on `ast.Import`/`ast.ImportFrom` — v6 always raised `AttributeError` on any script with imports).

## Security Hardening (post-v7.0 audit)

After publishing v7.0, a ClawHub security audit flagged 8 findings. I verified each against the actual code and confirmed 7 of them (1 was a false positive — the auditor misread a reference-file header as a skill-level activation trigger). The confirmed issues are fixed in v7.1:

10. **`safe_eval` no longer uses `eval()`** (was AST2 / HIGH). Replaced with an AST-walking evaluator that whitelists node types (literals, arithmetic/comparison/boolean operators, calls to whitelisted functions) and rejects attribute access, subscripting, comprehensions, and lambdas — closing the `().__class__.__subclasses__()` escape path. `allowed_names` now validates that injected values are scalars or callables only (no modules, no dunder-named keys).
11. **`exec(open(...).read())` removed from all code examples** (was LP3 + SQP-2). Replaced with `sys.path.insert(0, SCRIPTS); from <name> import <symbol>` — Python's import machinery validates the file is a proper module, caches it, and won't re-execute on subsequent imports. All 28 occurrences across SKILL.md + 5 reference files updated.
12. **`test_generator.stress_test` correctly tracks pass/fail** (was SDI-4). The v7.0 implementation never incremented `failed`, and treated both "parser raised" and "parser accepted" as `passed` — silently producing misleading results. The new implementation takes `should_accept` / `should_reject` predicates per case, classifies each case's expected outcome, and increments `failed` when the parser does the opposite of expected. Timeouts are always counted as failures.
13. **`debug_utils.extract_traceback` / `format_exception` / `summarize_exception` default to no locals** (was SQP-2 × 2). Locals may contain credentials, PII, tokens, or other sensitive runtime state. The default is now `include_locals=False` / `show_locals=False`; pass `True` explicitly for interactive debugging only. `summarize_exception` gained an `include_locals` parameter (was hardcoded to `True`).
14. **`references/debugging.md` warns about sensitive data in failing inputs** (was SQP-2). The "save failing input to disk" guidance now says: treat the input as potentially sensitive, prefer in-memory repros, redact or synthesize before saving, ask the user for approval before persisting real inputs. Added a new "Sensitive Data in Debugging Output" section documenting the locals-exposure trade-off across all three `debug_utils` helpers.

## Best Practices

- **Memory**: Use `SessionManager` for accurate memory tracking. DataFrame sizes use `memory_usage(deep=True)`; numpy arrays use `nbytes`.
- **Timeout**: Wrap any regex/parser/IO call that *might* block in `timeout_context`. Catastrophic backtracking will hang the session otherwise.
- **Large files**: `process_large_csv(output_path=...)` streams to disk. `parallel_map` for CPU-bound fan-out. `DaskProcessor` as a `with` block for lazy evaluation on big data.
- **Profiling**: For performance-critical code, always profile both CPU and memory — they often tell different stories. A function that's fast but allocates 5GB will OOM at scale.
- **Reproducibility**: Set seeds for any stochastic operation. Pin `random_state=42` in sklearn, `torch.manual_seed(42)` in torch.
- **Untrusted code**: Use `check_requirements(script_path)` to see what a script imports before running it. Use `safe_eval` for user-supplied expressions (it restricts builtins and only exposes `math`).
