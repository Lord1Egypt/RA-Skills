## Description:

Compare patient pre-admission medication lists with inpatient orders to automatically identify omitted or duplicated medications and improve medication safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical, pharmacy, and care-team users can use this skill to compare structured pre-admission medication lists with inpatient orders for a single patient encounter. It flags omissions, duplicates, dose changes, and critical-drug warnings for manual pharmacist or physician review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The executable can produce misleading clinical reports if its reconciliation output is treated as a clinical decision.

Mitigation: Use the report only as a review aid and require pharmacist or physician confirmation before medication decisions.

Risk: The skill may expose identifiable patient data through input files, terminal output, or saved reports.

Mitigation: Use only de-identified or authorized patient data, and avoid printing full reports in shared or logged terminals.

Risk: Unnecessary or unpinned requirements can add installation uncertainty.

Mitigation: Remove unnecessary requirements or pin dependencies before installing in a real clinical or PHI-handling environment.

## Reference(s):

- [Medication Reconciliation ClawHub Page](https://clawhub.ai/aipoch-ai/skills/medication-reconciliation)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or text guidance with optional JSON reconciliation reports and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a JSON report file when an output path is provided; reports include continued, discontinued, new, duplicate, dose_changed, warning, and recommendation sections.]

## Skill Version(s):

1.0.0 (source: server release evidence, released 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
