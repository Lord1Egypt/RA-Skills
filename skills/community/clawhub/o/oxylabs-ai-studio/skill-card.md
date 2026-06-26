## Description: <br>
Web scraping, crawling, searching, and browser automation using Oxylabs AI Studio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DrFIRASS](https://clawhub.ai/user/DrFIRASS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to scrape pages, search the web, crawl domains, map site URLs, and run browser-agent tasks through Oxylabs AI Studio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Oxylabs API key for scraping and browser automation. <br>
Mitigation: Store OXYLABS_API_KEY in a protected environment or secret manager, and do not paste it into chat or commit it. <br>
Risk: Scraping, crawling, mapping, and browser-agent actions operate on user-supplied targets. <br>
Mitigation: Confirm the target URL or domain before running the action and use the skill only for sites and data you are authorized to access. <br>
Risk: The setup script installs the Oxylabs AI Studio Python SDK when the native Oxylabs plugin is not detected. <br>
Mitigation: Install only if you intend to use Oxylabs for scraping or browser automation, and review the setup output before continuing. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/DrFIRASS/oxylabs-ai-studio) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/DrFIRASS) <br>
- [Oxylabs AI Studio](https://aistudio.oxylabs.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text results from Oxylabs AI Studio scripts, with setup and environment configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OXYLABS_API_KEY. Results may include scraped page content, search results, crawl output, site maps, or browser-agent findings.] <br>

## Skill Version(s): <br>
1.0.3 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
