## Description:

Scrapes websites using Playwright with stealth behavior for dynamic JavaScript content and bot-detection evasion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3coco3](https://clawhub.ai/user/3coco3)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to extract text from JavaScript-heavy webpages when they are authorized to access and scrape the target site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unrestricted anti-bot scraping behavior and URL input that can be abused to run local shell commands.

Mitigation: Install only after URL validation and command construction are remediated, and restrict use to authorized scraping targets.

Risk: The artifact calls a scraper script that is not included in the packaged files.

Mitigation: Verify the complete runtime package and expected scraper script before deployment.

Risk: The security guidance calls out dependency pinning and update concerns.

Mitigation: Pin or update dependencies and review the resolved package lock before enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3coco3/skills/playwright-scraper)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text returned by an MCP tool call]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The tool accepts a URL input; scraping must be limited to sites the user is authorized to access.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
