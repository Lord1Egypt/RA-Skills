# Knowledge Graph Workflow (Mode B/C)

## Infrastructure

```
{ontology_home}/
├── schema.yaml      ← 8 core types + discovered domain types
├── graph.jsonl      ← All entity data (append-only, soft-partitioned)
└── scan_filesystem.py (copy from skill scripts/)
```

## Step 1 — File Indexing (automated script, no LLM)

Run `scripts/scan_filesystem.py`:

```bash
python scripts/scan_filesystem.py --root /path/to/scan
python scripts/scan_filesystem.py --root /path --config namespace_rules.yaml
python scripts/scan_filesystem.py --root /path --extract-metadata
python scripts/scan_filesystem.py --root /path --dry-run
```

Creates Document + Project entities. Pure mechanical operation. See references/script-operations.md.

## Step 1.5 — User Scope Confirmation (MANDATORY)

After Step 1, **ask the user to review and confirm the analysis scope** before proceeding.

### Why this step exists

The user knows their own files best. Blindly sampling wastes compute on low-value folders (downloads, reference archives, AI-generated output). A 30-second user confirmation saves hours of misguided analysis.

### Procedure

1. Summarize Step 1 results: total projects, total documents, format distribution
2. Present a table of all projects/namespaces sorted by document count
3. Auto-suggest priorities based on heuristics:
   - Human work folders (contracts, meeting notes, client correspondence) → 重点
   - AI-generated folders (generate-docx.py, batch output) → 普通
   - Downloads, caches, reference archives → 忽略
4. Ask the user to confirm or adjust:
   - **重点** (priority): 2-3x normal sampling rate
   - **普通** (normal): default sampling rate
   - **忽略** (skip): excluded from Step 2 entirely
   - **全部** (all): accept defaults, analyze everything — user explicitly chooses to skip prioritization
5. User can also flag specific subfolders (e.g., "DM6 in Downloads is email, treat as 重点")

### Rules

- **Never skip this step.** Even experienced users benefit from reviewing the scan before committing compute.
- Respect "全部" — if the user wants everything analyzed, don't argue. Just apply default sampling rates.
- Store user choices in a `scope_config.json` alongside graph.jsonl for reproducibility.
- If the scan is small (<500 docs), suggest "全部" as default but still ask.

## Step 2 — Semantic Analysis (LLM, core step)

### Phase 2.1: Sampling

Minimum **10% coverage** of non-ignored documents (per Step 1.5 scope). Two rounds: wide → deep.

**Wide sampling**: Cover all non-ignored projects, all subdirectories, all formats. Per-project amounts scale with size (see Rule 11 in analysis-rules.md). 重点 projects get 2-3x sampling.

**Coverage validation**: After sampling, verify every non-ignored Project and every major subdirectory has representation. Fill gaps.

**Deep sampling**: After Phase 2.2, increase to 30-50% for high-value areas (≥10 named entities found, multiple formats coexist, new domain term clusters discovered, client/project names in path).

Stop when 5 consecutive docs yield no new entities or terms.

**Structured List Detection (Rule 13 — MANDATORY)**:

Before sampling, scan Step 1 index for files whose names match structured list patterns (列表/台账/名单/登记表/花名册/清单/通讯录/客户列表/list/roster/registry/inventory/catalog). These files are **exempt from sampling** — they go directly to Phase 2.2 for full extraction (every row, every sheet). Rationale: structured registries have zero information redundancy; sampling them loses entities permanently.

### Phase 2.2: LLM Document Reading

#### Pre-check: Project Environment Validation (MANDATORY)

Before reading any project's documents:

1. Read project context files (CLAUDE.md, README.md, etc.) if they exist
2. Determine document origin:
   - References to `generate-docx.py`, `python-docx`, batch generation → **AI-generated, deprioritize**
   - Timestamps clustered on same day, numbered filenames, similar sizes → batch generation signals
   - Contracts, meeting notes, handmade Excel, client correspondence → **human-written, highest priority**
3. Spend analysis budget on human-written work documents, not AI output

#### Pre-check: Directory Structure Analysis (free information)

File paths reveal domain structure without reading content:
- `工作记录/某部委项目/` → client project exists
- `Desktop/学习资料/` → personal learning area

#### Reading Office/PDF Files (MANDATORY, not optional)

Most users' core work is in Office formats. These are the PRIMARY target.

| Format | Method |
|--------|--------|
| .docx | python-docx: full text + all tables + embedded images |
| .doc/.wps | Convert via pywin32/LibreOffice → .docx → extract |
| .pdf | Read tool (direct) or PyMuPDF for text + images |
| .xlsx/.xls/.et | openpyxl/xlrd: **all sheets**, headers, first N rows. Sheet names are domain signals. Contains client lists, budgets, KPI tracking. |
| .pptx/.ppt/.dps | python-pptx: **all slides** + notes. Strategy summaries, client pitches. Info density often higher than Word. |
| .md/.txt | Read tool directly |

