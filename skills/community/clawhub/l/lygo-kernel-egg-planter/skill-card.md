## Description:

Consent-gated Kernel Egg Planter for SHA-256 and Merkle registry workflows with mandatory post-plant verification, consent-gated retrieval, optional local or Turbo anchoring, and no automatic publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and operators use this skill to prepare, verify, anchor, and retrieve LYGO kernel egg registry artifacts from a trusted LYGO stack under explicit consent. It is intended for local-first workflows where external anchoring and publishing remain separate, opt-in actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run Python tools from a user-selected LYGO_STACK_ROOT, so an untrusted stack root may execute untrusted code.

Mitigation: Use only a LYGO stack repository you control and trust, require the explicit trust marker, and run preflight before planting or retrieving.

Risk: Optional external anchoring can send data to external or persistent surfaces.

Mitigation: Prefer local-only operation and use external anchoring only after confirming the payload contains no private or secret data.

Risk: The security verdict is suspicious and cites consent and safety-check mismatches that require user review.

Mitigation: Review the security guidance before installation, require explicit consent, verify before retrieval, and do not bypass force or skip-verify protections.

Risk: The smoke test can list registry contents as part of its verification flow.

Mitigation: Avoid running smoke_test.py unless listing registry contents is acceptable for the environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-kernel-egg-planter)
- [Publisher profile](https://clawhub.ai/user/deepseekoracle)
- [GitHub link from skill metadata](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [Kernel egg tamper logic](https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/KERNEL_EGG_TAMPER_LOGIC.md)
- [Kernel Egg Retrieval](https://deepseekoracle.github.io/lygo-protocol-stack/KernelEggRetrieval.html)
- [Agent contract](references/AGENT_CONTRACT.md)
- [Consent and ethics](references/CONSENT_AND_ETHICS.md)
- [SkillSpector audit response](references/SKILLSPECTOR_AUDIT.md)
- [Legal, honest planting surfaces](references/SURFACES.md)
- [Four pillars](references/TAMPER_FOUR_PILLARS.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented artifact references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local-first operational guidance for preflight, consent, planting, verification, optional anchoring, and retrieval.]

## Skill Version(s):

1.3.1 (source: server release, claw.json, and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
