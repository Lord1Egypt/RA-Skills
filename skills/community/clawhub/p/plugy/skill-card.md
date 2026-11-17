## Description:

Solana trading skill for AI agents. Buy, sell, and create tokens across PumpFun, PumpSwap, LaunchLab, and Meteora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qualitydude](https://clawhub.ai/user/qualitydude)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to register a PLUGy wallet, authenticate to the PLUGy API, and direct agents to buy, sell, create, or monitor Solana tokens through the linked PLUGy action documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to handle wallet private keys and retain an API key.

Mitigation: Use minimal funds, require explicit human confirmation for trades and token creation, avoid storing secrets in agent memory or plaintext files, and rotate or revoke credentials if exposed.

Risk: The skill relies on mutable remote trading instructions and live API endpoints.

Mitigation: Review the remote PLUGy documents before installation and before high-impact actions, and only send the PLUGy API key to https://plugy.fun/api endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qualitydude/skills/plugy)
- [PLUGy Website](https://plugy.fun)
- [PLUGy Docs](https://plugy.fun/docs)
- [PLUGy Scope](https://plugy.fun/scope)
- [PLUGy Trade Guide](https://plugy.fun/trade.md)
- [PLUGy Create Guide](https://plugy.fun/create.md)
- [PLUGy Heartbeat Guide](https://plugy.fun/heartbeat.md)
- [PLUGy Security Rules](https://plugy.fun/rules.md)
- [PLUGy Skill Metadata](https://plugy.fun/skill.json)
- [PLUGy API Base](https://plugy.fun/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with curl examples, API parameters, and credential-handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to fetch mutable remote PLUGy action documents before performing trading, token creation, heartbeat, or security-rule workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
