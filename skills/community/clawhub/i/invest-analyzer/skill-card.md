## Description:

Invest Analyzer helps agents screen equities, analyze financial statements, calculate FCF-based valuation metrics, and draft position guidance for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litousteven](https://clawhub.ai/user/litousteven)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-oriented analysts use this skill to gather public financial data, screen A-share and Hong Kong equities, calculate FCF and owner earnings, and draft buy/hold/sell style reports. The reports are research support and require independent verification against official filings before any investment decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Baidu search credentials can be exposed if pasted into shell commands or stored in broadly readable files.

Mitigation: Configure keys through a secure secret mechanism where possible; if a file is unavoidable, restrict permissions and avoid pasting real keys into commands.

Risk: Financial figures or extracted PDF data can be stale, incomplete, or incorrectly parsed, leading to misleading valuation conclusions.

Mitigation: Verify key figures against official filings, prefer text-layer annual reports from official disclosure channels, and restart the analysis when a core data error is found.

Risk: The skill produces investment-oriented recommendations and position references that could be mistaken for automated trading advice.

Mitigation: Treat reports as research support only and do not grant the skill brokerage access or authority to place trades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litousteven/skills/invest-analyzer)
- [investTemplate V5.5.6](https://github.com/sunheyi6/investTemplate)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with tables, checklists, calculations, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include valuation assumptions, source-quality labels, risk notes, and position-sizing guidance for human review.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
