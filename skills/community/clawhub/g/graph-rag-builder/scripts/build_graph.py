#!/usr/bin/env python3
"""
build_graph.py — Knowledge Graph Construction (M3)

Reads all extracted/<url_hash>.json files produced by extract_concepts.py
and assembles a directed knowledge graph:

  Node types:
    page     — one per crawled URL
    chunk    — one per content section (from a page)
    concept  — one per unique extracted concept (deduplicated)

  Edge types:
    HAS_CHUNK   page → chunk
    MENTIONS    chunk → concept  (concept appears in this chunk)
    REQUIRES    chunk → concept  (chunk lists this as a prerequisite)
    RELATED     concept → concept  (from LLM-extracted relationships)
    LINKS_TO    page → page  (hyperlinks from the crawl)

Outputs:
  graph.json       — serialized MultiDiGraph (networkx node-link format)

Usage:
    python scripts/build_graph.py --input ./output/strudel-cc-mcp
    python scripts/build_graph.py --input ./output/strudel-cc-mcp --force
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency bootstrap
# ---------------------------------------------------------------------------

def _ensure_deps():
    deps = {"networkx": "networkx"}
    missing = [pkg for mod, pkg in deps.items() if not _import_ok(mod)]
    if missing:
        print(f"Installing: {', '.join(missing)}")
        os.system(f"pip install {' '.join(missing)} --break-system-packages -q")

def _import_ok(mod):
    try:
        __import__(mod)
        return True
    except ImportError:
        return False

_ensure_deps()

import networkx as nx


# ---------------------------------------------------------------------------
# Concept normalization
# ---------------------------------------------------------------------------

def normalize_concept(name: str) -> str:
    """Normalize a concept name for deduplication.

    Examples:
        'Mini Notation'  → 'mini notation'
        'note()'         → 'note'
        'FM Synthesis'   → 'fm synthesis'
        '  pitch  '      → 'pitch'
    """
    name = name.strip()
    if not name:
        return ""
    name = re.sub(r'\(\s*\)$', '', name)   # strip trailing ()
    name = name.lower()
    name = re.sub(r'[_\-]+', ' ', name)    # hyphens/underscores → space
    name = re.sub(r'\s+', ' ', name)       # collapse whitespace
    name = name.rstrip('.,;:')
    return name.strip()


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

class GraphBuilder:

    def __init__(self, input_dir: Path):
        self.input_dir = input_dir
        self.extracted_dir = input_dir / "extracted"
        self.raw_dir = input_dir / "raw_content"

        self.G = nx.MultiDiGraph()

        # Accumulators filled during load
        self._concept_meta: dict[str, dict] = {}     # norm → {name, desc, mention_count}
        self._chunk_mentions: list[tuple] = []        # (chunk_id, norm)
        self._chunk_requires: list[tuple] = []        # (chunk_id, norm)
        self._concept_rels: list[tuple] = []          # (src_norm, relation, tgt_norm, chunk_id)

    # ------------------------------------------------------------------
    # Phase 1: load extracted pages → page + chunk nodes
    # ------------------------------------------------------------------

    def _load_extracted(self) -> int:
        files = sorted(self.extracted_dir.glob("*.json"))
        if not files:
            print("  WARNING: No extracted JSON files found.",
                  "Run extract_concepts.py first.", file=sys.stderr)
            return 0

        loaded = skipped_dry = 0

        for f in files:
            data = json.loads(f.read_text())

            if data.get("model") == "dry-run":
                skipped_dry += 1
                continue

            url = data["url"]
            page_id = f"page:{url}"

            self.G.add_node(
                page_id,
                type="page",
                url=url,
                title=data.get("title", ""),
                processed_at=data.get("processed_at", ""),
            )

            for chunk in data.get("chunks", []):
                chunk_id = chunk["id"]

                self.G.add_node(
                    chunk_id,
                    type="chunk",
                    url=chunk["url"],
                    page_title=chunk.get("page_title", ""),
                    section=chunk.get("section", ""),
                    text=chunk.get("text", ""),
                    word_count=chunk.get("word_count", 0),
                    tags=chunk.get("tags", []),
                    code_examples=chunk.get("code_examples", []),
                )

                self.G.add_edge(page_id, chunk_id, type="HAS_CHUNK")

                # Collect concepts
                for concept in chunk.get("concepts", []):
                    cname = concept.get("name", "").strip()
                    norm = normalize_concept(cname)
                    if not norm:
                        continue
                    desc = concept.get("description", "")
                    if norm not in self._concept_meta:
                        self._concept_meta[norm] = {
                            "name": cname,
                            "description": desc,
                            "mention_count": 0,
                        }
                    else:
                        # Keep the longer description
                        if len(desc) > len(self._concept_meta[norm]["description"]):
                            self._concept_meta[norm]["description"] = desc
                        # Prefer title-cased canonical name
                        existing = self._concept_meta[norm]["name"]
                        if cname[0].isupper() and not existing[0].isupper():
                            self._concept_meta[norm]["name"] = cname
                    self._concept_meta[norm]["mention_count"] += 1
                    self._chunk_mentions.append((chunk_id, norm))

                # Collect prerequisites
                for prereq in chunk.get("prerequisites", []):
                    norm = normalize_concept(prereq)
                    if norm:
                        self._chunk_requires.append((chunk_id, norm))

                # Collect concept→concept relationships
                for rel in chunk.get("relationships", []):
                    src = normalize_concept(rel.get("source", ""))
                    tgt = normalize_concept(rel.get("target", ""))
                    relation = (rel.get("relation") or "related_to").strip() or "related_to"
                    if src and tgt:
                        self._concept_rels.append((src, relation, tgt, chunk_id))

            loaded += 1

        if skipped_dry:
            print(f"  Skipped {skipped_dry} dry-run file(s) — "
                  "re-run extract_concepts.py with a real API key to populate concepts")

        return loaded

    # ------------------------------------------------------------------
    # Phase 2: materialize concept nodes + all concept edges
    # ------------------------------------------------------------------

    def _build_concept_graph(self):
        # Create concept nodes
        for norm, meta in self._concept_meta.items():
            self.G.add_node(
                f"concept:{norm}",
                type="concept",
                name=meta["name"],
                norm_name=norm,
                description=meta["description"],
                mention_count=meta["mention_count"],
            )

        # chunk → concept (MENTIONS)
        for chunk_id, norm in self._chunk_mentions:
            cid = f"concept:{norm}"
            if self.G.has_node(cid):
                self.G.add_edge(chunk_id, cid, type="MENTIONS")

        # chunk → concept (REQUIRES) — create concept node if new
        for chunk_id, norm in self._chunk_requires:
            cid = f"concept:{norm}"
            if not self.G.has_node(cid):
                self.G.add_node(
                    cid,
                    type="concept",
                    name=norm,
                    norm_name=norm,
                    description="",
                    mention_count=0,
                )
            self.G.add_edge(chunk_id, cid, type="REQUIRES")

        # concept → concept (RELATED)
        for src_norm, relation, tgt_norm, chunk_id in self._concept_rels:
            src_id = f"concept:{src_norm}"
            tgt_id = f"concept:{tgt_norm}"
            for nid, nname in [(src_id, src_norm), (tgt_id, tgt_norm)]:
                if not self.G.has_node(nid):
                    self.G.add_node(
                        nid,
                        type="concept",
                        name=nname,
                        norm_name=nname,
                        description="",
                        mention_count=0,
                    )
            self.G.add_edge(
                src_id, tgt_id,
                type="RELATED",
                relation=relation,
                via_chunk=chunk_id,
            )

    # ------------------------------------------------------------------
    # Phase 3: page → page hyperlinks (from raw_content/*.json)
    # ------------------------------------------------------------------

    def _build_page_links(self):
        if not self.raw_dir.exists():
            return

        # Build url → page node id lookup
        url_to_nid = {
            data["url"]: nid
            for nid, data in self.G.nodes(data=True)
            if data.get("type") == "page"
        }

        for f in self.raw_dir.glob("*.json"):
            raw = json.loads(f.read_text())
            src_url = raw.get("url", "")
            src_id = url_to_nid.get(src_url)
            if not src_id:
                continue
            for link_url in raw.get("outgoing_links", []):
                tgt_id = url_to_nid.get(link_url)
                if tgt_id and tgt_id != src_id:
                    # Avoid duplicate hyperlink edges
                    existing = [
                        d for _, _, d in self.G.out_edges(src_id, data=True)
                        if d.get("type") == "LINKS_TO"
                        and self.G.nodes[_]["url"] == link_url
                        if False  # placeholder — use has_edge check below
                    ]
                    # nx.MultiDiGraph allows parallel edges; deduplicate via attribute
                    already = any(
                        d.get("type") == "LINKS_TO"
                        for _, t, d in self.G.out_edges(src_id, data=True)
                        if t == tgt_id
                    )
                    if not already:
                        self.G.add_edge(src_id, tgt_id, type="LINKS_TO")

    # ------------------------------------------------------------------
    # Main build
    # ------------------------------------------------------------------

    def build(self) -> dict:
        print("  Phase 1: Loading extracted pages...")
        n_pages = self._load_extracted()
        print(f"           {n_pages} page(s) with LLM data loaded")

        print("  Phase 2: Building concept nodes and edges...")
        self._build_concept_graph()

        print("  Phase 3: Building page hyperlink edges...")
        self._build_page_links()

        return self._stats()

    def _stats(self) -> dict:
        node_types: dict[str, int] = {}
        for _, d in self.G.nodes(data=True):
            t = d.get("type", "unknown")
            node_types[t] = node_types.get(t, 0) + 1

        edge_types: dict[str, int] = {}
        for _, _, d in self.G.edges(data=True):
            t = d.get("type", "unknown")
            edge_types[t] = edge_types.get(t, 0) + 1

        return {
            "pages":       node_types.get("page", 0),
            "chunks":      node_types.get("chunk", 0),
            "concepts":    node_types.get("concept", 0),
            "total_nodes": self.G.number_of_nodes(),
            "total_edges": self.G.number_of_edges(),
            "edge_types":  edge_types,
        }

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def save(self, output_path: Path, stats: dict):
        data = nx.node_link_data(self.G, edges="edges")
        data["meta"] = {
            "created_at": datetime.utcnow().isoformat() + "Z",
            "stats": stats,
        }
        output_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2)
        )


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def _print_stats(stats: dict):
    print()
    print("━" * 62)
    print("  Graph built!")
    print(f"  Pages:        {stats['pages']:>6}")
    print(f"  Chunks:       {stats['chunks']:>6}")
    print(f"  Concepts:     {stats['concepts']:>6}")
    print(f"  ─────────────────────────")
    print(f"  Total nodes:  {stats['total_nodes']:>6}")
    print(f"  Total edges:  {stats['total_edges']:>6}")
    if stats["edge_types"]:
        print()
        print("  Edge breakdown:")
        for etype, count in sorted(stats["edge_types"].items(), key=lambda x: -x[1]):
            print(f"    {etype:<20} {count:>6}")
    print("━" * 62)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Build knowledge graph from extracted concept data (M3)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input", required=True, metavar="DIR",
                        help="MCP output dir (e.g. ./output/strudel-cc-mcp)")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing graph.json")
    args = parser.parse_args()

    input_dir = Path(args.input)
    if not input_dir.exists():
        print(f"ERROR: Input directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)

    output_path = input_dir / "graph.json"
    if output_path.exists() and not args.force:
        print(f"graph.json already exists. Use --force to overwrite.")
        sys.exit(0)

    print(f"Building knowledge graph")
    print(f"  Input:  {input_dir}")
    print(f"  Output: {output_path}")
    print()

    builder = GraphBuilder(input_dir)
    stats = builder.build()
    builder.save(output_path, stats)

    _print_stats(stats)
    print(f"  Saved: {output_path}")
    print()


if __name__ == "__main__":
    main()
