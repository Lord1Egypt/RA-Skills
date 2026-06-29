## Description: <br>
Generate qualified B2B leads from Google Maps by defining an ICP, extracting matching businesses, scoring and qualifying leads, and exporting ready-to-outreach lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmapsscraper](https://clawhub.ai/user/gmapsscraper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and sales teams use this skill to plan Google Maps lead searches, run a third-party scraping job, score contactability signals, deduplicate results, and prepare outreach-ready lead lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a gmapsscraper.io API key and sends lead-search criteria to that third-party service. <br>
Mitigation: Use a dedicated API key, scope and rotate it where possible, and avoid submitting sensitive or confidential target criteria. <br>
Risk: Exported business contact data may be used for outreach subject to privacy, platform, and anti-spam requirements. <br>
Mitigation: Review Google Maps, privacy, anti-spam, and outreach compliance requirements before exporting emails or starting cold outreach. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/gmapsscraper/googlemapsleads) <br>
- [GMapsScraper homepage](https://gmapsscraper.io) <br>
- [GMapsScraper pricing](https://gmapsscraper.io/#pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash/curl snippets and CSV export expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GMAPS_SCRAPER_API_KEY and curl; sends lead-search criteria to gmapsscraper.io.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
