## Description: <br>
MoltGuard helps protect agents and users from prompt injection, data exfiltration, malicious commands, and related security risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomas-security](https://clawhub.ai/user/thomas-security) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users install OpenGuardrails/MoltGuard to add runtime protection for prompts, file and web content, commands, and data exposure risks. Organizations can configure an enterprise Core endpoint for managed deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install runtime security software and trust the @openguardrails/moltguard plugin. <br>
Mitigation: Install only after explicit user approval and treat the plugin and Core service as trusted components before enabling protection. <br>
Risk: The skill can use a remote scanning service and may route security checks to a public or enterprise Core endpoint. <br>
Mitigation: Use enterprise enrollment only with a Core URL that the organization controls and verifies. <br>
Risk: Status and claim commands may display API credentials or agent identifiers. <br>
Mitigation: Do not share /og_status or /og_claim output, and review where MoltGuard credentials are stored. <br>


## Reference(s): <br>
- [ClawHub OpenGuardrails page](https://clawhub.ai/thomas-security/openguardrails) <br>
- [OpenGuardrails MoltGuard homepage](https://github.com/openguardrails/openguardrails/tree/main/moltguard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and slash-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, status, account-claim, dashboard, enterprise enrollment, update, and uninstall commands.] <br>

## Skill Version(s): <br>
6.8.20 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
