# Workflow

1. Establish the fault timeline: user-perceived time, alarm trigger time, Kubernetes event time, deployment/configuration change time.
2. Prefer calling `huawei_root_cause_analyze`; if drill-down is needed, call rollout, dependency, change, network, node/pod diagnoser actions separately.
3. Workload rollout funnel has the highest priority: generation/observedGeneration, ReplicaSet, Pod Ready, Events, Logs, command/args, probes, image.
4. For dependency impact scope, use Service selector, Ingress backend, Pod Ready, and Node distribution to determine propagation paths.
5. For change impact scope, use audit logs, K8s historical events, AOM alarms, and current topology to verify the "change occurred before failure" causal chain.
6. For each root cause candidate, record supporting evidence, counter-evidence, data gaps, and remediation handoff.
7. Sort by impact scope, timeline alignment, evidence strength, and recoverability.
8. Output Top3 root causes, verification steps, impact scope, and remediation recommendations.
9. Clearly label low-confidence conclusions with required supplementary data.