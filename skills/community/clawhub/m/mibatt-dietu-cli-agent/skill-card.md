## Description: <br>
Use this skill when you need to operate Dietu through its official CLI for A-share market queries, strategy screening, decision workflows, or agent automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenee](https://clawhub.ai/user/kenee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to authenticate to Dietu and run CLI-based A-share market, research, decision, trading, and review workflows with structured output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated CLI workflows may expose Dietu access tokens if users paste real tokens directly into commands or logs. <br>
Mitigation: Use short-lived, least-privilege tokens stored in protected environment variables or a secret manager, avoid pasting real tokens directly into commands, and rotate or revoke tokens after automation use. <br>


## Reference(s): <br>
- [Auth](references/auth.md) <br>
- [Commands](references/commands.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kenee/mibatt-dietu-cli-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown, Code] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI output-format guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports json, markdown, table, and ndjson Dietu CLI output modes depending on the task.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
