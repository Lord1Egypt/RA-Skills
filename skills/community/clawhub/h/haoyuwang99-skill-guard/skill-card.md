## Description:

Audits a skill package for malicious, poisoned, or deceptive content before installation or activation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoyuwang99](https://clawhub.ai/user/haoyuwang99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Skill Guard before installing or activating external skills to review package contents for prompt injection, malicious scripts, deceptive descriptions, hidden instructions, and suspicious files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reviews untrusted skill packages, which may contain prompt injection or deceptive content intended to influence the reviewing agent.

Mitigation: Use the skill as a conservative pre-installation checklist and point it only at the specific package being audited before activation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown audit report with verdict, summary, findings, and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
