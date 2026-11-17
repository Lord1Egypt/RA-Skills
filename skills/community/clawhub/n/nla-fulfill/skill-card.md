## Description:

Fulfill an existing NLA escrow by helping users submit fulfillment text, monitor arbitration, and collect approved tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlegls](https://clawhub.ai/user/mlegls)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect an existing NLA escrow, draft fulfillment text, submit it through the nla CLI, monitor arbitration, and collect tokens after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide wallet-backed commands that spend gas, post fulfillment text on-chain, or transfer tokens.

Mitigation: Manually review and approve each transaction, validate escrow and address values, and use a low-value wallet where possible.

Risk: The skill relies on a globally installed nla CLI without a pinned version in the artifact.

Mitigation: Install a pinned and verified nla release in an isolated environment before use.

Risk: Private key handling is part of the workflow.

Mitigation: Avoid exposing unrelated secrets and keep wallet credentials isolated from other agent or shell environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mlegls/skills/nla-fulfill)
- [Publisher profile](https://clawhub.ai/user/mlegls)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose wallet-backed blockchain commands that require user review before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
