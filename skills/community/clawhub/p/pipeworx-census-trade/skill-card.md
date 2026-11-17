## Description:

Access detailed US international trade data including imports, exports, trade balance, and trends by commodity and country.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to query US Census international trade data through a Pipeworx-hosted MCP service for imports, exports, trade balance, and monthly trends by commodity or country.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trade query details are sent to a third-party Pipeworx-hosted MCP service.

Mitigation: Avoid including secrets, personal data, or unrelated conversation context in queries.

Risk: Returned trade data is remote service output rather than locally verified Census data.

Mitigation: Validate important figures against authoritative Census sources before relying on them for decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, API Calls, Configuration instructions]

**Output Format:** [Markdown or plain text responses from a remote MCP service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes Census trade query details to a third-party Pipeworx endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
