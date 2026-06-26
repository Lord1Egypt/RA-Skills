#!/usr/bin/env python3
"""OpenPaperGraph CLI — Multi-source academic literature discovery and citation network analysis.

Sources: arXiv, DBLP, Semantic Scholar, Google Scholar, CrossRef, OpenAlex, Unpaywall.
References from PDF parsing, citations from Google Scholar, S2 as fallback.

Outputs structured JSON to stdout. Progress/errors go to stderr.
Exit codes: 0=success, 1=argument error, 2=API/runtime error.

Usage:
    python openpapergraph_cli.py search "transformer" --limit 10
    python openpapergraph_cli.py search "transformer" --source arxiv --venue NeurIPS --limit 10
    python openpapergraph_cli.py graph ARXIV:1706.03762 --depth 1 --output graph.json
    python openpapergraph_cli.py graph "attention is all you need" -o graph.json
    python openpapergraph_cli.py graph paper.pdf -o graph.json
    python openpapergraph_cli.py recommend ARXIV:1706.03762 --limit 10
    python openpapergraph_cli.py monitor "vision transformer" --year-from 2025
    python openpapergraph_cli.py analyze graph.json
    python openpapergraph_cli.py summary graph.json --style overview
    python openpapergraph_cli.py pdf paper.pdf
    python openpapergraph_cli.py graph-from-pdf paper.pdf -o graph.json
    python openpapergraph_cli.py zotero --user-id ID --api-key KEY
    python openpapergraph_cli.py export graph.json --format bibtex --output refs.bib
    python openpapergraph_cli.py export graph.json --format markdown -o papers.md
    python openpapergraph_cli.py export-html graph.json -o graph.html --title "My Research"
    python openpapergraph_cli.py conferences
"""
import argparse
import json
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schemas import Paper, GraphData, SearchResult

# Regex for Semantic Scholar 40-char hex paper ID
import re
_S2_ID_RE = re.compile(r'^[0-9a-fA-F]{40}$')
_ARXIV_PREFIX_RE = re.compile(r'^ARXIV:', re.IGNORECASE)
_DOI_PREFIX_RE = re.compile(r'^DOI:', re.IGNORECASE)


def output(data, pretty=False, output_file=None):
    """Write JSON to stdout, or save to file if output_file is specified."""
    indent = 2 if pretty else None
    text = json.dumps(data, indent=indent, ensure_ascii=False)
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"  Output saved to: {output_file}", file=sys.stderr)
    else:
        print(text)


def _out(args, data):
    """Shorthand: output data with pretty and output_file from args."""
    output(data, pretty=args.pretty, output_file=getattr(args, 'output', None))


def resolve_paper_id(identifier: str) -> str:
    """Smart resolve: accept S2 ID, ARXIV:, DOI:, PDF path, or paper title.

    Returns a Semantic Scholar paper ID string.
    - 40-char hex → use as-is
    - ARXIV:xxxx or DOI:xxxx → use as-is (S2 accepts these prefixes)
    - *.pdf file path → extract title from PDF, search S2 for paper_id
    - anything else → treat as paper title, search arXiv then S2 for paper_id
    """
    identifier = identifier.strip()

    # Already a S2 hex ID
    if _S2_ID_RE.match(identifier):
        return identifier

    # Already prefixed (ARXIV: or DOI:)
    if _ARXIV_PREFIX_RE.match(identifier) or _DOI_PREFIX_RE.match(identifier):
        return identifier

    # PDF file → should be handled directly by cmd_graph/cmd_recommend, not here
    if identifier.lower().endswith('.pdf') and os.path.isfile(identifier):
        raise ValueError(f"PDF '{identifier}' should be handled directly (use graph-from-pdf or pass to cmd_graph/cmd_recommend)")

    # Treat as paper title → search
    print(f"  Resolving title: \"{identifier}\"", file=sys.stderr)
    return _search_for_paper_id(identifier)


