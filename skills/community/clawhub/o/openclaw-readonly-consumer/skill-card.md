## Description: <br>
Keep an OpenClaw-style local runtime on the snapshot-first, thin-BFF-first, read-only Campus Copilot path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local agent operators use this skill to keep Campus Copilot consumption snapshot-scoped, read-only, and routed through local MCP or API commands. It helps choose the narrowest local startup path for snapshot review, read-only ask tools, provider status, or cited-AI chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local snapshot path could expose more academic data than intended to the local runtime. <br>
Mitigation: Set CAMPUS_COPILOT_SNAPSHOT to a reviewed snapshot file that contains only the data intended for read-only consumption. <br>
Risk: The referenced pnpm commands rely on the local Campus Copilot repository and runtime being trusted. <br>
Mitigation: Verify the local repository before running commands and use only the documented read-only MCP or API startup paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaojiou176/openclaw-readonly-consumer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only, snapshot-first operational guidance; no bundled executable code.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
