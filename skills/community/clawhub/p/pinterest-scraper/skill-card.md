## Description:

Scrapes Pinterest boards, profiles, or search results with infinite scroll, image quality options, deduplication, resume support, and optional Telegram album sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kexu9](https://clawhub.ai/user/kexu9)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to run a Pinterest image scraping workflow for boards, profiles, or search results, selecting image quality, output location, resume behavior, duplicate handling, logging, and optional Telegram delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports disabled HTTPS safety checks during image downloads.

Mitigation: Review before installing, prefer environments with valid certificate stores, and do not rely on disabled certificate verification unless the interception risk is accepted.

Risk: The skill can upload local image files to Telegram and requires bot credentials.

Mitigation: Avoid Telegram mode for private or sensitive images, use narrowly scoped temporary credentials, and avoid passing long-lived tokens through shell history.

Risk: Scraping output, resume state, and logs are written to local folders.

Mitigation: Run the skill with a dedicated empty output folder and review generated files before reuse or sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kexu9/skills/pinterest-scraper)
- [Publisher profile](https://clawhub.ai/user/kexu9)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, files, configuration]

**Output Format:** [Markdown guidance with CLI commands; runtime output includes downloaded image files, a resume state JSON file, and optional log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable scroll count, output folder, image quality, deduplication, resume mode, verbose logging, and optional Telegram delivery.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
