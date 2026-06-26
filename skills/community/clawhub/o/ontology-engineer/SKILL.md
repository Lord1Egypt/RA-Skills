---
name: ontology-engineer
version: 1.1.1
description: >-
  Extract candidate ontology models from enterprise business systems AND build/maintain
  personal knowledge graphs from any file system. Use when: ontology extraction, 本体提取,
  schema analysis, entity extraction, data dictionary (数据字典), 表结构分析, knowledge graph
  (知识图谱), 全量扫描, file scan, personal knowledge (个人知识), or analyzing business
  system data models. Three operating modes:
  (A) Database/schema extraction — SCAN→EXTRACT→MERGE from SQL DDL, Word/Excel data
  dictionaries. Outputs ontology.json + review.md.
  (B) Filesystem scanning — index→analyze pipeline for personal knowledge graph. Reads
  Office/PDF/text, extracts entities and domain structures. Outputs graph.jsonl + schema.yaml.
  (C) External data scanning — same as B for others' data spaces (clients, partners).
  Handles .docx .doc .wps .pdf .xlsx .xls .et .pptx .ppt .dps .md .txt .sql .yaml .json .csv.
  Uses python-docx, PyMuPDF, openpyxl, python-pptx. Supports multimodal image analysis.
  No external API keys or network access required — the LLM running this skill IS the
  semantic analysis engine. All processing is local. File scanning is user-scoped via
  mandatory Step 1.5 confirmation before any analysis begins.
metadata.openclaw:
  homepage: "https://github.com/li2092/ontology-engineer"
  requires:
    bins:
      - python3
    anyBins:
      - libreoffice
      - word
  install:
    - type: uv
      packages:
        - python-docx
        - PyMuPDF
        - openpyxl
        - xlrd
        - python-pptx
        - Pillow
        - pyyaml
---

# Ontology Engineer

Extract candidate ontology models from existing data. Build and maintain personal knowledge graphs.

**Core principle**: Make implicit business models in existing data explicit. Don't create from scratch.

**Division of labor**: Scripts handle mechanical extraction (file scanning, format conversion, table parsing). LLM handles semantic judgment (entity identification, property selection, relationship discovery, naming, cross-source merging).

**Security model**:
- **No external API calls.** The LLM running this skill (Claude, OpenClaw, etc.) IS the semantic engine. No credentials, no network endpoints, no data exfiltration paths.
- **User-scoped scanning.** Step 1.5 is a MANDATORY interactive checkpoint — the user reviews and approves every folder before any content is read. Nothing is analyzed without explicit confirmation.
- **Local-only output.** All artifacts (graph.jsonl, schema.yaml, review.md) are written to a user-specified local directory. No data leaves the machine.
- **Append-only writes.** Scripts only create/append files. No deletion, no modification of existing user files.

## When This Skill Adds Value (and When It Doesn't)

Knowledge graphs and ontology extraction are not universally useful. Before starting, assess fit:

| Scenario | Value | Why |
|----------|-------|-----|
| **3+ heterogeneous systems** with inconsistent naming for the same concepts | High (Mode A) | Cross-system concept alignment is the core use case |
| **Agent product** needs factual grounding to reduce hallucination | High (Mode B/C) | Graph becomes Agent's fact base — auto-query before every response |
| **1000+ entities** with dense relationships across long time spans | High | Pattern discovery humans can't do manually (churn, cross-sell, capability mapping) |
| **Client consulting engagement** analyzing their data landscape | High (Mode A) | Core consulting deliverable: "here's what your data assets look like" |
| Small org, <200 entities, info fits in one person's head + Excel | Low (Mode B) | Graph just re-stores what user already knows — use as PoC/capability validation only |
| Single system, no cross-system integration need | Low (Mode A) | Read the schema directly; ontology layer adds overhead without value |

**Rule of thumb**: If the user's reaction to the output is "I already knew all this", the graph isn't producing incremental value. Redirect to Mode A (client projects) or Agent integration.

**Detailed value scenarios**: [references/value-scenarios.md](references/value-scenarios.md)

## Operating Modes

| Mode | Input | Output | Use When |
|------|-------|--------|----------|
| **A: Database Extraction** | SQL DDL, data dictionaries, Word/Excel schemas | ontology.json + review.md | Analyzing enterprise business systems |
| **B: Filesystem Scanning** | Local/cloud directories | graph.jsonl + schema.yaml | Building personal knowledge graph |
| **C: External Data** | Others' data spaces, shared drives | graph.jsonl (source=external) | Acquiring others' business models |

---

## Mode A: Database Extraction

Three-phase workflow for extracting ontology from structured data sources.

### Phase 1: SCAN

Run `scripts/scan_directory.py` to discover and classify files by priority (P1-P7).

```bash
python scripts/scan_directory.py "<dir>" --output scan_result.json --report
```

Review scan report. Process P1-P2 files first, expand as needed.

### Phase 2: EXTRACT

