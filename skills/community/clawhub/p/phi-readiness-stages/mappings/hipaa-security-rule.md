# HIPAA Security Rule Mapping

This companion reference maps PRS to the current HIPAA Security Rule baseline. It is not a substitute for live source verification or legal review.

Last reviewed against official source registry: March 17, 2026.

## Mapping approach

PRS does not restate every Security Rule standard. Instead, it groups mandatory readiness questions into operational domains that track the current rule's administrative, physical, and technical safeguard structure.

For row-level traceability, use `mappings/hipaa-security-rule-crosswalk.md`.

## PRS domain mapping

| PRS domain | Security Rule area |
| --- | --- |
| access control | technical safeguards |
| audit controls | technical safeguards |
| integrity | technical safeguards |
| transmission security | technical safeguards |
| encryption and secrets handling | technical safeguards plus implementation choices |
| risk analysis and remediation | administrative safeguards |
| workforce security | administrative safeguards |
| incident response | administrative safeguards |
| contingency and restore confidence | administrative safeguards |
| vendor management and BA analysis | administrative safeguards and related contract requirements |
| physical safeguards | physical safeguards |
| periodic evaluation and reassessment | administrative safeguards |

## PRS stage emphasis

- PRS-1 emphasizes foundational technical safeguards and basic governance prerequisites.
- PRS-2 adds the administrative and process maturity needed to support a defensible approval decision.
- PRS-3 adds explicit authorization, defined scope, and required contracting.
- PRS-4 adds live operational evidence and ongoing evaluation.

## Assessment rule

When a domain is relevant to the scoped workload, do not allow a strong technical showing to offset missing administrative, physical, approval, or operational evidence.

If a reviewer needs to distinguish HIPAA baseline from a stricter PRS readiness bar, make that distinction explicitly and cite the detailed crosswalk.
