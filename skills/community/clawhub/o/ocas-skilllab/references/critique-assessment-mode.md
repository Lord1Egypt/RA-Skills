# Critique — Assessment Mode

`critique.assess` runs Phases 1-3 only. Reads and scores, never modifies files.

Decision table:
| User says... | Command |
|---|---|
| "assess", "grade", "score", "evaluate" | `critique.assess` |
| "check against rubric", "audit" (no "fix") | `critique.assess` |
| "critique" (ambiguous) | `critique.assess` → offer to fix |
| "improve", "fix", "make better" | `critique.run` |
| "review and fix" | `critique.run` |

After assessment, ask: "Want me to generate a plan and apply fixes?" — require confirmation before mutating.