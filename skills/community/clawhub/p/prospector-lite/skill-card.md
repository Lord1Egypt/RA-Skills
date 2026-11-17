## Description:

Prospector Lite gives OpenClaw agents a structured B2B outreach workflow for prospect research, email verification, bounce handling, pipeline tracking, duplicate prevention, domain reputation protection, and iterative lessons logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicuahmadi](https://clawhub.ai/user/nicuahmadi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales operators, and founders use this skill to guide an agent through cold B2B prospecting, lead qualification, compliant work-email verification, outreach drafting, follow-up handling, and pipeline updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide recurring inbox access and outbound cold email.

Mitigation: Use a dedicated email account or narrowly scoped email tool, verify the email integration and permissions, and require manual approval before inbox reads, cron enablement, or external sends.

Risk: Cold outreach may damage sender reputation or contact people without adequate consent controls.

Mitigation: Apply the skill's send limits, work-email verification, bounce logging, duplicate checks, opt-out handling, and one-follow-up rule before any send.

## Reference(s):

- [Prospector Lite on ClawHub](https://clawhub.ai/nicuahmadi/skills/prospector-lite)
- [Sora Labs](https://sora-labs.net)
- [Sora Labs Tools](https://sora-labs.net/tools/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and email-template text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to maintain prospect pipeline and lessons-learned files; outbound email execution depends on a separately configured email tool.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
