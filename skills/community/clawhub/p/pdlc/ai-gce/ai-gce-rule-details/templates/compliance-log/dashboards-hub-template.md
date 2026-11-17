<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "DASHBOARD_FRAMEWORK_CONTRACT.md"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project_id}"
templateVersion: "1.0.0"
templateSchemaLocked: true
---
# DASHBOARDS.md Hub Index — Template

This template defines the `management_framework/dashboards/DASHBOARDS.md` marker file.
Any package that detects "no hub exists" creates this file as part of Step 3 in the
Dashboard Framework Contract §4 contribution behavior.

AI-GCE generates this template because it is typically the first package to create the
`dashboards/` folder (the compliance dashboard is the first to exist in the family).
However, ANY package that finds no hub may create it — the contract is package-agnostic.

**Dashboard Framework Contract:** v1.0.0

---

```markdown
<!-- Dashboard hub | contract v1.0.0 -->

---
generatedBy: {first-contributing-package}
generatedVersion: {version}
source: DASHBOARD_FRAMEWORK_CONTRACT.md
generatedOn: {date}
ownership: generated
projectId: {project_id}
---

# Dashboards

Consolidated dashboard hub for **{project_name}** (Project ID: `{project_id}`).
Each AI-* package contributes its own dashboard here, identified by `generatedBy` front-matter.

---

## Contributing Dashboards

| Dashboard | File | Producer | Scope | Last Refreshed |
|-----------|------|----------|-------|:--------------:|
| Compliance | compliance-dashboard.md | AI-GCE | Per-project | {date} |
| Quality | quality-dashboard.md | AI-TGE | Per-project | {date} |
| Project Status | project-status-dashboard.md | AI-PILC | Per-project | {date} |
| Architecture | architecture-dashboard.md | AI-ADLC | Per-project | {date} |
| Backlog | backlog-dashboard.md | AI-POLC | Per-project | {date} |
| UX | ux-dashboard.md | AI-UXD | Per-project | {date} |
| Readiness | readiness-dashboard.md | AI-DWG | Per-project (snapshot) | {date} |
| Portfolio | portfolio-dashboard.md | AI-PPM | Portfolio | {date} |
| Flow | flow-dashboard.md | AI-FLO | Portfolio | {date} |
| Idea Pipeline | idea-pipeline-dashboard.md | AI-ILC | Portfolio | {date} |

> **Note:** Only rows for packages that have actually contributed are shown.
> Remove placeholder rows for packages not yet active.

---

## Conventions

- One file per package, named by concern (`{concern}-dashboard.md`).
- Producer identified by `generatedBy` front-matter (not by filename or folder).
- Dashboards are regenerated (not hand-maintained) — `ownership: generated`.
- Filter by `generatedBy` to identify a package's contribution.
- Detection: this file's presence means "a dashboard hub exists here."
- RAG legend: 🟢 On Track / 🟡 At Risk / 🔴 Off Track.
- Staleness: if a dashboard's `generatedOn` is older than its source's last-modified date, it is stale.

## Operating Mode

- **Project mode** (default): Per-project dashboards sit flat in this folder.
- **Portfolio mode** (>1 project): Portfolio dashboards (PPM/FLO/ILC) sit flat here;
  per-project dashboards are partitioned under `{Project ID}/` subfolders.

See `DASHBOARD_FRAMEWORK_CONTRACT.md` §2 for full mode definitions.

---

*Hub Version: 1.0.0 | Contract: DASHBOARD_FRAMEWORK_CONTRACT.md v1.0.0*
```

---

## Usage Notes for AI-GCE Core Generator

When AI-GCE generates the compliance dashboard, it also checks for the hub:

```
Step 8 (Dashboard generation):
1. Check: does management_framework/dashboards/DASHBOARDS.md exist?
2. IF NO → generate dashboards/ folder + DASHBOARDS.md from this template + compliance-dashboard.md
3. IF YES → refresh compliance-dashboard.md only + update AI-GCE row in hub
```

This template is the authoritative source for the hub marker structure.
Other packages reference it but do NOT embed their own copy — they read the existing hub.

---

*Template Version: 1.0.0 | Package: AI-GCE (hub creator, any package may also create)*
