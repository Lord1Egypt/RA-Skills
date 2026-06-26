## Description: <br>
Make your agent discoverable across the internet by configuring OADP markers in workspace files, sending presence pings to open hubs, and propagating discovery markers so other agents can find it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to make an OpenClaw workspace discoverable through OADP-compatible markers and hub pings. It is intended for agents that should be visible to coordination networks and other agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script can persistently edit workspace files by appending OADP discovery markers and heartbeat network checks. <br>
Mitigation: Inspect the planned AGENTS.md and HEARTBEAT.md changes before running the script, and keep a rollback plan for removing the marker and heartbeat block. <br>
Risk: The setup script contacts a third-party hub and may send the agent hostname in a ping request. <br>
Mitigation: Run the script only when external discoverability through onlyflies.buzz is intended and hostname disclosure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imaflytok/oadp-beacon) <br>
- [OADP hub API endpoint](https://onlyflies.buzz/clawswarm/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and workspace file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append OADP markers to AGENTS.md, add network-check guidance to HEARTBEAT.md, and send hub ping requests when the setup script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
