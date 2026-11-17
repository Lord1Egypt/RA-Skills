## Description:

Generates runnable Gin SSR page templates from Figma page screenshots, producing static HTML and CSS with complete page structure, SEO metadata, and a final response containing generated file paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasper-zzq](https://clawhub.ai/user/jasper-zzq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold Chinese-language Gin SSR frontend pages from Figma screenshots. It is intended to create project-ready HTML and CSS files that can be reviewed, previewed, and committed into a Gin application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pages may include hardcoded SEO metadata, language settings, placeholder URLs, and page content.

Mitigation: Review and replace generated metadata, links, verification placeholders, and visible copy before committing or deploying.

Risk: Screenshot-based reconstruction may misread layout or text from the provided Figma image.

Mitigation: Compare the generated HTML and CSS against the source screenshot and correct structure, spacing, and copy before use.

Risk: The skill writes project files under Gin template and static asset paths.

Mitigation: Inspect file paths and diffs before accepting the generated files into an existing application.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasper-zzq/skills/gin-ssr-template)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown response with generated HTML and CSS file paths, plus project files written to the workspace]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces app/templates/page/{page_name}.html and app/static/css/{page_name}.css; Telegram sessions also include MEDIA attachment lines.]

## Skill Version(s):

0.0.14 (source: ClawHub release evidence, created 2026-03-20T15:17:19Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
