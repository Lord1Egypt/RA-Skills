## Description: <br>
Key Vault Manager Free helps agents use a local key-management workflow for key validation, masked file reads, local API proxy calls, and placeholder-based writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security-conscious users can use this skill to keep API keys local while validating key configuration, reading sensitive files in masked form, proxying API calls through a local tool, and writing placeholder-based updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary says the key-management instructions are broad and under-scoped for safe installation without review. <br>
Mitigation: Review the skill before installing it and use it only for explicit key-management tasks. <br>
Risk: The skill can guide file writes that restore real secrets from placeholders. <br>
Mitigation: Require confirmation and inspect a diff or backup before any write that could restore secret values. <br>
Risk: Local API proxy behavior can send requests to user-configured destinations. <br>
Mitigation: Restrict allowed API destinations and confirm the destination before proxy calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/key-vault-manager-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file-operation and API-call instructions; review before executing because the server security verdict is suspicious.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
