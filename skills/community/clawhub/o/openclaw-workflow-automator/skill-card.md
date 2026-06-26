## Description: <br>
Automate repeatable workflows with WhatsApp/Telegram notifications, Excel/CSV processing, browser automation, and flexible scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qashsolutions](https://clawhub.ai/user/qashsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to turn plain-English recurring tasks into approved workflow plans that can process files, automate browser actions, call APIs, send notifications, and run on schedules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run approved shell, browser, messaging, and scheduled actions with persistent local data. <br>
Mitigation: Review every workflow plan before approval, use restricted_mode and allowed_sites for higher-risk workflows, and set short approval TTLs and max-runs. <br>
Risk: Command output, screenshots, browser sessions, schedules, and run logs may contain sensitive data. <br>
Mitigation: Avoid banking, payment, admin, and other sensitive accounts; enable clear_session where appropriate; regularly purge sessions, screenshots, and run logs. <br>
Risk: Autonomous scheduled runs may continue acting after the original approval context has changed. <br>
Mitigation: Use plan approval expiry, run budgets, plan hash checks, and periodic schedule review before allowing continued autonomous execution. <br>


## Reference(s): <br>
- [Browser Automation Guide](references/browser-guide.md) <br>
- [Scheduling Guide](references/scheduling-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/qashsolutions/openclaw-workflow-automator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown workflow plans, command previews, JSON-like schedule records, shell commands, execution summaries, and notification guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local workflow plans, schedules, run logs, audit entries, screenshots, and notification payloads through the OpenClaw runtime.] <br>

## Skill Version(s): <br>
2.0.6 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
