## Description: <br>
Real-time competitive intelligence and market research using Bright Data's web scraping infrastructure to analyze competitors' pricing, features, reviews, hiring patterns, content strategy, and market positioning with live web data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and go-to-market teams use this skill to gather live web data and produce competitor snapshots, pricing comparisons, review intelligence, hiring-signal analysis, SEO/content comparisons, market maps, and battlecards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a curl-to-bash installer and Bright Data account login before collection workflows can run. <br>
Mitigation: Review the installer, credential storage, billing, and quota settings before enabling the workflow. <br>
Risk: Live scraping and pipeline collection can affect account costs and may be inappropriate for some target sites or data uses. <br>
Mitigation: Confirm target-site permissions, platform terms, and intended data use before running collection commands. <br>
Risk: Competitive reports can become misleading when pages are gated, stale, empty, or only partially collected. <br>
Mitigation: Cite source URLs, date-stamp analyses, and disclose gaps instead of filling missing facts. <br>


## Reference(s): <br>
- [Analysis Frameworks](artifact/references/analysis-frameworks.md) <br>
- [Data Source Selection Guide](artifact/references/data-source-guide.md) <br>
- [Industry Signal Interpretation Guide](artifact/references/industry-signals.md) <br>
- [Output Templates](artifact/references/output-templates.md) <br>
- [Bright Data CLI installer](https://cli.brightdata.com/install.sh) <br>
- [ClawHub skill page](https://clawhub.ai/meirk-brd/market-intel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with tables, source links, and inline shell commands; structured JSON may be collected from bdata when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live Bright Data CLI access; analyses should include source URLs and a data collection date.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
