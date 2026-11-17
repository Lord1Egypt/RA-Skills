## Description: <br>
Diagnoses local and LAN node connection or pairing failures by guiding an agent through standard skill-platform checks and a clear repair path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual operators use this skill to troubleshoot same-machine and LAN node connectivity, gateway binding, QR or pairing code, and device approval issues. It is intended for local development, home lab, and small LAN environments where the agent can inspect command output and propose one concrete fix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to approve a pending device request without enough identity verification. <br>
Mitigation: Inspect the pending device details and confirm it is the intended device before allowing any approval command. <br>
Risk: The skill can guide local skill-platform commands that change gateway settings. <br>
Mitigation: Review proposed configuration changes before execution and keep command execution under explicit user approval. <br>
Risk: Troubleshooting may rely on local or LAN command output that can expose connection details. <br>
Mitigation: Share only the command outputs needed for diagnosis and avoid exposing credentials, tokens, or unrelated network information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/node-connect-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and structured diagnostic conclusions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command summaries, root-cause mapping, current and expected gateway settings, and ordered repair steps.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
