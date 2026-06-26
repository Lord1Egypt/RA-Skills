# Final Deliverable Sample

Use this structure when handing results to the user.

## 1) Confirmed Team Roles
- Core: ...
- Optional: ...
- Deferred: ...

## 2) Agent Contracts
| Agent ID | Mission | Primary Output | Dependencies | Escalation |
|---|---|---|---|---|
| product-manager | ... | ... | ... | ... |

## 3) Collaboration Workflow
1. ...
2. ...
3. ...

## 3.1) Stage Deliverables with Paths (mandatory)
| Stage | Owner | Deliverable | Path |
|---|---|---|---|
| Requirement | 产品经理 | PRD | /workspace-<team>/shared/requirements/prd.md |
| Architecture | 技术架构师 | Arch spec | /workspace-<team>/shared/architecture/spec.md |
| UX | 交互设计师 | UI/UX package | /workspace-<team>/shared/design/ |
| Implementation | 全栈工程师 | Source bundle | /workspace-<team>/shared/implementation/ |
| QA | 测试工程师 | Test report | /workspace-<team>/shared/qa/report.md |

## 4) Protocol Summary
- Delegation envelope required: objective/context/output/deadline
- Status states: accepted/blocked/done
- Return-path mandatory for completion
- Timeout + escalation policy

## 5) Channel Binding Checklist
- [ ] Role-to-channel identity mapping confirmed
- [ ] Bindings configured
- [ ] Permissions validated
- [ ] Per-agent activation ping passed
- [ ] End-to-end smoke test passed

## 6) Operator Actions Remaining
- ...

## 7) Security Summary (mandatory)
- Security scanner used: skill-vetter / fallback
- Skills reviewed: ...
- Risk classification summary: LOW/MEDIUM/HIGH/EXTREME counts
- Blocked-for-review items: ...
- Install decisions and reasons: ...

## 8) Team Leader Boundary Check
- Confirm team-leader did not produce specialist implementation artifacts
- Confirm team-leader only orchestrated + communicated

## 9) Channel Binding Blueprints (provided automatically after report)
- Single-Bot Mode plan
- Multi-Bot Group Mode plan (with groupPolicy, requireMention, routing notes)

## 10) Runtime Progress Log Summary
- Stage by stage who-did-what timeline
- Each stage deliverable path and completion status

## 11) Smoke Test Prompt
"..."
