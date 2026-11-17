## Description:

Fetches public Douyin data through keyword search, creator post collection, video comment retrieval, and real-time hot-list queries for content research, competitor analysis, sentiment review, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect structured public Douyin search, creator post, comment, and hot-list data for marketing research, competitor monitoring, public-opinion analysis, and short-video topic planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin queries, URLs, and the Guaikei API token are sent to www.guaikei.com.

Mitigation: Treat GUAIKEI_API_TOKEN as a secret, avoid shared environments, and review network use before installation.

Risk: The security review flags token authentication through URL query strings.

Mitigation: Move token authentication to request headers before broad deployment.

Risk: Search, post, and comment results may be saved under logs by default.

Mitigation: Review log retention, avoid sensitive queries, and remove generated logs that are no longer needed.

Risk: The security review notes runtime promotional contact or redirection behavior that conflicts with the skill's stated neutral error policy.

Mitigation: Remove runtime promotional contact messages before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-public-data-pipeline)
- [Guaikei service and token documentation](https://www.guaikei.com)
- [Usage documentation](artifact/readme.md)
- [Complete CLI options](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [CLI request and response JSON Schemas](artifact/assets/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Files, Guidance]

**Output Format:** [Structured JSON from Node.js CLI commands, with stderr logs and optional JSON files saved under logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14 or newer and a GUAIKEI_API_TOKEN environment variable.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, references/changelog.md, src/config/constants.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
