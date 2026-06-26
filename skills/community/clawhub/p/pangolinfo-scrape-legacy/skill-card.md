## Description: <br>
Searches Google through Pangolin AI Mode and SERP APIs and scrapes Amazon pages for structured product, keyword, category, seller, ranking, and screenshot results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tammy-hash](https://clawhub.ai/user/tammy-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to authenticate with Pangolin, run Google AI Mode or standard SERP searches, and collect Amazon product or market data as structured JSON. It is useful when an agent needs search, AI overview, screenshot, or Amazon scrape data without building Pangolin API calls from scratch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches, URLs, follow-up prompts, zip code, and screenshot requests are sent to Pangolin's remote API. <br>
Mitigation: Avoid confidential searches and use the skill only where sending those inputs to Pangolin is acceptable. <br>
Risk: Pangolin bearer tokens or login-derived tokens are sensitive and may be cached at ~/.pangolin_token. <br>
Mitigation: Use a dedicated or revocable token where possible, protect shared machines, and remove or rotate the cached token when no longer needed. <br>


## Reference(s): <br>
- [Pangolinfo AI SERP canonical skill](https://clawhub.ai/pangolinfo/pangolinfo-ai-serp) <br>
- [Pangolinfo Amazon Scraper canonical skill](https://clawhub.ai/pangolinfo/pangolinfo-amazon-scraper) <br>
- [AI Mode API Reference](references/ai-mode-api.md) <br>
- [AI Overview SERP API Reference](references/ai-overview-serp-api.md) <br>
- [Amazon Scrape API Reference](references/amazon-api.md) <br>
- [Error Codes and Troubleshooting](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit structured JSON responses, raw Pangolin API responses, raw HTML or markdown for Amazon requests, and screenshot URLs when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
