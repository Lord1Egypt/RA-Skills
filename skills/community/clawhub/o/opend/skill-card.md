## Description:

Agentic trading and market-data workflows for Futu OpenD (MooMoo/Futu OpenAPI), including secret-ref credential loading, account discovery, position queries, and simulated or live order placement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscraters](https://clawhub.ai/user/oscraters)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to let an agent run local OpenD market-data checks, account and position queries, and simulated or explicit live order actions through a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect live trading accounts when REAL trading is enabled.

Mitigation: Keep SIMULATE as the default and require an explicit live-trade approval step before allowing REAL order placement or cancellation.

Risk: Legacy credential paths can store or expose trading credentials outside the preferred hosted secret-management path.

Mitigation: Use OpenClaw-managed secret injection for hosted or shared-agent deployments and reserve env, config, and keyring modes for controlled local workflows.

Risk: OPEND_SDK_PATH and trading SDK dependencies can change the code imported at runtime.

Mitigation: Use OPEND_SDK_PATH only with trusted directories and pin or review MooMoo/Futu SDK dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oscraters/skills/opend)
- [Futu OpenAPI references](references/api_docs.md)
- [Futu OpenAPI portal](https://www.futunn.com/OpenAPI)
- [Futu OpenAPI documentation](https://openapi.futunn.com/futu-api-doc/en/)
- [Get market snapshot API](https://openapi.futunn.com/futu-api-doc/en/quote/get-market-snapshot.html)
- [Place order API](https://openapi.futunn.com/futu-api-doc/en/trade/place-order.html)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON by default, with optional text output and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may call a local OpenD service and require the MooMoo/Futu SDK, credentials, and explicit REAL trading intent for live orders.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
