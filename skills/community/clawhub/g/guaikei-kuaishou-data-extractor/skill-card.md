## Description:

Fetches public Kuaishou data through Guaikei API commands for keyword video search, creator post listings, and video comment retrieval, returning structured JSON for downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operations teams, marketers, analysts, and developers use this skill to collect public Kuaishou search results, creator post lists, and video comments for trend research, competitor monitoring, KOL screening, and downstream reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, profile or video URLs, request parameters, and the GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use only where sharing those inputs with Guaikei is approved; scope and rotate the API token according to the user's credential policy.

Risk: Fetched comments and creator metadata may contain personal data and task results are saved locally under logs.

Mitigation: Treat results as potentially personal data, follow applicable platform and legal obligations, and delete or secure local logs when retention is not needed.

Risk: The skill is limited to public Kuaishou data and may return empty or error responses for invalid, unavailable, private, or rate-limited targets.

Mitigation: Check status and error_code before using results, avoid inventing data from empty responses, and retry or narrow requests only when the error condition supports it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-data-extractor)
- [Guaikei service website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Release changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Guidance]

**Output Format:** [Structured JSON status objects and local JSON log files, with brief Markdown guidance around commands and errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; responses include status, error_code, request, skill_metadata, and results.]

## Skill Version(s):

1.0.0 (source: skill frontmatter, package.json, release evidence, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
