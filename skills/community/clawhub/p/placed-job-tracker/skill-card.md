## Description:

Placed Job Tracker helps agents manage a user's job applications through the Placed API, including adding, listing, updating, deleting, and analyzing application records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajitsingh25](https://clawhub.ai/user/ajitsingh25)

### License/Terms of Use:

MIT-0

## Use Case:

External users and career-focused agents use this skill to track job applications, maintain status notes, and review pipeline analytics in the Placed career platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A long-lived Placed API key can expose job application data if stored or sourced insecurely.

Mitigation: Set PLACED_API_KEY in the environment or a secret manager; if using ~/.config/placed/credentials, restrict the file to owner-only permissions.

Risk: The delete job operation can remove application records without a documented safeguard.

Mitigation: Ask the agent to list the matching record and confirm the exact job ID before calling delete_job_application.

Risk: Placed receives job application details and notes handled through this skill.

Mitigation: Install only if comfortable sharing job application data with placed.exidian.tech, and avoid sending unnecessary sensitive notes.

## Reference(s):

- [Placed Job Tracker API Reference](references/api-guide.md)
- [Placed Homepage](https://placed.exidian.tech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a PLACED_API_KEY bearer token to call Placed job-tracking tools.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
