## Description:

Provides structured public Xiaohongshu data for content discovery, competitor monitoring, KOL screening, creator post monitoring, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketers, analysts, and content operations teams use this skill to retrieve public Xiaohongshu posts, post details, comments, and creator activity for data-supported planning and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note/profile URLs, and API-authenticated requests to www.guaikei.com.

Mitigation: Use it only for data you are authorized to share with the Guaikei service, and avoid sensitive research terms or private links.

Risk: GUAIKEI_API_TOKEN is used for authenticated requests and should be treated as a secret.

Mitigation: Store the token in a protected environment variable, rotate it if exposed, and avoid sharing command transcripts or environments that may reveal it.

Risk: Fetched content and signed URLs may be saved locally in the generated logs directory.

Mitigation: Protect or regularly delete generated logs, especially when handling customer, campaign, or competitive research data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-creator-list)
- [Guaikei service website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with inline shell commands; CLI execution returns JSON and writes JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; results are limited to public Xiaohongshu data returned through the Guaikei API.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
