# AGENTS.md

Navigation map for the harness autonomous runtime. This file is for orientation only --
it contains no implementation details. Follow the links to find what you need.

---

## TABLE OF CONTENTS

| What you need | Where to find it |
|---------------|-----------------|
| Architecture maps | `docs/architecture/` |
| Execution plans | `docs/exec-plans/` |
| Specs | `docs/specs/` |
| Quality reports | `docs/quality/` |
| ADRs | `docs/architecture/adr/` |
| Tests | `tests/` |
| Memory / failure log | `MEMORY.md` |
| Constraints | `references/constraints.md` |
| Tool registry | `tools/TOOL_REGISTRY.md` |
| Agent definitions | `agents/` |
| Templates | `templates/` |
| Generated tool logs | `docs/generated/tool-logs/` |
| External references (human-curated) | `docs/references/` |
| Web search staging (pending review) | `docs/generated/search-staging/` |

---

## HOW TO USE THIS SKILL (reading order)

1. CLAUDE.md or AGENTS.md if present (base context -- this file)
2. CONFIG.yaml (runtime settings)
3. runtime/loop.md (execution model)
4. runtime/context-engineering.md (context budget rules)
5. runtime/status-management.md (restore checkpoint if resuming)
6. MEMORY.md (prior failure context)
7. agents/dispatcher.md (task decomposition model)
8. Begin the loop

---

## CURRENT SYSTEM STATE

**Phase:** active | maintenance | optimization
**Last cycle:** NNN
**Last quality report:** `docs/quality/QUALITY-NNN.md`
**Open bugs:** 0
**Entropy score:** --
**Active constraints:** N (from references/constraints.md)
**Recent failures:** N (from MEMORY.md)

---

## RULE
This file is navigation only. No implementation details live here.
Update `Current System State` at the end of every cycle.
