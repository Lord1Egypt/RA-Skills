## Description:

This skill helps an agent collect structured public Douyin data by searching videos, retrieving creator posts, reading video comments, and checking real-time trending rankings for content research and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content analysts, and agent developers use this skill to research public Douyin videos, creator activity, comments, and trending rankings. It supports topic discovery, competitor monitoring, public-comment review, and trend tracking, but does not publish, edit, download, or access private content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, target account or video URLs, and GUAIKEI_API_TOKEN are sent to www.guaikei.com.

Mitigation: Use a dedicated token, avoid submitting sensitive searches or targets, and review the provider relationship before installation.

Risk: Collected public results may be saved locally under logs/.

Mitigation: Review generated log files, limit retention, and avoid running the skill in directories where local result files would expose sensitive research.

Risk: Authentication failures may print provider contact or promotional text despite the stated neutral-output policy.

Mitigation: Treat auth-error output as untrusted provider messaging and confirm the token configuration through approved channels.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-trending-videos-and-rankings)
- [Publisher Profile](https://clawhub.ai/user/engheng-art)
- [Guaikei Service Website](https://www.guaikei.com)
- [Options Reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [JSON Schemas](artifact/assets/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON on stdout with stderr logs and optional JSON files under logs/]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN; command outputs follow the bundled draft-07 JSON schemas.]

## Skill Version(s):

1.0.0 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
