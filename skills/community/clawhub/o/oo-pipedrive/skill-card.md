## Description: <br>
Pipedrive lets an agent operate Pipedrive CRM through the OOMOL connector to read, create, update, and delete records such as deals, persons, organizations, activities, pipelines, and stages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers with connected OOMOL and Pipedrive accounts use this skill to retrieve, search, create, update, and delete CRM records from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Pipedrive CRM data through OOMOL-connected credentials. <br>
Mitigation: Install only when agent access to Pipedrive data is intended, and review requested data access before execution. <br>
Risk: The skill can create, update, or delete CRM records. <br>
Mitigation: Require explicit user approval for the exact payload and expected effect before write or destructive actions. <br>


## Reference(s): <br>
- [ClawHub Pipedrive skill page](https://clawhub.ai/oomol/oo-pipedrive) <br>
- [Pipedrive homepage](https://www.pipedrive.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects containing data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
