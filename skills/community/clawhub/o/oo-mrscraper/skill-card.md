## Description:

Use the oo CLI to run MrScraper actions for fetching webpages, extracting data, and discovering sitemap URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use this skill to fetch webpages, extract structured or listing data, convert pages to Markdown, and discover sitemap URLs through a connected MrScraper account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run an unverified oo CLI installer.

Mitigation: Install a verified CLI release yourself and review the installer before running it.

Risk: Automatic skill synchronization can make persistent changes to other agents’ skills.

Mitigation: Review the synchronization behavior or disable it with OO_SKILLS_SYNC_DISABLED as documented in the oo CLI command reference.

Risk: Using the connected account shares account access and request data with OOMOL and MrScraper.

Mitigation: Use only an account and request data you are comfortable sharing with those services.

Risk: Scraping actions marked as writes can change MrScraper state.

Mitigation: Keep write approvals and review the exact payload and effect before running a write action.

## Reference(s):

- [MrScraper API documentation](https://docs.mrscraper.com/docs/api/overview)
- [MrScraper](https://mrscraper.com/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [HTML, JSON, Markdown, URL lists]

**Output Format:** [Action-dependent connector results returned as text, JSON, or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available result fields depend on the selected action and its input schema.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
