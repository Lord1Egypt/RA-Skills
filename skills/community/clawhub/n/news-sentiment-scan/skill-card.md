## Description: <br>
Scans stock-related news headlines, scores sentiment from -10 to +10, and prints a sentiment report with notable events and summary counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackpipipi](https://clawhub.ai/user/jackpipipi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run a Python helper for stock news sentiment triage across supported ticker formats. It is intended to summarize headline-level sentiment and notable events, not to provide investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation describes broad multi-source monitoring, while the artifact behavior centers on Yahoo Finance news headlines through yfinance. <br>
Mitigation: Treat reports as headline-level Yahoo Finance sentiment unless the skill is extended and verified against additional data sources. <br>
Risk: Sentiment scores and printed suggestions may be incomplete or misleading for financial decisions. <br>
Mitigation: Use the output only for triage and compare it with primary filings, reputable news, and independent financial analysis. <br>
Risk: The script depends on yfinance and pandas at runtime. <br>
Mitigation: Install and run the skill in a controlled Python environment and review dependencies before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackpipipi/news-sentiment-scan) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jackpipipi) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts stock code, optional day count, and optional market identifier; report includes sentiment score, events, counts, and a cautionary suggestion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
