## Description:

Professional legal workflows via HaoLvShi APIs for consultation reports, compensation calculators, contract review, complaints and answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtcto](https://clawhub.ai/user/mtcto)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and legal-service agents use this skill to collect case facts, route legal workflows, review contracts, calculate compensation or social-insurance benefits, and deliver HaoLvShi report or Word-document links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive legal facts, contracts, uploaded case materials, and generated report links may be sent to external HaoLvShi services.

Mitigation: Use the skill only when the user accepts HaoLvShi handling those materials, and avoid highly sensitive matters unless the user is comfortable with the service's privacy and retention practices.

Risk: The skill has broad implicit invocation for legal questions and can automatically open generated online report links.

Mitigation: Confirm the active legal workflow and use only current-session evidence before invoking it; present generated links clearly so the user can review the destination.

Risk: The security verdict is suspicious because of external-service data handling and automatic report-link behavior.

Mitigation: Review or pin the installer source and verify the zip or checksum when available before deployment.

## Reference(s):

- [HaoLvShi skill homepage](https://skills.ai.lvpin100.com)
- [ClawHub skill page](https://clawhub.ai/mtcto/skills/haolvshi-legal-skill)
- [Installation guide](https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/INSTALL.md)
- [Interaction workflow reference](references/interaction.md)
- [Legal consultation workflow reference](references/consultation.md)
- [Calculator workflow reference](references/calculator.md)
- [Contract review workflow reference](references/contract-review.md)
- [Pleading workflow reference](references/pleading.md)
- [Case materials workflow reference](references/case-materials.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with report or Word-document links, plus JSON returned by local workflow scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are grounded in the HaoLvShi workflow result for the current session and may include generated online report links.]

## Skill Version(s):

1.17.0 (source: server release metadata; artifact frontmatter and package.json report 1.17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
