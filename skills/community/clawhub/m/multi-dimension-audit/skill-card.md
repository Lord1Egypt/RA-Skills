## Description:

Full, deep audit of multi-file assets: fan out 4-7 parallel read-only subagents, verify high-severity findings in the lead reviewer, then synthesize. Produces dimension scores, a P0 list, and a phased remediation plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

Developers and reviewers use this skill to audit multi-file code, documentation, or skill assets and produce evidence-based findings, dimension scores, prioritized issues, and a phased remediation plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags conflicting subagent file-writing instructions and says its analysis is partial because referenced paths could not be resolved.

Mitigation: Review the conflicting instructions before installation and treat the scanner findings as incomplete until the unresolved paths are checked.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zuoyunlai/skills/multi-dimension-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown audit findings and remediation plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dimension scores, prioritized P0 findings, and phased recommendations]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
