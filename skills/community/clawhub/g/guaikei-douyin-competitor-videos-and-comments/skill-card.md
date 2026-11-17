## Description:

This skill helps agents collect structured public Douyin search, creator post, comment, and hot-list data for competitor research, topic discovery, feedback analysis, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External analysts, marketers, and developers use this skill to research public Douyin content, compare competitor accounts, inspect audience comments, and identify trending topics. It is intended for public-data collection and analysis, not video publishing, editing, downloading, or private account access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin research requests and GUAIKEI_API_TOKEN are sent to www.guaikei.com.

Mitigation: Use the skill only when the user explicitly wants Douyin public-data collection and is comfortable using the third-party service and token.

Risk: Results are saved under logs by default and may contain collected public profile, post, or comment data.

Mitigation: Store logs according to the user's data-handling policy, review them before sharing, and delete them when no longer needed.

Risk: The activation guidance is broad and may trigger during generic competitor or trend research.

Mitigation: Confirm the task is specifically about Douyin research before running collection commands.

Risk: Runtime service output, especially errors or links, may be untrusted.

Mitigation: Do not follow runtime contact instructions or links without independent verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-competitor-videos-and-comments)
- [README](readme.md)
- [Complete options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Input and output JSON schemas](assets/*.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; CLI stdout is JSON and default saved logs are JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; requests are sent to www.guaikei.com; individual collection commands can request up to 10000 records.]

## Skill Version(s):

1.0.0 (source: package.json, references/changelog.md, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
