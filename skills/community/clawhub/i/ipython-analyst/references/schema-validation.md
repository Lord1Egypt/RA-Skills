# Schema Validation Reference

Validate data against schemas, generate edge-case tests, verify chunking, diff outputs. **Load this reference when the user wants to validate JSON/CSV, fuzz a parser, verify text-chunking integrity, or compare two outputs for regressions.**

## Schema Validation

### Basic schema
```python
import sys
SCRIPTS = '/home/z/my-project/skills/ipython-analyst/scripts'
if SCRIPTS not in sys.path: sys.path.insert(0, SCRIPTS)
from chunking_validator import ChunkingValidator, validate_chunking
from output_differ import OutputDiffer, BaselineManager, compare_outputs
from schema_validator import SchemaValidator, SchemaField, validate_schema
from test_generator import TestCaseGenerator, TestCase, TestResult, generate_tests

schema = {
    'name':  SchemaField(type=str, required=True, description='User name'),
    'age':   SchemaField(type=int, min_value=0, max_value=150),
    'email': SchemaField(type=str, pattern=r'^[\w.]+@[\w.]+\.\w+$'),
    'role':  SchemaField(type=str, enum=['admin', 'user', 'guest']),
    'tags':  SchemaField(type=list, required=False),
}

result = validate_schema({'name': 'Alice', 'age': 30, 'email': 'a@b.com', 'role': 'admin'}, schema)
print(result['valid'])  # True
print(result['errors'])  # []
```

### Nested schemas
Mix `SchemaField` (leaf) with `dict` (recurse):

```python
schema = {
    'user': {  # nested object
        'name': SchemaField(type=str, required=True),
        'age':  SchemaField(type=int, min_value=0),
    },
    'orders': [SchemaField(type=dict)],  # list of dicts (each validated against orders_item)
    # Note: list-element schemas are simplified — use a custom validator for full per-element checks
}
```

### Strict mode
In strict mode, unknown keys are errors (default: warnings ignored):

```python
strict_validator = SchemaValidator(schema, strict=True)
result = strict_validator.validate({'name': 'Alice', 'age': 30, 'extra': 'unknown'})
# 'extra' is an error in strict mode
```

### Tuple types (any-of)
`SchemaField(type=(int, str))` accepts either int or str. Useful for IDs that can be numeric or string.

```python
schema = {'id': SchemaField(type=(int, str), required=True)}
validate_schema({'id': 42}, schema)   # valid
validate_schema({'id': 'abc'}, schema)  # valid
validate_schema({'id': 1.5}, schema)   # invalid (float not in tuple)
```

## Test Case Generation

### Edge-case fuzzing
```python

# Generate 50 adversarial inputs
cases = generate_tests(count=50)
for case in cases[:5]:
    print(f"{case.category:12s} {case.name}: {case.input_data!r}")
```

Categories: `empty`, `whitespace`, `unicode`, `control`, `special` (None/null/NaN/script tags), `boundary` (long strings), `injection` (SQL/XSS/path traversal).

### Stress test a parser
```python
def my_json_parser(s):
    return json.loads(s)  # raises on invalid input

gen = TestCaseGenerator()
cases = gen.generate(count=100)
result = gen.stress_test(my_json_parser, cases, timeout=1.0)
print(f"Passed: {result.passed}, Failed: {result.failed}, Timeouts: {result.timeouts}")
print(f"By category: {result.by_category}")
```

A timeout indicates catastrophic backtracking in your parser (regex-based parsers are especially vulnerable).

### Targeted tests from a regex pattern
```python
gen = TestCaseGenerator(source_code=open('parser.py').read())
# gen.patterns now contains all re.compile patterns from the source
for pattern in gen.patterns:
    print(f"Pattern: {pattern}")
    cases = gen.generate_targeted(pattern, count=20)
    # Run your parser against these cases
```

## Chunking Validation

When you split a long document into chunks (for RAG, batched LLM calls, parallel processing), verify nothing was lost.

```python

original = open('/home/z/my-project/upload/long_doc.md').read()
chunks = my_chunker(original, chunk_size=2000)
chunks = [{'content': c} for c in chunks]  # validator expects list of dicts

result = validate_chunking(original, chunks)
print(result['valid'])  # True if no hard errors
for issue in result['issues']:
    print(f"  [{issue['severity']}] chunk {issue['chunk']}: {issue['type']} — {issue['desc']}")
```

Checks performed:
- **Structural per chunk**: code fences balanced, no truncated markdown headers
- **Length preservation**: reassembled length matches original
- **Content preservation**: URLs, emails, code blocks, headers, list items, UUIDs all survived
- **Order preservation**: sampled substrings appear in same relative order

## Output Diffing (Regression Testing)

### Compare two values
```python

old = {'users': [{'id': 1, 'name': 'Alice'}], 'total': 1}
new = {'users': [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}], 'total': 2, 'page': 1}

d = OutputDiffer()
d.compare(old, new)
for diff in d.diffs:
    print(f"  {diff.diff_type:15s} at {diff.path}: {diff.old_value!r} → {diff.new_value!r}")
print(d.get_summary())
# {'total_diffs': 4, 'semantic_diffs': 4, 'by_type': {'added': 1, 'changed': 2, 'length_change': 1}}
```

### Numeric tolerance
```python
d = OutputDiffer(numeric_tolerance=0.01)  # ignore changes < 0.01
d.compare({'pi': 3.14159}, {'pi': 3.14160})  # no diff reported
```

### Ignore order in lists
```python
d = OutputDiffer(ignore_order=True)
d.compare({'items': [1, 2, 3]}, {'items': [3, 2, 1]})  # no diff
```

### Skip specific keys (e.g., timestamps)
```python
d = OutputDiffer(ignore_keys={'updated_at', 'etag'})
```

## Baseline Management

Capture a baseline before refactoring, then verify your changes didn't introduce regressions.

```python
bm = BaselineManager()

# Before refactoring
bm.save_baseline('process_output_v1', process(data))

# After refactoring
result = bm.compare_with_baseline('process_output_v1', new_process(data))
if result['status'] == 'match':
    print("No regressions!")
else:
    print(f"Regressions: {result['summary']}")
    for diff in result['diffs']:
        print(f"  {diff['path']}: {diff['old']} → {diff['new']}")
```

Baselines are stored as JSON in `/home/z/my-project/download/.baselines/`.

## Workflow: Validate a New API Endpoint

1. Define the response schema with `SchemaField`.
2. Hit the endpoint, parse JSON.
3. `validate_schema(response, schema)` — fix any hard errors.
4. Generate test cases with `TestCaseGenerator` and stress-test the endpoint.
5. Save a baseline with `BaselineManager.save_baseline`.
6. After any code change, `compare_with_baseline` to detect regressions.
