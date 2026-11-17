## Description:

ScrapeGraphAI (scrapegraphai.com). Use this skill for ANY ScrapeGraphAI request — searching and reading data. Whenever a task involves ScrapeGraphAI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search the web and fetch or extract structured information with ScrapeGraphAI through an already connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions run an unverified remote installer and may also synchronize other agent skills at startup.

Mitigation: Review and verify the CLI installer and any additional skills it installs before approving installation; use OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization when appropriate.

Risk: Content sent through the integration may be processed by OOMOL and ScrapeGraphAI.

Mitigation: Submit only content you intend both services to process.

## Reference(s):

- [ScrapeGraphAI API documentation](https://docs.scrapegraphai.com/api-reference/introduction)
- [ScrapeGraphAI](https://scrapegraphai.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Action results in JSON or requested content formats, with Markdown guidance and inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned content and structure depend on the selected ScrapeGraphAI action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
