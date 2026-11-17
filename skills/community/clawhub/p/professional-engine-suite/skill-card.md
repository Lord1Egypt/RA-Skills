## Description:

A professional reasoning suite that structures auditable, confidence-labeled analysis across medicine, investment, law, engineering, and shared decision-making tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Professionals and developers use the skill to structure and cross-check evidence reviews, financial valuations, legal rule analyses, and engineering derivations or proofs. Its reports document assumptions, confidence, and reasons for declining unsupported requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python helpers can execute user-supplied modules locally.

Mitigation: Run helpers only on trusted files or inside a sandbox; review before installing.

Risk: Medical, legal, and investment analysis may be mistaken for professional advice.

Mitigation: Treat reports as structured analysis aids and have qualified professionals verify conclusions before decisions.

Risk: User-added reference material can change subsequent high-stakes analyses.

Mitigation: Restrict and review additions to reference material before relying on later outputs.

## Reference(s):

- [Professional-Engine Suite on ClawHub](https://clawhub.ai/wangjiaocheng/skills/professional-engine-suite)
- [Professional-Engine Suite catalog](artifact/references/professional-engine-suite-catalog.md)
- [Professional-Engine Suite requirements](artifact/references/professional-engine-suite-requirements.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown reports, calculations, and out-of-domain responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes assumptions, evidence references, confidence labels, and verification results when applicable.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
