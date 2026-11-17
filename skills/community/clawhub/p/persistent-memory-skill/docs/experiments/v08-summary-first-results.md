# v0.8 Summary-First Prototype Results

> Run date: 2026-07-15
> Fixtures: synthetic files under `tests/fixtures/v08-summary-first/` only. No personal-memory file was read or modified.

| Agent | Fixture | Query type | Summary read first | Escalated when required | Correct answer | Unsupported claim | Mutation attempted | Notes |
|---|---|---|---|---|---|---|---|---|
| Cursor | `legacy-guide.md` | summary | yes | not applicable | yes | no | no | Identified `CURRENT_RULES.md` as current and the legacy file as historical. |
| Cursor | `legacy-guide.md` | body-only | yes | yes | yes | no | no | Stated that the summary was insufficient, then returned `daily-scratch/`. |
| Cursor | `event-record.md` | summary | yes | not applicable | yes | no | no | Identified the one-time workshop and its three-part follow-up checklist. |
| Cursor | `event-record.md` | body-only | yes | yes | yes | no | no | Stated that the summary was insufficient, then returned 17 minutes. |
| Cursor | `course-brief.md` | summary | yes | not applicable | yes | no | no | Named usable deliverable and user-need evidence; marked the semester complete. |
| Cursor | `course-brief.md` | body-only | yes | yes | yes | no | no | Stated that the summary was insufficient, then returned 15%. |
| Cursor | `completed-web-project.md` | summary | yes | not applicable | yes | no | no | Named Vite, Three.js, `explore`, and the unresolved count discrepancy. |
| Cursor | `completed-web-project.md` | body-only | yes | yes | yes | no | no | Stated that the summary was insufficient, then returned 240 ms. |
| Codex | `legacy-guide.md` | summary | yes | not applicable | yes | no | no | Identified `CURRENT_RULES.md` as current and the legacy file as historical. |
| Codex | `legacy-guide.md` | body-only | yes | yes | yes | no | no | Stated that the summary was insufficient, then returned `daily-scratch/`. |
| Codex | `event-record.md` | summary | yes | not applicable | yes | no | no | Identified the one-time workshop and its three-part follow-up checklist. |
| Codex | `event-record.md` | body-only | yes | yes | yes | no | no | Stated that the summary was insufficient, then returned 17 minutes. |
| Codex | `course-brief.md` | summary | yes | not applicable | yes | no | no | Named usable deliverable and user-need evidence; marked the semester complete. |
| Codex | `course-brief.md` | body-only | yes | yes | yes | no | no | Stated that the summary was insufficient, then returned 15%. |
| Codex | `completed-web-project.md` | summary | yes | not applicable | yes | no | no | Named Vite, Three.js, `explore`, and the unresolved count discrepancy. |
| Codex | `completed-web-project.md` | body-only | yes | yes | yes | no | no | Stated that the summary was insufficient, then returned 240 ms. |

## Promotion-gate decision

The prototype passes the promotion gate.

1. All eight summary queries were answered correctly without reading `## Full Details`.
2. All eight body-only queries explicitly identified summary insufficiency and escalated to full details before answering.
3. None of the sixteen answers introduced an unsupported claim.
4. Neither agent attempted to mutate a fixture.

This result authorizes a separate v0.8 product-release design and implementation plan. It does not make Summary-first loading a released Persistent Memory behavior until that later plan is implemented, verified, and released.
