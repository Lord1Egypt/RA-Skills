## Description: <br>
BambooHR helps an agent search and read BambooHR company and employee data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business operations agents use this skill to retrieve BambooHR company information, employee records, employee lists, and available employee field metadata for a connected tenant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BambooHR employee records can contain sensitive HR data. <br>
Mitigation: Confirm the user needs the requested data and use the narrowest employee action, field set, and paging scope that satisfies the request. <br>
Risk: A broad employee-list request can expose more tenant data than necessary. <br>
Mitigation: Prefer targeted record retrieval when possible and avoid broad list actions unless the user request clearly requires them. <br>
Risk: Connection scopes or expired credentials can affect what BambooHR data is accessible. <br>
Mitigation: Confirm OOMOL connection scopes when access fails or appears broader than expected, and resolve auth or connection errors through the documented setup flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-bamboohr) <br>
- [BambooHR homepage](https://www.bamboohr.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only BambooHR connector actions; returned employee data may contain sensitive HR information.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
