## Description:

Turn a one-line idea into a clickable, demo-ready PRD that combines structured requirements text with a single-file interactive HTML prototype.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yrainy9321](https://clawhub.ai/user/yrainy9321)

### License/Terms of Use:

MIT

## Use Case:

Product managers, founders, business stakeholders, and builders use this skill to turn incomplete product ideas into review-ready PRDs with clickable HTML prototypes, interaction notes, and optional static-site sharing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prototypes are active HTML and may include script-bearing behavior.

Mitigation: Review or edit generated HTML before opening content from untrusted requirements or publishing it.

Risk: The skill documentation describes the package as script-free, while the generated HTML can contain active scripts.

Mitigation: Treat generated pages as executable HTML rather than inert documents during review and sharing.

Risk: Optional browser verification dependencies can affect the local environment if installed loosely.

Mitigation: Use pinned dependencies or an isolated environment for optional Playwright verification.

Risk: The default QQ author chip may be inappropriate in user deliverables.

Mitigation: Remove or replace the default author chip when it should not appear in the final PRD or prototype.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yrainy9321/skills/prd-html-prototype)
- [Product methodology reference](references/product-methodology.md)
- [PRD structure reference](references/prd-structure.md)
- [Onboarding reference](references/ONBOARDING.md)
- [Static hosting deployment reference](references/deploy-github-pages.md)
- [Full interactive example](references/example-full.html)
- [Single-file PRD prototype template](assets/prd-template.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance plus generated single-file HTML prototype code and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce active script-bearing HTML for local preview or static hosting.]

## Skill Version(s):

1.4.0 (source: frontmatter, _meta.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
