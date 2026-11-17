## Description:

Generates a one-page model card for an AI system or agent covering identity, purpose, data, limitations, risks, and contact information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI governance teams use this skill to draft a record of an AI system's intended use, data, limitations, risks, and responsible contact for review and archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation describes JSON-RPC input, but the script accepts command-line arguments.

Mitigation: Use the documented CLI flags shown by --help and correct the interface documentation before operational use.

Risk: Permissions metadata says filesystem access is disabled, but --out writes a Markdown file.

Mitigation: Align permissions with actual script behavior and review the output path before writing.

Risk: Generated sections are Chinese-labeled even when the skill is used in English.

Mitigation: Review the generated card for its intended audience or localize the script.

## Reference(s):

- [Model Card Generator on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/model-card-generator)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [Markdown text; optional JSON containing the card data and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save Markdown to a local file; generated section labels are Chinese.]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
