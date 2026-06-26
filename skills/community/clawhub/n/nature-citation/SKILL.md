---
name: nature-citation
description: Strict Nature/CNS-family citation retrieval, verification, and export. Given a topic, claim, or list of papers, finds real citations, verifies DOIs, checks retraction status, and exports in BibTeX, RIS, ENW, or Zotero RDF format. Trigger when user needs citations, wants to verify references, or needs to export a reference list.
---

# nature-citation

## Purpose
Find, verify, and export citations for Nature-series manuscripts.
Strict accuracy: every reference must be real, accessible, and support the cited claim.

---

## Trigger Conditions
- "找参考文献" / "引用" / "citation" / "reference"
- "验证引用" / "verify DOI" / "check references"
- "导出文献" / "export BibTeX" / "Zotero" / "RIS" / "ENW"
- "这个说法有文献支持吗" / "find supporting papers for..."
- User pastes a claim and asks for citations

---

## Workflow

### Mode 1: Find citations for a claim
1. User provides: a scientific claim or topic
2. **First: search personal LitReview library** — `web_fetch("https://ybliterature.com/api/search?q=<URL-encoded-query>")`
   - If results found: use these as primary citations (already in user's library)
3. **CrossRef full-text search** — `web_fetch("https://api.crossref.org/works?query=<query>&filter=has-full-text:true&rows=5&sort=relevance")`
   - Extract: DOI, title, authors, year, journal, is-referenced-by-count
4. **Broader web search** — `web_search("<claim> site:nature.com OR site:science.org OR site:cell.com")`
5. **arXiv** — `web_search("arxiv <topic> <year>")`
6. For each candidate paper:
   - **Verify via CrossRef**: `web_fetch("https://api.crossref.org/works/<DOI>")`
     → confirms: real DOI, correct metadata, citation count
   - **Check retraction via RetractionWatch**: `web_search("site:retractionwatch.com \"<title keywords>\"")`
   - **Also check**: `web_search("<title> retraction OR retracted OR correction")`
   - Confirm it actually supports the claim (not just related)
7. Return ranked list: most relevant first, with support assessment and citation count

### Mode 2: Verify existing reference list
For each reference the user provides:
1. **CrossRef DOI lookup** (most reliable):
   - If DOI present: `web_fetch("https://api.crossref.org/works/<DOI>")`
   - Compare returned metadata with user's reference — flag any discrepancy
2. If no DOI: `web_search('"<author>" "<year>" "<journal>" "<title keywords>"')`
3. **Retraction check**: `web_search("site:retractionwatch.com \"<first author> <year>\"")`
4. Assess: does this ref support the claim it's cited for?
5. Flag: ✅ verified via CrossRef | ⚠️ found but unverified | ❌ wrong metadata or retracted

### Mode 3: Export reference list
Convert verified references to the requested format (see below).

---

## Nature Reference Style (numbered, Vancouver)

### Format:
```
[number]. LastName, A. B., LastName, C. D. & LastName, E. F. Title of article. 
Journal Abbrev. Vol, first–last page (Year).
```

### Rules:
- Up to 6 authors, then "et al."
- Journal names abbreviated (e.g., Nat. Mater., Nat. Commun., Science, J. Am. Chem. Soc.)
- Volume in bold (in final typeset, not manuscript)
- Pages with en-dash (–), not hyphen (-)
- Year in parentheses at end
- DOI optional in manuscript, required for online submission

### Example:
```
1. Liu, Z., Zhang, X. & Wang, Y. High-performance electrocatalysts for 
   oxygen evolution. Nat. Catal. 5, 234–243 (2022).
2. Chen, H. et al. Atomically dispersed metal catalysts. Science 375, 
   eabh1885 (2022).
```

---

## Export Formats

### BibTeX (for LaTeX/Overleaf):
```bibtex
@article{Liu2022,
  author  = {Liu, Zhen and Zhang, Xiao and Wang, Yong},
  title   = {High-performance electrocatalysts for oxygen evolution},
  journal = {Nature Catalysis},
  year    = {2022},
  volume  = {5},
  pages   = {234--243},
  doi     = {10.1038/s41929-022-00000-0}
}
```

### RIS (for Mendeley/Zotero import):
```
TY  - JOUR
AU  - Liu, Zhen
AU  - Zhang, Xiao
AU  - Wang, Yong
TI  - High-performance electrocatalysts for oxygen evolution
JO  - Nature Catalysis
PY  - 2022
VL  - 5
SP  - 234
EP  - 243
DO  - 10.1038/s41929-022-00000-0
ER  -
```

### ENW (EndNote):
```
%0 Journal Article
%A Liu, Zhen
%A Zhang, Xiao
%A Wang, Yong
%T High-performance electrocatalysts for oxygen evolution
%J Nature Catalysis
%D 2022
%V 5
%P 234-243
%R 10.1038/s41929-022-00000-0
```

### Zotero RDF:
Generate standard Zotero RDF XML format with `rdf:type bib:Article` entries.

---

## Journal Abbreviations (Nature Portfolio)

| Full name | Abbreviation |
|-----------|-------------|
| Nature | Nature |
| Nature Materials | Nat. Mater. |
| Nature Chemistry | Nat. Chem. |
| Nature Energy | Nat. Energy |
| Nature Catalysis | Nat. Catal. |
| Nature Communications | Nat. Commun. |
| Nature Methods | Nat. Methods |
| Nature Sustainability | Nat. Sustain. |
| Nature Computational Science | Nat. Comput. Sci. |
| Journal of the American Chemical Society | J. Am. Chem. Soc. |
| Angewandte Chemie International Edition | Angew. Chem. Int. Ed. |
| Advanced Materials | Adv. Mater. |
| ACS Nano | ACS Nano |
| Science | Science |
| Cell | Cell |

---

## Verification Checklist
For each reference, confirm:
- [ ] Author names correct (spelling, order)
- [ ] Year matches published version (not preprint)
- [ ] Journal name and abbreviation correct
- [ ] Volume and page numbers accurate
- [ ] DOI resolves to correct paper
- [ ] Not retracted (search "[title] retraction")
- [ ] Actually supports the cited claim

---

## Output
1. Verified reference list in Nature numbered style
2. Export file in requested format (BibTeX / RIS / ENW / Zotero RDF)
3. Verification report: ✅ confirmed / ⚠️ uncertain / ❌ problem found
