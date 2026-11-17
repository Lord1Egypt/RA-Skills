## Description:

Retrieves public Xiaohongshu notes, note details, comments, and creator posts for competitor content research and social media analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as content creators, brand marketers, market analysts, and social media operators use this skill to gather public Xiaohongshu content data for topic discovery, competitor monitoring, comment analysis, KOL screening, and trend research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, links, and the GUAIKEI_API_TOKEN are sent to the third-party guaikei.com API.

Mitigation: Install only when this data sharing is acceptable; store the token securely and rotate it if it may have appeared in request logs or saved artifacts.

Risk: Retrieved data may be written to the local logs directory in plaintext.

Mitigation: Treat generated logs as sensitive; review, protect, delete, or exclude the logs directory from commits and shared archives.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-competitor-content)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured JSON data with brief Markdown summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; retrieved results may be saved locally under logs/ as plaintext.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
