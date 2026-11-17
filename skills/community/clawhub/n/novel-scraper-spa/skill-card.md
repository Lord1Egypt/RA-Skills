## Description:

Supports scraping JavaScript-loaded novel sites with Playwright browser rendering, while automatically using requests for static sites when appropriate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch novel chapter text from static or JavaScript-rendered web pages and save the extracted content locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scraper accepts unrestricted URLs, which could cause the host to access internal, localhost, metadata, file://, or redirected resources.

Mitigation: Use only public novel pages that the operator intends to scrape, and reject internal, local, metadata, file://, and untrusted redirected URLs before execution.

Risk: The scraper writes extracted content to local storage.

Mitigation: Confirm the output path before running the scraper and review saved files before sharing or using them downstream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuzhihui886/skills/novel-scraper-spa)
- [Publisher profile](https://clawhub.ai/user/yuzhihui886)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text files and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saved output defaults to ~/.openclaw/workspace/novels/ unless a command-line output path is provided.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
