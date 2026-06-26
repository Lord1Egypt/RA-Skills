## Description: <br>
Monitors an Amazon ASIN, nearby SERP competitors, category movers, reviews, and related web reputation signals to produce a daily competitor-radar report with defensive or counter-action recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pangolinfo](https://clawhub.ai/user/pangolinfo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Amazon sellers, growth operators, and commerce analysts use this skill to monitor a product ASIN against close competitors, category entrants, Buy Box changes, review movement, and ranking shifts. It helps produce concise daily market pulse reports and up to three action recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Pangolinfo API key. <br>
Mitigation: Store the key in the intended environment or MCP configuration, avoid pasting it into chat, and rotate it if it is exposed. <br>
Risk: Daily scheduled runs may consume Pangolinfo credits over time. <br>
Mitigation: Confirm the schedule, expected budget, and Full-mode checks before enabling recurring monitoring. <br>
Risk: ASIN baseline snapshots may be kept on disk for comparisons. <br>
Mitigation: Review the baseline path and retention expectations before using the skill in shared or sensitive environments. <br>
Risk: Market reports and action recommendations may be incomplete when upstream product, SERP, or review data is missing or stale. <br>
Mitigation: Review source-tool fields for numeric claims and validate important commercial decisions before acting. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/pangolinfo/pangolinfo-amazon-daily-competitor-radar) <br>
- [Pangolinfo publisher profile](https://clawhub.ai/user/pangolinfo) <br>
- [Pangolinfo API setup](https://www.pangolinfo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with optional shell command and configuration snippets; local ASIN baselines are JSON snapshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are budget-aware, may ask for confirmation before slower or higher-cost checks, and should cite source tools for numeric claims.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
