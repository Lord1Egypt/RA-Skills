## Description:

Download manga chapters from MangaBat as image files using direct CDN URLs with optional Playwright browser fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrrqd](https://clawhub.ai/user/jrrqd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to guide manga chapter downloads from MangaBat URLs, including single chapters, chapter ranges, or all detected chapters. The skill provides setup and command guidance for CDN-based downloads and optional browser fallback when direct access is blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells users to locate manga_scraper.py with a broad home-directory search, while the artifact does not include that script.

Mitigation: Verify that manga_scraper.py comes from the same trusted package and execute it only from a fixed, reviewed path.

Risk: The workflow can scrape remote sites, write downloaded files, and optionally install Playwright and Chromium.

Mitigation: Require user confirmation before scraping, writing files, using browser fallback, or installing browser dependencies; prefer an isolated environment with pinned dependencies.

## Reference(s):

- [Manga Scraper on ClawHub](https://clawhub.ai/jrrqd/skills/manga-scraper)
- [Publisher profile: jrrqd](https://clawhub.ai/user/jrrqd)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to produce command-line download instructions and setup steps; the referenced scraper may write downloaded .webp image files when executed by the user.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
