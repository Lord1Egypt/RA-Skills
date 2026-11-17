## Description:

Complete Placed career platform integration for resume building, interview coaching, job tracking, ATS checking, cover letter generation, LinkedIn optimization, and salary tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajitsingh25](https://clawhub.ai/user/ajitsingh25)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to the Placed career platform for resume management, interview practice, job application tracking, ATS checks, cover letter generation, LinkedIn profile content, company research, and salary insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-loading instructions source a local credentials file, which can execute shell content and expose the Placed API key if the file is writable or mishandled.

Mitigation: Treat PLACED_API_KEY as a secret, avoid source-based credential loading, and store the key with restrictive permissions or a secret manager.

Risk: The skill can send sensitive career materials to the Placed service, including resumes, job applications, interview answers, salary expectations, and LinkedIn content.

Mitigation: Confirm with the user before sending sensitive career data and install the skill only when the user accepts sharing those materials with Placed.

## Reference(s):

- [Placed Homepage](https://placed.exidian.tech)
- [Placed API Key Settings](https://placed.exidian.tech/settings/api)
- [ClawHub Skill Page](https://clawhub.ai/ajitsingh25/skills/placed)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PLACED_API_KEY to call the Placed API and returns career-platform guidance or generated career materials.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
