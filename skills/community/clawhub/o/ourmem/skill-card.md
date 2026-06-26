## Description: <br>
Shared persistent memory for AI agents, available hosted or self-deployed, with Space-based sharing across agents and teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhyyz](https://clawhub.ai/user/yhyyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and teams use Ourmem to install and operate persistent memory for agents, store and search durable facts, import memory files, and share selected memories across Spaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain sensitive user, project, or organizational information. <br>
Mitigation: Avoid storing secrets, regulated data, or short-lived debugging context; review memories before import or sharing. <br>
Risk: Long-lived OMEM_API_KEY or apiKey values can grant access to the associated memory space. <br>
Mitigation: Keep keys out of source control, store configuration files with tight local permissions, and rotate exposed keys. <br>
Risk: Hosted or shared Spaces may expose memories beyond the original agent or session. <br>
Mitigation: Prefer self-hosting for sensitive work and confirm recipients before sharing memories or adding members to Spaces. <br>


## Reference(s): <br>
- [Ourmem ClawHub listing](https://clawhub.ai/yhyyz/ourmem) <br>
- [ourmem API Quick Reference](references/api-quick-ref.md) <br>
- [ourmem Hosted Setup Guide](references/hosted-setup.md) <br>
- [ourmem Self-Hosted Setup Guide](references/selfhost-setup.md) <br>
- [Hosted ourmem API](https://api.ourmem.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and curl/API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API key handling, platform-specific setup steps, and verification commands.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
