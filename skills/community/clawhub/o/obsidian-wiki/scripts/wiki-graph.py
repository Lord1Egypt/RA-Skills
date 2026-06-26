#!/usr/bin/env python3
"""wiki-graph.py — Export the wiki wikilink graph as JSON or GraphML.

Builds a node+edge graph from wikilinks across all wiki pages and writes it
to .wiki-meta/graph.json (default) or .wiki-meta/graph.graphml.

Usage:
  python3 wiki-graph.py <vault-path>                       # JSON → .wiki-meta/graph.json
  python3 wiki-graph.py <vault-path> --format graphml      # GraphML → .wiki-meta/graph.graphml
  python3 wiki-graph.py <vault-path> --stats               # print hub/orphan analysis
  python3 wiki-graph.py <vault-path> --format graphml --stats
  python3 wiki-graph.py <vault-path> --help

Stats include:
  total nodes, total edges, avg degree, top 10 hubs,
  orphans (no links in or out), articulation points (removal increases connected components)
"""
import os, sys, json, re, tempfile
from collections import defaultdict

# Ensure wiki_lib is importable from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wiki_lib import WikiMap, read_md, frontmatter_re

# ── Argument parsing ──────────────────────────────────────

if "--help" in sys.argv or "-h" in sys.argv:
    print("Usage: python3 wiki-graph.py <vault-path> [--format json|graphml] [--stats]")
    print("Export the wiki wikilink graph.")
    print("  --format json     Output JSON to .wiki-meta/graph.json (default)")
    print("  --format graphml  Output GraphML to .wiki-meta/graph.graphml")
    print("  --stats           Print hub/orphan/articulation point analysis to stdout")
    sys.exit(0)

vault = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else None
if not vault:
    print("Usage: python3 wiki-graph.py <vault-path> [--format json|graphml] [--stats]",
          file=sys.stderr)
    sys.exit(2)

_known_flags = {"--format", "--stats", "--help", "-h"}
fmt = "json"
stats_mode = "--stats" in sys.argv

args = sys.argv[2:]
i = 0
while i < len(args):
    if args[i] == "--format":
        if i + 1 >= len(args):
            print("Error: --format requires a value (json or graphml)", file=sys.stderr)
            sys.exit(2)
        fmt = args[i + 1].lower()
        if fmt not in ("json", "graphml"):
            print(f"Error: unknown format '{fmt}'. Use json or graphml.", file=sys.stderr)
            sys.exit(2)
        i += 2
    elif args[i] in ("--stats", "--help", "-h"):
        i += 1
    elif args[i].startswith("-"):
        print(f"Error: unknown option '{args[i]}'", file=sys.stderr)
        sys.exit(2)
    else:
        i += 1

wiki_dir = os.path.join(vault, "wiki")
if not os.path.isdir(wiki_dir):
    print(f"Error: {wiki_dir} not found", file=sys.stderr)
    sys.exit(2)

# ── Build maps ────────────────────────────────────────────

wm = WikiMap(vault)

# Warn about duplicate basenames (graph keyed by basename)
for dup_bn in sorted(wm._ambiguous_basenames):
    print(f"WARNING: duplicate basename '{dup_bn}' — graph node may be inaccurate", file=sys.stderr)

# Gather node metadata (type and tags from frontmatter)
node_meta = {}  # basename → {type, tags}
_type_re = re.compile(r"^type:\s*['\"]?(\S+?)['\"]?\s*$", re.MULTILINE)
_tags_re = re.compile(r"^tags:\s*\[(.+?)\]\s*$", re.MULTILINE)
for md in wm.content_pages():
    bn = os.path.splitext(os.path.basename(md))[0]
    content = read_md(md)
    node_type = "unknown"
    node_tags = []
    if content:
        fm_match = frontmatter_re.match(content)
        if fm_match:
            fm = fm_match.group(1)
            mt = _type_re.search(fm)
            if mt:
                node_type = mt.group(1)
            mg = _tags_re.search(fm)
            if mg:
                node_tags = [t.strip().strip("'\"") for t in mg.group(1).split(",") if t.strip()]
    node_meta[bn] = {"type": node_type, "tags": node_tags}

