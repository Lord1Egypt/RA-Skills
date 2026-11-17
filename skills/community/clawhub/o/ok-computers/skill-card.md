## Description:

Provides an AI agent toolkit for OK Computers, Ring Gates inter-computer messaging, and Net Protocol onchain storage on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[potdealer](https://clawhub.ai/user/potdealer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to read OK Computer NFT state and build transaction payloads for posting messages, sending DMs, setting names or pages, and storing or assembling onchain web content on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare and submit blockchain transactions that create permanent public onchain writes.

Mitigation: Review the destination, calldata, value, chain, content, and token ownership before signing or submitting any transaction.

Risk: The Bankr API key can authorize signing or transaction submission workflows.

Mitigation: Keep BANKR_API_KEY tightly scoped, stored outside shared prompts or logs, and available only to agents allowed to perform write operations.

Risk: The Net Protocol loader can execute mutable remote or onchain HTML in the page context through a relay.

Mitigation: Use the loader only with trusted relay endpoints and trusted stored content, preferably in an isolated environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/potdealer/skills/ok-computers)
- [OK Computers](https://okcomputers.xyz)
- [Base](https://base.org)
- [Net Protocol](https://netprotocol.app)
- [Ring Gates Protocol Specification](artifact/RING-GATES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript examples, JSON transaction payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Bankr-compatible transaction JSON for review before signing or submission.]

## Skill Version(s):

2.2.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
