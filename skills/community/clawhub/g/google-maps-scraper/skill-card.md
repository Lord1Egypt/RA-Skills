## Description: <br>
Scrape business data from Google Maps, including names, phones, emails, websites, ratings, and reviews, by keyword and location with no coding required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmapsscraper](https://clawhub.ai/user/gmapsscraper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to build Google Maps business lead lists by defining a targeted keyword and location, confirming paid API use, and retrieving structured business contact data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive third-party API key. <br>
Mitigation: Store GMAPS_SCRAPER_API_KEY securely, avoid exposing it in logs or shared files, and rotate it if it may have been disclosed. <br>
Risk: Each search consumes paid or limited credits. <br>
Mitigation: Confirm the exact keyword, location, expected result count, and credit cost with the user before submitting a scrape job. <br>
Risk: Scraped business contact data can create privacy, anti-spam, terms-of-service, and retention obligations. <br>
Mitigation: Use the collected data only for compliant purposes, avoid collecting more fields than needed, protect exported CSV files, and review Google Maps terms and applicable privacy or outreach rules before use. <br>


## Reference(s): <br>
- [Google Maps Scraper ClawHub Page](https://clawhub.ai/gmapsscraper/google-maps-scraper) <br>
- [gmapsscraper.io](https://gmapsscraper.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and CSV result handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GMAPS_SCRAPER_API_KEY and curl; downloaded results are CSV files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
