## Description:

Screens and ranks U.S.-listed low-float, low-priced common stocks, ordinary shares, and ADR/ADS securities for extreme squeeze candidates while checking catalysts, liquidity, supply, halts, dilution, and execution risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinjobs](https://clawhub.ai/user/qinjobs)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, traders, and research-oriented users, especially in Asia-Pacific time zones, use this skill to screen U.S. premarket, regular-session, and after-hours movers, then produce watchlists, status labels, risk flags, and verification checklists. The skill is for general software, data processing, and quantitative research workflows, not personalized investment advice or long-term valuation.

### Deployment Geography for Use:

Asia-Pacific users monitoring U.S. markets

## Known Risks and Mitigations:

Risk: Automated status labels may look actionable even when key trading-safety evidence is missing or stale.

Mitigation: Treat labels as screening and research outputs; independently verify halt status, current SEC and issuer supply risk, primary-source catalyst evidence, spreads, VWAP, and turnover before making any trading decision.

Risk: Low-float, low-priced, halted, or post-split stocks can become illiquid, gap through stops, or lose value rapidly.

Mitigation: Use conservative position sizing, avoid market orders in premarket or halt-resumption conditions, cap same-day risk, and reduce or avoid exposure when supply, spread, halt, or data-quality checks are unresolved.

Risk: The skill covers securities-screening workflows that may be regulated differently across user jurisdictions.

Mitigation: Use the output as general-purpose software and data-processing guidance only; obtain qualified legal or licensed financial advice before using it for public sale, client-directed alerts, regulated advice, brokerage, or automated trading.

## Reference(s):

- [Factor Model](references/factor-model.md)
- [2026 Extreme-Move Case Studies](references/case-studies-2026.md)
- [500% Extreme-Move Intraday Playbook](references/intraday-500pct-playbook.md)
- [CYCU 5-Minute Case Study](references/cycu-2026-07-30.md)
- [CYCU Company Press Release](https://investors.cycurion.com/pr/cycurion-lands-largest-contract-in-company-history-546-million-10year-award-with-top5-global-consulting-firm)
- [CYCU SEC S-1](https://www.sec.gov/Archives/edgar/data/1868419/000149315226031976/forms-1.htm)
- [CYCU SEC Form 8-K](https://www.sec.gov/Archives/edgar/data/1868419/000162828026048496/cycu-20260710.htm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and reports, JSON scoring output, CSV-compatible batch input, Python command examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs use U.S. Eastern Time as the primary trading-time reference and may include English or Chinese prose, status labels, path types, risk flags, official issuer-news summaries, candidate rankings, and risk controls.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
