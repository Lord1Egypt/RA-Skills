## Description:

Helps agents search public Douyin content, retrieve real-time trending topics, collect creator posts, and fetch video comments as structured JSON for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and marketing teams use this skill to collect public Douyin search results, creator posts, comments, and trending topics for content research, competitive monitoring, sentiment review, and report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin queries, URLs, and related request data to the third-party service at www.guaikei.com.

Mitigation: Use it only when third-party processing is intended and avoid submitting private, confidential, or unnecessary data.

Risk: GUAIKEI_API_TOKEN is sensitive and the server evidence flags third-party token handling risk.

Mitigation: Store the token in an environment variable, do not paste it into prompts or logs, and rotate it if exposure is suspected.

Risk: Collected search, post, and comment results are saved locally under logs by default.

Mitigation: Review, redact, or delete generated log files before sharing workspaces or reports.

Risk: The skill may trigger on broad content-research requests even when Douyin is not explicitly named.

Mitigation: Confirm the user wants public Douyin data collection before running broad search, post, or comment commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-fetch-parse-deliver-comments)
- [Repository URL from Skill Metadata](https://github.com/um-why/douyin-search-openclaw)
- [README](artifact/readme.md)
- [Options Reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [Request and Response JSON Schemas](artifact/assets/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Structured JSON on stdout, stderr status messages, and local JSON log files for search, post, and comment workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 16.14.0 and GUAIKEI_API_TOKEN; search, post, and comment results are saved under logs by default.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
