## Description: <br>
Fetches RSS news across domestic, international, technology, and AI categories and sends formatted Feishu card messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morrison230](https://clawhub.ai/user/morrison230) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to collect daily news from configured RSS sources and deliver a scheduled or manual briefing into a Feishu group. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script sends messages through a Feishu webhook while HTTPS certificate verification is disabled. <br>
Mitigation: Use a dedicated webhook, store it as a protected environment variable, and restore normal TLS certificate verification before scheduling the automation. <br>
Risk: Webhook secrets may be exposed if stored in shared or checked-in configuration files. <br>
Mitigation: Prefer the NEWS_DAILY_WEBHOOK environment variable and keep local config files out of version control. <br>


## Reference(s): <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Feishu interactive card JSON with markdown content, plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [News categories, item counts, target date, and webhook destination are configurable through environment variables or config files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
