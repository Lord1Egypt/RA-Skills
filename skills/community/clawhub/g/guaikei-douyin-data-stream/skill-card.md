## Description:

Retrieves public Douyin keyword search results, creator posts, video comments, and hot topics through Node.js command-line tools that return structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content analysts, marketers, and agents use this skill to collect public Douyin data for short-video topic research, competitor monitoring, comment analysis, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan says Douyin URLs, keywords, and GUAIKEI_API_TOKEN are sent to www.guaikei.com, with token values passed in URL query strings.

Mitigation: Use a scoped token where available, rotate it regularly, avoid sharing command output or request traces, and review whether the data sent to the service is appropriate for the user or organization.

Risk: The security scan notes that search, post, and comment results are written under the skill logs directory by default.

Mitigation: Treat generated logs as user data, restrict filesystem access to the skill directory, and delete or archive logs according to the organization's retention policy.

Risk: The security scan reports mismatches between documentation and runtime authentication messages, including non-neutral support messaging in runtime paths.

Mitigation: Review authentication-error output before deployment and ensure user-facing failures do not expose unexpected contact details or marketing text.

Risk: The skill has broad natural-language triggers for short-video, creator, comment, and trend queries, including cases where Douyin is not named explicitly.

Mitigation: Confirm platform intent before running commands when a user request could refer to another platform or to private, non-public data.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-data-stream)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei service and token help](https://www.guaikei.com)
- [CLI JSON schemas](assets/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Files, Guidance]

**Output Format:** [JSON from stdout with operational logs on stderr and archived JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; individual requests can return up to 10000 public records.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog, constants.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
