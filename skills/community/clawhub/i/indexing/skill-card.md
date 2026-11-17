## Description:

Helps agents troubleshoot Google Search Console indexing issues, choose noindex, canonical, and robots.txt fixes, and use the Google Indexing API where appropriate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kostja94](https://clawhub.ai/user/kostja94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and SEO practitioners use this skill to convert indexing signals from Search Console into prioritized fixes for crawlability, canonicalization, page quality, noindex decisions, and eligible Google Indexing API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect noindex, canonical, robots.txt, or Google Indexing API changes can affect whether important pages appear in search results.

Mitigation: Review suggested indexing changes before applying them, especially on important public content pages.

Risk: Blocking crawl access to pages that rely on noindex can prevent crawlers from seeing the directive.

Mitigation: Keep noindex pages crawlable unless there is a separate reason to block crawling, and verify behavior before release.

## Reference(s):

- [Page indexing report](https://support.google.com/webmasters/answer/7440203)
- [ClawHub skill page](https://clawhub.ai/kostja94/skills/indexing)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with prioritized action items, reference links, and inline code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SEO recommendations for noindex, canonical tags, robots.txt, URL Inspection, and Google Indexing API workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