def _title_similarity(a: str, b: str) -> float:
    """Simple Jaccard similarity on lowered word sets."""
    wa = set(re.sub(r'[^a-z0-9\s]', '', a.lower()).split())
    wb = set(re.sub(r'[^a-z0-9\s]', '', b.lower()).split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def _strip_arxiv_version(arxiv_id: str) -> str:
    """Strip version suffix from arXiv ID: ARXIV:2105.02723v1 → ARXIV:2105.02723"""
    return re.sub(r'v\d+$', '', arxiv_id)


def _search_for_paper_id(title: str) -> str:
    """Search arXiv first, then S2. Return ARXIV:ID directly (S2 API accepts it)."""
    from services import arxiv, semantic_scholar as s2

    # Try arXiv first (default source) — return ARXIV:xxxx directly
    try:
        total, papers = arxiv.search(title, limit=5)
        for p in papers:
            sim = _title_similarity(title, p.title)
            if sim >= 0.5:
                clean_id = _strip_arxiv_version(p.id)
                print(f"  Found on arXiv: {p.title} → {clean_id} (sim={sim:.2f})", file=sys.stderr)
                return clean_id  # "ARXIV:xxxx" — S2 API natively accepts this format
        if papers:
            print(f"  arXiv results not similar enough (best: {papers[0].title})", file=sys.stderr)
    except Exception as e:
        print(f"  arXiv search failed: {e}", file=sys.stderr)

    # Fallback to S2 direct search (uses _s2_search for S2-only)
    try:
        total, papers = s2._s2_search(title, limit=3)
        for p in papers:
            sim = _title_similarity(title, p.title)
            if sim >= 0.5:
                print(f"  Found on S2: {p.title} → {p.id} (sim={sim:.2f})", file=sys.stderr)
                return p.id
        if papers:
            # If no good match, take the first S2 result (S2 relevance ranking)
            print(f"  S2 best match: {papers[0].title} → {papers[0].id}", file=sys.stderr)
            return papers[0].id
    except Exception as e:
        print(f"  S2 search failed: {e}", file=sys.stderr)

    raise ValueError(f"Could not find paper matching: \"{title}\"")


def cmd_search(args):
    from services import semantic_scholar as s2, arxiv, dblp

    if args.source == "all":
        # s2.search() is now multi-source (arXiv + DBLP + S2) with dedup
        total, papers = s2.search(args.query, limit=args.limit, offset=args.offset)
        _out(args, SearchResult(total=total, papers=papers).to_dict())

    elif args.source == "arxiv":
        total, papers = arxiv.search(args.query, limit=args.limit, offset=args.offset)
        _out(args, SearchResult(total=total, papers=papers).to_dict())

    elif args.source == "dblp":
        total, papers = dblp.search(args.query, limit=args.limit, offset=args.offset, venue=args.venue)
        _out(args, SearchResult(total=total, papers=papers).to_dict())

    else:  # s2 — use S2-only search for explicit S2 source
        query = f"{args.query} venue:{args.venue}" if args.venue else args.query
        total, papers = s2._s2_search(query, limit=args.limit, offset=args.offset)
        _out(args, SearchResult(total=total, papers=papers).to_dict())


def cmd_graph(args):
    from services.graph_builder import build_graph, build_graph_from_pdfs

    # Separate file inputs by type
    pdf_paths = []
    bib_paths = []  # .bib and .json (CSL-JSON)
    non_files = []

    for p in args.paper_ids:
        lower = p.lower()
        if lower.endswith('.pdf') and os.path.isfile(p):
            pdf_paths.append(p)
        elif (lower.endswith('.bib') or lower.endswith('.json')) and os.path.isfile(p):
            bib_paths.append(p)
        else:
            non_files.append(p)

    # Parse BibTeX / CSL-JSON files → extract seed paper IDs
    bib_seed_ids = []
    if bib_paths:
        from services.bibtex_parser import parse_file
        for bib_path in bib_paths:
            print(f"  Parsing bibliography file: {bib_path}", file=sys.stderr)
            bib_papers = parse_file(bib_path)
            for bp in bib_papers:
                # Try to resolve to S2 ID for graph building
                pid = None
                if bp.arxiv_id:
                    pid = f"ARXIV:{bp.arxiv_id}"
                elif bp.doi:
                    pid = f"DOI:{bp.doi}"
                else:
                    # Search by title
                    try:
                        pid = _search_for_paper_id(bp.title)
                    except Exception as e:
                        print(f"  Could not resolve: {bp.title[:50]}... ({e})", file=sys.stderr)
                if pid:
                    bib_seed_ids.append(pid)
            print(f"  Resolved {len(bib_seed_ids)} papers from {bib_path}", file=sys.stderr)

    all_non_pdf_ids = non_files + bib_seed_ids

    if pdf_paths:
        # PDF inputs → directly parse references (no roundabout title search)
        print(f"  Direct PDF parsing: {len(pdf_paths)} file(s)", file=sys.stderr)
        graph = build_graph_from_pdfs(pdf_paths, depth=args.depth)

        # If there are also non-PDF IDs, build their graph and merge
        if all_non_pdf_ids:
            resolved_ids = [resolve_paper_id(pid) if not (pid.startswith('ARXIV:') or pid.startswith('DOI:') or _S2_ID_RE.match(pid)) else pid for pid in all_non_pdf_ids]
            id_graph = build_graph(resolved_ids, depth=args.depth)
            # Merge nodes and edges
            existing_ids = {n.id for n in graph.nodes}
            for node in id_graph.nodes:
                if node.id not in existing_ids:
                    graph.nodes.append(node)
                    existing_ids.add(node.id)
            existing_edges = {(e["source"], e["target"]) for e in graph.edges}
            for edge in id_graph.edges:
                if (edge["source"], edge["target"]) not in existing_edges:
                    graph.edges.append(edge)
            graph.total_papers = len(graph.nodes)
    else:
        # All non-PDF inputs → resolve IDs (S2 hex, ARXIV:, DOI:, or title)
        resolved_ids = []
        for pid in all_non_pdf_ids:
            if pid.startswith('ARXIV:') or pid.startswith('DOI:') or _S2_ID_RE.match(pid):
                resolved_ids.append(pid)
            else:
                resolved_ids.append(resolve_paper_id(pid))
        if not resolved_ids:
            raise ValueError("No paper IDs could be resolved. Check your input files.")
        graph = build_graph(resolved_ids, depth=args.depth)

    # Auto-enrich papers missing metadata (authors, year, abstract)
    incomplete = [p for p in graph.nodes if not p.year or not p.authors]
    if incomplete and args.output:
        print(f"  Enriching {len(incomplete)} papers with missing metadata...", file=sys.stderr)
        try:
            from services.graph_manager import enrich_incomplete_papers
            enriched = enrich_incomplete_papers(graph, args.output)
            if enriched:
                print(f"  Enriched {enriched}/{len(incomplete)} papers", file=sys.stderr)
        except Exception as e:
            print(f"  Auto-enrich failed (non-fatal): {e}", file=sys.stderr)

    _out(args, graph.to_dict())


def cmd_recommend(args):
    from services.semantic_scholar import recommend

    # Separate PDF files from paper IDs/titles
    pdf_paths = [p for p in args.paper_ids if p.lower().endswith('.pdf') and os.path.isfile(p)]
    non_pdfs = [p for p in args.paper_ids if p not in pdf_paths]

    resolved_ids = []

    # PDF inputs → parse references, use resolved paper IDs as seeds
    if pdf_paths:
        from services.pdf_parser import parse_pdf
        for pdf_path in pdf_paths:
            print(f"  Parsing PDF for recommendation seeds: {pdf_path}", file=sys.stderr)
            result = parse_pdf(pdf_path)
            for paper in result.get("resolved_papers", []):
                pid = paper.get("paper_id") or paper.get("id")
                if pid:
                    resolved_ids.append(pid)
        print(f"  Extracted {len(resolved_ids)} seed paper(s) from PDF(s)", file=sys.stderr)

    # Non-PDF inputs → resolve as usual (S2 hex, ARXIV:, DOI:, or title)
    for pid in non_pdfs:
        resolved_ids.append(resolve_paper_id(pid))

    if not resolved_ids:
        raise ValueError("No paper IDs resolved. Check your input.")

    papers = recommend(resolved_ids, limit=args.limit)
    _out(args, {"papers": [p.to_dict() for p in papers]})


def cmd_monitor(args):
    from services.semantic_scholar import search_recent
    papers = search_recent(args.query, year_from=args.year_from, limit=args.limit)
    _out(args, {"papers": [p.to_dict() for p in papers]})


def cmd_analyze(args):
    from services.analysis import analyze
    graph = GraphData.load(args.graph_file)
    result = analyze(graph.nodes)
    _out(args, result)


def cmd_summary(args):
    import os as _os
    # Apply --provider and --model overrides via env vars
    if getattr(args, 'provider', None):
        _os.environ["LLM_PROVIDER"] = args.provider
    if getattr(args, 'model', None):
        _os.environ["LLM_MODEL"] = args.model
    from services.analysis import summarize
    graph = GraphData.load(args.graph_file)
    result = summarize(graph.nodes, style=args.style)
    _out(args, result)


def cmd_llm_providers(args):
    from services.llm_client import list_providers
    result = list_providers()
    _out(args, {"providers": result, "total": len(result)})


def cmd_pdf(args):
    from services.pdf_parser import parse_pdf
    result = parse_pdf(args.file, use_grobid=getattr(args, 'use_grobid', False))
    _out(args, result)


def cmd_graph_from_pdf(args):
    from services.graph_builder import build_graph_from_pdfs
    graph = build_graph_from_pdfs(
        pdf_paths=args.files,
        depth=args.depth,
        include_unresolved=args.include_unresolved,
        use_grobid=args.use_grobid,
    )

    # Auto-enrich papers missing metadata
    incomplete = [p for p in graph.nodes if not p.year or not p.authors]
    if incomplete and args.output:
        print(f"  Enriching {len(incomplete)} papers with missing metadata...", file=sys.stderr)
        try:
            from services.graph_manager import enrich_incomplete_papers
            enriched = enrich_incomplete_papers(graph, args.output)
            if enriched:
                print(f"  Enriched {enriched}/{len(incomplete)} papers", file=sys.stderr)
        except Exception as e:
            print(f"  Auto-enrich failed (non-fatal): {e}", file=sys.stderr)

    _out(args, graph.to_dict())


def cmd_zotero(args):
    from services.zotero import import_papers, get_collections
    if args.list_collections:
        cols = get_collections(args.user_id, args.api_key)
        _out(args, cols)
    else:
        papers = import_papers(args.user_id, args.api_key, collection_key=args.collection, limit=args.limit)
        _out(args, {"papers": [p.to_dict() for p in papers]})


def cmd_export(args):
    from services.export import to_bibtex, to_csv, to_markdown, to_json
    graph = GraphData.load(args.graph_file)
    fmt = args.format
    if fmt == "csv":
        content = to_csv(graph.nodes)
    elif fmt == "markdown":
        content = to_markdown(graph.nodes)
    elif fmt == "json":
        content = to_json(graph.nodes)
    else:
        content = to_bibtex(graph.nodes)

    out_file = getattr(args, 'output', None)
    if out_file:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Output saved to: {out_file}", file=sys.stderr)
    else:
        print(content)


def cmd_export_html(args):
    """Export graph as an interactive HTML file."""
    from services.html_export import export_html

    graph = GraphData.load(args.graph_file)

    # Pre-generate summary if --summary flag is set
    pre_summary = None
    if getattr(args, 'summary', False):
        from services.analysis import summarize
        from services.llm_client import is_llm_available, get_provider_info
        if getattr(args, 'provider', None):
            os.environ["LLM_PROVIDER"] = args.provider
        if getattr(args, 'model', None):
            os.environ["LLM_MODEL"] = args.model
        print("  Pre-generating summary...", file=sys.stderr)
        pre_summary = summarize(graph.nodes, style="overview")
        method = pre_summary.get("method", "unknown")
        print(f"  Summary generated ({method}) — will be embedded in HTML", file=sys.stderr)
    else:
        print("  No --summary flag — users can enter API key at runtime in the HTML", file=sys.stderr)

    out_file = getattr(args, 'output', None) or "graph.html"
    title = getattr(args, 'title', None) or "Paper Graph"
    inline_js = getattr(args, 'inline', False)
    export_html(graph, output_path=out_file, title=title, pre_summary=pre_summary, inline_js=inline_js)


def cmd_serve(args):
    """Start interactive graph management server."""
    from services.graph_server import start_server
    start_server(args.graph_file, port=args.port, title=getattr(args, 'title', 'Paper Graph'))


def cmd_remove_seed(args):
    """Remove a seed paper and its exclusive connections from a graph."""
    graph = GraphData.load(args.graph_file)
    paper_id = args.paper_id
    # Support fuzzy title matching
    if not graph.find_node(paper_id):
        for n in graph.nodes:
            if n.title and paper_id.lower() in n.title.lower():
                paper_id = n.id
                print(f"  Matched: {n.title}", file=sys.stderr)
                break
    if paper_id not in graph.seed_papers:
        _out(args, {"status": "error", "message": f"'{args.paper_id}' is not a seed paper"})
        return
    stats = graph.remove_seed(paper_id)
    out_path = args.output or args.graph_file
    graph.save(out_path)
    _out(args, {"status": "ok", "graph_file": out_path, **stats})


def cmd_remove_paper(args):
    """Remove a non-seed paper from a graph."""
    graph = GraphData.load(args.graph_file)
    paper_id = args.paper_id
    # Support fuzzy title matching
    if not graph.find_node(paper_id):
        for n in graph.nodes:
            if n.title and paper_id.lower() in n.title.lower():
                paper_id = n.id
                print(f"  Matched: {n.title}", file=sys.stderr)
                break
    stats = graph.remove_node(paper_id)
    if "error" in stats:
        _out(args, {"status": "error", "message": stats["error"]})
        return
    if stats["removed_nodes"] == 0:
        _out(args, {"status": "error", "message": f"Paper '{args.paper_id}' not found in graph"})
        return
    out_path = args.output or args.graph_file
    graph.save(out_path)
    _out(args, {"status": "ok", "graph_file": out_path, **stats})


def cmd_conferences(args):
    from services.dblp import VENUE_KEYS
    _out(args, list(VENUE_KEYS.keys()))


def main():
    # Common args inherited by all subcommands
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    common.add_argument("--quiet", action="store_true", help="Suppress stderr progress")
    common.add_argument("--output", "-o", default=None, help="Save output to file (default: print to stdout)")

    parser = argparse.ArgumentParser(
        prog="openpapergraph_cli",
        description="Academic literature discovery and citation network analysis CLI.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    p = sub.add_parser("search", help="Search papers", parents=[common])
    p.add_argument("query", help="Search query")
    p.add_argument("--source", default="all", choices=["s2", "arxiv", "dblp", "all"], help="Search source (default: all — multi-source arXiv+DBLP+S2)")
    p.add_argument("--venue", default=None, help="Conference filter: ICLR, NeurIPS, ICML, ACL, EMNLP, NAACL, WebConf, KDD")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--offset", type=int, default=0)

    # graph
    p = sub.add_parser("graph", help="Build citation network", parents=[common])
    p.add_argument("paper_ids", nargs="+", help="Paper IDs, titles, or PDF paths (auto-resolved)")
    p.add_argument("--depth", type=int, default=1)

    # recommend
    p = sub.add_parser("recommend", help="Get paper recommendations", parents=[common])
    p.add_argument("paper_ids", nargs="+", help="Paper IDs, titles, or PDF paths (auto-resolved)")
    p.add_argument("--limit", type=int, default=20)

    # monitor
    p = sub.add_parser("monitor", help="Check for recent papers on a topic", parents=[common])
    p.add_argument("query", help="Topic to monitor")
    p.add_argument("--year-from", type=int, default=2024)
    p.add_argument("--limit", type=int, default=20)

    # analyze
    p = sub.add_parser("analyze", help="Topic analysis on a graph", parents=[common])
    p.add_argument("graph_file", help="Path to graph JSON file")

    # summary
    p = sub.add_parser("summary", help="Generate research summary", parents=[common])
    p.add_argument("graph_file", help="Path to graph JSON file")
    p.add_argument("--style", default="overview", choices=["overview", "trends", "gaps"])
    p.add_argument("--provider", default=None, help="LLM provider (e.g. openai, deepseek, qwen, zhipu, moonshot)")
    p.add_argument("--model", default=None, help="LLM model name (overrides provider default)")

    # pdf
    p = sub.add_parser("pdf", help="Extract references from PDF", parents=[common])
    p.add_argument("file", help="Path to PDF file")
    p.add_argument("--use-grobid", action="store_true", help="Use GROBID for structured extraction (needs Docker)")

    # graph-from-pdf
    p = sub.add_parser("graph-from-pdf", help="Build citation graph from PDF reference lists", parents=[common])
    p.add_argument("files", nargs="+", help="PDF file paths")
    p.add_argument("--depth", type=int, default=0, help="Expansion depth (0=PDF refs only, 1=expand via S2)")
    p.add_argument("--include-unresolved", action="store_true", help="Include unresolved references as nodes")
    p.add_argument("--use-grobid", action="store_true", help="Use GROBID for structured extraction (needs Docker)")

    # zotero
    p = sub.add_parser("zotero", help="Import from Zotero", parents=[common])
    p.add_argument("--user-id", required=True)
    p.add_argument("--api-key", required=True)
    p.add_argument("--collection", default=None, help="Collection key")
    p.add_argument("--list-collections", action="store_true")
    p.add_argument("--limit", type=int, default=50)

    # export
    p = sub.add_parser("export", help="Export graph as BibTeX/CSV/Markdown/JSON", parents=[common])
    p.add_argument("graph_file", help="Path to graph JSON file")
    p.add_argument("--format", default="bibtex", choices=["bibtex", "csv", "markdown", "json"])

    # export-html
    p = sub.add_parser("export-html", help="Export graph as interactive HTML visualization", parents=[common])
    p.add_argument("graph_file", help="Path to graph JSON file")
    p.add_argument("--title", default="Paper Graph", help="Page title")
    p.add_argument("--summary", action="store_true", help="Pre-generate AI summary at export time (requires LLM API key in env)")
    p.add_argument("--inline", action="store_true", help="Inline vis-network JS for fully offline use (~500KB larger)")
    p.add_argument("--provider", default=None, help="LLM provider for --summary (e.g. openai, deepseek)")
    p.add_argument("--model", default=None, help="LLM model for --summary")

    # conferences
    sub.add_parser("conferences", help="List supported conferences", parents=[common])

    # llm-providers
    sub.add_parser("llm-providers", help="List supported LLM providers and their status", parents=[common])

    # remove-seed
    p = sub.add_parser("remove-seed", help="Remove seed paper + exclusive connections", parents=[common])
    p.add_argument("graph_file", help="Path to graph JSON file")
    p.add_argument("paper_id", help="Paper ID or title substring to match")

    # remove-paper
    p = sub.add_parser("remove-paper", help="Remove a non-seed paper from graph", parents=[common])
    p.add_argument("graph_file", help="Path to graph JSON file")
    p.add_argument("paper_id", help="Paper ID or title substring to match")

    # serve — interactive graph management server
    p = sub.add_parser("serve", help="Start interactive graph server (HTML viewer + management)", parents=[common])
    p.add_argument("graph_file", help="Path to graph JSON file")
    p.add_argument("--port", type=int, default=8787, help="Server port (default: 8787)")
    p.add_argument("--title", default="Paper Graph", help="Page title")

    args = parser.parse_args()

    if args.quiet:
        import logging
        logging.disable(logging.CRITICAL)

    commands = {
        "search": cmd_search, "graph": cmd_graph, "graph-from-pdf": cmd_graph_from_pdf,
        "recommend": cmd_recommend, "monitor": cmd_monitor, "analyze": cmd_analyze,
        "summary": cmd_summary, "pdf": cmd_pdf, "zotero": cmd_zotero,
        "export": cmd_export, "export-html": cmd_export_html,
        "conferences": cmd_conferences, "llm-providers": cmd_llm_providers,
        "remove-seed": cmd_remove_seed, "remove-paper": cmd_remove_paper,
        "serve": cmd_serve,
    }

    try:
        commands[args.command](args)
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
