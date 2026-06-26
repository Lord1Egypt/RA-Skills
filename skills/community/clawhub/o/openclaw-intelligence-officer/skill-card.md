## Description: <br>
OpenClaw行业情报官 collects public industry trends from GitHub Trending, X, Zhihu, 36kr, Juejin, and related feeds, summarizes them with AI, and prepares reports for configured delivery channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muisenice](https://clawhub.ai/user/muisenice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor public technology and industry signals, generate concise summaries, and route scheduled intelligence reports to team communication channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports can be sent to external channels configured by the user, including webhooks, bots, email, and chat destinations. <br>
Mitigation: Use dedicated low-privilege webhooks or bot accounts and verify destinations before enabling scheduled pushes. <br>
Risk: API tokens and delivery credentials are required for some sources and push channels. <br>
Mitigation: Keep tokens out of source control and logs, rotate credentials periodically, and prefer secret storage where available. <br>
Risk: Scheduled collection and retained intelligence history may capture more public trend data than intended over time. <br>
Mitigation: Review cron schedules, configured sources, cache, logs, and summary history periodically; test changes with dry-run before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muisenice/openclaw-intelligence-officer) <br>
- [Publisher profile](https://clawhub.ai/user/muisenice) <br>
- [RSSHub](https://github.com/DIYgod/RSSHub) <br>
- [Huginn](https://github.com/huginn/huginn) <br>
- [TrendRadar](https://github.com/sansan0/TrendRadar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and HTML intelligence reports with inline shell commands and YAML-style configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include links, source labels, tags, local history paths, and delivery-channel settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
