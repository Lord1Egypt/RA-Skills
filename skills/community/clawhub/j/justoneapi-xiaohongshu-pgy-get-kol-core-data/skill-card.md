## Description:

Call GET /api/xiaohongshu-pgy/get-kol-core-data/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Core Metrics through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and campaign analysts use this skill to retrieve Xiaohongshu Creator Marketplace creator core metrics by KOL ID for benchmarking, vetting, and campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JustOneAPI tokens can be exposed through command-line arguments, shell history, logs, or screenshots.

Mitigation: Use short-lived, low-scope tokens where available, avoid sharing command transcripts, and rotate any token that may have been exposed.

Risk: The endpoint uses token authentication in query parameters, which can place token values in request URLs and downstream logs.

Mitigation: Review logging and proxy behavior before using real tokens, and restrict access to logs that may contain request URLs.

## Reference(s):

- [Operation reference](artifact/generated/operations.md)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_core_data&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_core_data&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-get-kol-core-data)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown summary followed by raw JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and kolId; optional query filters are passed as JSON parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
