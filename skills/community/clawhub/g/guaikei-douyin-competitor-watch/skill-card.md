## Description:

Guaikei Douyin Competitor Watch helps agents query public Douyin search results, creator posts, comments, and hot lists for competitor research and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and marketing analysts use this skill to query public Douyin search results, creator posts, comments, and hot lists for competitor analysis, trend tracking, and public sentiment review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keywords, target URLs, and related request data may be sent to Guaikei during use.

Mitigation: Use the skill only for non-sensitive public Douyin research, and tell users when their query terms or target URLs will be sent to the third-party service.

Risk: Broad activation can run the skill for ambiguous short-video, creator, comment, or trend requests.

Mitigation: Confirm ambiguous requests before execution and proceed only when the user intends public Douyin research.

Risk: Authentication and token handling were flagged for review, including runtime marketing/contact output and token authentication through URL query strings.

Mitigation: Review before installing; keep tokens in environment variables, avoid logging or echoing them, and require the publisher to remove runtime marketing/contact output and move token authentication out of URL query strings before routine use.

Risk: Successful runs can save JSON result logs locally.

Mitigation: Run the skill in an approved workspace, avoid sensitive inputs, and delete local result logs when retention is not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-competitor-watch)
- [README](artifact/readme.md)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [Input and output JSON schemas](artifact/assets/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; command output is JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful runs may save JSON result logs locally in the skill directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
