## Description: <br>
PandaDoc enables agents to operate a connected PandaDoc workspace through OOMOL's pandadoc connector, including document, template, folder, contact, and webhook actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage PandaDoc workspace resources from an agent, including reading details, creating documents or templates, managing contacts and folders, and configuring document lifecycle webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change PandaDoc state through write actions such as document creation, folder creation, contact updates, template creation, attachment uploads, and webhook creation. <br>
Mitigation: Confirm the exact action, target workspace object, and JSON payload with the user before running write actions. <br>
Risk: The skill can remove PandaDoc data through destructive actions such as deleting contacts or templates. <br>
Mitigation: Require explicit user approval for the specific target before running destructive actions. <br>
Risk: The skill requires access to a connected PandaDoc workspace through OOMOL-managed credentials. <br>
Mitigation: Install only when the agent is intended to operate that PandaDoc workspace, and review the connected account and scopes before use. <br>


## Reference(s): <br>
- [PandaDoc homepage](https://www.pandadoc.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub PandaDoc skill](https://clawhub.ai/oomol/oo-pandadoc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include PandaDoc action names, command invocations, JSON request payloads, and review guidance for write or destructive operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
