## Description: <br>
Js Render Scraper helps agents scrape JavaScript-rendered web pages with Playwright, including SPA, infinite-scroll, login-gated, and Shadow DOM pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plover061](https://clawhub.ai/user/plover061) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and generate Playwright-based scraping workflows for dynamic web pages that require browser automation, waits, scrolling, clicking, login flow handling, and HTML parsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used to scrape sites without sufficient authorization. <br>
Mitigation: Install and use it only for sites you own or are explicitly authorized to scrape, and review target terms before running browser automation. <br>
Risk: Anti-bot bypass guidance, including proxy pools, CAPTCHA solving, and stealth plugins, can support misuse. <br>
Mitigation: Avoid proxy-pool, CAPTCHA-solving, and stealth-plugin workflows unless they are explicitly approved for the target site and use case. <br>
Risk: Authenticated scraping can expose credentials or retrieve sensitive account content. <br>
Mitigation: Verify the login domain before providing credentials and avoid using accounts or pages that contain sensitive data unless retrieval is authorized. <br>


## Reference(s): <br>
- [Scraper example](references/scraper_example.py) <br>
- [ClawHub skill page](https://clawhub.ai/plover061/js-render-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets and JSON-style configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured scrape-result schemas with status, content, links, images, and error fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
