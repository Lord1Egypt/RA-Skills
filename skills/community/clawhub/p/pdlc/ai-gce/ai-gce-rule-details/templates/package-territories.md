<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: {version}
source: ai-gce-rules/core-generator.md
generatedOn: {ISO-date}
ownership: generated
---

# Package Territory Registry

**Purpose:** Declares paths that belong to AI-* family package infrastructure.
Files in these paths are NOT subject to application compliance hooks.

**Used by:** Every hook prompt's "Package Territory Check" preamble.

## Excluded Zones

| Path Prefix | Owner Package | Reason |
|-------------|---------------|--------|
| `.governance/hooks/` | AI-GCE | Hook infrastructure |
| `rules/` | AI-DWG / AI-GCE | Steering file infrastructure |
| `.governance/agents/` | AI-GCE | Agent infrastructure |
| `.governance/` | AI-GCE | Governance rules, agents, logs |
| `compliance-log/` | AI-GCE | Audit trail (append-only) |
| `project-initiation/` | AI-PILC | Upstream lifecycle output |
| `architecture/` | AI-ADLC | Upstream lifecycle output |
| `management_framework/` | Shared | Cross-package governance spine |
| `docs/compliance-dashboard.md` | AI-GCE | Generated dashboard |
| `templates/` | AI-DWG | Planning templates |

## Custom Exclusions (Team-Added)

<!-- custom -->
<!-- Teams can add project-specific paths here that should not trigger hooks -->
<!-- Example: vendor/, third-party/, generated/ -->
<!-- custom -->

## Rules

1. This file is the SINGLE SOURCE OF TRUTH for hook exclusion zones.
2. AI-GCE reads this file during hook generation to populate the preamble.
3. Paths are prefix-matched (e.g., `.governance/` matches `.governance/rules/x.md`).
4. Team additions in the "Custom Exclusions" section survive re-derivation.
5. If a path is in this registry, NO hook should fire against files in that path.