**Subagents must be `general-purpose` type** (with Bash). Never use `Explore` type for Phase 2.2.

**Never skip a file because it's binary.** Extract text with tools, then analyze.

#### Per-Document LLM Analysis

For each document, first determine its **document class**:

| Class | Examples | Extraction Mode |
|-------|----------|----------------|
| **Structured list** | Client lists, asset registers, contact directories, inventories, ledgers | **Full extraction**: every row = one entity, all columns = properties |
| **Narrative document** | Reports, memos, proposals, meeting notes, emails | **Semantic extraction**: summary + Track A + Track B (below) |

**If structured list** (Rule 13): Do NOT summarize. Read all sheets/tables, extract every data row as an independent entity. Map column headers to properties. This is non-negotiable — a 139-row client list must produce ~139 entities, not a 3-sentence summary.

**If narrative document**, extract:

**A. Understanding**: 1-2 sentence summary, domain, document type, knowledge density rating. High density → flag for deep sampling.

**B. Track A (Core Instances)**: Named persons (with role), organizations (with type), events (with dates), goals (with metrics), tasks, notes.

**C. Track B (Domain Terms)**: Professional vocabulary (no quantity limit), term relationships, domain classification (let it emerge, don't predefine).

**Content-based reclassification**: If you open a file expecting narrative content but discover it's actually a structured list (e.g., a .docx that's entirely tables of names), switch to full extraction mode immediately. Don't force narrative analysis on tabular data.

#### Image Analysis

.docx/.pdf embedded images (architecture diagrams, ER diagrams, flowcharts) → multimodal LLM visual analysis. Extract nodes and relationships. If LLM doesn't support images, note in review.md.

#### Large Document Chunking

>50KB text: split by sections, analyze each, merge in Phase 2.3.

#### Parallel Processing

>50 docs: split by Project, one general-purpose subagent per Project. Main agent aggregates in Phase 2.3.

### Phase 2.3: Aggregation

**Track A**: Deduplicate persons/organizations across documents. Same name + consistent context → merge, add labels for all projects. Unclear → review_flag.

**Track B**: Aggregate all term annotations → cluster by co-occurrence and semantic similarity → identify domain centers → name domains → identify core types within each domain → map inter-type relationships.

**Domains emerge from data, not predefined.**

### Phase 2.4: Cross-Project Alignment (Rule 12)

### Phase 2.5: Output

| Output | Target |
|--------|--------|
| Core type instances | graph.jsonl |
| Domain definitions | schema.yaml → domain_types |
| Domain type definitions | schema.yaml → domain_types → types |
| Domain instances | graph.jsonl |
| Review report | review.md |

## Step 3 — Runtime Evolution

Agent enriches the knowledge graph during daily conversations. `source.type = "runtime"`.

### Trigger Conditions

The agent should check and potentially update the graph when the user:
- Mentions a person with role/org context (e.g., "跟张三开了个会，他是XX的产品经理")
- Discusses events with dates (e.g., "上周五某IT系统项目通过验收了")
- Makes strategic decisions or key observations worth preserving
- Mentions new organizations, clients, or partners

### Procedure

1. **Check**: Query graph for existing entity (`python query_graph.py search "name"`)
2. **Compare**: If found, verify info is consistent. If new info, note but don't overwrite.
3. **Append**: If not found, create new entity with `source.type = "runtime"` and conversation context.

### Rules

- **Lightweight**: 1-3 entities per conversation max. This is passive enrichment, not a re-scan.
- **Evidence-based**: Only append what the user explicitly stated. Don't infer or guess.
- **Append-only**: Never modify or delete scan-derived entities. Runtime entities have lower authority than scan-derived ones.
- **Conflict handling**: If runtime info contradicts scan-derived data, note the conflict in a Note entity rather than overwriting.

## Mode C: External Data Scanning

Same as Mode B, but: source.target = "external", namespace = `external/{id}`, no prior knowledge assumed, can combine with Mode A for database schemas.

## Future Data Sources

| Source | Adapter | source.type |
|--------|---------|-------------|
| Email (Outlook/Gmail) | .ost/.pst or IMAP/API | email |
| Cloud drives | Sync directory or API | cloud |
| Chat records (WeChat/Slack) | Export or API | chat |
| Database | DDL/data dictionary (Mode A) | database |

## Backup and Migration

Everything is files. Copy directory, git commit, or cloud sync. graph.jsonl is append-only plain text. Filter by `graph` field to export subsets.
