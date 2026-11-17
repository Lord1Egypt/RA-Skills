## Description:

Openalgo Executor lets agents place market or limit orders, retrieve open positions, and fetch symbol quotes through an OpenAlgo API endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anthonyabraham1379-pixel](https://clawhub.ai/user/anthonyabraham1379-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to have an agent perform OpenAlgo trading operations and retrieve portfolio or market data. Because order commands can place real trades, it is intended for environments where endpoint trust and human order confirmation are enforced.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order commands can place real trades through OpenAlgo.

Mitigation: Require human confirmation before live order submission and test commands against a non-production account or paper-trading setup when possible.

Risk: The security summary reports an undocumented remote HTTP endpoint instead of the documented local OpenAlgo server.

Mitigation: Change or verify the default endpoint before installation, and use only a trusted local or authenticated HTTPS OpenAlgo server.

Risk: Custom or ngrok URLs may send trading requests to an untrusted service.

Mitigation: Avoid untrusted custom URLs and confirm the endpoint owner, transport security, and authentication before allowing order commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anthonyabraham1379-pixel/skills/openalgo-executor)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON, guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OpenAlgo endpoint can be configured with a URL argument; order commands may submit live trading requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
