# DGRA v0.4.1 Architecture: API-First, Cache-Assisted

## Problem Statement

Current v0.3 relies on **enumerated hardcoded lists**:
- `protein_domains.json`: 15 genes manually curated
- `tissue_context.json`: ~20 genes per tissue profile, manually classified
- `pseudogene_config.json`: 4 known pseudogene pairs
- `MANE_SELECT` dict in code: 17 transcripts hardcoded

This does not scale. Human genome has ~20,000 protein-coding genes. We cannot enumerate them all.

## New Architecture: API-First with Fallbacks

### Principle
**Query APIs first, cache results, use local overrides only for API errors or special cases.**

```
┌─────────────────────────────────────────────────────────────────┐
│                        DGRA Core Pipeline                        │
├─────────────────────────────────────────────────────────────────┤
│  Input VCF  →  API Query Layer  →  Cache Layer  →  Decision    │
│                (UniProt/Ensembl/GTEx/gnomAD)                   │
│                                ↓                                │
│                         Local Override Layer                     │
│                    (JSON corrections for known                   │
│                     API blind spots: pseudogenes,                │
│                     tissue-specific exceptions)                  │
└─────────────────────────────────────────────────────────────────┘
```

### Layer 1: API Query Layer (Primary Source)

| Data Need | API | Endpoint | Fallback if API Fails |
|-----------|-----|----------|----------------------|
| Canonical transcript | Ensembl REST | `/lookup/symbol/homo_sapiens/{gene}` | Use longest CDS transcript |
| MANE Select | NCBI E-utilities | `esearch+esummary` gene | Use RefSeq "NM_" prefix |
| Protein domains | UniProt REST | `/uniprotkb/{accession}` | Use InterPro API |
| Tissue expression | GTEx Portal API | `/rest/v1/expression/gene` | Use bulk GTEx RPKM data (local) |
| Gene function | Gene Ontology (GO) | GO API or Ensembl `/ontology` | Use Ensembl biotype |
| Population AF | gnomAD GraphQL | `variant` query | Use VCF INFO field |
| ClinVar | NCBI E-utilities | `esearch+efetch` | Use input VCF CLIN_SIG |
| Pseudogene check | UCSC API or local | `pseudogene.org` dump | Use local config (rare, ~50 pairs known) |

### Layer 2: Cache Layer

```python
# SQLite cache with TTL
CACHE_DB = "~/.openclaw/skills/dgra-genomic-risk/cache/dgra_cache.db"
TTL = 30 days  # Gene annotations don't change often
```

Cache keys:
- `uniprot:{gene}` → protein domains JSON
- `ensembl:{gene}` → canonical transcript + biotype
- `gtex:{gene}:{tissue}` → RPKM value
- `gnomad:{chrom}:{pos}:{ref}:{alt}` → AF + constraints
- `clinvar:{rsid}` → clinical significance

### Layer 3: Local Override Layer (Exception Handling)

Keep small JSON files ONLY for:
1. **Known API blind spots** — pseudogenes that APIs mis-annotate (SETBP1/VWFP1, GBA/GBAP1)
2. **Tissue-specific exceptions** — genes that GTEx says "low" but literature says "critical for HSC" (e.g., FANCD2 in quiescent HSCs may have low GTEx BM but is essential)
3. **Novel/candidate genes** — not yet in UniProt/GO with full annotation
4. **Correction rules** — when APIs return wrong canonical transcript (like SETBP1 isoform b)

Override file size target: **<100 genes total**, not 20,000.

## Module Refactoring Plan

### Module A: Transcript Priority → Ensembl/NCBI API

```python
async def get_canonical_transcript(gene: str) -> str:
    """
    1. Query Ensembl REST for canonical transcript
    2. Check NCBI Gene for MANE Select flag
    3. Fallback: select longest CDS isoform among RefSeq
    4. Cache result
    """
    # No hardcoded dict
```

### Module D: Protein Domain → UniProt API

```python
async def get_protein_domains(gene: str) -> List[Dict]:
    """
    1. Query UniProt for gene → uniprot ID mapping
    2. Query UniProt /uniprotkb/{id} for features (DOMAIN, REGION)
    3. Map amino acid position to overlapping features
    4. Cache result
    5. Fallback: return {"domain": "unknown", "source": "no_uniprot_data"}
    """
```

### Module E: Tissue Relevance → GTEx + GO API

```python
async def assess_tissue_relevance(gene: str, tissue: str) -> Dict:
    """
    1. Query GTEx API for tissue RPKM
    2. Query GO API for gene function annotations
    3. Use tissue profile rules (fast_track thresholds) on API data
    4. If gene not in any profile → default: "unknown_relevance, proceed_with_caution"
    
    No hardcoded gene list. Rules are:
    - RPKM > 10 + GO term matches tissue → primary
    - RPKM 1-10 + GO term matches → secondary  
    - RPKM < 1 + no GO match → none
    - RPKM not available → unknown (don't fast-track)
    """
```

### Module B: Pseudogene → Local Config (Exception Only)

Keep `pseudogene_config.json` but it's now **exception handling**, not primary source:
```python
def detect_pseudogene_artifact(variant):
    # Only check the ~50 known pseudogene pairs
    # Everything else: no pseudogene concern unless API flags it
```

### Module C: gnomAD → gnomAD API

```python
async def get_gnomad_frequency(chrom, pos, ref, alt):
    # Query gnomAD GraphQL API
    # Return structured result including NOT_CAPTURED
```

## Default Rules for Unknown Genes

When APIs return no data (gene not in UniProt, no GTEx data, no GO terms):

