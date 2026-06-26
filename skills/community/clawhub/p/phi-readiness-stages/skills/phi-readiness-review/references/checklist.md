# Review Checklist

## Phase 1: Scope

- name the workload
- name the environment
- define the deployment boundary
- identify expected data classes
- state whether PHI is excluded, planned, approved, or live

## Phase 2: HIPAA applicability

- determine whether the reviewed workflow likely implicates HIPAA
- determine likely role: covered entity, business associate, subcontractor, outside scope, or unclear
- note any dependency on customer deployment model or contract structure
- use `framework/applicability-role-matrix.md`
- use `health-app-and-api-scenarios.md` when apps, APIs, customer-hosted products, or consumer-health boundaries are involved

## Phase 3: Evidence inventory

- apply `framework/assessment-evidence-handling.md` before requesting, copying, or quoting artifacts
- collect repo and architecture evidence
- collect process and governance artifacts
- collect approval and contract artifacts
- collect live operational artifacts
- record missing artifacts explicitly
- check freshness using `framework/evidence-freshness.md`
- verify minimum artifacts using `framework/minimum-artifact-matrix.md`

## Phase 4: Source verification

- verify current official sources live
- separate current rule from proposed rule
- record access dates
- verify Privacy Rule, Breach Notification Rule, or state-law boundary sources when relevant

## Phase 5: Boundary and inheritance analysis

- identify inherited controls and retained responsibilities
- use `controls/shared-responsibility.md` when cloud, SaaS, or customer-hosted models are involved
- use `mobile-wearable-communications.md` when messages, device storage, lock-screen exposure, or wearables are in scope
- write a short regulatory-boundary note

## Phase 6: Stage analysis

- start at the lowest plausible stage and move upward only when the next stage is fully supported
- stop at the first stage whose next-stage requirements are not fully supported
- check every required domain
- use `mappings/hipaa-security-rule-crosswalk.md` when the assessment needs rule-level support or `PRS policy` labeling
- compare the case to the nearest example in `examples/` when stage calibration is uncertain
- document blockers that cap the stage

## Phase 7: Recommendations

- identify the minimum actions required for the next stage
- name the artifact that should exist after each action
- order by stage-gating impact first, then risk reduction, then effort
