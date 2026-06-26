## Description: <br>
Supercharged Daily Briefing helps an agent discover user-approved sources, monitor topics, and produce concise daily intelligence briefings with source management, scheduling, archives, and feedback loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and teams use this skill to turn an agent into a daily research assistant that tracks chosen topics, discovers and maintains sources, summarizes important developments, and delivers morning briefings in chat. It also supports source health checks, topic tuning, briefing archives, and optional dashboard views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Briefing topics, source URLs, fetched content, archives, and summaries may pass through the user's agent, web search or fetch providers, chat channel, and any enabled dashboard backend. <br>
Mitigation: Use only sources and delivery channels the user accepts, disclose the data flow before setup, and avoid enabling dashboard sync unless its storage and retention behavior are understood. <br>
Risk: Recurring briefings depend on setup and scheduler scripts that the security evidence says should be verified before use. <br>
Mitigation: Review and test setup, scheduler, retention, and delete/reset behavior before enabling automated delivery. <br>
Risk: Fetched articles, feeds, and web pages can contain prompt-injection content. <br>
Mitigation: Treat all external content as untrusted data, preserve the skill's URL safety checks, and require user confirmation before adding discovered sources. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/nollio/normieclaw-daily-briefing) <br>
- [Publisher profile](https://clawhub.ai/user/nollio) <br>
- [README](artifact/README.md) <br>
- [Security audit notes](artifact/SECURITY.md) <br>
- [Dashboard add-on specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chat-ready Markdown briefings, JSON configuration and archive records, and optional shell commands for scheduling checks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include source URLs, topic preferences, briefing archives, source health summaries, and setup or scheduling guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
