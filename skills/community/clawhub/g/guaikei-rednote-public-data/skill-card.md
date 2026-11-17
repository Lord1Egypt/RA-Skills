## Description:

Retrieves public Xiaohongshu/Rednote search results, note details, comments, and creator posts through Guaikei for content research and market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content operators, and data analysts use this skill to collect public Xiaohongshu/Rednote data for topic discovery, competitor monitoring, KOL screening, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keywords, Xiaohongshu URLs, and GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Confirm that this external API use is acceptable, use a dedicated revocable token, and monitor token or quota use.

Risk: Generated logs may contain full retrieved datasets and token-bearing Xiaohongshu URLs.

Mitigation: Protect or delete generated logs after use, especially before sharing the workspace or outputs.

Risk: The skill is intended for public Xiaohongshu/Rednote data only.

Mitigation: Use only public keywords or supported public URLs and do not request private, hidden, or logged-in content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-rednote-public-data)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei official site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text, Guidance]

**Output Format:** [JSON emitted by command-line scripts, with brief status text and follow-on analysis or summaries from the agent when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; command scripts may save retrieved datasets under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
