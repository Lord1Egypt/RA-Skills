## Description:

Generates ready-to-publish Gumroad product page markdown from structured product specifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn structured product details into Gumroad sales page copy in Markdown, including category-based disclaimers for financial, investment, health, or general products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated public product copy for financial, investment, tax, or health products can omit required context or create misleading regulated claims.

Mitigation: Review regulated claims before publication and do not suppress disclaimers for financial, investment, tax, or health product pages.

Risk: The artifact appears incomplete because the README references scripts and template data that are not present in the shipped files.

Mitigation: Verify required implementation files before relying on command examples, and treat this release as a copy-generation aid unless the missing files are supplied.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/skills/gumroad-page-gen-dv)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown sales page copy generated from structured product input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include category-specific disclaimer text; regulated financial, investment, tax, or health claims still require review before publication.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
