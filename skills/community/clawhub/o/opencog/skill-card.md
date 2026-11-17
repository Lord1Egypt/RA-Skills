## Description:

Trade on prediction markets. Create a local wallet, list markets, check prices, buy and sell outcome shares. Coming soon: create and fund markets directly from this skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xastraea](https://clawhub.ai/user/0xastraea)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to interact with Precog prediction markets from an agent, including wallet setup, market discovery, quotes, trades, and position checks. It supports testnet practice flows by default and mainnet flows only when explicitly selected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real wallet keys and stores PRIVATE_KEY in ~/.openclaw/.env.

Mitigation: Use a dedicated low-value wallet, verify the key file is owner-only readable, and avoid storing valuable mainnet keys there.

Risk: Installation provenance is unavailable for this release.

Mitigation: Install only from a repository and commit the user trusts, preferably one matching the declared homepage.

Risk: Mainnet commands and token approvals are real financial actions.

Mitigation: Use testnet by default, require explicit mainnet selection, quote before each trade, and get user confirmation before execution.

Risk: Custom RPC endpoints can observe signed transaction contents.

Mitigation: Use only trusted RPC endpoints when overriding the default public RPC configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xastraea/skills/opencog)
- [ClawHub-declared Homepage](https://github.com/openclaw/precog-skill)
- [Precog Documentation](https://learn.precog.markets)
- [Precog App](https://core.precog.markets)
- [MATE Token](https://matetoken.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and verbatim fenced command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before trading actions; mainnet commands use real funds and must be explicitly selected.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
