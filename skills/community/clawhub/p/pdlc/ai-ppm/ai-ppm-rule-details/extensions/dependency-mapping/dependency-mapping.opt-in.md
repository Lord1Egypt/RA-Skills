<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Cross-Project Dependency Mapping (Opt-In)

**ID:** E3
**Trigger:** Portfolio has >5 projects OR shared resources detected OR user mentions "dependencies", "blocked by", "dependency graph"
**Stages:** 4 (Prioritization), 7 (Roll-Up Ingestion)

---

## Detection

If any of the following are true, present this prompt:
- Portfolio Register has >5 active projects
- Two or more projects reference the same team, platform, or external vendor
- User says "dependencies", "blocked", "depends on", "prerequisite"

---

## Activation Prompt

```
🔗 Extension available: Cross-Project Dependency Mapping

This adds to Stages 4 and 7:
• Dependency graph (which projects depend on or block others)
• Critical path across the portfolio (longest dependency chain)
• Shared resource identification (teams/infrastructure used by multiple projects)
• Blocked-by detection during roll-up ingestion

Useful for: portfolios with shared teams, platform dependencies, or sequential initiatives.

Activate Dependency Mapping? [Yes / No]
```