1. Convert .doc files if needed: `scripts/convert_doc.py`
2. Extract tables from Word/Excel: `scripts/extract_tables.py`
3. Read extracted data, apply Rules 1-7 (see [analysis-rules.md](references/analysis-rules.md))
4. For text formats (.sql, .json, .yaml, .md, .csv): read directly

### Phase 3: MERGE

1. Cross-source entity deduplication (Rule 5)
2. Relationship consolidation
3. Output: `ontology.json` + `review.md`

**Detailed rules**: [references/analysis-rules.md](references/analysis-rules.md) (Rules 1-7)
**Quality checks**: [references/quality-checks.md](references/quality-checks.md)
**Script details**: [references/script-operations.md](references/script-operations.md)
**Modeling decisions**: [references/modeling-decisions.md](references/modeling-decisions.md)

---

## Mode B/C: Knowledge Graph

Two-step pipeline for building personal knowledge graphs from file systems.

### Step 1: File Indexing (script, no LLM)

```bash
python scripts/scan_filesystem.py --root /path --config namespace_rules.yaml --extract-metadata
```

Creates Document + Project entities in graph.jsonl. Pure mechanical operation.

**Key features**: Auto namespace inference, duplicate detection, .docx/.pdf metadata extraction, universal noise filtering.

### Step 1.5: User Scope Confirmation (MANDATORY interactive step)

After Step 1 completes, **present the scan summary to the user and ask for scope confirmation** before proceeding to Step 2. The user knows which folders matter most.

Display a table of all discovered projects/namespaces with document counts, then ask:

```
扫描完成，发现 {N} 个项目，共 {M} 篇文档。请标记每个文件夹的优先级：
- 🔴 重点（高采样率，优先分析）
- ⚪ 普通（默认采样率）
- ⚫ 忽略（跳过，不分析）
- 或输入"全部"跳过选择，按默认策略处理所有文件夹

| # | 项目 | 文档数 | 格式分布 | 默认优先级 |
|---|------|--------|----------|-----------|
| 1 | work/myfiles | 15,617 | .doc .docx .pdf .xlsx | 🔴 重点 |
| 2 | work/classified | 1,578 | .doc .pdf .xlsx | ⚪ 普通 |
| ... | ... | ... | ... | ... |

请输入调整（如 "2=忽略, 5=重点"）或 "全部" 或 "确认"：
```

**Rules**:
- User can mark any folder as 重点/普通/忽略
- User can type "全部" to skip selection and use defaults
- 重点 folders get 2-3x sampling rate, 忽略 folders are skipped entirely
- Default priority is auto-inferred: human work folders=重点, AI-generated=普通, downloads/cache=忽略
- **Never skip this step.** Even if obvious, let the user confirm.

### Step 2: Semantic Analysis (LLM, core step)

Five phases: Sampling → Document Reading → Aggregation → Cross-project Alignment → Output.

**Key decisions** (details in [knowledge-graph-workflow.md](references/knowledge-graph-workflow.md)):
- Minimum 10% coverage, 重点 folders 2-3x, 忽略 folders skip
- **Structured lists (Rule 13)**: Files named 列表/台账/名单/登记表/清单 etc. → full extraction (every row = one entity), NOT sampling. See [analysis-rules.md](references/analysis-rules.md) Rule 13.
- Dual-track extraction: Track A (named entities) + Track B (domain terms)
- Subagents must be `general-purpose` type (Bash access). Never use Explore type.
- Format tools: see [formats-and-deps.md](references/formats-and-deps.md)
- **Relation semantics**: Use enriched relation format with direction, cardinality, temporal range. See [relation-ontology.md](references/relation-ontology.md).

### Step 3: Runtime Evolution

Agent enriches the knowledge graph during daily conversations. `source.type = "runtime"`.

**When to trigger** (passive, no user action needed):
- User mentions a person by name + role/org → check graph, append if new
- User discusses a project/event with dates → append Event
- User makes a strategic decision or key insight → append Note
- User mentions a new organization/client → append Organization

**How to append**:
```bash
python query_graph.py search "张三"  # Check if entity exists
# If not found, append to graph.jsonl:
echo '{"op":"create","ts":"...","entity":{"id":"per-NNNNN","type":"Person","graph":"core/persons","source":{"type":"runtime","conversation_id":"..."},...}}' >> graph.jsonl
```

**Rules**:
- Only append entities with concrete evidence from the conversation
- Never overwrite existing entities — only add new ones or note conflicts
- Use `source.type = "runtime"` to distinguish from scan-derived entities
- Keep it lightweight: 1-3 entities per conversation, not a full re-scan

**Full workflow details**: [references/knowledge-graph-workflow.md](references/knowledge-graph-workflow.md)
**Analysis rules (8-12)**: [references/analysis-rules.md](references/analysis-rules.md)
**Format support & deps**: [references/formats-and-deps.md](references/formats-and-deps.md)

---

## Key Principles

