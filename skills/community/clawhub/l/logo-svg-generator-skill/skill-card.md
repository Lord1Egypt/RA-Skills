## Description:

Generates multi-size SVG logo sets from natural-language product briefs using Simple Icons design rules and an iterative visual review loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samonysh](https://clawhub.ai/user/samonysh)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, developers, and product teams use this skill to turn a product brief into a symbol-only SVG logo set with monochrome and brand-color variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates local files under output folders.

Mitigation: Run it in the intended workspace and review generated SVG, PNG, favicon, and metadata files before using or publishing them.

Risk: The inspected artifact describes Python helper scripts that were not present as executable files.

Mitigation: Review any future script files before execution, especially CDN fetching or deployment helpers.

Risk: Logo quality depends on an actual vision review unless the user knowingly chooses structural-only checking.

Mitigation: Use a vision-capable model for the review loop, or clearly label structural-only results for human visual review before shipping.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samonysh/skills/logo-svg-generator-skill)
- [Source repository](https://github.com/samonysh/logo-svg-generator-skill)
- [Simple Icons](https://simpleicons.org/)
- [Simple Icons contributing guidelines](https://github.com/simple-icons/simple-icons/blob/develop/CONTRIBUTING.md)
- [Simple Icons slug guidelines](https://github.com/simple-icons/simple-icons/blob/develop/slugs.md)
- [Design rules](references/design-rules.md)
- [Motif patterns](references/motif-patterns.md)
- [Sample icons](references/sample-icons.md)
- [Visual review prompt](assets/templates/visual-review-prompt.md)
- [Concept brief template](assets/templates/concept-brief-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with SVG, PNG, ICO, and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a 24x24 master SVG, multi-size monochrome and brand-color variants, raster previews, favicon assets, brand metadata, and review notes when available.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 0.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
