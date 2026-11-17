## Description:

Collects public Xiaohongshu content data through keyword note search, note detail retrieval, note comment retrieval, and creator post listing, then returns structured JSON for content research, competitor analysis, KOL screening, comment insight, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, brand marketers, analysts, and agents use this skill to gather public Xiaohongshu notes, comments, and creator posts for topic discovery, competitive monitoring, KOL evaluation, sentiment review, and trend reporting. The skill requires a Guaikei API token and should be used only for authorized public-data analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, URLs, and the Guaikei API token are sent to the Guaikei service, and the security evidence notes that the token is sent in URL query strings.

Mitigation: Use a dedicated, revocable token; avoid sensitive research targets on shared machines; and rotate the token if logs, shell history, or request traces may have exposed it.

Risk: Collected search results, note details, comments, and creator posts are automatically stored in local log files.

Mitigation: Periodically delete the local logs directory and avoid retaining collected data longer than needed for the authorized analysis.

Risk: The security evidence verdict is suspicious because the skill performs external data collection and stores results locally.

Mitigation: Review the intended data use, authorization scope, and local retention practices before deployment, especially for commercial or shared-machine workflows.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/guaikei-xiaohongshu-search-detail-comment-post)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Guidance]

**Output Format:** [Structured JSON on stdout with local JSON log archives and Markdown-style agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; each command reports status, error_code, request metadata, skill metadata, and results.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
