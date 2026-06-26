## Description: <br>
Run personalized email outreach campaigns via Lemlist. Manage campaigns, sequences, and tasks, track lead engagement, search people and company databases, and automate outreach workflows with labeling and scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and sales teams use this skill to operate Lemlist outreach from an agent, including campaign management, lead actions, task handling, analytics, and people or company database search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawLink connects to the user's Lemlist team and proxies authenticated Lemlist API requests. <br>
Mitigation: Install only when this access is acceptable, then verify the active Lemlist connection and intended team before using campaign or lead tools. <br>
Risk: Confirmed write actions can create or change campaigns, leads, schedules, tasks, unsubscribe records, and outreach status. <br>
Mitigation: Use read, list, search, or describe steps first, then review the write preview and confirm the target resource and intended effect before execution. <br>
Risk: High-impact actions such as deleting schedules, changing lead status, or modifying unsubscribe records can affect active outreach. <br>
Mitigation: Require explicit confirmation for destructive or outreach-affecting operations and report the real tool error if execution fails. <br>


## Reference(s): <br>
- [Lemlist API Documentation](https://docs.lemlist.com/) <br>
- [Lemlist Campaign Management](https://help.lemlist.com/en/) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ClawLink tool calls against the connected Lemlist team; write actions are previewed and confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
