## Description: <br>
Operates v0 through an OOMOL-connected account for chat, project, deployment, environment variable, webhook, billing, usage, and account-scope actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to let an agent manage a connected v0 workspace, including creating and updating chats, projects, deployments, environment variables, webhooks, and related account information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad v0 account actions, including writes and deletes across chats, projects, deployments, webhooks, environment variables, billing, and account scope. <br>
Mitigation: Review every write or delete request before approval and confirm the exact target, payload, and expected effect. <br>
Risk: The skill depends on an OOMOL-connected account and the oo CLI, so use transfers trust to that connector and account connection. <br>
Mitigation: Install and run it only when you want OOMOL-mediated v0 workspace management, and use the OOMOL CLI installer only if you trust that provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-v0) <br>
- [v0 homepage](https://v0.dev) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
