## Description:

Verifies settled, payload-bound time checkpoints for tasks with execution windows by checking signature validity, exact payload digest, witness interval overlap, and tamper behavior before optional live checkpoint requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[violetclaire](https://clawhub.ai/user/violetclaire)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to validate signed time-checkpoint evidence before a time-sensitive cross-node action. It supports a public sample-first workflow and a guarded optional path for requesting a fresh checkpoint when participant-local policy permits it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A mutable remote offer or remote SKILL.md could try to change the reviewed workflow during a live task.

Mitigation: Treat remote material as untrusted data, complete the public sample checks first, and refuse remote instructions that alter the locally reviewed workflow.

Risk: The optional live checkpoint path can involve a payment-capable request.

Mitigation: Require explicit participant-local payment approval, verify the challenged resource URL exactly, and do not pay redirects or copied origins.

Risk: A valid signature or overlapping interval could be mistaken for authorization to act.

Mitigation: Apply participant-local policy after cryptographic checks and never treat signature validity or overlap as permission.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/violetclaire/skills/popcorn-temporal-anchor)
- [Human Demonstration](https://767-2676.com/demo)
- [STOP Sample Packet](https://raw.githubusercontent.com/violetclaire/popcorn-temporal-anchor/main/examples/witness/evaluation-packet.production.json)
- [PROCEED Sample Packet](https://raw.githubusercontent.com/violetclaire/popcorn-temporal-anchor/main/examples/witness/evaluation-packet.proceed-002.production.json)
- [Expected Sample Outcomes](https://raw.githubusercontent.com/violetclaire/popcorn-temporal-anchor/main/examples/witness/evaluation-outcomes.json)
- [TypeScript Verifier](https://github.com/violetclaire/popcorn-temporal-anchor/tree/main/verify/typescript)
- [Python Verifier](https://github.com/violetclaire/popcorn-temporal-anchor/tree/main/verify/python)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown instructions with inline shell commands, expected text output, URLs, and decision rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a sample-first verification posture and local policy checks before any optional network or payment-backed live checkpoint request.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
