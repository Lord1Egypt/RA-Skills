## Description: <br>
Turso (turso.tech). Use this skill for ANY Turso request: reading, creating, updating, and deleting data through the OOMOL `oo` CLI instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Turso organizations, groups, databases, and available locations through an OOMOL-connected account. It supports read, write, and explicitly approved destructive database operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Turso databases and groups, which changes external service state. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: The skill can delete a Turso database. <br>
Mitigation: Require explicit approval for the specific organization and database before running the destructive action. <br>
Risk: The skill depends on authenticated OOMOL and Turso connections and may fail when credentials, scopes, or billing are unavailable. <br>
Mitigation: Use the documented setup recovery steps only after an action fails with the matching auth, connection, scope, credential, app, or billing error. <br>


## Reference(s): <br>
- [Turso homepage](https://turso.tech) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-turso) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may return JSON responses from the OOMOL connector, including data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
