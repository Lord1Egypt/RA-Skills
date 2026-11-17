## Description:

Collects public Douyin content through command-line tools for keyword search, creator posts, comments, and trending topics; it does not support editing, publishing, or private data access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content operations, marketing, research, and data-analysis users use this skill to retrieve public Douyin search results, creator posts, comments, and hot-list entries for topic research, competitor monitoring, sentiment review, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin keywords, target URLs, and the Guaikei API token are sent to guaikei.com.

Mitigation: Use the skill only for explicit Douyin data requests, confirm third-party data-sharing expectations, protect GUAIKEI_API_TOKEN, and rotate the token if it may have been exposed in URL-query form.

Risk: Search, post, and comment results are saved locally under logs.

Mitigation: Restrict access to generated log files, delete them when no longer needed, and avoid retaining collected data beyond the intended analysis task.

Risk: The activation scope is broad for Douyin-related operations.

Mitigation: Confirm the user's requested Douyin action and required keyword, creator profile URL, video URL, or aweme_id before running a command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-collect-public-data)
- [Guaikei API service](https://www.guaikei.com)
- [Complete option reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON command output with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; successful command output is also saved under the skill's logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill metadata, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
