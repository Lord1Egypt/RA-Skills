## Description:

Web Slide helps an agent turn user-provided material and style preferences into interactive HTML slide decks that can be opened directly in a browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balancegsr](https://clawhub.ai/user/balancegsr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and presentation authors use this skill to guide an agent through content collection, outline creation, visual theme selection, and browser-ready HTML slide generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read supplied materials and incorporate their contents into generated slides.

Mitigation: Use it only with documents you intend to use for slide generation, and avoid confidential inputs unless that use is approved.

Risk: The skill launches a temporary localhost theme picker and reads a theme choice file.

Mitigation: Validate selected theme IDs against the documented theme list before using them.

Risk: Slides that use chart or advanced animation components may load libraries from CDNs.

Mitigation: Review external dependency use before presenting in restricted or offline environments.

## Reference(s):

- [README](README.md)
- [Slide Generation Guidelines](references/guidelines.md)
- [HTML Slide Base](references/base.html)
- [Theme Picker](references/theme-picker.html)
- [Chart.js Component Reference](references/components/chart-js.html)
- [SVG Chart Component Reference](references/components/chart-svg.html)
- [GSAP Animation Recipes](references/components/gsap-recipes.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance plus generated HTML, CSS, and JavaScript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or edit local HTML slide files and may reference CDN-hosted chart or animation libraries when those components are used.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
