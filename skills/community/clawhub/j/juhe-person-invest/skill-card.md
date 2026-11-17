## Description:

Looks up a natural person's external investments and company appointments through the Juhe person-investment API using a name, Chinese national ID number, and optional mobile number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill for authorized due-diligence workflows that need to summarize a person's company legal-representative, executive, or shareholder relationships. The skill validates required identifiers, calls the Juhe API, and formats returned company relationship records for review.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill handles sensitive personal identifiers, including name, Chinese national ID number, and optional mobile number.

Mitigation: Use only for legitimate authorized lookups, minimize retained query data, and redact identifiers in shared outputs.

Risk: API keys and query data can be exposed through command-line arguments, GET URLs, shell history, or logged stdout.

Mitigation: Prefer the JUHE_PERSON_INVEST_KEY environment variable or a protected local .env file, avoid GET URLs with real data, and disable or redact logs that capture raw JSON output.

## Reference(s):

- [Juhe Natural Person External Investment and Appointment API](https://www.juhe.cn/docs/api/id/320)
- [ClawHub skill listing](https://clawhub.ai/juhemcp/skills/juhe-person-invest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and formatted text or JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JUHE_PERSON_INVEST_KEY; returned personal identifiers should be masked or redacted before sharing or logging.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
