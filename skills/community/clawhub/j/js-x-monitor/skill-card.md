## Description: <br>
Monitors configured X.com (Twitter) accounts on a schedule and sends notifications when new posts are detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imjszhang](https://clawhub.ai/user/imjszhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to track selected X.com accounts for industry updates, competitor activity, technical trends, or other recurring information-monitoring workflows. It manages monitored accounts, schedules checks, deduplicates seen posts, and sends summaries with source links to configured notification channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitored X.com content and source links can be sent to external messaging channels. <br>
Mitigation: Use only approved notification channels and review ~/.openclaw/x-monitor/config.json before starting monitoring. <br>
Risk: The skill relies on a logged-in browser session and can continue running as a scheduled background monitor. <br>
Mitigation: Use a dedicated low-privilege X.com browser profile where appropriate and stop the monitoring job when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/imjszhang/js-x-monitor) <br>
- [Quickstart](docs/QUICKSTART.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [JS-Eyes](https://github.com/imjszhang/JS-Eyes) <br>
- [js-search-x](https://github.com/imjszhang/js-search-x) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Notifications] <br>
**Output Format:** [Console text, Markdown-formatted notifications, and JSON configuration/state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, OpenClaw, JS-Eyes, js-search-x, an authenticated X.com browser session, and configured notification channels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, openclaw.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
