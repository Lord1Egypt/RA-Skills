## Description:

Create tokens on-chain, check fee earnings, check Kibi Credit balance, trigger agent credit reload, and interact with KibiBot's Agent API and Kibi LLM Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kibiagent](https://clawhub.ai/user/kibiagent)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage KibiBot token creation, account balances, fee earnings, credit reloads, and LLM Gateway configuration from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through financially consequential token creation and credit reload actions.

Mitigation: Require explicit user confirmation before token creation, manual credit reload, or reload-disable actions.

Risk: Agent Reload can move USDC or USDT from a configured trading wallet when enabled.

Mitigation: Use the least-privilege API key available and leave Agent Reload disabled unless the user intentionally wants agent-triggered reloads.

## Reference(s):

- [KibiBot Agent API Quick Reference](artifact/references/api.md)
- [KibiBot Skill Page](https://clawhub.ai/kibiagent/skills/kibibot-skill)
- [KibiBot](https://kibi.bot)
- [KibiBot Agent API](https://api.kibi.bot/agent/v1)
- [Kibi LLM Gateway](https://llm.kibi.bot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration snippets, API request examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated API calls that create tokens, query balances, reload credits, disable reload, or configure LLM Gateway access.]

## Skill Version(s):

1.5.2 (source: server release metadata and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
