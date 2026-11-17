## Description:

Global Stock Analysis helps agents research US, China, and EU markets using Alpha Vantage-powered terminal workflows for quotes, fundamentals, technical indicators, macro data, forex, crypto, and options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luohy15](https://clawhub.ai/user/luohy15)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to guide market-data collection and analysis from the terminal. It supports company research, stock comparison, technical and fundamental analysis, macro monitoring, forex and crypto checks, and US options-chain review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unpinned external CLI package, marketdata-cli.

Mitigation: Install only from trusted package sources, pin a reviewed version in controlled environments, and avoid --force unless replacing an existing install is intended.

Risk: The skill requires an Alpha Vantage API key.

Mitigation: Expose only the ALPHAVANTAGE_API_KEY needed for the requested command and avoid placing keys in shared logs or outputs.

Risk: Financial market outputs can be stale, incomplete, or misread as investment advice.

Mitigation: Verify important results against authoritative sources and treat generated analysis as research support.

## Reference(s):

- [Fundamental Analysis](references/fundamentals.md)
- [Technical Analysis](references/technicals.md)
- [Macro & Market Overview](references/macro.md)
- [Sector / Multi-Stock Comparison](references/comparison.md)
- [Forex & Crypto](references/forex-crypto.md)
- [Options Chain](references/options.md)
- [Alpha Vantage](https://www.alphavantage.co)
- [Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key)
- [Declared Skill Source](https://github.com/alphavantage/alpha_vantage_mcp)
- [Installation Tutorial](https://www.youtube.com/watch?v=Z6DjYKN4uos)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and terminal command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires marketdata-cli and ALPHAVANTAGE_API_KEY; command results may be CSV or JSON depending on CLI flags.]

## Skill Version(s):

0.0.14 (source: release evidence and frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
