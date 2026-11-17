## Description:

MOSES Governance is a constitutional governance harness for AI agents that applies modes, postures, role ordering, audit logging, lineage checks, signing gates, and commitment verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a governance layer around agent actions, including policy checks, role and posture controls, local audit trails, and optional signing or review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer later agent behavior and write persistent local governance audit or state files.

Mitigation: Install only after reviewing the governance behavior, and monitor or restrict the configured local state directories.

Risk: Optional witness and referee features can post governance data to external endpoints.

Mitigation: Keep witness and referee features disabled unless the endpoint, key handling, and exact payloads have been reviewed.

Risk: MOSES_OPERATOR_SECRET is a sensitive signing or attestation secret.

Mitigation: Set the secret only for specific signing or attestation workflows, and avoid keeping it in a general agent environment.

Risk: The security evidence flags incomplete advertised approval and signature guarantees.

Mitigation: Treat approval and signature claims as incomplete until the HMAC and headless-approval issues identified by the scanner are fixed.

## Reference(s):

- [Moses Governance ClawHub Page](https://clawhub.ai/sunrisesillneversee/skills/moses-governance)
- [MOSES Live Demo](https://mos2es.io)
- [Zenodo Record 18792459](https://zenodo.org/records/18792459)
- [Lattice Governance Model](references/lattice-governance.md)
- [Governance Modes Reference](references/modes.md)
- [Posture Controls Reference](references/postures.md)
- [Role Hierarchy Reference](references/roles.md)
- [Ghost Token Specification](references/ghost-token-spec.md)
- [Falsifiability Reference](references/falsifiability.md)
- [Shannon Extension](references/shannon-extension.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown instructions with CLI command examples and governance configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local governance state and audit files when its bundled scripts are run.]

## Skill Version(s):

0.5.10 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
