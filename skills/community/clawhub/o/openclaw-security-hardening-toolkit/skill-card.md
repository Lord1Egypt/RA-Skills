## Description: <br>
Audits and hardens OpenClaw deployments by checking instance exposure, credential handling, skill installation safety, gateway access control, session sandboxing, and incident response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thebrierfox](https://clawhub.ai/user/thebrierfox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw or Aegis deployments, reduce common exposure and credential risks, vet installed skills, configure access controls, and follow an incident response checklist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes commands and configuration changes that can affect gateway availability, credentials, filesystem permissions, and running sessions. <br>
Mitigation: Review each command before execution, run checks in the intended OpenClaw environment, and preserve logs or backups before containment and recovery steps. <br>
Risk: Credential rotation, token revocation, and key replacement can break dependent services or make encrypted data inaccessible if performed incorrectly. <br>
Mitigation: Follow the documented revocation order, verify replacement credentials in the provider dashboards, and record rotation dates and reasons. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thebrierfox/openclaw-security-hardening-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/thebrierfox) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with bash commands, JSON configuration snippets, checklists, and risk matrices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational security checks and incident response sequences for human review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
