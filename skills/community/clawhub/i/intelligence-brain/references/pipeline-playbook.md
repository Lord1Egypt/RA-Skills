# 8-Step Metabolic Pipeline — Operations Playbook

The pipeline transforms raw information into actionable intelligence. Every step is mandatory. Skipping steps produces noise, not insight.

## Pipeline SLA

- **Time budget**: 24 hours from ingestion to completion
- **Failure policy**: If any step cannot complete, flag for manual review, do not skip
- **Output format**: Markdown files in `company/data/signals/`
- **Model**: Steps 1-7 use free tier (zai/glm-4-flash). Step 8 uses premium for quality inference.

## Step 1: READ — Ingestion

**Goal**: Pull all incoming data into a single processing queue.

Sources:
- Department daily reports (`company/departments/*/reports/`)
- External feeds (RSS, news, research)
- CEO directives and strategy updates
- Customer feedback and inquiries
- System events (cron failures, errors, anomalies)

**Output**: `company/data/signals/raw/ingest_{YYYYMMDD}.md`

**Check**: Is the file non-empty? If no new data, skip to idle — do not force processing.

## Step 2: PARSE — Structuring

**Goal**: Extract structured fields from raw text.

For each document in the ingestion queue:
```markdown
- Source: {department}/{filename}
- Type: report | research | directive | feedback | alert
- Date: YYYY-MM-DD
- Author: {agent or human}
- Key entities: [person, product, platform, metric]
- Raw summary: {first-pass extraction}
```

**Output**: `company/data/signals/parsed/parsed_{YYYYMMDD}.md`

**Anti-pattern**: Parsing every word. The brain needs structure, not transcription.

## Step 3: DECOMPOSE — Atomization

**Goal**: Break structured content into atomic claims, data points, and actions.

Format:
```markdown
### Claims (assertions requiring verification)
- [C1] {claim text} — Source: {file} — Confidence: high|medium|low

### Data Points (quantifiable facts)
- [D1] {metric}: {value} — Source: {file} — Verified: yes|no

### Action Items (tasks derivable from this information)
- [A1] {action} — Priority: P0|P1|P2|P3 — Owner: {department}
```

**Output**: `company/data/signals/decomposed/decomposed_{YYYYMMDD}.md`

**Critical rule**: Confidence must be explicit. "High" = verified from 2+ sources. "Low" = single source, unverified.

## Step 4: ORGANIZE — Categorization

**Goal**: Tag and bucket every atom by domain and classification level.

Taxonomy:
```
Domain tags: #brand #sales #finance #legal #tech #market #ops #risk
Classification: 🔴TS 🟠C 🟡I 🟢P
Priority: P0 (urgent) / P1 (important) / P2 (standard) / P3 (background)
```

**Output**: `company/data/signals/organized/organized_{YYYYMMDD}.md`

**Rule**: If a tag doesn't exist in the taxonomy, create it and document it. Never use catch-all tags like #misc.

## Step 5: MERGE — Deduplication & Cross-Reference

**Goal**: Find duplicate information and contradictory claims.

Operations:
1. Compare new claims against existing knowledge base
2. Flag duplicates — keep the highest-confidence version
3. Flag contradictions — two claims that cannot both be true
4. Flag gaps — questions raised by new information that have no existing answer

**Output**: `company/data/signals/merged/merged_{YYYYMMDD}.md`

**Contradiction resolution**: When two claims conflict, the newer claim takes precedence ONLY if it comes from a more authoritative source. Otherwise, flag for human review.

## Step 6: USE — Application

**Goal**: Route processed intelligence to the departments that need it.

Routing rules:
```
#brand claims  → Brand department
#sales claims  → Sales department
#finance claims→ Finance department
#legal claims  → Legal department
#risk claims   → Inspector + Legal
#tech claims   → DataCenter
#market claims → CEO
```

**Output**: Messages dispatched to department shared folders.

## Step 7: DELETE — Cleanup

**Goal**: Remove processed raw data to prevent accumulation rot.

Delete policy:
- Raw ingest files → Delete after 24h (already parsed)
- Parsed files → Delete after 7 days (already decomposed)
- Decomposed files → Archive to 存藏库 (historical reference)
- Merged and organized files → Keep as knowledge base

**Output**: Clean workspace. Verified: `raw/` and `parsed/` directories are empty of files older than SLA.

**The rot principle**: Un-deleted data becomes noise. Noise drowns signal. A brain full of old facts can't think.

## Step 8: EXTRAPOLATE — Cross-File Inference

**Goal**: Generate insights that don't exist in any single document.

Process:
1. Load all active WISDOM_GRAPH nodes
2. Scan for new cross-domain connections
3. Generate ACTION_PIPELINE candidates
4. Identify ONE_MORE_THING insights

**Output**: Update `company/brain/upgrade/` with new inferences.

This step uses a premium model (deepseek-v4-pro or equivalent) because inference quality directly impacts strategic decisions. This is the one step where cost optimization takes a back seat to quality.

## Pipeline Health Checks

Weekly checklist:
- [ ] Has the pipeline run in the last 24 hours?
- [ ] Are `raw/` and `parsed/` directories clean of stale files?
- [ ] Any unresolved contradictions older than 7 days?
- [ ] WISDOM_GRAPH node count (should grow weekly)
- [ ] ACTION_PIPELINE P0 items (should never be empty — a brain with no urgent insights is a dead brain)
