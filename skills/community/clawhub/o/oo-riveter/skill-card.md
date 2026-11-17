## Description:

Riveter (riveterhq.com). Use this skill for ANY Riveter request — searching and reading data. Whenever a task involves Riveter, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Riveter account details and scrape public webpages through the Riveter connector. It checks an action's live input schema before sending a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may run unverified installers or make broader agent changes without clearly explaining them.

Mitigation: Review and approve CLI installation separately, prefer a verified fixed release, and consider disabling managed-skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: OOMOL brokers the connection and requests, and scraping may consume credits.

Mitigation: Account for brokered requests and scraping credit use when running this skill.

## Reference(s):

- [Riveter API documentation](https://docs.riveterhq.com/)
- [Riveter homepage](https://riveterhq.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API responses, Extracted text, Shell commands]

**Output Format:** [Markdown instructions with inline shell examples; action results are returned as JSON with data and execution metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill checks the live action schema before constructing a request.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
