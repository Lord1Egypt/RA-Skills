## Description: <br>
Initialize personal and team knowledge bases, create or join teams, create team project spaces, configure Gitea repository permissions, and maintain the AIFusionBot/system-config control repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to initialize paper-kb workspaces, manage personal and team knowledge-base repositories, bind team chats, and coordinate Gitea permissions for users and teams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Gitea admin-capable token and can create private repositories, grant collaborators, and update persistent workspace state. <br>
Mitigation: Install only for a Gitea server you operate, use the least-privilege bot or admin token that supports the required actions, and audit repository and collaborator changes after setup. <br>
Risk: The bundled example configuration includes a plain-HTTP Gitea endpoint. <br>
Mitigation: Replace GITEA_URL with a trusted HTTPS endpoint before use and keep tokens out of checked-in files. <br>
Risk: The skill maintains team, user, chat-binding, permission, and active-task state in AIFusionBot/system-config. <br>
Mitigation: Restrict access to the control repository, back it up, and review changes when repairing failed provisioning or binding team chats. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myd2002/skills/init-workspace) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown instructions with bash command examples; scripts return JSON status objects and interactive-card payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates private Gitea repositories, repository files, collaborator permissions, and persistent system-config records when executed with configured credentials.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
