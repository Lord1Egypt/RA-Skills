---
name: Code Smell
description: Static code smell detector for Python, JavaScript/TypeScript, Java, Go, and Ruby. Identifies 10 classic anti-patterns — long functions, god classes, too many parameters, deep nesting, magic numbers/strings, duplicate code blocks, TODO/FIXME debt markers, boolean traps, long method chains, and unreachable code — with per-smell severity ratings, line-level findings, and refactoring suggestions. Zero external dependencies. Zero competitors on ClawHub.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - code-quality
  - refactoring
  - static-analysis
  - developer-tools
  - python
  - javascript
  - typescript
  - java
  - go
  - ruby
---

# phy-code-smell

**Static code smell detector** — finds the 10 most damaging code quality anti-patterns across 5 languages with zero dependencies and zero configuration required.

Unlike linters (which check syntax rules), this tool detects **structural problems**: code that is syntactically valid but architecturally unsound, hard to test, and expensive to maintain.

## What It Detects

| ID | Smell | Severity | Why It Hurts |
|----|-------|----------|--------------|
| CS001 | Long Function (>40 lines) | HIGH | Impossible to test in isolation; hides bugs |
| CS002 | God Class (>20 methods or >400 lines) | HIGH | Single Responsibility violated; breaks teams' mental models |
| CS003 | Too Many Parameters (>5) | MEDIUM | Forces callers to remember argument order; usually means missing object |
| CS004 | Deep Nesting (>4 levels) | MEDIUM | Exponential cognitive load; extract early returns |
| CS005 | Magic Number/String | MEDIUM | Unreadable and unmaintainable; replace with named constant |
| CS006 | Duplicate Code Block (≥6 lines, ≥2 occurrences) | HIGH | Change in one copy never reaches the other |
| CS007 | TODO/FIXME/HACK Debt Marker | LOW | Documents intent to fix; tracks technical debt |
| CS008 | Boolean Trap (≥2 bool params) | MEDIUM | `render(true, false, true)` — no caller knows what these mean |
| CS009 | Long Method Chain (>5 dots) | LOW | Single-step debugging is impossible; violates Law of Demeter |
| CS010 | Unreachable Code (after return/break) | HIGH | Dead logic that misleads readers; suggests a refactoring gone wrong |

## Trigger Phrases

```
/phy-code-smell
Review my codebase for code smells
```

```
/phy-code-smell
Find long functions and god classes in src/
```

```
/phy-code-smell
Code quality audit before the refactoring sprint
```

```
/phy-code-smell
Show me the worst-smelling files in this project
```

---

## Implementation

When invoked, run the following Python analysis. Accept `--root` (default `.`) and optional `--min-severity` flag.

