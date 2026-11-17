## Description:

Use when the user needs a model, data source, or tool API through OpenAny and has authorized that spend. Connect the lite MCP server, then search_apis, get_api, and run_api only after the user accepts the live price.

This skill is ready for commercial/non-commercial use.

## Publisher:

[comunionio](https://clawhub.ai/user/comunionio)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use OpenAny to find models, data sources, and tool APIs, review live prices, and invoke a selected API after the user approves the cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill may send task details and API inputs to OpenAny and the selected provider.

Mitigation: Avoid including sensitive information unless you are comfortable sharing it with those services.

Risk: Running an API may charge the user's OpenAny balance and may have side effects.

Mitigation: Read the live price and obtain the user's approval before calling run_api.

Risk: The security scan had partial coverage because a referenced local path could not be resolved.

Mitigation: Review the unresolved component before installation or use.

## Reference(s):

- [OpenAny](https://openany.si)
- [OpenAny documentation](https://openany.si/docs/)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions, Text]

**Output Format:** [Markdown or plain text, with JSON API inputs when invoking a service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live API prices are presented for approval before a call is run.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
