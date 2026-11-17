## Description:

Helps agents search Douyin by keyword, fetch public creator posts, pull public video or note comments, and retrieve real-time hot lists for short-video research and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content analysts, and agents use this skill to collect public Douyin search, creator-post, comment, and hot-list data for content research, competitor analysis, sentiment review, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the API token, Douyin search terms, and Douyin URLs to Guaikei services.

Mitigation: Use a low-privilege or disposable token where possible, avoid sensitive or ambiguous requests, and prefer a revised release that transmits credentials in headers.

Risk: Fetched public Douyin data is saved locally by default.

Mitigation: Run the skill in a controlled workspace, review generated logs for sensitive content, and delete or protect retained JSON files according to local policy.

Risk: Broad natural-language triggers can invoke the skill even when the user does not explicitly name Douyin.

Mitigation: Confirm the intended platform and data scope before running commands for ambiguous short-video research requests.

Risk: Security evidence reports that runtime output contradicts token-handling and marketing-message promises.

Mitigation: Review stderr and error output before deployment, and prefer a revised version that removes runtime contact or marketing messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-pull-comments-stream)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Repository listed in skill metadata](https://github.com/um-why/douyin-search-openclaw)
- [Guaikei token and help site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [JSON CLI output with shell command guidance and local JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14.0 and GUAIKEI_API_TOKEN; fetched results are saved to logs/ by default.]

## Skill Version(s):

1.0.0 (source: server evidence, frontmatter, package.json, constants)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
