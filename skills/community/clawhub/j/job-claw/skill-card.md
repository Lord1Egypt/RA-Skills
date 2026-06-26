## Description: <br>
JobClaw automates job search workflows by searching LinkedIn and Indeed, scoring postings against a user's profile, and maintaining a local CSV tracker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weixijia](https://clawhub.ai/user/weixijia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use JobClaw to configure job-search preferences, run scheduled or on-demand searches, score job postings, track results, and send optional notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled workflows can modify local job records through automatic archive behavior. <br>
Mitigation: Review archive behavior before enabling scheduling, run archive commands in dry-run mode first, and enable committed archiving only after confirming it matches user expectations. <br>
Risk: Notification configuration can contain Telegram or OpenClaw credentials. <br>
Mitigation: Keep config.json private, leave notifications disabled unless needed, and avoid storing tokens in shared or synced workspaces. <br>
Risk: Dependency setup may attempt system-wide pip changes. <br>
Mitigation: Install dependencies inside a virtual environment rather than allowing system-wide package changes. <br>
Risk: The security evidence flags the scheduled runner as unsafe until dry-run behavior and archive URL validation are corrected. <br>
Mitigation: Avoid enabling scheduled runs until those workflow risks have been reviewed and resolved. <br>


## Reference(s): <br>
- [ClawHub JobClaw Release Page](https://clawhub.ai/weixijia/job-claw) <br>
- [Commands Reference](references/commands.md) <br>
- [Keyword Reference](references/keywords.md) <br>
- [Screening Guide](references/screening_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and CSV-oriented job-tracker records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local config, CSV tracker, logs, archive CSV, and optional notification messages when its commands are executed.] <br>

## Skill Version(s): <br>
1.0.20260329-142ceea (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
