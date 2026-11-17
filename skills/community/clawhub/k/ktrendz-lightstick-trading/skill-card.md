## Description:

Trade K-pop artist lightstick tokens on the K-Trendz bonding curve market with price checks, trading signals, and buy or sell commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hans1329](https://clawhub.ai/user/hans1329)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to check K-Trendz token prices and signals, then optionally buy or sell one artist lightstick token through configured shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real buy or sell orders for K-Trendz tokens without script-level confirmation.

Mitigation: Require explicit user confirmation immediately before running buy or sell commands, and prefer quote-only review before execution.

Risk: The skill handles a K-Trendz API key and stores that key locally in plaintext.

Mitigation: Use an environment variable or secret manager where possible, restrict local config file permissions, and rotate the key if local configuration is exposed.

Risk: Unsafe API response parsing could run code if a compromised API response is interpolated into Python code.

Mitigation: Avoid running the current scripts against untrusted responses; safer versions should parse JSON through stdin or files and validate fields before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hans1329/skills/ktrendz-lightstick-trading)
- [ClawHub publisher profile](https://clawhub.ai/user/hans1329)
- [K-Trendz bot API](https://k-trendz.com/api/bot/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with shell command invocations and script output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call K-Trendz API endpoints through local shell scripts after configuration with a K-Trendz API key.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
