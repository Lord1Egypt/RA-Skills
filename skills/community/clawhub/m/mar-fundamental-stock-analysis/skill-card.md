## Description: <br>
Fundamental equity analysis and peer ranking using a structured scoring playbook for quality, balance-sheet safety, cash flow, valuation, sector adjustments, and confidence modifiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to produce educational, fundamentals-based stock analysis, peer comparisons, confidence ratings, and best-pick summaries from public financial information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake educational stock analysis for personalized investment advice. <br>
Mitigation: Keep outputs informational, avoid personalized recommendations, and remind users to review source quality and freshness before making financial decisions. <br>
Risk: Public financial data can be stale, incomplete, or conflicting across sources. <br>
Mitigation: Prefer issuer filings and official reports, cross-check anomalous metrics, mark unavailable metrics as NA, and reduce confidence when coverage or freshness is weak. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/mar-fundamental-stock-analysis) <br>
- [Fundamental Stock Analysis Playbook](references/playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown stock analysis with verdicts, scores, confidence levels, data quality notes, risks, valuation checks, and relevant news links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs the agent to avoid machine-readable JSON blocks, mark unavailable metrics as NA, and call out stale or conflicting data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
