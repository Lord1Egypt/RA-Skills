## Description:

Check whether this agent is talking to a NEAR AI Cloud TEE endpoint or to an ordinary one, and cryptographically attest that endpoint. Reports which models the chain uses, which ones actually served recent turns, warns when a fallback sends prompts outside the enclave, verifies the Intel TDX quote, and uses the nearai-verify OpenClaw plugin for message-level proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eduv09](https://clawhub.ai/user/eduv09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect OpenClaw model routing and check NEAR AI Cloud endpoint and attestation evidence before relying on privacy claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An endpoint check does not establish trusted enclave software, and endpoint attestation is only a snapshot.

Mitigation: State the verification level and review which checks passed or were skipped; do not treat an endpoint check as proof of software trust.

Risk: Recent-history output does not prove which model completed a response, and fallback routing can send prompts outside the enclave.

Mitigation: Review routing and fallback behavior before sharing sensitive prompts, and do not present recent-history output as message-level proof.

Risk: The separate message-verification plugin uses a credential-backed integration.

Mitigation: Review the plugin and its permissions before enabling it, and limit credential access to what the integration requires.

## Reference(s):

- [NEAR AI Cloud verification](https://docs.near.ai/cloud/verification/)
- [NEAR AI Cloud private inference](https://docs.near.ai/cloud/private-inference/)
- [NEAR AI Cloud verifier](https://github.com/nearai/nearai-cloud-verifier)
- [Publisher-listed homepage](https://github.com/skalenetwork/smartclaws)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with optional JSON reports, shell commands, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports identify the verification level and checks performed; results depend on the selected command and available verification tools.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
