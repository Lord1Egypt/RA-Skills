# Output Templates

## A) Team roster table
| Agent ID | Role | Mission | Inputs | Outputs | Depends on | Escalates to |
|---|---|---|---|---|---|---|
| team-leader | Team Leader | Intake, dispatch, stage control, final merge | User request | Stage plans, delegated tasks, final report | all specialists | user |
| product-manager | PM | Own scope/priorities | Business goals | PRD, priorities | team-leader | team-leader |

## A.1) Split/Merge rationale table
| Role | function_and_value | why_split_or_not | unique_artifact | authority_boundary | dependency_count | expected_parallel_gain |
|---|---|---|---|---|---:|---|
| product-manager | Turns goals into execution-ready scope and priorities | Needs distinct product decision loop | PRD + priority plan | scope/prioritization | 3 | medium |

## B) Interaction flow
1. PM decomposes goal into workstreams.
2. Architect defines technical approach and interfaces.
3. Engineers implement in parallel where possible.
4. QA validates acceptance criteria.
5. PM consolidates results and reports.

## C) Channel binding checklist
- [ ] Confirm binding mode: Single-Bot Mode / Multi-Bot Group Mode
- [ ] Confirm target channel(s): Telegram / Discord / DingTalk / Feishu / ...
- [ ] Map each agent to its channel identity/bot.
- [ ] For Multi-Bot Group Mode: add all role bots into one shared group.
- [ ] Configure group-level routing (`groupPolicy`, `requireMention`, allowlist/routing).
- [ ] Verify permissions and routing.
- [ ] Perform activation ping for each agent.
- [ ] Run end-to-end smoke test.

## D) Smoke test prompt
"Create a minimal feature plan, implement skeleton tasks by role, report blockers, and return a final consolidated update."

## E) Final handoff summary
- Confirmed roles:
- Collaboration protocol:
- Agent creation plan:
- Channel binding steps:
- Validation results:
- Skill install report (requested / installed / blocked, with source+version+risk notes+scanner_used):
- Security report JSON (schema-based):
- Remaining manual actions:

## F) Security report JSON block
```json
{
  "summary": {"requested": 0, "installed": 0, "blocked": 0, "skipped": 0},
  "items": []
}
```
