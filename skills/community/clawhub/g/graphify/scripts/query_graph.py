#!/usr/bin/env python3
"""
Programmatic query helper for graphify-out/graph.json.

Usage:
    python query_graph.py                      # print full summary
    python query_graph.py --god-nodes          # list highest-degree nodes
    python query_graph.py --communities        # list community clusters
    python query_graph.py --neighbors NodeId   # show direct neighbours
    python query_graph.py --path NodeA NodeB   # shortest path
    python query_graph.py --search keyword     # fuzzy node search
    python query_graph.py --inferred           # show inferred edges (confidence > threshold)
    python query_graph.py --export-context     # emit AI context block for graph content
"""

import json
import argparse
import sys
from pathlib import Path
from collections import defaultdict, deque


def load_graph(graph_path: Path) -> dict:
    if not graph_path.exists():
        sys.exit(f"ERROR: graph.json not found at {graph_path}\nRun: graphify .")
    with open(graph_path) as f:
        return json.load(f)


def build_adjacency(graph: dict, directed: bool = False) -> dict[str, list[dict]]:
    adj: dict[str, list[dict]] = defaultdict(list)
    for edge in graph.get("edges", []):
        adj[edge["source"]].append(edge)
        if not directed:
            reverse = {**edge, "source": edge["target"], "target": edge["source"]}
            adj[edge["target"]].append(reverse)
    return adj


def node_by_id(graph: dict) -> dict[str, dict]:
    return {n["id"]: n for n in graph.get("nodes", [])}


def god_nodes(graph: dict, top_n: int = 10) -> list[dict]:
    nodes = graph.get("nodes", [])
    return sorted(nodes, key=lambda n: n.get("degree", 0), reverse=True)[:top_n]


def communities(graph: dict) -> list[dict]:
    return graph.get("communities", [])


def neighbours(graph: dict, node_id: str) -> tuple[dict | None, list[dict]]:
    nmap = node_by_id(graph)
    node = nmap.get(node_id)
    edges = [e for e in graph.get("edges", []) if node_id in (e["source"], e["target"])]
    return node, edges


def bfs_path(graph: dict, start: str, end: str) -> list[str] | None:
    adj = build_adjacency(graph, directed=False)
    visited = {start}
    queue: deque[list[str]] = deque([[start]])
    while queue:
        path = queue.popleft()
        current = path[-1]
        if current == end:
            return path
        for edge in adj.get(current, []):
            nxt = edge["target"]
            if nxt not in visited:
                visited.add(nxt)
                queue.append(path + [nxt])
    return None


def search_nodes(graph: dict, keyword: str) -> list[dict]:
    kw = keyword.lower()
    return [
        n for n in graph.get("nodes", [])
        if kw in n.get("label", "").lower()
        or kw in n.get("summary", "").lower()
        or kw in n.get("file", "").lower()
    ]


def inferred_edges(graph: dict, min_confidence: float = 0.7) -> list[dict]:
    return [
        e for e in graph.get("edges", [])
        if e.get("relation") == "INFERRED"
        and e.get("confidence", 0.0) >= min_confidence
    ]


def print_summary(graph: dict) -> None:
    meta = graph.get("metadata", {})
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    comms = graph.get("communities", [])
    print(f"graphify knowledge graph summary")
    print(f"  version   : {meta.get('graphify_version', 'unknown')}")
    print(f"  generated : {meta.get('generated_at', 'unknown')}")
    print(f"  nodes     : {len(nodes)}")
    print(f"  edges     : {len(edges)}")
    print(f"  communities: {len(comms)}")
    print()
    print("Top god nodes:")
    for n in god_nodes(graph, top_n=5):
        print(f"  [{n.get('degree', 0):>4d}] {n['label']}  ({n.get('file', '')})")
    print()
    print("Communities:")
    for c in comms[:8]:
        gods = ", ".join(c.get("god_nodes", []))
        print(f"  [{c['id']}] {c.get('label', 'unnamed')}  ({len(c.get('members', []))} members)  gods: {gods}")


