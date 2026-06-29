# Workflow

1. Default: run quick check first; if healthy, output heartbeat summary directly.
2. If quick check finds anomalies, escalate to deep diagnosis or parallel inspection.
3. Classify and summarize issues by domain: Pod, Node, Event, AOM, ELB, Resource.
4. Label each risk as P0/P1/P2 with recommended responsible owner.
5. Output read-only report — no automatic remediation.
6. For actionable items, provide a handoff checklist to `huawei-cloud-cce-auto-remediation-runner` for confirmed execution.