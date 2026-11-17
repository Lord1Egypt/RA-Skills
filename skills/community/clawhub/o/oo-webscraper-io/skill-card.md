## Description:

WebScraper.io (webscraper.io). Use this skill for ANY WebScraper.io request — reading, creating, updating, and deleting data. Whenever a task involves WebScraper.io, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect WebScraper.io account information, sitemaps, and scraping jobs, download results, and create, update, or delete resources through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code, and the CLI may make persistent changes through automatic installation or synchronization of other agent skills.

Mitigation: Review setup, install a verified CLI release yourself, and review or disable automatic skill installation and synchronization using OO_SKILLS_SYNC_DISABLED as documented by the publisher.

Risk: Actions can change or delete WebScraper.io resources.

Mitigation: Connect only the intended account, confirm the exact effect of write actions, and require explicit approval for destructive actions.

## Reference(s):

- [WebScraper.io Cloud API documentation](https://webscraper.io/documentation/web-scraper-cloud/api)
- [WebScraper.io](https://webscraper.io/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, JSON Lines, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples; action results may be JSON or JSON Lines.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that create, update, or delete resources require user confirmation; destructive actions require explicit approval.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
