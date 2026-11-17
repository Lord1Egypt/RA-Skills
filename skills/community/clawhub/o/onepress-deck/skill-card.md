## Description:

Builds slide decks from topics or documents as local HTML presentations, with optional OnePress-connected research, images, and PDF/PPTX export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getonepress](https://clawhub.ai/user/getonepress)

### License/Terms of Use:

MIT

## Use Case:

People creating pitch decks, lessons, research briefings, and other presentations can generate a ready-to-present local HTML deck or use OnePress for cited research and export options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected mode sends prompts and uploaded documents to OnePress.

Mitigation: Use local mode for private drafts; connect only when the material is appropriate to share with OnePress.

Risk: An exposed OnePress API key could allow unauthorized access.

Mitigation: Store ONEPRESS_API_KEY in an environment or secret store, never in chat or logs.

Risk: Local drafts may contain numbers that have not been verified live.

Mitigation: Verify figures before presenting and label unverified numbers as not verified live.

## Reference(s):

- [OnePress Deck on ClawHub](https://clawhub.ai/getonepress/skills/onepress-deck)
- [Local Deck Recipe](artifact/LOCAL-RECIPE.md)
- [OnePress](https://www.getonepress.com)

## Skill Output:

**Output Type(s):** [Code, Files, Guidance]

**Output Format:** [Self-contained HTML slide deck locally; downloadable presentation files or deck link in connected mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PDF and PPTX export, cited research, and generated imagery require a OnePress connection.]

## Skill Version(s):

3.1.4 (source: frontmatter, CHANGELOG, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
