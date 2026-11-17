## Description:

Collects public Xiaohongshu/RedNote search results, note details, creator posts, and comments for structured content, competitor, KOL, trend, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, analysts, content operators, and marketing teams use this skill to retrieve structured public Xiaohongshu/RedNote data for downstream analysis, reporting, monitoring, and comparison. It is intended for public content only and does not support logged-in, private, or hidden data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu targets and collected public data are sent to the Guaikei service.

Mitigation: Use the skill only when that external data transfer is acceptable for the intended workflow and data policy.

Risk: GUAIKEI_API_TOKEN and Xiaohongshu xsec_token URLs are sensitive and may appear in command inputs or saved outputs.

Mitigation: Avoid shared workspaces, treat tokens and URLs as secrets, and prefer a release that redacts tokens or passes authentication in headers.

Risk: Command results may be saved automatically as complete local result files.

Mitigation: Review the logs directory after use and delete retained result files that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-rednote-analytics)
- [Guaikei service website](https://www.guaikei.com)
- [Options and usage reference](artifact/references/options.md)
- [Artifact changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance, Configuration]

**Output Format:** [Markdown guidance with shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; command results may be saved locally under logs/.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact metadata also contains 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
