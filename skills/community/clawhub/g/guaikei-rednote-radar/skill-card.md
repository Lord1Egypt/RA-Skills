## Description:

Retrieves public Xiaohongshu note, comment, author, and engagement data through Guaikei API commands for KOL screening, competitor analysis, trend research, and content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, marketers, content operators, and data analysts use this skill to search Xiaohongshu public notes, inspect note details and comments, monitor public creator posts, and prepare downstream analysis or reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note/profile URLs, returned public data, and GUAIKEI_API_TOKEN to Guaikei's API.

Mitigation: Use it only in environments approved for that data sharing, keep the token secret, and rotate the token if it is exposed.

Risk: Command results are saved locally under logs/ and may contain retrieved public data used for analysis.

Mitigation: Store, review, and delete logs according to the user's data-handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-rednote-radar)
- [Guaikei API website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, json data, guidance]

**Output Format:** [Markdown guidance with shell commands; CLI execution returns structured JSON and writes local JSON logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; sends Xiaohongshu keywords, note/profile URLs, returned public data, and the token to Guaikei's API.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
