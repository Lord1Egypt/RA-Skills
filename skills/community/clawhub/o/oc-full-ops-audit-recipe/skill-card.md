## Description:

End-to-end OpenClaw audit and remediation recipe for gateway, channels, nodes, security, and memory sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyezir](https://clawhub.ai/user/xyezir)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to run a repeatable OpenClaw operational audit, prioritize findings, verify fixes, and document outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may lead an agent to propose disruptive operational fixes.

Mitigation: Keep explicit approval gates in place before applying changes, especially for gateway, security, node, or channel operations.

Risk: Audit outcomes written to memory could expose sensitive operational details.

Mitigation: Record only necessary summaries and avoid storing secrets, credentials, or sensitive infrastructure details.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise operational tables, action lists, verification notes, and command suggestions when appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include memory update summaries for daily and shared operational records.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
