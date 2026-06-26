## Description: <br>
Runs the Apify Google Maps Scraper actor to collect Google Maps business data, including local business leads, place URLs, Place IDs, websites, phones, addresses, coordinates, reviews, images, opening hours, and optional website contact enrichment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hundevmode](https://clawhub.ai/user/hundevmode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to build and run budget-controlled Google Maps scraping jobs through Apify for lead generation, local SEO, market research, directory building, and CRM enrichment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Google Maps scraping jobs and an Apify token to Apify. <br>
Mitigation: Use a dedicated APIFY_TOKEN with appropriate account controls, avoid exposing the token in prompts or logs, and run only jobs you are comfortable sending to Apify. <br>
Risk: Contact, review, social-link, and image-author fields can contain privacy-sensitive data. <br>
Mitigation: Collect only fields needed for a lawful use case, avoid reviewer profile data unless required, and apply applicable privacy, platform, retention, and anti-spam rules. <br>
Risk: Large or broad scraping jobs can create unexpected Apify costs. <br>
Mitigation: Start with small limits, split large jobs by area or keyword, and use budget caps such as the documented budget guard. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hundevmode/google-maps-scraper-apify) <br>
- [Skill homepage](https://github.com/hundevmode/apify-google-maps-scraper-agent-skill) <br>
- [Apify Google Maps Scraper actor](https://apify.com/x_guru/google-maps-scraper) <br>
- [Actor input guide](references/actor-input-guide.md) <br>
- [Sample input](references/sample_input.json) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON actor payloads or run results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns actor run summaries and dataset rows from Apify when executed with APIFY_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
