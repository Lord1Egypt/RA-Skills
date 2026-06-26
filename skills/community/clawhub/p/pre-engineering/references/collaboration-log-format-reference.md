# Collaboration Log Format Reference

## Log Format Rules

1. **Append only, never delete**: Collaboration documents only append new entries at the end — never delete or modify existing entries
2. **Uniform entry format**: Each entry starts with `## [time] Role — action description`, ends with `Status: <status_code>`
3. **Blank line between entries**: Every entry must be separated by a blank line, ensuring consistent and readable formatting
4. **Status declaration is mandatory and must be within an entry**: Every entry must include a status declaration line as the last line of the entry. **Status declarations must NEVER appear as standalone lines** — e.g., `Status: EXE_ING` cannot appear on its own line; it must be embedded within a complete entry
5. **Concise result summaries**: Content lines should be kept within 5 lines (excluding the status line)
6. **Standardized status codes**: Only the 7 fixed status codes may be used — no custom status codes
7. **Time must be obtained from system**: When writing a log entry, must first execute `date +"%Y-%m-%d %H:%M"` to get the current system time — never fill in time from memory or estimation

## Entry Format Template

```markdown
## [time] Role — <action description>
- Content line 1
- Content line 2
- Status: <status_code>
```

## Status Declaration Line Format

`Status: <status_code>` — The status code is the sole basis for agents to determine execution conditions; it must exactly match one of the 7 fixed status codes.

## Complete Example Log

```markdown
# Collaboration Log

## [2026-05-11 10:00] Human — Project Launch
- Initialized project, Planner please begin first planning cycle
- Status: PLN_WAIT

## [2026-05-11 14:00] Planner — Planning Started
- Goal: Implement user login feature
- Status: PLN_ING

## [2026-05-11 14:12] Planner — Requirement Planning Complete
- Requirement: Implement user login feature
- Approach highlights: JWT + bcrypt + React form library
- Status: REV_WAIT

## [2026-05-11 14:25] Reviewer — Requirement Review Approved
- Requirement reasonable, approach feasible, compatible with existing code
- Status: EXE_WAIT

## [2026-05-11 14:40] Executor — T1 Execution Complete
- Deliverable file: src/components/Login/index.tsx
- Key changes: Added login form component with form validation and submission logic
- Status: REV_WAIT

## [2026-05-11 15:00] Reviewer — Deliverable Review Rejected
- Rejection reason: Login component missing loading state and error message handling
- Status: EXE_WAIT

## [2026-05-11 15:10] Executor — T1 Re-execution Complete
- Deliverable file: src/components/Login/index.tsx (added loading and error handling)
- Status: REV_WAIT

## [2026-05-11 15:40] Reviewer — Deliverable Review Approved
- Status: PLN_WAIT

## [2026-05-11 16:10] Planner — Requirement Planning Complete
- Requirement: Implement user registration feature
- Status: REV_WAIT

... (loop continues until all features in project goals are delivered)

## [2026-05-11 17:35] Planner — No New Requirements Declaration
- No new requirements remaining in project goals
- Status: REV_WAIT

## [2026-05-11 17:45] Reviewer — Project Complete Confirmed
- Confirmed all project goals have been delivered
- Status: DONE
```