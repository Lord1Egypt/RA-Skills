## Description:

This skill helps agents retrieve public Douyin search results, creator posts, comments, and hot-ranking data for content planning, competitor monitoring, sentiment analysis, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, marketers, and content strategy teams can use this skill to collect public Douyin data for keyword research, creator monitoring, comment review, and trend tracking. It is not intended for private account data, publishing, editing, or watermark-removal workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin search terms, creator or video URLs, and comment targets to guaikei.com.

Mitigation: Use only public, non-sensitive targets and confirm that sending the requested data to the external service is acceptable for the environment.

Risk: The API token is sent in URL query parameters, and the security summary reports contradictory authentication-error behavior.

Mitigation: Use a dedicated, revocable token, avoid shared or regulated environments until reviewed, and inspect authentication-error output before operational use.

Risk: Returned datasets are stored locally under logs/ by default.

Mitigation: Store the skill in a controlled workspace, review generated logs for sensitive or restricted content, and rotate or delete logs according to data-handling policy.

Risk: Broad trigger language may cause the skill to be selected for vague short-video or trend-analysis requests.

Mitigation: Confirm the user intends Douyin public-data retrieval and verify target URLs, keywords, and limits before running commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-content-index)
- [Skill usage documentation](readme.md)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Input and output JSON schemas](assets/*.schema.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; executed CLI tools emit JSON on stdout and can write JSON logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN; CLI result limits are documented up to 10000 items per request.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, references/changelog.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
