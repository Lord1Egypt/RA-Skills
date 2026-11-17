## Description:

Searches public Xiaohongshu (RedNote) notes, retrieves note details and comments, and fetches creator public posts as structured data for trend discovery, competitor analysis, KOL screening, and comment insight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, marketers, content operators, data analysts, and developers use this skill to collect public Xiaohongshu content data for keyword research, note and comment analysis, creator monitoring, competitor tracking, and KOL evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that Xiaohongshu keywords, full supplied links, and the Guaikei API token are sent to the Guaikei service.

Mitigation: Install only when that data transfer is acceptable, avoid sensitive or private links, and treat xsec_token-bearing URLs as sensitive.

Risk: The security evidence reports that tokens and token-bearing links are sent through query strings.

Mitigation: Avoid sharing command traces or network logs and prefer a future version that moves credentials out of query strings.

Risk: The security evidence reports that retrieved data is automatically saved locally.

Mitigation: Review or delete generated logs after use and run the skill only in workspaces with appropriate data retention controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-kol-finder)
- [Guaikei Service Website](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with bash command examples and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may write retrieved results to local logs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata also reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
