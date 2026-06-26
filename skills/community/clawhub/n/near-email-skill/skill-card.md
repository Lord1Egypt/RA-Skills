## Description: <br>
Send and read blockchain-native emails using NEAR Email service for NEAR smart contract notifications and AI agent workflows with NEAR account identities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zavodil](https://clawhub.ai/user/zavodil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to add NEAR Email sending, reading, deletion, and count flows to smart contracts, wallet applications, and server-side AI agents. It is especially suited to mainnet NEAR account notifications and OutLayer-based email integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment keys, NEAR private keys, and email payloads may be exposed if copied into source code, client-side logs, or public plaintext flows. <br>
Mitigation: Keep credentials in secure secret storage, avoid client-side logging of keys or payloads, and use encrypted email for private content. <br>
Risk: Plaintext smart-contract notifications store email content publicly on the NEAR blockchain. <br>
Mitigation: Use plaintext sending only for non-sensitive automated notifications and choose encrypted email flows for private messages. <br>
Risk: Send, attachment, and delete operations can affect external recipients or user mailbox state. <br>
Mitigation: Require explicit user confirmation before sending attachments or deleting emails. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zavodil/near-email-skill) <br>
- [NEAR Email API Reference](api-reference.md) <br>
- [NEAR Email Code Examples](examples.md) <br>
- [OutLayer Dashboard](https://outlayer.fastnear.com/dashboard) <br>
- [OutLayer API Base](https://api.outlayer.fastnear.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Rust, JavaScript/TypeScript, Python, JSON, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include HTTPS API calls, NEAR transaction examples, and mainnet-only integration notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
