## Description:

Scrape.do (scrape.do). Use this skill for ANY Scrape.do request — searching and reading data. Whenever a task involves Scrape.do, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch public web pages through a connected Scrape.do account, retrieve account usage information, and capture page screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs unverified remote code and may add persistent agent skills that this package does not disclose; the downloaded installer and live connector implementation were not verified in the security review.

Mitigation: Review the CLI setup before installing, prefer a verified release, and disable automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Using the connector depends on the intended Scrape.do account and may incur service charges.

Mitigation: Connect only the intended account and consider service charges before running actions.

## Reference(s):

- [Scrape.do documentation](https://scrape.do/documentation/)
- [Scrape.do](https://scrape.do)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Markdown guidance with oo CLI commands; action results vary by action and may include HTML, JSON, account data, or a base64 screenshot.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data depends on the selected Scrape.do action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
