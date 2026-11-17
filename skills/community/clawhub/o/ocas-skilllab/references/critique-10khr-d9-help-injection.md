# D9: Minimal `--help` Injection Pattern for Python Scripts

When grinding scripts to add `--help` support, full argparse refactoring is often unnecessary and slow.
Use this lightweight pattern instead — insert after the shebang/docstring, before other imports:

```python
import sys
if "--help" in sys.argv or "-h" in sys.argv:
    print("Script description — what it does.")
    print("\nUsage: script.py [--flag] [--help]")
    print("\nOptions:")
    print("  --flag       What the flag does")
    print("  -h, --help   Show this help message")
    sys.exit(0)
```

## When to Use

- Script has no `argparse` and no `if __name__ == "__main__"` guard
- Script executes code at import time (no `main()` function)
- You need `--help` to pass D9 scoring without full refactoring

## Pattern Placement

Insert **immediately after** the docstring, **before** any other imports or code:

```python
#!/usr/bin/env python3
"""Script description.
Usage: script.py [--help]"""

import sys
if "--help" in sys.argv or "-h" in sys.argv:
    print("Script description.")
    print("\nUsage: script.py [--help]")
    print("\nOptions:")
    print("  -h, --help   Show this help message")
    sys.exit(0)

import json  # existing imports continue...
```

## Bash Scripts

Bash scripts use a `case` flag (already common in this library):

```bash
--help)
    sed -n '2,15p' "$0"
    exit 0
    ;;
```

## Verification

After adding, verify:
```bash
python3 script.py --help  # Should print usage and exit 0
echo $?                    # Should be 0
```

## Trade-off

This pattern is **not** a replacement for full argparse in production scripts. It's a grinding-time fix that satisfies D9's "--help documents usage" requirement with minimal edit risk. For scripts with complex flag parsing, consider full argparse instead.