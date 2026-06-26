## Description: <br>
Schedule automatic OpenClaw and skill updates with reliable cron templates, timezone-safe scheduling, and clear summary outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to schedule hands-off OpenClaw and ClawHub skill updates, choose safer dry-run or core-only modes, and receive concise update summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic updates can repeatedly change OpenClaw and installed skills without review each time. <br>
Mitigation: Start with the dry-run or core-only template, confirm the cron entry after setup, use a maintenance window, and avoid automatic all-skill updates where unexpected behavior changes would be costly. <br>


## Reference(s): <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/openclaw-auto-updater-litiao) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and update-summary templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cron schedules, timezone settings, dry-run and core-only alternatives, and concise status reporting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
