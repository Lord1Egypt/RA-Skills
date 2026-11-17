## Description:

Retrieves public Xiaohongshu search results, note details, comments, and creator post data as structured JSON for content research, trend analysis, creator monitoring, and comment review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content, marketing, and data-analysis users use this skill to query public Xiaohongshu data by keyword, note URL, or creator profile URL and then analyze the returned results. It supports downstream workflows such as topic selection, competitive monitoring, KOL screening, trend research, and comment sentiment or opinion clustering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, links, and the GUAIKEI_API_TOKEN to Guaikei's API.

Mitigation: Use only inputs approved for third-party API processing, avoid sensitive workspaces, and rotate the token if exposure is suspected.

Risk: Retrieved public data may be saved locally under logs.

Mitigation: Review generated log files before sharing a workspace and delete or redact logs that contain sensitive research targets.

Risk: The server security summary notes a mismatch between the narrow comment-focused summary and the broader search, detail, comment, and creator-monitoring behavior.

Mitigation: Review all four command paths before deployment and document the full scope for users who approve the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xiaohongshu-search-and-detail)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON from command-line scripts, with retrieved results optionally saved as local JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GUAIKEI_API_TOKEN and sends Xiaohongshu keywords or links to Guaikei's API.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
