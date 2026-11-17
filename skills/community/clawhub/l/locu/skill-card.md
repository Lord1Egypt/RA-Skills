## Description:

Manage tasks and projects via Locu's Public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidsmorais](https://clawhub.ai/user/davidsmorais)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to query Locu workspace information, including account details, tasks, and projects, through authenticated Locu Public API requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Locu personal access token and can read Locu user, task, and project data, including integrated Linear or Jira task data.

Mitigation: Use the least-privilege Locu token available, avoid exposing the token in logs or shared terminals, and revoke the token when the skill no longer needs access.

## Reference(s):

- [Locu skill page](https://clawhub.ai/davidsmorais/skills/locu)
- [Publisher profile](https://clawhub.ai/user/davidsmorais)
- [Locu user endpoint](https://api.locu.app/api/v1/me)
- [Locu tasks endpoint](https://api.locu.app/api/v1/tasks)
- [Locu projects endpoint](https://api.locu.app/api/v1/projects)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response-handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LOCU_API_TOKEN environment variable for authenticated Locu API calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
