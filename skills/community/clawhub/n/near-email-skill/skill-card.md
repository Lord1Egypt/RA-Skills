## Description:

Send and read blockchain-native emails with the NEAR Email service for NEAR smart contract notifications and AI agents operating with a NEAR account identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zavodil](https://clawhub.ai/user/zavodil)

### License/Terms of Use:


## Use Case:

Developers building NEAR applications and agent workflows use this skill to generate integration guidance and code for sending, reading, counting, and deleting NEAR Email messages through OutLayer payment-key or NEAR transaction flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext email content is public on the NEAR blockchain.

Mitigation: Use plaintext sending only for non-private automated notifications, and use the encrypted email flow for private content.

Risk: The skill documents delete_email behavior without clear confirmation guidance.

Mitigation: Require explicit human confirmation before generating or executing any mailbox deletion action.

Risk: Payment keys and NEAR signing authority can expose account value or email capabilities to generated code.

Mitigation: Keep payment keys and private keys in approved secret storage, scope operational access where possible, and require user approval before signing NEAR transactions.

Risk: The examples include mutable global install and dependency patterns.

Mitigation: Prefer pinned local installs and pinned dependency versions before using generated commands in production workflows.

## Reference(s):

- [NEAR Email integration guide](artifact/SKILL.md)
- [NEAR Email API reference](artifact/api-reference.md)
- [NEAR Email code examples](artifact/examples.md)
- [ClawHub skill page](https://clawhub.ai/zavodil/skills/near-email-skill)
- [OutLayer dashboard](https://outlayer.fastnear.com/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, API request examples, and integration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Rust smart contract snippets, JavaScript/TypeScript and Python agent examples, NEAR transaction parsing guidance, and payment-key setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
