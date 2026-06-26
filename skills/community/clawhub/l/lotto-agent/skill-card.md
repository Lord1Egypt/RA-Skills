## Description: <br>
Private lottery assistant for number generation, draw fetching, prize checking, report generation, and scheduled automation without prediction or winning claims. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenjinliuu](https://clawhub.ai/user/wenjinliuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent manage personal lottery workflows: generate rule-based random entries, store local ticket records, fetch draw results, check prizes, produce reports, and manage scheduled tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled lottery tasks can run unattended and optionally send push notifications. <br>
Mitigation: Review cron entries, task schedules, and notification targets before enabling push delivery; keep notification settings disabled until explicitly confirmed. <br>
Risk: Local lottery records may reveal personal ticket history, spending, and prize-checking activity. <br>
Mitigation: Store records in a private data directory, restrict filesystem access, and avoid sharing backups or logs that include ticket data. <br>
Risk: Fetched public draw data may be unavailable, delayed, or incomplete before final draw publication. <br>
Mitigation: Re-fetch draw data after publication and treat generated reports as convenience summaries rather than official prize confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wenjinliuu/lotto-agent) <br>
- [Public lottery draw data source](https://raw.githubusercontent.com/wenjinliuu/lottery-data-repo/main/public_data) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command results and human-readable text or Markdown messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local lottery records, fetch public draw data, and optionally send OpenClaw notifications when configured.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
