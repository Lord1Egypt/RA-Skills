## Description:

Dispatches HTTP 402 payment-required responses to x402 or MPP playbooks, guides confirmation and signing, and returns authorization headers for retrying payment-gated requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to access payment-gated HTTP resources by decoding supported 402 payment challenges, confirming payment terms, signing with an OKX wallet flow when appropriate, and replaying requests with the required payment header.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment authorization could approve terms the user did not clearly intend, including the wrong token, amount, recipient, network, or scheme.

Mitigation: Display decoded payment terms and proceed only after explicit user confirmation.

Risk: Local private-key fallback could expose sensitive signing material.

Mitigation: Prefer wallet or TEE signing and use a local private key only when necessary after the user explicitly chooses it.

Risk: Untrusted 402 headers or JSON could be copied into shell commands unsafely.

Mitigation: Use only trusted payment endpoints and avoid pasting untrusted header or JSON values directly into shell command strings.

## Reference(s):

- [MPP Protocol Playbook](artifact/protocols/mpp.md)
- [x402 Protocol Playbook](artifact/protocols/x402.md)
- [OKX Web3](https://web3.okx.com)
- [x402](https://x402.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and ready-to-paste HTTP authorization header strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for explicit user confirmation before wallet checks or signing.]

## Skill Version(s):

3.1.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
