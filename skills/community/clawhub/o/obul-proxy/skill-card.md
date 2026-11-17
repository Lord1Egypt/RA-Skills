## Description:

Obul Proxy (x402) helps agents route requests through Obul to call x402-enabled APIs while Obul handles payment negotiation automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notbdu](https://clawhub.ai/user/notbdu)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to construct authenticated Obul proxy requests, check proxy health, and troubleshoot x402 payment-related responses for upstream API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Open-ended proxy requests can reach arbitrary upstream services and may incur variable x402 charges.

Mitigation: Approve the upstream URL and expected cost before use, and restrict use to intended x402 API calls.

Risk: The skill requires an Obul API key for billable proxy calls.

Mitigation: Store OBUL_API_KEY in an environment variable, avoid logging it, and do not expose it in client-side code.

Risk: Sensitive data sent through unknown upstream services may leave the user's control.

Mitigation: Review request payloads and avoid sending secrets or sensitive data to untrusted upstream endpoints.

## Reference(s):

- [Obul homepage](https://obul.ai)
- [Obul proxy health endpoint](https://proxy.obul.ai/healthz)
- [ClawHub skill listing](https://clawhub.ai/notbdu/skills/obul-proxy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OBUL_API_KEY; proxied requests may incur upstream x402 charges.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
