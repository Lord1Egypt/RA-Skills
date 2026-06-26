## Description: <br>
Install and configure the Owletto memory plugin for OpenClaw, including OAuth login and MCP health verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buremba](https://clawhub.ai/user/buremba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install the Owletto memory plugin, authenticate with Owletto, configure the MCP endpoint, and verify connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth login grants account access to Owletto. <br>
Mitigation: Confirm the user trusts the Owletto plugin package and understands how access can be revoked before logging in. <br>
Risk: A wrong or untrusted MCP URL could connect OpenClaw to the wrong workspace or service. <br>
Mitigation: Verify the MCP URL points to the intended workspace before running login, configuration, or health-check commands. <br>
Risk: Long-term memory can retain sensitive information. <br>
Mitigation: Review how Owletto stores, uses, deletes, and revokes access to memories before deployment. <br>


## Reference(s): <br>
- [Owletto OpenClaw Setup release page](https://clawhub.ai/buremba/owletto-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes OAuth login, MCP endpoint selection, plugin installation, and health-check commands.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
