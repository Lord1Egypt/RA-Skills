## Description:

Collects public Douyin search, creator post, comment, and trending-topic data for short-video marketing analysis and content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to gather structured public Douyin data for keyword research, competitor account review, comment analysis, trend monitoring, and marketing reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin search terms, profile or video URLs, and GUAIKEI_API_TOKEN are sent to the vendor service.

Mitigation: Use only non-sensitive queries and URLs, provision the token with the least practical access, and rotate or revoke the token if exposure is suspected.

Risk: Collected comments, account data, and result datasets are saved locally by default.

Mitigation: Treat the logs directory as sensitive business or personal data, restrict access, review it regularly, and delete retained data when it is no longer needed.

Risk: Broad implicit triggers can invoke Douyin collection even when the user does not explicitly mention Douyin.

Mitigation: Confirm intent before running collection commands when the request is ambiguous or could involve another platform or private data.

Risk: Invalid-token paths may show vendor contact details despite the skill claiming they will not.

Mitigation: Review authentication-error output before exposing it to end users, and avoid presenting vendor contact details as neutral system guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-collection)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Input and output JSON schemas](assets/*.schema.json)
- [Guaikei service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-command workflows can return up to 10,000 public Douyin records and save JSON logs locally.]

## Skill Version(s):

1.0.0 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
