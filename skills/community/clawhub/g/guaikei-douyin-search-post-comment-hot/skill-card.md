## Description:

Collects structured JSON data from public Douyin search results, creator posts, video comments, and real-time hot topics for content research, competitor analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to run Douyin keyword search, creator-post retrieval, comment extraction, and hot-topic lookup commands. It supports marketing research, competitor monitoring, sentiment analysis, and trend tracking over public Douyin data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger broad network collection of Douyin search, post, hot-topic, and comment data.

Mitigation: Review prompts before execution, avoid ambiguous research requests, and constrain each run to the minimum query, URL, and result limit needed.

Risk: Queries, target URLs, and the Guaikei API token are sent to the third-party provider.

Mitigation: Use a dedicated, revocable GUAIKEI_API_TOKEN and avoid submitting sensitive queries or private target information.

Risk: Saved logs may contain third-party comments, profile metadata, video metadata, and large exported datasets.

Mitigation: Inspect and manage the local logs directory after use, retain only needed files, and ensure exports comply with platform rules and privacy obligations.

Risk: Server evidence reports a suspicious security verdict and notes unsafe token handling.

Mitigation: Review the skill before installation, rotate the token after testing, and run it only in an environment where network egress and generated files are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-search-post-comment-hot)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [JSON Schemas](assets/)
- [Guaikei Token and Usage Site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [shell commands, JSON, files, guidance]

**Output Format:** [JSON on stdout, operational messages on stderr, and optional saved JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14 or newer and a GUAIKEI_API_TOKEN environment variable; command results follow the bundled JSON Schema files.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, package.json, references/changelog.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
