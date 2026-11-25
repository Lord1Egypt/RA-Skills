## Description:

Assesses decision reversibility and risk at critical checkpoints

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow commands use this skill at consequential decision points to assess reversibility and decide whether to continue with a quick recommendation or escalate to War Room deliberation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can list audited sessions and interact with audit-history data; the security assessment is incomplete because a referenced local path and imported manager implementation were unavailable.

Mitigation: Review the audit-history access and behavior, and resolve the missing source context before relying on it in a sensitive workflow.

## Reference(s):

- [Attune plugin reference](https://github.com/athola/claude-night-market/tree/master/plugins/attune)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Structured checkpoint response in Markdown or YAML-like fields, with a recommendation or escalation orders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a reversibility score, selected mode, escalation decision, rationale, confidence, and user-confirmation requirement.]

## Skill Version(s):

1.10.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
