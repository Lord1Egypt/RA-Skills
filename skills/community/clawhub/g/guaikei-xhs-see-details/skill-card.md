## Description:

Collects public Xiaohongshu/RED keyword, note, creator post, and comment data through GUAIKEI commands so agents can return structured JSON for content research, competitor monitoring, KOL screening, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, brand marketers, analysts, and agent developers use this skill to retrieve public Xiaohongshu/RED search results, note details, creator post lists, and comments for market research, competitor monitoring, KOL screening, trend analysis, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu links, keywords, and the GUAIKEI API token are sent to guaikei.com.

Mitigation: Use the skill only for approved public-data collection, confirm that this data sharing is acceptable, and use a dedicated low-privilege token when possible.

Risk: Collected results may be saved locally in plaintext logs.

Mitigation: Avoid running sensitive research on shared machines, protect the workspace, and periodically delete generated logs that are no longer needed.

Risk: Requests for private, login-gated, or unauthorized data are outside the supported use case.

Mitigation: Limit use to public Xiaohongshu/RED data and decline tasks involving login, hidden content, posting, liking, commenting, or following.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-see-details)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; command execution returns structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may save collected results to local plaintext logs and can return up to 10000 structured records when limits and service responses allow.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
