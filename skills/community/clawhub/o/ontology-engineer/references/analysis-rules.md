# Analysis Rules

## Rules 1-7: Database/Schema Extraction (Mode A)

### Rule 1: Entity Identification (W3C Direct Mapping)

| Table Pattern | Maps To |
|--------------|---------|
| Independent business table | Object Type |
| Pure association table (only FKs + few attrs) | Link Type |
| Enum/dictionary table | Attribute value domain (don't model independently) |
| Technical table (logs, audit, temp) | Exclude |

Three-question test:
1. Do business people mention this concept daily?
2. Does it have an independent lifecycle (create → modify → archive)?
3. Can it exist independently (has own PK and business meaning)?

### Rule 2: Property Selection

- **Keep**: Fields with business decision value (max 15 per object type)
- **Exclude**: create_time, update_by, is_deleted, version, sort_order
- **Naming**: Business language ("客户名称" not "cust_nm"), keep original as annotation

### Rule 3: Promotion Judgment (Stanford Ontology 101)

Promote field to Object Type when:
- It has multiple dimensions of information (fare_class → pricing rules + refund policy + mileage)
- It needs its own properties (not just a value, but a "concept with substance")
- Multiple objects reference it (shared business entity)

Mark as `review_flag` for expert confirmation.

### Rule 4: Relationship Discovery

Evidence sources:
- **Foreign keys**: A has B's FK → A relates to B
- **Naming**: Fields ending in `_id`, `_code`, `_ref`
- **Business logic**: Semantics imply relationships even without FK
- **Association tables**: `_rel`, `_map`, `_link` or only two FKs → M:N

Each relationship needs: direction (A → verb → B), cardinality (1:1, 1:N, N:M), evidence.

### Rule 5: Cross-Source Entity Merging

- Identify same concept across systems (CRM.customer vs billing.party)
- Mark merge evidence: shared FK, naming similarity, semantic alignment
- Mark as `review_flag` for expert confirmation

### Rule 6: 30-Second Rule

- Every concept explainable to business person in 30 seconds
- If you can't explain it, adjust granularity
- Simple > complex; ontologies enrich incrementally

### Rule 7: Evidence Grading

| Source Type | Grade |
|------------|-------|
| SQL DDL with column + type + constraint | Definitive |
| Excel data dictionary with descriptions | Strong |
| Word document with table structure | Moderate |
| Requirements/architecture description | Inferred |
| Business logic or naming convention only | Weak |

---

## Rules 8-12: Knowledge Graph (Mode B/C)

### Rule 8: File Source Classification

| Level | Extensions | Step 2 Priority |
|-------|-----------|-----------------|
| **Core work docs** | .docx .doc .wps .pdf .xlsx .xls .et .pptx .ppt .dps | **Highest** — most users' primary output |
| Text docs | .md .txt .csv .tsv .rtf .odt .ods .odp | Medium — developer/note-taker format |
| Structured defs | .sql .ddl .yaml .yml .json .xml .graphql .proto | By content |
| Code files | .py .js .ts .go .rs .java etc. | No content analysis |

Office documents are the primary analysis target, not an edge case.

Must skip: node_modules, .git, __pycache__, .venv, venv, dist, build, site-packages, $RECYCLE.BIN.

### Rule 9: Project Structure Inference

- First-level directory = project grouping
- Second-level directory = specific project
- Project markers (README.md, package.json, .git) confirm boundaries
- Namespace convention: `core/`, `work/*`, `personal/*`, `external/*`, `uncategorized/*`

### Rule 10: Dual-Track Entity Discovery

Step 2 runs two tracks in parallel:

**Track A — Core Type Instantiation**: Extract instances of 8 core types (Person, Organization, Project, Task, Document, Event, Note, Goal) from document content.

**Track B — Domain Structure Discovery**: Cluster analysis to find naturally emerging domain knowledge structures. Not "leftovers from core types" — a parallel classification of how the user's professional knowledge is organized.

Domain type criteria (need 2+):
1. Appears in ≥3 files within the domain
2. Has describable attributes
3. Has nameable relationships with other domain concepts
4. Domain practitioners use this term daily (30-second rule)

Core types answer "what universal things exist in your world." Domain types answer "how is your professional knowledge organized."

### Rule 11: Smart Sampling

- Input is Step 1 index, not hardcoded filenames
- **Minimum 10% coverage** of total indexed documents
- Per-project scaling: ≤20 all, 21-100→30-50, 101-500→50-100, 501-2000→100-200, >2000→200-500
- Every subdirectory covered (2-3 files each)
- All file formats represented (don't skip .xlsx/.pptx)
- No time-based sorting; old docs can be more valuable
- Second round: high-value areas up to 30-50% coverage

### Rule 12: Cross-Project Concept Alignment

- Detection: similar attributes, similar relationship structure, overlapping descriptions
- Handling: mark as review_flag (type: merge), list candidates and evidence
- Never auto-merge: only flag, let user confirm

### Rule 13: Structured List Full Extraction

**Problem**: Sampling works for narrative documents (reports, memos) where information is distributed across paragraphs. But structured registries (client lists, asset inventories, contact directories) have zero redundancy — every row is a unique entity. Sampling these files loses data permanently.

**Detection** (two paths):

1. **Filename-based** (Phase 2.1, before reading): Match against patterns:
   - Chinese: 列表, 台账, 名单, 登记表, 花名册, 清单, 通讯录, 客户列表, 资产清册, 人员名册, 统计表
   - English: list, roster, directory, registry, inventory, catalog, manifest
   - Mark these for **mandatory full extraction** regardless of sampling quota

2. **Content-based** (Phase 2.2, during reading): If an opened file reveals:
   - Excel: Sequential numbered rows, each row = one entity with consistent columns
   - Word: Tables where each row has a name/company/person in the first column
   - Any format: Repeating structure where rows are independent entities, not parts of a narrative
   - → **Switch to full extraction mode mid-analysis**. Do not summarize. Extract every row.

**Extraction rules**:
- Read ALL sheets (Excel), ALL tables (Word)
- One entity per data row
- Map column headers to entity properties
- Preserve relationships encoded in the structure (e.g., "使用的产品" column → product usage relations)
- If >500 rows, batch into groups of 100 for processing

**Why this matters**: A real example — a client list Excel with 139 companies was sampled at 10%, yielding only 13 entities in the knowledge graph. The other 126 companies were invisible. Full extraction recovers 10x more entities from a single file at minimal additional cost.
