## Description:

Find and rank GitHub developers by location, technology, and role. Search for candidates, get scored profiles with tech stack matches, activity, and contact info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mordka](https://clawhub.ai/user/mordka)

### License/Terms of Use:


## Use Case:

Recruiters, sourcers, hiring teams, and developers use this skill to find GitHub developer candidates by location, technology stack, and role, then review scored profiles and available contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Returned emails, websites, and social profiles may be personal data.

Mitigation: Confirm a lawful basis for collection, storage, and outreach before using candidate contact data.

Risk: Search requests may disclose sensitive sourcing strategy to the GitHunt API.

Mitigation: Avoid sending sensitive recruiting criteria unless the user trusts GitHunt's handling of that data.

Risk: The helper scripts accept user-provided search arguments and a configurable GITHUNT_API_URL.

Mitigation: Run scripts only with trusted arguments and a trusted API URL value.

## Reference(s):

- [GitHunt website](https://githunt.ai)
- [GitHunt API base URL](https://api.githunt.ai/v1)
- [ClawHub GitHunt release page](https://clawhub.ai/mordka/skills/githunt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples; helper script output is plain text parsed from API JSON or Server-Sent Events.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces candidate search guidance and command output for GitHunt API requests; API responses may include personal contact data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
