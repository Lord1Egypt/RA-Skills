## Description:

Evaluate proposed agent actions against explicit scope, identity, permissions, risk, budget, and approval requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mdjahid11978-design](https://clawhub.ai/user/mdjahid11978-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to assess proposed consequential actions against identity, scope, permissions, risk, budget, and approval requirements, and to produce a decision with audit evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A policy decision may be misleading if identity, tenant, scope, or permission context is incomplete or comes only from untrusted request content.

Mitigation: Resolve policy from trusted server-side context, require approval when the action exceeds granted autonomy, and return a reason with an evidence reference.

## Reference(s):

- [Server-resolved source repository](https://github.com/mdjahid11978-design/Jahids-skills/tree/main/skills/jahids-governor-policy)
- [ClawHub skill page](https://clawhub.ai/mdjahid11978-design/skills/jahids-governor-policy)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured policy decision (ALLOW, DENY, or REQUIRE_APPROVAL) with a reason and evidence reference]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes audit evidence; the exact serialization depends on the host system.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
