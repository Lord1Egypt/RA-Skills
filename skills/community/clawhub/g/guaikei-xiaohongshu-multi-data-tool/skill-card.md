## Description:

Collects structured public Xiaohongshu data for keyword search, note details, comments, and creator posts, with JSON outputs for content research, comparison, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External content creators, marketers, analysts, and operators use this skill to retrieve public Xiaohongshu content data, compare posts or creators, analyze comments, monitor competitors, and prepare reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note or profile URLs, and GUAIKEI_API_TOKEN-backed requests to a third-party API.

Mitigation: Use only approved tokens, confirm the data-sharing authorization before running commands, and rotate the token if request details may have been exposed.

Risk: Generated logs can contain investigated links, xsec_token-bearing URLs, comments, profile-linked data, and full collected results.

Mitigation: Keep the workspace private, avoid committing logs, delete collected logs when no longer needed, and treat exported results as sensitive.

Risk: The skill is limited to public Xiaohongshu data and may return empty or error results for deleted, unavailable, private, or unauthorized content.

Mitigation: Check the returned status and error code before drawing conclusions, and request a different valid public link or broader keyword when the command reports no usable data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-xiaohongshu-multi-data-tool)
- [Guaikei API Service](https://www.guaikei.com)
- [Options and Calling Guide](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, Markdown]

**Output Format:** [Markdown guidance with inline shell commands; command results are structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; command runs can save collected JSON results to local logs.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact files report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
