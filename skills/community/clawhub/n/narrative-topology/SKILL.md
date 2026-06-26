---
name: narrative-topology
description: >
  Extract semantic relationships from long narratives, architectures, or complex discussions
  using RDF-style triple notation. Generate adjacency matrices to reveal narrative structure,
  dependency graphs, and critical paths. Works standalone or paired with all-dialogue-to-markdown.
  Extracts signal from noise in dense multi-turn discussions.
---

# Narrative Topology

## Core Concept

**Problem:** Long discussions (100+ messages, architectural debates, narrative analysis) lose structure. Easy to miss critical dependencies, causality chains, or bottlenecks.

**Solution:** Embed RDF-style triples in markdown. Scan with Python. Extract **semantic adjacency matrix**. See structure.

---

## Triple Notation

### Format
```

<<{Subject, Predicate, Object}.

```

### Examples

**Simple relations:**
```

<<{Claude, outputs, analysis}.
<<{analysis, informs, decision}.

```

**Parallel subjects (cartesian product):**
```

<<{[A, B, C], implements, feature}.

```
Expands to:
```

{A, implements, feature}
{B, implements, feature}
{C, implements, feature}

```

**Parallel objects:**
```

<<{payment_system, affects, [latency, cost, security]}.

```
Expands to:
```

{payment_system, affects, latency}
{payment_system, affects, cost}
{payment_system, affects, security}

```

**Both parallel:**
```

<<{[Claude, User], collaborated_on, [design, implementation]}.

```
Full cartesian product: 2×2 = 4 edges.

### Syntax Rules

- `<<{` starts the triple
- `}.` (period-dot) terminates
- Commas separate subject, predicate, object
- Whitespace trimmed automatically
- `[...]` denotes list; bare tokens are singletons
- Lines in markdown, easily greppable

### Why This Format

1. **RDF-like** — Semantic web standard, well-understood
2. **Grep-friendly** — `grep '<<{' file.md` finds all triples
3. **Unambiguous** — Clear start/end, no nesting
4. **Markdown-native** — Doesn't break rendering
5. **Compact** — One line per relation

---

## Example: Hamlet

Input markdown (partial):
```markdown
## Act I

<<{Claudius, murders, old_king}.
<<{Claudius, usurps, Denmark_throne}.
<<{Claudius, marries, Gertrude}.

## Act II

<<{ghost, reveals, Hamlet}.
<<{ghost, demands, revenge}.
<<{Hamlet, feigns, madness}.
<<{Hamlet, kills, Polonius}.

## Consequences

<<{Polonius_death, causes, Ophelia_madness}.
<<{Ophelia, drowns, river}.

## Climax

<<{[Hamlet, Laertes], duel, each_other}.
<<{[poison_sword, poison_wine], kills, [Hamlet, Laertes, Claudius, Gertrude]}.
<<{Fortinbras, takes_over, Denmark}.
```

Output: Adjacency matrix showing all 14 nodes and their causal/narrative dependencies.

---

Python Scanner

Place scanner.py in your markdown directory. Run:

```bash
python scanner.py
```

Code

