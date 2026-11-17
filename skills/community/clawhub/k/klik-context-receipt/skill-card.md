## Description:

Turn a short, redacted work update into a reviewable Context Receipt that records source, freshness, scope, authority, open questions, and a human-return condition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyixu](https://clawhub.ai/user/chengyixu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and agents use this skill after interruptions or handoffs to create a redacted Context Receipt that distinguishes current facts, allowed preparation, missing context, and when a person must take back control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may include sensitive source material in a handoff summary.

Mitigation: Provide only short redacted summaries and omit credentials, private transcripts, client data, financial data, health data, and other sensitive material.

Risk: A receipt could be mistaken for authorization to execute work or access systems.

Mitigation: Treat the receipt as a review aid only; return to a person for new access, judgment, external commitments, conflicting context, or tool action.

Risk: Context may be stale, missing, contradictory, or ambiguous.

Mitigation: State the gap or invalidator in the receipt and require human review before preparation continues.

Risk: The external Klik link is promotional or informational.

Mitigation: Open it only when choosing to learn about Klik; it is not required for the receipt workflow.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/chengyixu/skills/klik-context-receipt)
- [Klik pre-launch direction](https://pre.hiklik.ai/?utm_source=clawhub&utm_medium=companion_skill&utm_campaign=kickstarter_prelaunch&utm_content=context_receipt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown receipt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing; based on short redacted summaries supplied by the user.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
