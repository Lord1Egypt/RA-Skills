## Description: <br>
OpenClaw Memory System provides a prompt-driven three-layer memory workflow for OpenClaw agents, using scheduled extraction and Markdown files to retain task state, daily logs, and reusable long-term lessons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason99666](https://clawhub.ai/user/jason99666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw power users use this skill to install and operate a lightweight memory system that extracts marked decisions and insights into current state, daily archives, and CAR-format long-term memory. It is intended for agent workflows that need auditable context retention without a vector database or external service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent scheduled tasks may read session logs and write conversation-derived information into Markdown memory files. <br>
Mitigation: Review the cron task set before installation and install only in workspaces where persistent memory extraction is acceptable. <br>
Risk: The garbage-collection task can delete session files that match its cleanup rules. <br>
Mitigation: Disable or review the GC task, add dry-run or confirmation steps, and keep a workspace backup before enabling automated cleanup. <br>
Risk: Automated memory rewriting may preserve inaccurate, stale, or sensitive conversation details. <br>
Mitigation: Regularly inspect SESSION-STATE.md, daily memory archives, and MEMORY.md, and remove sensitive or incorrect entries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jason99666/light-memory) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Architecture reference](references/architecture.md) <br>
- [CAR format reference](references/car-format.md) <br>
- [Troubleshooting reference](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prompts with shell command snippets, generated memory files, cron configuration, and status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates SESSION-STATE.md, memory/YYYY-MM-DD.md, MEMORY.md, prompt templates, and OpenClaw cron task definitions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
