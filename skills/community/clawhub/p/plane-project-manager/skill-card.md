## Description:

Plane Project Manager helps agents use the Plane API to manage projects, issues, workspace members, and task progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using Plane use this skill to configure API access and ask an agent for Plane project, issue, member, and progress-management operations through API examples and curl commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to store Plane credential material in a plaintext credentials file.

Mitigation: Use a narrowly scoped Plane API token where possible, avoid storing a Plane password, protect the file with owner-only permissions, and do not sync or commit it.

Risk: Example POST and PATCH commands can create or update Plane projects and issues.

Mitigation: Run mutating commands only after confirming the target Plane URL, workspace, project, and intended change.

## Reference(s):

- [Plane API examples](artifact/references/api-examples.md)
- [ClawHub skill page](https://clawhub.ai/axelhu/skills/plane-project-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON credential examples and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq for examples; mutating POST/PATCH commands can create or update Plane records.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
