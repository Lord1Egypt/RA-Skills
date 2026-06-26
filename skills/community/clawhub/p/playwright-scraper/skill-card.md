## Description: <br>
Scrapes JavaScript-heavy websites through an MCP tool using Playwright stealth mode and browser spoofing options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[3coco3](https://clawhub.ai/user/3coco3) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch rendered page text from dynamic websites through the `stealth_scrape` MCP tool. It is intended for authorized scraping workflows that need JavaScript execution and configurable browser presentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a stealth web scraper that can bypass bot protections for arbitrary URLs. <br>
Mitigation: Use it only on targets where scraping is authorized and confirm the workflow complies with site terms, account rules, and applicable law. <br>
Risk: The security evidence flags shell interpolation of user-supplied URL input. <br>
Mitigation: Validate and constrain URLs before use; the publisher should remove shell interpolation or pass arguments without a shell before routine deployment. <br>
Risk: The artifact invokes a runtime script that is not included in the release package. <br>
Mitigation: Verify the missing runtime script and browser dependencies are present and reviewed before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/3coco3/playwright-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls] <br>
**Output Format:** [Plain text returned from an MCP tool call] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a target URL and returns scraped page output or an error message.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