```python
#!/usr/bin/env python3
"""
phy-code-smell — Static code quality smell detector
Detects CS001–CS010 in Python, JS/TS, Java, Go, Ruby
Zero external dependencies.
"""
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from collections import defaultdict


# ─────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────

MAX_FUNCTION_LINES = int(os.environ.get('MAX_FN_LINES', '40'))
MAX_CLASS_METHODS = int(os.environ.get('MAX_CLASS_METHODS', '20'))
MAX_CLASS_LINES = int(os.environ.get('MAX_CLASS_LINES', '400'))
MAX_PARAMS = int(os.environ.get('MAX_PARAMS', '5'))
MAX_NESTING = int(os.environ.get('MAX_NESTING', '4'))
MIN_DUP_LINES = int(os.environ.get('MIN_DUP_LINES', '6'))
MAX_CHAIN_DOTS = int(os.environ.get('MAX_CHAIN_DOTS', '5'))

SKIP_DIRS = {
    '__pycache__', '.git', 'node_modules', 'vendor', '.venv', 'venv',
    'dist', 'build', '.next', 'coverage', 'migrations', 'generated',
    '__tests__', 'e2e', 'fixtures', 'mocks',
}

SEVERITY_ORDER = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
SEVERITY_EMOJI = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🔵'}

CI_MODE = '--ci' in sys.argv
MIN_SEVERITY = next(
    (sys.argv[sys.argv.index('--min-severity') + 1]
     for _ in ['x'] if '--min-severity' in sys.argv),
    'LOW'
)


# ─────────────────────────────────────────────────────
# Data model
# ─────────────────────────────────────────────────────

@dataclass
class SmellFinding:
    check_id: str
    file: str
    line: int
    severity: str
    element: str      # function/class/block name
    description: str
    suggestion: str
    metric: str = ''  # e.g. "47 lines", "8 params"


# ─────────────────────────────────────────────────────
# File walker
# ─────────────────────────────────────────────────────

LANG_EXTENSIONS = {
    'python': {'.py'},
    'javascript': {'.js', '.mjs', '.cjs', '.jsx'},
    'typescript': {'.ts', '.tsx'},
    'java': {'.java', '.kt'},
    'go': {'.go'},
    'ruby': {'.rb'},
}

ALL_EXTENSIONS = set().union(*LANG_EXTENSIONS.values())


def get_lang(path: Path) -> Optional[str]:
    ext = path.suffix.lower()
    for lang, exts in LANG_EXTENSIONS.items():
        if ext in exts:
            return lang
    return None


def walk_files(root: Path):
    """Yield (path, content, lang) for all source files."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and not d.startswith('.')]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            lang = get_lang(fpath)
            if not lang:
                continue
            # Skip test files
            name_lower = fpath.name.lower()
            if any(x in name_lower for x in ('test', 'spec', '_test', '.test.',
                                              '.spec.', 'mock', 'fixture')):
                continue
            try:
                content = fpath.read_text(errors='ignore')
                yield fpath, content, lang
            except Exception:
                continue


# ─────────────────────────────────────────────────────
# CS001 — Long Function
# ─────────────────────────────────────────────────────

# Each entry: (lang_pattern, regex_for_function_start)
FUNCTION_START_PATTERNS = {
    'python': re.compile(
        r'^(?P<indent> {0,16})def\s+(?P<name>\w+)\s*\(', re.MULTILINE
    ),
    'javascript': re.compile(
        r'^(?P<indent> {0,16})(?:async\s+)?function\s*\*?\s*(?P<name>\w+)\s*\(|'
        r'^(?P<indent2> {0,16})(?:const|let|var)\s+(?P<name2>\w+)\s*=\s*(?:async\s+)?\(',
        re.MULTILINE
    ),
    'typescript': re.compile(
        r'^(?P<indent> {0,16})(?:async\s+)?function\s*\*?\s*(?P<name>\w+)\s*\(|'
        r'^(?P<indent2> {0,16})(?:const|let|var)\s+(?P<name2>\w+)\s*=\s*(?:async\s+)?\(',
        re.MULTILINE
    ),
    'java': re.compile(
        r'^(?P<indent> {0,16})(?:public|protected|private|static|final|synchronized|\s)+'
        r'[\w<>\[\]]+\s+(?P<name>\w+)\s*\(',
        re.MULTILINE
    ),
    'go': re.compile(
        r'^func\s+(?:\(\w+\s+\*?\w+\)\s+)?(?P<name>\w+)\s*\(',
        re.MULTILINE
    ),
    'ruby': re.compile(
        r'^(?P<indent> {0,16})def\s+(?P<name>\w[\w?!]*)',
        re.MULTILINE
    ),
}

# End markers per language (indent-based for Python/Ruby, brace for others)
BRACE_LANGS = {'javascript', 'typescript', 'java', 'go'}


def find_function_end_brace(content: str, start_pos: int) -> int:
    """Find the closing brace of a function, returns line number of closing brace."""
    depth = 0
    i = start_pos
    found_open = False
    while i < len(content):
        c = content[i]
        if c == '{':
            depth += 1
            found_open = True
        elif c == '}':
            depth -= 1
            if found_open and depth == 0:
                return content[:i].count('\n') + 1
        i += 1
    return content.count('\n') + 1


def find_function_end_indent(lines: list[str], start_line: int, base_indent: int) -> int:
    """For Python/Ruby: find the last line of the function body by indentation."""
    end = start_line
    for i in range(start_line + 1, len(lines)):
        line = lines[i]
        stripped = line.lstrip()
        if not stripped or stripped.startswith('#'):
            continue
        indent = len(line) - len(stripped)
        if indent <= base_indent:
            return i - 1
        end = i
    return end


def check_long_functions(fpath: Path, content: str, lang: str) -> list[SmellFinding]:
    findings = []
    pattern = FUNCTION_START_PATTERNS.get(lang)
    if not pattern:
        return []

    lines = content.split('\n')

    for m in pattern.finditer(content):
        name = (m.group('name') or m.groupdict().get('name2') or
                m.groupdict().get('name') or '<anonymous>')
        if name in {'<anonymous>', 'if', 'for', 'while', 'switch'}:
            continue
        start_line = content[:m.start()].count('\n') + 1

        if lang in BRACE_LANGS:
            end_line = find_function_end_brace(content, m.start())
        else:
            indent_group = m.groupdict().get('indent', '')
            base_indent = len(indent_group) if indent_group else 0
            end_line = find_function_end_indent(lines, start_line - 1, base_indent)

        fn_lines = end_line - start_line + 1
        if fn_lines > MAX_FUNCTION_LINES:
            findings.append(SmellFinding(
                check_id='CS001',
                file=str(fpath),
                line=start_line,
                severity='HIGH',
                element=name,
                description=f'Function `{name}` is {fn_lines} lines long (max: {MAX_FUNCTION_LINES}).',
                suggestion=(
                    f'Extract sub-operations into helper functions. '
                    f'Aim for each function to do ONE thing: describe it in a single sentence. '
                    f'Look for "and" in the function name — it usually signals two functions.'
                ),
                metric=f'{fn_lines} lines',
            ))
    return findings


# ─────────────────────────────────────────────────────
# CS002 — God Class
# ─────────────────────────────────────────────────────

CLASS_START_PATTERNS = {
    'python': re.compile(r'^class\s+(?P<name>\w+)', re.MULTILINE),
    'javascript': re.compile(r'^class\s+(?P<name>\w+)', re.MULTILINE),
    'typescript': re.compile(r'^(?:export\s+)?(?:abstract\s+)?class\s+(?P<name>\w+)', re.MULTILINE),
    'java': re.compile(
        r'^(?:public\s+|protected\s+|private\s+|abstract\s+|final\s+)*class\s+(?P<name>\w+)',
        re.MULTILINE
    ),
    'ruby': re.compile(r'^class\s+(?P<name>\w+)', re.MULTILINE),
}

METHOD_COUNT_PATTERNS = {
    'python': re.compile(r'^\s+def\s+\w+', re.MULTILINE),
    'javascript': re.compile(r'^\s+(?:async\s+)?\w+\s*\(', re.MULTILINE),
    'typescript': re.compile(r'^\s+(?:(?:public|private|protected|static|async)\s+)*\w+\s*\(', re.MULTILINE),
    'java': re.compile(
        r'^\s+(?:public|protected|private|static|final|synchronized|\s)+'
        r'[\w<>\[\]]+\s+\w+\s*\(', re.MULTILINE
    ),
    'ruby': re.compile(r'^\s+def\s+\w+', re.MULTILINE),
}


def check_god_classes(fpath: Path, content: str, lang: str) -> list[SmellFinding]:
    findings = []
    pattern = CLASS_START_PATTERNS.get(lang)
    method_pattern = METHOD_COUNT_PATTERNS.get(lang)
    if not pattern or not method_pattern:
        return []

    lines = content.split('\n')

    for m in pattern.finditer(content):
        name = m.group('name')
        start_line = content[:m.start()].count('\n') + 1

        if lang in BRACE_LANGS:
            end_line = find_function_end_brace(content, m.start())
        else:
            end_line = find_function_end_indent(lines, start_line - 1, 0)

        class_body = '\n'.join(lines[start_line - 1:end_line])
        class_lines = end_line - start_line + 1
        method_count = len(method_pattern.findall(class_body))

        issues = []
        if method_count > MAX_CLASS_METHODS:
            issues.append(f'{method_count} methods (max: {MAX_CLASS_METHODS})')
        if class_lines > MAX_CLASS_LINES:
            issues.append(f'{class_lines} lines (max: {MAX_CLASS_LINES})')

        if issues:
            findings.append(SmellFinding(
                check_id='CS002',
                file=str(fpath),
                line=start_line,
                severity='HIGH',
                element=name,
                description=f'God class `{name}`: {", ".join(issues)}.',
                suggestion=(
                    f'Apply Single Responsibility Principle. '
                    f'Group methods by responsibility and extract into separate classes. '
                    f'Common splits: data (model), behavior (service), presentation (formatter).'
                ),
                metric=', '.join(issues),
            ))
    return findings


# ─────────────────────────────────────────────────────
# CS003 — Too Many Parameters
# ─────────────────────────────────────────────────────

def count_params(param_str: str) -> int:
    """Count parameters in a parameter string, handling nested generics/types."""
    if not param_str.strip():
        return 0
    depth = 0
    count = 1
    for c in param_str:
        if c in '(<{[':
            depth += 1
        elif c in ')>}]':
            depth -= 1
        elif c == ',' and depth == 0:
            count += 1
    return count


PARAM_LIST_PATTERNS = {
    'python': re.compile(
        r'^\s*def\s+(?P<name>\w+)\s*\((?P<params>[^)]*)\)',
        re.MULTILINE
    ),
    'javascript': re.compile(
        r'(?:function\s+(?P<name>\w+)|(?P<name2>\w+)\s*=\s*(?:async\s+)?function)\s*\((?P<params>[^)]*)\)',
    ),
    'typescript': re.compile(
        r'(?:function\s+(?P<name>\w+)|(?P<name2>\w+)\s*=\s*(?:async\s+)?function)\s*\((?P<params>[^)]*)\)',
    ),
    'java': re.compile(
        r'(?:public|protected|private|static)\s+\S+\s+(?P<name>\w+)\s*\((?P<params>[^)]*)\)',
    ),
    'go': re.compile(
        r'func\s+(?:\(\w+\s+\*?\w+\)\s+)?(?P<name>\w+)\s*\((?P<params>[^)]*)\)',
    ),
    'ruby': re.compile(
        r'^\s*def\s+(?P<name>\w[\w?!]*)\s*\((?P<params>[^)]*)\)',
        re.MULTILINE
    ),
}

# Skip these Python special params
SKIP_PYTHON_PARAMS = {'self', 'cls', '*args', '**kwargs', '*', '/'}


def check_too_many_params(fpath: Path, content: str, lang: str) -> list[SmellFinding]:
    findings = []
    pattern = PARAM_LIST_PATTERNS.get(lang)
    if not pattern:
        return []

    for m in pattern.finditer(content):
        name = (m.groupdict().get('name') or m.groupdict().get('name2') or
                m.groupdict().get('name3') or '<func>')
        params_raw = m.groupdict().get('params', '') or ''
        if not params_raw.strip():
            continue

        # Normalize params
        if lang == 'python':
            params = [p.strip().split(':')[0].split('=')[0].strip()
                      for p in params_raw.split(',')]
            params = [p for p in params if p and p not in SKIP_PYTHON_PARAMS]
        else:
            params = [p.strip() for p in params_raw.split(',') if p.strip()]

        n = len(params)
        if n > MAX_PARAMS:
            line_no = content[:m.start()].count('\n') + 1
            findings.append(SmellFinding(
                check_id='CS003',
                file=str(fpath),
                line=line_no,
                severity='MEDIUM',
                element=name,
                description=f'Function `{name}` has {n} parameters (max: {MAX_PARAMS}).',
                suggestion=(
                    f'Group related parameters into a config object/dataclass. '
                    f'Example: replace (host, port, timeout, retries, ssl) with ConnectionConfig. '
                    f'Parameters that always travel together are a data clump.'
                ),
                metric=f'{n} params',
            ))
    return findings


# ─────────────────────────────────────────────────────
# CS004 — Deep Nesting
# ─────────────────────────────────────────────────────

# Indent-based for Python/Ruby; brace-count for others
NESTING_TRIGGERS = {
    'python': re.compile(r'^\s*(?:if|elif|else|for|while|with|try|except|finally)\b'),
    'javascript': re.compile(r'(?:if|else\s+if|for|while|switch|try|catch)\s*[\({]'),
    'typescript': re.compile(r'(?:if|else\s+if|for|while|switch|try|catch)\s*[\({]'),
    'java': re.compile(r'(?:if|else\s+if|for|while|switch|try|catch)\s*[\({]'),
    'go': re.compile(r'(?:if|else\s+if|for|switch|select)\s+'),
    'ruby': re.compile(r'^\s*(?:if|elsif|else|unless|while|until|for|begin|rescue|case)\b'),
}


def check_deep_nesting(fpath: Path, content: str, lang: str) -> list[SmellFinding]:
    findings = []
    lines = content.split('\n')

    if lang in ('python', 'ruby'):
        # Count nesting by indentation level (4 spaces = 1 level)
        for i, line in enumerate(lines):
            stripped = line.lstrip()
            if not stripped or stripped.startswith('#'):
                continue
            indent = len(line) - len(stripped)
            nesting = indent // 4
            if nesting > MAX_NESTING:
                findings.append(SmellFinding(
                    check_id='CS004',
                    file=str(fpath),
                    line=i + 1,
                    severity='MEDIUM',
                    element=stripped[:60],
                    description=f'Code nested {nesting} levels deep (max: {MAX_NESTING}).',
                    suggestion=(
                        'Invert conditions to return early. '
                        'Replace nested ifs with guard clauses: '
                        'if not condition: return. '
                        'Extract nested blocks into helper functions.'
                    ),
                    metric=f'{nesting} levels',
                ))
    else:
        # Brace-based nesting depth
        trigger = NESTING_TRIGGERS.get(lang)
        depth = 0
        for i, line in enumerate(lines):
            depth += line.count('{') - line.count('}')
            if depth > MAX_NESTING and trigger and trigger.search(line):
                stripped = line.strip()
                findings.append(SmellFinding(
                    check_id='CS004',
                    file=str(fpath),
                    line=i + 1,
                    severity='MEDIUM',
                    element=stripped[:60],
                    description=f'Control flow nested {depth} levels deep (max: {MAX_NESTING}).',
                    suggestion=(
                        'Extract inner blocks into named functions. '
                        'Use early returns to reduce nesting. '
                        'Consider guard clauses: validate inputs first, then process.'
                    ),
                    metric=f'{depth} levels',
                ))

    # Deduplicate consecutive lines — keep only highest nesting line per 5-line window
    deduped = []
    last_line = -10
    for f in sorted(findings, key=lambda x: x.line):
        if f.line - last_line >= 5:
            deduped.append(f)
            last_line = f.line
    return deduped


# ─────────────────────────────────────────────────────
# CS005 — Magic Numbers and Strings
# ─────────────────────────────────────────────────────

# Numbers that are almost always intentional and not "magic"
SAFE_NUMBERS = {
    '0', '1', '2', '-1', '0.0', '1.0', '0.5', '100', '1000',
    '1024', '65536', '3.14', '3.14159', '2.718', '60', '24', '7',
    '12', '365', '3600', '86400',
}

MAGIC_NUMBER_RE = re.compile(
    r'(?<![.\w])(-?\d+\.?\d*(?:[eE][+-]?\d+)?)(?![.\w])'
)

# Magic string: non-empty string literal of length ≥ 5 that isn't in common patterns
MAGIC_STRING_RE = re.compile(
    r"""(?<!\\)(?:["'])([^"'\\]{8,})(?:["'])"""
)

SAFE_STRING_PATTERNS = re.compile(
    r"""(?:https?://|//|#|SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|
    Content-Type|application/|charset=|text/|multipart/|
    %s|%d|{|}|\{\w+\}|\\n|\\t|
    __.*__|->|=>|error:|warning:|info:|debug:)""",
    re.IGNORECASE | re.VERBOSE
)


def check_magic_literals(fpath: Path, content: str, lang: str) -> list[SmellFinding]:
    findings = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        stripped = line.strip()
        # Skip comments, imports, constant definitions, test assertions
        if stripped.startswith(('//','#','*','import','from','require','const '
                                 'MAX','MIN','DEFAULT','CONFIG','TIMEOUT')):
            continue
        if any(x in stripped for x in ('assert', 'expect(', 'toBe(', 'assertEqual',
                                         '== True', '== False', 'const ', 'final ')):
            continue
        # Skip line if it looks like a constant definition
        if re.match(r'\s*(?:const|let|final|val|var)\s+[A-Z_]+\s*[=:]', line):
            continue

        # Magic numbers
        for m in MAGIC_NUMBER_RE.finditer(stripped):
            num = m.group(1)
            if num in SAFE_NUMBERS:
                continue
            # Skip array indices, loop counters, simple math in assignments
            ctx = stripped[max(0, m.start()-10):m.end()+10]
            if re.search(r'\[\s*' + re.escape(num) + r'\s*\]', ctx):
                continue

            findings.append(SmellFinding(
                check_id='CS005',
                file=str(fpath),
                line=i + 1,
                severity='MEDIUM',
                element=f'literal {num}',
                description=f'Magic number `{num}` — meaning unclear without context.',
                suggestion=f'Extract to a named constant: MAX_RETRIES = {num} or TIMEOUT_SECONDS = {num}',
                metric=f'literal {num}',
            ))
            break  # One finding per line for magic numbers

        # Magic strings (only flag once per line)
        for m in MAGIC_STRING_RE.finditer(stripped):
            s = m.group(1)
            if SAFE_STRING_PATTERNS.search(s):
                continue
            if len(s) < 8:
                continue
            # Skip paths, log messages, format strings
            if '/' in s or '%' in s or '{' in s:
                continue

            findings.append(SmellFinding(
                check_id='CS005',
                file=str(fpath),
                line=i + 1,
                severity='MEDIUM',
                element=f'"{s[:30]}"',
                description=f'Magic string `"{s[:30]}"` — should be a named constant.',
                suggestion='Move to a constants file or configuration. Makes typos catchable at compile time.',
                metric=f'string len={len(s)}',
            ))
            break  # One per line

    return findings


# ─────────────────────────────────────────────────────
# CS006 — Duplicate Code Blocks
# ─────────────────────────────────────────────────────

def _normalize_line(line: str) -> str:
    """Normalize a line for duplication comparison (strip whitespace, remove literals)."""
    line = line.strip()
    line = re.sub(r'"[^"]*"', '"STR"', line)
    line = re.sub(r"'[^']*'", '"STR"', line)
    line = re.sub(r'\b\d+\b', 'NUM', line)
    return line


def check_duplicate_blocks(fpath: Path, content: str, lang: str) -> list[SmellFinding]:
    findings = []
    lines = content.split('\n')
    normalized = [_normalize_line(l) for l in lines]

    # Build n-gram fingerprints
    n = MIN_DUP_LINES
    seen_blocks: dict[tuple, int] = {}  # fingerprint → first line number

    for i in range(len(normalized) - n + 1):
        block = tuple(normalized[i:i + n])
        # Skip blocks that are mostly blank/comments
        non_empty = sum(1 for l in block if l.strip() and not l.strip().startswith(('//','#','*')))
        if non_empty < n // 2:
            continue

        if block in seen_blocks:
            first_line = seen_blocks[block]
            findings.append(SmellFinding(
                check_id='CS006',
                file=str(fpath),
                line=i + 1,
                severity='HIGH',
                element=f'block at line {first_line}',
                description=(
                    f'Duplicate code block ({n} lines) — '
                    f'identical structure first seen at line {first_line}.'
                ),
                suggestion=(
                    f'Extract duplicated logic into a shared function. '
                    f'Even 3 occurrences of the same logic costs 3× the maintenance. '
                    f'Rule of Three: once = ok, twice = watch, thrice = extract.'
                ),
                metric=f'{n} duplicate lines',
            ))
        else:
            seen_blocks[block] = i + 1

    # Deduplicate findings for closely adjacent lines
    deduped = []
    last_line = -100
    for f in sorted(findings, key=lambda x: x.line):
        if f.line - last_line >= n:
            deduped.append(f)
            last_line = f.line
    return deduped


# ─────────────────────────────────────────────────────
# CS007 — TODO/FIXME/HACK Debt Markers
# ─────────────────────────────────────────────────────

DEBT_MARKER_RE = re.compile(
    r'(?://|#|<!--)\s*(?P<marker>TODO|FIXME|HACK|XXX|BUG|TEMP|KLUDGE)\b(?P<rest>[^\n]*)',
    re.IGNORECASE
)


def check_debt_markers(fpath: Path, content: str, lang: str) -> list[SmellFinding]:
    findings = []
    for m in DEBT_MARKER_RE.finditer(content):
        marker = m.group('marker').upper()
        rest = m.group('rest').strip()[:80]
        line_no = content[:m.start()].count('\n') + 1

        severity = 'HIGH' if marker in ('FIXME', 'BUG', 'HACK') else 'LOW'
        findings.append(SmellFinding(
            check_id='CS007',
            file=str(fpath),
            line=line_no,
            severity=severity,
            element=f'{marker}',
            description=f'{marker}: {rest}' if rest else f'{marker} marker with no description.',
            suggestion=(
                f'File a GitHub issue and link it: {marker}(#123). '
                f'Track debt in your issue tracker — not in code comments. '
                f'Use git-blame to see how old this is.'
            ),
            metric=marker,
        ))
    return findings


# ─────────────────────────────────────────────────────
# CS008 — Boolean Trap
# ─────────────────────────────────────────────────────

BOOL_PARAM_RE = re.compile(
    r'def\s+(?P<name>\w+)\s*\((?P<params>[^)]+)\)',
    re.IGNORECASE
)

BOOL_TYPE_RE = re.compile(r'\bbool(?:ean)?\b', re.IGNORECASE)
BOOL_DEFAULT_RE = re.compile(r'=\s*(?:True|False|true|false)\b')


def check_boolean_trap(fpath: Path, content: str, lang: str) -> list[SmellFinding]:
    findings = []

    # Pattern for function definitions with typed bool params
    for m in re.finditer(
        r'(?:def|function|func)\s+(?P<name>\w+)\s*\((?P<params>[^)]{1,300})\)',
        content, re.IGNORECASE
    ):
        name = m.group('name')
        params_raw = m.group('params')

        bool_params = []
        for param in params_raw.split(','):
            param = param.strip()
            if (BOOL_TYPE_RE.search(param) or
                    BOOL_DEFAULT_RE.search(param) or
                    re.search(r'\b(?:is_|has_|can_|should_|enable|disable|verbose|debug|force|dry_run)\w*\s*:', param)):
                bool_params.append(param.split(':')[0].split('=')[0].strip())

        if len(bool_params) >= 2:
            line_no = content[:m.start()].count('\n') + 1
            findings.append(SmellFinding(
                check_id='CS008',
                file=str(fpath),
                line=line_no,
                severity='MEDIUM',
                element=name,
                description=(
                    f'Function `{name}` has {len(bool_params)} boolean parameters '
                    f'({", ".join(bool_params[:3])}). '
                    f'Callers write `{name}(user, true, false)` — impossible to understand without the signature.'
                ),
                suggestion=(
                    f'Replace multiple bool params with an options object/enum: '
                    f'`{name}(user, mode=Mode.VERBOSE)` instead of `{name}(user, verbose=True, debug=False)`. '
                    f'Or split into separate functions: `{name}_verbose()`, `{name}_quiet()`.'
                ),
                metric=f'{len(bool_params)} bool params',
            ))
    return findings


# ─────────────────────────────────────────────────────
# CS009 — Long Method Chain
# ─────────────────────────────────────────────────────

METHOD_CHAIN_RE = re.compile(
    r'(\w+(?:\([^()]*\))?\s*(?:\.\s*\w+(?:\([^()]*\))?){' +
    str(MAX_CHAIN_DOTS) + r',})'
)


def check_long_chains(fpath: Path, content: str, lang: str) -> list[SmellFinding]:
    if lang not in ('javascript', 'typescript', 'java', 'ruby'):
        return []

    findings = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(('//','#','*')):
            continue
        dot_count = stripped.count('.')
        if dot_count < MAX_CHAIN_DOTS:
            continue

        m = METHOD_CHAIN_RE.search(stripped)
        if m:
            chain = m.group(1)
            chain_dots = chain.count('.')
            findings.append(SmellFinding(
                check_id='CS009',
                file=str(fpath),
                line=i + 1,
                severity='LOW',
                element=chain[:60],
                description=f'Method chain {chain_dots} calls deep — impossible to debug one step at a time.',
                suggestion=(
                    'Break the chain into named intermediate variables: '
                    'const filtered = users.filter(active); '
                    'const sorted = filtered.sort(byDate); '
                    'const names = sorted.map(getName);'
                ),
                metric=f'{chain_dots} chained calls',
            ))
    return findings


# ─────────────────────────────────────────────────────
# CS010 — Unreachable Code
# ─────────────────────────────────────────────────────

RETURN_BREAK_RE = {
    'python': re.compile(r'^\s+(return|raise|break|continue)\b'),
    'javascript': re.compile(r'^\s+(return|throw|break|continue)\b'),
    'typescript': re.compile(r'^\s+(return|throw|break|continue)\b'),
    'java': re.compile(r'^\s+(return|throw|break|continue)\b'),
    'go': re.compile(r'^\s+(return|panic\()\b'),
    'ruby': re.compile(r'^\s+(return|raise|next|break)\b'),
}


def check_unreachable_code(fpath: Path, content: str, lang: str) -> list[SmellFinding]:
    findings = []
    pattern = RETURN_BREAK_RE.get(lang)
    if not pattern:
        return []

    lines = content.split('\n')

    for i, line in enumerate(lines[:-1]):
        if not pattern.match(line):
            continue
        # Get indentation of the return/break line
        return_indent = len(line) - len(line.lstrip())
        # Look at the next non-blank line
        for j in range(i + 1, min(i + 4, len(lines))):
            next_line = lines[j]
            if not next_line.strip() or next_line.strip().startswith(('//','#','}')):
                continue
            next_indent = len(next_line) - len(next_line.lstrip())
            if next_indent == return_indent:
                # Same indentation — code after a terminal statement
                findings.append(SmellFinding(
                    check_id='CS010',
                    file=str(fpath),
                    line=j + 1,
                    severity='HIGH',
                    element=next_line.strip()[:60],
                    description=f'Unreachable code after `{line.strip()[:40]}`.',
                    suggestion=(
                        'Delete the unreachable code or move the terminal statement. '
                        'This often indicates a refactoring that was partially completed. '
                        'Use git blame to understand the intent.'
                    ),
                    metric='unreachable',
                ))
            break

    return findings


# ─────────────────────────────────────────────────────
# File-level summary
# ─────────────────────────────────────────────────────

@dataclass
class FileReport:
    path: str
    findings: list[SmellFinding] = field(default_factory=list)

    @property
    def smell_score(self) -> int:
        score = 0
        for f in self.findings:
            score += {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}.get(f.severity, 0)
        return score


# ─────────────────────────────────────────────────────
# Main runner
# ─────────────────────────────────────────────────────

CHECKS = [
    check_long_functions,
    check_god_classes,
    check_too_many_params,
    check_deep_nesting,
    check_magic_literals,
    check_duplicate_blocks,
    check_debt_markers,
    check_boolean_trap,
    check_long_chains,
    check_unreachable_code,
]


def run_audit(root: Path) -> int:
    print(f"\n🔍  phy-code-smell — scanning {root}\n{'─'*60}")

    all_findings: list[SmellFinding] = []
    file_reports: dict[str, FileReport] = {}

    severity_threshold = SEVERITY_ORDER.get(MIN_SEVERITY, 2)

    for fpath, content, lang in walk_files(root):
        file_findings: list[SmellFinding] = []
        for check in CHECKS:
            try:
                results = check(fpath, content, lang)
                file_findings.extend(results)
            except Exception:
                pass

        # Filter by severity
        file_findings = [f for f in file_findings
                         if SEVERITY_ORDER.get(f.severity, 2) <= severity_threshold]

        if file_findings:
            rel = str(fpath.relative_to(root) if root != Path('.') else fpath)
            file_reports[rel] = FileReport(path=rel, findings=file_findings)
            all_findings.extend(file_findings)

    if not all_findings:
        print("✅  No code smells found.")
        return 0

    # Sort findings by severity
    all_findings.sort(key=lambda f: (SEVERITY_ORDER.get(f.severity, 2), f.file, f.line))

    high = sum(1 for f in all_findings if f.severity == 'HIGH')
    med = sum(1 for f in all_findings if f.severity == 'MEDIUM')
    low = sum(1 for f in all_findings if f.severity == 'LOW')

    print(f"Found {len(all_findings)} smell(s) in {len(file_reports)} file(s): "
          f"🔴 HIGH={high}  🟡 MEDIUM={med}  🔵 LOW={low}")

    # Top 5 smelliest files
    sorted_files = sorted(file_reports.values(), key=lambda r: r.smell_score, reverse=True)
    print(f"\n📊 Smelliest files (by score):")
    for fr in sorted_files[:5]:
        print(f"  {fr.smell_score:3d} pts  {fr.path}  ({len(fr.findings)} findings)")

    # Findings grouped by severity
    current_severity = None
    for f in all_findings:
        if f.severity != current_severity:
            current_severity = f.severity
            emoji = SEVERITY_EMOJI.get(f.severity, '⚪')
            print(f"\n{emoji} {f.severity} — {f.check_id}\n{'─'*50}")

        print(f"\n[{f.check_id}] {f.file}:{f.line}  {f.metric}")
        print(f"  {f.description}")
        print(f"  → {f.suggestion}")

    # Summary by smell type
    print(f"\n{'═'*60}")
    smell_counts: dict[str, int] = defaultdict(int)
    for f in all_findings:
        smell_counts[f.check_id] += 1
    print("Smell breakdown:")
    for check_id, count in sorted(smell_counts.items(), key=lambda x: -x[1]):
        print(f"  {check_id}: {count}")

    print(f"\nCI fail-gate (fails on HIGH findings):")
    print(f"  python code_smell.py --root . --ci --min-severity HIGH")

    if CI_MODE and high > 0:
        print(f"\n[CI] Exit 1 — {high} HIGH severity smells found.")
        return 1
    return 0


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Static code smell detector')
    parser.add_argument('--root', default='.', help='Root directory to scan')
    parser.add_argument('--ci', action='store_true', help='Exit 1 on HIGH severity smells')
    parser.add_argument('--min-severity', choices=['HIGH', 'MEDIUM', 'LOW'],
                        default='LOW', help='Minimum severity to report')
    parser.add_argument('--max-fn-lines', type=int, default=40)
    parser.add_argument('--max-params', type=int, default=5)
    parser.add_argument('--max-nesting', type=int, default=4)
    args = parser.parse_args()

    MAX_FUNCTION_LINES = args.max_fn_lines
    MAX_PARAMS = args.max_params
    MAX_NESTING = args.max_nesting
    CI_MODE = args.ci
    MIN_SEVERITY = args.min_severity

    sys.exit(run_audit(Path(args.root)))
```

