## Description:

Formats Guangzhou Daily/Xinhuacheng news items into a Markdown news brief and WeChat-ready summary with titles, abstracts, links, editors, and reporters; separately verify the documented automation and push-delivery behavior before relying on it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeeye](https://clawhub.ai/user/freeeye)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators can ask an agent to prepare local Guangzhou news briefs from Guangzhou Daily/Xinhuacheng content, save a Markdown digest, and produce concise text suitable for WeChat-style sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation claims automatic fetching, scheduled pushes, and WeChat delivery, but security evidence says the included code does not implement those behaviors.

Mitigation: Verify fetching, scheduler, and push integrations separately before relying on automated delivery.

Risk: The skill may write Markdown output under ~/News.

Mitigation: Review local file paths and permissions before running it in shared or managed environments.

Risk: The script depends on third-party Python packages.

Mitigation: Install dependencies in a virtual environment with pinned versions where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freeeye/skills/guangzhou-daily-news)
- [Guangzhou Daily Xinhuacheng Main Site](https://gz-cmc.com)
- [Guangzhou Daily Xinhuacheng Mobile Site](https://huacheng.gz-cmc.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown news brief, plain-text sharing summary, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Markdown files under ~/News when used with news data; WeChat push and scheduled delivery require separate verification.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
