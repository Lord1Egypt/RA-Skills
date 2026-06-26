## Description: <br>
Proactive todo execution, heartbeat-driven review, and structured follow-up for a markdown todo system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyharry](https://clawhub.ai/user/hyharry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to let an assistant review a markdown todo file, pick a small set of actionable items, execute short tasks, draft plans for larger work, maintain local journals, and send concise progress reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring proactive execution can repeatedly act on todo items without tight per-action limits. <br>
Mitigation: Define allowed automatic actions before enabling cron, require explicit approval for high-impact tasks, and review status changes during each reconciliation. <br>
Risk: Todo details may be sent by email through the gog CLI. <br>
Mitigation: Verify sender and recipient settings before enabling email, avoid placing secrets in todos, and use chat fallback until delivery preferences are confirmed. <br>
Risk: Local todo and journal files may contain private work details. <br>
Mitigation: Keep todo/ and agent_work/ out of shared repositories or backups unless intentionally shared. <br>


## Reference(s): <br>
- [Proactive-Do Templates](references/templates.md) <br>
- [ClawHub Proactive-Do release page](https://clawhub.ai/hyharry/proactive-do) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions, status updates, todo edits, local journal files, and optional email report text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update todo/todo.md, agent_work/ journals, plan files, report archives, and email notifications when configured.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