# ── Build graph ───────────────────────────────────────────

# edges: list of (source_bn, target_bn)
edges_set = set()
links_out = defaultdict(int)   # source → count
links_in  = defaultdict(int)   # target → count

for md in wm.content_pages():
    src_bn = os.path.splitext(os.path.basename(md))[0]
    for target in wm.extract_links(md):
        status, resolved = wm.resolve_target(target)
        if resolved and status not in ("broken", "ambiguous"):
            if src_bn != resolved:
                edge = (src_bn, resolved)
                if edge not in edges_set:
                    edges_set.add(edge)
                    links_out[src_bn] += 1
                    links_in[resolved] += 1

# Ensure all known pages appear as nodes (even with no links)
all_nodes = set(wm.known_files) - {"index", "log"}

# ── Build output structures ───────────────────────────────

nodes = []
for bn in sorted(all_nodes):
    meta = node_meta.get(bn, {"type": "unknown", "tags": []})
    nodes.append({
        "id":       bn,
        "title":    wm.file_to_title.get(bn, bn),
        "type":     meta["type"],
        "tags":     meta["tags"],
        "links_out": links_out[bn],
        "links_in":  links_in[bn],
    })

edges = [{"source": s, "target": t, "weight": 1} for s, t in sorted(edges_set)]

# ── Stats computation ─────────────────────────────────────

def _compute_stats(edges, all_nodes):
    n = len(all_nodes)
    e = len(edges)
    avg_degree = (2 * e / n) if n > 0 else 0.0

    # Derive link counts from edges (pure — no globals)
    _links_out = defaultdict(int)
    _links_in  = defaultdict(int)
    degree     = defaultdict(int)  # undirected for hub ranking
    for edge in edges:
        _links_out[edge["source"]] += 1
        _links_in[edge["target"]] += 1
        degree[edge["source"]] += 1
        degree[edge["target"]] += 1

    top_hubs = sorted(all_nodes, key=lambda bn: degree[bn], reverse=True)[:10]

    orphans = sorted(
        bn for bn in all_nodes
        if _links_out[bn] == 0 and _links_in[bn] == 0
    )

    # Articulation point detection via Tarjan's algorithm — O(V+E)
    adj = defaultdict(set)
    for edge in edges:
        adj[edge["source"]].add(edge["target"])
        adj[edge["target"]].add(edge["source"])

    _disc = {}
    _low = {}
    _parent = {}
    _ap_set = set()
    _timer = [0]

    def _tarjan_iterative(root):
        """Iterative Tarjan's articulation point detection (avoids RecursionError)."""
        # Stack entries: (node, neighbor_iterator, children_count)
        _parent[root] = None
        _disc[root] = _low[root] = _timer[0]
        _timer[0] += 1
        stack = [(root, iter(sorted(adj[root])), 0)]
        while stack:
            u, neighbors, children = stack[-1]
            try:
                v = next(neighbors)
                if v not in _disc:
                    children += 1
                    stack[-1] = (u, neighbors, children)
                    _parent[v] = u
                    _disc[v] = _low[v] = _timer[0]
                    _timer[0] += 1
                    stack.append((v, iter(sorted(adj[v])), 0))
                elif v != _parent.get(u):
                    _low[u] = min(_low[u], _disc[v])
            except StopIteration:
                stack.pop()
                if stack:
                    parent_u = stack[-1][0]
                    _low[parent_u] = min(_low[parent_u], _low[u])
                    # Check articulation point conditions
                    p_node, p_neighbors, p_children = stack[-1]
                    if _parent.get(p_node) is None and p_children > 1:
                        _ap_set.add(p_node)
                    if _parent.get(p_node) is not None and _low[u] >= _disc[p_node]:
                        _ap_set.add(p_node)

    # Handle disconnected components
    for node in sorted(all_nodes):
        if node not in _disc:
            _tarjan_iterative(node)

    articulation_points = sorted(_ap_set)

    return {
        "total_nodes": n,
        "total_edges": e,
        "avg_degree":  round(avg_degree, 2),
        "top_hubs":    top_hubs,
        "orphans":     orphans,
        "articulation_points": articulation_points,
    }

