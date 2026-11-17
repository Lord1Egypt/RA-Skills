<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 1: Workspace Detection

## Purpose

Scan the workspace to determine topology mode, identify installed packages, discover active projects, and establish the operational context for all subsequent routing.

---

## Steps

### Step 1: Determine Topology Mode

Scan for layer markers:

| Signal | Interpretation |
|--------|---------------|
| `ppm-state.md` exists locally + project markers exist locally | Mode 1 or Mode 2 |
| `ppm-state.md` exists locally + NO project markers locally | Mode 3 |
| NO `ppm-state.md` locally + project markers exist | FLO is in a project workspace (read-only tracking) |
| Portfolio register has >1 project with non-local `workspace_ref` | Mode 2 (hub + remote) |

Present to operator:

```
Topology Detection:

  Portfolio layer markers: {found / not found}
  Project layer markers:   {found / not found}
  
  Detected mode: {1 / 2 / 3 / project-only}
  
  Confirm? [Y] or select: [1] Co-located [2] Hub [3] Distributed
```

### Step 2: Scan for Installed Packages

For each package in the marker registry, check if its marker exists:

| Package | Marker | Found? | Location |
|---------|--------|:------:|----------|
| AI-ILC | `ilc-state.md` | {✅/❌} | {path} |
| AI-PILC | `pilc-state.md` | {✅/❌} | {path} |
| AI-PPM | `ppm-state.md` | {✅/❌} | {path} |
| AI-ADLC | `adlc-state.md` | {✅/❌} | {path} |
| AI-UXD | `uxd-state.md` | {✅/❌} | {path} |
| AI-POLC | `polc-state.md` | {✅/❌} | {path} |
| AI-DWG | `.kiro/steering/workspace-rules.md` | {✅/❌} | {path} |
| AI-GCE | `.compliance-state.json` | {✅/❌} | {path} |

### Step 3: Discover Active Projects

For each found marker, extract the `Project ID`:
- Read the state file's `project_id` field
- Group markers by Project ID (one project may have multiple package markers)
- Determine each project's current position (latest package with Status=In Progress or Complete)

```
Projects discovered:

  | # | Project ID | Name | Current Position | Status |
  |---|------------|------|-----------------|--------|
  | 1 | PRJ-ERP-2026-001 | {from PIP} | AI-ADLC | In Progress |
  | 2 | PRJ-CRM-2026-002 | {from PIP} | AI-PILC | Complete |
```

### Step 4: Remote Workspace Discovery (Mode 2/3 only)

If Mode 2 or 3:

```
Remote workspaces:

  I need paths to project workspaces I can't see locally.
  
  Add a remote project:
  • Path: {absolute path or URI}
  • Project ID: {if known, or I'll scan for it}
  
  [A] Add remote workspace
  [S] Skip (configure later)
  [D] Done adding
```

For each remote workspace provided:
- Verify path is accessible (if local filesystem)
- Scan for markers at that path
- Extract Project ID and position
- Store as `workspace_ref` in the project entry

### Step 5: Build Package Inventory Summary

```
Workspace Summary:

  Topology:    Mode {1/2/3}
  Packages:    {N} detected locally
  Projects:    {N} total ({N} local, {N} remote)
  
  Package availability:
  ✅ AI-PILC  ✅ AI-ADLC  ✅ AI-UXD  ✅ AI-POLC
  ✅ AI-DWG   ❌ AI-GCE   ❌ AI-TGE  ✅ AI-PPM
  
  Note: Packages not detected will be skipped in routing.
  If a package is installed later, run "routing table rebuild".
```

---

## Gate

**Approval required before proceeding to Stage 2.**

Operator must confirm:
- Topology mode is correct
- Project inventory is complete (no missing projects)
- Remote workspaces are configured (Mode 2/3)
- Package availability is accurate

---

## Transition

```
✅ Stage 1 complete. Workspace scanned.

  Mode: {X} | Projects: {N} | Packages: {N} available
  
  Moving to Stage 2: Building the routing table from the canonical
  family chain + project profiles.
```

Load `configure/routing-table-build.md`.

---

*Part of AI-FLO v1.0.0*
