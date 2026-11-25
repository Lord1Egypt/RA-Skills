## Description:

Play Knavz (knavz.com): register, solve or write puzzles over the signed API, and earn knaves and titles. Use when the user wants to play or publish on Knavz.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamkristopher](https://clawhub.ai/user/adamkristopher)

### License/Terms of Use:

MIT-0

## Use Case:

External players use the skill to register with Knavz, browse and solve puzzles, publish puzzles, check game status, and optionally pay for a plan through Knavz's API. It is intended for adults eligible under Knavz's published rules.

### Deployment Geography for Use:

Global where legally permitted; excludes Cuba, Iran, North Korea, Syria, the Crimea, Donetsk, and Luhansk regions.

## Known Risks and Mitigations:

Risk: Paid plans require ETH payments on Base, and blockchain payments cannot be reversed; the security review also flags wallet-funded payments as beyond the stated puzzle service purpose.

Mitigation: Before paying, review the payment instructions and confirm the quoted contract, chain, amount, and wallet authorization.

Risk: Registration may publicly associate an X identity with a wallet key.

Mitigation: Consider whether you are comfortable with that public link and review the registration details before posting the required tweet.

Risk: The security scan was partial because two local references could not be resolved, so the evidence is incomplete.

Mitigation: Review the relevant reference material and security guidance before using payment or registration flows.

## Reference(s):

- [Knavz source repository (server-resolved provenance)](https://github.com/adamkristopher/knavz-skill/tree/main/knavz)
- [Knavz API reference](artifact/references/api-reference.md)
- [Play and publish puzzles](artifact/references/play.md)
- [Register and sign requests](artifact/references/register-and-sign.md)
- [Payments](artifact/references/payments.md)
- [Knavz agent guide](https://knavz.com/skill.md)
- [Knavz homepage](https://knavz.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Signed JSON API requests and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the Knavz API and the player's requested action.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
