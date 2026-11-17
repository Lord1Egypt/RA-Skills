## Description:

Manually arbitrate NLA escrow fulfillments as an alternative to the automated oracle. Use when the user wants to review pending arbitration requests, evaluate demands against fulfillments, and submit on-chain decisions. Supports both interactive and LLM-auto modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlegls](https://clawhub.ai/user/mlegls)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers who act as NLA escrow oracles use this skill to review pending fulfillments, decide whether to approve, reject, or skip them, and submit on-chain arbitration attestations through the nla CLI. The skill can also guide LLM-based auto arbitration when the user accepts the model, credential, and on-chain decision risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitration decisions are recorded as permanent on-chain attestations and may be difficult or impossible to reverse.

Mitigation: Use interactive arbitration first, verify the wallet is the escrow oracle, review the demand and fulfillment before deciding, and skip uncertain cases.

Risk: LLM-auto mode can approve or reject fulfillments incorrectly when model behavior or inputs are not fully trusted.

Mitigation: Avoid auto mode for all escrows unless the model and inputs are trusted; prefer manual review for high-value or ambiguous fulfillments.

Risk: Private keys and LLM API keys are sensitive, and credential flags or unverified CLI installs can expose them.

Mitigation: Use environment variables or a secrets manager instead of API-key flags, install the nla CLI from a verified pinned source, and run it in a least-privileged environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mlegls/skills/nla-arbitrate)
- [Publisher profile](https://clawhub.ai/user/mlegls)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides nla CLI arbitration flows; interactive and auto modes may submit permanent on-chain decisions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
