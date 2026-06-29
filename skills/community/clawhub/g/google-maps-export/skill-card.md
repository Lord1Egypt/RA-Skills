## Description: <br>
Export Google Maps business data to CSV, JSON, or CRM format, with bulk export, custom field mapping, and filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmapsscraper](https://clawhub.ai/user/gmapsscraper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to export Google Maps business listings, select fields and filters, and transform the result into CSV, JSON, or CRM import formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party scraping API, spends account credits, and saves exported business contact data locally. <br>
Mitigation: Confirm requested fields and filters before export, use the intended API key account, and review privacy and retention obligations before storing exported data. <br>
Risk: Exported email and contact fields may be imported into CRM or outreach workflows subject to privacy and anti-spam requirements. <br>
Mitigation: Collect only necessary fields and review applicable jurisdictional and organizational requirements before CRM import or outreach use. <br>


## Reference(s): <br>
- [gmapsscraper.io homepage](https://gmapsscraper.io) <br>
- [Google Maps Export on ClawHub](https://clawhub.ai/gmapsscraper/google-maps-export) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands, curl requests, and generated CSV, JSON, or CRM field mappings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GMAPS_SCRAPER_API_KEY, uses gmapsscraper.io credits, and can save exported business contact data locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
