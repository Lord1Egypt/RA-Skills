## Description:

Searches public Xiaohongshu notes, retrieves note details and comments, and tracks a creator's public posts as structured data for content research, competitor analysis, KOL screening, and trend insight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketing teams, market analysts, and agents use this skill to collect public Xiaohongshu search results, note details, comments, and creator post lists for analysis and report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Guaikei API token is sent in URL query strings.

Mitigation: Use a scoped or replaceable token, avoid environments where proxy or request URLs are broadly logged, and rotate the token if URL logs may have exposed it.

Risk: Fetched Xiaohongshu user and comment data is automatically saved locally under logs/.

Mitigation: Treat local logs as sensitive working data, review retention and sharing practices, and delete outputs that are no longer needed.

Risk: Keywords and Xiaohongshu URLs are sent to the third-party Guaikei API service.

Mitigation: Avoid sensitive investigations and confirm the data use is authorized, platform-compliant, and appropriate for the intended purpose before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-search-and-track)
- [Guaikei service site](https://www.guaikei.com)
- [Options and usage reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Structured JSON results and concise Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save fetched public social-data results under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; source files declare 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
