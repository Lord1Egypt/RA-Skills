#!/usr/bin/env python3
"""
dispatch.py — Discrete Hamiltonian Path Dispatcher with Sparse Matrices

Uses scipy.sparse for efficient storage and computation on large graphs.
All commands are identical to dispatch.py.

Usage:
  python dispatch.py <triples_file> query <current> <target> <logical_budget>
  python dispatch.py <triples_file> path   <start>    <end>
  python dispatch.py <triples_file> matrix
  python dispatch.py <triples_file> deps   <node>
 cache: Automatically save (names, idx, A, orig_n, dist) to .cache. If the modification time of the source file is less than or equal to the cache file time, skip the pre-computation. Setting the environment variable PATH_DISPATCH_NO_CACHE=1 can disable caching.
 
Import:
    from path_dispatch import parse_triples, build_graph(...)

    import path_dispatch
path_dispatch.parse_triples(...)
"""

import sys
import os
from collections import deque
import numpy as np
import scipy.sparse as sp

# ---------- Parsing (same as before) ----------
def parse_list(s):
    s = s.strip()
    if s.startswith('[') and s.endswith(']'):
        inner = s[1:-1].strip()
        return [x.strip() for x in inner.split(',')] if inner else []
    return [s]

def smart_split(content):
    parts, current, depth = [], [], 0
    for ch in content:
        if ch == ',' and depth == 0:
            parts.append(''.join(current).strip())
            current = []
        else:
            if ch == '[': depth += 1
            elif ch == ']': depth -= 1
            current.append(ch)
    if current:
        parts.append(''.join(current).strip())
    return parts if len(parts) == 3 else None

def parse_triples(filepath):
    triples = []
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not (line.startswith('<<{') and line.endswith('}.')):
                continue
            content = line[3:-2]
            parts = smart_split(content)
            if not parts:
                continue
            s_str, p_str, o_str = parts
            triples.append((parse_list(s_str), p_str, parse_list(o_str)))
    return triples

# ---------- Graph building (unchanged) ----------
def build_graph(triples):
    orig_set = set()
    for s_list, _, o_list in triples:
        for n in s_list:
            orig_set.add(n)
        for n in o_list:
            orig_set.add(n)
    orig_nodes = sorted(orig_set)
    idx = {n: i for i, n in enumerate(orig_nodes)}
    orig_n = len(orig_nodes)
    total_nodes = orig_n + len(triples)

    A = sp.lil_matrix((total_nodes, total_nodes), dtype=bool)
    for rel_id, (s_list, _, o_list) in enumerate(triples):
        v_node = orig_n + rel_id
        for s in s_list:
            A[idx[s], v_node] = True
        for o in o_list:
            A[v_node, idx[o]] = True
    A = A.tocsr()
    names = orig_nodes + [f"__rel_{i}__" for i in range(len(triples))]
    return names, idx, A, orig_n

