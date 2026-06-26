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