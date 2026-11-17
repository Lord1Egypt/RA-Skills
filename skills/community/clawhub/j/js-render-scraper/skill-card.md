## Description:

Js Render Scraper helps agents produce Playwright-based guidance and code for extracting content from JavaScript-rendered web pages, including SPAs, infinite-scroll pages, login-gated pages, and Shadow DOM content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plover061](https://clawhub.ai/user/plover061)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to plan and generate browser-automation scraping workflows for dynamic pages that require JavaScript execution, scrolling, waiting for selectors, clicking controls, login flows, or DOM parsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes guidance for logged-in scraping, which can expose real account credentials or session data.

Mitigation: Use only test credentials or controlled accounts, keep secrets out of prompts and generated files, and run scraping in a contained environment.

Risk: The skill discusses anti-bot, proxy, CAPTCHA, and stealth approaches that could be misused to bypass site controls.

Mitigation: Use the skill only for sites you are authorized to scrape, respect site terms and robots.txt, and do not use bypass guidance to evade access controls.

Risk: Browser automation can consume significant memory, network, and target-site resources.

Mitigation: Apply bounded timeouts, scroll limits, retry limits, and request delays before running generated scraping workflows.

## Reference(s):

- [scraper_example.py](artifact/references/scraper_example.py)
- [ClawHub skill page](https://clawhub.ai/plover061/skills/js-render-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python code examples and structured JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Playwright scraper configuration, Python scraping functions, parsing guidance, and structured result schemas.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
