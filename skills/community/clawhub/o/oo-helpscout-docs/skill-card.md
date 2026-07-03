## Description: <br>
Help Scout Docs (helpscout.com). Use this skill for ANY Help Scout Docs request - searching and reading data. Whenever a task involves Help Scout Docs, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent read, list, and search Help Scout Docs content through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and search Help Scout Docs through an OOMOL-connected account. <br>
Mitigation: Install and use it only when the user intends to expose Help Scout Docs content to the agent through that connected account. <br>
Risk: First-time CLI installation or account-connection setup can affect the user's local environment or connected services. <br>
Mitigation: Treat CLI installation, sign-in, billing recovery, and Help Scout connection steps as user-approved setup actions rather than automatic background actions. <br>
Risk: Connector responses may include Help Scout Docs content that is sensitive or internal. <br>
Mitigation: Review retrieved article, collection, category, and site data before sharing it outside the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-helpscout-docs) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Help Scout](https://www.helpscout.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Help Scout Docs connector actions return JSON data and execution metadata through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
