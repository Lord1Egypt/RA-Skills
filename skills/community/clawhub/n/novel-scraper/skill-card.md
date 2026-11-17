## Description:

Novel Scraper helps agents fetch web novel chapters from configured novel sites, detect pagination and chapter numbers, skip non-novel content, and save formatted TXT files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to download and organize web novel chapters as local TXT files, including chapter-range scraping, pagination completion, and merged output files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound web requests and follows redirects when fetching novel pages.

Mitigation: Use it only with public novel-site URLs you trust and review target URLs before execution.

Risk: Fetched text, logs, cache, catalog, and progress data are stored locally.

Mitigation: Review generated files before sharing them and clear local cache or logs when they are no longer needed.

Risk: Dependency ranges are not fully pinned, which can affect reproducibility.

Mitigation: Pin dependencies in controlled environments that require repeatable installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuzhihui886/skills/novel-scraper)
- [Skill documentation](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)
- [Release notes](artifact/RELEASE_NOTES.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; generated scraper outputs are UTF-8 TXT files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes novel text, logs, cache, catalog, and progress files locally under the OpenClaw workspace and /tmp cache paths.]

## Skill Version(s):

1.6.0 (source: server release evidence, _meta.json, CHANGELOG.md; changelog released 2026-04-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
