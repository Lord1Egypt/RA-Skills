# Bower - OKRs

skill_okrs:
  - name: proposal_precision
    metric: fraction of executed proposals not subsequently undone
    direction: maximize
    target: 0.80
    evaluation_window: 30_runs
  - name: apply_success_rate
    metric: fraction of approved proposals successfully applied
    direction: maximize
    target: 0.95
    evaluation_window: 30_runs
  - name: auto_approve_precision
    metric: fraction of auto-approved proposals not subsequently undone
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs
  - name: data_integrity
    metric: fraction of Drive scans that pass schema validation
    direction: maximize
    target: 1.00
    evaluation_window: 30_runs