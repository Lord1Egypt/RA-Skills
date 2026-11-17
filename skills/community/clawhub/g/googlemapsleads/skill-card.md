## Description:

Generate qualified B2B leads from Google Maps. Define your ICP, extract matching businesses, score and qualify leads, export ready-to-outreach lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmapsscraper](https://clawhub.ai/user/gmapsscraper)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, marketing, and business development users use this skill to define an ideal customer profile, run Google Maps lead searches through gmapsscraper.io, score and deduplicate matching businesses, and prepare outreach lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated shell command templates can be risky when untrusted or oddly formatted search terms are interpolated into JSON payloads.

Mitigation: Review commands before execution and build API payloads with validated inputs or a proper JSON encoder.

Risk: The workflow sends targeting criteria and lead/contact data to gmapsscraper.io.

Mitigation: Use only if the data-sharing model is acceptable, and confirm privacy and anti-spam obligations before outreach.

Risk: The workflow requires GMAPS_SCRAPER_API_KEY.

Mitigation: Store the API key in an environment variable or secrets manager, and avoid logging or committing it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gmapsscraper/skills/googlemapsleads)
- [gmapsscraper.io](https://gmapsscraper.io)
- [gmapsscraper.io Jobs API Endpoint](https://gmapsscraper.io/api/v1/jobs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and lead-scoring tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CSV-oriented lead-list guidance for export after API job results are available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
