## Description:

Connects to Firecrawl through the OOMOL oo CLI to search, scrape, crawl, and extract web data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to run Firecrawl web search, scraping, crawling, and extraction tasks through an OOMOL-connected account, and to check the status or results of asynchronous jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI may install or refresh other agent skills without clearly explaining those changes.

Mitigation: Review automatic skill installation before enabling the integration; install a reviewed release yourself and set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization if unwanted.

Risk: Some Firecrawl actions start jobs, change state, or cancel jobs.

Mitigation: Confirm the exact action, target, and effect before running write or destructive actions.

## Reference(s):

- [Firecrawl API documentation](https://docs.firecrawl.dev/)
- [Firecrawl](https://www.firecrawl.dev)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Firecrawl on ClawHub](https://clawhub.ai/oomol/skills/oo-firecrawl)
- [oomol publisher profile](https://clawhub.ai/user/oomol)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Firecrawl results as text, Markdown, or JSON, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results and formats depend on the selected Firecrawl action.]

## Skill Version(s):

1.0.8 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
