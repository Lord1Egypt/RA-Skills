## Description:

Manage Bing Webmaster Tools sites, crawl data, search performance, sitemaps, URL submissions, and account settings through OOMOL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use an OOMOL-connected Bing Webmaster account to inspect search and crawl information, submit URLs and sitemaps, and manage site settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback runs a downloaded installer without installation-specific approval.

Mitigation: Install a verified oo CLI yourself and require approval before running any downloaded installer.

Risk: The OOMOL connection can read Bing account information and make changes, including destructive changes.

Mitigation: Use narrowly scoped account access and confirm the exact target and effect before writes or deletions, as the skill directs.

## Reference(s):

- [Bing Webmaster Tools](https://www.bing.com/webmasters/)
- [Bing Webmaster API documentation](https://learn.microsoft.com/en-us/bingwebmaster/getting-access)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [OOMOL oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON data and shell command examples with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Bing Webmaster account data or proposed changes to sites, URLs, sitemaps, and settings.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
