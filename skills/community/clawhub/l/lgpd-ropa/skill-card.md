## Description:

Generate and maintain the Registro de Operações de Tratamento de Dados Pessoais (ROPA) required by LGPD Art. 37, supporting both standard controllers/operators and the simplified ANPD model for ATPP (Resolução CD/ANPD nº 2/2022 Art. 9). Consolidates data mapping, legal bases, DPO/ATPP channel, vendors, transfers, security, and retention into `.lgpd/ROPA.md`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goul4rt](https://clawhub.ai/user/goul4rt)

### License/Terms of Use:

MIT-0

## Use Case:

Privacy, data protection, and legal teams can use this skill to consolidate processing activities into an LGPD ROPA in `.lgpd/ROPA.md`, using either the simplified ATPP model or a more complete model. The Encarregado or legal responsible person reviews the draft before publication.

### Deployment Geography for Use:

Brazil

## Known Risks and Mitigations:

Risk: The security review did not cover some referenced local paths that were absent from the bundle.

Mitigation: Review the companion `.lgpd` files and any referenced materials that are needed before relying on the skill.

Risk: A draft ROPA may contain incomplete or inaccurate processing details.

Mitigation: Have the Encarregado or legal responsible person validate the ROPA before marking it as published.

## Reference(s):

- [Server-resolved source repository and skill path](https://github.com/goul4rt/lgpd-skills/tree/main/skills/lgpd-ropa)
- [ClawHub skill page](https://clawhub.ai/goul4rt/skills/lgpd-ropa)
- [ROPA template](assets/ropa-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown ROPA document and workflow/status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consolidates supplied processing records into `.lgpd/ROPA.md`; requires review by the Encarregado or legal responsible person before publication.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
