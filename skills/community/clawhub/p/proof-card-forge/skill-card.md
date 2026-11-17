## Description:

Generate shareable SVG and Markdown proof cards from a skill audit or release metadata for GitHub READMEs, landing pages, and ClawHub listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to create compact SVG and Markdown proof cards from audit or release metadata for READMEs, landing pages, and ClawHub listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated proof cards can create misleading audit badges if the source audit result is not independently verified.

Mitigation: Review the audit result before publishing and treat generated cards as self-asserted unless the script is hardened to reject do-not-publish audits, invalid schemas, missing authoritative success fields, and conflicting CLI overrides.

## Reference(s):

- [Proof Card Forge on ClawHub](https://clawhub.ai/zack-dev-cm/skills/proof-card-forge)
- [Source Manifest](references/source-manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with file paths, badge snippets, JSON summaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces proof-card SVG, Markdown badge snippet, and optional JSON summary files when invoked with suitable audit or release metadata.]

## Skill Version(s):

0.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
