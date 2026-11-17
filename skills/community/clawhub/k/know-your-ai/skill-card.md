## Description:

Command-line skill for running Know Your AI red-team security evaluations, checking vulnerabilities, and reviewing results through the service API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhengwu](https://clawhub.ai/user/juhengwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use this skill to connect Codex to a Know Your AI account, verify the configured target product, launch red-team evaluation runs, and review security scores and run history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: KNOW_YOUR_AI_DSN includes an authentication token and can grant access to the linked Know Your AI account.

Mitigation: Store the DSN as a secret, avoid logging or sharing it, and rotate it from the official dashboard if exposed.

Risk: Running an evaluation creates remote evaluation runs in the configured Know Your AI account.

Mitigation: Use the doctor and target commands first to confirm the DSN, product, and API connectivity before launching evaluations.

## Reference(s):

- [Know Your AI homepage](https://knowyourai.hydrox.ai)
- [HydroxAI](https://hydrox.ai)
- [ClawHub skill page](https://clawhub.ai/juhengwu/skills/know-your-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text from Node.js CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node >=18 and the KNOW_YOUR_AI_DSN environment variable.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
