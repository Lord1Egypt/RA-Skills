#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · Template rendering engine (contract script)
-------------------------------------------------
Render a Markdown template with placeholders plus YAML/JSON data into a final
Markdown artifact.

Supported template syntax (mini-Jinja, sufficient for PM documents):
  1. Variable:    {{ project.name }}   or  {{ this.id }}
  2. Loop:        {{#each risks}} ... {{this.description}} ... {{/each}}
  3. Loop vars:   {{@index}} / {{@first}} / {{@last}} (available inside loops, often used to join comma arrays)
  4. Condition:   {{#if framework == "scrum"}} ... {{else}} ... {{/if}}
                   (also accepts {{#else}}, the two are equivalent)
  5. Comparisons: ==  /  !=  (for #if)
  6. Literals:    "text"  /  'text'  /  true / false / null / number
  7. List index:  {{ burndown.[0].remaining }} (supports the arr.[n] form)
  8. Field join:  {{ join(burndown, ", ", "day") }} -> 1, 2, 3 (single-line join, for mermaid arrays; None falls back to 0 to avoid crashes)
  9. Mermaid safety helpers:
   - {{ mid(text) }}      -> mermaid node/task safe ID (spaces/dots/irregular chars -> underscore, guaranteed non-empty and not starting with a digit)
   - {{ mlabel(text) }}   -> mermaid label text (escapes double quotes, collapses whitespace, for use inside ["..."])
   - {{ gname(text) }}    -> gantt task display name (label-safe + colon -> full-width, to avoid breaking the `name :id` separator)
 10. Color helpers (risk register, etc.):
   - {{ sev_icon(text) }} / {{ risk_icon(text) }} -> map a severity (green/yellow/orange/red or
     low/medium/high/critical) to its canonical color word: green / yellow / orange / red; unknown -> empty string

Data merge: inside a loop, reference the current element via `this`; one level of nested
loops is supported (this is overwritten per level).
Missing variables output an empty string without raising (enabling partial-data rendering).
"""
import os
import sys
import argparse
import re

try:
    import yaml
except ImportError:
    yaml = None


# ---------- Expression evaluation ----------
def _resolve(path, ctx):
    """Resolve a value from ctx by '.' path, supporting dict / list indexing (incl. arr.[0])."""
    cur = ctx
    for part in str(path).split('.'):
        # support list index segment: arr.[0] -> 0
        if len(part) >= 3 and part.startswith('[') and part.endswith(']'):
            part = part[1:-1]
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return cur


def _resolve_or_literal(tok, ctx):
    tok = tok.strip()
    if len(tok) >= 2 and ((tok[0] == '"' and tok[-1] == '"') or (tok[0] == "'" and tok[-1] == "'")):
        return tok[1:-1]
    low = tok.lower()
    if low in ('true', 'false', 'null'):
        return {'true': True, 'false': False, 'null': None}[low]
    try:
        return int(tok)
    except ValueError:
        pass
    try:
        return float(tok)
    except ValueError:
        pass
    return _resolve(tok, ctx)


def _eval(expr, ctx):
    expr = expr.strip()
    # support helper calls inside #if, e.g. (eq granularity "fortnight") / (sev_cell x y)
    if expr.startswith('(') and expr.endswith(')'):
        inner = expr[1:-1].strip()
        if re.match(r'^\w+[(\s]', inner):
            hres = _call_helper(inner, ctx)
            if hres is not None:
                return hres
    for op in ('==', '!='):
        if op in expr:
            left, right = expr.split(op, 1)
            l = _resolve_or_literal(left, ctx)
            r = _resolve_or_literal(right, ctx)
            return (l == r) if op == '==' else (l != r)
    return _resolve_or_literal(expr, ctx)


def _split_args(s):
    """Split by comma, ignoring commas inside quotes (used for join() argument parsing)."""
    out = []
    cur = []
    in_q = None
    for ch in s:
        if in_q:
            cur.append(ch)
            if ch == in_q:
                in_q = None
        elif ch in ('"', "'"):
            in_q = ch
            cur.append(ch)
        elif ch == ',':
            out.append(''.join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append(''.join(cur))
    return [p.strip() for p in out]


def _join_call(tag, ctx):
    """Support field join of the form join(listExpr, "sep", "field") (single-line, no newlines).

    Example: {{ join(burndown, ", ", "day") }} -> 1, 2, 3
    Used to generate comma arrays for charts such as mermaid xychart.
    """
    m = re.match(r'^\s*join\s*\((.*)\)\s*$', tag, re.S)
    if not m:
        return None
    args = _split_args(m.group(1))
    if len(args) < 2:
        return ''
    lst = _resolve(args[0], ctx)
    if not isinstance(lst, (list, tuple)):
        return ''
    sep = args[1]
    if len(sep) >= 2 and ((sep[0] == '"' and sep[-1] == '"') or (sep[0] == "'" and sep[-1] == "'")):
        sep = sep[1:-1]
    field = args[2] if len(args) > 2 else ''
    if len(field) >= 2 and ((field[0] == '"' and field[-1] == '"') or (field[0] == "'" and field[-1] == "'")):
        field = field[1:-1]
    items = []
    for it in lst:
        if not field or field == 'this':
            # None -> '0': for numeric arrays like mermaid xychart, avoid [1, , 3] syntax errors
            items.append('0' if it is None else str(it))
        else:
            v = _resolve(field, it)
            items.append('0' if v is None else str(v))
    return sep.join(items)


def _mermaid_id(val):
    """Generate a mermaid-safe node/task ID.

    - spaces -> underscore
    - dot (.) -> underscore (mermaid gantt/flowchart IDs may not contain '.',
      naively deleting the dot would lose hierarchy and could cause duplicate IDs / errors)
    - other irregular characters -> underscore
    - guaranteed non-empty (empty falls back to a stable node_<hash>), and not starting with a digit (prefixed '_')
    Example: {{ mid this.id }} -> SOW1_1 (input 'SOW1.1')
    """
    if val is None:
        return ''
    s = re.sub(r'\s+', '_', str(val).strip())
    # Keep: word characters \w (letters/digits/underscore, including Unicode letters such
    # as CJK) and the hyphen '-'; everything else (dots/punctuation) -> underscore.
    # Mermaid accepts Unicode node/task IDs, so we keep CJK and only convert '.' etc. to
    # '_' (also avoiding illegal gantt task ids).
    s = re.sub(r'[^\w-]', '_', s)
    if s == '' or s == '_':
        h = abs(hash(str(val))) % 1000000
        return f'node_{h:06d}'
    if s[0].isdigit():
        s = '_' + s
    return s


def _mermaid_label(val):
    """Mermaid label text (for use inside ["..."] / "...").

    - double quote '"' -> single quote "'" (avoids breaking the double-quoted string)
    - collapse consecutive whitespace/newlines into a single space and strip ends
    Example: {{ mlabel this.from }} -> Order Service (safe even if the original contains quotes/newlines)
    """
    if val is None:
        return ''
    s = str(val).replace('"', "'")
    # Note: '\n' is a literal backslash+n here and is not matched by \s, so newlines inside
    # a node are preserved
    s = re.sub(r'[ \t\r\f\v]+', ' ', s).strip()
    return s


def _gantt_name(val):
    """Gantt task display name (text before the ':' separator).

    In a gantt line `task name :taskId, start, end`, a colon inside the task name
    breaks the separator, so ':' is replaced with the full-width colon '\uFF1A';
    '&' is mermaid's same-line multi-task operator and must be escaped too, otherwise
    an unescaped '&' makes the parser treat subsequent tokens as dateless tasks ->
    'undefined.endTime' error. Label-safe handling (quotes/whitespace) is reused as well.
    """
    s = _mermaid_label(val)
    # In gantt, ':' is the task/ID separator and '&' is the same-line multi-task operator;
    # both break the label and must be escaped. '&' is replaced with the full-width
    # ampersand '\uFF06' (U+FF06): visually still '&' but not treated as an operator,
    # avoiding the 'undefined.endTime' error.
    s = s.replace(':', '\uFF1A').replace('&', '\uFF06')
    return s


def _severity_icon(val):
    """Map a severity to its canonical color word (green/yellow/orange/red), used for color-coded
    display in the risk register, etc.

    Accepts English bands (green/yellow/orange/red) or English levels (low/medium/high/critical).
    Unknown -> empty string.
    Example: {{ sev_icon this.severity }} -> red (input 'red' / 'critical')
    """
    if not val:
        return ''
    s = str(val).strip().lower()
    if s in ('green', 'low'):
        return 'green'
    if s in ('yellow', 'medium'):
        return 'yellow'
    if s in ('orange', 'high'):
        return 'orange'
    if s in ('red', 'critical'):
        return 'red'
    # substring fallback (e.g. "10 orange", "15 high")
    if 'green' in s:
        return 'green'
    if 'yellow' in s:
        return 'yellow'
    if 'orange' in s:
        return 'orange'
    if 'red' in s:
        return 'red'
    return ''


def _assume_text(val):
    """RAID assumption rendering helper: works with both dict ({text: ...}) and plain-string forms.

    Templates use {{ assume_text(this) }} to render assumption items, avoiding the dict being
    str()-ified into a JSON literal like "{'text': '...'}" that breaks document readability.
    Example: {'text': '<=1600 source table'} -> '<=1600 source table'; '<=1600 source table' -> '<=1600 source table'.
    """
    if isinstance(val, dict):
        return str(val.get('text', ''))
    if val is None:
        return ''
    return str(val)


def _slug_call(tag, ctx):
    """Backward-compatible legacy form: slug(x) / slug x is equivalent to mid(x) (mermaid-safe ID)."""
    m = re.match(r'^\s*slug\s*\((.*)\)\s*$', tag, re.S)
    if not m:
        m = re.match(r'^\s*slug\s+(.+?)\s*$', tag, re.S)
    if not m:
        return None
    return _mermaid_id(_resolve_or_literal(m.group(1).strip(), ctx))


def _severity_band_from_score(score):
    """Map a score to its canonical color word via the 5x5 calibration matrix (fallback when severity is absent).

    Color bands: green 1-4 | yellow 5-9 | orange 10-15 | red 16-25.
    Unparseable -> empty string.
    """
    if score is None:
        return ''
    try:
        sc = float(str(score).strip())
    except (ValueError, AttributeError):
        return ''
    if sc <= 4:
        return 'green'
    if sc <= 9:
        return 'yellow'
    if sc <= 15:
        return 'orange'
    return 'red'


def _severity_cell(sev, score=None):
    """Prefer the explicit severity color; fall back to score-derived band when absent,
    so the color indicator is always shown.

    Usage: {{ sev_cell this.severity this.score }} -> red
    """
    icon = _severity_icon(sev)
    if icon:
        return icon
    return _severity_band_from_score(score)


def _call_helper(tag, ctx):
    """Dispatch known helper function calls: slug / mid / mlabel / gname / join.

    Returning None means this is not a recognized helper call (handed to general variable evaluation).
    """
    m = re.match(r'^\s*(\w+)\s*\((.*)\)\s*$', tag, re.S)
    if m:
        name = m.group(1)
        arg = m.group(2).strip()
        if name in ('slug', 'mid'):
            return _mermaid_id(_resolve_or_literal(arg, ctx))
        if name == 'mlabel':
            return _mermaid_label(_resolve_or_literal(arg, ctx))
        if name == 'gname':
            return _gantt_name(_resolve_or_literal(arg, ctx))
        if name in ('sev_icon', 'risk_icon'):
            return _severity_icon(_resolve_or_literal(arg, ctx))
        if name in ('sev_cell', 'sev_band'):
            # sev_cell(severity, score) / sev_band(score) -- supports comma or space separation
            inner = re.match(r'^\s*(.*?)\s*[,\s]\s*(.*)\s*$', arg, re.S)
            if name == 'sev_band':
                return _severity_band_from_score(_resolve_or_literal(arg, ctx))
            if inner and inner.group(2).strip():
                a = _resolve_or_literal(inner.group(1).strip(), ctx)
                b = _resolve_or_literal(inner.group(2).strip(), ctx)
                return _severity_cell(a, b)
            return _severity_cell(_resolve_or_literal(arg, ctx), None)
        if name == 'join':
            return _join_call(tag, ctx)
        if name == 'assume_text':
            return _assume_text(_resolve_or_literal(arg, ctx))
        if name == 'eq':
            # eq(a, b) or eq a b -> returns b's literal (truthy) when equal, else '' (falsy), for {{#if (eq ..)}}
            a_raw, b_raw = None, None
            inner = re.match(r'^\s*(.*?)\s*,\s*(.*)\s*$', arg, re.S)
            if inner:
                a_raw, b_raw = inner.group(1).strip(), inner.group(2).strip()
            else:
                # space-separated (also accepts quote-wrapped literals): eq granularity "fortnight"
                m2 = re.match(r'^\s*(\S+)\s+"([^"]*)"\s*$', arg, re.S)
                if m2:
                    a_raw, b_raw = m2.group(1).strip(), '"' + m2.group(2) + '"'
                else:
                    parts = arg.split(None, 1)
                    if len(parts) == 2:
                        a_raw, b_raw = parts[0].strip(), parts[1].strip()
            if a_raw is not None and b_raw is not None:
                a = _resolve_or_literal(a_raw, ctx)
                b = _resolve_or_literal(b_raw, ctx)
                return b if str(a) == str(b) else ''
            return ''
        return None
    # Backward-compatible bracket-less forms from doc examples: {{ slug this.from }} and {{ eq a b }}
    if tag.startswith('slug '):
        return _slug_call(tag, ctx)
    if tag.startswith('eq '):
        inner = tag[3:].strip()
        # convert to eq(a, b) form and re-enter parsing (supports quoted literals)
        m2 = re.match(r'^(\S+)\s+"([^"]*)"\s*$', inner, re.S)
        if m2:
            return _call_helper('eq(%s, "%s")' % (m2.group(1), m2.group(2)), ctx)
        parts = inner.split(None, 1)
        if len(parts) == 2:
            return _call_helper('eq(%s, %s)' % (parts[0], parts[1].strip('"')))
        return ''
    return None


# ---------- Block matching ----------
def _find_block(text, start, open_marker, close_marker):
    """From start, find the close_marker matching open_marker; return (inner text, index after close)."""
    depth = 1
    i = start
    L = len(text)
    while i < L and depth > 0:
        oi = text.find(open_marker, i)
        ci = text.find(close_marker, i)
        if ci == -1:
            raise ValueError(f"Unmatched block marker: {open_marker}")
        if oi != -1 and oi < ci:
            depth += 1
            i = oi + len(open_marker)
        else:
            depth -= 1
            i = ci + len(close_marker)
            if depth == 0:
                return text[start:ci], i
    return text[start:i], i


def _split_else(body):
    """Within a #if body, find the top-level (depth==1) {{else}} or {{#else}} as the then/else boundary.

    The two forms are equivalent: {{else}} and {{#else}}.
    """
    depth = 1
    i = 0
    L = len(body)
    while i < L:
        oi = body.find('{{#if ', i)
        oe = body.find('{{#each ', i)
        e1 = body.find('{{else}}', i)
        e2 = body.find('{{#else}}', i)
        ci = body.find('{{/if}}', i)
        ce = body.find('{{/each}}', i)
        cands = []
        if oi != -1:
            cands.append((oi, 'if'))
        if oe != -1:
            cands.append((oe, 'each'))
        if e1 != -1:
            cands.append((e1, 'else'))
        if e2 != -1:
            cands.append((e2, 'else2'))
        if ci != -1:
            cands.append((ci, 'ifc'))
        if ce != -1:
            cands.append((ce, 'eachc'))
        if not cands:
            break
        p, t = min(cands)
        if t == 'if':
            depth += 1; i = p + 6
        elif t == 'each':
            depth += 1; i = p + 8
        elif t == 'ifc':
            depth -= 1; i = p + 7
        elif t == 'eachc':
            depth -= 1; i = p + 9
        elif t in ('else', 'else2'):
            marker_len = len('{{else}}') if t == 'else' else len('{{#else}}')
            if depth == 1:
                return body[:p], body[p + marker_len:]
            i = p + marker_len
    return body, ''


# ---------- Recursive rendering ----------
def _parse(text, ctx):
    out = []
    i = 0
    L = len(text)
    while i < L:
        idx = text.find('{{', i)
        if idx == -1:
            out.append(text[i:]); break
        out.append(text[i:idx])
        end = text.find('}}', idx)
        if end == -1:
            out.append(text[idx:]); break
        tag = text[idx + 2:end].strip()
        if tag.startswith('#each '):
            expr = tag[6:].strip()
            body, ni = _find_block(text, end + 2, '{{#each ', '{{/each}}')
            val = _eval(expr, ctx)
            chunk = []
            if isinstance(val, (list, tuple)):
                n = len(val)
                for idx, item in enumerate(val):
                    sub = dict(ctx)
                    sub['this'] = item
                    sub['@index'] = idx
                    sub['@first'] = (idx == 0)
                    sub['@last'] = (idx == n - 1)
                    rendered = _parse(body, sub)
                    # strip leading/trailing newlines to avoid blank lines between consecutive rows
                    stripped = rendered.lstrip('\n').rstrip('\n')
                    # only add a newline when the loop body itself contains newlines (e.g. table rows);
                    # inline each (e.g. gantt dependency chains) keeps the same line intact.
                    chunk.append(stripped + '\n' if '\n' in rendered else stripped)
            out.append(''.join(chunk))
            i = ni
        elif tag.startswith('#if '):
            expr = tag[4:].strip()
            body, ni = _find_block(text, end + 2, '{{#if ', '{{/if}}')
            then_b, else_b = _split_else(body)
            branch = then_b if _truthy(_eval(expr, ctx)) else else_b
            out.append(_parse(branch, ctx))
            i = ni
        else:
            res = _call_helper(tag, ctx)
            if res is not None:
                out.append(res)
            else:
                val = _eval(tag, ctx)
                if isinstance(val, list):
                    val = ', '.join(str(x) for x in val)
                out.append('' if val is None else str(val))
            i = end + 2
    return ''.join(out)


def _truthy(v):
    if isinstance(v, (list, dict, str)):
        return len(v) > 0
    return bool(v)


def render(text, data):
    return _parse(text, data if isinstance(data, dict) else {})


# ---------- CLI ----------
def load_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    if path.endswith(('.yaml', '.yml')):
        if yaml is None:
            raise SystemExit("PyYAML is required: run `pip install pyyaml`")
        return yaml.safe_load(raw)
    return __import__('json').loads(raw)


def main():
    ap = argparse.ArgumentParser(description="PM Master template rendering engine")
    ap.add_argument('--template', required=True, help="Path to the .md template")
    ap.add_argument('--data', required=True, help="Path to the data .yaml/.json")
    ap.add_argument('--out', required=True, help="Output .md path")
    args = ap.parse_args()

    with open(args.template, 'r', encoding='utf-8') as f:
        tpl = f.read()
    data = load_data(args.data)
    result = render(tpl, data)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"[render] {args.template} + {args.data}  ->  {args.out}  ({len(result)} chars)")


if __name__ == '__main__':
    main()
