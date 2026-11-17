## Description:

Create crypto payment and withdrawal links for PayTheFlyPro across BSC, Ethereum, and TRON, with shareable URLs that include signature verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanlan](https://clawhub.ai/user/seanlan)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to generate PayTheFlyPro payment or withdrawal URLs and to query whether a payment or withdrawal serial number has been used on supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review reports that custom token payment or withdrawal links can be signed with incorrect non-native token amounts.

Mitigation: Avoid custom token payment or withdrawal links until token decimals are correctly resolved or explicitly verified before signing.

Risk: The skill signs payment and withdrawal authorization messages using a configured signer key.

Mitigation: Use a dedicated signer key, keep it separate from funded wallets, and verify npm dependencies before installation.

## Reference(s):

- [PayTheFlyPro homepage](https://pro.paythefly.com)
- [ClawHub skill page](https://clawhub.ai/seanlan/skills/paythefly)
- [Publisher profile](https://clawhub.ai/user/seanlan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with command-line examples and generated URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm dependencies, PayTheFlyPro project configuration, contract details, chain selection, and a dedicated signing key.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
