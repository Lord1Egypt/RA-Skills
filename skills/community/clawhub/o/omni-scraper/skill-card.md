## Description: <br>
Scrape URLs through Claw School's proxy and return structured JSON for Amazon product and search pages or raw HTML for other pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbeihanda](https://clawhub.ai/user/linbeihanda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to fetch webpage content and structured Amazon product or search data through an external scraping service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs and returned page content are routed through Claw School's external scraping service. <br>
Mitigation: Use only approved public or non-sensitive URLs; avoid internal systems, localhost or private-network URLs, authenticated pages, signed links, and sensitive query parameters unless data sharing is approved. <br>
Risk: The skill requires a CLAW_KEY credential. <br>
Mitigation: Store CLAW_KEY as a secret and do not place it in shared prompts, committed files, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linbeihanda/omni-scraper) <br>
- [Claw School](https://claw-school.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON, text] <br>
**Output Format:** [Markdown guidance with bash and JSON examples; API responses are JSON with parsed fields or raw HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAW_KEY and sends requested URLs to Claw School's scraping service.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
