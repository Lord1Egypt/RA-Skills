## Description:

Retrieve and analyze NOTAMs (Notices to Airmen) for airports worldwide using the Notamify Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[damians21](https://clawhub.ai/user/damians21)

### License/Terms of Use:

MIT-0

## Use Case:

Pilots, dispatchers, and aviation professionals use this skill to retrieve, summarize, and interpret active, nearby, historical, and route-specific NOTAMs for flight planning and situational awareness. The skill also guides agents in writing short Python scripts that query the Notamify SDK and present aviation impacts clearly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on `notamify-sdk` and executes generated Python scripts to query aviation data.

Mitigation: Install the SDK in a virtual environment, pin and review the package version where possible, and review generated scripts before execution.

Risk: The workflow requires a Notamify API token.

Mitigation: Expose only the `NOTAMIFY_TOKEN` needed for this workflow and never hardcode tokens in scripts.

Risk: NOTAM summaries and interpretations may be incomplete or unsuitable as the sole basis for operational decisions.

Mitigation: Treat returned NOTAM analysis as informational and verify flight decisions against official aviation sources.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/damians21/skills/notamify)
- [Notamify API docs](https://skymerse.gitbook.io/notamify-api)
- [Notamify Python SDK docs](https://skymerse.gitbook.io/notamify-api/sdk/python)
- [Notamify API manager](https://notamify.com/api-manager)
- [Notamify MCP source](https://github.com/skymerse/notamify-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SDK query parameters, summarized NOTAM impacts, and operational verification reminders.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
