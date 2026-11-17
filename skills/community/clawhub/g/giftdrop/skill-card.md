## Description:

Send, manage, and claim Solana crypto red packets via the GiftDrop API using wallet-authenticated requests and customizable gift parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiancookie](https://clawhub.ai/user/tiancookie)

### License/Terms of Use:


## Use Case:

Developers and agents use GiftDrop to register wallet-authenticated API keys and send, create, claim, and monitor Solana crypto red packets through GiftDrop REST endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes mainnet Solana wallet signing and an automated 0.5 SOL transfer workflow without clear human approval guardrails.

Mitigation: Require manual approval before any real transaction is signed or broadcast, and use a separate low-balance wallet for testing or operation.

Risk: The workflow depends on a third-party GiftDrop service, a host wallet address, and an external API domain.

Mitigation: Verify the host wallet and API domain independently before sending funds or registering API credentials.

Risk: API keys, wallet material, or private keys could be exposed through prompts, logs, or copied examples.

Mitigation: Never expose private keys or API keys in prompts or logs, and keep signing material outside agent-visible context.

## Reference(s):

- [GiftDrop ClawHub Skill Page](https://clawhub.ai/tiancookie/skills/giftdrop)
- [GiftDrop API Base URL](https://giftdrop.fun/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with curl commands and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet-authenticated REST request examples, rate limits, fees, token limits, and error-code guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
