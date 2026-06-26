## Description: <br>
Schedule automatic OpenClaw and skill updates with reliable cron templates, timezone-safe scheduling, and clear summary outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DasWeltall](https://clawhub.ai/user/DasWeltall) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure scheduled OpenClaw and ClawHub skill updates, including dry-run and core-only variants, and to receive concise update summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default workflow can repeatedly change OpenClaw and installed skills without per-update review. <br>
Mitigation: Start with dry-run or core-only scheduling, review the planned update scope and cadence, monitor local logs, and keep the cron job easy to edit or remove. <br>
Risk: Scheduled updates may restart the gateway or fail partially. <br>
Mitigation: Schedule updates during off-hours and require summaries to surface updated, unchanged, and failed items with clear error details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DasWeltall/openclaw-auto-updater) <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with bash command blocks and summary templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May configure recurring unattended updates and produce concise status summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
