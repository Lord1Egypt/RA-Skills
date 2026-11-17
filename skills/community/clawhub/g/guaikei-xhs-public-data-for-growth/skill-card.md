## Description:

Retrieves structured JSON from public Xiaohongshu data for keyword search, note details, note comments, and creator post history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketing teams, analysts, and agents use this skill to collect public Xiaohongshu search results, note metadata, comments, and creator post lists for topic research, competitor monitoring, KOL review, and content performance analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, URLs, and retrieved public data are sent through Guaikei's API.

Mitigation: Install only when that data flow is acceptable for the intended research or business context.

Risk: The skill handles a GUAIKEI_API_TOKEN and generated result logs, which can expose credentials or collected data if shared carelessly.

Mitigation: Use a dedicated revocable token, avoid shared workspaces for sensitive research, and regularly delete or protect generated logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-public-data-for-growth)
- [Guaikei API and token access](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands that return structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; command results may be saved under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