| Module | Default Behavior |
|--------|-----------------|
| Transcript | Use longest RefSeq NM transcript from input VCF |
| Protein domain | `{"domain": "unknown", "note": "No UniProt annotation available"}` |
| Tissue relevance | `{"tier_suggestion": "assess_via_standard_pipeline", "relevance": "unknown"}` — **do NOT fast-track** |
| gnomAD | `{"status": "NOT_CAPTURED"}` — continue with other modules |
| Tier classification | Conservative: unknown → Tier 2 if HIGH impact, Tier 3 if LOW + common |

## Implementation Priority

### Phase 1: ✅ COMPLETE (2026-05-19)

**Delivered:**
1. ✅ Cache layer skeleton (`scripts/dgra_cache.py`) — SQLite schema with TTL, hit/miss stats, bulk import/export
2. ✅ Configuration manager (`scripts/dgra_config.py`) — API endpoints, timeouts, retry policies, offline mode, env var overrides
3. ✅ API wrapper framework (`scripts/dgra_api.py`) — Async aiohttp client with rate limiting, retry, cache integration
4. ✅ Design document (`DESIGN_v0.4.md`) — Architecture specification
5. ✅ Requirements file (`requirements.txt`) — aiohttp dependency

**Files created:**
```
scripts/dgra_config.py      # 175 lines — config + API endpoint definitions
scripts/dgra_cache.py       # 320 lines — SQLite cache with TTL + stats
scripts/dgra_api.py         # 680 lines — 6 API wrappers + batch query
requirements.txt            # aiohttp dependency
```

**API wrappers implemented (skeleton):**
- `query_ensembl_gene()` — canonical transcript, biotype
- `query_ensembl_transcript_info()` — CDS, exons, translation
- `query_uniprot_by_gene()` — protein domains, GO terms, sequence length
- `query_gtex_expression()` — tissue RPKM
- `query_gnomad_variant()` — AF, constraint metrics
- `query_ncbi_clinvar()` — clinical significance
- `batch_query_genes()` — concurrent batch execution

**Verified:**
- Cache layer initializes SQLite DB correctly
- All modules import without syntax errors
- aiohttp dependency installable

**Next:** Phase 2 — Replace hardcoded data structures with API queries in `dgra_core.py`

### Phase 2: Next session (pending user approval)
1. Replace hardcoded MANE_SELECT with Ensembl query
2. Replace hardcoded PROTEIN_DOMAINS with UniProt query  
3. Replace hardcoded tissue gene lists with GTEx + GO rules
4. Add `--offline` mode support in CLI
5. Integration test with real API calls

### Phase 3: Robustness (future)
1. Rate limiting stress test
2. Retry logic edge cases
3. API key support for high-volume users
4. Cache invalidation strategy

## API Endpoints Reference

### Ensembl REST (no auth required)
- `https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene}?expand=1`
- Returns: canonical transcript, biotype, description

### UniProt REST (no auth required)
- `https://rest.uniprot.org/uniprotkb/search?query=gene:{gene}+AND+organism_id:9606`
- `https://rest.uniprot.org/uniprotkb/{accession}.json`
- Returns: sequence, features (domains, regions), GO terms

### GTEx Portal API (no auth required)
- `https://gtexportal.org/rest/v1/expression/gene?geneId={gene}&tissue={tissue}`
- Returns: median RPKM per tissue

### gnomAD GraphQL (no auth required)
- `https://gnomad.broadinstitute.org/api/`
- Query: `variant(chrom, pos, ref, alt)` → AF, constraints

### NCBI E-utilities (no auth required)
- `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`
- For ClinVar, Gene (MANE Select), PubMed

## Risk: What if all APIs are down?

**Fallback mode** (`--offline`):
- Use only input VCF annotation
- Use only local override JSON (pseudogenes, known exceptions)
- Apply conservative tier rules (unknown = assume relevance, no fast-track)
- Report confidence: "LOW — API data unavailable, manual review strongly recommended"

## Confidence Annotation

Every variant output gets a `confidence` field:
- `HIGH` — all APIs returned data, consistent results
- `MEDIUM` — one API failed, fallback used, consistent with others
- `LOW` — multiple APIs failed or returned conflicting data
- `MANUAL_REVIEW` — known API blind spot (pseudogene, complex locus)



## 离线模式设计（追加 2026-05-19）

### 为什么需要离线模式

离线模式（`--offline`）是 **fallback 机制**，不是降级版。

### 触发场景
1. **API 不可用** — 服务器无外网、API 限流/维护/故障
2. **批量重分析** — 同一批变异反复跑，API 调用浪费（缓存命中则跳过）
3. **临床环境** — 医院内网可能不允许外连 Ensembl/UniProt/GTEx

### 离线模式能做什么
```
✅ special_gene_lists 检查（coagulation/fa_dna_repair/cardiomopathy等）
✅ 假基因 VAF 异常检测
✅ 三层分级（Tier 1/2/3）
✅ 多击基因检测
✅ 生成 Markdown 报告
❌ 转录本校正（无 Ensembl）
❌ 蛋白功能域映射（无 UniProt）
❌ GTEx 表达量查询（无 GTEx API）
```

### 没有离线模式的后果
API 失败时整个 pipeline 崩溃，**一个变异都分析不了**。离线模式保证至少能出一份基于本地规则的保守报告。

### 实际验证（10条变异）
| 模式 | Ensembl | UniProt | GTEx | Tier 1 | Tier 2 | Tier 3 |
|------|---------|---------|------|--------|--------|--------|
| 在线 | 9/9 | 9/9 | 9/9 | 3 | 2 | 5 |
| 离线 | 0/9 | 0/9 | 0/9 | 3 | 2 | 5 |

**分级结果完全一致** — 因为 VWF/FANCD2/ABCB1 的判定靠的是 `special_gene_lists`，不依赖 API。

---
*Document version: 0.4-beta*
*Next step: SKILL.md + config.json for clawhub publish*
