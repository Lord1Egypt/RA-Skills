## Description:

代码沙箱 provides Markdown guidance and report patterns for assessing untrusted AI-generated code before it is run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review potentially unsafe AI-generated code, identify risky patterns, and prepare a sandbox execution report before using a real isolated execution environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the Markdown guidance and examples for an implemented sandbox.

Mitigation: Treat the skill as advisory documentation and execute untrusted code only in a separately verified disposable container or VM with network, filesystem, resource, and environment isolation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-code-sandbox)
- [ClawHub publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reports with inline Python and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory only; does not ship an executable sandbox.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