stats = _compute_stats(edges, all_nodes)

# ── JSON output ───────────────────────────────────────────

def _write_json(vault, nodes, edges, stats):
    meta_dir = os.path.join(vault, ".wiki-meta")
    os.makedirs(meta_dir, exist_ok=True)
    out_path = os.path.join(meta_dir, "graph.json")
    payload = {"nodes": nodes, "edges": edges, "stats": stats}
    fd, tmp = tempfile.mkstemp(dir=meta_dir, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        os.replace(tmp, out_path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return out_path

# ── GraphML output ────────────────────────────────────────

def _write_graphml(vault, nodes, edges):
    meta_dir = os.path.join(vault, ".wiki-meta")
    os.makedirs(meta_dir, exist_ok=True)
    out_path = os.path.join(meta_dir, "graph.graphml")

    def esc(s):
        return (str(s)
                .replace("&", "&amp;")
                .replace('"', "&quot;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/graphml"',
        '         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '         xsi:schemaLocation="http://graphml.graphdrawing.org/graphml'
        ' http://graphml.graphdrawing.org/graphml/1.1/graphml.xsd">',
        '  <key id="title"     for="node" attr.name="title"     attr.type="string"/>',
        '  <key id="type"      for="node" attr.name="type"      attr.type="string"/>',
        '  <key id="tags"      for="node" attr.name="tags"      attr.type="string"/>',
        '  <key id="links_out" for="node" attr.name="links_out" attr.type="int"/>',
        '  <key id="links_in"  for="node" attr.name="links_in"  attr.type="int"/>',
        '  <key id="weight"    for="edge" attr.name="weight"    attr.type="int"/>',
        '  <graph id="wiki" edgedefault="directed">',
    ]
    for node in nodes:
        lines.append(f'    <node id="{esc(node["id"])}">')
        lines.append(f'      <data key="title">{esc(node["title"])}</data>')
        lines.append(f'      <data key="type">{esc(node["type"])}</data>')
        lines.append(f'      <data key="tags">{esc(",".join(node["tags"]))}</data>')
        lines.append(f'      <data key="links_out">{node["links_out"]}</data>')
        lines.append(f'      <data key="links_in">{node["links_in"]}</data>')
        lines.append(f'    </node>')
    for i, edge in enumerate(edges):
        lines.append(f'    <edge id="e{i}" source="{esc(edge["source"])}" target="{esc(edge["target"])}">')
        lines.append(f'      <data key="weight">{edge["weight"]}</data>')
        lines.append(f'    </edge>')
    lines += ['  </graph>', '</graphml>']

    fd, tmp = tempfile.mkstemp(dir=meta_dir, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        os.replace(tmp, out_path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return out_path

# ── Execute ───────────────────────────────────────────────

if fmt == "json":
    out = _write_json(vault, nodes, edges, stats)
    print(f"Graph written: {out} ({len(nodes)} nodes, {len(edges)} edges)")
else:
    out = _write_graphml(vault, nodes, edges)
    print(f"Graph written: {out} ({len(nodes)} nodes, {len(edges)} edges)")

if stats_mode:
    print(f"\n=== Graph Stats ===")
    print(f"  Nodes:       {stats['total_nodes']}")
    print(f"  Edges:       {stats['total_edges']}")
    print(f"  Avg degree:  {stats['avg_degree']}")
    print(f"  Top hubs:    {', '.join(stats['top_hubs'][:10]) or '(none)'}")
    print(f"  Orphans:     {len(stats['orphans'])}")
    if stats["orphans"]:
        for o in stats["orphans"][:10]:
            print(f"    - {o}")
        if len(stats["orphans"]) > 10:
            print(f"    ... and {len(stats['orphans']) - 10} more")
    print(f"  Articulation pts: {len(stats['articulation_points'])}")
    if stats["articulation_points"]:
        for b in stats["articulation_points"][:10]:
            print(f"    - {b}")
        if len(stats["articulation_points"]) > 10:
            print(f"    ... and {len(stats['articulation_points']) - 10} more")
