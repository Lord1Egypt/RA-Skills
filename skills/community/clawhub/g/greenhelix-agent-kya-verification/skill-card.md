## Description:

Provides a Know Your Agent (KYA) implementation playbook for building agent identity binding, authority scoping, runtime behavioral monitoring, and tamper-evident audit trails for EU AI Act compliance, with Python examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this guide to design KYA controls for autonomous agent commerce platforms, including identity binding, authority scoping, runtime monitoring, audit trails, and reputation scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide may be treated as deployable KYA and payment-governance code even though the security evidence flags unsafe authority and revocation controls.

Mitigation: Treat it as reference material and require fail-closed identity checks, trusted operator verification, complete delegated-scope validation, revocation and escrow controls, sandbox defaults, timeouts, rollback, and secret-management review before implementation.

Risk: Examples involving live endpoints or signing keys could be copied into real environments without adequate isolation.

Mitigation: Run examples only in sandboxed test environments, protect AGENT_SIGNING_KEY as a secret, and add explicit production approval gates before using any pattern with live accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-kya-verification)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guide with Python code examples and configuration metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; references AGENT_SIGNING_KEY for signing examples and declares no install step.]

## Skill Version(s):

1.3.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
