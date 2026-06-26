## Description: <br>
MoltGuard is an OpenClaw security guard that helps protect agents and users from prompt injection, data exfiltration, and malicious commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomas-security](https://clawhub.ai/user/thomas-security) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use MoltGuard to add cloud-backed security monitoring and guardrails for agent activity, including prompt, behavior, and data-risk checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs automatic installation and cloud-backed monitoring without enough user-control and data-handling detail. <br>
Mitigation: Before enabling it, review the external plugin and provider terms and confirm what prompts, files, commands, secrets, and PII may be sent to Core. <br>
Risk: The skill may show or store an Agent ID or API key during setup and account claiming. <br>
Mitigation: Treat any Agent ID or API key it shows or stores as a secret and avoid sharing it in logs, prompts, screenshots, or support messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thomas-security/moltguard) <br>
- [OpenGuardrails MoltGuard homepage](https://github.com/openguardrails/openguardrails/tree/main/moltguard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May present status, quota, agent ID, API key, dashboard, and configuration guidance through OpenClaw commands.] <br>

## Skill Version(s): <br>
6.8.16 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
