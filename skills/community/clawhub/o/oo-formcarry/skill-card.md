## Description: <br>
Formcarry (formcarry.com). Use this skill for ANY Formcarry request - reading, creating, updating, and deleting data. Whenever a task involves Formcarry, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Formcarry forms and submissions through an OOMOL-connected account. It supports creating and deleting forms, listing submissions, and inspecting live action schemas before running connector actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected account and managed credentials to run connector actions. <br>
Mitigation: Connect the account only when the user is comfortable with connector-mediated requests and related account metadata passing through the service. <br>
Risk: The skill includes write and destructive actions for creating and deleting Formcarry forms. <br>
Mitigation: Confirm the exact action, target, payload, and intended effect with the user before running write actions, and require explicit approval before deleting a form. <br>
Risk: Connector action schemas can change over time. <br>
Mitigation: Inspect the live action schema before constructing each payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-formcarry) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Formcarry homepage](https://formcarry.com) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses may include JSON data and an execution identifier.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
