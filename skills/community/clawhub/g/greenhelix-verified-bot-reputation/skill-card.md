## Description:

Build cryptographic PnL proof workflows for trading bots using Ed25519 signatures and Merkle claim chains, with Python and API integration examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-bot operators use this guide to design reputation workflows that sign bot identities, submit performance metrics, build Merkle claim chains, and query verification or reputation data through GreenHelix APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private signing keys may be exposed if generated keys, AGENT_SIGNING_KEY values, or example output are pasted into terminals, chats, logs, notebooks, or CI output.

Mitigation: Store signing keys in a proper secret store, avoid printing private keys, and rotate any key generated or exposed while following the examples.

Risk: Sandbox and production GreenHelix API usage can be confused, which may send real trading metrics or credentials to the wrong environment.

Mitigation: Choose the sandbox or production base URL explicitly, confirm whether an API key is required, and avoid sending real trading data or credentials until the target environment is clear.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mirni/skills/greenhelix-verified-bot-reputation)
- [ClawHub publisher profile](https://clawhub.ai/user/mirni)
- [GreenHelix API documentation](https://api.greenhelix.net/docs)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guide with inline Python, JSON, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; examples reference AGENT_SIGNING_KEY and GreenHelix sandbox or production endpoints.]

## Skill Version(s):

1.3.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
