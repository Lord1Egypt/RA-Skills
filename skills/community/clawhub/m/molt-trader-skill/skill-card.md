## Description:

Enables agents to build automated strategies for the Molt Trader simulator, including opening and closing long or short positions, tracking portfolio metrics, and viewing leaderboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[801c07](https://clawhub.ai/user/801c07)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to automate simulated trading workflows, inspect portfolio performance, and compete on Molt Trader leaderboards. It is intended for simulated trading, not real-money brokerage execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using this skill can open, close, and manage simulated trading positions.

Mitigation: Require human review or scoped policy controls before enabling state-changing trading actions.

Risk: The configured API endpoint receives the Molt Trader API key.

Mitigation: Use a scoped API key and set MOLT_TRADER_BASE_URL only to a trusted HTTPS Molt endpoint or an intentional local development server.

Risk: Automatic retries can repeat state-changing calls if the API does not guarantee idempotency.

Mitigation: Disable or limit retries for open, close, and locate operations unless the deployment confirms idempotent handling.

Risk: Dependency-chain issues may affect shared or CI environments.

Mitigation: Update and review the dependency chain before using the skill in CI or shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/801c07/skills/molt-trader-skill)
- [Molt Trader documentation](https://moltrader.ai/docs)
- [Molt Trader website](https://moltrader.ai)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces SDK usage guidance and executable examples that may call the configured Molt Trader API endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
