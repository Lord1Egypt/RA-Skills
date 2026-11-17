## Description:

Ironclaw provides real-time threat classification for AI agents to screen skill files, messages, outbound data, and shell commands for risky content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samidh](https://clawhub.ai/user/samidh)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Ironclaw as an additional safety check before installing skills, responding to messages, sending outbound data, or running shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to send messages, commands, skill files, and possible secrets to a third-party API.

Mitigation: Submit only authorized, redacted content and do not send API keys, passwords, private keys, session cookies, proprietary code, private messages, or regulated data unless approved.

Risk: API keys used with the service could be exposed through prompts, logs, or copied examples.

Mitigation: Keep service API keys out of prompts and logs, use placeholders in examples, and store credentials only in approved secret-handling locations.

Risk: Heartbeat update checks involve network calls and could lead users to update skill files without enough review.

Mitigation: Treat update checks as manual, user-approved network actions and review changelogs before replacing any installed skill file.

Risk: The classifier may be uncertain or incorrect, especially on ambiguous content.

Mitigation: Use Ironclaw as an extra safety layer and manually review low-confidence or high-impact decisions before acting.

## Reference(s):

- [Ironclaw ClawHub listing](https://clawhub.ai/samidh/skills/ironclaw)
- [Ironclaw homepage](https://ironclaw.io)
- [Ironclaw API base](https://ironclaw.io/api/v1)
- [Ironclaw documentation](https://ironclaw.io/docs)
- [Ironclaw skill file](https://ironclaw.io/skill.md)
- [Ironclaw heartbeat file](https://ironclaw.io/heartbeat.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with JSON request examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides users to submit content_text and criteria_text to Ironclaw's label API and interpret label and confidence values.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
