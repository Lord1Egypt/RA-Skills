## Description: <br>
Find any local business by category and location on Google Maps, including names, phone numbers, emails, websites, ratings, and hours. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmapsscraper](https://clawhub.ai/user/gmapsscraper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find local businesses by category and location, optimize searches before spending service credits, and present Google Maps business profiles in a scannable format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches use a sensitive gmapsscraper.io API key. <br>
Mitigation: Store GMAPS_SCRAPER_API_KEY securely, avoid sharing command logs that expose it, and revoke or rotate the key if it is disclosed. <br>
Risk: Each search consumes third-party service credits. <br>
Mitigation: Confirm the business type, location, and filters before running a search so credits are spent intentionally. <br>
Risk: Search queries and collected business contact details are sent to or retrieved from a third-party service. <br>
Mitigation: Use exported contacts only for legitimate, compliant purposes and review applicable local laws, source terms, and outreach rules. <br>


## Reference(s): <br>
- [Local Business Finder on ClawHub](https://clawhub.ai/gmapsscraper/local-business-finder) <br>
- [gmapsscraper.io](https://gmapsscraper.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline bash commands and CSV download output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GMAPS_SCRAPER_API_KEY and curl; searches use third-party service credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
