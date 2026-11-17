## Description:

Helps agents search Douyin keywords, retrieve creator posts, fetch video comments, and query real-time hot lists for public content research, competitor analysis, comment analysis, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content analysts, and agents use this skill to collect and structure public Douyin search results, creator posts, video comments, and hot-list data for short-video topic research, competitive monitoring, public-comment analysis, and trend tracking.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Douyin keywords, profile or video URLs, and GUAIKEI_API_TOKEN are sent to the provider service.

Mitigation: Use only approved provider accounts, treat the token like a password, and rotate the token if it is exposed.

Risk: Fetched public comments and profile data may be stored locally in plaintext logs.

Mitigation: Store logs only in controlled workspaces, avoid committing or redistributing collected data, and delete logs when they are no longer needed.

Risk: Bulk public-data collection can create platform, privacy, or policy obligations.

Mitigation: Check applicable Douyin platform terms and privacy requirements before bulk collection, and keep collection scoped to the user's approved purpose.

Risk: Runtime authentication errors may display provider contact or website text despite the skill's neutral-error promise.

Mitigation: Review authentication error output before exposing it to end users and do not relay provider marketing or contact text in agent responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-deep-comments)
- [Guaikei service site](https://www.guaikei.com)
- [README](readme.md)
- [Complete options](references/options.md)
- [Changelog](references/changelog.md)
- [CLI JSON schemas](assets/*.schema.json)

## Skill Output:

**Output Type(s):** [shell commands, JSON, guidance, configuration]

**Output Format:** [Markdown guidance with inline shell commands; runtime commands emit JSON to stdout and write plaintext JSON logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN; individual collection commands support limits up to 10000 items.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
