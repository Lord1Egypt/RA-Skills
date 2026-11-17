# Change Request · {{ project.name }}

> Any baseline-deviating change to scope / schedule / resource / cost must be raised via this form and implemented only after CCB review.

## Change Summary
- **Change Request (CR)**: {{ cr.id }}
- **Requester**: {{ cr.requester }}
- **Date Raised**: {{ cr.date }}
- **Related Stage/Gate**: {{ cr.gate }}

## Change Content
| Item | Current State (Baseline) | Proposed After Change |
|----|--------------|----------|
| Scope | {{ cr.scope_before }} | {{ cr.scope_after }} |
| Schedule | {{ cr.schedule_before }} | {{ cr.schedule_after }} |
| Cost | {{ cr.cost_before }} | {{ cr.cost_after }} |
| Resource | {{ cr.resource_before }} | {{ cr.resource_after }} |

## Rationale
{{ cr.rationale }}

## Impact Assessment
- **Impact on critical path / milestones**: {{ cr.impact_schedule }}
- **Impact on budget / BAC**: {{ cr.impact_cost }}
- **Impact on quality / risk**: {{ cr.impact_risk }}
- **Impact on dependent components**: {{ cr.impact_dependency }}

## CCB Review Conclusion
| Role | Decision (Approve/Approve with Conditions/Reject) | Comments | Date |
|------|------------------------------|------|------|
| Sponsor |  |  |  |
| Project Manager (PM) |  |  |  |
| Governance Committee Chair |  |  |  |

> The conclusion must be synced into `change_log` to form the traceability chain; changes must not be implemented without approval.