---

## Example Output

```
🔍  phy-code-smell — scanning /home/user/myproject
────────────────────────────────────────────────────────────
Found 12 smell(s) in 4 file(s): 🔴 HIGH=5  🟡 MEDIUM=5  🔵 LOW=2

📊 Smelliest files (by score):
  18 pts  src/services/UserService.py  (6 findings)
   9 pts  src/api/handlers.py  (3 findings)
   5 pts  src/utils/formatters.ts  (2 findings)
   3 pts  src/models/order.rb  (1 finding)

🔴 HIGH — CS001
──────────────────────────────────────────────────────

[CS001] src/services/UserService.py:47  72 lines
  Function `create_user_with_notifications` is 72 lines long (max: 40).
  → Extract sub-operations into helper functions. Aim for each function to
    do ONE thing: describe it in a single sentence. Look for "and" in the
    function name — it usually signals two functions.

[CS002] src/services/UserService.py:12  24 methods, 487 lines
  God class `UserService`: 24 methods (max: 20), 487 lines (max: 400).
  → Apply Single Responsibility Principle. Common splits: data (model),
    behavior (service), presentation (formatter).

🟡 MEDIUM — CS003
──────────────────────────────────────────────────────

[CS003] src/api/handlers.py:89  8 params
  Function `handle_payment` has 8 parameters (max: 5).
  → Group related parameters into a config object: replace
    (host, port, timeout, retries, ssl) with ConnectionConfig.

[CS005] src/api/handlers.py:134  literal 86400
  Magic number `86400` — meaning unclear without context.
  → Extract to a named constant: SECONDS_PER_DAY = 86400

════════════════════════════════════════════════════════════
Smell breakdown:
  CS001: 3
  CS003: 3
  CS007: 2
  CS005: 2
  CS002: 1
  CS010: 1

CI fail-gate (fails on HIGH findings):
  python code_smell.py --root . --ci --min-severity HIGH
```

