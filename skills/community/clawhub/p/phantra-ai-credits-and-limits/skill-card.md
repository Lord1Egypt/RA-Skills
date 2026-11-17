## Description:

Explains Phantra credit costs, balances, quotes, approval steps, draft rendering, refusals, and rate limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeropage-onryo](https://clawhub.ai/user/zeropage-onryo)

### License/Terms of Use:

MIT-0

## Use Case:

External Phantra users use this skill to check credit balances and history, understand quoted costs, and handle refusals or rate limits. It guides them to approve spending or scene text changes explicitly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credit-consuming renders or scene text replacements can affect the user's account or work.

Mitigation: Show the current quote or proposed replacement and wait for explicit approval before spending credits or replacing scene text.

Risk: The external Phantra service implementation is not included in this release.

Mitigation: Use the intended Phantra connector and review the live quoted cost and balance before approving a spend.

## Reference(s):

- [Phantra AI](https://phantra.ai)
- [ClawHub skill release](https://clawhub.ai/zeropage-onryo/skills/phantra-ai-credits-and-limits)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Conversational text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize current balance, quoted credit costs, and next steps from connector replies.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
