<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Portfolio Connector — Interface Specification (v1.0 Stub)

**Purpose:** Define the interface seam where future multi-project portfolio management capability will plug into AI-ILC. In v1.0, this is a **stub only** — AI-ILC operates in single-project-per-workspace context. This file documents what the connector looks like so v1.1+ can implement it without breaking the v1.0 contract.

---

## v1.0 Behavior (Current)

In v1.0, AI-ILC assumes:
- **One project per workspace at a time**
- Feature routing targets *the* project present in the workspace
- No project discovery, selection, or cross-project routing
- The user tells AI-ILC whether a project exists (Stage 6, Q: "Does a project exist?")

This means the Portfolio Connector is **not called** in v1.0. It exists as a design document only.

---

## Why This Exists Now

Designing the interface before it's needed ensures:
1. v1.0's routing logic won't need restructuring when multi-project support arrives
2. The handoff contract (briefs) won't change shape
3. Template structures are forward-compatible
4. The state file schema already has the right fields

---

## v1.1+ Interface (Planned)

When implemented, the Portfolio Connector will provide:

### Input (AI-ILC calls the connector with)

```
{
  "action": "find_project" | "list_projects" | "get_project_context",
  "idea_name": "{idea name}",
  "idea_domain": "{detected domain}",
  "idea_scale": "{small / medium / large}"
}
```

### Output (connector returns)

```
{
  "projects": [
    {
      "name": "{project name}",
      "path": "{workspace path or repo URL}",
      "has_pilc": true/false,
      "has_adlc": true/false,
      "has_dlc_backlog": true/false,
      "domain_match": 0.0–1.0,
      "status": "active" | "completed" | "on-hold"
    }
  ],
  "recommendation": {
    "project": "{best match name}",
    "confidence": 0.0–1.0,
    "rationale": "{why this project}"
  }
}
```

### Behaviors

| Action | What It Does |
|--------|-------------|
| `find_project` | Given the idea's domain and scale, find the best-matching active project |
| `list_projects` | Return all known projects (for user selection when confidence is low) |
| `get_project_context` | Return enough about a specific project to run the impact assessment |

---

## Integration Points in AI-ILC

The connector would plug in at **Stage 6, Step 2** (Determine Project Existence):

**v1.0 (current):** Ask user "Does a project exist?"
**v1.1+ (with connector):**
1. Call `list_projects` to see what's available
2. If projects exist, call `find_project` with the idea's context
3. Present recommendation: "This idea seems to fit project '{name}' (confidence: {X}). Agree?"
4. If user confirms → call `get_project_context` for the impact assessment
5. If no match or user says "new project" → route to AI-PILC

---

## What the Connector Needs to Know About Projects

To route effectively, the connector needs a **Project Registry** (v1.1+ artifact):

| Field | Purpose |
|-------|---------|
| Name | Human-readable project identifier |
| Path | Where the project workspace lives |
| Domain | What domain the project covers (for matching) |
| Status | Active / On-hold / Completed |
| Has AI-PILC output? | Can receive change requests? |
| Has AI-DLC v1 backlog? | Can receive feature briefs? |
| Key stakeholders | For impact assessment context |
| Architecture summary | For determining if an idea impacts architecture |

This registry does NOT exist in v1.0. It's a v1.1+ deliverable.

---

## Forward-Compatibility Guarantees

These v1.0 design choices are connector-ready:

| v1.0 Element | Forward-Compatible Because |
|-------------|---------------------------|
| State file `Route` field | Values (`new-project`, `change-request`, `feature-backlog`) don't change — connector just helps DETERMINE the route, not change the values |
| Brief templates | Same brief format regardless of how the project was identified (manually or via connector) |
| Impact assessment (4 questions) | Works identically whether project context came from user input or connector |
| Idea Register | Already tracks route and destination — connector adds precision, not new fields |

---

## What v1.1+ Would Add (Not Built Now)

1. **Project Registry** — persistent file tracking known projects
2. **Connector logic** — the matching algorithm (domain similarity, status filtering)
3. **Cross-workspace awareness** — reading projects from different paths/repos
4. **Auto-discovery** — scanning for `pilc-state.md` / workspace markers to find projects
5. **Confidence threshold** — when to present recommendation vs. ask user to choose

---

## Scope Boundary (Hard Rule)

The Portfolio Connector is **ONLY** about routing — helping AI-ILC find the right project to send a brief to. It is NOT:
- Portfolio health monitoring
- Resource allocation across projects
- Project prioritization or ranking
- Capacity planning
- Program management
- Portfolio analytics or dashboards

Those are separate capabilities that may become their own package or extension.

---

*Version: 1.0.0 (stub) | Part of AI-ILC — AI-Driven Idea Life Cycle*
