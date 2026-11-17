## Description:

Transforms a user's Chinese talk script into a minimalist, Steve Jobs-style vertical HTML presentation with a refined manuscript, slide outline, and runnable HTML output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhj7860](https://clawhub.ai/user/zhj7860)

### License/Terms of Use:


## Use Case:

External users and presentation creators use this skill to turn a prepared talk script into a concise vertical slide deck with a technology-focused minimalist visual style. It is best suited for Chinese-first HTML presentation generation where the final artifact can be opened directly in a browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML presentations may contact third-party CDNs for CSS, fonts, or framework assets when opened.

Mitigation: Review generated HTML before distribution, and inline CSS or replace CDN resources with local assets for sensitive, offline, or restricted presentations.

## Reference(s):

- [Design specification](references/design-spec.md)
- [Slide types](references/slide-types.md)
- [HTML presentation template](assets/template.html)
- [ClawHub skill page](https://clawhub.ai/zhj7860/skills/ppt)

## Skill Output:

**Output Type(s):** [text, markdown, code]

**Output Format:** [Markdown narrative with a slide outline and complete HTML code block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs a single browser-runnable HTML presentation; when slide count is unspecified, the skill defaults to 8-20 vertical slides.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
