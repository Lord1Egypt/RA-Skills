## Description:

Scrape government permit databases (liquor licenses, business registrations, contractor permits, health permits) to generate B2B sales leads, enrich raw permit data with business emails via web scraping, and auto-email outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merjua14](https://clawhub.ai/user/merjua14)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to build B2B lead lists from public permit records, enrich them with contact information, and prepare or run outreach workflows for newly licensed businesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pipeline can automatically email scraped and search-enriched contacts before adequate review.

Mitigation: Run dry-run mode first, review recipients and message content, and do not provide a Resend API key until outreach is approved.

Risk: Live campaigns may lack sufficient safeguards for date filtering, suppression, unsubscribe handling, rate limiting, and CSV escaping.

Mitigation: Implement and verify those controls before enabling live email delivery.

Risk: Public-record scraping and outreach requirements vary by jurisdiction and data source.

Mitigation: Confirm each source and outreach use is lawful for the relevant jurisdiction and retain records of data provenance.

## Reference(s):

- [Government Permit Data Sources](references/data-sources.md)
- [Cold Email Compliance](references/compliance.md)
- [Texas TABC New Permits Issued](https://www.tabc.texas.gov/public-information/new-permits-issued/)
- [ClawHub Skill Page](https://clawhub.ai/merjua14/skills/gov-permit-scraper)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with shell commands, JavaScript code, JSON configuration, and CSV output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires external API keys for Brave Search enrichment and Resend email delivery; dry-run mode is available.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
