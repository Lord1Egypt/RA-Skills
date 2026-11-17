## Description:

Diagnoses GitHub personal access token failures by checking command construction, environment-variable handling, request details, and independent client results before concluding that a token is expired or revoked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to diagnose GitHub PAT authentication failures across API and repository workflows. It helps distinguish local command, environment, and request problems from token or account issues before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A repository-write step in the troubleshooting guidance could change repository content or trigger deployment workflows during diagnosis.

Mitigation: Review the step and avoid it unless the specific repository change is authorized and needed for diagnosis.

Risk: The security scan was partial and did not establish that all referenced behavior was inspected.

Mitigation: Review referenced behavior before installing or using the skill.

## Reference(s):

- [Token Failure Mode Decision Tree](references/token-failure-modes.md)
- [GitHub PAT Debugging on ClawHub](https://clawhub.ai/haiyangchenbj/skills/github-pat-debugging)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, Code]

**Output Format:** [Markdown with diagnostic steps and inline command or code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
