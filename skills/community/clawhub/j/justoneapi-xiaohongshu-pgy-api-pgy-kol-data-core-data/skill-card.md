## Description:

Call GET /api/xiaohongshu-pgy/api/pgy/kol/data/core_data/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Core Metrics through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing analysts use this skill to call JustOneAPI for Xiaohongshu Creator Marketplace (Pugongying) creator core metrics by userId, supporting creator vetting, benchmarking, and campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JustOneAPI tokens can be exposed through command-line arguments or URL query logs.

Mitigation: Use a narrowly scoped token when possible, avoid shell tracing or logging command lines, and rotate the token if it may have appeared in logs.

Risk: Backend errors or shared request URLs may contain query strings with sensitive token or request data.

Mitigation: Do not share full request URLs or raw errors that may contain query strings; redact sensitive fields before forwarding diagnostics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-api-pgy-kol-data-core-data)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_pgy_kol_data_core_data&utm_content=project_link)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_pgy_kol_data_core_data&utm_content=project_link)
- [Generated operations reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Node.js shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; required endpoint parameter is userId.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
