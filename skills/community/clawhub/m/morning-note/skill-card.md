## Description: <br>
Generates a daily investment morning note that summarizes macro market moves, sector signals, portfolio or watchlist changes, and upcoming catalysts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dzy11650](https://clawhub.ai/user/dzy11650) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors and analysts use this skill to generate a concise daily market briefing in Markdown, combining macro indicators, sector rotation signals, portfolio or watchlist movement, and a seven-day catalyst calendar. The skill is designed for signal awareness and explicitly avoids individual stock buy or sell recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Investment summaries may expose sensitive holdings, proprietary watchlists, or strategy notes when saved in the workspace or archived to IMA. <br>
Mitigation: Limit sensitive inputs, confirm who can access generated reports and IMA notes, and disable or explicitly confirm archive behavior for scheduled or ambiguous runs. <br>
Risk: Readers may mistake generated market signals for personalized investment recommendations. <br>
Mitigation: Keep the skill's no-buy-or-sell-recommendation constraint visible in outputs and require human review before acting on generated signals. <br>


## Reference(s): <br>
- [Artifact README](artifact/README.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dzy11650/morning-note) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Analysis, Guidance] <br>
**Output Format:** [Structured Markdown report saved to a dated file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report is constrained to 800-1200 Chinese characters or words as authored, includes a clear data cut-off time, and may optionally be archived to an IMA knowledge base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