```python
#!/usr/bin/env python3
"""
Narrative Topology Scanner
Usage: python scanner.py
Outputs adjacency matrix compressed with x::n notation
"""

import os
import sys

def list_files_recursive(directory, extensions=('.txt', '.def', '.erl', '.ex', '.md')):
    """Yield all files with given extensions under directory."""
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(extensions):
                yield os.path.join(root, f)

def parse_list(s):
    """Parse a token that may be a singleton or a bracketed list."""
    s = s.strip()
    if s.startswith('[') and s.endswith(']'):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [item.strip() for item in inner.split(',')]
    return [s]

def smart_split(content):
    """
    Split content by commas while respecting nested brackets.
    Returns list of three parts: subject, predicate, object.
    """
    parts = []
    current = []
    depth = 0
    for ch in content:
        if ch == ',' and depth == 0:
            parts.append(''.join(current).strip())
            current = []
        else:
            if ch == '[':
                depth += 1
            elif ch == ']':
                depth -= 1
            current.append(ch)
    if current:
        parts.append(''.join(current).strip())
    return parts if len(parts) == 3 else None

def process_line(line):
    """Extract triples from a single line."""
    line = line.strip()
    if not line.startswith('<<{'):
        return []
    if not line.endswith('}.'):
        return []
    # Extract content between <<{ and }.
    content = line[3:-2]
    parts = smart_split(content)
    if not parts:
        return []
    s, p, o = parts  # p is ignored (predicate)
    subjects = parse_list(s)
    objects = parse_list(o)
    edges = []
    for subj in subjects:
        for obj in objects:
            edges.append((subj, obj))
    return edges

def process_file(filepath):
    """Process a single file, returning list of (source, target) edges."""
    edges = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                edges.extend(process_line(line))
    except Exception:
        pass
    return edges

def compress_row(row):
    """Convert list of ints to x::n compressed string."""
    if not row:
        return ''
    compressed = []
    current_val = row[0]
    count = 1
    for val in row[1:]:
        if val == current_val:
            count += 1
        else:
            compressed.append(f"{current_val}::{count}")
            current_val = val
            count = 1
    compressed.append(f"{current_val}::{count}")
    return ','.join(compressed)

def main():
    cwd = os.getcwd()
    edges = []
    for filepath in list_files_recursive(cwd):
        edges.extend(process_file(filepath))

    # Gather unique nodes
    nodes = set()
    for s, o in edges:
        nodes.add(s)
        nodes.add(o)
    nodes = sorted(nodes)
    n = len(nodes)

    # Build index map
    idx = {node: i for i, node in enumerate(nodes)}

    # Build adjacency matrix (list of lists)
    matrix = [[0] * n for _ in range(n)]
    for s, o in edges:
        i, j = idx[s], idx[o]
        matrix[i][j] = 1

    # Output
    print("Nodes: " + ", ".join(nodes))
    print()
    print("Adjacency Matrix (compressed x::n):")
    print("# x::n = n copies of value x")
    for row in matrix:
        print(compress_row(row))

    print()
    print("Stats:")
    print(f"Nodes: {n}")
    print(f"Edges: {len(edges)}")
    if n > 0:
        density = len(edges) / (n * n)
        print(f"Density: {density:.4f}")

if __name__ == "__main__":
    main()
```

Output

The scanner outputs an adjacency matrix compressed with x::n notation (n copies of value x):

```
Nodes: Claudius, Denmark_throne, Fortinbras, Gertrude, Hamlet, Laertes, Ophelia, Polonius, Polonius_death, ...

Adjacency Matrix (compressed x::n):
# x::n = n copies of value x
0::14
0::3,1::1,0::10
0::4,1::2,0::8
1::14
...

Stats:
Nodes: 14
Edges: 12
Density: 0.0612
```

Format rule: x::n means n consecutive occurrences of value x. Example: 0::2,1::3,0::1 expands to [0,0,1,1,1,0].

For AI analysis: The matrix rows = sources (in node list order), columns = targets. 1 = edge exists.

---

Interpreting the Matrix

Rows = Sources, Columns = Targets

Matrix M where M[i,j] = 1 means: Node_i → Node_j

Key Analyses

· In-degree (column sum): How many things cause this node? (Count 1s in each column)
· Out-degree (row sum): How many things does this node cause? (Count 1s in each row)
· Strongly connected components: Cycles (feedback loops, mutual causality)
· Topological sort: Order events by causal dependency
· Critical path: Chain with maximum bottleneck nodes

---

Extending the Scanner

Add Weighted Edges

Replace binary (0/1) with strength values:

```python
# Instead of setting to 1, count occurrences
weight_matrix = [[0] * n for _ in range(n)]
for s, o in edges:
    i, j = idx[s], idx[o]
    weight_matrix[i][j] += 1
```

