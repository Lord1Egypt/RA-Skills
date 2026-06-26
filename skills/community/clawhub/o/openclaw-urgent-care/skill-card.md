## Description: <br>
Diagnose and recover from common OpenClaw failures, including gateway outages, locked tools, provider errors, routing issues, and setup health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scsays](https://clawhub.ai/user/scsays) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and OpenClaw users use this skill to triage gateway, routing, provider, scheduler, plugin, and configuration failures and choose a short recovery path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting steps may edit sensitive local OpenClaw configuration files or change tool-access settings. <br>
Mitigation: Back up ~/.openclaw files before applying changes and review any setting that enables full tool access. <br>
Risk: Logs, auth profiles, and provider errors may contain API keys or sensitive account details. <br>
Mitigation: Avoid pasting secrets or full logs into chats; redact keys and account identifiers before sharing diagnostics. <br>
Risk: The skill references a separate Claw Mart recovery product that is external software. <br>
Mitigation: Verify the external product and installer independently before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scsays/openclaw-urgent-care) <br>
- [Claw Mart OpenClaw Urgent Care product](https://www.shopclawmart.com) <br>
- [Publisher profile](https://clawhub.ai/user/scsays) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local OpenClaw config edits, restarts, diagnostics, and recovery checklists for user review.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
