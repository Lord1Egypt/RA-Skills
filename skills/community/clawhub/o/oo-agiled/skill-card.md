## Description: <br>
Agiled (agiled.app) lets an agent read, create, update, and delete Agiled CRM contacts, projects, and tasks through an OOMOL-connected `oo` CLI account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Agiled CRM, project, and task data from an agent session after their OOMOL account is signed in and connected to Agiled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and delete Agiled contacts, projects, and tasks. <br>
Mitigation: Review the exact target and JSON payload with the user before approving write or destructive actions. <br>
Risk: The skill depends on a third-party OOMOL CLI connection to the user's Agiled account. <br>
Mitigation: Install and run it only when the user trusts OOMOL and is comfortable connecting Agiled through the `oo` CLI. <br>


## Reference(s): <br>
- [Agiled homepage](https://agiled.app) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-agiled) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses from connector runs include a data object and meta.executionId when commands succeed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
