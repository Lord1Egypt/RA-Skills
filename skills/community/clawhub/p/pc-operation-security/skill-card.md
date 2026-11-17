## Description:

Classifies and grades personal computer operations by security risk using the PC-OCS v1.0 standard for local and browser activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaiyu](https://clawhub.ai/user/huaiyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to assess individual or batches of PC operations for L1-L4 risk, audit operation safety, and get protective recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advisory keyword-based classification can misclassify ambiguous or context-dependent operations.

Mitigation: Review high-impact decisions manually and apply the skill's rule of treating uncertain or combined operations at the highest applicable level.

Risk: The shell helper echoes user-provided operation text in terminal output, and evidence.security cautions against untrusted strings containing terminal control characters.

Mitigation: Avoid passing untrusted terminal-control input to evaluate.sh until output escaping or sanitization is added; treat the helper as advisory only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaiyu/skills/pc-operation-security)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or terminal text with risk level, rationale, suggested mitigations, and related scenarios.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory classification output; shell helper accepts a single operation description.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
