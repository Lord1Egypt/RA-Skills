## Description:

Real-time crypto and stock hype detection using Reddit, CoinGecko, DEXScreener, and StockTwits with local Ollama-based signal validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peti0402](https://clawhub.ai/user/peti0402)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and schedule a Node.js scanner that monitors public market-hype sources, validates candidates with a local Ollama model, and writes pending alerts for an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags an undocumented trading-account monitor that may store account equity and positions.

Mitigation: Remove or explicitly review the trading-monitor integration before installation, use read-only brokerage credentials if retained, avoid storing raw account details in alerts.json, and restrict file permissions.

Risk: AI-generated market alerts can be influenced by public posts and may be misleading as financial advice.

Mitigation: Treat alerts as untrusted decision support, require human review before trading decisions, and keep alert generation separate from trade execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peti0402/skills/hype-scanner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code and configuration snippets; the scanner produces JSON alert files and log text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Node.js execution and an Ollama model endpoint; generated market alerts should be treated as untrusted decision support.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
