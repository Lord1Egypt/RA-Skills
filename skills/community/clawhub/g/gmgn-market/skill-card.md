## Description:

Get crypto and meme token price charts, trending meme coin rankings by volume, newly launched launchpad tokens, and real-time token signals through GMGN CLI/API workflows on Solana, BSC, Base, or Ethereum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmgnai](https://clawhub.ai/user/gmgnai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market analysts use this skill to query GMGN market data for token candles, trending tokens, launchpad listings, and token signal feeds. It helps agents choose the correct gmgn-cli market command, interpret returned fields, and report token market data without relying on the GMGN website.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup may install an unpinned global npm CLI.

Mitigation: Install a reviewed, pinned gmgn-cli version before using the skill.

Risk: The skill requires GMGN credentials and includes first-time setup steps that handle key material.

Mitigation: Use a secure secret-entry path such as gmgn-cli config set-key, avoid exposing temporary private keys, and rotate or revoke the API key if it is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gmgnai/skills/gmgn-market)
- [GMGN API key setup](https://gmgn.ai/ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and summarized CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON field interpretation, rate-limit retry timing, and chain-specific token risk indicators.]

## Skill Version(s):

1.4.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
