## Description:

Build event-driven agent commerce systems using saga patterns, compensating transactions, dead letter handling, exactly-once processing, backpressure, async escrow settlement, event bus architecture, and webhook integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this guide to design asynchronous agent commerce workflows for long-running escrow evaluations, multi-agent negotiations, distributed transaction sagas, dead letter recovery, exactly-once event handling, backpressure, and webhook-driven settlement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production-framed examples include automated financial escrow release and dispute flows without enough validation or user control.

Mitigation: Keep examples in a sandbox, verify signed or authorized event sources, check authoritative escrow state before release or dispute actions, and require manual approval or strict policy limits for real-money settlement.

Risk: Illustrative code could be copied into an agent with overly broad credentials or unrestricted API access.

Mitigation: Use scoped credentials, restrict API origins, and review the implementation before installing or adapting it for a live system.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mirni/skills/greenhelix-async-agent-commerce)
- [GreenHelix Sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API Endpoint](https://api.greenhelix.net/v1)
- [GreenHelix Agent Production Hardening](https://clawhub.ai/skills/greenhelix-agent-production-hardening)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with Python code examples, shell commands, configuration snippets, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing educational content; examples require independent review before production use.]

## Skill Version(s):

1.3.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
