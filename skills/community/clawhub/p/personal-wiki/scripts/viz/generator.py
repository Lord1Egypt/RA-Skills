from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from document import OKFDocument, OKFDocumentError

_INDEX_NAME = "index.md"
_LINK_RE = re.compile(r"\]\(([^)\s]+\.md)(?:#[A-Za-z0-9_\-]*)?\)")
_TYPE_PALETTE = {
    "BigQuery Dataset": "#8b5cf6",
    "BigQuery Table": "#3b82f6",
    "Reference": "#10b981",
}
_DEFAULT_NODE_COLOR = "#94a3b8"


@dataclass
class Concept:
    id: str
    type: str
    title: str
    description: str
    resource: str
    tags: list[str]
    body: str
    links_to: list[str] = field(default_factory=list)

    def to_node(self) -> dict[str, Any]:
        color = _TYPE_PALETTE.get(self.type, _DEFAULT_NODE_COLOR)
        return {
            "data": {
                "id": self.id,
                "label": self.title or self.id,
                "type": self.type,
                "description": self.description,
                "resource": self.resource,
                "tags": self.tags,
                "color": color,
                "size": 30 + min(60, len(self.body) // 200),
            }
        }


_WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")


def _norm_alias(s: str) -> str:
    """Normalise an alias for fuzzy wikilink matching."""
    return s.strip().lower().replace(" ", "_").replace("—", "-").replace("－", "-")


def _extract_links(
    body: str,
    doc_dir: Path,
    bundle_root: Path,
    alias_map: dict[str, str] | None = None,
) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    bundle_root_resolved = bundle_root.resolve()
    # Standard Markdown links: [text](path.md)
    for m in _LINK_RE.finditer(body):
        target = m.group(1)
        if "://" in target or target.startswith("/"):
            continue
        try:
            resolved = (doc_dir / target).resolve().relative_to(bundle_root_resolved)
        except ValueError:
            continue
        rel = resolved.as_posix()
        if rel.endswith(".md"):
            rel = rel[:-3]
        if rel and rel not in seen:
            seen.add(rel)
            out.append(rel)
    # Obsidian-style wikilinks: [[Concept Name]] or [[Concept|alias]]
    if alias_map:
        for m in _WIKILINK_RE.finditer(body):
            cid = alias_map.get(_norm_alias(m.group(1)))
            if cid and cid not in seen:
                seen.add(cid)
                out.append(cid)
    return out


def _walk_concepts(bundle_root: Path) -> list[Concept]:
    md_paths = [
        p for p in sorted(bundle_root.rglob("*.md")) if p.name != _INDEX_NAME
    ]
    # First pass: parse docs and build an alias map for wikilink resolution.
    parsed: list[tuple[str, Path, Any]] = []
    alias_map: dict[str, str] = {}
    for md_path in md_paths:
        rel = md_path.relative_to(bundle_root).with_suffix("")
        concept_id = "/".join(rel.parts)
        try:
            doc = OKFDocument.parse(md_path.read_text(encoding="utf-8"))
        except OKFDocumentError:
            continue
        parsed.append((concept_id, md_path, doc))
        # Aliases: bare filename, frontmatter title, and first H1 heading.
        aliases = {md_path.stem, concept_id}
        fm = doc.frontmatter or {}
        if fm.get("title"):
            aliases.add(str(fm["title"]))
        h1 = re.search(r"^#\s+(.+)$", doc.body or "", re.M)
        if h1:
            aliases.add(h1.group(1).strip())
        for a in aliases:
            alias_map.setdefault(_norm_alias(a), concept_id)

    # Second pass: build concepts with links resolved against alias_map.
    concepts: list[Concept] = []
    for concept_id, md_path, doc in parsed:
        fm = doc.frontmatter or {}
        tags = fm.get("tags") or []
        if not isinstance(tags, list):
            tags = [str(tags)]
        concept = Concept(
            id=concept_id,
            type=str(fm.get("type") or "Unknown"),
            title=str(fm.get("title") or concept_id),
            description=str(fm.get("description") or ""),
            resource=str(fm.get("resource") or ""),
            tags=[str(t) for t in tags],
            body=doc.body or "",
            links_to=_extract_links(
                doc.body or "", md_path.parent, bundle_root, alias_map
            ),
        )
        concepts.append(concept)
    return concepts


def _build_graph(concepts: list[Concept]) -> dict[str, Any]:
    ids = {c.id for c in concepts}
    nodes = [c.to_node() for c in concepts]
    edges: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str]] = set()
    for c in concepts:
        for target in c.links_to:
            if target == c.id or target not in ids:
                continue
            key = (c.id, target)
            if key in seen_edges:
                continue
            seen_edges.add(key)
            edges.append({
                "data": {
                    "id": f"{c.id}__{target}",
                    "source": c.id,
                    "target": target,
                }
            })
    bodies = {c.id: c.body for c in concepts}
    types = sorted({c.type for c in concepts})
    return {
        "nodes": nodes,
        "edges": edges,
        "bodies": bodies,
        "types": types,
        "palette": _TYPE_PALETTE,
    }


def _load_template() -> str:
    template_path = Path(__file__).parent / "viz.html"
    return template_path.read_text(encoding="utf-8")


def _load_asset(name: str) -> str:
    asset_path = Path(__file__).parent / name
    return asset_path.read_text(encoding="utf-8")


def generate_visualization(
    bundle_root: Path,
    out_path: Path,
    *,
    bundle_name: str | None = None,
) -> dict[str, int]:
    """Walk a bundle and write a single self-contained HTML visualization.

    Returns counts: {'concepts': N, 'edges': M, 'bytes': K}.
    """
    bundle_root = Path(bundle_root)
    out_path = Path(out_path)
    if not bundle_root.is_dir():
        raise FileNotFoundError(f"Bundle directory not found: {bundle_root}")

    concepts = _walk_concepts(bundle_root)
    graph = _build_graph(concepts)
    template = _load_template()
    css = _load_asset("viz.css")
    js = _load_asset("viz.js")
    name = bundle_name or bundle_root.resolve().name

    html = (
        template
        .replace("/*__VIZ_CSS__*/", css)
        .replace("/*__VIZ_JS__*/", js)
        .replace("__BUNDLE_NAME__", json.dumps(name))
        .replace("__BUNDLE_DATA__", json.dumps(graph))
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    return {
        "concepts": len(concepts),
        "edges": len(graph["edges"]),
        "bytes": len(html.encode("utf-8")),
    }
