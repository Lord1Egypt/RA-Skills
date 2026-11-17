## Description:

omnifun helps agents discover, quote, trade, and launch memecoins across supported chains through omni.fun APIs, including market data, strategy analysis, rewards, webhooks, and spending controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xzcov](https://clawhub.ai/user/0xzcov)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to interact with omni.fun market, trading, token launch, reward, and webhook APIs. It supports read-only market workflows without credentials and authenticated workflows that return calldata for wallet signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated trading and token launch workflows can involve real wallets or funds when returned calldata is signed and submitted.

Mitigation: Use a dedicated low-balance wallet and require manual review before signing returned calldata, launching tokens, or claiming rewards.

Risk: Broad trading triggers or generic prompts may cause an agent to initiate unintended omni.fun actions.

Mitigation: Require explicit user intent for trade, launch, and reward actions, and configure strict per-trade limits, daily limits, approved chains, approved actions, and emergency pause controls.

Risk: The OMNIFUN_API_KEY is used for authenticated endpoints and may be exposed through logs or process telemetry.

Mitigation: Avoid logging the API key, prefer public no-auth endpoints for read-only market data, and rotate the key if exposure is suspected.

Risk: Webhook changes, reward claims, and signed transactions can create durable account or financial effects.

Mitigation: Require manual review before webhook changes, reward claims, token launches, or wallet-signing steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xzcov/skills/omnifun)
- [Publisher profile](https://clawhub.ai/user/0xzcov)
- [omni.fun homepage](https://omni.fun)
- [omni.fun app](https://app.omni.fun)
- [omni.fun API docs](https://app.omni.fun/.well-known/openapi.json)
- [omni.fun public SKILL.md](https://app.omni.fun/.well-known/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API request examples]

**Output Format:** [Markdown with curl command examples and JSON payload snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for command examples; authenticated workflows use OMNIFUN_API_KEY.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter and changelog mention 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
