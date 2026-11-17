## Description:

Provides commodity market analysis for steel, non-ferrous metals, energy chemicals, raw materials, and related supply-chain questions using Mysteel analysis services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyb92](https://clawhub.ai/user/wyb92)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, traders, procurement teams, and agents use this skill to request commodity price, supply-demand, inventory, and market trend analysis. The skill checks for a Mysteel API key, sends a focused query to the Mysteel analysis endpoint, and returns an expanded Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to store a Mysteel API key in a plaintext project file.

Mitigation: Use a protected local secret or environment variable for production credentials and avoid committing real API keys to the skill tree.

Risk: The documented exec command interpolates user-provided query text into a shell command.

Mitigation: Pass query arguments without shell interpolation, or strictly quote and validate untrusted query text before execution.

Risk: Market-analysis queries are sent to the Mysteel endpoint.

Mitigation: Use the skill only when the endpoint is trusted and avoid sending unnecessary sensitive business information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wyb92/skills/mysteel-marketanalysis)
- [API key configuration](references/api_key.md)
- [Mysteel analysis script](scripts/analyze.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown market analysis report with supporting configuration and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Mysteel API key and sends the market-analysis query to the Mysteel endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
