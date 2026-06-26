## Description: <br>
Operates Google Forms through OOMOL's googleforms connector and oo CLI for reading, creating, and updating forms and responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect Google Forms schemas, read form data and responses, create forms, and apply form updates through an OOMOL-connected Google Forms account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: State-changing Google Forms actions can create forms, batch update forms, or change publish and response-acceptance settings. <br>
Mitigation: Confirm the exact write payload and intended effect with the user before running actions tagged as write. <br>
Risk: OOMOL setup or login commands can initiate account access changes when run unnecessarily. <br>
Mitigation: Run installer, login, or connection steps only when a command fails with the matching setup or authentication error. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-googleforms) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Google Forms homepage](https://workspace.google.com/products/forms/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action payload construction.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
