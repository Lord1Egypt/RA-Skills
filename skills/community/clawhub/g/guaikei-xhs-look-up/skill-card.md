## Description:

Looks up public Xiaohongshu content by keyword, note URL, comment thread, or creator profile and returns structured data for content research, competitor monitoring, KOL screening, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External teams, creators, marketers, data analysts, and agents use this skill to retrieve public Xiaohongshu search results, note details, comments, and creator posts before performing analysis or report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note or profile URLs, and the GUAIKEI_API_TOKEN to guaikei.com.

Mitigation: Install only when that data sharing is acceptable, treat the token as sensitive, and rotate it if it is exposed.

Risk: Fetched results are saved automatically to the local logs directory.

Mitigation: Review and clean saved logs after use when results may contain sensitive research, business, or account-analysis data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-look-up)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Node.js shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results include status, error_code, message, request metadata, skill_metadata, and results; successful runs are also saved under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package.json and skill metadata report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
