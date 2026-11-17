# Look — OKRs

Skill-level OKRs from `spec-ocas-journal.md`. All runs contribute to these metrics.

```yaml
skill_okrs:
  - name: draft_accuracy
    metric: fraction of ActionDrafts accepted without modification
    direction: maximize
    target: 0.75
    evaluation_window: 30_runs
  - name: domain_routing_accuracy
    metric: fraction of images routed to correct domain on first attempt
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs
  - name: confirmation_compliance
    metric: fraction of high-risk actions requiring confirmation before execution
    direction: maximize
    target: 1.0
    evaluation_window: 30_runs
```
