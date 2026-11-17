## Description:

Retrieves structured public Xiaohongshu/XHS note search results, note details, comments, and creator posts through Guaikei for competitor monitoring, trend research, KOL screening, and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, brand marketers, market analysts, and agent developers use this skill to collect public Xiaohongshu/XHS data before producing summaries, comparisons, reports, trend analysis, KOL screening, or comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the GUAIKEI API token and Xiaohongshu keywords or URLs to guaikei.com, including credentials in URL query strings.

Mitigation: Use a dedicated, revocable GUAIKEI_API_TOKEN and install the skill only when sending those inputs to Guaikei is acceptable.

Risk: Collected comments, profile data, and token-bearing Xiaohongshu URLs may be saved automatically under local logs/ files.

Mitigation: Review the logs/ directory after use, delete files that are no longer needed, and avoid submitting sensitive links.

Risk: The skill is limited to public Xiaohongshu/XHS data and depends on a third-party API service.

Mitigation: Confirm authorization and acceptable-use requirements before running collection tasks, and do not use it for private, hidden, or login-only content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-competitor-watch)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results may also be written to local logs/ files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