- **Model business concepts, not database tables.** Table names ≠ object names.
- **Extract then express.** Make implicit models explicit, don't create from nothing.
- **Experts judge.** Produce candidates; final decisions belong to humans. When in doubt, flag it.
- **Invest in invariants.** Stable entities and relationships, not technical details.
- **Handle what exists.** Real projects use Word and Excel. Adapt to the data.
- **Scripts extract, LLM analyzes.** Mechanical extraction via Python. Semantic judgment via LLM.
- **Coverage over perfection.** 60% of files at moderate depth beats 3% at maximum depth.
- **Generic skeleton + domain discovery.** 8 core types (BFO-aligned). Domain types discovered by scanning.
- **Single source of truth.** All data in one graph.jsonl. Soft partition via graph/labels/source.
- **Relations carry semantics.** Direction, cardinality, temporal range, evidence. Not just type + target.
- **Append-only evolution.** Never delete entities. Deprecate, reclassify, version.

## Ontology Theory References

| Reference | When to Read |
|-----------|-------------|
| [modeling-decisions.md](references/modeling-decisions.md) | Core type boundaries, entity vs enum, promotion judgment |
| [relation-ontology.md](references/relation-ontology.md) | Relation format, core relation catalog, ternary relations |
| [ontology-evolution.md](references/ontology-evolution.md) | Schema versioning, entity reclassification, conflict resolution |
| [constraints-and-inference.md](references/constraints-and-inference.md) | Type/relation constraints, inference rules, inconsistency detection |
| [value-scenarios.md](references/value-scenarios.md) | When this skill adds value and when it doesn't |

---

## Output Formats

### graph.jsonl (Mode B/C)

```jsonl
{"op":"create","ts":"2026-01-15T10:00:00Z","entity":{"id":"per-00001","type":"Person","graph":"core/persons","labels":["employee"],"source":{"type":"scan","scan_id":"step2-r1"},"properties":{"name":"张三","roles":["项目经理"],"organizations":["某科技公司"]},"relations":[{"type":"works_at","target_id":"org-00002","direction":"forward","cardinality":"N:1","temporal":{"start":"2019-01","end":null},"confidence":"high"}],"created_at":"2026-01-15T10:00:00Z"}}
```

Required: `id`, `type`, `graph`, `source`, `created_at`. Optional: `labels`, `properties`, `relations`.

Relation fields: `type` + `target_id` required. Optional: `direction` (forward/reverse/bidirectional), `cardinality` (1:1/1:N/N:1/N:M), `temporal` ({start, end}), `evidence` (source entity ID), `confidence` (high/medium/low). See [relation-ontology.md](references/relation-ontology.md).

### schema.yaml (Mode B/C)

```yaml
meta:
  version: "2.0"
core_types:       # 8 fixed (BFO-aligned): Person, Organization, Project, Task, Document, Event, Note, Goal
domain_types:     # Discovered by Step 2 Track B, grouped by domain
namespaces:       # core/, work/*, personal/*, external/*, uncategorized/*
source_types:     # scan | runtime | manual | email | cloud | chat
relation_schema:  # Relation fields: type, target_id, direction, cardinality, temporal, evidence, confidence
relation_types:   # Core relation catalog grouped by source type pair
constraints:      # type_constraints (required props, enums), relation_constraints, id_pattern
inference_rules:  # Transitive subsidiary, symmetric partner, inverse works_at, etc.
schema_evolution:  # Version format, backward compatibility rules
```

### ontology.json (Mode A)

```json
{
  "meta": {"generated_by": "ontology-engineer", "source_files": [], "domain": "..."},
  "object_types": [{"name": "...", "english": "...", "core_properties": [], "confidence": "high|medium|low"}],
  "link_types": [{"from": "A", "relation": "verb", "to": "B", "cardinality": "1:N", "evidence": "..."}],
  "review_flags": [{"type": "promotion|merge|ambiguity|missing", "item": "...", "question": "..."}]
}
```

### review.md

1. Scan summary  2. Model overview  3. Object catalog  4. Relationship map  5. Review items  6. Cross-source merges  7. Data quality notes  8. Decision log

---

## Scripts

| Script | Mode | Purpose |
|--------|------|---------|
| `scripts/scan_filesystem.py` | B/C | File indexing, namespace inference, metadata extraction |
| `scripts/scan_directory.py` | A | File discovery with P1-P7 priority classification |
| `scripts/convert_doc.py` | A | .doc → .docx conversion |
| `scripts/extract_tables.py` | A | Table extraction from Word/Excel |

**Details**: [references/script-operations.md](references/script-operations.md)

---

## Agent Integration

| Component | Purpose | Status |
|-----------|---------|--------|
| `query_graph.py` | Search entities by type/name/graph/labels, traverse relations | Done |
| Runtime write | Agent appends new entities during conversation (Step 3) | Done |
| MCP Server | Expose graph as tools: `search_entities`, `get_relations` | Planned |
| Prompt injection | Agent auto-queries graph for context before handling tasks | Planned |

**Query tool usage**:
```bash
python query_graph.py stats                    # Overview
python query_graph.py search "关键词"           # Search
python query_graph.py type Person --limit 20   # By type
python query_graph.py get per-00001            # Details
python query_graph.py relations per-00001      # Relations
python query_graph.py domain --limit 30        # Domain terms
python query_graph.py export Person --format csv  # Export
```
