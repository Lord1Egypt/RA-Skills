## Description:

Collects public Kuaishou/Kwai search results, creator post data, and video comments through Guaikei APIs and returns structured JSON for analysis workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, marketers, and analysts use this skill to retrieve public Kuaishou keyword results, creator post lists, and video comments for trend research, competitive monitoring, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou query targets and requested public content are sent to the third-party Guaikei API service.

Mitigation: Use the skill only when the workspace and user are approved to send those targets to www.guaikei.com.

Risk: Fetched public comments, posts, and search results are retained in local plaintext logs.

Mitigation: Avoid shared workspaces for sensitive analysis, review the logs directory after use, and delete logs that should not be retained.

Risk: The GUAIKEI_API_TOKEN can authorize API access if exposed.

Mitigation: Provide the token through a protected environment variable and do not print, paste, or share it in prompts, logs, or reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-public-comment-fetcher)
- [Guaikei API Service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance, Configuration]

**Output Format:** [JSON result envelopes with status, error_code, request metadata, skill_metadata, and results, plus concise Markdown guidance when an agent explains usage or failures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are also saved as local plaintext JSON logs under the skill's logs directory.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
