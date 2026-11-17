## Description:

Retrieves public Xiaohongshu (Rednote) notes, note details, creator posts, and comments so agents can support trend monitoring, competitor analysis, KOL screening, and comment review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, analysts, and operations teams use this skill to collect structured public Xiaohongshu data for content planning, market trend analysis, competitor monitoring, KOL review, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keywords, Xiaohongshu URLs, limits, and the GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Review whether this external API flow is acceptable before installation and rotate the token if exposure is suspected.

Risk: Full command results are saved under logs/ and may include research history or Xiaohongshu URLs.

Mitigation: Avoid committing or syncing logs, delete them when no longer needed, and treat saved results as sensitive operational data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-rednote-growth)
- [Guaikei official site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI commands return structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and saves command results under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
