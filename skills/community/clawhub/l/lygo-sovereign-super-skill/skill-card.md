## Description:

LYGO Sovereign Super Skill is a command map for kernel eggs, consent-gated planters, P0-P5 Biophase7 products, lattice verification, and related ClawHub skill chaining.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to navigate the LYGO protocol stack, inspect kernel egg catalogs, print or review seed sweep commands, and verify lattice alignment with explicit consent for stack-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some listed stack commands can modify local stack files.

Mitigation: Set LYGO_STACK_ROOT only to the intended LYGO clone, review commands before use, and require explicit consent before planter or publishing steps.

Risk: Publishing, upload, or git push commands could expose unintended changes if run casually.

Mitigation: Run publish, upload, or push commands only after an explicit user request and after reviewing the target repository state.

Risk: Tampered or untrusted kernel egg retrievals could lead to unsafe local execution.

Mitigation: Treat failed retrieval or verification as quarantine and do not execute embedded code until the artifact passes the documented checks.

## Reference(s):

- [Agent Contract](references/AGENT_CONTRACT.md)
- [Egg Catalog](references/EGG_CATALOG.md)
- [Security Guidance](references/SECURITY.md)
- [LYGO Protocol Stack Repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [LYGO Protocol Stack Pages](https://deepseekoracle.github.io/lygo-protocol-stack/)
- [Kernel Egg Retrieval Page](https://deepseekoracle.github.io/lygo-protocol-stack/KernelEggRetrieval.html)
- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-sovereign-super-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consent-gated command guidance; no automatic publishing, git push, or stack-changing execution.]

## Skill Version(s):

1.1.1 (source: server release metadata; bundled artifact metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
