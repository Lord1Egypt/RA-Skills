## Description:

CircleCI (circleci.com). Use this skill for ANY CircleCI request — reading, creating, and updating data. Whenever a task involves CircleCI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CI operators use the skill to inspect CircleCI users, projects, pipelines, workflows, jobs, artifacts, environment variables, and Insights data. They can also trigger a pipeline after reviewing and approving the exact action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs remote installer code, and the external installer behavior has not been verified.

Mitigation: Review and approve CLI installation separately, and use a verified release where available.

Risk: The CLI handles CircleCI credentials and can perform actions that change pipeline state.

Mitigation: Limit CircleCI permissions and retain the documented approval step before triggering pipelines.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [CircleCI](https://circleci.com)
- [CircleCI API v2 documentation](https://circleci.com/docs/api/v2/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON data, Guidance]

**Output Format:** [Shell commands and JSON responses, with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change CircleCI state require approval before execution.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