---

## Configuration via Environment Variables

```bash
# All thresholds are configurable
export MAX_FN_LINES=50      # default: 40
export MAX_CLASS_METHODS=25  # default: 20
export MAX_CLASS_LINES=500   # default: 400
export MAX_PARAMS=4          # default: 5
export MAX_NESTING=3         # default: 4
export MIN_DUP_LINES=8       # default: 6

python code_smell.py --root src/
```

Or via CLI flags:
```bash
python code_smell.py --root . --max-fn-lines 60 --max-params 6 --min-severity HIGH
```

---

## Relationship to Other phy- Skills

| Skill | What It Checks |
|-------|----------------|
| `phy-code-smell` (this) | **Structural quality** — functions, classes, complexity |
| `phy-ts-any-auditor` | TypeScript `any` type sprawl |
| `phy-regex-audit` | ReDoS vulnerabilities in regex patterns |
| `phy-flag-janitor` | Dead feature flags |
| `phy-concurrency-audit` | Race conditions and TOCTOU bugs |
| `phy-dead-code` | Unused CSS selectors |

`phy-code-smell` is the language-agnostic structural audit layer. The others are targeted deep-dives into specific problem domains.

---

## Supported Languages

| Language | CS001 | CS002 | CS003 | CS004 | CS005 | CS006 | CS007 | CS008 | CS009 | CS010 |
|----------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| Python | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| JavaScript | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| TypeScript | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Java / Kotlin | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Go | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| Ruby | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ |

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
