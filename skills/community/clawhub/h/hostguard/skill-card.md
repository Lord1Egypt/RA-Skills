## Description:

Checks whether OpenClaw is listening beyond localhost or running with elevated privileges, then offers a conservative lockdown fix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use HostGuard to assess local OpenClaw host binding, port listener state, and elevated-privilege execution before deciding whether a lockdown change is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect local environment files and process-listening state while assessing OpenClaw exposure.

Mitigation: Review the reported files and command results before acting on the assessment, and limit use to systems where this local inspection is authorized.

Risk: The optional lockdown fix can change an existing host binding to 127.0.0.1.

Mitigation: Approve file changes only when loopback binding is intended, and rely on the skill's backup behavior before editing.

## Reference(s):

- [HostGuard on ClawHub](https://clawhub.ai/tobewin/skills/hostguard)
- [tobewin publisher profile](https://clawhub.ai/user/tobewin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown report with inline shell commands and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill distinguishes runtime listener state from configuration file state and avoids claiming definite public exposure without stronger evidence.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