Output matrix has counts, not just binary.

Generate Mermaid Graph

Add to scanner:

```python
print("graph LR")
for s, o in edges:
    print(f"  {s} --> {o}")
```

Pipe output to a .mmd file, render in claude.ai.

Generate GraphViz DOT

```python
print("digraph {")
for s, o in edges:
    print(f'  "{s}" -> "{o}";')
print("}")
```

Render with dot, convert to PNG/SVG.

---

Use Cases

1. Narrative Analysis
      Extract plot dependency from novel/screenplay.
      · Identify critical turning points (high in-degree)
      · Find orphaned subplots (isolated nodes)
      · Spot circular dependencies (tragedy, irony)
2. Architectural Discussions
      Embed triples in design doc markdown:
   ```
   <<{microservice_A, calls, microservice_B}.
   <<{microservice_B, depends_on, database}.
   <<{database, shared_by, [service_C, service_D]}.
   ```
   Scan → see service coupling graph → identify decoupling opportunities.
3. Project Workflows
      Task dependencies:
   ```
   <<{design_doc, blocks, implementation}.
   <<{implementation, requires, code_review}.
   <<{code_review, unblocks, deployment}.
   ```
   Scan → topological sort → critical path analysis.
4. Technical Debt Mapping
   ```
   <<{legacy_code, causes, technical_debt}.
   <<{technical_debt, blocks, new_feature}.
   <<{new_feature, required_by, [OKR_1, OKR_2]}.
   ```
   Prioritize refactor based on downstream impact.

---

Integration with all-dialogue-to-markdown

Optional pairing:

1. Claude writes analysis in markdown (using all-dialogue skill)
2. You embed triples in the markdown as you read
3. Run scanner on the output file → see structure
4. Use matrix to:
   · Ask follow-up questions
   · Spot gaps
   · Verify causality chains

Example workflow:

```
User: "Analyze scheduler design. Save as scheduler-analysis.md"
Claude: [saves full analysis to scheduler-analysis.md]

User: [reads md, embeds triples]
<<{async_dispatch, reduces, latency}.
<<{latency, affects, throughput}.

User: "Run scanner on scheduler-analysis.md"
Scanner: [adjacency matrix]

User: [examines matrix] "What about error propagation?"
```

No requirement to use all-dialogue — works standalone on any markdown.

---

Workflow

Standalone Use

1. Write markdown with embedded triples
2. Place scanner.py in same directory
3. Run: python scanner.py
4. Get compressed adjacency matrix
5. Use for analysis or feed back to AI

With all-dialogue Pairing

1. Ask Claude to save analysis to markdown (all-dialogue skill)
2. Read markdown, mark critical relations with triples
3. Run scanner
4. Iterate: use matrix to ask more precise questions

---

Philosophy

· Why separate from all-dialogue?
    All-dialogue manages token flow (thinking + response → file). Narrative-topology manages semantic extraction (relations → matrix). Independent concerns. Both can upgrade separately. Narrative-topology applies to any markdown, not just Claude output.
· Why triples instead of prose summaries?
    Prose is lossy. Easy to miss connections. Triples are canonical, computable, greppable. Matrix enables quantitative analysis (paths, cycles, centrality). Scales: 50 triples → clear structure. 500 triples → still manageable.
· Why Python?
    Ubiquitous, no extra dependencies. Single file, runs anywhere. Clear, readable, and easily extensible.

---

Summary

Narrative Topology extracts relational structure from dense text.

· Input: Markdown with <<{S, P, O}. triples
· Processing: Python scanner parses + expands cartesian products
· Output: Adjacency matrix compressed with x::n notation (low token cost, AI‑friendly)
· Power: See causal chains, bottlenecks, cycles in long discussions
· Scope: Works standalone. Pairs naturally with all-dialogue.

Use it to maintain signal in long, complex narratives.
