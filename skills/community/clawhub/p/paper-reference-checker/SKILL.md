---
name: paper-reference-checker
description: This skill should be used when the user asks to "check paper citations", "verify references", "detect fake citations", "validate bibliography", "check if papers exist", "查文献真伪", "检查论文引用", "验证参考文献", "识别虚假引用", or uploads a PDF/Overleaf document and wants to verify whether the cited papers genuinely exist. Provides systematic verification of academic references against Google Scholar, CNKI, arXiv, and other academic databases to detect AI-hallucinated or fabricated citations.
version: 1.2.1
---

# Paper Reference Checker

Systematically verify academic references to detect AI-hallucinated or fabricated citations. Queries Google Scholar, arXiv, CNKI, and other databases.

---

## Core Workflow

### Phase 1: Citation Extraction (Token-Efficient First)

**ALWAYS use targeted extraction before full-document reading — saves 80–95% tokens.**

| Input Type | Primary Method | Fallback |
|------------|---------------|----------|
| arXiv link | arxiv.org/html/{ID} → find references section | Full HTML, then PDF |
| PDF file | Last 15–20% of pages only | Expand to 30% → 50% → full |
| Overleaf link | Regex cite-keys from .tex → filter .bib/.bbl | Inline bibitem in .tex |
| Pasted list | Parse directly | — |

### Phase 2: Multi-Platform Querying (Priority Order)

1. **DOI** → https://doi.org/{DOI} — resolves = ✅ confirmed
2. **arXiv ID** → https://arxiv.org/abs/{ID} — match = ✅ confirmed
3. **Google Scholar** → search "Full Title"
4. **arXiv search** → arxiv.org/search/
5. **CNKI** → cnki.net
6. **Fallbacks**: Semantic Scholar · PubMed · IEEE Xplore · ACM DL · DBLP

### Phase 3: Authenticity Judgment

| Status | Label | Criteria |
|--------|-------|----------|
| ✅ | VERIFIED | Found in ≥1 authoritative DB |
| ⚠️ | UNCERTAIN | Partial match |
| ❌ | NOT FOUND | No match across all queried channels |
| 🔴 | FABRICATED | Non-existent venue, unresolvable DOI |
| 🔗 | BROKEN CITATION | [?] marker in PDF body |

### Phase 4: Report Output

See examples/sample-report.md for full example.

## Support Files

| File | Purpose |
|------|---------|
| references/citation-extraction.md | Format rules |
| references/search-strategies.md | Per-database query tactics |
| references/verification-criteria.md | Decision flowchart |
| scripts/extract_references.md | Full decision tree |
| examples/sample-report.md | Complete report example |
| examples/bibtex-example.bib | Annotated BibTeX |

## Databases
Google Scholar · arXiv · CNKI · Semantic Scholar · PubMed · IEEE Xplore · ACM DL · DBLP · DOI Resolver · Crossref
