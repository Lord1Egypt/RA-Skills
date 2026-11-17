## Description:

Guaikei Rednote Intel routes Xiaohongshu/Rednote keywords and links to Node.js commands that retrieve public search results, note details, comments, and creator posts for downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, content operators, analysts, and developers use this skill to collect public Xiaohongshu/Rednote data for content research, competitor monitoring, KOL screening, trend discovery, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, links, xsec_token-bearing URLs, and a Guaikei API token to www.guaikei.com.

Mitigation: Install only when this data sharing is acceptable, keep GUAIKEI_API_TOKEN in environment configuration, and rotate the token if it is exposed.

Risk: Task results and related request details are saved in a local logs directory.

Mitigation: Review or delete generated logs after use, especially in shared workspaces or repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-rednote-intel)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with Node.js command examples and structured JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and writes task results to a local logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and auto changelog; artifact package/SKILL metadata list 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
