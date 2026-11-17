## Description:

Lightweight CS and engineering issue triage with skeleton-first intake, conservative severity/category routing, ownership recommendation, no-response follow-up handling, and durable case tracking through either an issue tracker such as Linear or plain log files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yonghyeokrhee](https://clawhub.ai/user/yonghyeokrhee)

### License/Terms of Use:

MIT-0

## Use Case:

Support, CS operations, and engineering teams use this skill to convert customer-reported incidents, billing or entitlement delays, permission issues, and loose operational notes into structured triage records with severity, category, ownership, next actions, and follow-up handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Support cases may include customer identifiers, payment or order references, billing details, or incident notes that are persisted in plain local case logs.

Mitigation: Use an approved tracker when possible; if local logs are used, mask sensitive fields, keep logs out of source control and shared sync folders, restrict access, and define retention and deletion rules.

Risk: Weak or incomplete evidence may lead to incorrect severity, category, module, or owner recommendations.

Mitigation: Keep facts, guesses, and missing information separated; do not invent a root cause; keep the issue at TRIAGED when ownership confidence is low; move to RESOLVED only after explicit recovery confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yonghyeokrhee/skills/meta-coordinator)
- [Korean demo script](references/demo-script-ko.md)
- [Tracker workflow mapping](references/tracker-workflow.md)
- [Log-only workflow](references/log-only-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown triage record with optional JSONL-compatible case-event structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates facts, guesses, and missing information; includes issue skeleton, quick triage, likely module, owner suggestion, next actions, status move, and optional no-response follow-up.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
