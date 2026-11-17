## Description:

Searches Liepin jobs, reviews or updates resumes, and prepares job applications through the Liepin MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xllinbupt](https://clawhub.ai/user/xllinbupt)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career-support agents use this skill to search roles on Liepin, inspect resume information, update resume sections, and prepare applications after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Liepin account tokens, resume data, and job application actions.

Mitigation: Protect the saved configuration file, avoid exposing full tokens in logs or conversations, and revoke or regenerate the token if it may have been saved with weak permissions or sent to an untrusted endpoint.

Risk: Job applications and resume updates can affect the user's account and may be difficult to undo.

Mitigation: Manually verify every resume update or job application and require explicit user confirmation before applying to a role.

Risk: The configurable MCP URL can send tokens and account data to an untrusted destination.

Mitigation: Use only the official Liepin endpoint unless the alternate destination is fully trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xllinbupt/skills/liepin-jobs)
- [Project Homepage](https://github.com/xllinbupt/MCP2skill)
- [Liepin MCP Configuration Page](https://www.liepin.com/mcp/server)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and optional JSON tool output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return human-readable job and resume summaries or raw JSON when requested.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
