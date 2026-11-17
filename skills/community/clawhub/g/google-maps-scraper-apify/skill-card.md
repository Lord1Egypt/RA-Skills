## Description:

Runs an Apify Google Maps Scraper actor to collect and enrich Google Maps business data such as leads, place identifiers, contact details, reviews, images, opening hours, and coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hundevmode](https://clawhub.ai/user/hundevmode)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers, operators, and growth teams use this skill to build local lead lists, enrich CRM records, collect review data, or run local SEO and market research workflows from Google Maps data through Apify.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify API tokens can be exposed if hardcoded, printed, or passed insecurely.

Mitigation: Provide APIFY_TOKEN through a protected environment variable or secret manager, avoid elevated OS privileges, and do not print full tokens in user-facing output.

Risk: Contact enrichment and reviewer data collection may include personal data.

Mitigation: Only enable website contact enrichment or reviewer personal data fields when there is a lawful, explicit need for the workflow.

Risk: Large scraping runs can create unexpected Apify usage costs.

Mitigation: Start with small jobs, use per-run budget limits, and scale by city, keyword, or area after checking sample results.

## Reference(s):

- [Actor Input Guide](references/actor-input-guide.md)
- [Sample Actor Input](references/sample_input.json)
- [Troubleshooting](references/troubleshooting.md)
- [Apify Google Maps Scraper Actor](https://apify.com/x_guru/google-maps-scraper)
- [Project Homepage](https://github.com/hundevmode/apify-google-maps-scraper-agent-skill)
- [ClawHub Skill Page](https://clawhub.ai/hundevmode/skills/google-maps-scraper-apify)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON payloads; runner output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN; actor results depend on Google Maps, public websites, and selected add-ons.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
