## Description: <br>
Enables an agent to read, create, and update Asana workspaces, projects, and tasks through the OOMOL Asana connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to operate Asana through an OOMOL-connected account, including workspace and project discovery, task reads, and controlled project or task creation and updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Asana account data through OOMOL-managed credentials. <br>
Mitigation: Install only when OOMOL-connected tooling should access the user's Asana account, and review the Asana scopes before use. <br>
Risk: Write actions can create or update Asana projects and tasks. <br>
Mitigation: Confirm the exact target, payload, and intended effect with the user before running create or update actions. <br>
Risk: The artifact includes a remote CLI install snippet. <br>
Mitigation: Prefer installing the oo CLI from verified official instructions or a signed package instead of blindly piping a remote script into a shell. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-asana) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Asana homepage](https://asana.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions return JSON responses with data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
