## Description:

Prevents panic-driven errors by enforcing a calm, step-by-step recovery process after mistakes or critical feedback to ensure safe, trusted fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanhuelsing](https://clawhub.ai/user/vanhuelsing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of agent systems use this skill to help agents recover safely after mistakes, critical feedback, or pressure to rush a fix. It is especially relevant for agents that can affect production systems, sensitive data, infrastructure, or multi-agent delegation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may pause and wait for approval during urgent production, infrastructure, credential, or data incidents.

Mitigation: Use role-specific triggers, trusted feedback sources, timeout or escalation behavior, and pre-approved reversible containment actions for genuine emergencies.

Risk: Over-applying the protocol can create unnecessary approvals or slow routine low-risk corrections.

Mitigation: Apply the documented severity assessment: reserve the full protocol for high-risk situations, use abbreviated recovery for medium issues, and allow simple acknowledge-fix-verify handling for low-risk mistakes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vanhuelsing/skills/panic-prevention)
- [README](artifact/README.md)
- [Protocol flow](artifact/PROTOCOL-FLOW.md)
- [Panic scenarios](artifact/examples/panic-scenarios.md)
- [Test scenarios](artifact/tests/test-scenarios.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown protocol guidance with checklists, examples, and integration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no runtime dependencies.]

## Skill Version(s):

1.0.5 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