# ---------- All-pairs shortest paths (BFS from each node) ----------
def all_pairs_shortest_paths(A, n):
    """
    Returns distance matrix dist (n x n) where dist[i][j] is shortest path
    length (physical steps) from i to j, or n+1 if unreachable.
    """
    INF = n + 1
    dist = np.full((n, n), INF, dtype=np.int16)
    for s in range(n):
        dist[s, s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            # iterate over neighbors (successors)
            for v in A[u].nonzero()[1]:
                if dist[s, v] > dist[s, u] + 1:
                    dist[s, v] = dist[s, u] + 1
                    q.append(v)
    return dist

# ---------- Query functions ----------
def next_hops(v, T_phys, phys_budget, A, dist, n):
    if phys_budget <= 0:
        return []
    neighbors = A[v].nonzero()[1]
    res = []
    for w in neighbors:
        # distance from v to w is exactly 1 (direct edge)
        # but we use dist[v,w] for generality
        d_vw = dist[v, w]  # should be 1
        d_wT = dist[w, T_phys]
        if d_vw + d_wT <= phys_budget:
            res.append(w)
    return res

def bfs_shortest_path(start_phys, end_phys, A, n, orig_n, names):
    """BFS used for `path` command to reconstruct the actual path."""
    if start_phys == end_phys:
        return ([names[start_phys]], 0)
    queue = deque([(start_phys, [start_phys])])
    visited = {start_phys}
    while queue:
        node, path = queue.popleft()
        for w in A[node].nonzero()[1]:
            if w not in visited:
                new_path = path + [w]
                if w == end_phys:
                    logical_path = [names[p] for p in new_path if p < orig_n]
                    logical_hops = (len(new_path) - 1) // 2
                    return logical_path, logical_hops
                visited.add(w)
                queue.append((w, new_path))
    return None, -1

# ---------- Command handlers ----------
def cmd_matrix(names, A, dist, orig_n):
    total_n = len(names)
    print("=== Original Nodes ===")
    for i in range(orig_n):
        print(f"  {i:3d}  {names[i]}")
    print(f"\n=== Virtual Nodes ({total_n - orig_n}) ===")
    for i in range(orig_n, total_n):
        print(f"  {i:3d}  {names[i]}")
    # Convert to dense for display (only if total_n manageable)
    print("\n=== Adjacency Matrix (A) ===")
    A_dense = A.toarray().astype(int)
    header = "     " + " ".join(f"{i:2d}" for i in range(total_n))
    print(header)
    for i, row in enumerate(A_dense):
        bits = " ".join(" 1" if v else " 0" for v in row)
        print(f"{i:3d}  {bits}   {names[i]}")
    # Optionally show distance matrix summary (too large maybe)
    print(f"\nNodes: {total_n}  |  Distance matrix computed (shape {dist.shape})")

def cmd_path(start_name, end_name, names, idx, A, orig_n):
    if start_name not in idx or end_name not in idx:
        print("Unknown node.")
        return
    s, e = idx[start_name], idx[end_name]
    total_n = len(names)
    logical_path, logical_hops = bfs_shortest_path(s, e, A, total_n, orig_n, names)
    if logical_path is None:
        print(f"No path from '{start_name}' to '{end_name}'")
    else:
        print(f"Shortest logical path ({logical_hops} hops):")
        print("  " + " → ".join(logical_path))

def cmd_query(current_name, target_name, logical_budget, names, idx, A, dist, orig_n):
    if current_name not in idx or target_name not in idx:
        print("Unknown node.")
        return
    v, T = idx[current_name], idx[target_name]
    total_n = len(names)
    phys_budget = 2 * logical_budget
    result = next_hops(v, T, phys_budget, A, dist, total_n)
    readable = []
    for w in result:
        if w >= orig_n:
            targets = [names[t] for t in range(orig_n) if A[w, t]]
            if len(targets) == 1:
                readable.append(targets[0])
            else:
                readable.append("{" + ", ".join(targets) + "}")
        else:
            readable.append(names[w])
    print(f"next_hops(current={current_name}, target={target_name}, logical_budget={logical_budget})")
    if not result:
        print("  ∅")
    else:
        print("  →", readable)

def cmd_deps(node_name, names, idx, triples, orig_n):
    if node_name not in idx:
        print(f"Unknown node: {node_name}")
        return
    deps = []
    for s_list, pred, o_list in triples:
        if node_name in o_list:
            if len(s_list) == 1:
                source_str = s_list[0]
            else:
                source_str = "{" + ", ".join(s_list) + "}"
            deps.append((source_str, pred))
    if not deps:
        print(f"No direct dependencies for '{node_name}'")
    else:
        print(f"Dependencies for '{node_name}':")
        for src, pred in deps:
            print(f"  from {src} via '{pred}'")

def usage():
    print(__doc__)
    sys.exit(1)

def main():
    import pickle
    if len(sys.argv) < 3:
        usage()
    filepath = sys.argv[1]
    command = sys.argv[2]
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    cache_path = filepath + ".cache"
    no_cache = os.environ.get("PATH_DISPATCH_NO_CACHE", "0") == "1"
    use_cache = (not no_cache) and os.path.exists(cache_path) and \
                os.path.getmtime(cache_path) >= os.path.getmtime(filepath)

    triples = None
    names = idx = A = orig_n = dist = None

    if use_cache:
        try:
            with open(cache_path, "rb") as f:
                names, idx, A, orig_n, dist = pickle.load(f)
            # Validate dist dimensions
            total_n = len(names)
            if dist.shape != (total_n, total_n):
                raise ValueError("Invalid dist shape")
        except Exception as e:
            print(f"Cache load failed: {e}. Rebuilding...", file=sys.stderr)
            use_cache = False

    if (not use_cache) or command == "deps":
        triples = parse_triples(filepath)
        if not triples:
            print("No triples found.")
            sys.exit(1)

    if not use_cache:
        names, idx, A, orig_n = build_graph(triples)
        total_n = len(names)
        print("Precomputing all-pairs shortest paths...", file=sys.stderr)
        dist = all_pairs_shortest_paths(A, total_n)
        try:
            with open(cache_path, "wb") as f:
                pickle.dump((names, idx, A, orig_n, dist), f)
        except Exception as e:
            print(f"Cache save failed: {e}", file=sys.stderr)

    total_n = len(names)

    if command == "matrix":
        cmd_matrix(names, A, dist, orig_n)
    elif command == "path":
        if len(sys.argv) < 5:
            usage()
        cmd_path(sys.argv[3], sys.argv[4], names, idx, A, orig_n)
    elif command == "query":
        if len(sys.argv) < 6:
            usage()
        cmd_query(sys.argv[3], sys.argv[4], int(sys.argv[5]), names, idx, A, dist, orig_n)
    elif command == "deps":
        if len(sys.argv) < 4:
            usage()
        cmd_deps(sys.argv[3], names, idx, triples, orig_n)
    else:
        usage()

if __name__ == "__main__":
    main()