# Applicability and Role Triage

Use this reference when the scope or HIPAA role is ambiguous.

Read this with `framework/applicability-role-matrix.md`.

## Questions to answer

- Does the workload receive, maintain, transmit, process, or store PHI or ePHI now?
- Is the workload being prepared to do so later?
- Is the organization operating as a covered entity, business associate, subcontractor, or as infrastructure outside HIPAA scope for the specific workflow?
- Is the product offered on behalf of a covered entity or business associate, or selected by the individual for their own use?
- Does patient-directed API access change the role analysis?
- Is the answer dependent on a contract, customer deployment model, or service boundary that has not been shown?
- Can free text, uploads, exports, support channels, or logs introduce PHI into a workflow described as non-PHI?
- Are inherited controls or support access changing the role analysis?

Use `health-app-and-api-scenarios.md` when mobile apps, patient apps, connected devices, provider APIs, or consumer-health boundaries are involved.

If the boundary looks similar to a known archetype, compare it to the nearest example in `examples/` before finalizing scope and role language.

## Conservative defaults

- If PHI handling is only hypothetical and the current workload is restricted to non-PHI, treat the current state as PRS-0 or PRS-1 depending on implementation intent.
- If role depends on contract structure not provided, say `likely` and reduce confidence.
- If a vendor provides only commodity tooling with no access to PHI in the scoped model, do not assume BA status without evidence.
- If an app is chosen by the individual for their own use and no evidence shows it is acting on behalf of a regulated entity, do not assume HIPAA scope automatically.
- If a service stores or can access customer ePHI as part of its function, treat BA analysis as likely relevant and require evidence.
- If a non-PHI workflow can only theoretically or incidentally receive PHI through user-generated content, record the ingress risk and required boundary controls without inflating the current stage.
- If live forms, uploads, chat, support channels, logs, or similar workflows intentionally accept or routinely receive PHI, reassess the current scope as potentially PHI-bearing rather than treating it as a future-only risk.
- If deployment model changes the answer, split the assessment by deployment boundary.

## Role output language

Use one of:

- likely covered entity
- likely business associate
- likely subcontractor
- likely outside HIPAA scope for the reviewed workflow
- unclear from available evidence
