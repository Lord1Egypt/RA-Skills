## Description:

Create tokens on-chain, check fee earnings, check Kibi Credit balance, trigger agent credit reload, and interact with KibiBot's Agent API and Kibi LLM Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kibubot](https://clawhub.ai/user/kibubot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect agents to KibiBot for token creation, fee and wallet lookups, Kibi Credit balance checks, credit reloads, and LLM gateway access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An enabled agent can create on-chain tokens or reload Kibi Credits from a trading wallet without a clearly required per-action confirmation step.

Mitigation: Require explicit confirmation before each token creation or credit reload, including amount, source wallet, chain, token details, platform, and expected cost or quota impact.

Risk: Authenticated use exposes the relevant API key, LLM prompts, account/profile data, and wallet-related operations to KibiBot.

Mitigation: Install only when the user trusts KibiBot for those operations and scope API-key permissions to the capabilities the agent actually needs.

## Reference(s):

- [KibiBot ClawHub Skill Page](https://clawhub.ai/kibubot/skills/kibi)
- [KibiBot Agent API](https://kibi.bot/agent)
- [KibiBot API Keys](https://kibi.bot/settings/api-keys)
- [Kibi LLM Gateway](https://kibi.bot/llm)
- [OpenClaw Setup](https://kibi.bot/llm/openclaw)
- [Kibi Credits](https://kibi.bot/credits)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON configuration examples, API request examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a KibiBot API key for authenticated API and gateway operations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
