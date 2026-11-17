## Description:

Activates all CREATED conditions under a Gougoubi proposal with deterministic committee checks, optional minimum stake joining, and structured voting results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers with wallet and contract-call capability use this skill to activate all CREATED conditions for a Gougoubi proposal on BSC Mainnet, including committee membership checks, optional minimum staking, and per-condition voting result reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate live BSC Mainnet staking and voting transactions from a user's wallet.

Mitigation: Use it only when the on-chain effects are intended, review the stake amount and gas, and confirm each wallet transaction deliberately.

Risk: Automated operation could submit stake or vote transactions without a user's desired limits.

Mitigation: Avoid unattended use unless explicit stake and vote approval limits are added before execution.

## Reference(s):

- [Contract Methods](references/CONTRACT_METHODS.md)
- [Gougoubi Repository](https://github.com/gougoubi/gougoubi)
- [Gougoubi Website](https://gougoubi.ai)
- [ClawHub Skill Page](https://clawhub.ai/chinasong/skills/gougoubi-activate-created-conditions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with structured JSON success and failure results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns transaction hashes, condition counts, per-condition successes and failures, warnings, and next actions.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
