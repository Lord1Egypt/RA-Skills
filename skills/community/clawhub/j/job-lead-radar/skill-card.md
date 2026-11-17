## Description:

Scrapes and collects job leads from Indeed, ZipRecruiter, ProductionHUB, LinkedIn, and Peerspace on demand or on a schedule for production and creative roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gullish42069](https://clawhub.ai/user/gullish42069)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and creative production teams use this skill to gather job lead data from supported job boards, run one-off searches, or schedule recurring monitoring for production and creative roles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends chosen job search terms to third-party job sites and stores results or logs locally.

Mitigation: Run or schedule the skill only with queries appropriate for disclosure to those sites, and manage local result and log files according to the user's data handling expectations.

Risk: The scraper depends on the third-party scrapling package.

Mitigation: Install in a virtual environment and pin or review the dependency before use.

Risk: Anti-bot protections on Indeed, ZipRecruiter, and LinkedIn may reduce results or return no listings.

Mitigation: Treat empty or reduced results from those sites as expected scraping limitations and compare against more reliable sources such as ProductionHUB and Peerspace when appropriate.

## Reference(s):

- [Job Query Templates](artifact/references/queries.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON]

**Output Format:** [Console status text plus a JSON results file containing timestamps, sources, queries, job entries, links, and per-source errors when scraping fails.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are saved to scripts/job_leads.json; scheduled runs may also append logs when configured with cron.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
