## Description:

Creates and optimizes title tags, meta descriptions, Open Graph tags, and Twitter cards to improve search click-through rates and social sharing previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skullhaven](https://clawhub.ai/user/skullhaven)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users, developers, marketers, and content teams use this skill to create or improve metadata for web pages, including search result snippets and social preview tags. It supports new pages, existing tag optimization, social sharing setup, duplicate or missing tag fixes, and A/B test suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes an optional install-all npx command for a larger skills bundle.

Mitigation: Only run the command after trusting the publisher and verifying or pinning the package version.

Risk: Generated tags may be inappropriate for non-US or non-English pages if locale assumptions are not checked.

Mitigation: Confirm the target language and locale before publishing generated metadata.

Risk: SEO recommendations can create misleading snippets if generated titles or descriptions do not match page content.

Mitigation: Review generated tags against the actual page content and validation checklist before deployment.

## Reference(s):

- [Meta Tag Formulas Reference](artifact/references/meta-tag-formulas.md)
- [Meta Tags Optimizer on ClawHub](https://clawhub.ai/skullhaven/skills/meta-tags-optimizer-2)
- [SEO & GEO Skills Library](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with HTML meta tag code blocks, recommendation tables, rationale, and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated title and description options, complete meta tag blocks, Open Graph and Twitter Card tags, CTR analysis, and A/B test suggestions.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter metadata version is 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
