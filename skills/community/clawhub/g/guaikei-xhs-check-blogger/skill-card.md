## Description:

Searches public Xiaohongshu posts by keyword, retrieves post details and comments, and monitors a blogger's public works for social media research and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brand marketers, operators, and data analysts use this skill to collect public Xiaohongshu post, comment, author, and profile-work data through the Guaikei API for trend research, competitor monitoring, KOL screening, and internal reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, target URLs, and the Guaikei API token to www.guaikei.com.

Mitigation: Install only when that data sharing is acceptable, treat GUAIKEI_API_TOKEN as a secret, and rotate or remove it if exposed.

Risk: Generated log files may contain target links, xsec_token values, comments, author metadata, and business research results.

Mitigation: Protect the logs/ directory and regularly delete generated files that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-check-blogger)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Structured JSON on stdout, saved JSON log files, and concise Markdown guidance for routing, inputs, and failure handling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; commands may write results to logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
