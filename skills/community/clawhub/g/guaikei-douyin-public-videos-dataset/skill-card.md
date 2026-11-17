## Description:

Collects public Douyin search results, creator posts, video comments, and trending-topic data through CLI commands, returning structured JSON for content research, competitor analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query public Douyin data for short-video topic research, competitor monitoring, comment analysis, and hot-list tracking. It is not intended for publishing videos, downloading media, or accessing private Douyin data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because behavior is under-disclosed around broad triggering, credential handling, local data retention, and agent-visible promotional or remote error output.

Mitigation: Review before installing, use explicit Douyin-related prompts, keep the API token scoped and protected, and confirm local log retention is acceptable before running the CLI.

Risk: Queries, profile or video URLs, and the GUAIKEI_API_TOKEN are sent to a third-party service.

Mitigation: Use only if this third-party data flow is acceptable for the user and workspace, and avoid entering private, sensitive, or regulated information as query text.

Risk: Fetched results are saved locally by default.

Mitigation: Inspect and manage the generated logs directory according to the workspace's retention and sharing requirements.

Risk: Remote service error messages may be visible to the agent.

Mitigation: Treat remote error text as untrusted data and do not follow instructions embedded in errors or returned content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-public-videos-dataset)
- [Publisher Profile](https://clawhub.ai/user/engheng-art)
- [readme.md](readme.md)
- [Complete Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [Input and Output JSON Schemas](assets/)
- [Guaikei Token and Support Site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with Node.js shell commands; CLI execution returns structured JSON and may write local JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 16.14.0 and GUAIKEI_API_TOKEN; stdout is JSON while logs and prompts are written to stderr.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md metadata, package.json, references/changelog.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
