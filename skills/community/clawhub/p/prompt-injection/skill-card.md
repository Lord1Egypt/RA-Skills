## Description:

Helps agents contain prompt injection in untrusted text by removing LLM tool access, fencing input, validating decisions in code, and requiring explicit approvals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents handling untrusted messages, tickets, or web content use this skill to design or audit a contained LLM reading step, validate its output, and prevent text from authorizing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LLM CLI updates could change tool-isolation behavior.

Mitigation: Pin a tested CLI version and rerun the documented preflight after updates.

Risk: Mismanaged approval secrets or nonce records could weaken approval controls.

Mitigation: Keep approval secrets separate from provider credentials and maintain appropriate ledger permissions and retention.

## Reference(s):

- [Prompt Injection Containment on ClawHub](https://clawhub.ai/alexbloch-ia/skills/prompt-injection)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with code and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce an eight-check containment report with PASS/FAIL results.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
