## Description: <br>
Nex Reports creates, schedules, and delivers automated business reports by combining data from Nex tools, IMAP email, calendar files, taskboards, and custom commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, business operators, and teams use Nex Reports to build recurring business briefings, stakeholder summaries, and operational snapshots from multiple local and service-backed data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CUSTOM module can run user-configured shell commands. <br>
Mitigation: Use CUSTOM only with reviewed commands from trusted report configurations. <br>
Risk: Reports may include sensitive business data and can be delivered through Telegram. <br>
Mitigation: Prefer local file output for sensitive reports and treat Telegram delivery as sharing contents with a third-party service. <br>
Risk: IMAP access requires email account credentials. <br>
Mitigation: Use app-specific IMAP credentials and limit credential exposure to the environment where reports run. <br>


## Reference(s): <br>
- [Nex Reports ClawHub page](https://clawhub.ai/nexaiguy/nex-reports) <br>
- [Nex AI homepage](https://nex-ai.be) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, HTML, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown, HTML, Telegram text, JSON, and saved report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save reports locally or send report contents to Telegram when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