def export_context_block(graph: dict) -> str:
    lines = ["<graphify_context>"]
    meta = graph.get("metadata", {})
    lines.append(f"nodes={len(graph.get('nodes', []))} edges={len(graph.get('edges', []))} generated={meta.get('generated_at', '')}")
    lines.append("")
    lines.append("GOD NODES (highest-degree concepts):")
    for n in god_nodes(graph, top_n=10):
        lines.append(f"  {n['label']} (degree={n.get('degree', 0)}, file={n.get('file', '')}, community={n.get('community', '?')})")
    lines.append("")
    lines.append("COMMUNITIES:")
    for c in graph.get("communities", []):
        members_preview = ", ".join(c.get("members", [])[:5])
        lines.append(f"  [{c['id']}] {c.get('label', 'unnamed')}: {members_preview}{'...' if len(c.get('members', [])) > 5 else ''}")
    lines.append("</graphify_context>")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Query graphify-out/graph.json")
    parser.add_argument("--graph", default="graphify-out/graph.json", help="Path to graph.json")
    parser.add_argument("--god-nodes", action="store_true")
    parser.add_argument("--communities", action="store_true")
    parser.add_argument("--neighbors", metavar="NODE_ID")
    parser.add_argument("--path", nargs=2, metavar=("FROM", "TO"))
    parser.add_argument("--search", metavar="KEYWORD")
    parser.add_argument("--inferred", action="store_true")
    parser.add_argument("--min-confidence", type=float, default=0.7)
    parser.add_argument("--export-context", action="store_true")
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()

    graph = load_graph(Path(args.graph))
    nmap = node_by_id(graph)

    if args.god_nodes:
        print(f"Top {args.top} god nodes:")
        for n in god_nodes(graph, top_n=args.top):
            print(f"  [{n.get('degree', 0):>4d}] {n['label']}  ({n.get('file', '')}:{n.get('line', '')})")

    elif args.communities:
        for c in communities(graph):
            print(f"\n[Community {c['id']}] {c.get('label', 'unnamed')}  ({len(c.get('members', []))} members)")
            for m in c.get("members", []):
                node = nmap.get(m, {})
                print(f"  - {node.get('label', m)}  ({node.get('file', '')})")

    elif args.neighbors:
        node, edges = neighbours(graph, args.neighbors)
        if not node:
            sys.exit(f"Node '{args.neighbors}' not found. Use --search to find node IDs.")
        print(f"Node: {node['label']}  ({node.get('file', '')})\n")
        for e in edges:
            other_id = e["target"] if e["source"] == args.neighbors else e["source"]
            other = nmap.get(other_id, {})
            conf = f"  conf={e['confidence']:.2f}" if "confidence" in e else ""
            direction = "→" if e["source"] == args.neighbors else "←"
            print(f"  {direction} {other.get('label', other_id)}  [{e.get('relation', '')} {e.get('label', '')}]{conf}")

    elif args.path:
        start, end = args.path
        if start not in nmap or end not in nmap:
            matches_start = search_nodes(graph, start)
            matches_end = search_nodes(graph, end)
            if not matches_start:
                sys.exit(f"Node '{start}' not found.")
            if not matches_end:
                sys.exit(f"Node '{end}' not found.")
            start = matches_start[0]["id"]
            end = matches_end[0]["id"]
            print(f"Resolved: {start} → {end}")
        path = bfs_path(graph, start, end)
        if path is None:
            print(f"No path found between '{start}' and '{end}'.")
        else:
            print(f"Shortest path ({len(path) - 1} hops):")
            for node_id in path:
                n = nmap.get(node_id, {})
                print(f"  {n.get('label', node_id)}  ({n.get('file', '')})")

    elif args.search:
        results = search_nodes(graph, args.search)
        if not results:
            print(f"No nodes matching '{args.search}'.")
        else:
            print(f"{len(results)} result(s) for '{args.search}':")
            for n in results[:args.top]:
                print(f"  {n['id']}  {n['label']}  ({n.get('file', '')})  community={n.get('community', '?')}")

    elif args.inferred:
        edges = inferred_edges(graph, min_confidence=args.min_confidence)
        print(f"{len(edges)} inferred edges with confidence >= {args.min_confidence}:")
        for e in sorted(edges, key=lambda x: x.get("confidence", 0), reverse=True)[:args.top]:
            src = nmap.get(e["source"], {}).get("label", e["source"])
            tgt = nmap.get(e["target"], {}).get("label", e["target"])
            print(f"  {src} --[{e.get('label', '')} conf={e.get('confidence', 0):.2f}]--> {tgt}")

    elif args.export_context:
        print(export_context_block(graph))

    else:
        print_summary(graph)


if __name__ == "__main__":
    main()
