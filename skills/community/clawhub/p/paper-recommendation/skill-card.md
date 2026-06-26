## Description: <br>
Automates discovery, review task generation, scoring, and briefing creation for AI research papers from arXiv. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SJF-ECNU](https://clawhub.ai/user/SJF-ECNU) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers and developer agents use this skill to fetch recent AI papers, generate parallel review tasks, extract PDF text, and assemble concise research briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scheduled workflow can repeatedly send briefings to a hardcoded Telegram account. <br>
Mitigation: Do not enable the daily cron or run daily_workflow.py until the Telegram recipient is replaced or removed and confirmed before each delivery. <br>
Risk: The daily workflow path may not match the installed paper-recommendation skill path. <br>
Mitigation: Fix the cron and script paths to the installed skill location before enabling scheduled execution. <br>
Risk: Private research topics, proprietary papers, or sensitive notes could be sent through an external messaging channel. <br>
Mitigation: Use local-only output for sensitive work and review generated briefings before any external delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SJF-ECNU/paper-recommendation) <br>
- [arXiv paper search and PDF source](https://arxiv.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown briefings, JSON paper and review-task records, and shell commands for fetching, PDF extraction, sub-agent review, and delivery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local PDF and briefing files under the configured research directory and may send briefing summaries through a configured Telegram delivery channel.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
