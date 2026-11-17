## Description:

guaikei·小红书内容雷达 helps agents query public Xiaohongshu content for keyword search, note details, comments, and creator post lists; it does not support login, posting, liking, private content, or cross-platform retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, analysts, and agents use this skill to retrieve public Xiaohongshu search results, note details, comments, and creator posts for topic research, competitor or KOL monitoring, trend tracking, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu queries, supplied links, and GUAIKEI_API_TOKEN are sent to a third-party GuaiKei service.

Mitigation: Install only when that data flow is acceptable, treat GUAIKEI_API_TOKEN as a secret, and rotate the token if it is exposed.

Risk: Saved command results may contain research history, public comments, and tokenized Xiaohongshu URLs.

Mitigation: Review and restrict access to the logs directory, and clear retained outputs when they are no longer needed.

Risk: The security verdict is suspicious because credential handling and saved results require user review before installation.

Mitigation: Review the skill and its security guidance before deployment, especially in environments with sensitive research workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-content-radar)
- [GuaiKei API token and support site](https://www.guaikei.com)
- [Options and invocation guide](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; command results may also be saved under logs/ and can include research history, public comments, and tokenized URLs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata lists 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
