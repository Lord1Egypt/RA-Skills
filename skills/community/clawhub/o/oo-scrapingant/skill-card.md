## Description: <br>
ScrapingAnt helps agents use an OOMOL-connected ScrapingAnt account to scrape pages, convert content to Markdown, extract structured fields, and check API credit usage through the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to retrieve, transform, or extract webpage data through ScrapingAnt without directly handling raw API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected ScrapingAnt account and may depend on sensitive account credentials managed outside the skill. <br>
Mitigation: Install only when the user intends the agent to use that connected account, and sign in or connect ScrapingAnt only after an auth or connection error requires setup. <br>
Risk: Scraping actions may return webpage HTML, text, headers, cookies, XHRs, and iframe data from URLs the user provides. <br>
Mitigation: Review target URLs and returned data before sharing or storing results, especially when pages may contain sensitive or third-party content. <br>
Risk: The first-time setup path includes remote installer commands for the oo CLI. <br>
Mitigation: Verify the oo CLI installation path and installer source before running setup commands. <br>


## Reference(s): <br>
- [ScrapingAnt homepage](https://scrapingant.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-scrapingant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return scraped page HTML, text, cookies, headers, XHRs, iframe data, extracted JSON fields, Markdown content, API credit status, and connector execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
