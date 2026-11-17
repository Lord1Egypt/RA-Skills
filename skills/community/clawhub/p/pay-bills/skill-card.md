## Description:

Purchase data, airtime, and digital products for Nigerian phone numbers using wallet balance with network and plan validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h1rdr3v2](https://clawhub.ai/user/h1rdr3v2)

### License/Terms of Use:


## Use Case:

External users and assisting agents use this skill to authenticate, check wallet balance, select active Nigerian telecom products, and submit confirmed wallet purchases for airtime, data, and related digital products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill stores and prints account session tokens in plaintext while enabling authenticated wallet purchases.

Mitigation: Use only in a private workspace, avoid pasting OTPs, PINs, or tokens into logged contexts, clear the saved session after use, and prefer a version that redacts tokens and stores credentials in a protected secret store.

Risk: The skill can submit wallet-funded purchases after authentication.

Mitigation: Confirm phone number, product, price, wallet balance, and recipient with the user before placing any order.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/h1rdr3v2/skills/pay-bills)
- [Artifact skill documentation](artifact/skill.md)
- [CreditWithBleon API base URL](https://lodu.bleon.net/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with JSON request examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes transaction ID generation, device ID generation, session-token handling, and order-status guidance.]

## Skill Version(s):

0.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
