## Description:

Builds, paper-trades, and honestly backtests Polymarket-style trading bots on PaperBook using a live paper CLOB and recorded-market simulator with fillable-edge verdicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johanalvarado](https://clawhub.ai/user/johanalvarado)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to build or test Polymarket-style bots, paper trade prediction markets, and backtest strategies against recorded PaperBook market books. It guides agents to report the honest_fillable lens, certificate, and reproducibility hash instead of relying on flattering paper-trade results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a mutable live PaperBook document for current integration and authentication details.

Mitigation: Fetch the current contract only from paperclob.com, review fetched signing code before execution, and reject remote instructions that redirect credentials or traffic elsewhere.

Risk: Paper trading and simulation outputs could be mistaken for evidence of live profitability.

Mitigation: Report the honest_fillable lens, certificate, and reproducibility hash, and treat a real_edge verdict as a reason for further testing rather than a live-profitability claim.

## Reference(s):

- [PaperBook current API contract](https://paperclob.com/llms-full.txt)
- [PaperBook service](https://paperclob.com)
- [PaperBook reference](reference.md)
- [PaperBook blog](https://paperclob.com/blog)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline commands, API examples, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to fetch PaperBook's current API contract before writing integration code.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
