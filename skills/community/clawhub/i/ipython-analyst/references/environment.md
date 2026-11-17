# Environment & Session Reference

Verify installed packages, parse logs, detect file formats, manage session memory. **Load this reference when the user wants to know what's installed, parse log files, identify an unknown file format, or track IPython session memory.**

## Environment Checks

### Verify packages are installed
```python
import sys
SCRIPTS = '/home/z/my-project/skills/ipython-analyst/scripts'
if SCRIPTS not in sys.path: sys.path.insert(0, SCRIPTS)
from env_check import check_requirements, verify_environment
from format_detector import FormatDetector, detect_format
from log_analyzer import LogAnalyzer, analyze_logs
from session_manager import SessionManager, VariableInfo, memory_report

# Check common data science packages
result = verify_environment(verbose=True)
# pandas: ok
# numpy: ok
# PIL: ok
# cv2: ok  (v6 falsely reported missing)
# ...

print(result['status'])  # 'ok' or 'issues'
print(result['missing'])  # list of missing packages
```

### Check imports in a script
```python
# Extract all imports from a script, check what's missing
result = check_requirements(script_path='/home/z/my-project/upload/mystery.py', verbose=True)
print(f"Missing: {result['missing']}")
```

### Check specific packages with version specs
```python
result = check_requirements(requirements={
    'pandas': '>=2.0',
    'numpy':  '>=1.24',
    'scikit-learn': '>=1.3',  # PyPI name — auto-mapped to 'sklearn' for import
    'PIL':    None,            # import name — checked directly
    'cv2':    None,            # import name — checked directly
})
for r in result['details']:
    print(f"  {r.name}: {r.status} ({r.version})")
```

### PyPI name vs import name
Common mismatches handled by `env_check.py`:

| PyPI distribution | Import name |
|-------------------|-------------|
| pillow | PIL |
| opencv-python | cv2 |
| scikit-learn | sklearn |
| pyyaml | yaml |
| beautifulsoup4 | bs4 |
| python-dateutil | dateutil |
| python-dotenv | dotenv |

v6 lowercased all names so `'PIL'` became `'pil'` (not a real module) — the check always failed for Pillow. v7 uses the explicit mapping table.

## Log Analysis

### Load and summarize
```python

summary = analyze_logs('/home/z/my-project/upload/app.log')
print(summary)
# {'total': 12453, 'unparsed': 12, 'by_level': {'INFO': 11000, 'WARNING': 1200, 'ERROR': 253},
#  'errors': 253, 'top_error_patterns': [...], 'time_range': {'start': '...', 'end': '...'}}
```

### Supported log formats
- Python logging: `2026-01-15 10:30:45,123 - myapp - INFO - message`
- Standard: `2026-01-15 10:30:45 INFO message`
- Syslog: `Jan 15 10:30:45 host myapp: message`
- JSON-lines: `{"timestamp": "...", "level": "ERROR", "message": "..."}`

For custom formats, subclass `LogAnalyzer` and override `_parse()`.

### Drill into errors
```python
a = LogAnalyzer()
a.load('/home/z/my-project/upload/app.log')

# All errors
for entry in a.get_errors()[:10]:
    print(f"{entry['timestamp']} [{entry['level']}] {entry['message']}")

# Most common error patterns (numbers normalized to #)
for pattern, count in a.error_patterns(10):
    print(f"  {count:5d}  {pattern[:100]}")

# Filter by time window
recent_errors = a.time_window(start='2026-01-15 10:00', end='2026-01-15 11:00')
```

## Format Detection

When you have a file with no extension (or wrong extension), detect its format heuristically.

```python

with open('/home/z/my-project/upload/mystery_file') as f:
    content = f.read()

fmt = detect_format(content, debug=True)
# === Format Detection: json (high) ===
#   json         1.10  ['+0.80: Object structure (single root) (1 match)', '+0.30: JSON key pattern (12 matches)']
#   ...
```

Supported formats: JSON, XML, HTML, CSV, YAML, Markdown, Python, SQL, TOML, INI, log.

### Scoring
Each format has positive indicators (raise score) and counter-indicators (lower score). The first match of an indicator adds the full weight; subsequent matches add diminishing amounts. Format with the highest score wins; below threshold → 'unknown'.

## Session Memory Management

### Check what's eating memory
```python

sm = SessionManager()
for v in sm.list_variables()[:10]:
    print(f"  {v.size_bytes / 1024 / 1024:8.2f}MB  {v.type_name:15s}  {v.name}")
```

### Compress dormant variables
If you have a big intermediate you might need again but don't need right now:

```python
sm.compress_variable('big_intermediate_df')
# Now `big_intermediate_df` is gone from the namespace, but compressed bytes are cached.

# Restore later
df = sm.decompress_variable('big_intermediate_df')

# What's compressed?
print(sm.list_compressed())
# {'big_intermediate_df': 'DataFrame'}
```

### Memory report (one-liner)
```python
memory_report()
# Total: 523.4MB | Operational: 12.1MB
```

### Mark operational variables
Variables you don't want compressed (active models, live connections):

```python
sm.mark_operational('model', 'pipe', 'scaler')
# These will be skipped by compress_variable
```

## Common Pitfalls

### `PIL` vs `pillow`
Always import as `from PIL import Image`, not `import pil`. The package is `pillow` on PyPI but the import name is `PIL` (capital). `env_check.py` handles this mapping; if you write your own check, use `'PIL'` not `'pillow'` for the import.

### Log parsing ambiguity
The Python logging format `2026-01-15 10:30:45,123 - myapp - INFO - message` is matched by multiple patterns. `LogAnalyzer` tries patterns in order and uses the first match — for ambiguous cases, override `_parse()` to use your specific format.

### Format detection threshold
`detect_format` returns 'unknown' if the best score < 0.3. This is intentional — for very short or ambiguous content, it's better to say "unknown" than misidentify. If the user knows the format, ask them rather than guessing.

## Workflow: Debugging "It Works On My Machine"

1. `check_requirements(script_path)` to compare installed packages between environments.
2. Look for version mismatches in `result['mismatches']`.
3. If a package is missing, recommend `pip install <name>` with the correct PyPI name (use `PACKAGE_TO_IMPORT` reverse lookup).
4. Check env vars: `FunctionIsolator.mock_env()` lets you reproduce specific env states.
5. Check filesystem: `FunctionIsolator.mock_file()` lets you reproduce specific file contents.
