## Description: <br>
Run AI-powered, unblockable web scraping, data extraction with natural language via the MrScraper API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-mrscraper](https://clawhub.ai/user/ai-mrscraper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call the MrScraper API for unblocking pages, starting natural-language scraper runs, rerunning saved scraper configurations, and fetching scraped results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends target URLs, extraction instructions, workflow steps, and scraped page data to MrScraper. <br>
Mitigation: Use it only when sharing that data with MrScraper is acceptable for the target site, data class, and organization policy. <br>
Risk: The security evidence flags anti-bot bypass and scriptable scraping workflows as requiring extra user-safety boundaries. <br>
Mitigation: Use the skill only on sites and sessions you are authorized to scrape, avoid paywalls and authenticated accounts unless explicitly permitted, and do not pass cookies unless strictly necessary. <br>
Risk: The skill requires a sensitive API token. <br>
Mitigation: Store MRSCRAPER_API_TOKEN in an environment variable or secret manager, never expose it in client-side code, logs, commits, or generated output. <br>


## Reference(s): <br>
- [MrScraper homepage](https://mrscraper.com/) <br>
- [ClawHub skill page](https://clawhub.ai/ai-mrscraper/mrscraper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with HTTP and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the MRSCRAPER_API_TOKEN environment variable and sends requests to MrScraper API hosts.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
